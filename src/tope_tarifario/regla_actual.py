"""Regla simplificada que aplica hoy el sistema (línea base)."""

from tarifas import DIARIO, DIAS_MENSUAL, DIAS_SEMANAL, MENSUAL, PASAJE, SEMANAL


def costo_regla_actual(viajes_por_dia: list[int]) -> int:
    """Calcula lo que cobra hoy la regla simplificada del sistema.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del mes.

    Returns:
        El costo cobrado en pesos.
    """
    # TODO: documente en el README cómo interpretó la regla del caso.
    raise NotImplementedError
