import java.util.*;

/**
 * Clase que representa una arista/arco dirigida con peso.
 */
class Edge {
    int dest;
    double weight;

    public Edge(int dest, double weight) {
        this.dest = dest;
        this.weight = weight;
    }

    @Override
    public String toString() {
        return "-> " + dest + " (peso: " + weight + ")";
    }
}

/**
 * Clase que representa un Digrafo usando Lista de Adyacencia.
 */
class DirectedGraph {
    // Mapa donde la clave es el nodo de origen y el valor es la lista de aristas
    // salientes
    private final Map<Integer, List<Edge>> adjList;

    public DirectedGraph() {
        this.adjList = new HashMap<>();
    }

    /**
     * Agrega un vértice al grafo si no existe.
     */
    public void addVertex(int v) {
        adjList.putIfAbsent(v, new ArrayList<>());
    }

    /**
     * Agrega una arista dirigida desde 'src' hacia 'dest' con un peso dado.
     */
    public void addEdge(int src, int dest, double weight) {
        addVertex(src);
        addVertex(dest);
        adjList.get(src).add(new Edge(dest, weight));
    }

    /**
     * Obtiene los vecinos (aristas salientes) de un vértice.
     */
    public List<Edge> getNeighbors(int v) {
        return adjList.getOrDefault(v, Collections.emptyList());
    }

    /**
     * Obtiene el conjunto de todos los vértices del grafo.
     */
    public Set<Integer> getVertices() {
        return adjList.keySet();
    }

    /**
     * Muestra la estructura del grafo en consola.
     */
    public void printGraph() {
        System.out.println("=== Estructura del Digrafo ===");
        for (int v : adjList.keySet()) {
            System.out.println("Vértice [" + v + "]: " + adjList.get(v));
        }
    }
}

public class Main {
    public static void main(String[] args) {
        // 1. Instanciación del grafo
        DirectedGraph graph = new DirectedGraph();

        // 2. Poblado de datos de prueba
        // Se crean conexiones dirigidas con sus respectivos pesos:
        graph.addEdge(0, 1, 4.0);
        graph.addEdge(0, 2, 2.5);
        graph.addEdge(1, 2, 1.2);
        graph.addEdge(1, 3, 5.0);
        graph.addEdge(2, 3, 8.1);
        graph.addEdge(2, 4, 10.0);
        graph.addEdge(3, 4, 2.3);
        graph.addEdge(4, 0, 3.7); // Ciclo hacia el origen

        // 3. Imprimir el grafo completo
        graph.printGraph();

        System.out.println("\n=== Ejemplo de Procesamiento ===");

        // 4. Ejemplo de procesamiento: Iteración sobre nodos y cálculo de grados de
        // salida
        for (int u : graph.getVertices()) {
            List<Edge> neighbors = graph.getNeighbors(u);
            System.out.println("El nodo " + u + " tiene " + neighbors.size() + " aristas salientes:");

            for (Edge edge : neighbors) {
                System.out.println("   Vértice destino: " + edge.dest + " | Peso: " + edge.weight);
            }
        }
    }
}