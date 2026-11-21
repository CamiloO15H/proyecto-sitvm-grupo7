"""Mide el proceso actual y estima su costo en el volumen real (línea base).

Ejecutar desde la raíz del repositorio, con el entorno activado:
    python src/linea_base/medicion.py

Produce en graficas/linea_base/: tiempo_vs_n.png y resultados.md.
"""

import platform
import time
from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt

from datos import generar_saldos, generar_validaciones
from proceso_actual import deduplicar_actual, ordenar_actual
from proceso_actual import tramo_maximo_actual

CARPETA = Path(__file__).resolve().parents[2] / "graficas" / "linea_base"

TAMANOS: list[int] = [500, 1000, 2000, 3000, 4000, 8000]
"""Tamaños medidos; incluyen las parejas 500-1000, 1000-2000 y 4000-8000."""

REPETICIONES: int = 3
"""Veces que se repite cada medición para promediar el ruido."""

POTENCIA_KW: float = 0.5
"""Servidor de 500 W bajo carga sostenida."""

VALIDACIONES_DIA: int = 1_400_000
"""Validaciones de un día hábil típico."""

PROPORCION_UNICAS: float = 0.935
"""Fracción que queda tras quitar las repetidas (6,5 % repetidas)."""

INTERVALOS_HISTORICO: int = 166_000
"""Intervalos de 5 minutos por estación en dos años."""

ESTACIONES: int = 80
"""Estaciones de metro y cable."""

EJECUCIONES_ANO: dict[str, int] = {
    "1. Deduplicación": 365,
    "2. Ordenamiento": 365,
    "3. Franjas de congestión": 12,
}
"""Veces al año que corre cada operación (supuesto del equipo para la 3)."""


def medir(funcion: Callable, entrada: list, repeticiones: int) -> float:
    """Mide el tiempo medio de una llamada, sin contar la generación de datos.

    Args:
        funcion: operación del proceso actual.
        entrada: datos ya generados.
        repeticiones: veces que se repite la llamada.

    Returns:
        Tiempo medio en segundos.
    """
    total = 0.0
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        funcion(entrada)
        total += time.perf_counter() - inicio
    return total / repeticiones


def constante_cuadratica(tamanos: list[int], tiempos: list[float]) -> float:
    """Estima c en t ≈ c·n² con los tres tamaños mayores (menos ruido).

    Args:
        tamanos: tamaños medidos.
        tiempos: tiempos medidos, alineados con tamanos.

    Returns:
        Segundos por n².
    """
    pares = list(zip(tamanos, tiempos))[-3:]
    return sum(t / n**2 for n, t in pares) / len(pares)


def tabla_markdown(encabezado: list[str], filas: list[list[str]]) -> str:
    """Arma una tabla en formato Markdown.

    Args:
        encabezado: títulos de las columnas.
        filas: celdas de cada fila, ya formateadas.

    Returns:
        La tabla como texto.
    """
    lineas = ["| " + " | ".join(encabezado) + " |"]
    lineas.append("|" + " --- |" * len(encabezado))
    for fila in filas:
        lineas.append("| " + " | ".join(fila) + " |")
    return "\n".join(lineas)


def main() -> None:
    """Mide las tres operaciones, grafica y extrapola al volumen real."""
    CARPETA.mkdir(parents=True, exist_ok=True)
    print("Midiendo el proceso actual... (tarda alrededor de un minuto)")
    tiempos: dict[str, list[float]] = {n: [] for n in EJECUCIONES_ANO}
    operaciones: dict[str, list[int]] = {n: [] for n in EJECUCIONES_ANO}
    for n in TAMANOS:
        validaciones = generar_validaciones(n)
        aceptadas, comparaciones = deduplicar_actual(validaciones)
        tiempos["1. Deduplicación"].append(
            medir(deduplicar_actual, validaciones, REPETICIONES)
        )
        operaciones["1. Deduplicación"].append(comparaciones)

        ordenadas, comparaciones = ordenar_actual(aceptadas)
        assert ordenadas == sorted(aceptadas, key=lambda v: (v[1], v[3]))
        tiempos["2. Ordenamiento"].append(
            medir(ordenar_actual, aceptadas, REPETICIONES)
        )
        operaciones["2. Ordenamiento"].append(comparaciones)

        saldos = generar_saldos(n)
        *_, tramos = tramo_maximo_actual(saldos)
        tiempos["3. Franjas de congestión"].append(
            medir(tramo_maximo_actual, saldos, REPETICIONES)
        )
        operaciones["3. Franjas de congestión"].append(tramos)
        print(f"  n = {n} listo")

    fig, ax = plt.subplots(figsize=(8, 5))
    for nombre, valores in tiempos.items():
        ax.plot(TAMANOS, valores, marker="o", label=nombre)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Proceso actual: tiempo frente al tamaño de la entrada")
    ax.set_xlabel("n: registros o intervalos (escala log)")
    ax.set_ylabel("Tiempo medio (s, escala log)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(CARPETA / "tiempo_vs_n.png", dpi=150)
    plt.close(fig)

    equipo = platform.processor() or platform.machine()
    sistema = f"{platform.system()} {platform.release()}"
    salida = [
        "# Línea base del proceso actual\n\n"
        f"Equipo: {equipo}, {sistema}, Python {platform.python_version()}. "
        f"Semilla 2026, {REPETICIONES} repeticiones por tamaño.\n"
    ]
    filas = []
    for i, n in enumerate(TAMANOS):
        fila = [str(n)]
        for nombre in EJECUCIONES_ANO:
            fila += [
                f"{tiempos[nombre][i]:.3e}",
                f"{operaciones[nombre][i]:,}",
            ]
        filas.append(fila)
    encabezado = ["n"]
    for nombre in EJECUCIONES_ANO:
        encabezado += [f"{nombre}: tiempo (s)", f"{nombre}: operaciones"]
    salida.append("## Mediciones\n\n" + tabla_markdown(encabezado, filas))

    filas = []
    for nombre in EJECUCIONES_ANO:
        for d1, d2 in [(1000, 2000), (4000, 8000)]:
            i1, i2 = TAMANOS.index(d1), TAMANOS.index(d2)
            filas.append(
                [
                    nombre,
                    f"{d1} → {d2}",
                    f"{tiempos[nombre][i2] / tiempos[nombre][i1]:.2f}",
                    f"{operaciones[nombre][i2] / operaciones[nombre][i1]:.2f}",
                ]
            )
    salida.append(
        "## Factor al duplicar n (esperado ≈ 4 por ser Θ(n²))\n\n"
        + tabla_markdown(
            [
                "Operación",
                "n → 2n",
                "Factor de tiempo",
                "Factor de operaciones",
            ],
            filas,
        )
    )

    volumen = {
        "1. Deduplicación": (VALIDACIONES_DIA, 1),
        "2. Ordenamiento": (int(VALIDACIONES_DIA * PROPORCION_UNICAS), 1),
        "3. Franjas de congestión": (INTERVALOS_HISTORICO, ESTACIONES),
    }
    filas = []
    total_noche = 0.0
    total_ano = 0.0
    for nombre, (n_real, veces) in volumen.items():
        c = constante_cuadratica(TAMANOS, tiempos[nombre])
        horas = c * n_real**2 * veces / 3600
        kwh = POTENCIA_KW * horas
        anual = kwh * EJECUCIONES_ANO[nombre]
        total_ano += anual
        if EJECUCIONES_ANO[nombre] == 365:
            total_noche += horas
        filas.append(
            [
                nombre,
                f"{n_real:,}" + (f" × {veces}" if veces > 1 else ""),
                f"{c:.3e}",
                f"{horas:,.1f}",
                f"{kwh:,.2f}",
                str(EJECUCIONES_ANO[nombre]),
                f"{anual:,.0f}",
            ]
        )
    salida.append(
        "## Extrapolación al volumen real (t ≈ c·n²)\n\n"
        + tabla_markdown(
            [
                "Operación",
                "n real",
                "c (s por n²)",
                "Horas por ejecución",
                "kWh por ejecución",
                "Ejecuciones al año",
                "kWh al año",
            ],
            filas,
        )
        + f"\n\nOperaciones 1 y 2 juntas: {total_noche:,.1f} h por noche "
        f"(ventana de 4 h). Total de las operaciones 1 a 3: "
        f"{total_ano:,.0f} kWh al año."
    )

    texto = "\n\n".join(salida) + "\n"
    (CARPETA / "resultados.md").write_text(texto, encoding="utf-8")
    print(texto)
    print(f"Gráfica y tablas guardadas en {CARPETA}")


if __name__ == "__main__":
    main()