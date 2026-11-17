"""Experimentos de tiempo y operaciones, y gráficas del tope tarifario.

Ejecutar desde la raíz del repositorio:
    python src/tope_tarifario/medicion.py
"""

import time
from pathlib import Path

import matplotlib.pyplot as plt

CARPETA_GRAFICAS = Path(__file__).resolve().parents[2] / "graficas" / "tope_tarifario"
REPETICIONES: int = 5


def medir_tiempo(funcion, instancias: list[list[int]]) -> float:
    """Mide el tiempo medio de una solución sobre las mismas instancias.

    Args:
        funcion: solución a medir (estrategia, exhaustiva o regla actual).
        instancias: instancias ya generadas (no se cronometra su creación).

    Returns:
        Tiempo medio por instancia, en segundos.
    """
    # TODO: usar time.perf_counter() solo alrededor de la llamada.
    raise NotImplementedError


def graficar(
    tamanos: list[int], series: dict[str, list[float]], eje_y: str, archivo: str
) -> None:
    """Dibuja varias series en los mismos ejes y guarda la imagen.

    Args:
        tamanos: valores de d (días del periodo).
        series: nombre de la solución -> valores medidos.
        eje_y: rótulo del eje y, con unidades.
        archivo: nombre del PNG dentro de graficas/tope_tarifario/.
    """
    # TODO: título, ejes rotulados con unidades y leyenda.
    raise NotImplementedError


if __name__ == "__main__":
    CARPETA_GRAFICAS.mkdir(parents=True, exist_ok=True)
    # TODO: al menos 6 tamaños (con una pareja d y 2d), verificar dentro del
    # experimento que estrategia == exhaustiva, y producir
    # tiempo_vs_n.png y operaciones_vs_n.png.
