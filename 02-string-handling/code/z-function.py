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


def points_agrupation(nums: list[int]) -> list[int]:
    n = len(nums)
    return []


if __name__ == "__main__":
    print(zfunction("abaxabab"))
