from flask import Blueprint, render_template, request, redirect, url_for,flash
from db import Ingreso
from init import db
from datetime import datetime
from sqlalchemy import extract
from flask_paginate import Pagination, get_page_parameter
bp=Blueprint('main',__name__)
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

    page=request.args.get(get_page_parameter(),type=int,default=1)
    per_page=5

    ingresos_query=db.session.query(Ingreso).filter(
       Ingreso.user_name == user_name,
       extract('month',Ingreso.fecha_ingreso) == mes_actual,
       extract('year',Ingreso.fecha_ingreso) == anio_actual
    )

    total = ingresos_query.count()

    ingresos= ingresos_query.order_by(Ingreso.fecha_ingreso.desc()).limit(per_page).offset((page-1)* per_page).all()

    pagination=Pagination(page=page,total=total,per_page=per_page,record_name='ingresos',css_framework='bootstrap5')

    return render_template('home.html',show_login_button=False, show_canvas=True,ingresos=ingresos,pagination=pagination)





