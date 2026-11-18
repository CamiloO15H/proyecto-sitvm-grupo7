"""Liquidación del tope tarifario de una tarjeta por programación dinámica."""

from tarifas import DIAS_MENSUAL, DIAS_SEMANAL, MENSUAL, SEMANAL, costo_del_dia


def costo_minimo_contado(viajes_por_dia: list[int]) -> tuple[int, int]:
    """Calcula el costo mínimo y cuenta las opciones evaluadas.

    Llena la tabla del último día al primero. La posición d + 1 es el caso
    base y vale 0. Un día sin viajes hereda el valor del día siguiente (una
    opción); un día con viajes compara tres opciones: pagarlo solo, comprar un
    pase semanal o comprar un pase mensual.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del mes. El índice 0
            es el primer día; un día sin viajes vale 0.

    Returns:
        Una tupla con el costo mínimo en pesos y el número de opciones
        evaluadas.
    """
    dias = len(viajes_por_dia)
    tabla = [0] * (dias + 2)
    operaciones = 0

    for dia in range(dias, 0, -1):
        viajes = viajes_por_dia[dia - 1]

        if viajes == 0:
            operaciones += 1
            tabla[dia] = tabla[dia + 1]
            continue

        operaciones += 1
        mejor = costo_del_dia(viajes) + tabla[dia + 1]

        operaciones += 1
        semanal = SEMANAL + tabla[min(dia + DIAS_SEMANAL, dias + 1)]
        if semanal < mejor:
            mejor = semanal

        operaciones += 1
        mensual = MENSUAL + tabla[min(dia + DIAS_MENSUAL, dias + 1)]
        if mensual < mejor:
            mejor = mensual

        tabla[dia] = mejor

    return tabla[1], operaciones


def costo_minimo(viajes_por_dia: list[int]) -> int:
    """Calcula el costo de la combinación más barata que cubre los viajes.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del mes. El índice 0
            es el primer día; un día sin viajes vale 0.

    Returns:
        El costo mínimo en pesos.
    """
    return costo_minimo_contado(viajes_por_dia)[0]


def liquidar_tope(viajes_por_dia: list[int], cobrado: int) -> int:
    """Calcula la devolución que corresponde al usuario.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del mes.
        cobrado: pesos que se le cobraron durante el mes.

    Returns:
        La diferencia entre lo cobrado y el costo mínimo, nunca negativa.
    """
    return max(0, cobrado - costo_minimo(viajes_por_dia))
