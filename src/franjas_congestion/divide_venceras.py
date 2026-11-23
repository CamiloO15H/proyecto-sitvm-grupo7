"""Tramo de mayor suma por divide y vencerás, en Θ(n log n)."""

Tramo = tuple[int, int, int]


def _tramo_que_cruza(
    saldos: list[int], inicio: int, medio: int, fin: int
) -> tuple[Tramo, int]:
    """Busca el mejor tramo que contiene los intervalos medio y medio + 1.

    Args:
        saldos: serie completa de saldos.
        inicio: primer índice de la mitad que se está resolviendo.
        medio: último índice de la mitad izquierda.
        fin: último índice de la mitad que se está resolviendo.

    Returns:
        El tramo (suma, inicio, fin) y el número de intervalos recorridos.
    """
    suma = 0
    mejor_izquierda = saldos[medio]
    limite_izquierdo = medio
    operaciones = 0
    for posicion in range(medio, inicio - 1, -1):
        suma += saldos[posicion]
        operaciones += 1
        if suma > mejor_izquierda:
            mejor_izquierda = suma
            limite_izquierdo = posicion

    suma = 0
    mejor_derecha = saldos[medio + 1]
    limite_derecho = medio + 1
    for posicion in range(medio + 1, fin + 1):
        suma += saldos[posicion]
        operaciones += 1
        if suma > mejor_derecha:
            mejor_derecha = suma
            limite_derecho = posicion

    tramo = (mejor_izquierda + mejor_derecha, limite_izquierdo, limite_derecho)
    return tramo, operaciones


def _resolver(
    saldos: list[int], inicio: int, fin: int
) -> tuple[Tramo, int]:
    """Resuelve el subproblema de los intervalos inicio a fin, incluidos.

    Args:
        saldos: serie completa de saldos.
        inicio: primer índice del subproblema.
        fin: último índice del subproblema.

    Returns:
        El mejor tramo (suma, inicio, fin) dentro del rango y el número de
        intervalos recorridos.
    """
    if inicio == fin:
        return (saldos[inicio], inicio, inicio), 1

    medio = (inicio + fin) // 2
    izquierdo, ops_izquierda = _resolver(saldos, inicio, medio)
    derecho, ops_derecha = _resolver(saldos, medio + 1, fin)
    cruzado, ops_cruce = _tramo_que_cruza(saldos, inicio, medio, fin)

    mejor = izquierdo
    if derecho[0] > mejor[0]:
        mejor = derecho
    if cruzado[0] > mejor[0]:
        mejor = cruzado
    return mejor, ops_izquierda + ops_derecha + ops_cruce


def tramo_divide_venceras_contado(saldos: list[int]) -> tuple[Tramo, int]:
    """Busca el tramo de mayor suma y cuenta los intervalos recorridos.

    Divide la serie por la mitad. El mejor tramo está completo en la mitad
    izquierda, completo en la derecha o cruza el punto medio; el último caso
    se resuelve extendiendo desde el medio hacia ambos lados. Una operación es
    un intervalo recorrido, ya sea en un caso base o al extender el cruce.

    Args:
        saldos: saldos netos por intervalo de cinco minutos, con al menos un
            elemento.

    Returns:
        Una tupla con el tramo (suma, inicio, fin), con extremos incluidos, y
        el número de intervalos recorridos.

    Raises:
        ValueError: si la serie está vacía.
    """
    if not saldos:
        raise ValueError("la serie no puede estar vacía")
    return _resolver(saldos, 0, len(saldos) - 1)


def tramo_divide_venceras(saldos: list[int]) -> Tramo:
    """Devuelve el tramo consecutivo de mayor suma por divide y vencerás.

    Args:
        saldos: saldos netos por intervalo de cinco minutos, con al menos un
            elemento.

    Returns:
        El tramo (suma, inicio, fin), con extremos incluidos.

    Raises:
        ValueError: si la serie está vacía.
    """
    return tramo_divide_venceras_contado(saldos)[0]
