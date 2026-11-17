"""Pruebas con assert de la liquidación del tope tarifario.

Ejecutar desde la raíz del repositorio:
    python src/tope_tarifario/pruebas.py
"""

from estrategia import costo_minimo, liquidar_tope
from exhaustivo import costo_exhaustivo
from regla_actual import costo_regla_actual


def probar_casos_limite() -> None:
    """Verifica mes vacío, un solo día, días sin viajes y pases que sobran."""
    # TODO


def probar_ejemplo_a_mano() -> None:
    """Verifica el ejemplo pequeño resuelto a mano en el README."""
    # TODO


def probar_contra_exhaustiva() -> None:
    """Verifica al menos 20 instancias aleatorias (semilla fija)."""
    # TODO


def probar_restriccion_negocio() -> None:
    """La devolución es exactamente lo cobrado menos el mínimo."""
    # TODO


def probar_contraejemplo() -> None:
    """La regla actual cobra más que el mínimo en la instancia del README."""
    # TODO


if __name__ == "__main__":
    probar_casos_limite()
    probar_ejemplo_a_mano()
    probar_contra_exhaustiva()
    probar_restriccion_negocio()
    probar_contraejemplo()
    print("Todas las pruebas pasaron")
