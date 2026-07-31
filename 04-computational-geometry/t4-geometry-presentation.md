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
## Tema 4: Geometría Computacional

**Profesor - Alison Muñoz Capote**
*Tecnológico de Monterrey*

---

# Mapa del Tema 4 y Objetivos

### Objetivos del Tema:
1. Comprender y aplicar las primitivas geométricas básicas sin depender del uso intensivo de trigonometría.
2. Resolver problemas de proximidad y colisión en el plano 2D de manera eficiente.
3. Analizar e implementar algoritmos para el cálculo del Casco Convexo (Convex Hull).
4. Comprender la teoría de los Diagramas de Voronoi y su aplicación en la división territorial.

### Subtemas del Módulo:
* **4.1 Primitivas: Orientación e Intersección**
* **4.2 Inclusión de Puntos en Polígonos**
* **4.3 Par de Puntos Más Cercanos (Closest Pair)**
* **4.4 Casco Convexo (Convex Hull)**
* **4.5 Diagramas de Voronoi y Triangulación de Delaunay**

---

# Repaso Breve: Primitivas Geométricas

En Geometría Computacional, evitamos el uso de divisiones (pendientes $m = \Delta y / \Delta x$) y trigonometría ($\sin, \cos$) tanto como sea posible. 
¿Por qué? **Por los errores de precisión de punto flotante.** Preferimos sumas y multiplicaciones enteras.

* **Punto:** Un par de coordenadas $P = (x, y)$.
* **Vector:** Una dirección y magnitud $\vec{v} = P_2 - P_1 = (x_2 - x_1, y_2 - y_1)$.
* **Producto Cruz (2D):** Dado $\vec{u} = (x_1, y_1)$ y $\vec{v} = (x_2, y_2)$, su magnitud orientada es:
  $$\vec{u} \times \vec{v} = (x_1 \cdot y_2) - (x_2 \cdot y_1)$$
  *El signo del Producto Cruz nos dice si $\vec{v}$ gira a la izquierda o a la derecha respecto a $\vec{u}$.*

---

# 4.1 Orientación e Intersección de Segmentos
### (El núcleo de las colisiones 2D)

---

# 4.1 Situación Problemática: Motor de Videojuegos

<div class="problem-box">

### 🎮 Detección de Colisiones (Ray Casting)
Estás desarrollando un motor de física para un videojuego 2D. Tienes el trayecto de una bala (Segmento $A: P_1 \rightarrow P_2$) y el muro de un edificio (Segmento $B: P_3 \rightarrow P_4$). 

* **El Enfoque Algebraico:** Calcular las ecuaciones de las dos rectas ($y = mx + b$), igualarlas para hallar el punto de intersección $(x, y)$, y verificar si ese punto está dentro de los límites de ambos segmentos.
* **El Problema:** ¿Qué pasa si el muro es vertical? La pendiente $m$ se vuelve infinito (división por cero). El código colapsa o se llena de múltiples declaraciones `if` para casos especiales.
* **Desafío:** ¿Podemos saber si dos segmentos se cruzan usando una sola fórmula matemática que jamás divida por cero y sea inmune a las líneas verticales u horizontales?
</div>

---

# 4.1 Teoría: Orientación de 3 Puntos

Dados tres puntos ordenados $A$, $B$, y $C$, ¿hacia dónde "gira" el camino si camino de $A \rightarrow B \rightarrow C$?

Calculamos el producto cruz de los vectores $\vec{AB}$ y $\vec{BC}$:
$$val = (B_y - A_y) \cdot (C_x - B_x) - (B_x - A_x) \cdot (C_y - B_y)$$

1. **$val = 0$:** Los puntos son **Colineales** (están en la misma línea).
2. **$val > 0$:** Orientación en sentido **Horario (Clockwise)** (Giro a la derecha).
3. **$val < 0$:** Orientación en sentido **Antihorario (Counterclockwise)** (Giro a la izquierda).

*Para que dos segmentos $P_1P_2$ y $P_3P_4$ se crucen, los extremos de un segmento deben quedar en lados opuestos del otro segmento.*

---

# 4.1 Implementación: Intersección de Segmentos


```python
def orientation(p, q, r):
    # Retorna: 0 (Colineal), 1 (Horario), 2 (Antihorario)
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0
    return 1 if val > 0 else 2

def on_segment(p, q, r):
    # Verifica si el punto 'q' está sobre el segmento 'pr'
    if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
        q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
        return True
    return False

def do_intersect(p1, q1, p2, q2):
    o1, o2 = orientation(p1, q1, p2), orientation(p1, q1, q2)
    o3, o4 = orientation(p2, q2, p1), orientation(p2, q2, q1)

    # Caso General: Los extremos se alternan mutuamente
    if o1 != o2 and o3 != o4: return True

    # Casos Especiales (Colineales e inscritos)
    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True

    return False
```

---

# 4.1 Solución a la Situación Problemática

<div class="solution-box">

### 🎮 Resultado para el Motor de Videojuegos

* **Colisión por Álgebra Tradicional:**
  Requiere múltiples `if/else` para evitar división por cero (cálculo de pendiente), sufre de imprecisión de redondeo `float` y requiere operaciones extras para verificar los límites del segmento.
* **Colisión por Orientación (Producto Cruz):**
  Usando la función `do_intersect`, realizamos únicamente multiplicaciones, restas y comparaciones lógicas. 
  1. Si las coordenadas son enteras, no hay pérdida de precisión (el producto cruz da un número entero exacto).
  2. Nunca hay división por cero; las líneas verticales se procesan con la misma rapidez que las horizontales.
  3. Ejecución en tiempo constante matemático puro $O(1)$.

**Conclusión:** La geometría orientada mediante el producto cruz ofrece la forma más rápida y estable computacionalmente para detectar intersecciones.
</div>

---

# 4.2 Inclusión de Puntos en Polígonos
### (Tiempo Estimado: 1.5 Horas)

---

# 4.2 Situación Problemática: Geocercas (Geofencing)

<div class="problem-box">

### 📍 Delimitación de Zonas de Entrega
Trabajas para una app de delivery. Tienes las coordenadas GPS que forman un polígono complejo de 50 vértices (la "Zona de Entrega Norte"). Recibes la coordenada actual del repartidor ($P_0$).

* **El Problema:** El polígono no es un cuadrado simple ni un círculo perfecto, es **cóncavo** (tiene formas irregulares, bahías, "entradas" y "salidas").
* **La Intuición Geométrica:** No basta con medir la distancia al centro. Un repartidor podría estar físicamente "cerca" del centroide, pero haber cruzado una frontera cóncava quedando fuera de la zona legal.
* **Desafío:** ¿Cómo determinar algorítmicamente si un punto cualquiera en el plano 2D está estrictamente *dentro* o *fuera* de un polígono irregular de $N$ lados?
</div>

---

# 4.2 Teoría: Ray Casting Algorithm (Par/Impar)

Para determinar la inclusión de un punto, utilizamos el **Algoritmo del Rayo (Ray Casting / Crossing Number)**.

Imagina que estás parado en el punto $P_0$. Disparas un "rayo láser" en cualquier dirección infinita (por convención, horizontal hacia la derecha hasta $x = +\infty$).

**La Regla del Teorema de Jordan (Par / Impar):**
1. Cuenta cuántas veces cruza tu rayo los bordes del polígono.
2. Si el número de cruces es **IMPAR**, el punto está **DENTRO** del polígono.
3. Si el número de cruces es **PAR**, el punto está **FUERA**.

*Excepción Cuidado:* Si tu rayo cruza exactamente sobre un vértice del polígono, debes contar el cruce correctamente comprobando si los vértices adyacentes están a lados opuestos del rayo.

---

# 4.2 Implementación: Ray Casting en Python

```python
def is_inside_polygon(polygon, p):
    # polygon: Lista de puntos [(x1,y1), (x2,y2)...]
    n = len(polygon)
    if n < 3: return False
    
    # Crear un punto en el infinito horizontal derecho
    extreme = (10**9, p[1])
    count = i = 0
    
    while True:
        next_node = (i + 1) % n
        
        # Verificar si el segmento cruza con el rayo
        if do_intersect(polygon[i], polygon[next_node], p, extreme):
            # Si cruza y está colineal, verificar si el punto toca el borde
            if orientation(polygon[i], p, polygon[next_node]) == 0:
                return on_segment(polygon[i], p, polygon[next_node])
            count += 1
            
        i = next_node
        if i == 0: break
        
    return count % 2 == 1 # Retorna True si impar (DENTRO)
```

---

# 4.2 Solución a la Situación Problemática

<div class="solution-box">

### 📍 Resultado para las Zonas de Entrega (Geocercas)

* **Evaluación con Distancias o Centroides:**
  Basarse únicamente en el "centro" del área falla horriblemente en polígonos complejos (como formas de "U" o herraduras), validando posiciones que están físicamente fuera.
* **Con Algoritmo de Ray Casting ($O(N)$):**
  Lanzamos el rayo virtual infinito. Por cada uno de los $N=50$ lados de la geocerca, verificamos si hay intersección usando nuestra primitiva de **Orientación**.
  Como no requiere trigonometría ni divisiones, tomará exactamente 50 iteraciones de tiempo $O(1)$. 
  Tiempo de ejecución: **Fracciones de microsegundo**.

**Conclusión:** El Teorema de Jordan (Ray Casting) brinda a aplicaciones como Uber, Rappi o Didi un método algebraicamente infalible y rapidísimo para validar la pertenencia de coordenadas GPS en áreas irregulares.
</div>

---

# 4.3 Par de Puntos Más Cercanos (Closest Pair)
### (Tiempo Estimado: 1.5 Horas)

---

# 4.3 Situación Problemática: Tráfico Aéreo

<div class="problem-box">

### ✈️ Alerta de Colisión en Radar
Eres el ingeniero de sistemas del control de tráfico aéreo. En este instante, hay $N = 100,000$ aeronaves en el espacio aéreo, representadas como puntos $(x,y)$ en la pantalla del radar.

* **El Problema:** Debes hacer sonar una alerta si dos aviones se acercan peligrosamente. Para ello, necesitas encontrar rutinariamente **cuál es el par de aviones que tiene la menor distancia entre sí**.
* **La Fuerza Bruta:** Medir la distancia de cada avión contra todos los demás ($O(N^2)$) requiere $\approx 5 \times 10^9$ cálculos pitagóricos en cada barrido del radar. ¡El servidor colapsará!
* **Desafío:** ¿Cómo reducimos esto a $O(N \log N)$ para procesar los datos en tiempo real y evitar accidentes?
</div>

---

# 4.3 Teoría: Enfoque Divide y Vencerás

Podemos aplicar el mismo principio del *Merge Sort* pero en el espacio 2D.

1. **Ordenar y Dividir:** Ordenamos todos los puntos por su coordenada $X$. Trazamos una línea vertical imaginaria que divida los puntos en dos mitades exactas: Mitad Izquierda ($L$) y Mitad Derecha ($R$).
2. **Conquistar:** Recursivamente, encontramos la distancia mínima exclusiva de la mitad izquierda ($d_L$) y la de la mitad derecha ($d_R$).
3. **El Mínimo Temporal:** Sea $\delta = \min(d_L, d_R)$. ¿Es $\delta$ la respuesta definitiva final? 
   *No necesariamente.* Podría existir un avión en el extremo derecho de $L$ y otro en el extremo izquierdo de $R$ cuya distancia cruzando la frontera sea menor a $\delta$.

---

# 4.3 Teoría: La Franja Central (The Strip)

Para verificar si hay puntos cruzando la frontera divisoria a una distancia menor que $\delta$:

1. **Filtrar:** Tomamos solo los aviones cuya distancia en el eje $X$ hacia la línea central sea estrictamente menor que $\delta$. Esto crea una "franja" vertical intermedia.
2. **Ordenar por Y:** Ordenamos los puntos de esta franja por su coordenada $Y$.
3. **El Truco Geométrico:** Aunque haya muchos puntos en la franja, se demuestra matemáticamente que, al escanear de abajo hacia arriba, **solo necesitamos comparar cada punto con como máximo sus siguientes 7 vecinos**. 
   *(Si hubiera más de 7 aviones a una distancia menor que $\delta$ en esa franja, ¡esos aviones ya estarían a una distancia menor que $\delta$ entre sí y los habríamos detectado antes!)*

---

# 4.3 Implementación: Franja Central en Python

Para mantener el código limpio, dividimos la lógica. Primero, la función que evalúa la franja central (Strip) en tiempo lineal $O(N)$.

```python
import math

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def closest_strip(strip, d):
    min_d = d
    # Ordenar la franja por el eje Y
    strip.sort(key=lambda point: point[1]) 
    
    # Comprobar puntos cercanos (bucle interno es O(1) en la práctica)
    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            # Si la diferencia en Y supera a 'min_d', ya no hay necesidad de seguir
            if (strip[j][1] - strip[i][1]) >= min_d:
                break
            min_d = min(min_d, distance(strip[i], strip[j]))
            
    return min_d
```
---

# 4.3 Implementación: Closest Pair Recursivo

```python
def closest_pair_rec(points_sorted_x, points_sorted_y):
    n = len(points_sorted_x)
    # Caso base: 3 puntos o menos, usar fuerza bruta
    if n <= 3:
        return brute_force_closest(points_sorted_x)
        
    mid = n // 2
    mid_point = points_sorted_x[mid]
    
    # Dividir: Mitad izquierda y derecha
    Pyl = [p for p in points_sorted_y if p[0] <= mid_point[0]]
    Pyr = [p for p in points_sorted_y if p[0] > mid_point[0]]
    
    # Conquistar: Recursión
    dl = closest_pair_rec(points_sorted_x[:mid], Pyl)
    dr = closest_pair_rec(points_sorted_x[mid:], Pyr)
    d = min(dl, dr)
    
    # Franja Central (Strip)
    strip = [p for p in points_sorted_y if abs(p[0] - mid_point[0]) < d]
    
    return min(d, closest_strip(strip, d))
```

---

# 4.3 Solución a la Situación Problemática

<div class="solution-box">

### ✈️ Resultado para la Alerta de Colisión en Radar

* **Fuerza Bruta ($O(N^2)$):**
  Para $100,000$ aviones, realizar la comparación de todos contra todos toma $\approx 5 \times 10^9$ operaciones por cada frame del radar. Esto introduciría "lag" (retraso) en una pantalla de control de tráfico aéreo, lo cual es fatal.
* **Divide y Vencerás ($O(N \log N)$):**
  1. El ordenamiento inicial toma $O(N \log N)$.
  2. La división recursiva del plano toma $\log N$ niveles de profundidad.
  3. El filtrado y revisión de la "Franja Central" toma tiempo lineal $O(N)$ en cada nivel, gracias al límite matemático de 7 comparaciones.
  Tiempo total de ejecución: **< 0.1 segundos**.

**Conclusión:** Hemos resuelto un problema geométrico bidimensional masivo utilizando puramente principios de diseño de algoritmos (Divide y Vencerás), permitiendo rastreo de proximidad en tiempo real.
</div>

---

# 4.4 Casco Convexo (Convex Hull)
### (Tiempo Estimado: 2.5 Horas)

---

# 4.4 Situación Problemática: Cerca Perimetral

<div class="problem-box">

### 🌲 Envolviendo la Reserva Forestal
El departamento de silvicultura ha mapeado con GPS la ubicación exacta de $N = 20,000$ árboles milenarios. Tienen el presupuesto justo para comprar una cerca de malla ciclónica. Quieren rodear **todos** los árboles utilizando la **menor cantidad de metros de cerca posible**.

* **El Problema Físico:** Imagina que los árboles son clavos en una tabla de madera. Si tomas una liga de goma (banda elástica) gigante, la estiras alrededor de todos los clavos y la sueltas, la forma que tomará la liga al contraerse es exactamente el polígono que buscamos.
* **Geometría:** Ese polígono se llama **Casco Convexo (Convex Hull)**. Es el polígono convexo más pequeño que contiene a todos los puntos.
* **Desafío:** ¿Cómo logramos que la computadora "suelte la liga" matemáticamente en tiempo $O(N \log N)$ y detecte qué árboles forman el borde exterior?
</div>

---

# 4.4 Teoría: Algoritmo Monotone Chain (Andrew)

Existen muchos algoritmos para este problema (Jarvis March, Graham Scan). Estudiaremos la **Cadena Monótona de Andrew** por ser extremadamente elegante y reutilizar nuestra función de `orientation()`.

### El Concepto:
Construimos el polígono en dos mitades: la **Cadena Superior** (techo) y la **Cadena Inferior** (suelo).

1. **Ordenamiento inicial:** Ordenamos todos los puntos por su coordenada X (de izquierda a derecha). En caso de empate, por su coordenada Y.
2. El primer punto (el más a la izquierda) y el último punto (el más a la derecha) **siempre** formarán parte del casco convexo.

---

# 4.4 Teoría: Filtro de Giro a la Izquierda

La clave del algoritmo es mantener una **Pila (Stack)** temporal de los vértices que conforman el borde.

Al procesar los puntos de izquierda a derecha (para la cadena inferior):
1. Añadimos el punto actual a la pila.
2. Revisamos los **últimos 3 puntos** de la pila.
3. Calculamos su orientación. Si el giro al ir de `P1 -> P2 -> P3` es **hacia la derecha** (o colineal), significa que el punto intermedio forma una "abolladura" o concavidad hacia adentro.
4. Como la liga de goma nunca se abollaría hacia adentro, **eliminamos (pop) el punto intermedio de la pila**.
5. Repetimos hasta que los últimos 3 puntos siempre den un estricto **giro a la izquierda (Antihorario)**.

---

# 4.4 Implementación: Casco Convexo (Andrew's Monotone Chain)

```python
def convex_hull(points):
    # Ordenar por X, y en caso de empate por Y
    points = sorted(set(points))
    if len(points) <= 1: return points

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Construir la cadena inferior (Lower Hull)
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Construir la cadena superior (Upper Hull)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # El último punto de cada cadena es el primero de la otra
    return lower[:-1] + upper[:-1]
```

---

# 4.4 Solución a la Situación Problemática

<div class="solution-box">

### 🌲 Resultado para la Reserva Forestal

* **Fuerza Bruta (Envoltura de Regalo / Jarvis March):**
  Toma $O(N \times h)$ donde $h$ es el número de puntos en el perímetro. Si todos los $20,000$ árboles formaran un círculo gigante, tomaría $O(N^2) \approx 4 \times 10^8$ operaciones.
* **Cadena Monótona de Andrew ($O(N \log N)$):**
  1. Ordenar los $20,000$ puntos toma $\approx 2.8 \times 10^5$ operaciones.
  2. Construir ambas cadenas toma tiempo estrictamente lineal $O(N)$, porque cada punto se añade (push) y se elimina (pop) de la pila **como máximo una vez**.
  Tiempo total de ejecución: **< 0.05 segundos**.

**Conclusión:** Encontramos la forma perimetral óptima para la cerca minimizando el gasto en material. El uso de una Pila (Stack) convierte un problema de filtrado 2D complejo en un recorrido de tiempo lineal.
</div>

---

# 4.5 Diagramas de Voronoi y Triangulación de Delaunay
### (Tiempo Estimado: 2.5 Horas)

---

# 4.5 Situación Problemática: Zonas de Cobertura

<div class="problem-box">

### 🏥 Despliegue de Ambulancias en la Ciudad
Una metrópoli tiene $N = 500$ estaciones de ambulancia dispersas en su geografía. Cuando ocurre un accidente en la coordenada $P = (x, y)$, el sistema debe enviar inmediatamente la ambulancia **más cercana**.

* **Fuerza Bruta:** Comparar la distancia del accidente con las 500 estaciones toma $O(N)$. 
* **El Problema Real:** El sistema de emergencias procesa millones de llamadas al día. Calcular $O(N)$ por cada llamada genera un inmenso consumo de CPU. Necesitamos una búsqueda en tiempo logarítmico $O(\log N)$.
* **Desafío:** ¿Podemos "dividir" el mapa de la ciudad en sectores precalculados, de tal forma que con solo saber en qué sector cayó el accidente, sepamos instantáneamente qué estación es la dueña de esa zona?
</div>

---

# 4.5 Teoría: Diagramas de Voronoi

Un **Diagrama de Voronoi** es la partición definitiva del espacio. Dado un conjunto de puntos "semilla" (las estaciones de ambulancia), el espacio se divide en **celdas o polígonos**.

Cada celda representa el área de influencia de una semilla. 
*Propiedad principal:* **Cualquier coordenada dentro de una celda está estrictamente más cerca de la semilla de esa celda que de cualquier otra semilla en todo el mapa.**

### ¿Cómo se construyen las fronteras?
Las fronteras que separan dos celdas adyacentes son segmentos de la **bisectriz perpendicular** de la línea imaginaria que une a las dos semillas. Si te paras exactamente en la frontera, estás a la misma distancia de ambas estaciones.

---

# 4.5 Teoría: Triangulación de Delaunay (El Grafo Dual)

Si trazamos una arista entre las semillas de aquellas celdas de Voronoi que comparten una frontera, obtenemos una malla de triángulos conocida como la **Triangulación de Delaunay**.

### Propiedades Matemáticas Fascinantes:
1. **El Círculo Vacío (Empty Circumcircle):** Si dibujas un círculo perfecto que pase por los 3 vértices de cualquier triángulo de Delaunay, **ningún otro punto del grafo** estará dentro de ese círculo.
2. **Maximiza el ángulo mínimo:** De todas las formas posibles de triangular los puntos, Delaunay evita producir triángulos "delgados y alargados" (astillas), lo que la hace ideal para modelado 3D y gráficos por computadora.

*El Diagrama de Voronoi y la Triangulación de Delaunay son las dos caras de una misma moneda (Grafos Duales).*

---

# 4.5 Construcción y Búsqueda Espacial

Construir estos diagramas con fuerza bruta (calculando todas las intersecciones de mediatrices) tomaría $O(N^4)$. Afortunadamente, tenemos algoritmos óptimos:

### Algoritmo de Fortune (Línea de Barrido / Sweep Line)
Inventado por Steven Fortune (1986), utiliza una línea vertical imaginaria que "barre" el plano de izquierda a derecha. Mantiene el estado del diagrama usando una estructura de árbol binario balanceado (para la "línea de playa" parabólica) y una cola de prioridad para los "eventos" de cruce. 
* **Complejidad de Construcción:** $O(N \log N)$.

### Localización de Puntos (Point Location)
Una vez construido el Diagrama de Voronoi, lo pre-procesamos en una estructura de Búsqueda Espacial (como un *Trapezoidal Map* o *Quadtree*). Esto nos permite que, dado un punto $P$ cualquiera, encontrar a qué polígono pertenece tome exactamente **$O(\log N)$**.

---

# 4.5 Solución a la Situación Problemática

<div class="solution-box">

### 🏥 Resultado para el Sistema de Ambulancias

* **Fuerza Bruta Lineal ($O(N)$):**
  Para $N=500$ estaciones y millones de llamadas, calcular distancias repetidamente satura los servidores, aumenta la latencia del sistema y cuesta valiosos segundos de vida en el despacho.
* **Diagrama de Voronoi + Búsqueda Espacial ($O(\log N)$):**
  1. El mapa de la metrópoli se divide en 500 celdas de Voronoi *offline* (una sola vez al inicio del día) en milisegundos.
  2. Cuando entra la llamada con el GPS del accidente, la base de datos realiza una búsqueda espacial estructurada tomando $\approx 9$ operaciones ($\log_2 500 \approx 9$).
  Tiempo de despacho computacional: **Instantáneo (< 0.0001 ms)** por accidente.

**Conclusión:** Voronoi transforma un problema de cálculo continuo de distancias en un problema de búsqueda precalculada, logrando escalabilidad infinita para los sistemas logísticos modernos.
</div>

---

# 4.6 Matriz Comparativa Final del Tema 4

| Problema / Técnica | Herramienta Principal | Complejidad | Caso de Uso Real |
| :--- | :--- | :--- | :--- |
| **Cruce de Segmentos** | Producto Cruz (Orientación)| $O(1)$ | Motor físico de videojuegos |
| **Punto en Polígono** | Ray Casting (Teorema Jordan)| $O(N)$ lados | Geocercas (Delivery/Drones) |
| **Par Más Cercano** | Divide y Vencerás (Strip) | $O(N \log N)$ | Control de Tráfico Aéreo |
| **Casco Convexo** | Monotone Chain (Pila + Cruz)| $O(N \log N)$ | Delimitación de perímetros |
| **Cobertura Espacial** | Voronoi / Fortune | $O(N \log N)$ | Asignación de servicios |
| **Mallas 3D óptimas** | Triangulación Delaunay | $O(N \log N)$ | Gráficos por computadora |

---

# Conclusiones y Próximos Pasos

---

# Conclusiones y Preguntas de Repaso

### Conclusiones del Módulo:
1. **Evitar los Flotantes:** La división y la trigonometría introducen errores de precisión letales. El *Producto Cruz* es el rey indiscutible de la geometría 2D robusta.
2. **El Paradigma Espacial:** *Divide y Vencerás* no solo sirve para arreglos lineales (Merge Sort), sino que brilla al partir el plano cartesiano en cuadrantes.
3. **El Pre-procesamiento salva vidas:** Construir un Diagrama de Voronoi o un Casco Convexo "una vez", permite que miles de consultas posteriores se respondan en tiempo logarítmico.

### Preguntas de Repaso:
1. Explica matemáticamente por qué usar la fórmula de la pendiente ($m$) para detectar colisiones es una mala práctica en programación.
2. En el algoritmo *Ray Casting*, ¿qué sucede si el rayo pasa exactamente por encima de un vértice del polígono? ¿Cómo lo manejas en el código?
3. En el problema del "Par Más Cercano", ¿por qué solo necesitamos comparar cada punto de la franja central con un máximo de 7 vecinos?
4. ¿Qué significa que tres puntos den un "giro a la derecha" al calcular un Casco Convexo, y qué acción desencadena esto en la pila?

---

# ¡Gracias por su atención!

**Siguiente Clase:** Tema 5 - Técnicas de Búsqueda Avanzada (Heurísticas, A*, y Problemas NP-Hard).
