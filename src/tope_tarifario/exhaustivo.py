"""Solución exhaustiva del tope tarifario: prueba todas las combinaciones."""

from tarifas import DIARIO, DIAS_MENSUAL, DIAS_SEMANAL, MENSUAL, PASAJE, SEMANAL


def costo_exhaustivo(viajes_por_dia: list[int]) -> int:
    """Calcula el mismo costo probando todas las combinaciones de productos.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del mes.

    Returns:
        El costo mínimo en pesos.
    """
    # TODO: solo para instancias pequeñas; su costo es exponencial.
    raise NotImplementedError
