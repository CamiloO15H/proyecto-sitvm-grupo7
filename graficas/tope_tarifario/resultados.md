# Resultados de la medición

Equipo: AMD64 Family 25 Model 97 Stepping 2, AuthenticAMD, Windows 11, Python 3.13.3. Semilla 2026, 20 tarjetas por tamaño, 5 repeticiones.


## Experimento A

| d | Programación dinámica: tiempo (s) | Programación dinámica: operaciones | Exhaustiva (recursiva): tiempo (s) | Exhaustiva (recursiva): operaciones | Regla actual: tiempo (s) | Regla actual: operaciones |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 1.14e-06 | 13 | 1.55e-06 | 13 | 7.17e-07 | 14 |
| 10 | 2.02e-06 | 28 | 4.74e-06 | 41 | 1.10e-06 | 26 |
| 15 | 2.92e-06 | 42 | 1.23e-05 | 129 | 1.62e-06 | 38 |
| 20 | 4.39e-06 | 56 | 6.35e-05 | 407 | 1.88e-06 | 48 |
| 25 | 4.65e-06 | 70 | 1.07e-04 | 1162 | 2.24e-06 | 60 |
| 30 | 5.89e-06 | 84 | 3.10e-04 | 3482 | 2.88e-06 | 72 |
| 40 | 7.53e-06 | 112 | 2.84e-03 | 30596 | 4.42e-06 | 94 |

## Experimento B

| d | Programación dinámica: tiempo (s) | Programación dinámica: operaciones | Regla actual: tiempo (s) | Regla actual: operaciones |
| --- | --- | --- | --- | --- |
| 30 | 7.04e-06 | 84 | 2.68e-06 | 72 |
| 60 | 1.52e-05 | 169 | 6.69e-06 | 140 |
| 120 | 2.30e-05 | 337 | 1.14e-05 | 278 |
| 240 | 4.86e-05 | 671 | 2.42e-05 | 552 |
| 480 | 1.16e-04 | 1346 | 5.05e-05 | 1100 |
| 960 | 2.33e-04 | 2683 | 9.09e-05 | 2198 |
| 1920 | 4.85e-04 | 5385 | 1.85e-04 | 4392 |
| 3840 | 9.52e-04 | 10742 | 3.87e-04 | 8780 |
| 7680 | 1.87e-03 | 21502 | 7.29e-04 | 17558 |

## Experimento C (todas las combinaciones)

| d | tiempo (s) | operaciones |
| --- | --- | --- |
| 3 | 7.67e-06 | 84 |
| 4 | 2.99e-05 | 340 |
| 5 | 1.30e-04 | 1364 |
| 6 | 4.66e-04 | 5460 |
| 7 | 1.82e-03 | 21844 |
| 8 | 6.84e-03 | 87380 |

## Factor al duplicar d

| Solución | d → 2d | Factor de tiempo | Factor de operaciones |
| --- | --- | --- | --- |
| Programación dinámica | 10 → 20 | 2.17 | 1.98 |
| Programación dinámica | 20 → 40 | 1.71 | 1.99 |
| Exhaustiva (recursiva) | 10 → 20 | 13.38 | 9.86 |
| Exhaustiva (recursiva) | 20 → 40 | 44.72 | 75.21 |
| Regla actual | 10 → 20 | 1.71 | 1.85 |
| Regla actual | 20 → 40 | 2.36 | 1.96 |
| Programación dinámica (B) | 960 → 1920 | 2.09 | 2.01 |
| Programación dinámica (B) | 3840 → 7680 | 1.96 | 2.00 |
| Regla actual (B) | 960 → 1920 | 2.03 | 2.00 |
| Regla actual (B) | 3840 → 7680 | 1.88 | 2.00 |

## Extrapolación a 950,000 tarjetas, d = 30

| Solución | s por tarjeta | Horas por cierre | ¿Cabe en 4 h? | kWh por cierre | kWh por año (12 cierres) |
| --- | --- | --- | --- | --- | --- |
| Programación dinámica | 5.89e-06 | 0.0016 | sí | 0.0008 | 0.009 |
| Exhaustiva (recursiva) | 3.10e-04 | 0.0817 | sí | 0.0408 | 0.490 |
| Regla actual | 2.88e-06 | 0.0008 | sí | 0.0004 | 0.005 |
| Todas las combinaciones (4^d) | 9.03e+10 | 2.38e+13 | no | 1.19e+13 | 1.43e+14 |

## Sobrecobro de la regla actual (1.000 tarjetas de 30 días)

| Tarjetas con sobrecobro | Sobrecobro medio por tarjeta | Sobrecobro máximo | Si se repitiera en 950,000 tarjetas |
| --- | --- | --- | --- |
| 1.5% | $60 | $11,400 | $56,525,000 por mes |
