# Rediseño del proceso nocturno de recaudo del SITVM

**Análisis de algoritmos · Proyecto final · Grupo 7 · Caso 1 — Recaudo del transporte**

| Integrante |
| --- |
| Heyner Mena Campaña |
| Juan Andrés Ramírez Castañeda |
| Camilo Ospina Hernández |
| Juliana Arenas Arias |

**Estado:** entrega parcial (Laboratorio 4, 18 de noviembre de 2026): operación 4, liquidación del tope tarifario. El resto se completa para el 23 de noviembre de 2026.

---

## 1. Análisis del problema

### 1.1 Descripción del problema computacional

Pendiente para la entrega del 23 de noviembre.

### 1.2 Operación 4 — Liquidación del tope tarifario: entradas, salida y restricciones

<!-- Parte 1 del Lab 4. Con unidades y límites del caso: viajes por día de una tarjeta
     (d = 28 a 31 días), tarifas en pesos, 950.000 tarjetas, ventana 00:00–04:00, servidor de 500 W.
     Restricción: devolución exacta frente a la combinación más barata. -->

### 1.3 Operaciones críticas del proceso

Pendiente para la entrega del 23 de noviembre.

### 1.4 Costo energético del proceso actual (línea base)

Pendiente para la entrega del 23 de noviembre.

### 1.5 Supuestos

<!-- Documentar aquí, como mínimo:
     - Cómo se trata un mes de 31 días frente al pase mensual de 30 días.
     - Cómo se interpretó la regla simplificada actual, con un ejemplo.
     - Que se trabaja con el perfil general (los diferenciales tienen la misma estructura).
     - Que un pase puede comprarse aunque sobre al final del mes. -->

## 2. Diseño de la solución

### 2.1 Estructuras de datos seleccionadas

Pendiente para la entrega del 23 de noviembre.

### 2.2 Operación 4 — Por qué el problema admite programación dinámica

<!-- Subestructura óptima y subproblemas que se repiten. -->

### 2.3 Operación 4 — Ejemplo resuelto a mano

<!-- Ejemplo de 4 a 8 días, tabla llenada del último día al primero, y reconstrucción de las compras.
     Debe ser el mismo que se prueba en pruebas.py. -->

### 2.4 Operación 4 — Recurrencia

<!-- Recurrencia, cada término, caso base y orden de llenado. -->

### 2.5 Segunda operación

Pendiente para la entrega del 23 de noviembre.

## 3. Implementación

### 3.1 Operación 4 — Código

- [Estrategia (programación dinámica)](src/tope_tarifario/estrategia.py)
- [Solución exhaustiva](src/tope_tarifario/exhaustivo.py)
- [Regla actual](src/tope_tarifario/regla_actual.py)
- [Pruebas](src/tope_tarifario/pruebas.py)
- [Tarifas](src/tope_tarifario/tarifas.py)

### 3.2 Tecnologías y herramientas

<!-- Python, versión; matplotlib; entorno virtual. -->

### 3.3 Decisiones de implementación

<!-- Decisiones relevantes: indexación de días, contador de operaciones, etc. -->

## 4. Evaluación del desempeño

### 4.1 Operación 4 — Complejidad temporal y espacial

<!-- DP Θ(d) frente a exhaustiva exponencial en los días con viaje; regla actual. -->

### 4.2 Operación 4 — Verificación

<!-- Qué casos cubre pruebas.py: límites, ejemplo a mano, ≥ 20 aleatorias, restricción del negocio, contraejemplo. -->

### 4.3 Operación 4 — Diseño de los experimentos y resultados

- [Generador de datos](src/tope_tarifario/datos.py)
- [Medición](src/tope_tarifario/medicion.py)

![Tiempo frente a d](graficas/tope_tarifario/tiempo_vs_n.png)

![Operaciones frente a d](graficas/tope_tarifario/operaciones_vs_n.png)

<!-- Nota de cómo se midió: repeticiones, semilla, tamaños, equipo donde se midió. -->

### 4.4 Operación 4 — Lo medido contra lo esperado

<!-- Pareja d y 2d: factor de crecimiento de tiempo y de operaciones de cada solución. -->

### 4.5 Operación 4 — Extrapolación al volumen real y ventana operativa

<!-- 950.000 tarjetas; ventana de 4 h; DP, regla actual y exhaustiva. -->

### 4.6 Segunda operación

Pendiente para la entrega del 23 de noviembre.

## 5. Análisis comparativo

### 5.1 Operación 4 — Contraejemplo de la regla actual

<!-- Instancia, resultado de la regla, óptimo y diferencia. Es la misma de pruebas.py. -->

### 5.2 Operación 4 — Condición contraria

<!-- Qué tendría que cambiar para que una estrategia voraz fuera la adecuada. -->

### 5.3 Operación 4 — Recomendación

<!-- Qué adoptar, qué gana la organización y qué límite o riesgo debe conocer. -->

### 5.4 Comparación global y solución seleccionada

Pendiente para la entrega del 23 de noviembre.

## 6. Implicaciones éticas, sociales y ambientales

### 6.1 Consumo energético — Operación 4

<!-- kWh = kW × h con 0,5 kW: regla actual frente a DP, y proyección a un año (12 cierres de mes). -->

### 6.2 Preguntas de impacto del caso

Pendiente para la entrega del 23 de noviembre.

### 6.3 Consecuencias sobre las personas

Pendiente para la entrega del 23 de noviembre.

### 6.4 Marco normativo y buenas prácticas

Pendiente para la entrega del 23 de noviembre.

### 6.5 Sostenibilidad de la decisión (crecimiento del 30 %)

Pendiente para la entrega del 23 de noviembre.

## 7. Conclusiones

Pendiente para la entrega del 23 de noviembre.

---

## Reproducción

Requisitos: Python 3.10 o superior.

```cmd
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/tope_tarifario/pruebas.py
python src/tope_tarifario/medicion.py
```

En Linux o macOS, el entorno se activa con `source .venv/bin/activate`.

<!-- Explicar cómo se generan los datos sintéticos (datos.py, semilla) y qué produce medicion.py. -->
