"""Bloque IF, operadores lógicos, función max y operador ternario."""


def maximo_basico(a: float, b: float) -> float:
    """Toma dos números y devuelve el mayor.
    

    Restricción: No utilizar la función max"""
    maximo:float
    if a>b: 
        maximo=a
    elif b==a:
        maximo=b=a
    else:
        maximo=b
    return maximo


# NO MODIFICAR - INICIO
assert maximo_basico(10, 5) == 10
assert maximo_basico(9, 18) == 18
# NO MODIFICAR - FIN
