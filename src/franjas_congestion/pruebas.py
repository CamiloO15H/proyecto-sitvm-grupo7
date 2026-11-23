"""Pruebas con assert de las franjas de congestión.

Ejecutar desde la raíz del repositorio:
    python src/franjas_congestion/pruebas.py
"""

import random
from collections.abc import Callable

from datos import generar_saldos
from divide_venceras import (
    tramo_divide_venceras,
    tramo_divide_venceras_contado,
)
from fuerza_bruta import tramo_fuerza_bruta, tramo_fuerza_bruta_contado
from kadane import tramo_kadane, tramo_kadane_contado

Tramo = tuple[int, int, int]

ALGORITMOS: dict[str, Callable[[list[int]], Tramo]] = {
    "fuerza bruta": tramo_fuerza_bruta,
    "divide y vencerás": tramo_divide_venceras,
    "Kadane": tramo_kadane,
}


def comprobar_tramo(saldos: list[int], tramo: Tramo) -> None:
    """Comprueba que el tramo sea no vacío, válido y sume lo que dice.

    Args:
        saldos: serie de saldos sobre la que se calculó el tramo.
        tramo: tupla (suma, inicio, fin) con extremos incluidos.
    """
    suma, inicio, fin = tramo
    assert 0 <= inicio <= fin < len(saldos), (saldos, tramo)
    assert sum(saldos[inicio:fin + 1]) == suma, (saldos, tramo)


def probar_casos_limite() -> None:
    """Verifica un elemento, solo negativos, solo positivos y serie vacía."""
    for nombre, algoritmo in ALGORITMOS.items():
        assert algoritmo([7]) == (7, 0, 0), nombre
        assert algoritmo([-7]) == (-7, 0, 0), nombre
        assert algoritmo([0]) == (0, 0, 0), nombre

        assert algoritmo([-8, -3, -6, -2, -5]) == (-2, 3, 3), nombre
        assert algoritmo([4, 1, 7, 2, 9, 3]) == (26, 0, 5), nombre
        assert algoritmo([0, 0, 0, 0])[0] == 0, nombre

        assert algoritmo([-5, 9]) == (9, 1, 1), nombre
        assert algoritmo([9, -5]) == (9, 0, 0), nombre
        assert algoritmo([4, 6]) == (10, 0, 1), nombre

        try:
            algoritmo([])
        except ValueError:
            pass
        else:
            raise AssertionError(f"{nombre} aceptó una serie vacía")


def probar_ejemplo_a_mano() -> None:
    """Verifica un ejemplo pequeño de 8 intervalos con tramo óptimo único."""
    saldos = [-3, 5, -2, 8, -6, 3, 9, -4]
    for nombre, algoritmo in ALGORITMOS.items():
        assert algoritmo(saldos) == (17, 1, 6), nombre

    cruzado = [-5, -4, 6, 7, 8, 9, -4, -5]
    for nombre, algoritmo in ALGORITMOS.items():
        assert algoritmo(cruzado) == (30, 2, 5), nombre


def probar_contra_fuerza_bruta() -> None:
    """Verifica al menos 20 series aleatorias con semilla fija."""
    rng = random.Random(2026)

    for _ in range(40):
        n = rng.randint(1, 60)
        saldos = [rng.randint(-60, 55) for _ in range(n)]
        esperado = tramo_fuerza_bruta(saldos)[0]

        for nombre, algoritmo in ALGORITMOS.items():
            tramo = algoritmo(saldos)
            assert tramo[0] == esperado, (nombre, saldos)
            comprobar_tramo(saldos, tramo)


def probar_contra_referencia_independiente() -> None:
    """Compara las tres estrategias con una referencia escrita con sum."""
    rng = random.Random(7)

    for _ in range(25):
        n = rng.randint(1, 20)
        saldos = [rng.randint(-60, 55) for _ in range(n)]
        referencia = max(
            sum(saldos[i:j + 1])
            for i in range(n)
            for j in range(i, n)
        )

        for nombre, algoritmo in ALGORITMOS.items():
            assert algoritmo(saldos)[0] == referencia, (nombre, saldos)


def probar_restriccion_negocio() -> None:
    """El tramo es no vacío, válido y la entrada no se modifica."""
    rng = random.Random(11)

    for n in (1, 2, 3, 10, 57, 200):
        saldos = generar_saldos(n)
        copia = saldos.copy()

        for nombre, algoritmo in ALGORITMOS.items():
            tramo = algoritmo(saldos)
            comprobar_tramo(saldos, tramo)
            assert saldos == copia, f"{nombre} modificó la entrada"

    for _ in range(10):
        saldos = [rng.randint(-60, 55) for _ in range(rng.randint(1, 30))]
        sumas = {algoritmo(saldos)[0] for algoritmo in ALGORITMOS.values()}
        assert len(sumas) == 1, saldos


def probar_generador() -> None:
    """Los datos sintéticos son reproducibles y están en el rango declarado."""
    assert generar_saldos(0) == []
    assert generar_saldos(500) == generar_saldos(500)
    assert generar_saldos(500) != generar_saldos(501)[:500]
    assert all(-60 <= saldo <= 55 for saldo in generar_saldos(1000))
    assert len(generar_saldos(333)) == 333

    try:
        generar_saldos(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("generar_saldos aceptó n negativo")


def probar_contraste_con_regla_actual() -> None:
    """La regla actual (todos los tramos) da la misma suma con más trabajo.

    La estrategia actual evalúa todos los tramos, así que no se equivoca de
    suma: lo que pierde frente a Kadane y divide y vencerás es el número de
    operaciones.
    """
    saldos = generar_saldos(200)

    tramo_actual, operaciones_actual = tramo_fuerza_bruta_contado(saldos)
    tramo_kadane_, operaciones_kadane = tramo_kadane_contado(saldos)
    tramo_dyv, operaciones_dyv = tramo_divide_venceras_contado(saldos)

    assert tramo_actual[0] == tramo_kadane_[0] == tramo_dyv[0]
    assert operaciones_actual == 200 * 201 // 2
    assert operaciones_kadane == 200
    assert operaciones_kadane < operaciones_dyv < operaciones_actual


def probar_contadores() -> None:
    """Verifica las fórmulas del número de operaciones de cada estrategia."""
    for n in (1, 2, 5, 64, 100, 257):
        saldos = generar_saldos(n)
        assert tramo_fuerza_bruta_contado(saldos)[1] == n * (n + 1) // 2
        assert tramo_kadane_contado(saldos)[1] == n

    for n in (1, 2, 8, 16, 32):
        saldos = generar_saldos(n)
        operaciones = tramo_divide_venceras_contado(saldos)[1]
        assert n <= operaciones <= n * (n.bit_length() + 1), (n, operaciones)

    pequeno = tramo_divide_venceras_contado(generar_saldos(1000))[1]
    grande = tramo_divide_venceras_contado(generar_saldos(2000))[1]
    assert 2.0 < grande / pequeno < 2.3


def probar_funciones_contadas_coinciden() -> None:
    """Cada función contada devuelve el mismo tramo que la versión simple."""
    rng = random.Random(5)

    for _ in range(20):
        saldos = [rng.randint(-60, 55) for _ in range(rng.randint(1, 40))]
        contado, sin_contar = tramo_fuerza_bruta_contado, tramo_fuerza_bruta
        assert contado(saldos)[0] == sin_contar(saldos)
        assert tramo_kadane_contado(saldos)[0] == tramo_kadane(saldos)
        contado = tramo_divide_venceras_contado
        sin_contar = tramo_divide_venceras
        assert contado(saldos)[0] == sin_contar(saldos)


if __name__ == "__main__":
    probar_casos_limite()
    probar_ejemplo_a_mano()
    probar_contra_fuerza_bruta()
    probar_contra_referencia_independiente()
    probar_restriccion_negocio()
    probar_generador()
    probar_contraste_con_regla_actual()
    probar_contadores()
    probar_funciones_contadas_coinciden()
    print("Todas las pruebas pasaron")
