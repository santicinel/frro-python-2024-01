"""Base de Datos SQL - Búsqueda"""

import datetime
import sqlite3
from ejercicio_01 import reset_tabla
from ejercicio_02 import agregar_persona


def buscar_persona(id_persona):
    """Implementar la función buscar_persona, que devuelve el registro de una 
    persona basado en su id. El retorno es una tupla que contiene sus campos: 
    id, nombre, nacimiento, dni y altura. Si no encuentra ningún registro, 
    devuelve False."""
    conn = sqlite3.connect("basedatos.db")
    curs = conn.cursor() 
    curs.execute("SELECT * FROM persona WHERE IdPersona=?", (id_persona,))
    persona = curs.fetchone()
    
    conn.close()
    
    if persona:
        
        return persona
    else:
        return False
    

# NO MODIFICAR - INICIO
@reset_tabla
def pruebas():
    juan = buscar_persona(agregar_persona('juan perez', datetime.datetime(1988, 5, 15), 32165498, 180))
    assert juan == (1, 'juan perez', datetime.datetime(1988, 5, 15), 32165498, 180)
    assert buscar_persona(12345) is False

if __name__ == '__main__':
    pruebas()
# NO MODIFICAR - FIN
