import requests
from datetime import datetime

# Función para obtener la inflación mensual a partir de la API del BCRA
def obtener_inflacion_mensual(meses):
    id_variable = "29"  # Reemplaza con el ID de la variable de inflación REM
    current_date = datetime.now()
    start_date = current_date.replace(year=current_date.year - 1).strftime('%Y-%m-%d')  # Fecha desde hace un año
    end_date = current_date.strftime('%Y-%m-%d')  # Fecha hasta el día de hoy

    # Formar la URL para obtener los datos de la inflación
    url = f"https://api.bcra.gob.ar/estadisticas/v2.0/DatosVariable/{id_variable}/2024-10-31/2024-10-31"

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        data = response.json()  # Devuelve los datos en formato JSON

        results = data.get('results', [])
        if results:
            # Extraer el valor de inflación del primer resultado
            inflacion_rem = results[0].get('valor', None)
            if inflacion_rem is not None:
                inflacion_mensual = (pow(1 + inflacion_rem / 100, 1 / 12) - 1) * 100
                inflacion_total = pow(1 + inflacion_mensual, meses) - 1
                print(f'Inflacion mensual {inflacion_total}')
                return inflacion_total
            else:
                print("No se encontró el valor de inflación en el resultado.")
                return 0
        else:
            print("No se encontraron resultados en la API.")
            return 0

    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud a la API: {e}")
        return 0  # En caso de error, devolver 0