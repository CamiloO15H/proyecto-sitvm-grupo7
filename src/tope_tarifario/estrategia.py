"""Liquidación del tope tarifario de una tarjeta por programación dinámica."""

from tarifas import DIARIO, DIAS_MENSUAL, DIAS_SEMANAL, MENSUAL, PASAJE, SEMANAL


def costo_minimo(viajes_por_dia: list[int]) -> int:
    """Calcula el costo de la combinación más barata que cubre los viajes.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del mes. El índice 0
            es el primer día; un día sin viajes vale 0.

    Returns:
        El costo mínimo en pesos.
    """
    # TODO: programación dinámica sobre los días del mes.
    raise NotImplementedError


def liquidar_tope(viajes_por_dia: list[int], cobrado: int) -> int:
    """Calcula la devolución que corresponde al usuario.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del mes.
        cobrado: pesos que se le cobraron durante el mes.

    Returns:
        La diferencia entre lo cobrado y el costo mínimo, nunca negativa.
    """
    # TODO: use costo_minimo.
    raise NotImplementedError
