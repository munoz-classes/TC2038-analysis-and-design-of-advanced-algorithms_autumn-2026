public class Divide {
    public static void main(String[] args) {
        System.out.println("Begin...");
        int n = 7;
        // System.out.print("Fibonacci para n=" + n + " es: " + fibonacci(n));
        // hanoi(5, 'A', 'C', 'B');

        int[] A = { 13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7 };
        System.out.println(maxASubarray(A, 0, A.length - 1));
    }

    public static class SubArrayResult {
        int left, right, sum;

        SubArrayResult(int left, int right, int sum) {
            this.left = left;
            this.right = right;
            this.sum = sum;
        }

        @Override
        public String toString() {
            return "SubArrayResult [Inicio=" + left + ", Fin=" + right + ", Suma=" + sum + "]";
        }
    }

    public static SubArrayResult maxASubarray(int[] list, int low, int high) {
        if (low == high) {
            return new SubArrayResult(low, high, list[low]);
        }
        int mid = low + (high - low) / 2;
        SubArrayResult leftResult = maxASubarray(list, low, mid);
        SubArrayResult rightResult = maxASubarray(list, mid + 1, high);
        SubArrayResult cross = MaxSubarray.findMaxCrossingSubarray(list, low, mid, high);
        if (leftResult.sum >= rightResult.sum && leftResult.sum >= cross.sum) {
            return leftResult;
        }

        if (rightResult.sum >= cross.sum) {
            return rightResult;
        }

        return cross;

    }

    public static class MaxSubarray {
        public static SubArrayResult findMaxCrossingSubarray(int[] list, int low, int mid, int high) {
            int leftSum = Integer.MIN_VALUE, sum = 0, maxLeft = mid;
            for (int i = mid; i >= low; i--) {
                sum += list[i];
                if (sum > leftSum) {
                    leftSum = sum;
                    maxLeft = i;
                }
            }
            int rightSum = Integer.MIN_VALUE, maxRight = mid + 1;
            sum = 0;
            for (int j = mid + 1; j <= high; j++) {
                sum += list[j];
                if (sum > rightSum) {
                    rightSum = sum;
                    maxRight = j;
                }
            }
            return new SubArrayResult(maxLeft, maxRight, leftSum + rightSum);
        }
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