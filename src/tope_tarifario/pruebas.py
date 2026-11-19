"""Pruebas con assert de la liquidación del tope tarifario.

Ejecutar desde la raíz del repositorio:
    python src/tope_tarifario/pruebas.py
"""

import random

from estrategia import costo_minimo, liquidar_tope
from exhaustivo import costo_exhaustivo
from regla_actual import costo_regla_actual


def probar_casos_limite() -> None:
    """Verifica mes vacío, un solo día, días sin viajes y pases que sobran."""
    assert costo_minimo([]) == 0
    assert costo_exhaustivo([]) == 0

    assert costo_minimo([1]) == 3900
    assert costo_exhaustivo([1]) == 3900

    assert costo_minimo([3]) == 9500
    assert costo_exhaustivo([3]) == 9500

    sin_viajes = [0, 0, 0, 0, 0]
    assert costo_minimo(sin_viajes) == 0
    assert costo_exhaustivo(sin_viajes) == 0

    cuatro_dias = [3, 3, 3, 3]
    assert costo_minimo(cuatro_dias) == 36000
    assert costo_exhaustivo(cuatro_dias) == 36000

    assert costo_regla_actual([]) == 0
    febrero = [3] * 28
    assert costo_regla_actual(febrero) == 135000, febrero
    assert costo_minimo(febrero) == 135000, febrero

    mes_31 = [3] * 31
    assert costo_minimo(mes_31) == 144500, mes_31
    assert costo_regla_actual(mes_31) == 144500, mes_31


def probar_ejemplo_a_mano() -> None:
    """Verifica el ejemplo pequeño resuelto a mano en el README."""
    viajes = [3, 3, 1, 0, 3, 3, 2, 1]
    esperado = 39900

    assert costo_minimo(viajes) == esperado
    assert costo_exhaustivo(viajes) == esperado


def probar_contra_exhaustiva() -> None:
    """Verifica al menos 20 instancias aleatorias con semilla fija."""
    rng = random.Random(2026)

    for _ in range(25):
        dias = rng.randint(1, 8)
        viajes = []

        for _ in range(dias):
            viajes.append(rng.randint(0, 4))

        esperado = costo_exhaustivo(viajes)
        obtenido = costo_minimo(viajes)

        assert obtenido == esperado, viajes


def probar_restriccion_negocio() -> None:
    """La devolución es exactamente lo cobrado menos el mínimo."""
    viajes = [3, 3, 1, 0, 3, 3, 2, 1]
    minimo = 39900

    assert liquidar_tope(viajes, 50000) == 10100
    assert liquidar_tope(viajes, minimo) == 0
    assert liquidar_tope(viajes, 30000) == 0


def probar_contraejemplo() -> None:
    """La regla actual cobra más que el mínimo en el contraejemplo."""
    viajes = [0, 0, 0, 0, 0, 3, 3, 3, 3]

    costo_regla = costo_regla_actual(viajes)
    costo_optimo = costo_minimo(viajes)

    assert costo_regla == 38000, viajes
    assert costo_optimo == 36000, viajes
    assert costo_regla > costo_optimo, viajes

    contra = [0, 0, 0] + [3] * 7 + [0] * 20
    assert costo_regla_actual(contra) == 64500, contra
    assert costo_minimo(contra) == 36000, contra
    assert liquidar_tope(contra, 64500) == 28500, contra


if __name__ == "__main__":
    probar_casos_limite()
    probar_ejemplo_a_mano()
    probar_contra_exhaustiva()
    probar_restriccion_negocio()
    probar_contraejemplo()
    print("Todas las pruebas pasaron")