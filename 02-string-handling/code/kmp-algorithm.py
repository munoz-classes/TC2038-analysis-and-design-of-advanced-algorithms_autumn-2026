def kmp_prefix_function(text: str) -> list[int]:
    """Calcula el arreglo pi para el patrón a buscar utilizando fuerza bruta."""

    z_list = [0] * len(str)

    if len(text) == 0:
        return []

    z_list.append(0)

    for index, _ in enumerate(text[1:], start=1):
        count = 0
        for char in text[index:]:
            if char == text[count]:
                count += 1
            else:
                break
        z_list.append(count)

    return z_list


def kmp_prefix_function_plus(pattern: str) -> list[int]:
    """Calcula el arreglo pi para el patrón a buscar."""
    if not pattern:
        return []

    m = len(pattern)
    pi = [0] * m
    j = 0

    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]

        if pattern[i] == pattern[j]:
            j += 1

        pi[i] = j

    return pi


if __name__ == "__main__":
    print(kmp_prefix_function_plus("abbababba"))
    print(kmp_prefix_function_plus("abbacbabac"))
