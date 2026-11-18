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

Para resolver el problema del tope tarifario se recibe como entrada una lista llamada viajes_por_dia. Cada posición de la lista representa un día del mes y el valor guardado indica la cantidad de viajes que realizó el usuario durante ese día. Para el caso real se trabaja con meses de entre 28 y 31 días, y todos los costos se manejan en pesos colombianos. Por ejemplo, una lista como [3, 0, 2, 1] representa cuatro días, donde el primer día se hicieron 3 viajes, el segundo ninguno, el tercero 2 y el cuarto 1.

A partir de esta información, el algoritmo debe calcular cuál es el menor valor que el usuario debería pagar, teniendo en cuenta las diferentes opciones disponibles: pagar los viajes de manera individual, utilizar un pase diario, un pase semanal o un pase mensual. La idea es no escoger simplemente la opción que parece más barata en cada día por separado, sino encontrar la combinación que dé el menor costo total.

Para realizar el cálculo también se tuvieron en cuenta algunas restricciones definidas para el problema. Cada mes se analiza de manera independiente, por lo que no se tienen en cuenta pases comprados en meses anteriores. Además, un pase puede cubrir días que queden por fuera del final del mes; en este caso simplemente se utiliza para los días restantes y el tiempo que sobre no genera ninguna devolución.

Otra restricción importante es que el resultado debe ser exacto. Si al usuario se le cobró un valor mayor al mínimo calculado, se debe devolver exactamente la diferencia entre ambos valores. De esta forma no se devuelve ni menos dinero al usuario ni más dinero del que realmente corresponde.

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

Todo el código está escrito en Python 3.13. La única biblioteca externa es matplotlib 3.11.2, que usamos solo para dibujar las gráficas; la programación dinámica, la búsqueda exhaustiva y la regla actual las implementamos nosotros, sin bibliotecas de optimización. Para medir el tiempo usamos `time.perf_counter()` y para los datos sintéticos el módulo `random` con semilla fija.

Trabajamos con un entorno virtual (`venv`) y dejamos la dependencia en `requirements.txt`, así cualquiera puede instalar exactamente lo mismo. El control de versiones lo llevamos en Git y GitHub, donde cada integrante sube sus cambios con su propia cuenta.

### 3.3 Decisiones de implementación

- **Las tarifas están en un solo archivo.** `tarifas.py` tiene los precios, la duración de los pases y la función `costo_del_dia`, para calcular más barato el pagar un solo día. Las tres soluciones se usan, así que todas parten de la misma regla para un día y la comparación es justa.
- **Contamos operaciones sin cambiar las firmas pedidas.** Toda solución tiene una versión "contada" (`costo_minimo_contado`, `costo_exhaustivo_contado`, `costo_regla_actual_contado`) que devuelve el costo y el número de opciones que se evaluaron. La función original llama la versión y devuelve solo el costo. No usamos variables globales.
- **Los datos son reproducibles.** `datos.py` genera las tarjetas con una semilla fija (2026 más el número de días), y en cada tamaño las tres soluciones se miden sobre las mismas tarjetas. Cerca del 90 % de los días tienen entre 1 y 4 viajes, porque la guía va pidiendo viajes en todos o casi todos los días.
- **Los días se cuentan del 1 al d**, como en el calendario, y la posición d + 1 es el caso base (no quedan días por pagar). Así el código se lee igual que la recurrencia del informe.

## 4. Evaluación del desempeño

### 4.1 Operación 4 — Complejidad temporal y espacial

<!-- DP Θ(d) frente a exhaustiva exponencial en los días con viaje; regla actual. -->

### 4.2 Verificación

Para verificar que la solución propuesta encuentre realmente el costo mínimo, se creó el archivo `pruebas.py`, donde se comparan los resultados de la programación dinámica con la solución exhaustiva en diferentes tipos de casos.

Primero se probaron algunos casos límite, como una lista vacía, un solo día con viajes, varios días sin ningún viaje y un periodo corto donde resulta más económico utilizar un pase semanal que pagar cada día por separado. Esto permite comprobar que el algoritmo también funciona correctamente en situaciones sencillas o poco comunes.

También se utilizó el ejemplo que se resolvió manualmente, correspondiente a la lista `[3, 3, 1, 0, 3, 3, 2, 1]`, cuyo costo mínimo esperado es de $39.900. Tanto la estrategia de programación dinámica como la solución exhaustiva deben obtener este mismo valor.

Además, se generan 25 casos aleatorios pequeños utilizando una semilla fija. Para cada uno de estos casos se calcula el resultado con la solución exhaustiva y luego se compara con el obtenido por programación dinámica. Se utilizan tamaños pequeños debido a que la solución exhaustiva aumenta rápidamente su costo a medida que crece la cantidad de días, por lo que en esta parte se usa principalmente como una forma de comprobar que la estrategia optimizada está llegando al mismo resultado mínimo.

También se verifica la restricción principal del negocio relacionada con la devolución. Si al usuario se le cobró un valor mayor al costo mínimo, la devolución debe ser exactamente la diferencia entre ambos valores. Si el cobro ya corresponde al mínimo o es menor, la devolución debe ser cero.

Por último, se incluye el contraejemplo `[0, 0, 0, 0, 0, 3, 3, 3, 3]`, en el cual la regla actual obtiene un costo de $38.000, mientras que la estrategia propuesta encuentra un costo mínimo de $36.000. Con esta prueba se busca comprobar que la regla actual no siempre encuentra la opción más económica.

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

`datos.py` genera las tarjetas sintéticas con semilla fija, de modo que cada ejecución produce los mismos datos. `pruebas.py` verifica que la programación dinámica coincide con la solución exhaustiva y que se cumple la restricción del negocio; si todo está bien, imprime "Todas las pruebas pasaron". `medicion.py` corre los experimentos y guarda en `graficas/tope_tarifario/` las gráficas `tiempo_vs_n.png`, `operaciones_vs_n.png` y `tiempo_dp_periodos_largos.png`, junto con `resultados.md`, que tiene las tablas usadas en este informe.

<!-- Explicar cómo se generan los datos sintéticos (datos.py, semilla) y qué produce medicion.py. -->
