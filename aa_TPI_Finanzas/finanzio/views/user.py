from flask import Blueprint, request, redirect, url_for, flash,session,render_template
from db import Ingreso,Gasto,Categoria
from init import db
from datetime import datetime
from controllers.reports_data import get_ingresos_gastos_por_mes,obtener_gastos_por_categoria
import plotly.graph_objects as go
from controllers.prediccion import obtener_prediccion_gastos

user_bp=Blueprint('user',__name__)

@user_bp.route('/ingreso',methods=['POST'])
#@jwt_required()
def ingreso_dinero():
    if request.method== 'POST':
            #csrf_token_form=request.form.get('csrf_token')
            #csrf_token_cookie=request.cookies.get('csrf_access_token')
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
    
    return redirect(url_for('main.home'))

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