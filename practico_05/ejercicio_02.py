"""Base de Datos - ORM"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ejercicio_01 import Base, Socio
from typing import List, Optional
from sqlalchemy.orm.exc import UnmappedInstanceError


from typing import List, Optional

class DatosSocio():

    def __init__(self):
        self.__engine=create_engine("sqlite:///prueba.db")
        self.__Session = sessionmaker(bind=self.__engine)
        Base.metadata.create_all(bind = self.__engine)

    def buscar(self, id_socio: int) -> Optional[Socio]:
        """Devuelve la instancia del socio, dado su id. Devuelve None si no 
        encuentra nada.
        """
        sesion=self.__Session()
        socio=sesion.query(Socio).filter(Socio.id_socio==id_socio).first()
        sesion.close()
        return socio

    def buscar_dni(self, dni_socio: int) -> Optional[Socio]:
        """Devuelve la instancia del socio, dado su dni. Devuelve None si no 
        encuentra nada.
        """
        sesion=self.__Session()
        socio=sesion.query(Socio).filter(Socio.dni==dni_socio).first()
        sesion.close()
        return socio
        
    def todos(self) -> List[Socio]:
        """Devuelve listado de todos los socios en la base de datos."""
        sesion=self.__Session()
        socio=sesion.query(Socio).all()
        sesion.close()
        return socio

    def borrar_todos(self) -> bool:
        """Borra todos los socios de la base de datos. Devuelve True si el 
        borrado fue exitoso.
        """
        sesion=self.__Session()
        sesion.query(Socio).delete()
        sesion.commit()
        borrados=sesion.deleted
        sesion.close()
        
        return not bool(borrados)

    def alta(self, socio: Socio) -> Socio:
        """Agrega un nuevo socio a la tabla y lo devuelve"""
        sesion=self.__Session(expire_on_commit=False)
        sesion.add(socio)
        sesion.commit()
        sesion.expunge(socio)
        sesion.close()


    def baja(self, id_socio: int) -> bool:
        """Borra el socio especificado por el id. Devuelve True si el borrado 
        fue exitoso.
        """
        sesion=self.__Session(expire_on_commit=False)
        socio=sesion.query(Socio).filter(Socio.id_socio==id_socio).first()
        if socio:
            sesion.delete(socio)
            sesion.commit()
        else: 
            raise UnmappedInstanceError
        sesion.close()
        return bool(socio)

    def modificacion(self, socio: Socio) -> Socio:
        """Guarda un socio con sus datos modificados. Devuelve el Socio 
        modificado.
        """
        sesion = self.__Session()
        socio_viejo=sesion.query(Socio).filter(Socio.id_socio==socio.id_socio).first()
        if socio_viejo:
            socio_viejo.asignar(socio)
            sesion.commit()
        else:
            raise UnmappedInstanceError
        sesion.close()
        return socio
    
    def contarSocios(self) -> int:
        """Devuelve el total de socios que existen en la tabla"""
        sesion=self.__Session()
        cant_personas=sesion.query(Socio).count()
        sesion.close()
        return cant_personas



# NO MODIFICAR - INICIO

# Test Creación
datos = DatosSocio()

# Test Alta
socio = datos.alta(Socio(dni=1234567, nombre='Juan', apellido='Perez'))
assert socio.id_socio > 0

# Test Baja
assert datos.baja(socio.id_socio) == True

# Test Consulta
socio_2 = datos.alta(Socio(dni=1234567, nombre='Carlos', apellido='Perez'))
assert datos.buscar(socio_2.id) == socio_2

# Test Buscar DNI
socio_2 = datos.alta(Socio(dni=1234567, nombre='Carlos', apellido='Perez'))
assert datos.buscar_dni(socio_2.dni) == socio_2

# Test Modificación
socio_3 = datos.alta(Socio(dni=1234568, nombre='Susana', apellido='Gimenez'))
socio_3.nombre = 'Moria'
socio_3.apellido = 'Casan'
socio_3.dni = 13264587
datos.modificacion(socio_3)
socio_3_modificado = datos.buscar(socio_3.id)
assert socio_3_modificado.id == socio_3.id
assert socio_3_modificado.nombre == 'Moria'
assert socio_3_modificado.apellido == 'Casan'
assert socio_3_modificado.dni == 13264587

# Test Conteo
assert len(datos.todos()) == 3

# Test Delete
datos.borrar_todos()
assert len(datos.todos()) == 0

# NO MODIFICAR - FIN