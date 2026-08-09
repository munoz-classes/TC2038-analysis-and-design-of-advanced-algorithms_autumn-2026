public class DivideAndConquer {
    public static void main(String[] args) {
        int[] arr = { 38, 27, 43, 3, 9, 82, 10 };
        System.out.println("Original array: ");
        printArray(arr);

        mergeSort(arr, 0, arr.length - 1);

        System.out.println("\nSorted array: ");
        printArray(arr);
    }

    /**
     * Función utilitaria para imprimir un arreglo
     */
    public static void printArray(int[] arr) {
        for (int value : arr) {
            System.out.print(value + " ");
        }
        System.out.println();
    }

    public static void mergeSort(int[] arr, int left, int right) {
        if (left < right) {
            // Encuentra el punto medio del arreglo
            int mid = left + (right - left) / 2;

            // Ordena la primera y segunda mitad
            mergeSort(arr, left, mid);
            mergeSort(arr, mid + 1, right);

            // Combina las mitades ordenadas
            merge(arr, left, mid, right);
        }
    }

    public static void merge(int[] arr, int left, int mid, int right) {
        // Tamaño de los subarreglos
        int n1 = mid - left + 1;
        int n2 = right - mid;

        // Crear arreglos temporales
        int[] L = new int[n1];
        int[] R = new int[n2];

        // Copiar datos a los arreglos temporales
        for (int i = 0; i < n1; i++) {
            L[i] = arr[left + i];
        }
        for (int j = 0; j < n2; j++) {
            R[j] = arr[mid + 1 + j];
        }

        // Combinar los arreglos temporales de nuevo en el arreglo original
        int i = 0, j = 0, k = left;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) {
                arr[k] = L[i];
                i++;
            } else {
                arr[k] = R[j];
                j++;
            }
            k++;
        }

        // Copiar los elementos restantes de L[], si los hay
        while (i < n1) {
            arr[k] = L[i];
            i++;
            k++;
        }

        // Copiar los elementos restantes de R[], si los hay
        while (j < n2) {
            arr[k] = R[j];
            j++;
            k++;
        }
    }
}
