from sqlalchemy.sql import func
from sqlalchemy import and_ 
from db import Usuario, Gasto,Categoria,SessionLocal,Ingreso
def comparar_gastos(user_name):
    session = SessionLocal()

    subquery_ingresos = (
        session.query(
            Ingreso.user_name,
            func.sum(Ingreso.monto).label("ingreso_total")
        )
        .group_by(Ingreso.user_name)
        .subquery()
    )

    ingreso_usuario = (
        session.query(subquery_ingresos.c.ingreso_total)
        .filter(subquery_ingresos.c.user_name == user_name)
        .scalar()
    )

    if ingreso_usuario is None:
        raise ValueError("El usuario no tiene ingresos registrados.")

    rango_min = ingreso_usuario * 0.8
    rango_max = ingreso_usuario * 1.2

    subquery_promedios = (
        session.query(
            Gasto.id_categoria,
            func.avg(Gasto.monto).label("promedio_categoria")
        )
        .join(Usuario, Usuario.user_name == Gasto.user_name)
        .join(subquery_ingresos, subquery_ingresos.c.user_name == Usuario.user_name)
        .filter(
            and_(
                subquery_ingresos.c.ingreso_total >= rango_min,
                subquery_ingresos.c.ingreso_total <= rango_max
            )
        )
        .group_by(Gasto.id_categoria)
        .subquery()
    )

    subquery_gastos_usuario = (
        session.query(
            Gasto.id_categoria,
            func.sum(Gasto.monto).label("gasto_total_usuario")
        )
        .filter(Gasto.user_name == user_name)
        .group_by(Gasto.id_categoria)
        .subquery()
    )

    resultados = (
        session.query(
            Categoria.descripcion.label("categoria"),
            subquery_gastos_usuario.c.gasto_total_usuario.label("gasto_usuario"),
            subquery_promedios.c.promedio_categoria
        )
        .join(subquery_gastos_usuario, subquery_gastos_usuario.c.id_categoria == Categoria.id_categoria)
        .outerjoin(subquery_promedios, subquery_promedios.c.id_categoria == Categoria.id_categoria)
        .all()
    )

    resultado_final = []
    for row in resultados:
        if row.promedio_categoria is not None:
            estado = "por encima" if row.gasto_usuario > row.promedio_categoria else "por debajo"
            resultado_final.append({
                "categoria": row.categoria,
                "gasto_usuario": row.gasto_usuario,
                "promedio_categoria": row.promedio_categoria,
                "estado": estado
            })

    session.close()
    return resultado_final


