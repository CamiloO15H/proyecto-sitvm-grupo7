# Resultados medidos de las franjas de congestion

Equipo: Windows-11-10.0.26100-SP0; Python 3.12.0.
Semilla base 2026 + n, 5 repeticiones por algoritmo y tamano.
Solo se cronometra el algoritmo; datos sinteticos creados antes.

## Experimento A: tres algoritmos

| n | Fuerza bruta: tiempo (s) | Fuerza bruta: operaciones | Divide y venceras: tiempo (s) | Divide y venceras: operaciones | Kadane: tiempo (s) | Kadane: operaciones |
| --- | --- | --- | --- | --- | --- | --- |
| 250 | 0.00260752 | 31375 | 0.0004637 | 2244 | 2.694e-05 | 250 |
| 500 | 0.00981866 | 125250 | 0.0006662 | 4988 | 3.662e-05 | 500 |
| 1000 | 0.0372075 | 500500 | 0.00137578 | 10976 | 7.432e-05 | 1000 |
| 2000 | 0.146506 | 2001000 | 0.0030975 | 23952 | 0.00015234 | 2000 |
| 4000 | 0.583755 | 8002000 | 0.00618726 | 51904 | 0.0003118 | 4000 |

## Experimento B: escalabilidad

| n | Divide y venceras: tiempo (s) | Divide y venceras: operaciones | Kadane: tiempo (s) | Kadane: operaciones |
| --- | --- | --- | --- | --- |
| 4000 | 0.00627638 | 51904 | 0.0003376 | 4000 |
| 8000 | 0.0132951 | 111808 | 0.00061714 | 8000 |
| 16000 | 0.0278336 | 239616 | 0.00127566 | 16000 |
| 32000 | 0.0664129 | 511232 | 0.002557 | 32000 |
| 64000 | 0.138145 | 1086464 | 0.00504434 | 64000 |
| 128000 | 0.255493 | 2300928 | 0.0101898 | 128000 |
| 256000 | 0.559504 | 4857856 | 0.0270019 | 256000 |

## Factor al duplicar n

| Estrategia | n -> 2n | Factor tiempo | Factor operaciones |
| --- | --- | --- | --- |
| Fuerza bruta | 250 -> 500 | 3.77 | 3.99 |
| Fuerza bruta | 500 -> 1000 | 3.79 | 4.00 |
| Fuerza bruta | 1000 -> 2000 | 3.94 | 4.00 |
| Fuerza bruta | 2000 -> 4000 | 3.98 | 4.00 |
| Divide y venceras | 250 -> 500 | 1.44 | 2.22 |
| Divide y venceras | 500 -> 1000 | 2.07 | 2.20 |
| Divide y venceras | 1000 -> 2000 | 2.25 | 2.18 |
| Divide y venceras | 2000 -> 4000 | 2.00 | 2.17 |
| Kadane | 250 -> 500 | 1.36 | 2.00 |
| Kadane | 500 -> 1000 | 2.03 | 2.00 |
| Kadane | 1000 -> 2000 | 2.05 | 2.00 |
| Kadane | 2000 -> 4000 | 2.05 | 2.00 |
| Divide y venceras | 32000 -> 64000 | 2.08 | 2.13 |
| Divide y venceras | 128000 -> 256000 | 2.19 | 2.11 |
| Kadane | 32000 -> 64000 | 1.97 | 2.00 |
| Kadane | 128000 -> 256000 | 2.65 | 2.00 |

## Extrapolacion a 166000 intervalos por estacion, 80 estaciones

Supuestos: una serie independiente por estacion; ejecucion secuencial; servidor a 0,5 kW bajo carga sostenida; 12 ejecuciones por ano.
Los tiempos se extrapolan segun la complejidad teorica y son estimaciones.

| Estrategia | Tiempo base (s) | n medido | Horas / ejecucion | kWh / ejecucion | kWh / ano |
| --- | --- | --- | --- | --- | --- |
| Fuerza bruta | 0.583755 | 4000 | 22.342 | 11.171 | 134.05 |
| Divide y venceras | 0.559504 | 256000 | 0.0077818 | 0.0038909 | 0.046691 |
| Kadane | 0.0270019 | 256000 | 0.00038909 | 0.00019454 | 0.0023345 |

**Nota:** la operacion 3 se extrapola con 12 ejecuciones por ano segun la convencion del equipo; la ventana de cuatro horas del caso esta fijada expresamente para las operaciones 1, 2 y 4.
