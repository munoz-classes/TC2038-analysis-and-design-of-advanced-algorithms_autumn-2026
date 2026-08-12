---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #fcfcfc
color: #222222
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 21px;
    padding: 35px 50px;
  }
  h1 {
    color: #003366;
    font-size: 36px;
  }
  h2 {
    color: #0055a5;
    font-size: 28px;
    border-bottom: 2px solid #0055a5;
    padding-bottom: 8px;
    margin-top: 0;
  }
  h3 {
    color: #222;
    font-size: 22px;
  }
  code {
    background-color: #eef2f7;
    color: #a71d5d;
    font-family: 'Fira Code', 'Consolas', monospace;
    font-size: 18px;
  }
  pre {
    background-color: #f4f6f9;
    border-left: 4px solid #0055a5;
    padding: 12px;
    font-size: 16px;
  }
  .problem-box {
    background-color: #fff8e6;
    border-left: 6px solid #ffb300;
    padding: 15px;
    margin-top: 10px;
    border-radius: 4px;
  }
  .solution-box {
    background-color: #eef9f1;
    border-left: 6px solid #2e7d32;
    padding: 15px;
    margin-top: 10px;
    border-radius: 4px;
  }
---

# TC2038 - Análisis y Diseño de Algoritmos Avanzados
## Tema 1: Técnicas de Diseño de Algoritmos (9 Horas)

**Profesor - Alison Muñoz Capote**
*Tecnológico de Monterrey*

---

# Mapa del Tema 1 y Objetivos

### Objetivos del Tema:
1. Comprender la filosofía y modelo de cómputo de las 5 técnicas fundamentales.
2. Identificar la estructura subyacente de un problema para elegir la técnica óptima.
3. Analizar la complejidad temporal y espacial ($O, \Omega, \Theta$).
4. Implementar soluciones eficientes a problemas complejos.

### Distribución de Contenido (9 horas lectivas):
* **1.1 Divide y Vencerás** (1.5 hrs)
* **1.2 Programación Dinámica** (2.5 hrs)
* **1.3 Algoritmos Avaros (Greedy)** (1.5 hrs)
* **1.4 Backtracking** (1.5 hrs)
* **1.5 Ramificación y Poda (Branch & Bound)** (2.0 hrs)

---

# Repaso Breve: Notación Asintótica y Complejidad

Antes de diseñar algoritmos, debemos medir su eficiencia:

* **$O(g(n))$ (Cota Superior):** Mide el peor caso de tiempo de ejecución.
* **$\Omega(g(n))$ (Cota Inferior):** Mide el mejor caso de tiempo de ejecución.
* **$\Theta(g(n))$ (Cota Ajustada):** Comportamiento exacto del algoritmo.

### Jerarquía de Complejidades Comunes:
$$O(1) < O(\log n) < O(n) < O(n \log n) < O(n^2) < O(2^n) < O(n!)$$

**Regla de oro:** El diseño algorítmico busca desplazar problemas de clases exponenciales $O(2^n)$ a polinomiales $O(n^k)$ o logarítmicas $O(n \log n)$.

---

# 1.1 Divide y Vencerás
### (Tiempo Estimado: 1.5 Horas)

---

# 1.1 Situación Problemática: Monitoreo Aéreo

<div class="problem-box">

### ✈️ El Desafío del Control de Tráfico Aéreo
Un sistema de radar monitorea $N$ aeronaves en un sector aéreo. Para evitar colisiones en tiempo real, el sistema debe calcular constantemente el **par de aviones más cercanos** ($P_i, P_j$) y alertar si la distancia es menor a un umbral de seguridad $d_{min}$.

* **Datos de Entrada:** Un conjunto $P$ de $N$ puntos en un plano 2D $(x, y)$, donde $N = 100,000$.
* **Enfoque Ingenuo (Fuerza Bruta):** Comparar cada par posible.
  $$\text{Pares a evaluar} = \frac{N(N-1)}{2} \approx 5 \times 10^9 \text{ operaciones } \implies O(N^2)$$
* **Problema:** Un algoritmo $O(N^2)$ toma varias decenas de segundos; la alerta llegará demasiado tarde.
* **Meta:** ¿Podemos resolver esto en $O(N \log N)$ para respuesta inmediata en milisegundos?
</div>

---

# 1.1 Filosofía de Divide y Vencerás

La técnica de **Divide y Vencerás** rompe un problema complejo en subproblemas más pequeños del mismo tipo de manera recursiva.

### Las 3 Fases Fundamentales:

1. **Dividir:** Dividir la instancia del problema original en $a$ subproblemas independientes de tamaño $n/b$.
2. **Vencer (Resolver):** Resolver los subproblemas recursivamente. Si el tamaño del subproblema es suficientemente pequeño (caso base), resolverlo de forma directa (fuerza bruta).
3. **Combinar:** Unir las soluciones de los subproblemas para formar la solución completa del problema original.

---

# 1.1 Estructura Recurrente y Ecuación General

El tiempo de ejecución de un algoritmo de Divide y Vencerás se expresa mediante una **ecuación de recurrencia**:

$$T(n) = a \cdot T\left(\frac{n}{b}\right) + f(n)$$

Donde:
* $n$: Tamaño de la entrada.
* $a \ge 1$: Número de subproblemas creados en la división.
* $b > 1$: Factor por el cual se reduce el tamaño del problema.
* $f(n)$: Tiempo requerido para **dividir** el problema y **combinar** las soluciones.

---

# 1.1 El Teorema Maestro (Master Theorem)

Herramienta matemática para resolver recurrencias de la forma $T(n) = a T(n/b) + f(n)$:

Sea $c_{crit} = \log_b a$. Comparamos $f(n)$ con $n^{\log_b a}$:

1. **Caso 1 (Dominio de Subproblemas):** Si $f(n) = O(n^{\log_b a - \epsilon})$ para $\epsilon > 0$, entonces:
   $$T(n) = \Theta(n^{\log_b a})$$

2. **Caso 2 (Equilibrio):**
   Si $f(n) = \Theta(n^{\log_b a} \log^k n)$ con $k \ge 0$, entonces:
   $$T(n) = \Theta(n^{\log_b a} \log^{k+1} n)$$

3. **Caso 3 (Dominio de Combinación):**
   Si $f(n) = \Omega(n^{\log_b a + \epsilon})$ y $a f(n/b) \le c f(n)$ ($c < 1$), entonces:
   $$T(n) = \Theta(f(n))$$

---

# 1.1 Caso de Estudio: Multiplicación de Karatsuba

### Multiplicación Tradicional vs. Karatsuba
Multiplicar dos números de $n$ dígitos tradicionalmente toma $O(n^2)$ operaciones.

* **Multiplicación Estándar:** Requiere 4 multiplicaciones de tamaño $n/2$:
  $$T(n) = 4T(n/2) + O(n) \implies T(n) = \Theta(n^{\log_2 4}) = \Theta(n^2)$$
* **Truco de Karatsuba:** Observar que $(A+B)(C+D) = AC + (AD+BC) + BD$.
  Por ende: $AD + BC = (A+B)(C+D) - AC - BD$. ¡Solo requiere **3 multiplicaciones**!
  $$T(n) = 3T(n/2) + O(n) \implies T(n) = \Theta(n^{\log_2 3}) \approx \Theta(n^{1.585})$$

---

# 1.1 Algoritmo del Par de Puntos Más Cercanos

Volviendo al problema del radar aéreo:

1. **Preprocesamiento:** Ordenar los puntos según coordenada $X$ (lista $P_x$) y según $Y$ (lista $P_y$). $O(n \log n)$.
2. **Dividir:** Trazar una línea vertical $L$ que divida los puntos en dos mitades $Q$ (izquierda) y $R$ (derecha) de tamaño $n/2$.
3. **Vencer:** Hallar la distancia mínima recursivamente en $Q$ ($d_1$) y en $R$ ($d_2$). Sea $\delta = \min(d_1, d_2)$.
4. **Combinar:** ¿Existe algún par con un punto en $Q$ y otro en $R$ con distancia $< \delta$?
   * Crear una franja vertical centrada en $L$ de ancho $2\delta$.
   * Para cada punto en la franja, solo necesitamos revisar los siguientes **7 puntos** ordenados por la coordenada $Y$.

---

# 1.1 Pseudocódigo y Análisis de Complejidad

```python
def closest_pair_rec(Px, Py):
    if len(Px) <= 3:
        return fuerza_bruta(Px)
    
    mid = len(Px) // 2
    Qx, Rx = Px[:mid], Px[mid:]
    mid_x = Px[mid].x
    
    Qy = [p for p in Py if p.x <= mid_x]
    Ry = [p for p in Py if p.x > mid_x]
    
    delta1 = closest_pair_rec(Qx, Qy)
    delta2 = closest_pair_rec(Rx, Ry)
    delta = min(delta1, delta2)
    
    # Combinar: Buscar en la franja
    strip = [p for p in Py if abs(p.x - mid_x) < delta]
    min_strip = delta
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 8, len(strip))):
            min_strip = min(min_strip, dist(strip[i], strip[j]))
            
    return min(delta, min_strip)
```

**Complejidad:** $T(n) = 2T(n/2) + O(n) \implies T(n) = \Theta(n \log n)$.

---

# 1.1 Solución a la Situación Problemática

<div class="solution-box">

### ✈️ Resultado para el Sistema de Control Aéreo

* **Fuerza Bruta ($O(N^2)$):**
  Para $N = 100,000$, realiza $\approx 5 \times 10^9$ comparaciones. Tiempo estimado: **~15 a 20 segundos**. Inaceptable para seguridad aérea.

* **Con Divide y Vencerás ($O(N \log N)$):**
  Para $N = 100,000$, $N \log_2 N \approx 1.66 \times 10^6$ operaciones.
  Tiempo estimado de ejecución: **~12 milisegundos**.

**Conclusión:** Aplicar Divide y Vencerás reduce el tiempo de cómputo en un factor de **1500x**, permitiendo monitoreo en tiempo real.
</div>

---

# 1.1 Resumen de Divide y Vencerás

### ¿Cuándo es adecuada esta técnica?
* Cuando el problema se puede descomponer en **subproblemas disjuntos e independientes**.
* Cuando la etapa de **combinación** es eficiente ($O(n)$ o $O(1)$).

### Limitaciones:
* **Overhead de Recursión:** La profundidad del árbol de llamadas consume espacio en stack $O(\log n)$.
* **Ineficiencia por subproblemas repetidos:** Si los subproblemas se solapan, Divide y Vencerás vuelve a calcular lo mismo múltiples veces (¡Para esto necesitaremos Programación Dinámica!).

---

# 1.2 Programación Dinámica
### (Tiempo Estimado: 2.5 Horas)

---

# 1.2 Situación Problemática: Asignación de Presupuesto

<div class="problem-box">

### 💼 Optimización de Inversión en Proyectos (Mochila 0/1)
Una empresa de tecnología dispone de un fondo de inversión $W = \$10 \text{ MUSD}$. Existen $N = 8$ proyectos candidatos. Cada proyecto $i$ requiere un capital $w_i$ y promete un retorno financiero esperado $v_i$.

* No se pueden financiar proyectos de forma parcial (se acepta todo o nada).
* **Fuerza Bruta:** Probar los $2^N = 2^8 = 256$ subconjuntos posibles.
* **¿Qué pasa si $N = 50$?** $$2^{50} \approx 1.12 \times 10^{15} \text{ evaluaciones. A 1 GHz, tomaría 13 días.}$$
* **Desafío:** ¿Cómo obtener la combinación que maximice la ganancia en menos de un segundo?
</div>

---

# 1.2 ¿Qué es la Programación Dinámica (DP)?

Técnica de diseño inventada por **Richard Bellman** (1950) para resolver problemas de optimización.

### Dos Propiedades Fundamentales Requeridas:

1. **Subestructura Óptima:**
   La solución óptima del problema global contiene en su interior las soluciones óptimas de sus subproblemas.

2. **Solapamiento de Subproblemas (Overlapping Subproblems):**
   El algoritmo recursivo resuelve los **mismos subproblemas** una y otra vez, en lugar de generar subproblemas siempre nuevos.

---

# 1.2 D&C vs. Programación Dinámica

| Característica | Divide y Vencerás | Programación Dinámica |
| :--- | :--- | :--- |
| **Naturaleza de Subproblemas** | **Independientes / Disjuntos** (Ej. Quicksort, Mergesort) | **Solapados / Repetidos** (Ej. Fibonacci, LCS, Mochila) |
| **Estructura de Evaluación** | Árbol de recursión simple | Grafo Acíclico Dirigido (DAG) de estados |
| **Almacenamiento** | No almacena resultados intermedios | **Memoriza** o **tabula** resultados para reuso ($O(1)$) |
| **Enfoque Típico** | Top-Down | Top-Down (Memo) o Bottom-Up (Tabulación) |

---

# 1.2 Enfoques de DP: Top-Down vs. Bottom-Up

### 1. Top-Down con Memorización (Memoization)
* Se mantiene la estructura recursiva natural del problema.
* Antes de computar $f(state)$, se consulta una tabla/hash. Si ya fue calculado, se retorna inmediatamente.
* **Ventaja:** Solo calcula los estados estrictamente necesarios.

### 2. Bottom-Up con Tabulación (Tabulation)
* Se resuelven primero los casos base y se llena una tabla de forma iterativa de lo más pequeño a lo más grande.
* **Ventaja:** Elimina la sobrecarga de llamadas recursivas en el stack y facilita optimización de espacio.

---

# 1.2 El Principio de Optimizabilidad de Bellman

> *"En una secuencia óptima de decisiones, toda subsecuencia debe ser también óptima con respecto a los estados inicial y final de dicha subsecuencia."*

### Formulación General de una Ecuación de Recurrencia DP:

$$DP(estado) = \min_{d \in D} / \max_{d \in D} \Big\{ \text{Costo}(d) + DP(\text{SiguienteEstado}(estado, d)) \Big\}$$

**Identificar los ESTADOS:** Un *estado* es el conjunto mínimo de parámetros que definen un subproblema de manera unívoca.

---

# 1.2 Caso de Estudio 1: Subsecuencia Común Más Larga (LCS)

### Definición del Problema:
Dadas dos cadenas $X = [x_1, x_2, \dots, x_m]$ e $Y = [y_1, y_2, \dots, y_n]$, encontrar la longitud de la subsecuencia más larga presente en ambas en el mismo orden relativo (no necesariamente contigua).

### Ejemplo:
* $X = \text{"ABCBDAB"}$
* $Y = \text{"BDCABA"}$
* **LCS:** $\text{"BCBA"}$ (longitud 4)

### Definición de Estados:
Sea $DP[i][j]$ la longitud de la LCS de los prefijos $X[1..i]$ e $Y[1..j]$.

---

# 1.2 LCS: Ecuación de Recurrencia y Casos

### Casos Base:
$$DP[i][0] = 0 \quad \forall i, \qquad DP[0][j] = 0 \quad \forall j$$

### Relación de Transición de Estados:
$$DP[i][j] = \begin{cases} 
DP[i-1][j-1] + 1 & \text{si } X[i] == Y[j] \\
\max(DP[i-1][j], DP[i][j-1]) & \text{si } X[i] \neq Y[j]
\end{cases}$$

* **Explicación Intuitiva:**
  * Si los caracteres coinciden, forman parte de la LCS; sumamos 1 al resultado anterior.
  * Si no coinciden, la mejor solución proviene de descartar el caracter actual de $X$ o de $Y$.

---

# 1.2 LCS: Construcción de la Tabla Bottom-Up

Construcción paso a paso para $X = \text{"ABCB"}$, $Y = \text{"BDCB"}$:

| $DP[i][j]$ | $\emptyset$ | B (1) | D (2) | C (3) | B (4) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $\emptyset$ | **0** | **0** | **0** | **0** | **0** |
| **A (1)** | **0** | 0 | 0 | 0 | 0 |
| **B (2)** | **0** | **1** | 1 | 1 | 1 |
| **C (3)** | **0** | 1 | 1 | **2** | 2 |
| **B (4)** | **0** | 1 | 1 | 2 | **3** |

* Longitud de LCS = $DP[4][4] = 3$ ($\text{"BCB"}$).
* **Complejidad:** $O(m \cdot n)$ en tiempo y espacio.

---

# 1.2 LCS: Código de Implementación

```python
def lcs_length(X, Y):
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    return dp[m][n]
```

---

# 1.2 Caso de Estudio 2: Problema de la Mochila 0/1

Volviendo a nuestro problema de inversión:

* $N$ elementos, cada uno con peso $w_i$ y valor $v_i$.
* Capacidad máxima de la mochila (presupuesto): $W$.
* Variable de decisión $x_i \in \{0, 1\}$.

### Definición del Estado $DP[i][w]$:
El valor máximo alcanzable utilizando un subconjunto de los primeros $i$ elementos con una capacidad de peso disponible $w$.

### Recurrencia:
$$DP[i][w] = \begin{cases} 
DP[i-1][w] & \text{si } w_i > w \\
\max(DP[i-1][w], \, v_i + DP[i-1][w - w_i]) & \text{si } w_i \le w
\end{cases}$$

---

# 1.2 Mochila 0/1: Llenado Tabular y Ejemplo

Datos: Capacidad $W = 5$. Elementos: 1) $w_1=2, v_1=3$; 2) $w_2=3, v_2=4$; 3) $w_3=4, v_3=5$.

| $i \setminus w$ | 0 | 1 | 2 | 3 | 4 | 5 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | 0 | 0 | 0 | 0 | 0 | 0 |
| **1 ($w_1=2, v_1=3$)** | 0 | 0 | **3** | 3 | 3 | 3 |
| **2 ($w_2=3, v_2=4$)** | 0 | 0 | 3 | **4** | 3 | **7** |
| **3 ($w_3=4, v_3=5$)** | 0 | 0 | 3 | 4 | **5** | **7** |

* Resultado Óptimo = $DP[3][5] = 7$ (Seleccionando elementos 1 y 2).
* **Complejidad Temporal:** $\Theta(N \cdot W)$.
* **Complejidad Espacial:** $O(N \cdot W)$ (Reducible a $O(W)$ manteniendo solo la fila previa).

---

# 1.2 Solución a la Situación Problemática

<div class="solution-box">

### 💼 Resultado para la Empresa de Inversión

* **Fuerza Bruta ($O(2^N)$):**
  Para $N = 50$ proyectos, $2^{50}$ alternativas requerirían **13 días** de cálculo continuo.

* **Programación Dinámica ($O(N \cdot W)$):**
  Con $N = 50$ y Presupuesto $W = 10,000$ (en miles de USD), la tabla requiere:
  $$\text{Operaciones} = 50 \times 10,000 = 500,000 \text{ pasos.}$$
  Tiempo de ejecución: **< 5 milisegundos**.

**Impacto:** Permite simulaciones de escenarios financieros instantáneas y toma de decisiones estratégica en tiempo real.
</div>

---

# 1.2 Resumen de Programación Dinámica

### Checklist para diseñar un algoritmo DP:
1. **Definir la estructura de estados:** ¿Qué variables mínimas identifican un subproblema?
2. **Identificar los casos base:** Soluciones triviales.
3. **Formular la ecuación de recurrencia:** Transición entre estados.
4. **Elegir el enfoque de cómputo:** Top-Down (con Memo) o Bottom-Up (Tabular).
5. **Optimizar el espacio:** ¿Puedo retener solo los últimos estados en lugar de toda la matriz?

---

# 1.3 Algoritmos Avaros (Greedy)
### (Tiempo Estimado: 1.5 Horas)

---

# 1.3 Situación Problemática: Programación de Tareas

<div class="problem-box">

### ☁️ Asignación Eficiente de Servidores en la Nube
Un servidor en la nube recibe $N = 1,000$ peticiones de procesamiento en un día. Cada tarea $i$ tiene un tiempo de inicio $s_i$ y un tiempo de fin $f_i$. El servidor solo puede ejecutar **una tarea a la vez**.

* **Objetivo:** Atender el **mayor número posible de tareas** a lo largo del día.
* **Intento 1:** Seleccionar siempre la tarea de menor duración ($f_i - s_i$).
* **Intento 2:** Seleccionar siempre la tarea que inicia primero ($s_i$).
* **Pregunta:** ¿Existe una regla simple (decisión local inmediata) que garantice matemáticamente el máximo global sin explorar todas las combinaciones posibles?
</div>

---

# 1.3 Filosofía del Algoritmo Avaro (Greedy)

Un algoritmo **Avaro (Greedy)** construye la solución paso a paso, tomando en cada paso la decisión que parece **más prometedora en ese instante (óptimo local)**, sin volver atrás jamás (sin backtracking).

<pre><code>   [Estado Actual] ───(Tomar la mejor opción local)───> [Siguiente Estado]
</code></pre>

### La Gran Ventaja:
Son algoritmos extremadamente sencillos de implementar y muy eficientes en tiempo de ejecución (generalmente $O(N)$ o $O(N \log N)$ debido al ordenamiento previo).

### El Gran Riesgo:
**"Lo voraz no siempre es óptimo."** Tomar la mejor decisión local puede conducir a una trampa que bloquee el óptimo global.

---

# 1.3 Propiedades Fundamentales para Correctitud

Para que un algoritmo Greedy garantice la solución óptima, debe cumplir dos propiedades clave:

1. **Propiedad de la Elección Avara (Greedy Choice Property):**
   Se puede llegar a una solución óptima global realizando elecciones locales inmediatas (sin necesidad de evaluar subproblemas futuros ni revisar decisiones pasadas).

2. **Subestructura Óptima:**
   Una solución óptima al problema contiene soluciones óptimas a sus subproblemas (misma propiedad requerida en DP).

---

# 1.3 Comparación: Greedy vs. DP vs. Fuerza Bruta

| Algoritmo | Toma de Decisiones | Revisa Opciones | Garantía de Óptimo | Complejidad Típica |
| :--- | :--- | :--- | :--- | :--- |
| **Fuerza Bruta** | Explora todo | Sí (Todas) | Sí | Exponencial $O(2^N)$ |
| **Prog. Dinámica** | Combina subproblemas | Sí (Evalúa opciones) | Sí | Polinomial $O(N \cdot K)$ |
| **Algoritmo Avaro** | Una sola decisión irreversible | **No** | **Solo si se demuestra** | Muy rápido $O(N \log N)$ |

---

# 1.3 Caso de Estudio: Selección de Actividades

Volviendo al problema del servidor en la nube:

### Reglas de Candidatos Greedy:
* **Candidato A (Inicio más temprano):** Falla si la primera tarea dura todo el día.
* **Candidato B (Menor duración):** Falla si una tarea corta bloquea dos tareas compatibles.
* **Candidato C (Fin más temprano $f_i$):** **¡SÍ ES ÓPTIMO!**

### Estrategia Greedy Óptima:
1. Ordenar todas las tareas por su tiempo de finalización $f_i$ en orden ascendente.
2. Seleccionar la primera tarea.
3. Para cada tarea posterior $i$, si $s_i \ge f_{última\_seleccionada}$, incluirla y actualizar el tiempo de fin.

---

# 1.3 Demostración de Correctitud: Greedy Stays Ahead

Demostraremos por **Inducción (Término de Intercambio)** que la estrategia de ordenar por $f_i$ es óptima:

* Sea $A = \{a_1, a_2, \dots, a_k\}$ el conjunto de actividades elegidas por el algoritmo Greedy.
* Sea $O = \{o_1, o_2, \dots, o_m\}$ el conjunto de actividades de una solución óptima cualquiera, ordenadas por tiempo de fin.
* Queremos probar que $k = m$ (Greedy selecciona tantas actividades como la óptima).

**Paso Inductivo:**
Para todo $r \le k$, se cumple que $f(a_r) \le f(o_r)$.
* Para $r=1$: Greedy elige $a_1$ con el $f_1$ mínimo absoluto, luego $f(a_1) \le f(o_1)$.
* Asumiendo $f(a_{r-1}) \le f(o_{r-1})$: Como $o_r$ es compatible con $o_{r-1}$, también es compatible con $a_{r-1}$. Por ende, Greedy tenía la opción de elegir $o_r$, pero eligió $a_r$ porque $f(a_r) \le f(o_r)$.

**Conclusión:** Greedy "siempre va adelante" en tiempo disponible, luego $k = m$. $\blacksquare$

---

# 1.3 Pseudocódigo y Complejidad
```python
def activity_selection(activities):
    # activities es una lista de tuplas (inicio, fin, id)
    # 1. Ordenar por tiempo de finalización f_i: O(N log N)
    sorted_activities = sorted(activities, key=lambda x: x[1])
    
    selected = []
    last_finish_time = -1
    
    # 2. Selección voraz: O(N)
    for act in sorted_activities:
        start, finish, act_id = act
        if start >= last_finish_time:
            selected.append(act)
            last_finish_time = finish
            
    return selected
```

**Análisis de Complejidad:**
* **Tiempo:** $O(N \log N)$ impulsado por la etapa de ordenamiento. El bucle de selección toma $O(N)$.
* **Espacio:** $O(N)$ para almacenar el resultado.

---

# 1.3 Solución a la Situación Problemática

<div class="solution-box">

### ☁️ Resultado para el Servidor en la Nube

* **Enfoque de Programación Dinámica ($O(N^2)$):**
  Para $N = 1,000$, realizaría alrededor de $1,000,000$ operaciones.

* **Enfoque Avaro / Greedy ($O(N \log N)$):**
  1. Ordenar 1,000 tareas por tiempo de fin: $\approx 10,000$ operaciones.
  2. Recorrido lineal de decisión: $1,000$ comparaciones.
  3. Total de operaciones: $\approx 11,000$.

**Conclusión:** El algoritmo Greedy resuelve el problema de scheduling de forma **matemáticamente perfecta** en menos de **1 milisegundo**, siendo 100 veces más rápido que la solución por DP.
</div>

---

# 1.3 Resumen de Algoritmos Avaros

### ¿Cuándo usar Greedy?
1. Cuando el problema pide optimizar una métrica global.
2. Cuando se pueda **probar matemáticamente** la propiedad de la elección avara.

### ¡Cuidado!
Si el problema exige tomar decisiones que dependen de combinaciones futuras complejas (como la Mochila 0/1 entera), Greedy **fallará** y ofrecerá solo una aproximación. En esos casos, se debe recurrir a Programación Dinámica, Backtracking o Branch & Bound.

---

# 1.4 Backtracking
### (Tiempo Estimado: 1.5 Horas)

---

# 1.4 Situación Problemática: Ubicación de Servidores

<div class="problem-box">

### 🛡️ El Problema de las N-Reinas / Antenas Anticolisión
Se debe colocar $N = 12$ antenas transmisoras de alta potencia en un grid de $12 \times 12$. Por interferencia destructiva, **ninguna par de antenas puede compartir la misma fila, columna o línea diagonal**.

* **Espacio de Búsqueda Total:**
  Colocar 12 antenas en 144 casillas sin restricciones:
  $$\binom{144}{12} \approx 1.57 \times 10^{17} \text{ combinaciones.}$$
* **Sabiendo que hay 1 por fila:**
  $$12^{12} \approx 8.9 \times 10^{12} \text{ evaluaciones.}$$
* **Desafío:** ¿Cómo explorar este espacio gigantesco descartando millones de configuraciones inválidas en segundos?
</div>

---

# 1.4 ¿Qué es Backtracking?

**Backtracking** (Búsqueda Sistemática con Retroceso) es una técnica de **fuerza bruta inteligente** para resolver problemas de satisfacción de restricciones y optimización combinatoria.

<pre><code>                  [Raíz: Estado Inicial]
                 /          |           \
           [Elección 1] [Elección 2] [Elección 3]
              /    \          | (Inválido - PODA ✂️)
          [Sol 1]  [Sol 2]   ❌
</code></pre>

### Principios Fundamentales:
1. Modela el espacio de búsqueda como un **Árbol de Espacio de Estados**.
2. Explora el árbol utilizando **Búsqueda en Profundidad (DFS)**.
3. Evalúa en cada paso una **Función de Validación (Poda)**. Si una decisión viola las reglas, se **aborta la rama entera** inmediatamente y se "retrocede" (backtrack) al nodo padre.

---

# 1.4 Construcción del Árbol de Espacio de Estados

Un árbol de espacio de estados contiene:

* **Raíz:** Estado inicial vacío (ninguna decisión tomada).
* **Nodos Internos:** Soluciones parciales vectoriales $X = (x_1, x_2, \dots, x_k)$.
* **Hojas:** Soluciones completas $(x_1, x_2, \dots, x_n)$ o callejones sin salida.
* **Ramas:** Las opciones válidas para la variable de decisión $x_{k+1}$.

<pre><code>                 Nivel 0: []
                /           \
    Nivel 1: [x1=1]        [x1=2]
            /      \          |
Nivel 2: [1, 1]  [1, 2]     [2, 1]
         (Poda ✂️)  (Válido) (Válido)
</code></pre>

---

# 1.4 Esquema General de un Algoritmo de Backtracking

El patrón genérico en código recursivo:

```python
def backtracking(solucion_parcial, nivel, candidatos):
    if es_solucion_completa(solucion_parcial):
        procesar_solucion(solucion_parcial)
        return
    
    for opcion in obtener_candidatos(solucion_parcial, nivel):
        if es_valido(opcion, solucion_parcial):
            # 1. Hacer elección
            solucion_parcial.append(opcion)
            
            # 2. Explorar en profundidad
            backtracking(solucion_parcial, nivel + 1, candidatos)
            
            # 3. Deshacer elección (BACKTRACK)
            solucion_parcial.pop()
```

---

# 1.4 Caso de Estudio: Problema de las $N$-Reinas

### Representación Vectorial de la Solución:
Vector $Tablero[1..N]$, donde $Tablero[i] = j$ significa que en la fila $i$, la reina está colocada en la columna $j$.
* Esto garantiza automáticamente que no haya dos reinas en la misma fila.

### Condición de Validación (Sin Ataque):
Para colocar una reina en la fila $i$, columna $j$, debemos verificar que para toda reina previa en fila $k < i$:
1. **Misma Columna:** $Tablero[k] \neq j$
2. **Misma Diagonal:** $|Tablero[k] - j| \neq |k - i|$

---

# 1.4 N-Reinas: Implementación en Python

```python
def solve_n_queens(n):
    results = []
    board = [-1] * n  # board[fila] = columna
    
    def is_safe(row, col):
        for prev_row in range(row):
            prev_col = board[prev_row]
            # Mismas columnas o mismas diagonales
            if prev_col == col or abs(prev_col - col) == abs(prev_row - row):
                return False
        return True

    def backtrack(row):
        if row == n:
            results.append(list(board))
            return
        for col in range(n):
            if is_safe(row, col):
                board[row] = col          # Tomar decisión
                backtrack(row + 1)        # Recursión
                board[row] = -1           # Retroceso (Backtrack)

    backtrack(0)
    return results
```

---

# 1.4 Análisis de la Eficiencia de la Poda

Visualización del impacto de la poda al cortar ramas en los niveles superiores del árbol:

<pre><code>                          (Raíz)
                   /        |        \
            [col 0]      [col 1]      [col 2]
            /  |  \      /  |  \      /  |  \
           ❌ ❌  ✅    ❌  ❌ ❌    ✅ ❌  ❌
                 /
            (Explora)
</code></pre>

### Estadísticas de Evaluación para $N = 8$:
* **Espacio de búsqueda ingenuo ($8^8$):** $16,777,216$ evaluaciones.
* **Con Backtracking y Poda:** Se visitan únicamente **2,057 nodos**.
* **Reducción:** ¡Se descarta el **99.98%** del espacio de búsqueda sin explorarlo!

---

# 1.4 Solución a la Situación Problemática

<div class="solution-box">

### 🛡️ Resultado para la Colocación de Antenas ($N=12$)

* **Fuerza Bruta Ingenua ($12^{12}$):**
  $8.91 \times 10^{12}$ estados. A 1 GHz, tomaría más de **2.4 horas** calcularlo.

* **Backtracking con Poda de Diagonales y Columnas:**
  Se evalúan únicamente **14,200,000 nodos**.
  Tiempo real de ejecución en Python: **~1.2 segundos**.
  Número total de soluciones válidas encontradas: **14,200 configuraciones**.

**Conclusión:** Backtracking convierte un problema NP-completo intratable a escala humana en un cálculo ejecutable en tiempo real mediante podas tempranas.
</div>

---

# 1.4 Resumen de Backtracking

### Fortalezas:
* Garantiza encontrar **todas las soluciones válidas** si existen.
* Requiere muy poca memoria: solo almacena la rama actual del árbol de profundidad $O(N)$.

### Debilidades:
* En el peor de los casos (cuando las podas no son efectivas), la complejidad sigue siendo exponencial $O(b^d)$ o factorial $O(N!)$.
* No utiliza estimaciones heurísticas para decidir qué rama explorar primero (explora a ciegas según el orden del bucle).

---

# 1.5 Ramificación y Poda (Branch and Bound)
### (Tiempo Estimado: 2.0 Horas)

---

# 1.5 Situación Problemática: Optimización Logística

<div class="problem-box">

### 🚚 El Problema del Agente Viajero (TSP)
Una empresa de logística debe enviar un camión a visitar $N = 15$ ciudades y regresar al depósito inicial, recorriendo la **mínima distancia total posible**.

* **Espacio de Búsqueda:** $(N-1)! / 2$ rutas posibles.
  $$\text{Para } N = 15 \implies 14! / 2 \approx 4.35 \times 10^{10} \text{ rutas posibles.}$$
* **Inconveniente de Backtracking (DFS):** DFS puede profundizar a lo largo de una ruta muy mala (de 5,000 km) y perder horas explorando sus hijas antes de darse cuenta de que era una pésima opción.
* **Necesidad:** ¿Podemos calcular una **cota matemática** que nos diga de antemano: *"Esta ruta parcial jamás será mejor que la mejor ruta ya conocida de 1,200 km, ¡abandónala de inmediato!"*?
</div>

---

# 1.5 ¿Qué es Ramificación y Poda (Branch & Bound)?

Técnica diseñada por **A. H. Land y A. G. Doig** (1960) para **problemas de optimización combinatoria**.

A diferencia de Backtracking (que solo busca satisfacción de restricciones mediante DFS), Branch & Bound utiliza **cotas matemáticas (Bounds)** para descartar subárboles completos de optimización.

### Elementos Clave:
1. **Ramificación (Branching):** Dividir el espacio de soluciones en subproblemas disjuntos (generar hijos de un nodo).
2. **Poda (Bounding):** Calcular en cada nodo una cota para el valor óptimo que se puede obtener a partir de él.
   * **Problema de Minimización:** Cota Inferior ($Lower\_Bound$).
   * **Problema de Maximización:** Cota Superior ($Upper\_Bound$).
3. **Cota Global ($Best\_Cost$):** El costo de la mejor solución completa encontrada hasta el momento.

---

# 1.5 Criterio de Poda en Branch & Bound

Supongamos un problema de **Minimización** (ej. distancia en el TSP):

<pre><code>                   [Nodo Raíz]
                  /           \
      [Nodo A: LB = 120km]    [Nodo B: LB = 210km]
             |
      [Solución Completa X: Costo = 150km] ───> Best_Cost = 150km !
</code></pre>

### Regla de Poda (Pruning Condition):
Si para un nodo parcial $k$, su cota inferior cumple:

$$Lower\_Bound(k) \ge Best\_Cost\_Actual$$

--> **¡SE PODA EL NODO $k$ INMEDIATAMENTE!** ✂️

**Razón:** Ninguna solución descendiente del nodo $k$ podrá tener un costo menor a $Lower\_Bound(k)$. Como ya poseemos una solución completa de $150 \text{ km}$, continuar explorando la rama $B$ ($210 \text{ km}$) es un desperdicio garantizado de tiempo.

---

# 1.5 Estrategias de Exploración del Árbol

A diferencia de Backtracking (que solo usa DFS), B&B permite diversas estrategias de selección del siguiente nodo a expandir:

1. **FIFO (First In, First Out) / BFS:**
   Utiliza una **Cola estándar**. Explora el árbol nivel por nivel. Consume mucha memoria $O(b^d)$.

2. **LIFO (Last In, First Out) / DFS:**
   Utiliza una **Pila**. Consume poca memoria $O(d)$, pero puede demorar en hallar una buena cota inicial.

3. **Best-First Search (Búsqueda por la Mejor Cota):**
   Utiliza una **Cola de Prioridad (Min-Heap)**.
   * **Estrategia Óptima:** Extrae siempre el nodo del árbol que tenga la cota más prometedora ($Lower\_Bound$ más pequeño).
   * Minimiza el número total de nodos expandidos.

---

# 1.5 Caso de Estudio: TSP con Branch & Bound

### ¿Cómo calcular una Cota Inferior ($LB$) para un nodo parcial en TSP?

Dado un recorrido parcial que ya visitó un conjunto de ciudades:
1. **Costo Actual ($C_{actual}$):** Suma de los pesos de las aristas ya recorridas.
2. **Estimación del Resto:** Para cada ciudad aún no visitada (y para la última visitada), tomar la suma de las **dos aristas incidentes de menor costo**.
3. **Fórmula de Cota Inferior Simplificada:**

$$Lower\_Bound = C_{actual} + \frac{1}{2} \sum_{v \in \text{No visitadas}} (\text{mín1}(v) + \text{mín2}(v))$$

Esta cota se calcula en $O(V^2)$ y garantiza ser menor o igual a la distancia real final.

---

# 1.5 Traza de Ejecución de Best-First B&B

```python
import heapq

def tsp_branch_and_bound(graph):
    n = len(graph)
    pq = [] # Guarda tuplas: (Lower_Bound, costo_actual, ruta)
    best_cost = float('inf')
    best_path = []
    
    # Inserción del Nodo raíz
    root_lb = calc_lower_bound(graph, path=[0])
    heapq.heappush(pq, (root_lb, 0, [0]))
    
    while pq:
        lb, cost, path = heapq.heappop(pq)
        
        if lb >= best_cost: # Regla de Poda ✂️
            continue
            
        curr = path[-1]
        if len(path) == n:
            total = cost + graph[curr][0] # Regreso al origen
            if total < best_cost:
                best_cost, best_path = total, path + [0]
            continue
            
        for nxt in range(n):
            if nxt not in path:
                new_path = path + [nxt]
                new_cost = cost + graph[curr][nxt]
                new_lb = calc_lower_bound(graph, new_path)
                
                if new_lb < best_cost:
                    heapq.heappush(pq, (new_lb, new_cost, new_path))
                    
    return best_cost, best_path
```

---

# 1.5 Solución a la Situación Problemática

<div class="solution-box">

### 🚚 Resultado para el Problema de Logística ($N=15$)

* **Búsqueda Exhaustiva / Fuerza Bruta:**
  $4.35 \times 10^{10}$ rutas. Tiempo estimado: **~12 horas**.

* **Backtracking Puro (DFS sin cotas estrictas):**
  Explora $1.2 \times 10^8$ nodos. Tiempo estimado: **~15 minutos**.

* **Branch & Bound con Best-First (Cola de Prioridad + LB):**
  Gracias a la poda agresiva con $LB \ge Best\_Cost$, se evalúan únicamente **18,500 nodos**.
  Tiempo de ejecución: **0.18 segundos**.

**Conclusión:** Branch & Bound reduce la búsqueda en un factor de **2,000,000x** comparado con la fuerza bruta, encontrando la ruta óptima demostrable.
</div>

---

# 1.5 Matriz Comparativa Final del Tema 1

| Técnica | Adecuada para... | Subproblemas | ¿Requiere Cotas? | Complejidad Típica |
| :--- | :--- | :--- | :--- | :--- |
| **Divide y Vencerás** | Problemas desglosables | Independientes | No | $O(N \log N)$ |
| **Prog. Dinámica** | Optimización con repeticiones | Solapados | No | $O(N \cdot K)$ (Polinomial) |
| **Algoritmos Avaros** | Elecciones locales de óptimo global | Subestr. Óptima | No | $O(N \log N)$ |
| **Backtracking** | Búsqueda con restricciones | Árbol de Estados | No | $O(b^d)$ (Exponencial) |
| **Branch & Bound** | Optimización combinatoria exacta | Árbol de Estados | **Sí (LB / UB)** | $O(b^d)$ con poda |

---

# Conclusiones y Próximos Pasos

---

# Conclusiones del Tema 1

1. **No existe una técnica única universal:** El éxito del ingeniero de software radica en reconocer la **geometría y propiedades** del problema.
2. Si los subproblemas son independientes $\implies$ **Divide y Vencerás**.
3. Si los subproblemas se solapan $\implies$ **Programación Dinámica**.
4. Si una regla local garantiza el óptimo global $\implies$ **Algoritmo Avaro (Greedy)**.
5. Si debemos explorar combinaciones complejas $\implies$ **Backtracking** o **Branch & Bound**.

---

# Preguntas de Repaso

1. ¿Por qué la multiplicación de Karatsuba logra una complejidad de $O(n^{1.585})$ mientras que la tradicional es $O(n^2)$?
2. Explica la diferencia entre la técnica de *Memorización* y la de *Tabulación* en Programación Dinámica.
3. Demuestra por qué el algoritmo Greedy de selección de actividades **falla** si ordenamos por tiempo de inicio en lugar de tiempo de finalización.
4. ¿En qué escenario un algoritmo de Branch & Bound se comporta exactamente igual que un algoritmo de Backtracking?
5. ¿Qué es una cota inferior ($Lower\_Bound$) y cómo influye en la velocidad de ejecución de Branch & Bound?

---

# ¡Gracias por su atención!

**Siguiente Clase:** Tema 2 - Manejo de Strings Avanzado.