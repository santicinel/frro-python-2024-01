from flask import Blueprint, render_template, request, redirect, url_for,flash
from db import Usuario, obtener_sesion
from init import db,bcrypt
from datetime import datetime

bp=Blueprint('main',__name__)
@bp.route('/')
def index():
  return render_template('index.html',show_login_button=True,show_canvas=False)

@bp.route('/login')
def login():
  return render_template('login.html',show_login_button=False)

@bp.route('/home')
def home():
  return render_template('home.html',show_login_button=False, show_canvas=True)

@bp.route('/loginuser',methods=['POST'])
def loginuser():
  user_name=request.form['username']
  contraseña=request.form['contraseña']
  with next(obtener_sesion()) as session:
        usuario = session.query(Usuario).filter(Usuario.user_name == user_name).first()
  if usuario and bcrypt.check_password_hash(usuario.contraseña,contraseña):
    return redirect(url_for('main.home'))
  else:
    return redirect(url_for('main.index'))
  

@bp.route('/register')
def register():
  return render_template('register.html')

@bp.route('/newuser',methods=['POST'])
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
        return redirect(url_for('main.index'))
    
    except Exception as e:
      db.session.rollback()
      flash(f'error al registrar: {e}')
      return redirect(url_for('main.register'))
  return redirect(url_for('main.index'))


