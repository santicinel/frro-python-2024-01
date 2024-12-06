from db import SessionLocal, Gasto, Categoria
from sqlalchemy import func
from datetime import datetime, timedelta
from controllers.inflacion import obtener_inflacion_mensual


def obtener_prediccion_gastos(user_name, months=1):
    session = SessionLocal()
    current_date = datetime.now()
    start_date = current_date - timedelta(days=30 * months)

    # Consulta los gastos agrupados por categoría
    gastos = session.query(
        Gasto.id_categoria,
        func.sum(Gasto.monto).label('total_gastos')
    ).filter(
        Gasto.user_name == user_name,
        Gasto.fecha_gasto >= start_date
    ).group_by(Gasto.id_categoria).all()

    # Obtener todas las categorías
    categorias = {categoria.id_categoria: categoria.descripcion for categoria in session.query(Categoria).all()}

   
    inflacion = obtener_inflacion_mensual()

    # Calcular predicción
    predicciones = [
        {
            'categoria': categorias[gasto.id_categoria],
            'gasto_actual': gasto.total_gastos,
            'gasto_predicho': gasto.total_gastos * (1 + inflacion / 100)
        }
        for gasto in gastos
    ]

    session.close()
    return predicciones
