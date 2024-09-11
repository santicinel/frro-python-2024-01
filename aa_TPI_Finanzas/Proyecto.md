# NOMBRE_DEL_PROYECTO

Finanzio

## Descripción del proyecto

This app is designed to predict a person's monthly expenses, helping them keep a detailed record of upcoming expenses and their saving capacity.

## Modelo Entidad Relación

https://app.diagrams.net/#G1H6dw80HDBGuTKxCx0Edm0yzFTFedM9Vo#%7B%22pageId%22%3A%22mTJiV4btCfIQWjWJuAaB%22%7D

## Requerimientos

### Funcionales
- Registrar altas de usuario.
- Realizar calculo del gasto futuro de la persona.
- Registrar los gastos.
- Consumir la Api externa para obtener valor de inflación.
- Se debe registrar la fecha de creación de la cuenta.
- El usuario puede ingresar sus ingresos y gastos mensuales durante el primer mes.
- Los gastos e ingresos deben ser clasificados según categorías con prioridad.
- La predicción debe considerar posibles variaciones e imprevistos en los gastos mes a mes.
    

### No Funcionales
- El sistema debe funcionar correctamente en múltiples navegadores (Sólo Web).
- Todas las contraseñas deben guardarse con encriptado criptográfico.
- Todas los Tokens / API Keys o similares no deben exponerse de manera pública.
- El sistema debe diseñarse con la arquitectura en 3 capas.
- El sistema debe utilizar control de versiones mediante GIT.
- El sistema debe estar programado en Python 3.8 o superior.
- El sistema debe funcionar desde una ventana normal y una de incógnito de manera independiente.



### Narrativa
Funcionalidades Clave:

    Ingreso de Datos Iniciales:
        El usuario ingresa sus gastos e ingresos totales durante el primer mes.
        La aplicación utiliza el índice de inflación proporcionado por INDEC para predecir los gastos futuros. 

    Gestión Continua:
        Permite al usuario agregar, modificar y eliminar ingresos en cualquier momento.
        Clasifica y analiza los gastos según prioridades predefinidas.

    Predicciones y Análisis:
        A partir de los datos ingresados y el índice de inflación, la aplicación predice los gastos futuros.
        Considera posibles variaciones e imprevistos en los gastos mes a mes, ofreciendo un margen de ajuste.
        Luego de la predicción de gastos, realiza una breve conclusión del pronostico de ese mes.

Beneficios:

    Ayuda a los usuarios a planificar sus finanzas con antelación, facilitando la toma de decisiones informadas sobre ahorro y gasto.
    Los usuarios pueden actualizar sus ingresos y gastos en cualquier momento, manteniendo el control sobre sus finanzas.
    Proporciona una vista detallada de los gastos clasificados por prioridad, ayudando a identificar áreas de mejora en la gestión financiera personal.
      

### Reglas de negocio
1) Un usuario se registra con mail, nombre, apellido, dni, contraseña, fecha nacimiento y un username. Se registra la fecha de creación de cuenta.
2) Un usuario va a ingresar sus gastos mensuales, puede tener uno o muchos gastos. Se registra la fecha de cada gasto.
3) Un usuario carga sus ingresos mensuales. Puede tener mas de uno y querer eliminarlos o sumarlos en cualquier momento.
4) Los gastos tienen categorias.
5) Las categorias tienen prioridades enumeradas de 1-5.
6) Las prioridades son: Primordial , Alta, Media, Baja, Evitable. (alquiler=primordial=5, adornos=evitable=1)
7) Las predicciones de gastos pertenecen a un cliente y a sus gastos mensuales.
8) Se puede predecir a varios meses futuros. 
9) Un usuario va a poder ver una comparación de sus gastos con el promedio de los gastos de las personas.
10) Un usuario va a poder cuando quiera ver la predicción de gastos al mes siguiente.
11) El sistema debe ser capaz de realizar el calculo de la predicción con el dato del gasto de la persona y el dato de la inflación.


       

      

    
