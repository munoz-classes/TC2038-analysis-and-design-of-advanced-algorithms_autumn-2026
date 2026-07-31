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
## Tema 2: Manejo de Strings (9 Horas)

**Profesor - Alison Muñoz Capote**
*Tecnológico de Monterrey*

---

# Mapa del Tema 2 y Objetivos

### Objetivos del Tema:
1. Comprender la teoría de búsqueda de patrones exacta en textos largos.
2. Analizar estructuras de datos avanzadas para representar sufijos.
3. Implementar algoritmos lineales y sublineales para evitar la fuerza bruta en el procesamiento de cadenas.
4. Conocer las aplicaciones reales en bioinformática, compresión y ciberseguridad.

### Distribución de Contenido (9 horas lectivas):
* **2.1 Algoritmo KMP** (1.5 hrs)
* **2.2 Z Function** (1.0 hr)
* **2.3 Algoritmo de Manacher** (1.5 hrs)
* **2.4 Hashing de Strings (Rabin-Karp)** (1.0 hr)
* **2.5 Suffix Arrays** (2.5 hrs)
* **2.6 Longest Common Substring** (1.5 hrs)

---

# Repaso Breve: Terminología de Cadenas (Strings)

Antes de empezar, estandaricemos nuestro vocabulario matemático para una cadena $S$ de longitud $N$:

* **Alfabeto ($\Sigma$):** Conjunto finito de caracteres válidos (ej. ASCII, $\{A, C, G, T\}$).
* **Prefijo:** Una subcadena que comienza en el índice 0 y termina en algún índice $i \le N-1$.
* **Sufijo:** Una subcadena que termina en el índice $N-1$ y comienza en algún índice $i \ge 0$.
* **Substring (Subcadena):** Una secuencia *contigua* de caracteres dentro de $S$.
* **Subsequence (Subsecuencia):** Secuencia *no necesariamente contigua* obtenida eliminando caracteres de $S$, manteniendo el orden.
* **Palíndromo:** Cadena que se lee igual de izquierda a derecha que de derecha a izquierda.

---

# 2.1 Algoritmo Knuth-Morris-Pratt (KMP)
### (Tiempo Estimado: 1.5 Horas)

---

# 2.1 Situación Problemática: Búsqueda en Genomas

<div class="problem-box">

### 🧬 El Desafío de la Bioinformática Computacional
Tenemos la secuencia de ADN de un cromosoma humano (Texto $T$ de longitud $N \approx 250,000,000$ bases nitrogenadas). Queremos encontrar todas las apariciones de un gen específico o marcador de enfermedad (Patrón $P$ de longitud $M = 10,000$).

* **Enfoque de Fuerza Bruta:** Comparar el patrón $P$ en cada posición posible de $T$.
  $$\text{Peor de los casos} = O(N \times M) \approx 2.5 \times 10^{12} \text{ comparaciones.}$$
* **El Problema del Re-cálculo:** Si los primeros 9,999 caracteres coinciden pero el último falla, la fuerza bruta retrocede el puntero del texto casi 10,000 posiciones y vuelve a empezar.
* **Desafío:** ¿Podemos encontrar todas las coincidencias en un tiempo lineal $O(N + M)$ mirando cada carácter del genoma **una sola vez**?
</div>

---

# 2.1 La Ineficiencia de la Fuerza Bruta

Analicemos por qué la búsqueda ingenua es lenta:

Texto $T$: `A A A A A A A A A B`
Patrón $P$: `A A A A B`

1. Comparamos en el índice 0. Coinciden 4 'A', pero falla en 'B'.
2. **Fuerza bruta:** Avanzamos el patrón una posición a la derecha. Volvemos a comparar desde el índice 1 del texto.

*¡Pero nosotros ya sabíamos que esos caracteres eran 'A'!*
La fuerza bruta "olvida" la información que acaba de descubrir. Necesitamos un algoritmo que tenga **memoria** sobre el patrón mismo.

---

# 2.1 La Solución: El Arreglo LPS (Patrón sobre sí mismo)

La genialidad de Donald Knuth, Vaughan Pratt y James H. Morris se basa en preprocesar el patrón $P$ para identificar sus simetrías internas antes de buscarlo en $T$.

### El Arreglo LPS (Longest Proper Prefix which is also Suffix)
Para cada posición $i$ en el patrón, calculamos la longitud del **prefijo propio más largo que también es un sufijo** de la subcadena $P[0..i]$.

**Ejemplo para el patrón $P =$ `A B A B A C A`**

| Índice $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Caracter** | A | B | A | B | A | C | A |
| **LPS[$i$]** | 0 | 0 | 1 | 2 | 3 | 0 | 1 |

* *Explicación $i=4$ (`ABABA`):* El prefijo `ABA` (longitud 3) es igual al sufijo `ABA`. Por lo tanto, LPS[4] = 3.

---

# 2.1 ¿Cómo usa KMP el Arreglo LPS?

Cuando ocurre un desajuste (mismatch) entre el Texto $T[i]$ y el Patrón $P[j]$:

* **En Fuerza Bruta:** Retrocedemos $i$ al inicio y $j = 0$.
* **En KMP:** El índice $i$ en el texto **nunca retrocede**. Solo actualizamos el índice $j$ del patrón consultando nuestra "memoria":
  $$j = LPS[j - 1]$$

Esto significa: *"Ya que los caracteres anteriores coincidían, no empieces desde cero. Desplaza el patrón para alinear el prefijo más largo que ya sabemos que coincide con el sufijo que acabamos de leer."*

---

# 2.1 Implementación del KMP en Python

```python
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0  # longitud del prefijo-sufijo actual
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1] # Retroceso inteligente
            else:
                lps[i] = 0
                i += 1
    return lps
```

---

# 2.1 El Bucle de Búsqueda Principal (KMP Search)

```python
def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    i = j = 0  # i para text, j para pattern
    matches = []
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1; j += 1
            
        if j == m:
            matches.append(i - j)  # ¡Patrón encontrado!
            j = lps[j - 1]         # Buscar la siguiente ocurrencia
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]     # Uso del LPS para no retroceder 'i'
            else:
                i += 1
    return matches
```

---

# 2.1 Solución a la Situación Problemática

<div class="solution-box">

### 🧬 Resultado para la Búsqueda en Genomas

* **Enfoque de Fuerza Bruta:**
  Complejidad $O(N \times M)$.
  Para $N = 250,000,000$ y $M = 10,000 \implies \approx 2.5 \times 10^{12}$ operaciones.
  Tiempo estimado: **~40 a 60 minutos** por cromosoma.

* **Con Algoritmo KMP:**
  1. Preprocesar Patrón (LPS): $O(M) \implies 10,000$ operaciones.
  2. Búsqueda en Texto (KMP): $O(N) \implies 250,000,000$ operaciones.
  Complejidad Total: $O(N + M) \implies \approx 2.5 \times 10^8$ operaciones.
  Tiempo de ejecución: **~0.2 a 0.5 segundos**.

**Conclusión:** KMP elimina el recálculo, reduciendo el tiempo de una hora a fracciones de segundo, haciendo viable la bioinformática a gran escala.
</div>

---

# 2.2 Z Function
### (Tiempo Estimado: 1.0 Hora)

---

# 2.2 Situación Problemática: Detección de Plagio

<div class="problem-box">

### 📝 El Desafío de Búsqueda de Patrones Simultánea
Imagina que trabajas en un sistema de detección de plagio. Tienes un documento sospechoso $T$ (Texto) y quieres saber cuántas veces y en qué posiciones aparece una frase exacta $P$ (Patrón).

* **El Enfoque KMP:** Funciona excelente, pero requiere construir una tabla separada para el patrón y luego iterar sobre el texto manejando dos punteros distintos con una lógica de retroceso asimétrica.
* **Desafío:** ¿Existe alguna forma de evaluar el texto y el patrón al mismo tiempo, utilizando **un solo arreglo** y una lógica más directa basada simplemente en prefijos? 
* **Idea:** ¿Qué pasaría si concatenamos el Patrón y el Texto separándolos con un símbolo especial? $S = P + \text{"\$"} + T$.
</div>

---

# 2.2 ¿Qué es la Z-Function?

La **Z-Function** (o Z-Array) es un arreglo $Z$ donde cada posición $Z[i]$ almacena la **longitud de la subcadena más larga que comienza en $S[i]$ y que también es un prefijo de $S$**.

### Ejemplo para $S =$ `a b a c a b a`

| Índice $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Caracter** | a | b | a | c | a | b | a |
| **$Z[i]$** | 0 | 0 | 1 | 0 | 3 | 0 | 1 |

* *Explicación $i=4$ (`aba`):* La subcadena que empieza en el índice 4 es `aba`. El prefijo de toda la cadena $S$ también es `aba`. Al coincidir 3 caracteres, $Z[4] = 3$.

---

# 2.2 Optimización con la "Z-Box"

Calcular el arreglo $Z$ con fuerza bruta tomaría $O(N^2)$. Para hacerlo en $O(N)$, mantenemos un intervalo $[L, R]$ (la **Z-Box**) que representa el bloque de coincidencia más a la derecha encontrado hasta ahora.

### Lógica de Optimización:
Al calcular $Z[i]$:
1. **Si $i > R$:** No hay información previa útil. Comparamos los caracteres uno por uno usando fuerza bruta y actualizamos $[L, R]$.
2. **Si $i \le R$:** ¡Estamos dentro de una Z-Box! Podemos usar los valores $Z$ ya calculados. Específicamente, el valor inicial de $Z[i]$ será al menos:
   $$Z[i] = \min(R - i + 1, Z[i - L])$$
   A partir de ahí, solo comprobamos si podemos extender la coincidencia más allá de $R$.

---

# 2.2 Implementación de Z-Function en Python

```python
def compute_z_function(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    
    for i in range(1, n):
        if i <= r:
            # Usar información previamente calculada (Z-Box)
            z[i] = min(r - i + 1, z[i - l])
            
        # Intentar extender la coincidencia por fuerza bruta
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
            
        # Actualizar la Z-Box si llegamos más lejos que R
        if i + z[i] - 1 > r:
            l = i
            r = i + z[i] - 1
            
    return z
```

---

# 2.2 Solución a la Situación Problemática

<div class="solution-box">

### 📝 Resultado para el Sistema de Plagio

Construimos una nueva cadena: $S = P + \text{"\$"} + T$.
(El caracter `$` garantiza que los valores $Z$ nunca excedan la longitud de $P$).

1. Concatenamos: $S = \text{"FRASE}\text{\$}\text{TEXTO-MUY-LARGO-DONDE-ESTA-LA-FRASE"}$.
2. Calculamos el arreglo $Z$ para $S$ en tiempo $O(|P| + |T|)$.
3. Iteramos sobre el arreglo $Z$: **Si encontramos algún $Z[i] == |P|$**, significa que exactamente en esa posición comienza una copia idéntica del patrón.

**Conclusión:** Z-Function resuelve la búsqueda de patrones con una lógica más intuitiva que KMP, logrando el mismo tiempo lineal $O(N)$ mediante la técnica de concatenación y el reuso inteligente de prefijos.
</div>

---

# 2.3 Algoritmo de Manacher
### (Tiempo Estimado: 1.5 Horas)

---

# 2.3 Situación Problemática: Procesamiento de Señales

<div class="problem-box">

### 📡 Detección de Palíndromos en Cadenas de ADN o Señales
Imagina que estás analizando una larga secuencia de caracteres (o señales bidireccionales) y necesitas aislar la **subcadena palindrómica más larga** dentro de un texto de tamaño $N = 100,000$.

* **Fuerza Bruta Ingenua:** Probar cada par de índices $(i, j)$ y verificar si es palíndromo: $O(N^3)$.
* **Expansión desde el centro:** Hay $2N - 1$ centros posibles (letras y los espacios entre ellas). Expandir cada uno toma $O(N)$. Tiempo total: $O(N^2)$.
* **El Problema:** Para $N = 100,000$, $O(N^2)$ implica $\approx 10^{10}$ operaciones en el peor caso (ej. un texto formado solo por letras 'A').
* **Desafío:** ¿Podemos encontrar el palíndromo más largo en tiempo lineal $O(N)$ sin explorar áreas que ya sabemos que son simétricas?
</div>

---

# 2.3 El Truco Inicial: Unificar Longitudes

Un palíndromo puede ser de longitud **impar** (`"aba"`, centro exacto en 'b') o **par** (`"abba"`, centro imaginario entre las 'b'). Para evitar manejar ambos casos con lógica separada en el código, Manacher transforma la cadena.

### La Transformación:
Insertamos un caracter especial (ej. `#`) al principio, al final y entre cada letra. Además, ponemos limitadores únicos en los extremos (`^` y `$`) para evitar comprobaciones de desbordamiento de índice.

* **Original:** $S =$ `"abba"`
* **Transformada:** $T =$ `"^#a#b#b#a#$"`

Ahora, **todos** los palíndromos en $T$ tienen longitud impar y un centro bien definido en un índice específico del arreglo.

---

# 2.3 El Arreglo $P$ y la Magia de la Simetría

Manacher construye un arreglo $P$, donde $P[i]$ almacena el **radio** del palíndromo más largo centrado en $T[i]$.

### Reuso por Espejeo (Symmetry):
Mantenemos registro del palíndromo que ha llegado más a la derecha, recordando su centro $C$ y su borde derecho $R$.
Si estamos evaluando un índice $i$ que está dentro de ese borde ($i < R$):
1. Calculamos la posición "espejo" de $i$ con respecto al centro $C$: $i' = 2C - i$.
2. Como el lado derecho es un reflejo exacto del izquierdo, $P[i]$ será al menos igual a $P[i']$.
3. ¡Pero cuidado! No podemos garantizar la simetría más allá del borde $R$. Por tanto:
   $$P[i] = \min(R - i, P[i'])$$

---

# 2.3 Algoritmo de Manacher: Paso a Paso

El núcleo del algoritmo fluye así:

1. Transformar la cadena original $S$ a la cadena unificada $T$.
2. Inicializar arreglo $P$ con ceros. Iniciar Centro $C = 0$ y Borde Derecho $R = 0$.
3. Iterar cada índice $i$ de 1 a $|T|-2$:
   * **Espejo inicial:** Si $i < R$, hacer $P[i] = \min(R - i, P[2C - i])$.
   * **Expansión manual:** Intentar expandir el palíndromo centrado en $i$ carácter por carácter hacia la izquierda y derecha.
   * **Actualización del Borde:** Si el palíndromo expandido supera el borde derecho $R$, se actualiza el nuevo "monarca" de la simetría: $C = i$ y $R = i + P[i]$.
4. El valor máximo en el arreglo $P$ nos da la longitud del palíndromo más largo.

---

# 2.3 Implementación de Manacher en Python

```python
def manacher(s):
    if not s: return ""
    # 1. Transformación
    T = "^#" + "#".join(s) + "#$"
    n = len(T)
    P = [0] * n
    C = R = 0
    
    # 2. Bucle Principal
    for i in range(1, n - 1):
        if i < R:
            P[i] = min(R - i, P[2 * C - i])
        # Expandir
        while T[i + 1 + P[i]] == T[i - 1 - P[i]]:
            P[i] += 1
        # Actualizar C y R
        if i + P[i] > R:
            C, R = i, i + P[i]
            
    # 3. Extraer el palíndromo máximo
    max_len, center_idx = max((val, idx) for idx, val in enumerate(P))
    start = (center_idx - max_len) // 2
    return s[start: start + max_len]
```

---

# 2.3 Solución a la Situación Problemática

<div class="solution-box">

### 📡 Resultado para la Búsqueda de Señales Simétricas

* **Expansión Tradicional Centro-Afuera ($O(N^2)$):**
  Para un texto de $N = 100,000$, en el peor caso la expansión a ciegas puede tomar hasta $\approx 10^{10}$ operaciones. Tardaría varios segundos de cómputo.

* **Con Algoritmo de Manacher ($O(N)$):**
  Gracias al uso del arreglo $P$ y la posición espejo, el ciclo `while` interno que hace la comparación a fuerza bruta **sólo avanza el borde derecho $R$**. Como $R$ nunca retrocede y su valor máximo es $2N$, el número total de comparaciones es lineal.
  Tiempo de ejecución: **< 0.05 segundos**.

**Conclusión:** Manacher demuestra matemáticamente cómo almacenar estados de simetría reduce drásticamente la complejidad computacional.
</div>

---

# 2.4 Hashing de Strings (Algoritmo de Rabin-Karp)
### (Tiempo Estimado: 1.0 Hora)

---

# 2.4 Situación Problemática: Antivirus y Firmas

<div class="problem-box">

### 🦠 Escaneo de Firmas de Malware
Un motor de antivirus escanea un archivo binario $T$ (longitud $N = 10^8$ bytes) buscando una firma de virus específica $P$ (longitud $M = 10^4$ bytes). 

* **Enfoque KMP/Z-Function:** Muy rápidos, pero si tenemos *múltiples* firmas distintas, hacer un preprocesamiento complejo para cada una empieza a ser costoso en memoria y tiempo.
* **Idea Intuitiva:** ¿Qué tal si en lugar de comparar letra por letra, convertimos la cadena $P$ a un único número (un "hash") y lo comparamos numéricamente con los bloques de $T$?
* **El Problema:** Calcular el hash de cada bloque de $T$ desde cero toma $O(M)$. Iterar esto $N$ veces nos devuelve a la fuerza bruta $O(N \times M)$.
* **Desafío:** ¿Podemos calcular el hash de la siguiente ventana de texto en tiempo $O(1)$ basándonos en la ventana anterior?
</div>

---

# 2.4 Hashing Polinomial

Para comparar cadenas en tiempo $O(1)$, mapeamos la cadena a un valor entero usando un **Hash Polinomial**.

Para una cadena $S$ de longitud $M$, su valor hash se calcula como:

$$H(S) = \left( \sum_{i=0}^{M-1} S[i] \cdot p^i \right) \pmod m$$

Donde:
* $S[i]$ es el valor numérico (ASCII) del caracter.
* $p$ es una base prima (ej. 31 para minúsculas, 257 para el set ASCII completo).
* $m$ es un módulo grande (ej. $10^9 + 7$) para evitar desbordamientos numéricos.

**Colisiones:** Dos cadenas distintas podrían dar el mismo hash. Si $H(A) == H(B)$, hacemos una comparación real caracter por caracter para confirmar que no sea un falso positivo.

---

# 2.4 El Concepto de "Rolling Hash"

La verdadera magia de Rabin-Karp es cómo pasa de una ventana a la siguiente en $O(1)$. 

Dada una ventana de texto $T[i \dots i+M-1]$ cuyo hash ya conocemos ($H_{actual}$), queremos calcular el hash de la siguiente ventana $T[i+1 \dots i+M]$.

**Pasos de la ventana deslizante (slide):**
1. **Restar** el valor del caracter que sale por la izquierda ($T[i] \cdot p^{M-1}$).
2. **Multiplicar** todo el resto por la base $p$ para "desplazar" las posiciones (shift).
3. **Sumar** el valor del nuevo caracter que entra por la derecha ($T[i+M]$).

*Con aritmética modular, este desplazamiento toma solo operaciones matemáticas básicas de tiempo constante $O(1)$.*

---

# 2.4 Implementación de Rabin-Karp en Python

```python
def rabin_karp(text, pattern, p=257, m=10**9+7):
    n, k = len(text), len(pattern)
    if k > n: return []
    
    p_pow = 1
    hash_p, hash_t = 0, 0
    
    # Precomputar hashes iniciales y p^(k-1)
    for i in range(k):
        hash_p = (hash_p * p + ord(pattern[i])) % m
        hash_t = (hash_t * p + ord(text[i])) % m
        if i < k - 1: p_pow = (p_pow * p) % m
        
    matches = []
    for i in range(n - k + 1):
        if hash_p == hash_t and text[i:i+k] == pattern:
            matches.append(i) # Verificación extra por posible colisión
        if i < n - k:
            # Rolling Hash O(1)
            hash_t = (hash_t - ord(text[i]) * p_pow) % m
            hash_t = (hash_t * p + ord(text[i+k])) % m
            hash_t = (hash_t + m) % m # Evitar negativos en Python
    return matches
```

---

# 2.4 Solución a la Situación Problemática

<div class="solution-box">

### 🦠 Resultado para el Escaneo Antivirus

* **Recalcular Hash desde Cero ($O(N \times M)$):**
  Inviable para archivos masivos.
* **Rabin-Karp con Rolling Hash ($O(N + M)$):**
  El preprocesamiento del patrón toma $O(M)$. Luego, iterar sobre el archivo de $10^8$ bytes toma $O(N)$ porque cada "salto" de ventana es $O(1)$.
* **El Verdadero Poder (Extensibilidad):**
  Si buscamos **miles de firmas de virus a la vez**, en lugar de comparar contra un hash numérico, comparamos `hash_t` contra un `HashSet` (Tabla Hash en memoria) de todas las firmas. ¡La búsqueda de múltiples patrones se resuelve en el mismo tiempo $O(N)$!

**Conclusión:** El Rolling Hash convierte cadenas complejas en números comparables al instante, siendo la base fundamental de los sistemas de escaneo modernos y detección de plagio masivo.
</div>

---

# 2.5 Arreglos de Sufijos (Suffix Arrays)
### (Tiempo Estimado: 2.5 Horas)

---

# 2.5 Situación Problemática: Índices de Búsqueda Masiva

<div class="problem-box">

### 📚 El Desafío del Motor de Búsqueda (Indexación)
Imagina que tienes una base de datos con el texto completo de Wikipedia ($T$). Los usuarios ingresarán millones de consultas de búsqueda ($P$) cada segundo. 

* **El Problema con KMP/Rabin-Karp:** Estos algoritmos requieren recorrer el texto $T$ *completo* por cada búsqueda. Si $T$ tiene 100 GB, escanearlo para cada palabra ingresada destruiría los servidores.
* **El Desafío:** Necesitamos un **Índice** precalculado sobre $T$. Gastaremos mucho tiempo y memoria construyendo este índice *una sola vez*, pero a cambio, queremos que buscar cualquier patrón $P$ tome un tiempo proporcional solo a la longitud del patrón $O(|P|)$, **independientemente de qué tan masivo sea el texto $T$**.
</div>

---

# 2.5 ¿Qué es un Arreglo de Sufijos?

Un **Suffix Array (SA)** es un arreglo de enteros que contiene los índices de inicio de todos los sufijos de una cadena $S$, **ordenados alfabéticamente (lexicográficamente)**.

### Ejemplo para $S =$ `banana$`
Los sufijos de `banana$` (donde `$` es menor que la 'a') son:
0: `banana$` | 1: `anana$` | 2: `nana$` | 3: `ana$` | 4: `na$` | 5: `a$` | 6: `$`

**Sufijos Ordenados y el Arreglo SA:**
1. `$` (Índice **6**)
2. `a$` (Índice **5**)
3. `ana$` (Índice **3**)
4. `anana$` (Índice **1**)
5. `banana$` (Índice **0**)
6. `na$` (Índice **4**)
7. `nana$` (Índice **2**)

$\implies SA = [6, 5, 3, 1, 0, 4, 2]$

---

# 2.5 La Potencia del Suffix Array (Búsqueda Binaria)

¿Por qué ordenar los sufijos resuelve nuestro problema de búsqueda masiva?

Si todos los sufijos están ordenados alfabéticamente, cualquier aparición de un patrón $P$ será un **prefijo** de uno o más sufijos adyacentes en la lista ordenada.

Por lo tanto, **podemos usar Búsqueda Binaria** sobre el Arreglo de Sufijos:
1. Buscar el patrón $P$ en el arreglo $SA$ (tamaño $N$).
2. Cada comparación de cadenas en la búsqueda binaria toma $O(|P|)$.
3. **Tiempo Total de Búsqueda:** $O(|P| \log N)$.

*¡Hemos independizado el tiempo de búsqueda del tamaño lineal del texto!*

---

# 2.5 Construcción: Del $O(N^2 \log N)$ al $O(N \log^2 N)$

Extraer todos los sufijos y ordenarlos usando el método tradicional de un lenguaje de programación (ej. `sort()`) compara cadenas enteras en cada paso, tomando $O(N^2 \log N)$. Inviable para textos grandes.

### Optimización: Prefix Doubling (Duplicación de Prefijos)
En lugar de comparar los sufijos completos, los ordenamos iterativamente por sus prefijos de longitud $1, 2, 4, 8, 16 \dots$

* **Paso 1:** Ordenamos los sufijos por su primera letra. Asignamos clases de equivalencia (rango).
* **Paso $k$:** Para ordenar los sufijos por longitud $2L$, usamos tuplas compuestas por la clase del prefijo de longitud $L$ que inicia en $i$, y la clase del prefijo de longitud $L$ que inicia en $i+L$. 
* Al ordenar tuplas de 2 enteros, evitamos comparar cadenas largas, bajando el tiempo a $O(N \log^2 N)$ o $O(N \log N)$ con Radix Sort.

---

# 2.5 Implementación: Suffix Array (Prefix Doubling)

```python
def build_suffix_array(s):
    n = len(s)
    sa = list(range(n))
    rank = [ord(c) for c in s]
    k = 1
    
    while k < n:
        # Ordenamos usando tuplas: (rango_actual, rango_siguiente_mitad)
        sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))
        
        tmp_rank = [0] * n
        for i in range(1, n):
            prev, curr = sa[i - 1], sa[i]
            # Si la tupla es diferente a la anterior, incrementamos el rango
            tmp_rank[curr] = tmp_rank[prev] + (
                (rank[prev], rank[prev + k] if prev + k < n else -1) !=
                (rank[curr], rank[curr + k] if curr + k < n else -1)
            )
        rank = tmp_rank
        if rank[sa[-1]] == n - 1: break # Todos los rangos son únicos
        k *= 2
        
    return sa
```

---

# 2.5 Solución a la Situación Problemática

<div class="solution-box">

### 📚 Resultado para el Motor de Búsqueda (Wikipedia)

* **Búsqueda Secuencial (KMP/Rabin-Karp):**
  Para $T = 10 \text{ GB}$ ($10^{10}$ chars), buscar la palabra "algoritmo" ($M=9$) tomaría $\approx 10^{10}$ operaciones. Cada búsqueda tardaría varios segundos. Imposible de escalar a miles de usuarios.

* **Con Suffix Array + Búsqueda Binaria:**
  Construimos el Suffix Array *offline* (tarda minutos u horas, pero se hace una sola vez).
  Para buscar "algoritmo":
  Tiempo = $O(|P| \log N) \implies 9 \times \log_2(10^{10}) \approx 9 \times 33 = 297 \text{ comparaciones!}$
  Tiempo de ejecución: **< 0.001 milisegundos**.

**Conclusión:** El Suffix Array transforma problemas de Big Data inmanejables en operaciones logarítmicas de microsegundos, formando la base estructural de buscadores y bases de datos genómicas (como BLAST).
</div>

---

# 2.6 Longest Common Substring (LCS)
### (Tiempo Estimado: 1.5 Horas)

---

# 2.6 Situación Problemática: Análisis de Similitud

<div class="problem-box">

### 🕵️ Detección de Copia Exacta entre Dos Libros
Tienes dos documentos inmensos: el Libro A ($N = 500,000$ caracteres) y el Libro B ($M = 600,000$ caracteres). Sospechas que un autor copió un capítulo entero del otro. Quieres encontrar la **cadena de texto idéntica más larga** que aparece en ambos libros.

* **Programación Dinámica Tradicional:** Vimos en el Tema 1 que la subsecuencia o subcadena común se puede resolver con DP construyendo una matriz bidimensional.
* **El Problema:** La matriz requiere $O(N \times M)$ en espacio y tiempo. Para estos libros, significa una tabla de $3 \times 10^{11}$ celdas (¡cientos de Gigabytes en RAM!). Simplemente colapsará el sistema.
* **Desafío:** ¿Podemos resolver esto en tiempo $O(N + M)$ y espacio lineal usando las herramientas que acabamos de aprender?
</div>

---

# 2.6 La Solución: Suffix Array + LCP

Podemos resolver este problema reduciéndolo a arreglos de sufijos mediante un ingenioso truco de concatenación.

1. **Concatenar:** Unimos ambos libros con caracteres terminales únicos: 
   $S = \text{LibroA} + \text{"#"} + \text{LibroB} + \text{"\$"}$
2. **Arreglo LCP (Longest Common Prefix):** Es un arreglo complementario al Suffix Array. El valor $LCP[i]$ almacena la longitud del prefijo común más largo entre dos sufijos adyacentes en el arreglo ordenado: $SA[i]$ y $SA[i-1]$.
3. **El Algoritmo de Kasai:** Nos permite calcular el arreglo LCP en tiempo estrictamente lineal $O(|S|)$, sin comparar repetidamente desde cero.

---

# 2.6 Extracción de la Subcadena Más Larga

Una vez que tenemos el **Suffix Array (SA)** ordenado y el **Arreglo LCP** para nuestra cadena concatenada $S$, la lógica es hermosa y directa:

Si dos sufijos comparten un prefijo largo, en el Suffix Array ordenado **quedarán uno al lado del otro**. 

**Regla de Búsqueda:**
1. Recorrer el arreglo LCP.
2. Buscar el valor máximo $LCP[i]$.
3. **Condición estricta:** Para que ese prefijo común pertenezca a ambos libros, el sufijo $SA[i]$ debe provenir del Libro A y el sufijo $SA[i-1]$ debe provenir del Libro B (o viceversa). Comprobamos esto viendo si los índices caen antes o después del caracter `#`.

---

# 2.6 Implementación: LCS con Kasai (LCP)

```python
def kasai_lcp(s, sa):
    n = len(s)
    rank, lcp = [0] * n, [0] * n
    for i, suf in enumerate(sa): rank[suf] = i
    
    h = 0
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rank[i]] = h
            if h > 0: h -= 1
    return lcp

def longest_common_substring(s1, s2):
    s = s1 + '#' + s2 + '$'
    sa = build_suffix_array(s)
    lcp = kasai_lcp(s, sa)
    
    max_len, best_start, sep = 0, 0, len(s1)
    for i in range(1, len(s)):
        # Condición: que los sufijos vengan de lados diferentes del '#'
        if (sa[i] < sep and sa[i-1] > sep) or (sa[i] > sep and sa[i-1] < sep):
            if lcp[i] > max_len:
                max_len, best_start = lcp[i], sa[i]
                
    return s[best_start : best_start + max_len]
```

---

# 2.6 Solución a la Situación Problemática

<div class="solution-box">

### 🕵️ Resultado para el Análisis Literario

* **Programación Dinámica ($O(N \times M)$):**
  $3 \times 10^{11}$ operaciones. Requeriría alrededor de $\approx 300 \text{ GB}$ de memoria RAM. Inviable en una computadora estándar.

* **Suffix Array + LCP ($O(N + M)$):**
  1. Construcción SA: Tiempo lineal o $O(N \log N)$ (Fracciones de segundo).
  2. Construcción LCP (Kasai): $O(N+M)$ (Casi instantáneo).
  3. Escaneo lineal del LCP: $1.1 \times 10^6$ operaciones.
  
**Conclusión:** Encontramos el capítulo copiado exacto usando apenas $\approx 10 \text{ MB}$ de RAM y menos de **1 segundo** de procesamiento, demostrando que estructurar los datos correctamente (SA) vence a la fuerza bruta e incluso a la Programación Dinámica en escenarios de Big Data.
</div>

---

# 2.7 Matriz Comparativa Final del Tema 2

| Algoritmo / Estructura | Caso de Uso Principal | Complejidad Búsqueda | Modificación del Patrón |
| :--- | :--- | :--- | :--- |
| **Fuerza Bruta** | Textos ultra cortos | $O(N \times M)$ | Dinámica |
| **KMP** | Búsqueda exacta estándar | $O(N + M)$ | Dinámica ($O(M)$ preproc) |
| **Z-Function** | Múltiples patrones (concatenados)| $O(N + M)$ | Dinámica |
| **Manacher** | Palíndromos más largos | $O(N)$ | N/A |
| **Rabin-Karp** | Múltiples patrones paralelos | $O(N + M)$ | Dinámica (Hashes) |
| **Suffix Array** | Bases de datos / Indexación masiva | $O(\|P\| \log N)$ | **Estática** (Índice previo) |

---

# Conclusiones y Próximos Pasos

---

# Conclusiones del Tema 2

1. **La memoria del algoritmo:** Técnicas como KMP y Z-Function logran tiempo lineal al evitar re-evaluar caracteres que ya "conocen".
2. **Transformación del problema:** Manacher simplifica la lógica par/impar modificando la cadena original, una técnica brillante en diseño de algoritmos.
3. **El poder de las Matemáticas:** Rabin-Karp cambia el paradigma de comparar "letras" a comparar "números" mediante el *Rolling Hash*.
4. **Precomputación (Trade-off):** Los Suffix Arrays consumen recursos al crearse, pero transforman búsquedas masivas de tiempo lineal a logarítmico.

---

# Preguntas de Repaso

1. En el algoritmo KMP, ¿qué significa el valor almacenado en `LPS[i]` y cómo evita que el puntero del texto retroceda?
2. Explica la diferencia principal de filosofía entre la tabla $Z$ y el algoritmo de KMP.
3. ¿Por qué el algoritmo de Manacher inserta un caracter "fantasma" (como `#`) entre cada letra de la cadena original?
4. En el Hashing de Strings, ¿qué es una colisión y cómo debe manejarla el algoritmo de Rabin-Karp para evitar falsos positivos?
5. Si buscar una palabra en un texto con Rabin-Karp toma tiempo proporcional al texto completo, ¿por qué en un Suffix Array toma tiempo proporcional solo a la palabra buscada?

---

# ¡Gracias por su atención!

**Siguiente Clase:** Tema 3 - Algoritmos sobre Grafos (Dijkstra, Flujo Máximo, Árboles Recubridores).