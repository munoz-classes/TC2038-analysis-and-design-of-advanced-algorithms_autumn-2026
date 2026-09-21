# PARTE 1
# complejidad O(n)

def construirLps(patron):
    lenPatron = len(patron)
    lps = [0] * lenPatron
    lenPrevia = 0 # la longuitud mas larga dl prefijo previo
    i =  1

    while i < lenPatron:
        if patron[i] == patron[lenPrevia]:
            lenPrevia += 1
            lps[i] = lenPrevia
            i += 1
        else:
            if lenPrevia != 0:
                lenPrevia = lps[lenPrevia - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def buscarKmp(texto, patron):
    if not patron or not texto:
        return False, -1

    lenTexto = len(texto)
    lenPatron = len(patron)

    # contruimos la tabla de prefijos para el patron
    lps = construirLps(patron)

    iTexto = 0 # caracter actual en "texto"
    iPatron = 0 # caracter actual en "patron"

    # escanear el texto de transmision
    while iTexto < lenTexto:
        if texto[iTexto] == patron[iPatron]:
            iTexto += 1
            iPatron += 1

        # si logramos encontrar el patron completo
        if iPatron == lenPatron:
            posicion_inicial_base_1 = (iTexto - lenPatron) + 1
            return True, posicion_inicial_base_1

        # si no coincide y esta desalineado
        elif iTexto < lenTexto and texto[iTexto] != patron[iPatron]:
            if iPatron != 0:
                # usamos la tabla LPS para "saltar" comparaciones y no volver a leer todo
                iPatron = lps[iPatron - 1]
            else:
                iTexto += 1

    return False, -1


# PARTE 2
# complejidad O(n)
def manacherPalindromoLargo(texto):

    if not texto:
        return 0, 0

    # Normalizar la cadena (insertamos #, delimitamos inicio y fianl)
    tTransformado = "¿#" + "#".join(texto) + "#?"
    lenTotal = len(tTransformado)
    radio = [0] * lenTotal # almacen del radio del palindromo en cada centro

    centro = 0 # mejor centro hasta el momento
    limDer = 0 # limite dercho del mejor hasta le momento

    # parte principal MANACHER
    for i in range(1, lenTotal-1):
        iEspejo = 2 * centro - i # posicion simetrica de i respecto a centro

        if i < limDer:
            radio[i] = min(limDer - i, radio[iEspejo])
        else:
            radio[i] = 0


        # probamos a expandir el palindromo desde i
        while tTransformado[i + 1 + radio[i]] == tTransformado[i - 1 - radio[i]]:
            radio[i]+= 1

        # si el palindromo actual superaa limDer, se actualiza
        if i + radio[i] > limDer:
            centro = i
            limDer = i + radio[i]

    # Encontrar el radio max y su centro
    lenMax = 0
    iCentroMax = 0
    for i in range(1, lenTotal - 1):
        if radio[i] > lenMax:
            lenMax = radio[i]
            iCentroMax = i

    # mapear los indices de regreso al texto original
    # estas posiciones son en base 0
    posicionInicial = (iCentroMax - 1 - lenMax) // 2
    posicionFinal = posicionInicial + lenMax - 1

    # pasar a base 1
    posicionInicial = posicionInicial + 1
    posicionFinal = posicionFinal + 1

    return posicionInicial, posicionFinal


# PARTE 3
# construcción SA O(n log n), LCP O(n), búsqueda O(n) --> Total O(n log n)
def leer(nombre):
    # Elimina espacios y saltos de línea al inicio y final del texto, y devuelve el texto limpio
    with open(nombre, 'r') as f:
        return f.read().strip()

# Se construye el suffix array de un texto dado, y se devuelve como una lista de enteros
# tiempo O(n log n), espacio O(n)
def construir_suffix_array(texto):
    s = texto + '\x00' #Caracter nulo al final para asegurar que todos los sufijos sean distintos
    n = len(s)

    # ordenamiento inicial según el primer caracter de cada sufijo
    sa = sorted(range(n), key=lambda i: s[i])
    rank = [0] * n
    for i in range(1, n):
        rank[sa[i]] = rank[sa[i - 1]] + (s[sa[i]] != s[sa[i - 1]])

    # mientras todos los sufijos no estén ordenados, se duplica la longitud de los prefijos considerados
    k = 1
    while k < n and rank[sa[-1]] < n - 1:
        # counting sort
        segundo = [(rank[i + k] if i + k < n else -1) + 1 for i in range(n)]
        maxv = max(segundo) + 1
        cont = [0] * maxv
        for v in segundo:
            cont[v] += 1
        for i in range(1, maxv):
            cont[i] += cont[i - 1]
        sa_tmp = [0] * n
        for i in range(n - 1, -1, -1):
            cont[segundo[i]] -= 1
            sa_tmp[cont[segundo[i]]] = i

        # counting sort
        primero = rank[:]
        maxv = max(primero) + 1
        cont = [0] * maxv
        for v in primero:
            cont[v] += 1
        for i in range(1, maxv):
            cont[i] += cont[i - 1]
        sa_nuevo = [0] * n
        for i in range(n - 1, -1, -1):
            idx = sa_tmp[i]
            cont[primero[idx]] -= 1
            sa_nuevo[cont[primero[idx]]] = idx
        sa = sa_nuevo

        # recalculamos los rangos de los sufijos ordenados
        nuevo_rank = [0] * n
        for i in range(1, n):
            a, b = sa[i - 1], sa[i]
            ka = (rank[a], rank[a + k] if a + k < n else -1)
            kb = (rank[b], rank[b + k] if b + k < n else -1)
            nuevo_rank[b] = nuevo_rank[a] + (1 if kb != ka else 0)
        rank = nuevo_rank
        k *= 2

    # eliminamos el sufijo vacío y devolvemos el suffix array
    return sa[1:]

# se contruye el lcp 
# tiempo O(n), espacio O(n)
def construir_lcp(texto, sa):
    n = len(texto)
    # arreglo inverso del suffix array, para poder calcular el lcp en O(n)
    rank = [0] * n
    for i, suf in enumerate(sa):
        rank[suf] = i
    lcp = [0] * n
    # algoritmo de Kasai para calcular el lcp
    h = 0
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and texto[i + h] == texto[j + h]:
                h += 1
            lcp[rank[i]] = h
            if h > 0:
                h -= 1
        else:
            h = 0
    return lcp

# encontrar la subcadena común más larga entre dos textos y devolver su posición inicial y final en el primer texto
def substring_comun_mas_largo(t1, t2):
    # concatenar con separador
    combinado = t1 + '#' + t2
    sa = construir_suffix_array(combinado)
    lcp = construir_lcp(combinado, sa)
    # recorrer lcp
    n1 = len(t1)

    mejor = 0
    inicio = 0
    for i in range(1, len(sa)):
        a, b = sa[i - 1], sa[i]
        if (a < n1) != (b < n1):
            if lcp[i] > mejor:
                mejor = lcp[i]
                inicio = a if a < n1 else b

    return inicio + 1, inicio + mejor


def leerArchivo(nombre_archivo):
    """
    Lee un archivo de texto, elimina saltos de línea y retornos de carro
    para procesar únicamente el flujo continuo de caracteres.
    """
    with open(nombre_archivo, 'r') as f:
        contenido = f.read()
        return contenido.replace('\n', '').replace('\r', '').strip()

    

# BLOQUE PRINCIPAL DE EJECUCIÓN (MAIN)
if __name__ == "__main__":
    # Cargar los 5 archivos requeridos
    t1 = leerArchivo('transmission1.txt')
    t2 = leerArchivo('transmission2.txt')
    m1 = leerArchivo('mcode1.txt')
    m2 = leerArchivo('mcode2.txt')
    m3 = leerArchivo('mcode3.txt')

    # PARTE 1: Búsqueda de mcodeX en transmisión1 y transmisión2
    transmisiones = [t1, t2]
    mcodes = [m1, m2, m3]

    for t in transmisiones:
        for m in mcodes:
            encontrado, pos = buscarKmp(t, m)
            if encontrado:
                print(f"true {pos}")
            else:
                print("false")

    # PARTE 2: Búsqueda del palíndromo más largo en cada archivo de transmisión
    ini_p1, fin_p1 = manacherPalindromoLargo(t1)
    print(f"{ini_p1} {fin_p1}")

    ini_p2, fin_p2 = manacherPalindromoLargo(t2)
    print(f"{ini_p2} {fin_p2}")

    # PARTE 3: Subcadena común más larga entre transmission1 y transmission2
    ini_lcs, fin_lcs = substring_comun_mas_largo(t1, t2)
    print(f"{ini_lcs} {fin_lcs}")