"""Interpretación acordada de la regla simplificada del SITVM."""

from tarifas import DIAS_SEMANAL, MENSUAL, SEMANAL, costo_del_dia


def costo_regla_actual_contado(viajes_por_dia: list[int]) -> tuple[int, int]:
    """Aplica bloques semanales fijos y luego revisa el mensual.

    Args:
        viajes_por_dia: Viajes diarios en el periodo.

    Returns:
        Cobro según la regla actual y opciones evaluadas.
    """
    dias = len(viajes_por_dia)
    operaciones = 0
    costos_dia: list[int] = []

    for viajes in viajes_por_dia:
        operaciones += 2  # pasaje sencillo y pase diario
        costos_dia.append(costo_del_dia(viajes))

    total = 0
    for inicio in range(0, dias, DIAS_SEMANAL):
        bloque = sum(costos_dia[inicio:inicio + DIAS_SEMANAL])
        operaciones += 2  # costo por días y pase semanal
        total += min(bloque, SEMANAL)

    if dias >= 30:
        operaciones += 2  # total por semanas y alternativa mensual
        if total > MENSUAL:
            adicional = costos_dia[30] if dias == 31 else 0
            total = MENSUAL + adicional

    return total, operaciones


def costo_regla_actual(viajes_por_dia: list[int]) -> int:
    """Devuelve el cobro calculado con los bloques fijos acordados.

    Args:
        viajes_por_dia: Cantidad de viajes de cada día.

    Returns:
        Total cobrado en pesos.
    """
    return costo_regla_actual_contado(viajes_por_dia)[0]
