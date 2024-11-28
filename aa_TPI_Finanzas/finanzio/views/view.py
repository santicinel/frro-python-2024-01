from flask import Blueprint, render_template, request, redirect, url_for,flash
from db import Usuario, obtener_sesion
from init import db,bcrypt
from datetime import datetime

bp=Blueprint('main',__name__)
@bp.route('/')
def index():
  return render_template('index.html',show_login_button=True,show_canvas=False)

@bp.route('/home')
def home():
  return render_template('home.html',show_login_button=False, show_canvas=True)





