public class Divide {
    public static void main(String[] args) {
        System.out.println("Begin...");
        int n = 7;
        System.out.print("Fibonacci para n=" + n + " es: " + fibonacci(n));
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
}