from flask import Blueprint, render_template, request, redirect, url_for,flash
from db import Ingreso,Categoria,Gasto
from init import db
from datetime import datetime
from sqlalchemy import extract,func
from sqlalchemy.orm import joinedload
from flask_paginate import Pagination, get_page_parameter


bp=Blueprint('main',__name__)


def get_categorias():
    return db.session.query(Categoria).all()


@bp.route('/')
def index():
  return render_template('index.html',show_login_button=True,show_canvas=False)

@bp.route('/home',methods=['GET'])
def home():
    user_name=request.cookies.get('usuario')
    if not user_name:
      flash(f'Por favor inica sesión','warning')
      return redirect(url_for('index.html'))
    
    mes_actual=datetime.now().month
    anio_actual=datetime.now().year

    categorias=get_categorias()

    page=request.args.get(get_page_parameter(),type=int,default=1)
    per_page=5

    ingresos_query=db.session.query(Ingreso).filter(
       Ingreso.user_name == user_name,
       extract('month',Ingreso.fecha_ingreso) == mes_actual,
       extract('year',Ingreso.fecha_ingreso) == anio_actual
    )

    gastos_query=db.session.query(Gasto).options(joinedload(Gasto.categoria)).filter(
       Gasto.user_name == user_name,
       extract('month',Gasto.fecha_gasto) == mes_actual,
       extract('year',Gasto.fecha_gasto) == anio_actual
    )
    
    calculo_total_gastos=total_gastos(gastos_query)
    
    total = ingresos_query.count()

    ingresos= ingresos_query.order_by(Ingreso.fecha_ingreso.desc()).limit(per_page).offset((page-1)* per_page).all()

    gastos=gastos_query.order_by(Gasto.fecha_gasto.desc())

    total_ingresos=calculo_total_ingresos(ingresos_query)

    pagination=Pagination(page=page,total=total,per_page=per_page,record_name='ingresos',css_framework='bootstrap5')

    return render_template('home.html',
                           show_login_button=False, 
                           show_canvas=True,ingresos=ingresos,
                           pagination=pagination,
                           categorias=categorias,
                           gastos = gastos,
                          calculo_total_gastos=calculo_total_gastos,
                          total_ingresos=total_ingresos
                          )

def total_gastos(gastos_query):
   total_gastos=gastos_query.with_entities(func.sum(Gasto.monto)).scalar() or 0

   return total_gastos


def calculo_total_ingresos(ingresos_query):
   total_gastos=ingresos_query.with_entities(func.sum(Ingreso.monto)).scalar() or 0

   return total_gastos
