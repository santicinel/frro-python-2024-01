

from enum import auto
from sqlalchemy import Column, Double, ForeignKey, Integer, String, Date, create_engine
from sqlalchemy.orm import Relationship, relationship, sessionmaker, declarative_base


DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/finanzio_bd"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




def obtener_sesion():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

class Usuario(Base):

    __tablename__ = 'usuarios'

    user_name=Column(String(250),primary_key=True)
    dni=Column(Integer,unique=True,nullable=False)
    nombre=Column(String(250),nullable=False)
    apellido=Column(String(250),nullable=False)
    contraseña=Column(String(250),nullable=False)
    email=Column(String(250),nullable=False)
    fecha_nacimiento=Column(Date,nullable=False)
    fecha_registro=Column(Date,nullable=False)
    

    ingresos = relationship("Ingreso", back_populates="usuarios")
    gastos_mensuales = relationship('GastoMensual', back_populates='usuarios')

class Gasto(Base):

    __tablename__ = 'gastos'

    id_gasto=Column(Integer,nullable=False, primary_key=True, autoincrement=True)
    fecha_gasto=Column(Date,nullable=False)
    monto=Column(Double,nullable=False)
    descripcion=Column(String(250),nullable=False)
    tipo=Column(String(250),nullable=False)

    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'))
    categoria = relationship('Categoria', back_populates='gastos')
    gastos_mensuales = relationship('GastoMensual', back_populates='gastos')

class Ingreso(Base):
    __tablename__ = 'ingresos'
    id_ingreso=Column(Integer,nullable=False, primary_key=True, autoincrement=True)
    fecha_ingreso=Column(Date,nullable=False)
    monto=Column(Double,nullable=False)
    descripcion=Column(String(250),nullable=False)
   

    user_name = Column(String(250), ForeignKey('usuarios.user_name'))

    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="ingresos")
    
class Categoria(Base):

    __tablename__= 'categorias'
    id_categoria=Column(Integer,nullable=False, primary_key=True, autoincrement=True)
    descripcion=Column(String(250),nullable=False)
    prioridad=Column(Integer,nullable=False)


    gastos = relationship('Gasto', back_populates='categorias')

class GastoMensual(Base):

    __tablename__ = 'gastos_mensual'

    user_name = Column(String(250),ForeignKey('usuarios.user_name'),primary_key=True)
    id_gastos = Column(Integer,ForeignKey('gastos.id_gasto'),primary_key=True)
    
    usuario = relationship("Usuario", back_populates="gastos_mensuales")
    gasto = relationship('Gasto', back_populates='gastos_mensuales')
    prediccion = relationship('Prediccion' ,back_populates='gastos_mensuales')


class Prediccion(Base):
    __tablename__ = 'predicciones'

    id_prediccion=Column(Integer,nullable=False, primary_key=True, autoincrement=True)
    fecha_predecir=Column(Date,nullable=False)
    gasto_futuro=Column(Double, nullable=False)

    id_gastos = Column(Integer,ForeignKey('gastos_mensual.id_gastos'))
    user_name = Column(String(250),ForeignKey('gastos_mensual.user_name'))
    gastos_mensuales = relationship('GastoMensual', back_populates='prediccion')


Base.metadata.create_all(bind=engine)
