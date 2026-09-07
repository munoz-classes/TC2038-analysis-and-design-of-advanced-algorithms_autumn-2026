def zfunction(pattern: str) -> list[int]:
    if not pattern:
        return []

    m = len(pattern)

    z = [0] * m

    L = R = 0

    for i in range(1, m):
        if i > R:
            while i + z[i] < m and pattern[z[i]] == pattern[i + z[i]]:
                z[i] += 1

            if z[i] > 0:  # actualizar caja
                L = i
                R = i + z[i] - 1
        else:
            # buscar gemelo
            k = i - L
            # buscar espacio
            espacio = R - i + 1
            # caso 2a
            if z[k] < espacio:
                z[i] = z[k]
            # caso 2b
            else:
                z[i] = espacio
                while i + z[i] < m and pattern[z[i]] == pattern[i + z[i]]:
                    z[i] += 1

                # actualizar caja
                L = i

                R = i + z[i] - 1


def shuffle_plus(nums: list[int], n: int) -> list[int]:
    sol = [0] * 2 * n
    for i in range(n):
        sol[2 * i] = nums[i]
        sol[2 * i + 1] = nums[n + i]
    return sol


def shuffle(nums: list[int], n: int) -> list[int]:
    sol = [0] * 2 * n
    a = 0
    b = (2 * n) - 1
    grouping(nums, sol, a, b, n)
    return sol


def grouping(nums: list[int], sol: list[int], a: int, b: int, n: int):
    # base
    if a == b:
        if a < n:
            sol[2 * a] = nums[a]
        else:
            sol[2 * (a - n) + 1] = nums[a]
        return

    # divide
    m = (b - a) // 2
    # left [a, m] right [m+1, b]
    grouping(nums, sol, a, a + m, n)
    grouping(nums, sol, a + m + 1, b, n)


def findMaxConsecutiveOnes(nums: list[int]) -> int:
    c = _c = 0
    for value in nums:
        if value == 1:
            _c += 1
        else:
            c = max(c, _c)
            _c = 0
    return max(c, _c)


if __name__ == "__main__":
    nums = [1, 1, 0, 1, 1, 1]
    # n = 4
    print(findMaxConsecutiveOnes(nums))
