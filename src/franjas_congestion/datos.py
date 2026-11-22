"""Generacion reproducible de saldos netos por intervalos de cinco minutos."""

import random


def generar_saldos(n: int, semilla: int = 2026) -> list[int]:
    """Genera saldos netos sinteticos para una plataforma.

    Args:
        n: Cantidad de intervalos de cinco minutos (no negativa).
        semilla: Semilla base para reproducir los mismos datos.

    Returns:
        Lista de n enteros entre -60 y 55, incluidos.

    Raises:
        ValueError: Si n es negativo.
    """
    if n < 0:
        raise ValueError("n debe ser mayor o igual a cero")
    rng = random.Random(semilla + n)
    return [rng.randint(-60, 55) for _ in range(n)]
