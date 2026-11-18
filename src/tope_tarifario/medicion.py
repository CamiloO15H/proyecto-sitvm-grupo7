"""Experimentos de tiempo y operaciones, y gráficas del tope tarifario.

Ejecutar desde la raíz del repositorio, con el entorno activado:
    python src/tope_tarifario/medicion.py

Produce en graficas/tope_tarifario/:
    tiempo_vs_n.png, operaciones_vs_n.png, tiempo_dp_periodos_largos.png
    y resultados.md (las tablas para pegar en el README).
"""

import platform
import time
from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt

from datos import generar_instancias
from estrategia import costo_minimo, costo_minimo_contado
from exhaustivo import (
    costo_combinaciones,
    costo_combinaciones_contado,
    costo_exhaustivo,
    costo_exhaustivo_contado,
)
from regla_actual import costo_regla_actual, costo_regla_actual_contado

CARPETA = Path(__file__).resolve().parents[2] / "graficas" / "tope_tarifario"

REPETICIONES: int = 5
"""Veces que se repite cada medición para promediar el ruido del sistema."""

TARJETAS_POR_TAMANO: int = 20
"""Instancias (tarjetas) que se miden en cada tamaño."""

TAMANOS_A: list[int] = [5, 10, 15, 20, 25, 30, 40]
"""Experimento A: DP, exhaustiva y regla; parejas d y 2d: 10-20, 20-40."""

TAMANOS_B: list[int] = [30, 60, 120, 240, 480, 960, 1920, 3840, 7680]
"""Experimento B: solo DP y regla, en periodos largos."""

TAMANOS_C: list[int] = [3, 4, 5, 6, 7, 8]
"""Experimento C: todas las combinaciones (4^d); solo tamaños muy pequeños."""

TARJETAS_C: int = 3
"""Instancias por tamaño en el experimento C (pueden tardar segundos)."""

TARJETAS_REALES: int = 950_000
"""Tarjetas usadas al menos una vez al mes, según el cliente."""

DIAS_MES: int = 30
"""Tamaño de un mes para la extrapolación."""

VENTANA_H: float = 4.0
"""Ventana operativa de la noche de cierre (00:00 a 04:00), en horas."""

POTENCIA_KW: float = 0.5
"""Potencia del servidor bajo carga sostenida: 500 W."""

CIERRES_POR_ANO: int = 12
"""Noches de cierre de mes en un año."""

Solucion = Callable[[list[int]], int]
SolucionContada = Callable[[list[int]], tuple[int, int]]


def medir_tiempo(
    funcion: Solucion, instancias: list[list[int]], repeticiones: int
) -> float:
    """Mide el tiempo medio de una solución sobre las mismas instancias.

    Solo se cronometra la llamada a la solución, nunca la generación de datos.

    Args:
        funcion: solución a medir (estrategia, exhaustiva o regla actual).
        instancias: instancias ya generadas.
        repeticiones: veces que se recorre todo el conjunto de instancias.

    Returns:
        Tiempo medio por instancia, en segundos.
    """
    total = 0.0
    for _ in range(repeticiones):
        for viajes in instancias:
            inicio = time.perf_counter()
            funcion(viajes)
            total += time.perf_counter() - inicio
    return total / (repeticiones * len(instancias))


def contar_operaciones(
    funcion: SolucionContada, instancias: list[list[int]]
) -> float:
    """Calcula el número medio de operaciones (opciones evaluadas).

    Args:
        funcion: versión contada de la solución; devuelve (costo, operaciones).
        instancias: instancias ya generadas.

    Returns:
        Operaciones medias por instancia.
    """
    total = 0
    for viajes in instancias:
        _, operaciones = funcion(viajes)
        total += operaciones
    return total / len(instancias)


def verificar_iguales(instancias: list[list[int]]) -> None:
    """Comprueba en el experimento que la DP da lo mismo que la exhaustiva.

    Args:
        instancias: instancias donde ambas soluciones alcanzan a correr.

    Raises:
        AssertionError: si alguna instancia da costos distintos.
    """
    for viajes in instancias:
        assert costo_minimo(viajes) == costo_exhaustivo(viajes), viajes


def graficar(
    series: dict[str, tuple[list[int], list[float]]],
    titulo: str,
    eje_y: str,
    archivo: str,
    escala_log: bool,
) -> None:
    """Dibuja varias series en los mismos ejes y guarda la imagen.

    Args:
        series: nombre de la solución -> (tamaños, valores medidos).
        titulo: título de la gráfica.
        eje_y: rótulo del eje y, con unidades.
        archivo: nombre del PNG dentro de graficas/tope_tarifario/.
        escala_log: True para usar escala logarítmica en el eje y.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    for nombre, (tamanos, valores) in series.items():
        ax.plot(tamanos, valores, marker="o", label=nombre)
    if escala_log:
        ax.set_yscale("log")
    ax.set_title(titulo)
    ax.set_xlabel("d: días del periodo (días)")
    ax.set_ylabel(eje_y)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(CARPETA / archivo, dpi=150)
    plt.close(fig)


def experimento_a() -> dict[str, dict[str, list[float]]]:
    """Mide DP, exhaustiva y regla actual en tamaños donde las tres corren.

    Returns:
        Por solución, las listas "tiempo" (s) y "operaciones".
    """
    soluciones: dict[str, tuple[Solucion, SolucionContada]] = {
        "Programación dinámica": (costo_minimo, costo_minimo_contado),
        "Exhaustiva (recursiva)": (costo_exhaustivo, costo_exhaustivo_contado),
        "Regla actual": (costo_regla_actual, costo_regla_actual_contado),
    }
    resultados = {n: {"tiempo": [], "operaciones": []} for n in soluciones}
    for d in TAMANOS_A:
        instancias = generar_instancias(d, TARJETAS_POR_TAMANO)
        verificar_iguales(instancias)
        for nombre, (funcion, contada) in soluciones.items():
            resultados[nombre]["tiempo"].append(
                medir_tiempo(funcion, instancias, REPETICIONES)
            )
            resultados[nombre]["operaciones"].append(
                contar_operaciones(contada, instancias)
            )
        print(f"  A: d = {d} listo")
    return resultados


def experimento_b() -> dict[str, dict[str, list[float]]]:
    """Mide solo DP y regla actual en periodos largos.

    Returns:
        Por solución, las listas "tiempo" (s) y "operaciones".
    """
    soluciones: dict[str, tuple[Solucion, SolucionContada]] = {
        "Programación dinámica": (costo_minimo, costo_minimo_contado),
        "Regla actual": (costo_regla_actual, costo_regla_actual_contado),
    }
    resultados = {n: {"tiempo": [], "operaciones": []} for n in soluciones}
    for d in TAMANOS_B:
        instancias = generar_instancias(d, TARJETAS_POR_TAMANO)
        for nombre, (funcion, contada) in soluciones.items():
            resultados[nombre]["tiempo"].append(
                medir_tiempo(funcion, instancias, REPETICIONES)
            )
            resultados[nombre]["operaciones"].append(
                contar_operaciones(contada, instancias)
            )
        print(f"  B: d = {d} listo")
    return resultados


def experimento_c() -> dict[str, list[float]]:
    """Mide la exploración de todas las combinaciones en tamaños muy pequeños.

    Returns:
        Las listas "tiempo" (s) y "operaciones".
    """
    resultados: dict[str, list[float]] = {"tiempo": [], "operaciones": []}
    for d in TAMANOS_C:
        instancias = generar_instancias(d, TARJETAS_C)
        for viajes in instancias:
            assert costo_combinaciones(viajes) == costo_minimo(viajes), viajes
        resultados["tiempo"].append(
            medir_tiempo(costo_combinaciones, instancias, 1)
        )
        resultados["operaciones"].append(
            contar_operaciones(costo_combinaciones_contado, instancias)
        )
        print(f"  C: d = {d} listo")
    return resultados


def experimento_d(cantidad: int = 1000) -> tuple[float, float, float]:
    """Estima cuánto cobra de más la regla actual en meses sintéticos.

    Args:
        cantidad: tarjetas sintéticas de 30 días que se comparan.

    Returns:
        (fracción de tarjetas con sobrecobro, sobrecobro medio por tarjeta en
        pesos, sobrecobro máximo en pesos).
    """
    instancias = generar_instancias(DIAS_MES, cantidad, semilla=7)
    diferencias = [costo_regla_actual(v) - costo_minimo(v) for v in instancias]
    con_sobrecobro = sum(1 for x in diferencias if x > 0)
    return (
        con_sobrecobro / cantidad,
        sum(diferencias) / cantidad,
        max(diferencias),
    )


def factor(valores: list[float], tamanos: list[int], d: int) -> float:
    """Calcula cuánto se multiplica un valor al pasar de d a 2d.

    Args:
        valores: valores medidos, alineados con tamanos.
        tamanos: tamaños medidos.
        d: tamaño de partida; 2d también debe estar en tamanos.

    Returns:
        valor(2d) / valor(d).
    """
    return valores[tamanos.index(2 * d)] / valores[tamanos.index(d)]


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


def extrapolar(segundos_por_tarjeta: float) -> tuple[float, float, float]:
    """Lleva el tiempo de una tarjeta al volumen real de un cierre de mes.

    La DP y la regla son lineales en d y cada tarjeta es independiente, así
    que el tiempo total es el de una tarjeta por el número de tarjetas.

    Args:
        segundos_por_tarjeta: tiempo medio medido con d = 30.

    Returns:
        (horas por cierre, kWh por cierre, kWh por año).
    """
    horas = segundos_por_tarjeta * TARJETAS_REALES / 3600
    kwh = POTENCIA_KW * horas
    return horas, kwh, kwh * CIERRES_POR_ANO


def main() -> None:
    """Corre los tres experimentos, genera las gráficas y las tablas."""
    CARPETA.mkdir(parents=True, exist_ok=True)
    print("Midiendo... (tarda alrededor de un minuto)")
    a = experimento_a()
    b = experimento_b()
    c = experimento_c()

    graficar(
        {n: (TAMANOS_A, r["tiempo"]) for n, r in a.items()}
        | {"Todas las combinaciones (4^d)": (TAMANOS_C, c["tiempo"])},
        "Tope tarifario: tiempo por tarjeta frente a los días del periodo",
        "Tiempo medio por tarjeta (s, escala log)",
        "tiempo_vs_n.png",
        escala_log=True,
    )
    graficar(
        {n: (TAMANOS_A, r["operaciones"]) for n, r in a.items()}
        | {"Todas las combinaciones (4^d)": (TAMANOS_C, c["operaciones"])},
        "Tope tarifario: operaciones por tarjeta frente a los días",
        "Opciones evaluadas por tarjeta (escala log)",
        "operaciones_vs_n.png",
        escala_log=True,
    )
    graficar(
        {n: (TAMANOS_B, r["tiempo"]) for n, r in b.items()},
        "Programación dinámica y regla actual en periodos largos",
        "Tiempo medio por tarjeta (s)",
        "tiempo_dp_periodos_largos.png",
        escala_log=False,
    )

    equipo = platform.processor() or platform.machine()
    sistema = f"{platform.system()} {platform.release()}"
    salida = [
        "# Resultados de la medición\n\n"
        f"Equipo: {equipo}, {sistema}, Python {platform.python_version()}. "
        f"Semilla 2026, {TARJETAS_POR_TAMANO} tarjetas por tamaño, "
        f"{REPETICIONES} repeticiones.\n"
    ]

    filas = []
    for i, d in enumerate(TAMANOS_A):
        fila = [str(d)]
        for r in a.values():
            fila += [f"{r['tiempo'][i]:.2e}", f"{r['operaciones'][i]:.0f}"]
        filas.append(fila)
    encabezado = ["d"]
    for n in a:
        encabezado += [f"{n}: tiempo (s)", f"{n}: operaciones"]
    salida.append("## Experimento A\n\n" + tabla_markdown(encabezado, filas))

    filas = []
    for i, d in enumerate(TAMANOS_B):
        fila = [str(d)]
        for r in b.values():
            fila += [f"{r['tiempo'][i]:.2e}", f"{r['operaciones'][i]:.0f}"]
        filas.append(fila)
    encabezado = ["d"]
    for n in b:
        encabezado += [f"{n}: tiempo (s)", f"{n}: operaciones"]
    salida.append("## Experimento B\n\n" + tabla_markdown(encabezado, filas))

    filas = [
        [str(d), f"{c['tiempo'][i]:.2e}", f"{c['operaciones'][i]:.0f}"]
        for i, d in enumerate(TAMANOS_C)
    ]
    salida.append(
        "## Experimento C (todas las combinaciones)\n\n"
        + tabla_markdown(["d", "tiempo (s)", "operaciones"], filas)
    )

    filas = []
    for nombre, r, tamanos in [(n, r, TAMANOS_A) for n, r in a.items()] + [
        (n + " (B)", r, TAMANOS_B) for n, r in b.items()
    ]:
        pares = (
            [(10, 20), (20, 40)]
            if tamanos is TAMANOS_A
            else [(960, 1920), (3840, 7680)]
        )
        for d1, _ in pares:
            filas.append(
                [
                    nombre,
                    f"{d1} → {2 * d1}",
                    f"{factor(r['tiempo'], tamanos, d1):.2f}",
                    f"{factor(r['operaciones'], tamanos, d1):.2f}",
                ]
            )
    salida.append(
        "## Factor al duplicar d\n\n"
        + tabla_markdown(
            [
                "Solución",
                "d → 2d",
                "Factor de tiempo",
                "Factor de operaciones",
            ],
            filas,
        )
    )

    filas = []
    i30 = TAMANOS_A.index(DIAS_MES)
    for nombre, r in a.items():
        horas, kwh, anual = extrapolar(r["tiempo"][i30])
        cabe = "sí" if horas <= VENTANA_H else "no"
        filas.append(
            [
                nombre,
                f"{r['tiempo'][i30]:.2e}",
                f"{horas:.4f}",
                cabe,
                f"{kwh:.4f}",
                f"{anual:.3f}",
            ]
        )
    # Todas las combinaciones: se extrapola con el tiempo por combinación
    # medido en el tamaño mayor y las 4^30 combinaciones de un mes.
    seg_por_combinacion = c["tiempo"][-1] / c["operaciones"][-1]
    seg_tarjeta = seg_por_combinacion * 4**DIAS_MES
    horas, kwh, anual = extrapolar(seg_tarjeta)
    filas.append(
        [
            "Todas las combinaciones (4^d)",
            f"{seg_tarjeta:.2e}",
            f"{horas:.2e}",
            "no",
            f"{kwh:.2e}",
            f"{anual:.2e}",
        ]
    )
    salida.append(
        f"## Extrapolación a {TARJETAS_REALES:,} tarjetas, d = {DIAS_MES}\n\n"
        + tabla_markdown(
            [
                "Solución",
                "s por tarjeta",
                "Horas por cierre",
                f"¿Cabe en {VENTANA_H:.0f} h?",
                "kWh por cierre",
                "kWh por año (12 cierres)",
            ],
            filas,
        )
    )

    fraccion, medio, maximo = experimento_d()
    salida.append(
        "## Sobrecobro de la regla actual (1.000 tarjetas de 30 días)\n\n"
        + tabla_markdown(
            [
                "Tarjetas con sobrecobro",
                "Sobrecobro medio por tarjeta",
                "Sobrecobro máximo",
                f"Si se repitiera en {TARJETAS_REALES:,} tarjetas",
            ],
            [
                [
                    f"{fraccion:.1%}",
                    f"${medio:,.0f}",
                    f"${maximo:,.0f}",
                    f"${medio * TARJETAS_REALES:,.0f} por mes",
                ]
            ],
        )
    )

    texto = "\n\n".join(salida) + "\n"
    (CARPETA / "resultados.md").write_text(texto, encoding="utf-8")
    print(texto)
    print(f"Gráficas y tablas guardadas en {CARPETA}")


if __name__ == "__main__":
    main()