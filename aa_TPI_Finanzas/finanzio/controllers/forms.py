from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

class RegisterForm(FlaskForm):
  username = StringField('Usuario',validators=[DataRequired(message="El usuario es obligatorio")])
  dni =  StringField('DNI',validators=[DataRequired(message="El DNI es oblitagorio"),Length(min=8,max=8, message='El DNI debe tener 8 Dígitos')])
  nombre= StringField('Nombre',validators=[DataRequired(message="El nombre es obligatorio")])
  apellido= StringField('Apellido',validators=[DataRequired(message="El apellido es obligatorio")])
  email= EmailField('Email',validators=[DataRequired(message="El email es obligatorio"),
                                        Email(message="Por favor, introduzca un email válido")])
  password= PasswordField('Contraseña', validators=[DataRequired(message="La contraseña es obligatoria"),Length(min=6,message="La contraseña debe tener al menos 6 carácteres"),
                                                    ])
  confirm_password=PasswordField('Confirmar contraseña',validators=[DataRequired(message="La confirmación de contraseña es obligatoria"),
                                                                    EqualTo('password',message="Las contraseñas no coinciden")])
  fecha_nacimiento=DateField('Fecha de Nacimiento',validators=[DataRequired(message="La fecha de nacimiento es obligatoria")])

class LoginForm(FlaskForm):
  username=StringField('Usuario',validators=[DataRequired()])
  password=PasswordField('Contraseña',validators=[DataRequired()])
