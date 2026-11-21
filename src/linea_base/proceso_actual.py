"""Reproducción de las estrategias que usa hoy el proceso nocturno.

Sirve solo para medir la línea base (apartado 1.4 del informe). Cada
función devuelve su resultado y el número de operaciones elementales.
"""

from datos import Validacion


def deduplicar_actual(
    validaciones: list[Validacion],
) -> tuple[list[Validacion], int]:
    """Operación 1: compara cada validación con todas las ya aceptadas.

    Dos registros son la misma validación si coinciden el validador, la
    tarjeta y la marca de tiempo. La lista original no se modifica.

    Args:
        validaciones: registros en el orden en que llegan.

    Returns:
        (validaciones aceptadas, comparaciones realizadas).
    """
    aceptadas: list[Validacion] = []
    comparaciones = 0
    for nueva in validaciones:
        clave = (nueva[0], nueva[1], nueva[3])
        repetida = False
        for vieja in aceptadas:
            comparaciones += 1
            if clave == (vieja[0], vieja[1], vieja[3]):
                repetida = True
                break
        if not repetida:
            aceptadas.append(nueva)
    return aceptadas, comparaciones


def ordenar_actual(
    validaciones: list[Validacion],
) -> tuple[list[Validacion], int]:
    """Operación 2: ordenamiento por inserción por tarjeta y hora.

    Trabaja sobre una copia para no modificar el archivo original.

    Args:
        validaciones: validaciones ya depuradas.

    Returns:
        (validaciones ordenadas, comparaciones realizadas).
    """
    datos = list(validaciones)
    comparaciones = 0
    for i in range(1, len(datos)):
        actual = datos[i]
        clave = (actual[1], actual[3])
        j = i - 1
        while j >= 0:
            comparaciones += 1
            if (datos[j][1], datos[j][3]) <= clave:
                break
            datos[j + 1] = datos[j]
            j -= 1
        datos[j + 1] = actual
    return datos, comparaciones


def tramo_maximo_actual(saldos: list[int]) -> tuple[int, int, int, int]:
    """Operación 3: evalúa todos los tramos posibles de la serie.

    Para cada inicio acumula la suma hacia la derecha, así que evalúa
    n·(n + 1)/2 tramos.

    Args:
        saldos: saldo neto de cada intervalo de 5 minutos.

    Returns:
        (suma máxima, inicio, fin, tramos evaluados); inicio y fin son
        índices incluidos.
    """
    mejor, inicio_mejor, fin_mejor = saldos[0], 0, 0
    tramos = 0
    for inicio in range(len(saldos)):
        suma = 0
        for fin in range(inicio, len(saldos)):
            suma += saldos[fin]
            tramos += 1
            if suma > mejor:
                mejor, inicio_mejor, fin_mejor = suma, inicio, fin
    return mejor, inicio_mejor, fin_mejor, tramos