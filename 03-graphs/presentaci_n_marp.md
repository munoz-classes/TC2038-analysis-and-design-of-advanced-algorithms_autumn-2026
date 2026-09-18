## marp: true
theme: default
paginate: true
backgroundColor: #ffffff

# Estructuras de Datos Avanzadas

## Grafos y Tries

**Implementación, propiedades y análisis en memoria.**

# Objetivos de la Sesión

* Comprender la topología de red y sus componentes.

* Dominar las estructuras de representación en memoria (Matrices y Listas de Adyacencia).

* Implementar algoritmos de Grafos en Python.

* Entender y codificar la estructura del Árbol Trie.

# Índice de Contenidos

1. Concepto de Grafo

2. Propiedades y Representación en Memoria

3. Implementación de Grafos en Código

4. El Árbol Trie

5. Implementación de Tries en Código

# 1. Concepto de Grafo

# ¿Qué es un grafo?

Una red de conexiones. Modela relaciones complejas donde no existe una jerarquía estricta (a diferencia de los árboles tradicionales).

# Componentes Principales: Vértices

También conocidos como **nodos**. Son las entidades fundamentales que almacenan la información.

# Componentes Principales: Aristas

También conocidas como **enlaces** (edges). Son las conexiones tangibles que unen a los vértices.

# La Fórmula Fundamental

## G = (V, E)

Un Grafo (G) es un conjunto de Vértices (V) y un conjunto de Aristas (E - Edges).

# Tipos de Grafos: Dirigido

Las conexiones son unidireccionales. Si hay una arista de A hacia B, no implica que exista de B hacia A.

# Tipos de Grafos: No Dirigido

Las relaciones son simétricas o bidireccionales por defecto. Una conexión entre A y B se puede recorrer en ambos sentidos.

# Tipos de Grafos: Ponderado

Cada arista contiene un "peso". Este peso puede representar costo, distancia, tiempo o capacidad.

# Tipos de Grafos: No Ponderado

Todas las conexiones tienen un costo unitario idéntico. Solo importa si existe o no la conexión.

# Topología: Ciclos

Un ciclo es una ruta que comienza y termina en el mismo vértice, permitiendo recorrer un bucle infinito.

# Topología: Acíclicos

Redes estrictamente sin bucles ni retornos posibles. Una vez que se avanza, no se puede regresar al origen.

# DAG

**Directed Acyclic Graph** (Grafo Acíclico Dirigido).
Es la base algorítmica para la resolución de dependencias, como en los gestores de paquetes o sistemas de compilacióConcepto de Grafon.

# Aplicaciones Reales

* Redes sociales (amigos, seguidores).

* Sistemas GPS y mapas (rutas más cortas).

* Motores de recomendación.

* Topología de redes de computadoras.

# 2. Propiedades y Memoria

# El Desafío de la Memoria

¿Cómo almacenamos topologías irregulares e interconectadas en una memoria de computadora que es lineal?

# Matriz de Adyacencia

Una cuadrícula 2D (matriz cuadrada) que marca con un 1 la existencia de conexiones directas y con un 0 la ausencia de ellas.

# Matriz de Adyacencia: Visualización

|  | A | B | C | 
 | ----- | ----- | ----- | ----- | 
| A | 0 | 1 | 0 | 
| B | 1 | 0 | 1 | 
| C | 0 | 1 | 0 | 

# Complejidad Espacial de la Matriz

## $O(V^2)$

Complejidad cuadrática. Es muy costosa en redes grandes porque reserva memoria incluso para conexiones que no existen.

# Lista de Adyacencia

Un mapa, diccionario o arreglo donde cada vértice almacena únicamente una lista de sus vecinos directos.

# Lista de Adyacencia: Visualización

* **A** $\rightarrow$ \[B\]

* **B** $\rightarrow$ \[A, C\]

* **C** $\rightarrow$ \[B\]

# Complejidad Espacial de la Lista

## $O(V + E)$

Complejidad lineal. Altamente eficiente ya que solo ocupa memoria proporcional a las entidades y conexiones reales.

# ¿Cuándo usar Matriz?

**Grafos Densos:** Cuando casi todas las conexiones posibles entre vértices existen. Las operaciones de consulta son $O(1)$.

# ¿Cuándo usar Lista?

**Grafos Dispersos:** Cuando hay pocos enlaces por nodo (la mayoría de los casos reales). Ahorra cantidades masivas de memoria.

# 3. Grafos en Código

# Implementación: Estructura Base

```
class Grafo:
    def __init__(self):
        # Utilizamos un diccionario para la Lista de Adyacencia
        self.adyacencia = {}

```

# Implementación: Insertando Entidades

```
    def agregar_vertice(self, v):
        if v not in self.adyacencia:
            self.adyacencia[v] = []

```

# Implementación: Creando Enlaces

```
    def agregar_arista(self, origen, destino):
        # Grafo dirigido
        self.adyacencia[origen].append(destino)
        
        # Si fuera NO dirigido, agregamos también:
        # self.adyacencia[destino].append(origen)

```

# Recorridos de un Grafo

Algoritmos para visitar y explorar cada nodo del grafo sistemáticamente sin entrar en ciclos infinitos.

# BFS (Búsqueda en Anchura)

Exploración expansiva nivel por nivel. Ideal para encontrar la ruta más corta en grafos no ponderados.

# BFS: Implementación (Usando Cola)

```
from collections import deque

def bfs(grafo, inicio):
    visitados = set()
    cola = deque([inicio])
    
    while cola:
        nodo = cola.popleft()
        if nodo not in visitados:
            visitados.add(nodo)
            cola.extend(grafo[nodo])

```

# DFS (Búsqueda en Profundidad)

Exploración ramificada hasta el fondo. Avanza lo más lejos posible por una rama antes de retroceder (backtracking).

# DFS: Implementación (Recursividad/Pila)

```
def dfs(grafo, inicio, visitados=None):
    if visitados is None:
        visitados = set()
        
    visitados.add(inicio)
    
    for vecino in grafo[inicio]:
        if vecino not in visitados:
            dfs(grafo, vecino, visitados)
            
    return visitados

```

# 4. El Árbol Trie

# ¿Qué es un Trie?

También llamado *Prefix Tree* (Árbol de Prefijos).
Es un tipo especial de árbol n-ario optimizado específicamente para almacenar y buscar cadenas de texto (strings).

# Propiedad Fundamental

A diferencia de los árboles de búsqueda binaria, los nodos no almacenan la clave entera. Cada nodo representa **un único carácter o letra**.

# Rutas Compartidas

Las palabras que comparten un mismo prefijo comparten también los mismos nodos iniciales en la estructura de memoria.

*Ejemplo: "gato" y "ganar" comparten la 'g' y la 'a'.*

# Complejidad Temporal del Trie

## $O(L)$

La búsqueda es extremadamente veloz y solo depende de la longitud $L$ de la palabra que estamos buscando, independientemente de cuántos millones de palabras existan en el árbol.

# Casos de Uso Reales

* Autocompletado predictivo en buscadores.

* Correctores ortográficos.

* Enrutamiento de direcciones IP en redes.

* Juegos como Scrabble o Boggle.

# 5. Tries en Código

# El Nodo Trie

Cada nodo debe tener referencias a sus hijos y una bandera booleana para indicar si ahí termina una palabra válida.

```
class NodoTrie:
    def __init__(self):
        self.hijos = {} # Diccionario letra -> NodoTrie
        self.fin_palabra = False

```

# La Clase Trie

```
class Trie:
    def __init__(self):
        # La raíz siempre es un nodo vacío
        self.raiz = NodoTrie()

```

# Inserción de Palabras

```
    def insertar(self, palabra):
        nodo = self.raiz
        for char in palabra:
            if char not in nodo.hijos:
                nodo.hijos[char] = NodoTrie()
            nodo = nodo.hijos[char]
        
        # Marcamos el último nodo como fin de palabra
        nodo.fin_palabra = True

```

# Búsqueda de Palabras Exactas

```
    def buscar(self, palabra):
        nodo = self.raiz
        for char in palabra:
            if char not in nodo.hijos:
                return False
            nodo = nodo.hijos[char]
            
        return nodo.fin_palabra

```

# Búsqueda de Prefijos (Autocompletado)

```
    def empieza_con(self, prefijo):
        nodo = self.raiz
        for char in prefijo:
            if char not in nodo.hijos:
                return False
            nodo = nodo.hijos[char]
            
        return True # Si llegamos aquí, el prefijo existe

```

# Resumen Final

* **Grafos:** Flexibilidad total para modelar relaciones. Optimizados con listas de adyacencia.

* **Tries:** Estructura rígida pero inigualable en velocidad y memoria para manejar prefijos y diccionarios de texto.

# Preguntas y Respuestas

**¡Gracias por tu atención!**