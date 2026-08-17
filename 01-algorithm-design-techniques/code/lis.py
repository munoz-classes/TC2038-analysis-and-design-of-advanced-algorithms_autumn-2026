import random as rnd


def lis(A):
    dp = [1] * len(A)
    print(dp)

    for i in range(1, len(dp)):
        sub_probs = [dp[k] for k in range(i) if A[k] < A[i]]
        dp[i] = 1 + max(sub_probs, default=0)
    return max(dp, default=0)


if __name__ == "__main__":
    A = [rnd.randint(1, 100) for _ in range(10)]
    print(A)
    print(max(A, default=0))
    print(lis(A))
