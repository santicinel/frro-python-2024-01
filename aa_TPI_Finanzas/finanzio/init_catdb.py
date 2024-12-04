import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db import Categoria, Base
import os
from dotenv import load_dotenv
load_dotenv()

engine= create_engine(os.getenv('DATABASE_URL'))
SessionLocal=sessionmaker(bind=engine)

def ini_cat():
  session = SessionLocal()
  try:

    with open ("categorias.json","r") as archivo:
      categorias = json.load(archivo)

      for categoria in categorias :
        existe = session.query(Categoria).filter_by(descripcion=categoria["descripcion"]).first()

        if not existe:
          nueva_categoria = Categoria(
            descripcion=categoria["descripcion"],
            prioridad=categoria["prioridad"]
          )

          session.add(nueva_categoria)

    session.commit()

  except Exception as e:
    session.rollback()
    print(f'Error en categorias: {e}')

  finally:
    session.close()


if __name__ == "__main__":
  Base.metadata.create_all(bind=engine)
  ini_cat()