"""Tramo de mayor suma por fuerza bruta: evalúa todos los tramos posibles."""

Tramo = tuple[int, int, int]


def tramo_fuerza_bruta_contado(saldos: list[int]) -> tuple[Tramo, int]:
    """Busca el tramo de mayor suma y cuenta los tramos evaluados.

    Para cada posición de inicio extiende el tramo un intervalo a la vez,
    manteniendo la suma acumulada, de modo que cada tramo se evalúa una sola
    vez. Una operación es un tramo evaluado.

    Args:
        saldos: saldos netos por intervalo de cinco minutos, con al menos un
            elemento.

    Returns:
        Una tupla con el tramo (suma, inicio, fin), con extremos incluidos, y
        el número de tramos evaluados, que es n(n + 1) / 2.

    Raises:
        ValueError: si la serie está vacía.
    """
    if not saldos:
        raise ValueError("la serie no puede estar vacía")

    mejor_suma = saldos[0]
    mejor_inicio = 0
    mejor_fin = 0
    operaciones = 0

    for inicio in range(len(saldos)):
        suma = 0
        for fin in range(inicio, len(saldos)):
            suma += saldos[fin]
            operaciones += 1
            if suma > mejor_suma:
                mejor_suma = suma
                mejor_inicio = inicio
                mejor_fin = fin

    return (mejor_suma, mejor_inicio, mejor_fin), operaciones


def tramo_fuerza_bruta(saldos: list[int]) -> Tramo:
    """Devuelve el tramo consecutivo de mayor suma probando todos los tramos.

    Args:
        saldos: saldos netos por intervalo de cinco minutos, con al menos un
            elemento.

    Returns:
        El tramo (suma, inicio, fin), con extremos incluidos.

    Raises:
        ValueError: si la serie está vacía.
    """
    return tramo_fuerza_bruta_contado(saldos)[0]
