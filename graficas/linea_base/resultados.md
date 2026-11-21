# Línea base del proceso actual

Equipo: AMD64 Family 25 Model 97 Stepping 2, AuthenticAMD, Windows 11, Python 3.13.3. Semilla 2026, 3 repeticiones por tamaño.


## Mediciones

| n | 1. Deduplicación: tiempo (s) | 1. Deduplicación: operaciones | 2. Ordenamiento: tiempo (s) | 2. Ordenamiento: operaciones | 3. Franjas de congestión: tiempo (s) | 3. Franjas de congestión: operaciones |
| --- | --- | --- | --- | --- | --- | --- |
| 500 | 6.442e-03 | 114,603 | 5.121e-03 | 58,765 | 5.438e-03 | 125,250 |
| 1000 | 2.728e-02 | 457,620 | 1.982e-02 | 216,237 | 2.282e-02 | 500,500 |
| 2000 | 1.045e-01 | 1,829,403 | 8.440e-02 | 865,273 | 9.511e-02 | 2,001,000 |
| 3000 | 2.379e-01 | 4,108,312 | 1.830e-01 | 1,933,831 | 2.126e-01 | 4,501,500 |
| 4000 | 4.242e-01 | 7,293,504 | 3.566e-01 | 3,506,597 | 4.582e-01 | 8,002,000 |
| 8000 | 1.745e+00 | 29,344,681 | 1.450e+00 | 14,168,155 | 1.583e+00 | 32,004,000 |

## Factor al duplicar n (esperado ≈ 4 por ser Θ(n²))

| Operación | n → 2n | Factor de tiempo | Factor de operaciones |
| --- | --- | --- | --- |
| 1. Deduplicación | 1000 → 2000 | 3.83 | 4.00 |
| 1. Deduplicación | 4000 → 8000 | 4.12 | 4.02 |
| 2. Ordenamiento | 1000 → 2000 | 4.26 | 4.00 |
| 2. Ordenamiento | 4000 → 8000 | 4.07 | 4.04 |
| 3. Franjas de congestión | 1000 → 2000 | 4.17 | 4.00 |
| 3. Franjas de congestión | 4000 → 8000 | 3.45 | 4.00 |

## Extrapolación al volumen real (t ≈ c·n²)

| Operación | n real | c (s por n²) | Horas por ejecución | kWh por ejecución | Ejecuciones al año | kWh al año |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Deduplicación | 1,400,000 | 2.674e-08 | 14.6 | 7.28 | 365 | 2,657 |
| 2. Ordenamiento | 1,309,000 | 2.176e-08 | 10.4 | 5.18 | 365 | 1,890 |
| 3. Franjas de congestión | 166,000 × 80 | 2.566e-08 | 15.7 | 7.86 | 12 | 94 |

Operaciones 1 y 2 juntas: 24.9 h por noche (ventana de 4 h). Total de las operaciones 1 a 3: 4,641 kWh al año.
