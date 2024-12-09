from flask import Blueprint, render_template, request, redirect, url_for, flash,make_response,session
from db import Usuario, obtener_sesion
from init import bcrypt,db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/loginuser', methods=['POST'])
def loginuser():
    user_name = request.form['username']
    contraseña = request.form['contraseña']
    with next(obtener_sesion()) as sessionMake:
        usuario = sessionMake.query(Usuario).filter(Usuario.user_name == user_name).first()

    if usuario and bcrypt.check_password_hash(usuario.contraseña, contraseña):
        response=make_response(redirect(url_for('main.home')))
        session["user_id"] = usuario.user_name  # Guarda el ID del usuario en la sesión
        session["user_name"] = usuario.nombre  
        response.set_cookie(
           key='usuario',
           value=user_name,
           httponly=True,
           secure=True,
           samesite='Lax'
        )
        return response
    else:
        flash('Usuario o contraseña incorrecta')
        return redirect(url_for('auth.login'))
    


@auth_bp.route('/register')
def register():
    return render_template('register.html')

@auth_bp.route('/newuser',methods=['POST'])
def new_user():
  if request.method == 'POST':
    user_name=request.form['username']
    dni=request.form['dni']
    nombre=request.form['nombre']
    apellido=request.form['apellido']
    contraseña=request.form['contraseña']
    email=request.form['email']
    fecha_nacimiento=request.form['fecha_nacimiento']
    fecha_registro = datetime.now()

    contraseña_hashed=bcrypt.generate_password_hash(contraseña).decode('UTF-8')
    nuevo_usuario=Usuario(
      user_name=user_name,
      dni=dni,
      nombre=nombre,
      apellido=apellido,
      contraseña=contraseña_hashed,
      email=email,
      fecha_nacimiento=fecha_nacimiento,
      fecha_registro=fecha_registro)
    
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('usuario registrado ')
        return redirect(url_for('auth.login'))
    
    except Exception as e:
      db.session.rollback()
      flash(f'error al registrar: {e}')
      return redirect(url_for('auth.register'))
  return redirect(url_for('main.index'))

@auth_bp.route("/logout")
def logout():
    session.clear()  # Elimina toda la información de la sesión
    return redirect(url_for('main.index'))