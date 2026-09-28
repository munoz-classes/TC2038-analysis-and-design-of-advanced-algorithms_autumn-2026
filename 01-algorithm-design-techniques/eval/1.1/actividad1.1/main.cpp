/*
 * ============================================================================
 * main.cpp
 * ----------------------------------------------------------------------------
 * Curso : TC2038 - Analisis y diseno de algoritmos avanzados
 * Tema  : Divide y venceras - MergeSort
 * ----------------------------------------------------------------------------
 * Descripcion:
 *   Lee un entero N seguido de N valores reales (double), uno por linea,
 *   desde la entrada estandar, y los imprime ordenados de MAYOR a MENOR
 *   utilizando el algoritmo MergeSort (divide y venceras).
 *
 * Compilacion:
 *   g++ -std=c++17 -Wall -Wextra -O2 -o main main.cpp
 *
 * Complejidad global:
 *   Tiempo : O(n log n) en el peor, mejor y caso promedio.
 *   Espacio: O(n) por los arreglos temporales usados en la fusion.
 * ============================================================================
 */

#include <iostream>
#include <vector>
#include <iomanip>

/*
 * mergeHalves
 * ----------------------------------------------------------------------------
 * COMBINA dos mitades ya ordenadas de mayor a menor:
 *   a[low..mid]  y  a[mid+1..high]
 * en un unico tramo a[low..high] ordenado de mayor a menor.
 *
 * Estabilidad: al usar '>=' en la comparacion, ante valores iguales se toma
 * primero el elemento de la mitad izquierda, preservando el orden relativo
 * original (ordenamiento estable).
 *
 * Complejidad:
 *   Tiempo : O(n)   con n = high - low + 1
 *   Espacio: O(n)   por las copias 'left' y 'right'
 */
void mergeHalves(std::vector<double> &a, int low, int mid, int high) {
    std::vector<double> left(a.begin() + low, a.begin() + mid + 1);
    std::vector<double> right(a.begin() + mid + 1, a.begin() + high + 1);

    std::size_t i = 0;   // indice sobre 'left'
    std::size_t j = 0;   // indice sobre 'right'
    int k = low;         // posicion de escritura en 'a'

    // Mientras queden elementos en AMBAS mitades, tomamos el mayor del frente.
    while (i < left.size() && j < right.size()) {
        if (left[i] >= right[j]) {
            a[k] = left[i];
            ++i;
        } else {
            a[k] = right[j];
            ++j;
        }
        ++k;
    }

    // Se vacio una mitad; copiamos lo que sobre de la otra (ya esta ordenado).
    while (i < left.size()) {
        a[k] = left[i];
        ++i;
        ++k;
    }

    while (j < right.size()) {
        a[k] = right[j];
        ++j;
        ++k;
    }
}

/*
 * mergeSort
 * ----------------------------------------------------------------------------
 * DIVIDE y VENCE de forma recursiva el tramo a[low..high].
 *   1. DIVIDE : calcula el punto medio.
 *   2. VENCE  : ordena recursivamente cada mitad.
 *   3. COMBINA: fusiona ambas mitades ya ordenadas.
 *
 * Complejidad:
 *   Tiempo : O(n log n)  (recurrencia T(n) = 2 T(n/2) + O(n))
 *   Espacio: O(log n)    por la pila de recursion (mas O(n) de mergeHalves)
 */
void mergeSort(std::vector<double> &a, int low, int high) {
    if (low >= high) {                   // Caso base: 0 o 1 elemento, ya ordenado
        return;
    }

    int mid = low + (high - low) / 2;    // punto medio (evita desbordamiento)
    mergeSort(a, low, mid);              // ordena la mitad izquierda
    mergeSort(a, mid + 1, high);         // ordena la mitad derecha
    mergeHalves(a, low, mid, high);      // combina ambas mitades
}

/*
 * main
 * ----------------------------------------------------------------------------
 * Lee la entrada, invoca el ordenamiento e imprime el resultado.
 *
 * Complejidad:
 *   Tiempo : O(n log n) dominada por mergeSort.
 *   Espacio: O(n) por el arreglo de valores.
 */
int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) {   // sin un N valido no hay nada que ordenar
        return 0;
    }

    if (n <= 0) {             // N igual o menor a cero: salida vacia
        return 0;
    }

    std::vector<double> a(static_cast<std::size_t>(n));
    for (std::size_t idx = 0; idx < a.size(); ++idx) {
        std::cin >> a[idx];
    }

    mergeSort(a, 0, n - 1);

    // 15 cifras significativas: imprime enteros limpios (5, no 5.000000)
    // y conserva los decimales de los valores reales.
    std::cout << std::setprecision(15);
    for (const double value : a) {
        std::cout << value << "\n";
    }

    return 0;
}