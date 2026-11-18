"""Tarifas vigentes del perfil general del SITVM."""

PASAJE: int = 3900
"""Pasaje sencillo: un viaje."""

DIARIO: int = 9500
"""Pase diario: viajes ilimitados durante un día calendario."""

SEMANAL: int = 36000
"""Pase semanal: viajes ilimitados durante 7 días consecutivos."""

MENSUAL: int = 135000
"""Pase mensual: viajes ilimitados durante 30 días consecutivos."""

DIAS_SEMANAL: int = 7
"""Días consecutivos que cubre el pase semanal."""

DIAS_MENSUAL: int = 30
"""Días consecutivos que cubre el pase mensual."""


def costo_del_dia(viajes: int) -> int:
    """Calcula lo más barato para pagar solo un día.

    Args:
        viajes: viajes de la tarjeta en ese día.

    Returns:
        El menor valor entre los pasajes sencillos y el pase diario, en
        pesos; 0 si el día no tiene viajes.
    """
    return min(viajes * PASAJE, DIARIO)