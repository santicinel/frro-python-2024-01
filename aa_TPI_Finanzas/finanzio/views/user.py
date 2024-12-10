from flask import Blueprint, request, redirect, url_for, flash,session,render_template
from db import Ingreso,Gasto,Categoria
from init import db
from datetime import datetime
from controllers.reports_data import get_ingresos_gastos_por_mes,obtener_gastos_por_categoria
import plotly.graph_objects as go
from controllers.prediccion import obtener_prediccion_gastos
from db import obtener_sesion
from sqlalchemy.orm import Session
from controllers.helpers import obtener_tipos_gasto
from views.view import total_gastos, calculo_total_ingresos,get_categorias
from sqlalchemy import extract

user_bp=Blueprint('user',__name__)

@user_bp.route('/ingreso',methods=['POST'])
#@jwt_required()
def ingreso_dinero():
    if request.method== 'POST':
        user_name=request.cookies.get('usuario')
        monto=request.form['monto']
        descripcion=request.form['descripcion']
        fecha_ingreso=datetime.now()
        nuevo_ingreso=Ingreso(
            fecha_ingreso=fecha_ingreso,
            monto=monto,
            descripcion=descripcion,
            user_name=user_name   
        )

        try:
            db.session.add(nuevo_ingreso)
            db.session.commit()
            flash('Ingreso agregado correctamente','success')

            return redirect(url_for('main.home'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al ingreso : {e}','danger')
            return redirect(url_for('main.home'))
    return redirect(url_for('main.home'))

@user_bp.route('/ingresogasto',methods=['POST'])
def ingreso_gasto():
    tipos_gasto=obtener_tipos_gasto()
    if request.method== 'POST':         
        user_name=request.cookies.get('usuario')
        monto=request.form.get('gasto')
        id_categoria=request.form.get('id_categoria')
        descripcion=request.form.get('descripcion')
        fecha_gasto=datetime.now()
        
        if not id_categoria or not monto or not descripcion:
            flash("Todos los campos deben ser completados","error")
            return redirect(url_for('main.home'))
        

        nuevo_gasto=Gasto(

            fecha_gasto=fecha_gasto,
            monto=float(monto),
            descripcion=descripcion,
            id_categoria=int(id_categoria),
            tipo=request.form.get('tipo'),
            user_name=user_name
        )

        try:
            db.session.add(nuevo_gasto)
            db.session.commit()
            flash("Gasto agregado correctamente","success")
            return redirect(url_for('main.home'))
        except Exception as e:
            flash(f"Error al agregar el gasto:{str(e)}","error")
            return redirect(url_for('main.home'))
    
    return render_template('home.html',tipos_gasto=tipos_gasto)

@user_bp.route('/reports', methods=['GET'])
def reports():
    user_name = request.cookies.get('usuario')
    if not user_name:
        flash('Por favor inicia sesión', 'warning')
        return redirect(url_for('auth.login'))
    
    ingresos_por_mes, gastos_por_mes = get_ingresos_gastos_por_mes(user_name)

    # Combinar los resultados de ingresos y gastos
    datos_por_mes = {}
    for ingreso in ingresos_por_mes:
        año_mes = f"{int(ingreso.año)}-{int(ingreso.mes):02d}"
        datos_por_mes[año_mes] = {'ingresos': ingreso.total_ingresos, 'gastos': 0}

    for gasto in gastos_por_mes:
        año_mes = f"{int(gasto.año)}-{int(gasto.mes):02d}"
        if año_mes not in datos_por_mes:
            datos_por_mes[año_mes] = {'ingresos': 0, 'gastos': gasto.total_gastos}
        else:
            datos_por_mes[año_mes]['gastos'] = gasto.total_gastos

    # Preparar datos para el gráfico
    labels = sorted(datos_por_mes.keys())
    ingresos_data = [datos_por_mes[label]['ingresos'] for label in labels]
    gastos_data = [datos_por_mes[label]['gastos'] for label in labels]

    # Crear gráfico
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=labels,
        y=ingresos_data,
        name='Ingresos',
        marker_color='green'
    ))

    fig.add_trace(go.Bar(
        x=labels,
        y=gastos_data,
        name='Gastos',
        marker_color='red'
    ))

    fig.update_layout(
        title='Ingresos vs Gastos por Mes',
        xaxis_title='Mes',
        yaxis_title='Monto',
        barmode='group',
        template='plotly_white'
    )

    graph_html = fig.to_html(full_html=False)

    gastos_categoria = obtener_gastos_por_categoria(user_name, months=6)  # Últimos 6 meses

    # Datos para el gráfico de torta
    labels_categoria = [gasto['categoria'] for gasto in gastos_categoria]
    values_categoria = [gasto['total_gastos'] for gasto in gastos_categoria]

    # Crear gráfico de torta para Distribución de Gastos por Categoría
    fig2 = go.Figure(data=[go.Pie(labels=labels_categoria, values=values_categoria, hole=0.3)])

    fig2.update_layout(
        title='Distribución de Gastos por Categoría',
        template='plotly_white'
    )

    # Convertir el gráfico de torta a HTML
    graph_html2 = fig2.to_html(full_html=False)

    return render_template('reports.html',
                           show_login_button=False,
                           show_canvas=True,
                           graph_html=graph_html,
                           graph_html2=graph_html2)

@user_bp.route('/prediccion',methods=['GET'])
def prediccion():
    user_name=request.cookies.get('usuario')
    predicciones=obtener_prediccion_gastos(user_name)
    categorias = [p['categoria'] for p in predicciones]
    gastos_actuales = [p['gasto_actual'] for p in predicciones]
    gastos_predichos = [p['gasto_predicho'] for p in predicciones]

    fig=go.Figure()

    fig.add_trace(go.Bar(
        x=categorias,
        y=gastos_actuales,
        name='Gasto actual',
        marker=dict(color='blue',opacity=0.6)
    ))

    fig.add_trace(go.Bar(
        x=categorias,
        y=gastos_predichos,
        name='Gastos predichos',
        marker=dict(color='orange',opacity=0.6)
    ))

    fig.update_layout(
        title='Predicción de gastos por categoría',
        xaxis_title='Categorias',
        yaxis_title='Montos($)',
        barmode='group'
    )

    graph_html = fig.to_html(full_html=False)

    return render_template('prediccion.html', graph_html=graph_html,show_canvas=True)


@user_bp.route('/editargasto/<int:id>',methods=['GET','POST'])
def editar_gasto(id):
    gasto = db.session.query(Gasto).filter_by(id_gasto=id).first()
    categorias = db.session.query(Categoria).all()
    if not gasto:
        flash("No se encontró el gasto.", "error")
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        # Actualizar los datos del gasto
        gasto.monto = request.form.get('monto')
        gasto.descripcion = request.form.get('descripcion')

        id_categoria = request.form.get('id_categoria')
        categoria_seleccionada=db.session.query(Categoria).filter_by(id_categoria=id_categoria).first()
        
        if categoria_seleccionada:
            gasto.categoria=categoria_seleccionada

        db.session.commit()
        flash("El gasto se ha actualizado correctamente", "success")
        return redirect(url_for('main.home'))

    tipos_gastos = obtener_tipos_gasto()
    return render_template('editargasto.html',
                           show_canvas=True,
                           show_login_button=False,
                           gasto=gasto,
                           categorias=categorias,
                           tipos_gastos=tipos_gastos,)


@user_bp.route('/eliminar_gasto/<int:id_gasto>', methods=['POST'])
def eliminar_gasto(id_gasto):
    session: Session = next(obtener_sesion())  # Obtén la sesión
    gasto = session.query(Gasto).filter(Gasto.id_gasto == id_gasto).first()
    if gasto:
        session.delete(gasto)
        session.commit()
        return redirect(url_for('main.home'))
    else:
        return "El gasto no existe", 404