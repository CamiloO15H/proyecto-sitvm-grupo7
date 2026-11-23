"""Tramo de mayor suma con el algoritmo de Kadane, en una sola pasada."""

Tramo = tuple[int, int, int]


def tramo_kadane_contado(saldos: list[int]) -> tuple[Tramo, int]:
    """Busca el tramo de mayor suma y cuenta los intervalos recorridos.

    Mantiene el mejor tramo que termina en el intervalo actual: si el tramo
    acumulado hasta el intervalo anterior es negativo, no ayuda y se empieza
    uno nuevo; si no, se extiende. Una operación es un intervalo procesado.

    Args:
        saldos: saldos netos por intervalo de cinco minutos, con al menos un
            elemento.

    Returns:
        Una tupla con el tramo (suma, inicio, fin), con extremos incluidos, y
        el número de intervalos procesados, que es n.

    Raises:
        ValueError: si la serie está vacía.
    """
    if not saldos:
        raise ValueError("la serie no puede estar vacía")

    suma_actual = saldos[0]
    inicio_actual = 0
    mejor_suma = suma_actual
    mejor_inicio = 0
    mejor_fin = 0
    operaciones = 1

    for posicion in range(1, len(saldos)):
        operaciones += 1
        if suma_actual < 0:
            suma_actual = saldos[posicion]
            inicio_actual = posicion
        else:
            suma_actual += saldos[posicion]
        if suma_actual > mejor_suma:
            mejor_suma = suma_actual
            mejor_inicio = inicio_actual
            mejor_fin = posicion

    return (mejor_suma, mejor_inicio, mejor_fin), operaciones


def tramo_kadane(saldos: list[int]) -> Tramo:
    """Devuelve el tramo consecutivo de mayor suma con Kadane.

    Args:
        saldos: saldos netos por intervalo de cinco minutos, con al menos un
            elemento.

    Returns:
        El tramo (suma, inicio, fin), con extremos incluidos.

    Raises:
        ValueError: si la serie está vacía.
    """
    return tramo_kadane_contado(saldos)[0]
