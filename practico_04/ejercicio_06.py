"""Base de Datos SQL - Creación de tablas auxiliares"""

from ejercicio_01 import borrar_tabla, crear_tabla
import sqlite3

def crear_tabla_peso():
    """Implementar la funcion crear_tabla_peso, que cree una tabla PersonaPeso con:
        - IdPersona: Int() (Clave Foranea Persona)
        - Fecha: Date()
        - Peso: Int()
    """
    db=sqlite3.connect("basedatos.db")
    cur=db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS personaPeso(IdPersona INT , fecha DATE, peso INT, CONSTRAINT fk_persona FOREIGN KEY (IdPersona) REFERENCES persona(IdPersona))")
    db.commit()
    db.close()

def borrar_tabla_peso():
    """Implementar la funcion borrar_tabla, que borra la tabla creada 
    anteriormente."""
    db=sqlite3.connect("basedatos.db")
    cur=db.cursor()
    cur.execute("DROP TABLE personaPeso")
    db.commit()
    db.close()


# NO MODIFICAR - INICIO
def reset_tabla(func):
    def func_wrapper():
        crear_tabla()
        crear_tabla_peso()
        func()
        borrar_tabla_peso()
        borrar_tabla()
    return func_wrapper
# NO MODIFICAR - FIN
