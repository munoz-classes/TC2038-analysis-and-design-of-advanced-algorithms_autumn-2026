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
## Tema 3: Grafos y Algoritmos de Redes (14 Horas)

**Profesor - Alison Muñoz Capote**
*Tecnológico de Monterrey*

---

# Mapa del Tema 3 y Objetivos

### Objetivos del Tema:
1. Dominar representaciones eficientes de grafos y estructuras de prefijos.
2. Analizar e implementar algoritmos de rutas óptimas, árboles de recubrimiento mínimo y flujo en redes.
3. Resolver problemas clasificados como NP-completos sobre grafos.
4. Aplicar modelos de grafos a sistemas reales de transporte, telecomunicaciones y redes.

### Subtemas del Módulo:
* **3.1 Trie** | **3.2 Ruta Cobertura DAG** | **3.3 Dijkstra** | **3.4 Floyd-Warshall**
* **3.5 Mochila en Grafos** | **3.6 Agente Viajero (TSP)** | **3.7 Prim**
* **3.8 Kruskal** | **3.9 ABB Óptimo (Gilbert & Moore)** | **3.10 Coloreo** | **3.11 Flujo Máximo**

---

# Repaso Breve: Formalismo de Grafos

Un grafo $G = (V, E)$ consta de un conjunto de vértices $V$ y aristas $E$.

* **Direccionado vs No Direccionado:** Aristas con o sin sentido explícito.
* **Grafo Ponderado:** Cada arista $(u, v)$ posee un peso o costo $w(u, v) \in \mathbb{R}$.
* **Representaciones en Memoria:**
  * **Matriz de Adyacencia ($V \times V$):** Acceso $O(1)$, Espacio $O(V^2)$. Ideal para grafos densos ($E \approx V^2$).
  * **Lista de Adyacencia:** Espacio $O(V + E)$. Ideal para grafos dispersos ($E \ll V^2$).

---

# 3.1 Trie (Árbol Prefijo)
### (Tiempo Estimado: 1.0 Hora)

---

# 3.1 Situación Problemática: Auto-completado Real

<div class="problem-box">

### 🔍 Motor de Sugerencias de Búsqueda
Un buscador procesa millones de palabras clave. Cuando un usuario escribe un prefijo como `"alg"`, el sistema debe devolver en **milisegundos** todas las palabras del diccionario ($N = 500,000$ palabras) que inicien con `"alg"`.

* **Fuerza Bruta en Arreglo:** Recorrer todo el diccionario comparando prefijos con KMP tomaría $O(N \times |P|)$.
* **Búsqueda Binaria en Arreglo Ordenado:** $O(|P| \log N)$ para encontrar el rango, pero insertar o eliminar palabras dinámicamente requiere desplazar elementos en $O(N)$.
* **Desafío:** ¿Podemos buscar e insertar palabras en tiempo proporcional **únicamente a la longitud de la palabra** $O(|W|)$, sin depender de la cantidad total de palabras $N$?
</div>

---

# 3.1 ¿Qué es un Trie?

Un **Trie** (o Árbol Prefijo) es una estructura de datos en árbol utilizada para almacenar un conjunto de cadenas donde los nodos comparten prefijos comunes.

### Propiedades Clave:
1. La **Raíz** representa una cadena vacía.
2. Cada **Arista** está etiquetada con un carácter del alfabeto $\Sigma$.
3. Un **Nodo** almacena una bandera booleana (`is_end_of_word`) indicando si la ruta desde la raíz forma una palabra válida.
4. Si dos palabras comparten un prefijo de longitud $K$, comparten exactamente los mismos primeros $K$ nodos en el árbol.

---

# 3.1 Implementación de Trie en Python

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False  # El prefijo no existe
            node = node.children[char]
        return True  # Existen palabras con este prefijo
```

---

# 3.1 Solución a la Situación Problemática

<div class="solution-box">

### 🔍 Resultado para el Motor de Búsqueda

* **Búsqueda en Arreglos Tradicionales:**
  Para $N = 500,000$ palabras, buscar un prefijo y actualizar el diccionario requeriría desplazar posiciones en memoria ($O(N)$), bloqueando la base de datos con cada inserción.
* **Con la Estructura Trie:**
  1. Insertar una nueva palabra toma $O(|W|)$. Si la palabra tiene 10 letras, son solo 10 operaciones en el diccionario de nodos.
  2. Buscar si el prefijo "alg" existe toma $O(|P|) \implies$ **¡Exactamente 3 saltos de puntero!** Independientemente de que el diccionario tenga 100 o 10 millones de palabras.

**Conclusión:** El Trie desacopla el tiempo de búsqueda del tamaño de la base de datos, posibilitando el auto-completado en milisegundos mientras el usuario teclea.
</div>

---

# 3.2 Ruta Cobertura en DAG (Grafos Acíclicos Dirigidos)
### (Tiempo Estimado: 1.0 Hora)

---

# 3.2 Situación Problemática: Gestión de Proyectos

<div class="problem-box">

### 🏗️ La Ruta Crítica en la Construcción
Diriges la construcción de un rascacielos. Tienes $V = 10,000$ tareas. Muchas tareas dependen estrictamente de otras (ej. no puedes poner el techo sin antes levantar los muros). Conoces el tiempo que toma cada tarea.

* **El Problema:** Si asignas infinitos trabajadores para hacer tareas en paralelo, ¿cuál es el **tiempo mínimo** absoluto en el que se puede terminar todo el proyecto?
* **Modelado:** Es un Grafo Acíclico Dirigido (DAG). Los vértices son etapas, las aristas son dependencias, y los pesos son el tiempo. Buscamos el **camino más largo** (Ruta Crítica) desde el inicio hasta el fin.
* **El Desafío:** En grafos generales, hallar el camino más largo es un problema *NP-Hard*. ¿Cómo lo resolvemos eficientemente aquí?
</div>

---

# 3.2 Ordenamiento Topológico: La Clave del DAG

Un **Grafo Acíclico Dirigido (DAG)** tiene una propiedad matemática única: sus vértices se pueden alinear en una secuencia lineal (de izquierda a derecha) de tal forma que **todas las aristas apunten hacia adelante**.

### ¿Cómo obtenerlo? (Algoritmo de Kahn)
1. Llevar un conteo de los "grados de entrada" (`in-degree`) de cada vértice.
2. Colocar en una Cola los nodos con `in-degree == 0` (tareas sin prerrequisitos).
3. Extraer un nodo, agregarlo al orden topológico, y reducir el `in-degree` de sus vecinos.
4. Si un vecino llega a `in-degree == 0`, insertarlo en la cola.

**Complejidad:** $O(V + E)$. Explora cada vértice y arista exactamente una vez.

---

# 3.2 Relajación Dinámica sobre el DAG

Una vez que tenemos el **Orden Topológico**, procesamos los vértices de izquierda a derecha. Como sabemos que no hay aristas hacia atrás (no hay ciclos), podemos aplicar **Programación Dinámica** de forma lineal sin preocuparnos de bucles infinitos.

### Ecuación de Relajación para la Ruta Más Larga:
Para cada vértice $u$ en el orden topológico, revisamos sus vecinos $v$:
$$dist[v] = \max(dist[v], dist[u] + peso(u, v))$$

* Esta técnica garantiza que al llegar al turno de procesar un vértice $v$, **ya hemos evaluado todos los caminos posibles** que llevan a él.
* Funciona idéntico para la **Ruta Más Corta** (simplemente cambiando $\max$ por $\min$).

---

# 3.2 Implementación: Ruta Crítica en DAG

```python

from collections import deque, defaultdict

def longest_path_dag(vertices, edges):
    adj = defaultdict(list)
    in_degree = {v: 0 for v in vertices}
    for u, v, weight in edges:
        adj[u].append((v, weight))
        in_degree[v] += 1
        
    # 1. Orden Topológico (Kahn)
    queue = deque([v for v in vertices if in_degree[v] == 0])
    topo_order = []
    
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v, _ in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
    # 2. Relajación (Programación Dinámica)
    dist = {v: float('-inf') for v in vertices}
    dist[topo_order[0]] = 0  # Nodo inicial
    
    for u in topo_order:
        if dist[u] != float('-inf'):
            for v, weight in adj[u]:
                if dist[u] + weight > dist[v]:
                    dist[v] = dist[u] + weight
                    
    return max(dist.values())
```

---

# 3.2 Solución a la Situación Problemática

<div class="solution-box">

### 🏗️ Resultado para el Proyecto de Construcción

* **Evaluación Ingenua (Fuerza Bruta):**
  En un grafo con $10,000$ nodos, buscar todas las rutas posibles del inicio al fin para encontrar la más larga tomaría un tiempo factorial o exponencial $O(2^V)$, imposible de calcular antes de que termine el siglo.
* **Evaluación con Orden Topológico y DP ($O(V + E)$):**
  1. Encontramos el orden de las tareas en $O(V + E)$.
  2. Relajamos las aristas una sola vez de izquierda a derecha en $O(V + E)$.
  Para $10,000$ vértices y $30,000$ dependencias, son **$\approx 40,000$ operaciones simples**.
  Tiempo de ejecución: **< 0.05 segundos**.

**Conclusión:** Aprovechar la propiedad "Acíclica" del grafo nos permite usar Programación Dinámica lineal para resolver en milisegundos un problema que de otro modo sería intratable.
</div>

---

# 3.3 Algoritmo de Dijkstra
### (Tiempo Estimado: 1.5 Horas)

---

# 3.3 Situación Problemática: Navegación GPS

<div class="problem-box">

### 🗺️ El Motor de Rutas de Google Maps / Waze
Un sistema GPS modela una ciudad como un grafo donde las intersecciones son vértices ($V = 500,000$) y las calles son aristas ($E = 1,500,000$). Las aristas tienen pesos (distancia o tiempo estimado de llegada). Quieres ir del punto A al punto B lo más rápido posible.

* **El Problema con BFS:** La Búsqueda en Anchura (BFS) encuentra la ruta con *menos saltos* (aristas), pero no funciona si las aristas tienen pesos diferentes (una autopista de 10km vs 10 cuadras de 1km).
* **El Problema con DAGs:** La ciudad **tiene ciclos** (puedes dar la vuelta a la manzana). No podemos usar ordenamiento topológico.
* **Desafío:** ¿Cómo encontramos la ruta más corta (o rápida) desde un nodo origen a todos los demás nodos en un grafo con pesos y ciclos, sin quedarnos atrapados en un bucle infinito?
</div>

---

# 3.3 Filosofía de Dijkstra

Diseñado por Edsger W. Dijkstra en 1956, es un **Algoritmo Avaro (Greedy)** clásico. 

**La idea central:** Mantenemos un conjunto de nodos cuyas distancias mínimas desde el origen ya son definitivas. En cada paso, expandimos nuestra "frontera" eligiendo el nodo no visitado que tenga la **distancia acumulada más pequeña**.

### Los 3 Pilares del Algoritmo:
1. **Cola de Prioridad (Min-Heap):** Nos permite extraer el nodo más cercano en tiempo $O(\log V)$ en lugar de buscarlo linealmente en $O(V)$.
2. **Relajación de Aristas:** Si encontramos un camino hacia $V$ pasando por $U$ que es mejor que el camino que conocíamos hacia $V$, actualizamos la distancia:
   `if dist[U] + weight < dist[V] then dist[V] = dist[U] + weight`
3. **Pesos No Negativos:** Dijkstra asume que viajar por una arista *siempre suma* distancia. **Falla matemáticamente si hay aristas con peso negativo** (Para eso usaremos Bellman-Ford o Floyd-Warshall).

---

# 3.3 Implementación de Dijkstra en Python


```python
import heapq

def dijkstra(graph, start):
    # graph es un diccionario de listas de adyacencia: {u: [(v, peso), ...]}
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    
    # Min-heap almacena tuplas: (distancia_acumulada, nodo)
    pq = [(0, start)]
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        # Si sacamos un nodo desactualizado (ya encontramos una ruta mejor antes)
        if current_dist > dist[u]:
            continue
            
        for v, weight in graph[u]:
            distance = current_dist + weight
            
            # Relajación
            if distance < dist[v]:
                dist[v] = distance
                heapq.heappush(pq, (distance, v))
                
    return dist
```
---

# 3.3 Solución a la Situación Problemática

<div class="solution-box">

### 🗺️ Resultado para la Navegación GPS

* **El problema de BFS:** Ignora los pesos (tráfico/distancia) y solo cuenta esquinas. Te enviaría por calles lentas si son numéricamente menos tramos.
* **Fuerza Bruta:** Explorar todas las rutas en una ciudad con ciclos es un bucle infinito.
* **Con Algoritmo de Dijkstra ($O(E \log V)$):**
  Para $V = 500,000$ y $E = 1,500,000$:
  El uso de una cola de prioridad (Min-Heap) permite encontrar el siguiente nodo a explorar en $\approx 19$ operaciones ($\log_2 500,000$).
  El total de operaciones en el peor caso ronda los $\approx 3 \times 10^7$, lo cual un servidor moderno ejecuta en **< 0.1 segundos**.

**Conclusión:** Dijkstra garantiza matemáticamente la ruta óptima expandiendo un "círculo de conocimiento" desde el origen, siendo el núcleo de cualquier sistema de navegación moderno.
</div>

---

# 3.4 Algoritmo de Floyd-Warshall
### (Tiempo Estimado: 1.0 Hora)

---

# 3.4 Situación Problemática: Tablas de Enrutamiento

<div class="problem-box">

### 🌐 Telecomunicaciones y Nodos Troncales
Trabajas en un proveedor de Internet con $V = 1,000$ enrutadores principales. Para que los paquetes de datos viajen por la red, **cada enrutador necesita conocer la ruta más corta hacia todos los demás 999 enrutadores** para construir su tabla de enrutamiento estática. Además, algunos enlaces tienen "pesos negativos" (por acuerdos comerciales de subsidio de tráfico).

* **Usando Dijkstra:** Tendríamos que ejecutar Dijkstra 1,000 veces (una vez por cada nodo origen). Peor aún, ¡Dijkstra **falla matemáticamente** y se cicla si existen pesos negativos!
* **Desafío:** ¿Cómo calcular la distancia mínima entre *absolutamente todos los pares de nodos* simultáneamente, manejando aristas negativas y en un código extremadamente simple?
</div>

---

# 3.4 Teoría: Programación Dinámica en Grafos

El Algoritmo de Floyd-Warshall (1962) abandona el enfoque *Greedy* de Dijkstra y utiliza **Programación Dinámica**.

En lugar de avanzar por aristas, se pregunta:
*"¿Qué pasa si intento ir del nodo $i$ al nodo $j$, pero usando el nodo $k$ como un atajo intermedio?"*

### La Ecuación de Transición de Estados:
Mantenemos una matriz de distancias $D$ de tamaño $V \times V$.
Para cada posible nodo intermedio $k$ (desde 0 hasta $V-1$), actualizamos toda la matriz:

$$D[i][j] = \min(D[i][j], \,\, D[i][k] + D[k][j])$$

Si la ruta directa de $i$ a $j$ es más larga que ir de $i \to k$ y luego de $k \to j$, nos quedamos con la ruta a través de $k$.

---

# 3.4 Implementación de Floyd-Warshall en Python

```python
def floyd_warshall(V, edges):
    # Inicializar la matriz de distancias con infinito
    dist = [[float('inf')] * V for _ in range(V)]
    
    # La distancia de un nodo a sí mismo es 0
    for i in range(V):
        dist[i][i] = 0
        
    # Cargar los pesos iniciales de las aristas
    for u, v, weight in edges:
        dist[u][v] = weight
        
    # Programación Dinámica: Los 3 bucles anidados
    for k in range(V):          # Nodo intermedio
        for i in range(V):      # Nodo origen
            for j in range(V):  # Nodo destino
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    
    return dist
```

---

# 3.4 Solución a la Situación Problemática

<div class="solution-box">

### 🌐 Resultado para la Red de Enrutadores

* **Complejidad del Algoritmo:** Observando los 3 bucles anidados `for` que van de $0$ a $V$, es evidente que la complejidad temporal es exactamente **$O(V^3)$** y la espacial es **$O(V^2)$**.
* **Ejecución Real:** Para $V = 1,000$ enrutadores, el algoritmo realizará $10^9$ comparaciones. En un lenguaje compilado (C++/Java), esto toma apenas **$\approx 1$ a $2$ segundos**.
* **Detección de Anomalías:** Si después de ejecutar el algoritmo, algún elemento de la diagonal principal `dist[i][i]` es menor a cero, significa que encontramos un **Ciclo de Peso Negativo** en la red (una falla crítica de configuración que genera un bucle de tráfico infinito), algo que Dijkstra jamás habría detectado.

**Conclusión:** Floyd-Warshall cambia velocidad teórica por simplicidad suprema y robustez ante pesos negativos.
</div>

---

# 3.5 Mochila en Grafos (DP con Restricciones)
### (Tiempo Estimado: 1.0 Hora)

---

# 3.5 Situación Problemática: Rescate con Tiempo Límite

<div class="problem-box">

### 🎒 Exploración de Ruinas con Recursos
Un robot explorador entra en una red de cuevas (Grafo $G$). Cada cueva $v$ contiene un mineral de valor $val[v]$. Moverse por la arista $(u, v)$ consume un tiempo $w(u, v)$. El robot tiene una batería que dura exactamente $T_{max}$ minutos.

* **El Problema Clásico:** En la mochila 0/1 estándar del Tema 1, los elementos no tienen restricciones de "ruta" para ser recolectados. Aquí, recolectar un elemento en $v$ obliga al robot a pagar el costo de viajar por el grafo hasta $v$.
* **Desafío:** ¿Cómo maximizamos el valor rescatado sin que el robot se quede sin batería a mitad de camino, sabiendo que la ubicación actual restringe qué decisiones futuras son físicamente posibles?
</div>

---

# 3.5 Teoría e Implementación: Estados de Grafo

Fusionamos Programación Dinámica con el recorrido del Grafo. Definimos el estado `dp(u, t)` como el **valor máximo** obtenible empezando en el nodo $u$ con $t$ tiempo restante.

```python
def knapsack_graph(u, time_left, memo, graph, values):
    if time_left < 0: 
        return float('-inf') # Ruta inválida (batería agotada)
    if (u, time_left) in memo: 
        return memo[(u, time_left)]
    
    best_val = values[u] # Opción 1: Me detengo aquí
    
    # Opción 2: Viajo a un vecino y sigo explorando
    for v, travel_time in graph[u]:
        if time_left >= travel_time:
            # Recursión reduciendo el tiempo disponible
            val = values[u] + knapsack_graph(v, time_left - travel_time, memo, graph, values)
            best_val = max(best_val, val)
            
    memo[(u, time_left)] = best_val
    return best_val
```

---

# 3.6 Problema del Agente Viajero (TSP)
### (Tiempo Estimado: 1.5 Horas)

---

# 3.6 Situación Problemática: Logística Perfecta

<div class="problem-box">

### 🚚 Reparto de Paquetería
Un conductor de reparto debe salir de la central (nodo 0), entregar paquetes en $N$ ciudades exactamente **una vez**, y regresar a la central minimizando la distancia o consumo de combustible total.

* **Fuerza Bruta:** Generar todas las permutaciones de ciudades toma $O(N!)$. Para $N = 20$, $20! \approx 2.4 \times 10^{18}$. ¡El servidor tardaría siglos en terminar!
* **Algoritmos Avaros (Greedy):** Ir siempre a la ciudad más cercana suele ser una "trampa" que te deja aislado lejos de la central al final de la ruta, forzando un retorno carísimo.
* **Desafío:** ¿Podemos resolver esto de manera óptima (matemáticamente exacta) en un tiempo mucho menor que factorial, digamos $O(2^N \cdot N^2)$, haciendo viable calcularlo para $N=20$ en microsegundos?
</div>

---

# 3.6 Teoría: DP con Máscaras de Bits (Bitmasking)

Para usar Programación Dinámica en el TSP, el subproblema necesita saber: en qué ciudad estamos actualmente y **qué ciudades ya visitamos** históricamente en esta ruta.

Como $N \le 20$, podemos representar el conjunto de ciudades visitadas como un **número entero** usando sus bits (Máscara de Bits).

### Representación del Estado:
* Supongamos $N = 4$ ciudades. Visitadas: `{0, 2, 3}`.
* Binario: `1101` (El bit $i$ es 1 si la ciudad $i$ fue visitada). Decimal = $13$.
* **Estado DP:** `dp[u][mask]` $\implies$ "Costo mínimo para visitar las ciudades faltantes y volver al inicio, si estoy en la ciudad `u` y ya visité las ciudades indicadas en `mask`".

**Transición General:**
$$dp[u][mask] = \min_{v \notin mask} \Big( dist(u, v) + dp[v][mask \cup \{v\}] \Big)$$

---

# 3.6 Implementación: TSP con Máscaras de Bits

```python
def tsp_bitmask(graph, u, mask, memo, n):
    # Caso base: Si ya visitamos todas las ciudades
    if mask == (1 << n) - 1:
        # Retornar a la ciudad de origen (0)
        return graph[u][0] if graph[u][0] > 0 else float('inf')
        
    if memo[u][mask] != -1:
        return memo[u][mask]
        
    ans = float('inf')
    # Intentar visitar cada ciudad 'v' no visitada aún
    for v in range(n):
        if (mask & (1 << v)) == 0:  # Si el bit 'v' es 0 (no visitada)
            if graph[u][v] > 0:     # Si hay camino
                # Llamada recursiva marcando el bit 'v' como 1
                cost = graph[u][v] + tsp_bitmask(graph, v, mask | (1 << v), memo, n)
                ans = min(ans, cost)
                
    memo[u][mask] = ans
    return ans
```

---

# 3.6 Solución a la Situación Problemática

<div class="solution-box">

### 🚚 Resultado para el Reparto de Paquetería ($N=20$)

* **Fuerza Bruta / Permutaciones ($O(N!)$):**
  $2.4 \times 10^{18}$ operaciones. Tomaría literalmente **miles de años** en un servidor convencional.
  
* **Programación Dinámica con Bitmasking ($O(2^N \cdot N^2)$):**
  Los estados posibles son $2^{20}$ (máscaras) multiplicados por $20$ (nodos actuales). Las transiciones toman $O(N)$.
  Total de operaciones: $2^{20} \times 20^2 \approx 4.19 \times 10^8$.
  Tiempo estimado de ejecución: **~0.2 a 0.5 segundos**.

**Conclusión:** La compresión del estado histórico mediante Máscaras de Bits transforma un problema intratable factorial en uno de tiempo exponencial controlable, permitiendo logística óptima en tiempo real para flotas pequeñas.
</div>

---

# 3.7 Árboles de Recubrimiento Mínimo (Algoritmo de Prim)
### (Tiempo Estimado: 1.0 Hora)

---

# 3.7 Situación Problemática: Redes Eléctricas

<div class="problem-box">

### ⚡ Electrificación Rural
El gobierno necesita conectar $V = 5,000$ comunidades rurales a la red eléctrica. Hay $E = 20,000$ posibles rutas para tirar los cables, cada una con un costo distinto (dependiendo del terreno y la distancia).

* **Condición 1:** Todas las comunidades deben estar conectadas entre sí (directa o indirectamente).
* **Condición 2:** Queremos gastar la **menor cantidad de dinero** (cable) posible en total.
* **Reflexión:** Si cerramos un ciclo (un anillo de cables), estamos gastando cable extra sin conectar a ninguna comunidad nueva. Por ende, la solución óptima **jamás tendrá ciclos**. Una red conectada sin ciclos es un **Árbol**.
* **Desafío:** ¿Cómo encontrar el Árbol de Recubrimiento de Costo Mínimo (MST) de forma eficiente?
</div>

---

# 3.7 Algoritmo de Prim: Expandiendo el Imperio

El Algoritmo de Prim (1930 / 1957) es un algoritmo **Avaro (Greedy)** que construye el Árbol Mínimo (MST) expandiendo un único componente conectado paso a paso.

### La Filosofía de Prim:
1. Empezar en un nodo cualquiera (ej. el nodo 0). Éste es ahora tu "Árbol en Construcción".
2. Mirar todas las aristas que conectan los nodos *dentro* de tu árbol con los nodos que aún están *fuera* de él.
3. Elegir la arista **más barata** y agregarla al árbol, incorporando al nuevo nodo.
4. Repetir hasta que todos los vértices estén dentro del árbol.

*¿Cómo encontramos la arista más barata rápidamente?* ¡Igual que en Dijkstra, usando una **Cola de Prioridad (Min-Heap)**!

---

# 3.7 Implementación de Prim en Python


```python
import heapq

def prim_mst(V, graph):
    # graph: diccionario de listas de adyacencia {u: [(v, peso), ...]}
    visited = [False] * V
    min_heap = [(0, 0)]  # (peso, nodo_destino)
    mst_cost = 0
    edges_used = 0
    
    while min_heap and edges_used < V:
        weight, u = heapq.heappop(min_heap)
        
        if visited[u]:
            continue
            
        visited[u] = True
        mst_cost += weight
        edges_used += 1  # Solo se cuenta al procesar un nodo por primera vez
        
        for v, w in graph[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (w, v))
                
    return mst_cost
```

---

# 3.7 Solución a la Situación Problemática

<div class="solution-box">

### ⚡ Resultado para la Red de Electrificación Rural

* **Enfoque de Fuerza Bruta:**
  Buscar todas las combinaciones de aristas que formen un árbol y elegir el más barato tomaría tiempo exponencial, imposible para $V = 5,000$.
* **Con Algoritmo de Prim ($O(E \log V)$):**
  1. Insertar y extraer nodos en el Min-Heap toma tiempo logarítmico.
  2. Al evaluar $20,000$ aristas, el tiempo de procesamiento es dominado por el heap: $\approx 20,000 \times \log_2(5,000) \approx 2.4 \times 10^5$ operaciones.
  Tiempo estimado de ejecución: **< 0.01 segundos**.

**Conclusión:** El algoritmo de Prim garantiza encontrar la red más económica (el Árbol de Recubrimiento Mínimo) de manera matemáticamente perfecta en una fracción de segundo, ahorrando millones en presupuesto de infraestructura.
</div>

---

# 3.8 Algoritmo de Kruskal y Conjuntos Disjuntos
### (Tiempo Estimado: 1.0 Hora)

---

# 3.8 Situación Problemática: Red Submarina

<div class="problem-box">

### 🌊 Conexión de Fibra Óptica entre Islas
Debes tender cables de fibra óptica submarina entre un archipiélago de $V = 100,000$ islas. Te han dado una lista con los costos de tender cable entre pares específicos de islas (las aristas, $E = 150,000$).

* **El Problema con Prim:** Prim crece un solo árbol desde un nodo central. Pero al planificar redes masivas diseminadas (como islas), es más natural ir conectando los pares de islas más cercanos sin importar en qué parte del mapa estén, hasta que todo se fusione.
* **El Riesgo del Ciclo:** Si conectas la Isla A con la B (que es barato), y luego intentas conectar la C con la A, debes estar absolutamente seguro de que C y A no estaban ya conectadas indirectamente. Si lo están, estarás creando un ciclo y desperdiciando cable carísimo.
* **Desafío:** ¿Cómo determinamos en tiempo $O(1)$ si dos vértices ya pertenecen a la misma red antes de conectarlos?
</div>

---

# 3.8 Filosofía de Kruskal y Union-Find

El Algoritmo de Kruskal (1956) tiene una lógica sorprendentemente sencilla:
1. **Ordenar** todas las aristas del grafo de menor a mayor peso.
2. Iterar sobre las aristas ordenadas. Si la arista conecta dos árboles distintos, agregarla al MST. Si conecta dos nodos que ya están en el mismo árbol, ignorarla.

### La Magia: Estructura Union-Find (Conjuntos Disjuntos)
Para detectar ciclos rápidamente, usamos un arreglo donde cada nodo apunta a su "padre" o "raíz" del componente.
* `Find(x)`: Sube por los padres hasta encontrar la raíz suprema de la red de `x`. Si `Find(A) == Find(B)`, ya están conectados. *(Se optimiza con Compresión de Caminos)*.
* `Union(A, B)`: Conecta la raíz de la red de A con la raíz de la red de B. *(Se optimiza con Unión por Rango)*.

---

# 3.8 Implementación de Kruskal en Python

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i):
        if self.parent[i] == i: return i
        # Path Compression: el nodo apunta directamente a la raíz
        self.parent[i] = self.find(self.parent[i]) 
        return self.parent[i]

    def union(self, i, j):
        root_i, root_j = self.find(i), self.find(j)
        if root_i != root_j: # Union by Rank
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
```

---

# 3.8 Código Principal y Complejidad


```python
def kruskal_mst(V, edges):
    # edges es una lista de tuplas: (peso, u, v)
    mst_cost = 0
    edges_used = 0
    uf = UnionFind(V)
    
    # 1. Ordenar aristas por peso: O(E log E)
    edges.sort() 
    
    # 2. Iterar e intentar unir: O(E * α(V))
    for weight, u, v in edges:
        if uf.find(u) != uf.find(v): # No forman ciclo
            uf.union(u, v)
            mst_cost += weight
            edges_used += 1
            if edges_used == V - 1:
                break # El MST está completo
                
    return mst_cost
```
**Complejidad General:** $O(E \log E)$ por la fase de ordenamiento. La función de Ackermann inversa $\alpha(V)$ del Union-Find hace que las operaciones de detección de ciclos sean prácticamente $O(1)$.

---

# 3.8 Solución a la Situación Problemática

<div class="solution-box">

### 🌊 Resultado para la Red de Fibra Óptica Submarina

* **Prim (Múltiples frentes simultáneos):**
  Lidiar con múltiples "frentes" y distancias inconexas en archipiélagos es computacionalmente incómodo de implementar y propenso a ineficiencias de memoria.
* **Algoritmo de Kruskal con Union-Find ($O(E \log E)$):**
  1. Ordenamos las $150,000$ posibles rutas de fibra óptica: $\approx 2.7 \times 10^6$ operaciones de ordenamiento.
  2. Procesamos secuencialmente usando `Find()` y `Union()`. Dado que la complejidad de Union-Find amortizada es $O(1)$, la fase de conexión toma en la práctica solo unas $150,000$ operaciones.
  Tiempo de ejecución: **< 0.1 segundos**.

**Conclusión:** Kruskal demuestra que el enfoque global de "ordenar aristas" combinado con la estructura de Conjuntos Disjuntos (Union-Find) es la forma más natural y elegante de integrar sistemas distribuidos geográficamente.
</div>

---

# 3.9 Árboles Binarios de Búsqueda Óptimos
### (Tiempo Estimado: 1.0 Hora)

---

# 3.9 Situación Problemática: Buscador por Frecuencia

<div class="problem-box">

### 📖 Diccionarios Pre-cargados Inteligentes
Construyes la estructura de datos interna de un motor de traducción. Tienes $N$ palabras clave en orden alfabético. Sabes exactamente qué tan probable es que el usuario busque cada palabra. Por ejemplo, "el" y "de" tienen un $40\%$ de probabilidad conjunta, mientras que "espectrofotometría" tiene un $0.0001\%$.

* **El Problema con AVL / Red-Black Trees:** Los árboles balanceados garantizan altura $O(\log N)$ estructural. Pero, ¿tiene sentido que la palabra "el" esté a profundidad 15 solo por balancear el árbol, mientras palabras raras están muy cerca de la raíz?
* **Desafío:** ¿Cómo construimos un Árbol Binario de Búsqueda (ABB) que minimice el **costo esperado de búsqueda**, acercando las palabras más frecuentes a la raíz sin violar el ordenamiento de búsqueda binaria?
</div>

---

# 3.9 Teoría: DP en Estructuras de Árboles

Este problema no se puede resolver con un algoritmo Avaro (poner siempre la más frecuente como raíz muchas veces aísla horriblemente al resto). Requerimos **Programación Dinámica**.

* **Subproblema:** Dado un rango de claves ordenadas desde $i$ hasta $j$, debemos elegir una clave $k$ ($i \le k \le j$) para que sea la **raíz de ese subárbol**.
* Al hacer a $k$ la raíz, las claves $i \dots k-1$ van al subárbol izquierdo, y $k+1 \dots j$ al derecho.
* **Costo (Transición):** Al unir los subárboles bajo la nueva raíz $k$, todos los nodos descienden un nivel de profundidad. Por lo tanto, el costo total suma el costo de los subárboles más la suma de frecuencias del rango:

$$C[i, j] = \min_{i \le k \le j} \Big( C[i, k-1] + C[k+1, j] \Big) + \sum_{m=i}^{j} \text{freq}[m]$$

---

# 3.9 Implementación del ABB Óptimo (O(N³))

```python
def optimal_bst(keys, freq):
    n = len(keys)
    # cost[i][j] almacena el costo mínimo del rango de claves i a j
    cost = [[0] * (n + 1) for _ in range(n + 1)]
    
    # Casos base: árboles de 1 solo elemento
    for i in range(n):
        cost[i][i] = freq[i]
        
    # L es la longitud de la cadena de claves a evaluar
    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            cost[i][j] = float('inf')
            
            # Precalcular suma de frecuencias en el rango [i, j]
            fsum = sum(freq[i:j+1])
            
            # Probar cada clave r como posible raíz
            for r in range(i, j + 1):
                c = fsum
                if r > i: c += cost[i][r - 1]
                if r < j: c += cost[r + 1][j]
                if c < cost[i][j]:
                    cost[i][j] = c
                    
    return cost[0][n - 1]
```

---

# 3.10 Coloreo de Grafos
### (Tiempo Estimado: 1.0 Hora)

---

# 3.10 Situación Problemática: Asignación de Frecuencias

<div class="problem-box">

### 📻 Redes de Telefonía Celular
Una compañía de telecomunicaciones debe asignar frecuencias de radio a $V = 1,000$ torres celulares. Si dos torres están lo suficientemente cerca como para que sus señales se solapen (hay una arista entre ellas), **no pueden transmitir en la misma frecuencia** o causarán interferencia.

* **El Costo:** El gobierno cobra millones de dólares por cada banda de frecuencia licenciada. Por lo tanto, el objetivo es utilizar la **mínima cantidad posible de frecuencias diferentes**.
* **Modelado:** Esto es un problema clásico de **Coloreo de Vértices**. Buscamos el "Número Cromático" $\chi(G)$, el mínimo de colores para pintar el grafo sin que dos nodos adyacentes compartan color.
* **Desafío:** Hallar el número cromático exacto es un problema **NP-Completo** (imposible de resolver rápido para grafos grandes). ¿Qué hacemos en la vida real?
</div>

---

# 3.10 Teoría: El Enfoque Heurístico (Avaro)

Ya que el cálculo exacto (usando Backtracking) tomaría un tiempo $O(m^V)$, la industria utiliza **Algoritmos Avaros (Greedy)** heurísticos. No garantizan usar el mínimo absoluto de colores, pero dan una solución excelente y válida en tiempo polinomial.

### Algoritmo de Coloreo Avaro Simple:
1. Asignar el "Color 0" al primer vértice.
2. Para cada uno de los vértices restantes:
   * Mirar los colores que ya han sido asignados a sus vecinos adyacentes.
   * Asignarle el **color disponible con el número más bajo** que no esté siendo usado por ningún vecino.

*Para mejorar este algoritmo (como en Welsh-Powell), conviene **ordenar primero los vértices de mayor a menor grado**, coloreando primero los nodos más problemáticos.*

---

# 3.10 Implementación: Coloreo Avaro en Python

```python
def greedy_coloring(V, adj):
    # result[i] guardará el color asignado al vértice i
    result = [-1] * V
    result[0] = 0 # Pintar el primer nodo con el color 0
    
    # Arreglo temporal para marcar colores no disponibles
    available = [True] * V 
    
    for u in range(1, V):
        # Marcar los colores de los vecinos como ocupados
        for i in adj[u]:
            if result[i] != -1:
                available[result[i]] = False
                
        # Encontrar el primer color disponible
        color = 0
        while color < V and not available[color]:
            color += 1
            
        result[u] = color # Asignar el color encontrado
        
        # Resetear el arreglo para la próxima iteración
        for i in adj[u]:
            if result[i] != -1:
                available[result[i]] = True
                
    return result, max(result) + 1 # Retorna arreglo y total de colores
```

---

# 3.10 Solución a la Situación Problemática

<div class="solution-box">

### 📻 Resultado para las Torres Celulares

* **Solución Exacta (Backtracking):**
  Asegura el mínimo absoluto de frecuencias, pero para $1,000$ torres conectadas aleatoriamente, el tiempo de cálculo supera la vida útil del universo.
* **Solución con Coloreo Avaro ($O(V^2)$ o $O(V + E)$):**
  Se procesan los nodos uno por uno. Solo requiere mirar a los vecinos inmediatos.
  Para $1,000$ torres y digamos $50,000$ posibles superposiciones, toma apenas **$\approx 50,000$ operaciones simples**.
  Tiempo estimado de ejecución: **< 0.05 segundos**.

**Conclusión:** En la ingeniería real, frente a problemas NP-Completos como el Coloreo, cambiamos la "perfección inalcanzable" por una "aproximación instantánea y altamente eficiente" usando técnicas Greedy.
</div>

---

# 3.11 Flujo Máximo en Redes (Redes de Flujo)
### (Tiempo Estimado: 2.5 Horas)

---

# 3.11 Situación Problemática: Cuellos de Botella

<div class="problem-box">

### 🚰 Suministro de Agua a la Metrópoli
Tienes un sistema de acueductos que transporta agua desde un gran embalse (El **Origen / Source**, $S$) hasta una ciudad metropolitana (El **Destino / Sink**, $T$). 
El agua viaja a través de varias estaciones de bombeo intermedias (Nodos) unidas por tuberías (Aristas). 

* **La Restricción:** Cada tubería tiene una capacidad máxima de transporte en litros por segundo (ej. un tubo estrecho soporta 10 L/s, uno grueso 50 L/s).
* **El Problema con Dijkstra:** Dijkstra encontraría el camino más corto, pero enviar toda el agua por un solo camino reventaría esa tubería. Queremos mandar agua por **todos los caminos posibles simultáneamente**.
* **Desafío:** ¿Cómo calculamos el **Flujo Máximo** absoluto que puede llegar a la ciudad, descubriendo exactamente qué tuberías forman el "cuello de botella" de todo el sistema?
</div>

---

# 3.11 Teoría: Red Residual y Ford-Fulkerson

El Algoritmo de **Ford-Fulkerson** (1956) no calcula flujos "de golpe", sino de manera iterativa buscando **Caminos de Aumento**.

### Conceptos Fundamentales:
1. **Red Residual:** Un grafo paralelo que muestra cuánta capacidad *adicional* queda en cada tubería y, crucialmente, permite "deshacer" flujo enviado previamente creando aristas virtuales en dirección contraria.
2. **Camino de Aumento:** Cualquier ruta desde $S$ hasta $T$ en la red residual donde todas las aristas tienen capacidad $> 0$.
3. **Cuello de Botella:** La capacidad mínima de las aristas a lo largo de un camino de aumento hallado.

**El Bucle:** Mientras exista un camino de aumento, empujamos el flujo equivalente al cuello de botella y actualizamos la red residual.

---

# 3.11 Implementación: Edmonds-Karp (BFS)

Usar BFS para hallar caminos de aumento (variante de Edmonds-Karp) garantiza eficiencia en tiempo $O(V \cdot E^2)$.

<pre><code class="language-python">from collections import deque

def bfs_path(C, F, source, sink, parent):
    visited = set([source])
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in range(len(C)):
            if v not in visited and C[u][v] - F[u][v] > 0:
                parent[v] = u
                visited.add(v)
                if v == sink: return True
                queue.append(v)
    return False

def max_flow(C, source, sink):
    n = len(C)
    F = [[0] * n for _ in range(n)] # Matriz de Flujos
    parent = [-1] * n
    total_flow = 0
    
    while bfs_path(C, F, source, sink, parent):
        path_flow = float('inf')
        s = sink
        while s != source: # Buscar el cuello de botella
            path_flow = min(path_flow, C[parent[s]][s] - F[parent[s]][s])
            s = parent[s]
            
        total_flow += path_flow
        v = sink
        while v != source: # Actualizar matriz residual
            u = parent[v]
            F[u][v] += path_flow
            F[v][u] -= path_flow # Arista de retroceso (deshacer)
            v = u
            
    return total_flow
</code></pre>

---

# 3.11 Solución a la Situación Problemática

<div class="solution-box">

### 🚰 Resultado para el Suministro de Agua

* **Intentos Avaros (Dijkstra):** Mandar agua por la "ruta más corta" saturaría una cañería de 10 L/s y dejaría las demás tuberías de 50 L/s vacías. El flujo total sería apenas 10 L/s.
* **Con Algoritmo de Flujo Máximo:**
  Evaluamos la red completa descubriendo cómo las corrientes se dividen y se vuelven a unir.
  Identificamos matemáticamente el **Corte Mínimo (Min-Cut)**: el conjunto de tuberías críticas que dictan el límite de todo el sistema. Si queremos más agua en la ciudad, el algoritmo nos dice *exactamente* cuáles 3 tuberías del acueducto debemos reemplazar por unas más grandes.

**Conclusión:** Ford-Fulkerson no solo maximiza el transporte de recursos en redes físicas o de datos, sino que es la herramienta definitiva para detectar vulnerabilidades en infraestructuras críticas.
</div>

---

# 3.12 Matriz Comparativa Final del Tema 3

| Problema | Algoritmo | Restricciones / Tipo de Grafo | Complejidad |
| :--- | :--- | :--- | :--- |
| **Búsqueda de Prefijos** | Trie | Cadenas de texto | $O(\|W\|)$ |
| **Rutas con Dependencias** | Orden Topológico | DAG (Sin ciclos) | $O(V + E)$ |
| **Ruta Más Corta** | Dijkstra | Pesos $\ge 0$ | $O(E \log V)$ |
| **Todos los Pares** | Floyd-Warshall | Pesos negativos permitidos | $O(V^3)$ |
| **Agente Viajero (TSP)** | DP + Bitmasking | Grafos densos $N \le 20$ | $O(2^N \cdot N^2)$ |
| **Árbol Mínimo (MST)** | Prim / Kruskal | Grafos Conexos Ponderados | $O(E \log V)$ |
| **Coloreo** | Coloreo Avaro | Aproximación Heurística | $O(V + E)$ |
| **Cuellos de Botella** | Ford-Fulkerson | Redes de Capacidades | $O(V \cdot E^2)$ |

---

# Conclusiones y Próximos Pasos

---

# Conclusiones y Preguntas de Repaso

### Conclusiones del Módulo:
1. **El modelado lo es todo:** Un problema logístico, un juego de sudoku o una red de servidores se pueden resolver con el mismo algoritmo si lo abstraes a Nodos y Aristas.
2. **Propiedades ocultas:** Identificar si el grafo es Acíclico (DAG) puede reducir el tiempo de cálculo de años a milisegundos usando Programación Dinámica.
3. **El estado histórico:** El uso de Bitmasking demuestra que podemos comprimir información compleja para domar la explosión combinatoria.

### Preguntas de Repaso:
1. ¿Por qué el algoritmo de Dijkstra falla matemáticamente cuando existen pesos negativos en el grafo?
2. Explica la utilidad de la función `Find()` con "Compresión de Caminos" en el algoritmo de Kruskal.
3. ¿Cómo usarías el Algoritmo de Flujo Máximo para determinar a qué jugadores emparejar en un torneo de ajedrez (Matching Bipartito)?
4. ¿Por qué un Árbol Binario de Búsqueda Óptimo (Gilbert-Moore) podría colocar un elemento en la raíz aunque no sea el de la "mitad" estricta del arreglo?

---

# ¡Gracias por su atención!

**Siguiente Clase:** Tema 4 - Geometría Computacional (Proximidad, Voronoi, y Cascos Convexos).