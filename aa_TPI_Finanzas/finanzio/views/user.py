from flask import Blueprint, request, redirect, url_for, flash,jsonify,abort,session
from db import Ingreso,Usuario
from init import db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

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
