from sqlalchemy import Column, Double, ForeignKey, Integer, String, Date, column, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:admin@localhost:3306/finanzio_db"
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

    user_name = Column(String(250), primary_key=True)
    dni = Column(Integer, unique=True, nullable=False)
    nombre = Column(String(250), nullable=False)
    apellido = Column(String(250), nullable=False)
    contraseña = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    fecha_registro = Column(Date, nullable=False)

    # Un usuario puede tener 0 o muchos ingresos y gastos
    ingresos = relationship("Ingreso", back_populates="usuario")
    gastos_mensuales = relationship('GastoMensual', back_populates='usuario')
    gastos = relationship('Gasto', back_populates='usuario')  # Relación corregida aquí


class Gasto(Base):
    __tablename__ = 'gastos'

    id_gasto = Column(Integer, primary_key=True, autoincrement=True)
    fecha_gasto = Column(Date, nullable=False)
    monto = Column(Double, nullable=False)
    descripcion = Column(String(250), nullable=False)
    tipo = Column(String(250), nullable=False)

    # Un gasto tiene una única categoría
    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'))
    categoria = relationship('Categoria', back_populates='gastos')

    # Un gasto pertenece a un usuario
    user_name = Column(String(250), ForeignKey('usuarios.user_name'))
    usuario = relationship("Usuario", back_populates="gastos")
class Ingreso(Base):
    __tablename__ = 'ingresos'

    id_ingreso = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(Date, nullable=False)
    monto = Column(Double, nullable=False)
    descripcion = Column(String(250), nullable=False)

    # Un ingreso pertenece a un usuario
    user_name = Column(String(250), ForeignKey('usuarios.user_name'), nullable=False)
    usuario = relationship("Usuario", back_populates="ingresos")


class Categoria(Base):
    __tablename__ = 'categorias'

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(250), nullable=False)
    prioridad = Column(Integer, nullable=False)

    # Una categoría puede estar en muchos gastos
    gastos = relationship('Gasto', back_populates='categoria')


class Prediccion(Base):
    __tablename__ = 'predicciones'

    id_prediccion = Column(Integer, primary_key=True, autoincrement=True)
    fecha_predecir = Column(Date, nullable=False)
    gasto_futuro = Column(Double, nullable=False)

    # Referencias al gasto mensual
    id_gasM = Column(Integer, ForeignKey('gastos_mensual.id_gasM'), nullable=False)
    gasto_mensual = relationship('GastoMensual', back_populates='predicciones',)

class GastoMensual(Base):
    __tablename__ = 'gastos_mensual'
    # Llave compuesta que relaciona GastoMensual con Usuario y Gasto
    id_gasM =  Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(250), ForeignKey('usuarios.user_name'),nullable=False)
    id_gasto = Column(Integer, ForeignKey('gastos.id_gasto'),nullable=False)
    # Relaciones
    usuario = relationship("Usuario", back_populates="gastos_mensuales")
    gasto = relationship('Gasto', backref='gasto_mensuales')
    # Relación con Prediccion
    predicciones = relationship('Prediccion', back_populates='gasto_mensual',)


Base.metadata.create_all(bind=engine)
