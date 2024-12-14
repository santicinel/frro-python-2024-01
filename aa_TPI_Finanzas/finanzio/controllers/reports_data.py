from sqlalchemy import func
from datetime import datetime, timedelta
from db import SessionLocal, Categoria, Gasto


def get_ingresos_gastos_por_mes(user_name):
    from db import SessionLocal, Ingreso, Gasto
    session = SessionLocal()

    ingresos_por_mes = (
        session.query(
            func.extract('year', Ingreso.fecha_ingreso).label('año'),
            func.extract('month', Ingreso.fecha_ingreso).label('mes'),
            func.sum(Ingreso.monto).label('total_ingresos')
        )
        .filter(Ingreso.user_name == user_name)
        .group_by(func.extract('year', Ingreso.fecha_ingreso), func.extract('month', Ingreso.fecha_ingreso))
        .order_by(func.extract('year', Ingreso.fecha_ingreso), func.extract('month', Ingreso.fecha_ingreso))
        .all()
    )

    gastos_por_mes = (
        session.query(
            func.extract('year', Gasto.fecha_gasto).label('año'),
            func.extract('month', Gasto.fecha_gasto).label('mes'),
            func.sum(Gasto.monto).label('total_gastos')
        )
        .filter(Gasto.user_name == user_name)
        .group_by(func.extract('year', Gasto.fecha_gasto), func.extract('month', Gasto.fecha_gasto))
        .order_by(func.extract('year', Gasto.fecha_gasto), func.extract('month', Gasto.fecha_gasto))
        .all()
    )

    session.close()
    return ingresos_por_mes, gastos_por_mes

def obtener_gastos_por_categoria(user_name, months=12):
    session = SessionLocal()
    
    current_date = datetime.now()
    if months == 6:
        start_date = current_date - timedelta(days=180)
    else:
        start_date = datetime(current_date.year, 1, 1)

    gastos = session.query(
        Gasto.id_categoria,
        func.sum(Gasto.monto).label('total_gastos')
    ).filter(
        Gasto.user_name == user_name,
        Gasto.fecha_gasto >= start_date
    ).group_by(Gasto.id_categoria).all()

    categorias = {categoria.id_categoria: categoria.descripcion for categoria in session.query(Categoria).all()}

    gastos_categoria = [
        {'categoria': categorias[gasto.id_categoria], 'total_gastos': gasto.total_gastos}
        for gasto in gastos
    ]

    session.close()
    return gastos_categoria