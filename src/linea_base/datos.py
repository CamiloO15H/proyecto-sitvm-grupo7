"""Datos sintéticos para medir el proceso actual, con semilla fija."""

import random

SEMILLA: int = 2026
"""Semilla fija para que cualquiera reproduzca las mismas instancias."""

PROPORCION_REPETIDAS: float = 0.065
"""Validaciones reenviadas: el caso informa entre 4 % y 9 %; se usa el punto
medio."""

PERFILES: list[str] = [
    "general",
    "estudiante",
    "adulto_mayor",
    "discapacidad",
]
"""Perfiles de tarifa que informa el cliente."""

Validacion = tuple[int, int, int, int, int, str]
"""(id_validador, id_tarjeta, id_estacion, marca_tiempo, valor, perfil)."""


def generar_validaciones(n: int, semilla: int = SEMILLA) -> list[Validacion]:
    """Genera un día de validaciones con algunas repetidas por reenvío.

    Args:
        n: número total de registros que llegan (incluidas las repetidas).
        semilla: semilla fija.

    Returns:
        Lista de validaciones en el orden en que llegan.
    """
    rng = random.Random(semilla + n)
    unicas = n - int(n * PROPORCION_REPETIDAS)
    validaciones: list[Validacion] = []
    for _ in range(unicas):
        validaciones.append(
            (
                rng.randint(1, 2100),
                rng.randint(1, 3_200_000),
                rng.randint(1, 120),
                rng.randint(16_200, 84_600),  # segundos: 04:30 a 23:30
                3900,
                rng.choice(PERFILES),
            )
        )
    for _ in range(n - unicas):
        posicion = rng.randrange(len(validaciones) + 1)
        validaciones.insert(posicion, rng.choice(validaciones))
    return validaciones


def generar_saldos(n: int, semilla: int = SEMILLA) -> list[int]:
    """Genera la serie de saldos netos de una plataforma por intervalo.

    Args:
        n: número de intervalos de 5 minutos.
        semilla: semilla fija.

    Returns:
        Saldo neto de cada intervalo (puede ser negativo).
    """
    rng = random.Random(semilla + n)
    return [rng.randint(-60, 55) for _ in range(n)]