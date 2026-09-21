from collections import deque

class Grafo:
    def __init__(self):
        self.adyacencia = {}

    def agregar_vertice(self, v):
        """
            agregar vertice para grafo dirigido 
        """
        if v not in self.adyacencia:
            self.adyacencia[v] = []

    def agregar_arista(self, origen, destino):
        """
            agregar arista para grafo dirigido 
        """
        self.adyacencia[origen].append(destino)
        #Si fuera un grafo no dirigido habria que agregar también destino-origen

    def bfs(self, inicio):
        """
            algoritmo breadth first search 
        """
        visitados = set() 
        cola = deque([inicio])

        while cola:
            nodo = cola.popleft()
            if nodo not in visitados:
                visitados.add(nodo)
                cola.extend(self.adyacencia[nodo])

        return visitados

    def dfs(self, inicio):
        """
        algoritmo deep first search 
        """
        visitados = set()
        self._dfs_recursivo(inicio, visitados)

    def _dfs_recursivo(self, inicio, visitados):
        if visitados == None:
            visitados = set()
        visitados.add(inicio)
        for vecino in self.adyacencia[inicio]:
            if vecino not in visitados:
                self._dfs_recursivo(vecino, visitados)

        return visitados

    def buscar_vertice(self, v):
        """
        Si está el nodo se devuelve la lista de adyacencia, sino, se devuelve None 
        """
        if v in self.adyacencia:
            return self.adyacencia[v]
        return None

class NodoTrie:
    def __init__(self):
        self.hijos = {}
        self.fin_palabra = False

class Trie:
    def __init__(self):
        self.raiz = NodoTrie()


    def insertar(self, palabra: str):
        nodo = self.raiz
        for char in palabra:
            if char not in nodo.hijos:
                nodo.hijos[char] = NodoTrie()


if __name__ == "__main__":
    print("grafo")

