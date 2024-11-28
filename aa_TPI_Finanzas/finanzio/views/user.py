from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import Ingreso
from init import db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_wtf.csrf import csrf_exempt
user_bp=Blueprint('user',__name__)

@user_bp.route('/ingreso',methods=['POST'])
@csrf_exempt()
@jwt_required()
def ingreso_dinero():
    if request.method== 'POST':
        monto=request.form['monto']
        descripcion=request.form['descripcion']
        fecha_ingreso=datetime.now()
        user_name=get_jwt_identity()

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