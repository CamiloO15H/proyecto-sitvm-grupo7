"""Generador de instancias sintéticas de viajes por día, con semilla fija."""

import random

SEMILLA: int = 2026
"""Semilla fija para que cualquiera reproduzca las mismas instancias."""


def generar_viajes(dias: int, rng: random.Random) -> list[int]:
    """Genera los viajes por día de una tarjeta durante un periodo.

    Args:
        dias: número de días del periodo.
        rng: generador aleatorio con semilla fija.

    Returns:
        Lista de viajes por día; el índice 0 es el primer día.
    """
    # TODO: viajes en todos o casi todos los días (la guía lo exige
    # para que los días con viaje crezcan con d).
    raise NotImplementedError


def generar_instancias(
    dias: int, cantidad: int, semilla: int = SEMILLA
) -> list[list[int]]:
    """Genera varias tarjetas con el mismo número de días.

    Args:
        dias: número de días de cada instancia.
        cantidad: número de instancias (tarjetas) a generar.
        semilla: semilla fija.

    Returns:
        Lista de instancias de viajes por día.
    """
    # TODO: use random.Random(semilla) y generar_viajes.
    raise NotImplementedError
