"""Mediciones reproducibles de las estrategias de franjas de congestion.

Ejecutar desde la raiz del repositorio:
    python src/franjas_congestion/medicion.py

Requiere los modulos fuerza_bruta.py, divide_venceras.py y kadane.py de
la misma carpeta, con las firmas acordadas por el equipo.
"""

import math
import platform
import time
from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt

from datos import generar_saldos
from divide_venceras import (
    tramo_divide_venceras,
    tramo_divide_venceras_contado,
)
from fuerza_bruta import tramo_fuerza_bruta, tramo_fuerza_bruta_contado
from kadane import tramo_kadane, tramo_kadane_contado

Tramo = tuple[int, int, int]
Algoritmo = Callable[[list[int]], Tramo]
AlgoritmoContado = Callable[[list[int]], tuple[Tramo, int]]

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "graficas" / "franjas_congestion"
REPETICIONES = 5
SEMILLA = 2026
TAMANOS_A = [250, 500, 1000, 2000, 4000]
TAMANOS_B = [4000, 8000, 16000, 32000, 64000, 128000, 256000]
N_REAL = 166000
ESTACIONES = 80
POTENCIA_KW = 0.5
EJECUCIONES_ANO = 12

ALGORITMOS: dict[str, tuple[Algoritmo, AlgoritmoContado]] = {
    "Fuerza bruta": (tramo_fuerza_bruta, tramo_fuerza_bruta_contado),
    "Divide y venceras": (
        tramo_divide_venceras,
        tramo_divide_venceras_contado,
    ),
    "Kadane": (tramo_kadane, tramo_kadane_contado),
}


def comprobar_tramo(saldos: list[int], tramo: Tramo) -> None:
    """Comprueba que el resultado describe un tramo no vacio valido.

    Args:
        saldos: Serie de saldos, con al menos un elemento.
        tramo: Tupla (suma, inicio, fin) con extremos incluidos.

    Raises:
        AssertionError: Si indices o suma son incorrectos.
    """
    valor, inicio, fin = tramo
    assert 0 <= inicio <= fin < len(saldos), (len(saldos), tramo)
    assert sum(saldos[inicio:fin + 1]) == valor, tramo


def verificar_instancia(saldos: list[int], nombres: list[str]) -> None:
    """Verifica acuerdo en suma optima, integridad y no mutacion.

    Args:
        saldos: Serie sintetica de entrada.
        nombres: Algoritmos a comparar, segun ALGORITMOS.
    """
    original = saldos.copy()
    sumas = []
    for nombre in nombres:
        tramo = ALGORITMOS[nombre][0](saldos)
        comprobar_tramo(saldos, tramo)
        assert saldos == original, f"{nombre} modifico la entrada"
        sumas.append(tramo[0])
    assert len(set(sumas)) == 1, dict(zip(nombres, sumas))


def medir_tiempo(algoritmo: Algoritmo, saldos: list[int]) -> float:
    """Obtiene el tiempo medio en segundos sin medir la generacion de datos.

    Args:
        algoritmo: Funcion que resuelve el subarreglo maximo.
        saldos: Una instancia fija generada antes del cronometro.

    Returns:
        Tiempo medio por ejecucion, en segundos.
    """
    total = 0.0
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        algoritmo(saldos)
        total += time.perf_counter() - inicio
    return total / REPETICIONES


def medir_series(
    tamanos: list[int], nombres: list[str]
) -> dict[str, dict[str, list[float]]]:
    """Mide tiempo y operaciones de cada algoritmo sobre identicas series.

    Args:
        tamanos: Longitudes de las series de entrada.
        nombres: Nombre de cada algoritmo a medir.

    Returns:
        Diccionario con listas de tiempos y operaciones por algoritmo.
    """
    resultados = {
        nombre: {"tiempo": [], "operaciones": []} for nombre in nombres
    }
    for n in tamanos:
        saldos = generar_saldos(n, SEMILLA)
        verificar_instancia(saldos, nombres)
        for nombre in nombres:
            algoritmo, contado = ALGORITMOS[nombre]
            tiempo = medir_tiempo(algoritmo, saldos)
            tramo, operaciones = contado(saldos)
            comprobar_tramo(saldos, tramo)
            assert operaciones >= 0, (nombre, n, operaciones)
            if nombre == "Fuerza bruta":
                assert operaciones == n * (n + 1) // 2
            elif nombre == "Kadane":
                assert operaciones == n
            resultados[nombre]["tiempo"].append(tiempo)
            resultados[nombre]["operaciones"].append(float(operaciones))
        print(f"Medido: n = {n:,}; estrategias: {', '.join(nombres)}")
    return resultados


def graficar(
    tamanos: list[int],
    resultados: dict[str, dict[str, list[float]]],
    campo: str,
    nombre_archivo: str,
    titulo: str,
    eje_y: str,
    logaritmico: bool,
) -> None:
    """Guarda una grafica reproducible, con leyenda y unidades.

    Args:
        tamanos: Longitudes de entrada, en orden ascendente.
        resultados: Diccionario de las mediciones.
        campo: Clave "tiempo" u "operaciones".
        nombre_archivo: Archivo PNG de salida.
        titulo: Titulo de la grafica.
        eje_y: Descripcion y unidades del eje vertical.
        logaritmico: Si el eje vertical es logaritmico.
    """
    fig, ax = plt.subplots(figsize=(9, 5.2))
    for nombre, valores in resultados.items():
        ax.plot(tamanos, valores[campo], marker="o", label=nombre)
    if logaritmico:
        ax.set_yscale("log")
    ax.set_xlabel("Numero de intervalos de 5 minutos (n)")
    ax.set_ylabel(eje_y)
    ax.set_title(titulo)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(SALIDA / nombre_archivo, dpi=160)
    plt.close(fig)


def crecimiento(nombre: str, n: int) -> float:
    """Devuelve la funcion de crecimiento teorico del algoritmo.

    Args:
        nombre: Nombre de una estrategia conocida.
        n: Longitud de la entrada, siempre positiva.

    Returns:
        Termino de crecimiento asintotico sin constantes.
    """
    if nombre == "Fuerza bruta":
        return float(n * n)
    if nombre == "Divide y venceras":
        return n * math.log2(n)
    return float(n)


def extrapolar(nombre: str, tiempo_medido: float, n_medido: int) -> tuple[float, float, float]:
    """Extrapola tiempo y energia de 80 estaciones y 12 ejecuciones anuales.

    Args:
        nombre: Algoritmo medido.
        tiempo_medido: Segundos por una serie de n_medido intervalos.
        n_medido: Longitud de la serie efectivamente medida.

    Returns:
        (horas por ejecucion de las 80 estaciones, kWh por ejecucion,
        kWh por ano).
    """
    factor = crecimiento(nombre, N_REAL) / crecimiento(nombre, n_medido)
    segundos_totales = tiempo_medido * factor * ESTACIONES
    horas = segundos_totales / 3600
    return horas, POTENCIA_KW * horas, POTENCIA_KW * horas * EJECUCIONES_ANO


def tabla(encabezados: list[str], filas: list[list[str]]) -> str:
    """Construye una tabla Markdown.

    Args:
        encabezados: Titulos de las columnas.
        filas: Valores de todas las filas.

    Returns:
        Texto Markdown de la tabla.
    """
    encabezado = "| " + " | ".join(encabezados) + " |"
    separador = "| " + " | ".join("---" for _ in encabezados) + " |"
    cuerpo = ["| " + " | ".join(fila) + " |" for fila in filas]
    return "\n".join([encabezado, separador, *cuerpo])


def guardar_resultados(
    a: dict[str, dict[str, list[float]]],
    b: dict[str, dict[str, list[float]]],
) -> None:
    """Escribe las tablas, factores de duplicacion y proyecciones.

    Args:
        a: Mediciones con las tres estrategias.
        b: Mediciones largas solo con divide y venceras y Kadane.
    """
    lineas = [
        "# Resultados medidos de las franjas de congestion",
        "",
        f"Equipo: {platform.platform()}; Python {platform.python_version()}.",
        f"Semilla base {SEMILLA} + n, {REPETICIONES} repeticiones por algoritmo y tamano.",
        "Solo se cronometra el algoritmo; datos sinteticos creados antes.",
        "",
        "## Experimento A: tres algoritmos",
        "",
    ]
    encabezados = ["n"]
    for nombre in a:
        encabezados += [f"{nombre}: tiempo (s)", f"{nombre}: operaciones"]
    filas = []
    for i, n in enumerate(TAMANOS_A):
        fila = [str(n)]
        for valores in a.values():
            fila += [f"{valores['tiempo'][i]:.6g}", f"{valores['operaciones'][i]:.0f}"]
        filas.append(fila)
    lineas += [tabla(encabezados, filas), "", "## Experimento B: escalabilidad", ""]
    encabezados = ["n"]
    for nombre in b:
        encabezados += [f"{nombre}: tiempo (s)", f"{nombre}: operaciones"]
    filas = []
    for i, n in enumerate(TAMANOS_B):
        fila = [str(n)]
        for valores in b.values():
            fila += [f"{valores['tiempo'][i]:.6g}", f"{valores['operaciones'][i]:.0f}"]
        filas.append(fila)
    lineas += [tabla(encabezados, filas), "", "## Factor al duplicar n", ""]
    filas = []
    for nombre, valores in a.items():
        for n in [250, 500, 1000, 2000]:
            i = TAMANOS_A.index(n)
            j = TAMANOS_A.index(n * 2)
            filas.append([
                nombre,
                f"{n} -> {2*n}",
                f"{valores['tiempo'][j] / valores['tiempo'][i]:.2f}",
                f"{valores['operaciones'][j] / valores['operaciones'][i]:.2f}",
            ])
    for nombre, valores in b.items():
        for n in [32000, 128000]:
            i = TAMANOS_B.index(n)
            j = TAMANOS_B.index(n * 2)
            filas.append([
                nombre,
                f"{n} -> {2*n}",
                f"{valores['tiempo'][j] / valores['tiempo'][i]:.2f}",
                f"{valores['operaciones'][j] / valores['operaciones'][i]:.2f}",
            ])
    lineas += [
        tabla(["Estrategia", "n -> 2n", "Factor tiempo", "Factor operaciones"], filas),
        "",
        "## Extrapolacion a 166000 intervalos por estacion, 80 estaciones",
        "",
        "Supuestos: una serie independiente por estacion; ejecucion secuencial; "
        "servidor a 0,5 kW bajo carga sostenida; 12 ejecuciones por ano.",
        "Los tiempos se extrapolan segun la complejidad teorica y son estimaciones.",
        "",
    ]
    filas = []
    for nombre in ALGORITMOS:
        valores = a if nombre == "Fuerza bruta" else b
        tamanos = TAMANOS_A if nombre == "Fuerza bruta" else TAMANOS_B
        tiempo = valores[nombre]["tiempo"][-1]
        horas, energia, anual = extrapolar(nombre, tiempo, tamanos[-1])
        filas.append([nombre, f"{tiempo:.6g}", str(tamanos[-1]), f"{horas:.5g}", f"{energia:.5g}", f"{anual:.5g}"])
    lineas += [
        tabla(["Estrategia", "Tiempo base (s)", "n medido", "Horas / ejecucion", "kWh / ejecucion", "kWh / ano"], filas),
        "",
        "**Nota:** la operacion 3 se extrapola con 12 ejecuciones por ano segun "
        "la convencion del equipo; la ventana de cuatro horas del caso "
        "esta fijada expresamente para las operaciones 1, 2 y 4.",
        "",
    ]
    (SALIDA / "resultados.md").write_text("\n".join(lineas), encoding="utf-8")


def main() -> None:
    """Ejecuta las mediciones y crea tres imagenes y un reporte Markdown."""
    SALIDA.mkdir(parents=True, exist_ok=True)
    nombres_a = list(ALGORITMOS)
    nombres_b = ["Divide y venceras", "Kadane"]
    a = medir_series(TAMANOS_A, nombres_a)
    b = medir_series(TAMANOS_B, nombres_b)
    graficar(
        TAMANOS_A, a, "tiempo", "tiempo_vs_n.png",
        "Franjas de congestion: tiempo por estrategia",
        "Tiempo medio (s, escala logaritmica)", True,
    )
    graficar(
        TAMANOS_A, a, "operaciones", "operaciones_vs_n.png",
        "Franjas de congestion: opciones u operaciones evaluadas",
        "Operaciones contadas (escala logaritmica)", True,
    )
    graficar(
        TAMANOS_B, b, "tiempo", "tiempo_largo.png",
        "Franjas de congestion: rendimiento con series largas",
        "Tiempo medio (s)", False,
    )
    guardar_resultados(a, b)
    print(f"Archivos generados en {SALIDA}")


if __name__ == "__main__":
    main()
