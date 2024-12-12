from flask import Blueprint, render_template, request, redirect, url_for, flash,make_response,session
from db import Usuario, obtener_sesion
from init import bcrypt,db
from datetime import datetime
from controllers.forms import RegisterForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/loginuser', methods=['POST'])
def loginuser():
    user_name = request.form['username']
    contraseña = request.form['contraseña']

    if not user_name or not contraseña:
       flash("Debes completar todos los campos","danger")
       return redirect(url_for('auth.login'))
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
        flash("Usuario o contraseña incorrecta","warning")
        return redirect(url_for('auth.login'))
    


@auth_bp.route('/register')
def register():
    form = RegisterForm()  # Instancia del formulario
    return render_template('register.html', form=form)

@auth_bp.route('/newuser',methods=['POST','GET'])
def new_user():
    form = RegisterForm(request.form)  # Instancia del formulario
    if  request.method=='POST' and form.validate():  # Si el formulario se valida correctamente
        try:
            user_name = form.username.data
            dni = form.dni.data
            nombre = form.nombre.data
            apellido = form.apellido.data
            contraseña = form.password.data
            email = form.email.data
            fecha_nacimiento = form.fecha_nacimiento.data
            fecha_registro = datetime.now()

            # Hashear la contraseña
            contraseña_hashed = bcrypt.generate_password_hash(contraseña).decode('UTF-8')

            # Crear una nueva instancia de Usuario
            nuevo_usuario = Usuario(
                user_name=user_name,
                dni=dni,
                nombre=nombre,
                apellido=apellido,
                contraseña=contraseña_hashed,
                email=email,
                fecha_nacimiento=fecha_nacimiento,
                fecha_registro=fecha_registro
            )

            # Agregar a la base de datos
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado correctamente', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el usuario: {str(e)}', 'danger')

    return render_template('register.html', form=form)

@auth_bp.route("/logout")
def logout():
    session.clear()  # Elimina toda la información de la sesión
    return redirect(url_for('main.index'))