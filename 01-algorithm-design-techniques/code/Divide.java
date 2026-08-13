public class Divide {
    public static void main(String[] args) {
        System.out.println("Begin...");
        int n = 7;
        // System.out.print("Fibonacci para n=" + n + " es: " + fibonacci(n));
        hanoi(5, 'A', 'C', 'B');
    }

    public static int fibonacci(int n) {
        if (n < 2)
            return n;
        int value = fibonacci(n - 1) + fibonacci(n - 2);
        return value;
    }

    public static int fibonacci_plus(int n) {
        return n < 2 ? n : fibonacci_plus(n - 1) + fibonacci_plus(n - 2);
    }

    public static int binary(int[] list, int value) {
        int left = 0;
        int right = list.length - 1;

        while (left <= right) {
            int middle = left + (right - left) / 2;

            if (list[middle] == value) {
                return middle;
            } else if (list[middle] < value) {
                left = middle + 1;
            } else {
                right = middle - 1;
            }
        }
        return -1;
    }

    public static int[] quicksort(int[] list) {
        if (list == null || list.length < 2) {
            return list;
        }
        quicksort(list, 0, list.length - 1);
        return list;
    }

    private static void quicksort(int[] list, int left, int right) {
        if (left < right) {
            int pivotIndex = partition(list, left, right);
            quicksort(list, left, pivotIndex - 1);
            quicksort(list, pivotIndex + 1, right);
        }
    }

    private static int partition(int[] list, int left, int right) {
        int pivot = list[right];
        int i = left - 1;

        for (int j = left; j < right; j++) {
            if (list[j] <= pivot) {
                i++;
                swap(list, i, j);
            }
        }

        swap(list, i + 1, right);
        return i + 1;
    }

    private static void swap(int[] list, int i, int j) {
        int temp = list[i];
        list[i] = list[j];
        list[j] = temp;
    }

    public static void hanoi(int n, char source, char target, char auxiliary) {
        if (n == 1) {
            System.out.println("Move disk 1 from " + source + " to " + target);
            return;
        }
        hanoi(n - 1, source, auxiliary, target);
        System.out.println("Move disk " + n + " from " + source + " to " + target);
        hanoi(n - 1, auxiliary, target, source);
    }

}