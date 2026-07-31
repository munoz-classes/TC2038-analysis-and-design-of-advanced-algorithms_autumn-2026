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
## Tema 5: Técnicas de Búsqueda Avanzada y Heurísticas

**Profesor - Alison Muñoz Capote**
*Tecnológico de Monterrey*

---

# Mapa del Tema 5 y Objetivos

### Objetivos del Tema:
1. Comprender los límites matemáticos de la computación (Clases P vs NP).
2. Diseñar e implementar el algoritmo A* para búsqueda informada de rutas.
3. Analizar algoritmos de Búsqueda Local para optimización en espacios continuos o masivos.
4. Aplicar técnicas bioinspiradas (Algoritmos Genéticos) para aproximar soluciones intratables.

### Subtemas del Módulo:
* **5.1 Clases de Complejidad (P, NP, NP-Hard)**
* **5.2 Búsqueda Heurística (Algoritmo *)**
* **5.3 Búsqueda Local (Hill Climbing)**
* **5.4 Recocido Simulado (Simulated Annealing)**
* **5.5 Algoritmos Genéticos y Bioinspirados**

---

# Repaso Breve: El Muro de la Intratabilidad

A lo largo del curso aprendimos a domar la complejidad:
* Ordenar arreglos pasó de $O(N^2)$ a $O(N \log N)$.
* Buscar en grafos pasó de tiempo exponencial a $O(V+E)$ o $O(V^3)$.

**Sin embargo, existe un muro impenetrable:**
Existen miles de problemas industriales (Logística, Asignación de Horarios, Plegamiento de Proteínas) para los cuales el mejor algoritmo conocido sigue siendo **exponencial o factorial** ($O(2^N)$, $O(N!)$).
Para $N = 100$, un algoritmo $O(2^N)$ tomaría más tiempo en ejecutarse que la edad actual del universo entero. A estos problemas los llamamos **Intratables**.

---

# 5.1 Clases de Complejidad Computacional
### (P, NP, NP-Complete, NP-Hard)

---

# 5.1 Situación Problemática: El Premio del Millón

<div class="problem-box">

### 💰 La Criptografía y las Transacciones Bancarias
Los sistemas de seguridad de todo el mundo (RSA, cifrado bancario) se basan en un principio matemático: **Es fácil verificar una respuesta, pero es increíblemente difícil encontrarla**.
* **Ejemplo:** Si te doy los números primos $P=137$ y $Q=313$, multiplicarlos ($137 \times 313 = 42,881$) te toma 1 segundo. Pero si solo te doy el $42,881$ y te pido que encuentres sus factores primos, tomará mucho más tiempo.
* **El Problema:** La humanidad asume que *no existe* un atajo algorítmico rápido para factorizar números inmensos o resolver problemas como el Sudoku o el TSP en tiempo polinomial. 
* **Desafío:** ¿Qué pasaría si alguien demuestra matemáticamente que la "Búsqueda" puede ser tan rápida como la "Verificación"? (El problema P vs NP).
</div>

---

# 5.1 Teoría: El Zoológico de la Complejidad

Clasificamos los problemas según la velocidad de los algoritmos que los resuelven:

1. **Clase P (Polynomial):** Problemas que pueden ser **resueltos** en tiempo polinomial ($O(N), O(N^2), O(N^k)$). Ej: Ordenamiento, Dijkstra, KMP.
2. **Clase NP (Nondeterministic Polynomial):** Problemas para los cuales, si te doy una posible solución, puedes **verificar si es correcta** en tiempo polinomial. Ej: Si te doy un camino en el TSP, sumar sus aristas para ver si el costo es menor a $X$ toma tiempo lineal. *(Nota: Todo problema P es también NP).*
3. **NP-Complete:** Los problemas más difíciles dentro de NP. Si descubres un algoritmo polinomial para resolver UNO de ellos, podrías resolver **TODOS** los problemas NP del mundo rápidamente.
4. **NP-Hard:** Problemas que son al menos tan difíciles como los NP-Complete, pero que ni siquiera podemos verificar sus respuestas en tiempo polinomial.

---

# 5.1 Solución a la Situación Problemática

<div class="solution-box">

### 💰 Resultado del Enigma (P vs NP)

* **El Estado Actual:** Nadie ha podido probar si $P = NP$ o si $P \neq NP$. Sin embargo, la comunidad científica asume abrumadoramente que **$P \neq NP$**.
* **La Implicación Práctica:** Si aceptamos que los problemas NP-Hard (como optimizar rutas logísticas masivas o empaquetar cajas en contenedores 3D) *no tienen* algoritmos de solución exacta rápida, **debemos dejar de buscar la perfección**.
* **El Nuevo Paradigma:** Aquí nacen las **Heurísticas**. Estrategias que no nos garantizan la respuesta óptima matemática, pero nos dan una respuesta "suficientemente buena" (ej. 98% del óptimo) en fracciones de segundo. ¡Ese 2% de error es un precio que la industria está feliz de pagar!

</div>

---

# 5.2 Búsqueda Heurística (Algoritmo A*)
### (Tiempo Estimado: 2.5 Horas)

---

# 5.2 Situación Problemática: Movimiento de IA

<div class="problem-box">

### 🤖 Pathfinding en Videojuegos (StarCraft / Age of Empires)
Imagina un mapa de cuadrícula enorme de $1000 \times 1000$ celdas. Le ordenas a tu unidad militar moverse desde una esquina del mapa hasta la esquina opuesta. Hay montañas y ríos (obstáculos) en el medio.

* **El Problema con Dijkstra:** Dijkstra expande su búsqueda en todas direcciones por igual, como un círculo de agua en un estanque. Examinará miles de celdas en la dirección *equivocada* antes de llegar al objetivo. Es matemáticamente perfecto, pero computacionalmente lento para tiempo real (60 FPS).
* **Desafío:** ¿Podemos darle "intuición" al algoritmo para que expanda su búsqueda prioritariamente hacia donde "sabe" que está el destino, ignorando caminos que se alejan del objetivo?
</div>

---

# 5.2 Teoría: La Ecuación de A* (A-Star)

Creado en 1968, el algoritmo A* modifica a Dijkstra añadiendo una **Heurística**. 

En lugar de elegir el siguiente nodo $n$ basándose solo en la distancia recorrida desde el inicio, evalúa una función de costo combinada $f(n)$:

$$f(n) = g(n) + h(n)$$

* **$g(n)$ (Costo Real):** Distancia exacta recorrida desde el nodo de inicio hasta $n$.
* **$h(n)$ (Heurística):** Estimación o "suposición inteligente" del costo desde el nodo $n$ hasta el destino final. (Ej. Distancia en línea recta).

**La Regla de Oro (Admisibilidad):** Para que A* garantice encontrar la ruta más corta, la heurística $h(n)$ **nunca debe sobreestimar** la distancia real. Si exagera, podría saltarse caminos mejores.

---

# 5.2 Implementación de A* en Python

```python
import heapq

def a_star(graph, start, goal, h):
    # graph: {nodo: [(vecino, peso)]} | h: {nodo: valor_heuristico}
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    parent = {}
    
    while open_set:
        current_f, current = heapq.heappop(open_set)
        if current == goal: return reconstruct_path(parent, current)
            
        for neighbor, weight in graph[current]:
            tentative_g = g_score[current] + weight
            
            # Si encontramos un camino más rápido a este vecino
            if tentative_g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + h[neighbor]
                heapq.heappush(open_set, (f_score, neighbor))
                
    return None # No hay ruta
```

---

# 5.2 Solución a la Situación Problemática

<div class="solution-box">

### 🤖 Resultado para el Pathfinding de IA

* **Dijkstra ($f(n) = g(n)$):**
  Sin heurística, la IA explora celdas a la izquierda, arriba, y abajo, a pesar de que el destino está a la derecha. Para un mapa gigante, exploraría quizás $300,000$ celdas antes de hallar la meta.
* **Algoritmo A* con Heurística de Distancia Manhattan:**
  El componente $h(n)$ actúa como un "imán" que arrastra la búsqueda hacia el objetivo. 
  Solo explora celdas a los lados si encuentra un muro y se ve forzado a rodearlo. En el mismo mapa, podría explorar apenas $15,000$ celdas para encontrar *exactamente la misma ruta óptima*.
  
**Conclusión:** A* combina la infalibilidad de Dijkstra con la velocidad de la búsqueda orientada, siendo el algoritmo fundamental que mueve a todos los personajes en la historia de los videojuegos y el ruteo moderno.
</div>

---

# 5.3 Búsqueda Local (Hill Climbing)
### (Tiempo Estimado: 1.5 Horas)

---

# 5.3 Situación Problemática: Optimización Continua

<div class="problem-box">

### 📡 Diseño de Antenas de Telecomunicación
Eres un ingeniero de hardware. Debes diseñar la forma de una antena para maximizar la recepción de señal. Tienes 3 parámetros ajustables: *Longitud*, *Ángulo de inclinación* y *Curvatura*. 

* **El Problema con A*:** A* y Dijkstra requieren un "estado inicial" y un "estado final". ¡Pero aquí no conoces el estado final! No sabes cuáles son las medidas perfectas, solo puedes construir una antena simulada, medir su señal, y decir "esto captó 85 dB".
* **Infinitas Opciones:** Los parámetros son números continuos (ej. ángulo de 45.123°). Hay literalmente infinitas combinaciones posibles. La fuerza bruta es imposible.
* **Desafío:** ¿Cómo instruimos a la computadora para que encuentre la mejor combinación de medidas si no podemos explorar todas las opciones ni sabemos cuál es el límite de la perfección?
</div>

---

# 5.3 Teoría: La Metáfora del Alpinista

El algoritmo **Hill Climbing (Escalada de Colinas)** es una técnica de Búsqueda Local guiada puramente por una función heurística de evaluación.

**Imagina a un alpinista con los ojos vendados tratando de llegar a la cima de una montaña:**
1. **Estado Inicial:** Genera una solución aleatoria (Aterriza en un punto de la montaña).
2. **Generación de Vecinos:** Da un paso pequeño en todas las direcciones posibles (Modifica ligeramente los parámetros de la antena).
3. **Evaluación:** Siente con sus pies qué dirección sube más.
4. **Transición:** Si una dirección sube, se mueve hacia allá.
5. **Condición de Parada:** Si todos los pasos posibles van hacia abajo, asume que ha llegado a la cima y se detiene.

---

# 5.3 El Peligro Matemático: Óptimos Locales

La mayor debilidad de Hill Climbing es que es "miope". Solo mira a sus vecinos inmediatos.

* **Óptimo Global:** El pico más alto de toda la cordillera (Monte Everest). ¡La solución que realmente queremos!
* **Óptimo Local:** Una pequeña colina. Si el alpinista ciego llega a la cima de esta colinita, sentirá que todas las direcciones bajan y se detendrá, creyendo que ganó, sin saber que el Everest estaba a solo 2 kilómetros de distancia.
* **Meseta (Plateau):** Una zona plana donde todos los vecinos tienen el mismo valor. El alpinista no sabe hacia dónde caminar y se queda vagando sin rumbo.

*Nota: Para mitigar esto, en la industria se usa **Random-Restart Hill Climbing** (lanzar al alpinista desde 100 lugares distintos del mapa y quedarse con la mejor cima).*

---

# 5.3 Implementación de Hill Climbing en Python

```python
import random

def hill_climbing(objective_function, get_neighbors, initial_state):
    # objective_function: retorna el "puntaje" de un estado (mayor es mejor)
    current_state = initial_state
    current_score = objective_function(current_state)
    
    while True:
        neighbors = get_neighbors(current_state)
        best_neighbor = None
        best_score = float('-inf')
        
        # Evaluar a todos los vecinos inmediatos
        for neighbor in neighbors:
            score = objective_function(neighbor)
            if score > best_score:
                best_neighbor = neighbor
                best_score = score
                
        # Si ningún vecino es mejor que mi estado actual, ¡llegué a la cima!
        if best_score <= current_score:
            return current_state, current_score
            
        # Dar el paso hacia arriba
        current_state = best_neighbor
        current_score = best_score
```

---

# 5.3 Solución a la Situación Problemática

<div class="solution-box">

### 📡 Resultado para el Diseño de Antenas

* **Fuerza Bruta Continua:**
  Evaluar cada milímetro y cada grado decimal requeriría $10^{20}$ simulaciones físicas, tardando milenios.
* **Algoritmo de Hill Climbing:**
  1. Creamos una antena aleatoria (ej. 10cm, 90°). Señal: 40dB.
  2. La computadora varía los valores en $+1$ y $-1$.
  3. Descubre que aumentar el ángulo a 91° sube la señal a 42dB. Sigue subiendo por ese camino.
  4. En menos de **1000 iteraciones** ($\approx 0.1$ segundos), el algoritmo se atasca en una cima local que otorga 89dB de señal.
  
**Conclusión:** Hill Climbing es increíblemente eficiente en memoria ($O(1)$, ya que solo recuerda el estado actual), permitiendo optimizar parámetros en la vida real. Sin embargo, su vulnerabilidad a los Óptimos Locales nos obliga a buscar un algoritmo más "valiente".
</div>

---

# 5.4 Recocido Simulado (Simulated Annealing)
### (Tiempo Estimado: 1.5 Horas)

---

# 5.4 Situación Problemática: Circuitos VLSI

<div class="problem-box">

### 💻 Diseño de Microprocesadores (VLSI)
Estás diseñando la placa base de un teléfono móvil. Tienes millones de transistores y componentes que deben ubicarse de tal forma que la longitud total de los cables de cobre sea la mínima posible (para reducir el calor y el retardo de señal).

* **El Problema con Hill Climbing:** Si usas Hill Climbing puro, el algoritmo moverá los componentes mejorando el diseño rápidamente, pero pronto se atascará en un "Óptimo Local" (una configuración mediocre donde cualquier pequeño cambio empeora las cosas a corto plazo).
* **El Sacrificio:** A veces, para organizar bien tu habitación, primero tienes que desordenarla un poco más. Hill Climbing se niega rotundamente a aceptar movimientos que "empeoren" la situación actual.
* **Desafío:** ¿Cómo le enseñamos a la computadora a "aceptar" temporalmente movimientos malos, con la esperanza de que la lleven a un valle mucho más profundo (óptimo global) más adelante?
</div>

---

# 5.4 Teoría: La Metáfora de la Metalurgia

En la metalurgia, para crear una espada fuerte, se calienta el acero a temperaturas extremas (los átomos se mueven caóticamente) y luego se **enfría muy lentamente** (los átomos se asientan en la estructura cristalina más fuerte y estable posible).

El **Recocido Simulado** (Kirkpatrick, 1983) imita este proceso:
1. **Alta Temperatura Inicial:** Al principio, el algoritmo tiene mucha "energía térmica". Si un paso empeora la solución, ¡lo acepta de todos modos con alta probabilidad! Esto le permite saltar fuera de los Óptimos Locales.
2. **Enfriamiento Gradual (Cooling Schedule):** Con cada iteración, la "temperatura" disminuye. 
3. **Baja Temperatura Final:** Al final, cuando la temperatura es casi cero, ya no acepta movimientos malos y se comporta exactamente igual que el estricto Hill Climbing.

---

# 5.4 Teoría: La Ecuación de Probabilidad

¿Con qué probabilidad aceptamos un movimiento que **empeora** la solución?
Utilizamos la distribución de Boltzmann de la termodinámica:

$$P(\text{aceptar}) = e^{\frac{-\Delta E}{T}}$$

* **$\Delta E$ (Diferencia de Energía):** Qué tan malo es el nuevo movimiento comparado con el actual. (Si es terriblemente malo, $\Delta E$ es grande, y la probabilidad baja).
* **$T$ (Temperatura):** Si $T$ es enorme, la fracción se acerca a cero, y $e^0 = 1$ (100% de probabilidad de aceptarlo). Si $T$ es pequeño, la probabilidad cae a casi 0%.

---

# 5.4 Implementación: Recocido Simulado


```python
import math
import random

def simulated_annealing(obj_func, get_neighbor, initial_state, temp, cooling_rate):
    current_state = initial_state
    current_score = obj_func(current_state)
    best_state, best_score = current_state, current_score
    
    while temp > 1:
        neighbor = get_neighbor(current_state)
        neighbor_score = obj_func(neighbor)
        
        # Diferencia (si es positivo, el vecino es mejor)
        delta_e = neighbor_score - current_score
        
        # Aceptar si es mejor, o aceptar con probabilidad P si es peor
        if delta_e > 0 or random.random() < math.exp(delta_e / temp):
            current_state = neighbor
            current_score = neighbor_score
            
            # Guardar el mejor histórico absoluto
            if current_score > best_score:
                best_state, best_score = current_state, current_score
                
        # Enfriar el sistema
        temp *= cooling_rate # ej. cooling_rate = 0.99
        
    return best_state, best_score
```

---

# 5.4 Solución a la Situación Problemática

<div class="solution-box">

### 💻 Resultado para el Diseño de Circuitos VLSI

* **Evaluación con Hill Climbing (Alpinista ciego):**
  Acomodaba los transistores hasta lograr reducir la longitud total de cable a $50$ metros, pero quedaba atrapado en una configuración local y no podía mejorar más.
* **Con Recocido Simulado:**
  Durante las primeras iteraciones (Temperatura Alta), la computadora desordenaba agresivamente el circuito, empeorando el cableado a $80$ metros. Pero esto le permitió escapar de la "trampa". Al enfriarse, convergió en una configuración globalmente armónica, logrando reducir la longitud total a **$12$ metros**.

**Conclusión:** Simular el ruido térmico de la física dota a nuestros algoritmos de la "valentía" necesaria para explorar el mapa completo, convirtiendo al Recocido Simulado en el estándar de oro para el diseño de hardware industrial.
</div>

---

# 5.5 Algoritmos Genéticos y Bioinspirados
### (Tiempo Estimado: 2.0 Horas)

---

# 5.5 Situación Problemática: Horarios Universitarios

<div class="problem-box">

### 🏫 El Problema del Timetabling (Asignación de Horarios)
Eres el director académico del Tec. Tienes que crear el horario para $10,000$ alumnos, $500$ profesores y $200$ aulas. 

* **Restricciones Duras:** Un profesor no puede dar dos clases al mismo tiempo. Dos clases no pueden usar la misma aula a la misma hora. Un alumno no puede tener empalmes.
* **Restricciones Suaves:** Los profesores prefieren no tener "huecos" de 4 horas entre clases.
* **La Complejidad:** Es un problema **NP-Hard** masivo. Hay más combinaciones de horarios posibles que átomos en el universo. Ningún algoritmo matemático exacto terminará jamás.
* **Desafío:** ¿Cómo logramos que la computadora nos entregue un horario "excelente" (sin choques y con pocas quejas) de forma totalmente automatizada en un par de minutos?
</div>

---

# 5.5 Teoría: Evolución por Selección Natural

En los años 70, John Holland propuso imitar la teoría de Darwin. En lugar de tener "una" solución mutando (como en el Recocido Simulado), tendremos una **población completa de soluciones** que se reproducen entre sí.

### Conceptos Clave:
1. **Individuo (Cromosoma):** Un horario completo propuesto (probablemente lleno de errores al principio).
2. **Función de Aptitud (Fitness):** Una función que califica al horario. (Ej. Empieza con 1000 puntos, pero le restamos 50 pts por cada maestro cruzado, y 10 pts por cada aula sobreocupada).
3. **Selección:** Los horarios con mayor puntaje (los "más aptos") tienen mayor probabilidad de ser elegidos para reproducirse.
4. **Cruzamiento (Crossover):** Tomar la mitad de un buen horario A y la mitad de un buen horario B para crear un horario "Hijo" C.
5. **Mutación:** Cambiar al azar una clase de salón para introducir diversidad.

---

# 5.5 Implementación: El Ciclo Genético en Python

```python
import random

def genetic_algorithm(population, fitness_fn, generations, mutation_rate):
    for _ in range(generations):
        # 1. Evaluar a toda la población
        population = sorted(population, key=fitness_fn, reverse=True)
        
        # Condición de victoria temprana
        if fitness_fn(population[0]) == PUNTAJE_PERFECTO: break
            
        new_generation = []
        # Conservar a la "Élite" (los mejores de la generación anterior)
        new_generation.extend(population[:ELITISM_COUNT])
        
        while len(new_generation) < len(population):
            # 2. Selección por Ruleta o Torneo
            parent1 = select_parent(population, fitness_fn)
            parent2 = select_parent(population, fitness_fn)
            
            # 3. Cruzamiento (Crossover)
            child = crossover(parent1, parent2)
            
            # 4. Mutación
            if random.random() < mutation_rate:
                child = mutate(child)
                
            new_generation.append(child)
            
        population = new_generation
        
    return max(population, key=fitness_fn) # Retornar el mejor individuo final
```

---

# 5.5 Solución a la Situación Problemática

<div class="solution-box">

### 🏫 Resultado para los Horarios Universitarios

* **Enfoques Avaros (Greedy):** Asignar clases una por una hasta que te quedes atascado. Genera horarios inusables donde el 30% de los alumnos se quedan sin aulas.
* **Algoritmos Genéticos:**
  Creamos $100$ horarios generados al azar. La función de Fitness los califica. Destruimos los $50$ peores y cruzamos a los $50$ mejores. 
  Al principio, el mejor horario tiene 4,000 empalmes. Tras $500$ generaciones evolutivas (que toman $\approx 3$ minutos de CPU), las "buenas combinaciones" de clases sobreviven y se heredan, mientras que la mutación arregla los bloqueos.
  
**Conclusión:** Terminamos con un horario donde los choques llegaron a **cero**. Aprovechamos milenios de sabiduría biológica para resolver en minutos los problemas logísticos y de diseño más formidables de la humanidad.
</div>

---

# 5.6 Matriz Comparativa Final del Tema 5

| Algoritmo | Tipo de Problema | Filosofía Principal | Garantía de Óptimo |
| :--- | :--- | :--- | :--- |
| **Dijkstra** | Rutas / Grafos | Expansión ciega y segura | **Sí** (Matemático) |
| **A* (A-Star)** | Pathfinding IA | Expansión guiada por un "imán" (Heurística) | **Sí** (Si $H$ es admisible) |
| **Hill Climbing** | Optimización Continua | Subir ciegamente buscando una cima | **No** (Atrapado en Óptimo Local) |
| **Recocido Simulado** | Asignación / Disposición | Empeorar para luego mejorar (Física) | **Alta probabilidad** (Si se enfría lento) |
| **Algoritmo Genético**| Problemas NP-Hard | Evolución colectiva, mutación y herencia | **No** (Aproximación excelente) |

---

# Conclusiones y Próximos Pasos

---

# Conclusiones y Preguntas de Repaso

### Conclusiones de la Asignatura (TC2038):
1. **La Elegancia del Tiempo y el Espacio:** Empezamos midiendo $O(N)$ y terminamos domando $O(N!)$. La ingeniería de software no trata sobre escribir código rápido, sino sobre **evitar el código innecesario**.
2. **El Arte de Rendirse (A Tiempo):** Entender que un problema es *NP-Hard* separa al programador novato del Ingeniero Experto. Saber cuándo abandonar la perfección matemática a cambio de una heurística es una decisión crítica de diseño.
3. **Inspiración Universal:** Los mejores algoritmos de la humanidad no nacieron en un teclado; fueron robados de las hormigas, la metalurgia, la genética y la física cuántica.

### Preguntas de Cierre:
1. Si creas una Heurística $h(n)$ para A* que a veces estima una distancia mayor a la real, ¿qué le pasará al camino resultante?
2. ¿Por qué el Recocido Simulado es superior a Hill Climbing en mapas de optimización "montañosos"?
3. En los Algoritmos Genéticos, ¿cuál es el peligro de tener una tasa de Mutación del 0%? ¿Y del 100%?

---

# ¡Gracias por su esfuerzo y dedicación!

**Fin del Curso TC2038**
*Análisis y Diseño de Algoritmos Avanzados*
