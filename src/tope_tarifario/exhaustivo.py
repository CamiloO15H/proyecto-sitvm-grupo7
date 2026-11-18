"""Soluciones exhaustivas para verificar el tope tarifario."""

from tarifas import (
    DIARIO, DIAS_MENSUAL, DIAS_SEMANAL, MENSUAL, PASAJE, SEMANAL,
    costo_del_dia,
)


def costo_exhaustivo_contado(viajes_por_dia: list[int]) -> tuple[int, int]:
    """Explora las compras posibles sin reutilizar subproblemas.

    Args:
        viajes_por_dia: Número de viajes de cada día del periodo.

    Returns:
        Costo mínimo y cantidad de opciones evaluadas.
    """
    dias = len(viajes_por_dia)
    operaciones = 0

    def buscar(dia: int) -> int:
        """Encuentra el menor costo desde el día indicado hasta el final."""
        nonlocal operaciones
        if dia >= dias:
            return 0
        if viajes_por_dia[dia] == 0:
            return buscar(dia + 1)

        operaciones += 1
        mejor = costo_del_dia(viajes_por_dia[dia]) + buscar(dia + 1)
        operaciones += 1
        semanal = SEMANAL + buscar(min(dia + DIAS_SEMANAL, dias))
        if semanal < mejor:
            mejor = semanal
        operaciones += 1
        mensual = MENSUAL + buscar(min(dia + DIAS_MENSUAL, dias))
        if mensual < mejor:
            mejor = mensual
        return mejor

    return buscar(0), operaciones


def costo_exhaustivo(viajes_por_dia: list[int]) -> int:
    """Devuelve el costo mínimo sin memoización.

    Args:
        viajes_por_dia: Viajes por cada día del periodo.

    Returns:
        Costo mínimo en pesos.
    """
    return costo_exhaustivo_contado(viajes_por_dia)[0]


def costo_combinaciones_contado(viajes_por_dia: list[int]) -> tuple[int, int]:
    """Prueba cuatro decisiones por día, incluso compras redundantes.

    Args:
        viajes_por_dia: Viajes registrados en cada día.

    Returns:
        Menor costo y número de opciones exploradas.
    """
    dias = len(viajes_por_dia)
    operaciones = 0
    mejor = float("inf")

    def explorar(dia: int, cubierto_hasta: int, acumulado: int) -> None:
        """Recorre todas las decisiones por día, sin memorizar ni podar."""
        nonlocal operaciones, mejor
        if dia == dias:
            if acumulado < mejor:
                mejor = acumulado
            return

        operaciones += 1
        sencillo = 0 if dia < cubierto_hasta else viajes_por_dia[dia] * PASAJE
        explorar(dia + 1, cubierto_hasta, acumulado + sencillo)

        operaciones += 1
        diario = 0 if dia < cubierto_hasta else DIARIO
        explorar(dia + 1, cubierto_hasta, acumulado + diario)

        operaciones += 1
        explorar(
            dia + 1,
            max(cubierto_hasta, dia + DIAS_SEMANAL),
            acumulado + SEMANAL,
        )

        operaciones += 1
        explorar(
            dia + 1,
            max(cubierto_hasta, dia + DIAS_MENSUAL),
            acumulado + MENSUAL,
        )

    explorar(0, 0, 0)
    return int(mejor), operaciones


def costo_combinaciones(viajes_por_dia: list[int]) -> int:
    """Devuelve el mínimo al examinar las cuatro elecciones de cada día.

    Args:
        viajes_por_dia: Viajes de cada día.

    Returns:
        Costo mínimo en pesos.
    """
    return costo_combinaciones_contado(viajes_por_dia)[0]
