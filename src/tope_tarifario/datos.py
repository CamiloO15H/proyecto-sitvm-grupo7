"""Generador de instancias sintéticas de viajes por día, con semilla fija."""

import random

SEMILLA: int = 2026
"""Semilla fija para que cualquiera reproduzca las mismas instancias."""

PROB_DIA_CON_VIAJES: float = 0.9
"""Probabilidad de que un día tenga viajes (casi todos los días)."""

VIAJES_POSIBLES: list[int] = [1, 2, 3, 4]
"""Cantidades de viajes que puede tener un día con viajes."""

PESOS_VIAJES: list[int] = [2, 4, 3, 1]
"""Pesos relativos de cada cantidad; lo más común es ida y vuelta (2)."""


def generar_viajes(dias: int, rng: random.Random) -> list[int]:
    """Genera los viajes por día de una tarjeta durante un periodo.

    Args:
        dias: número de días del periodo.
        rng: generador aleatorio con semilla fija.

    Returns:
        Lista de viajes por día; el índice 0 es el primer día.
    """
    viajes: list[int] = []
    for _ in range(dias):
        if rng.random() < PROB_DIA_CON_VIAJES:
            viajes.append(rng.choices(VIAJES_POSIBLES, PESOS_VIAJES)[0])
        else:
            viajes.append(0)
    return viajes


def generar_instancias(
    dias: int, cantidad: int, semilla: int = SEMILLA
) -> list[list[int]]:
    """Genera varias tarjetas con el mismo número de días.

    Args:
        dias: número de días de cada instancia.
        cantidad: número de instancias (tarjetas) a generar.
        semilla: semilla fija; la misma semilla da las mismas instancias.

    Returns:
        Lista de instancias de viajes por día.
    """
    rng = random.Random(semilla + dias)
    instancias: list[list[int]] = []
    for _ in range(cantidad):
        instancias.append(generar_viajes(dias, rng))
    return instancias