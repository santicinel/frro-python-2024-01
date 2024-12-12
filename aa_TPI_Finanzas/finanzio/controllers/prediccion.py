from db import SessionLocal, Gasto, Categoria, Prediccion
from sqlalchemy import func
from datetime import datetime, timedelta
from controllers.inflacion import obtener_inflacion_mensual

def obtener_prediccion_gastos(user_name, months=1):
    session = SessionLocal()
    current_date = datetime.now()

    try:
        # Determinar la fecha para la predicción
        fecha_predecir = current_date + timedelta(days=30 * months)

        # Verificar si ya existe una predicción válida para este usuario y período
        predicciones_existentes = session.query(Prediccion).join(Gasto).filter(
            Gasto.user_name == user_name,
            Prediccion.fecha_predecir == fecha_predecir
        ).all()

        if predicciones_existentes:
            # Si existen predicciones, devolverlas
            predicciones = [
                {
                    'categoria': session.query(Categoria).filter_by(id_categoria=gasto.id_categoria).first().descripcion,
                    'gasto_actual': None,  # Opcional
                    'gasto_predicho': p.gasto_futuro
                }
                for p in predicciones_existentes
                for gasto in session.query(Gasto).filter(Gasto.id_gasto == p.id_gasto)
            ]
            return predicciones

        # Obtener los gastos del usuario agrupados por categoría
        start_date = current_date - timedelta(days=30 * months)
        gastos = session.query(
            Gasto.id_categoria,
            func.sum(Gasto.monto).label('total_gastos')
        ).filter(
            Gasto.user_name == user_name,
            Gasto.fecha_gasto >= start_date,
            Gasto.fecha_gasto <= current_date,  # Solo hasta la fecha actual
            Gasto.tipo.in_(["Ocasional", "Fijo"])
        ).group_by(Gasto.id_categoria).all()

        # Obtener todas las categorías
        categorias = {categoria.id_categoria: categoria.descripcion for categoria in session.query(Categoria).all()}

        # Calcular la inflación mensual
        inflacion = obtener_inflacion_mensual(meses=months)

        predicciones = []
        for gasto in gastos:
            gasto_predicho = gasto.total_gastos * (1 + inflacion / 100)
            predicciones.append({
                'categoria': categorias[gasto.id_categoria],
                'gasto_actual': gasto.total_gastos,
                'gasto_predicho': gasto_predicho
            })

            # Guardar la predicción en la base de datos
            nueva_prediccion = Prediccion(
                fecha_predecir=fecha_predecir,
                gasto_futuro=gasto_predicho,
                id_gasto=None if not gasto.id_categoria else gasto.id_categoria
            )
            session.add(nueva_prediccion)

        session.commit()
        return predicciones

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()
