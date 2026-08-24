def e_queens(n: int, places: list[int]) -> list[int]:
    if len(places) == n:
        return places
    solution = None
    row = 0
    while not solution and row < n:
        #
        if is_safe(row, places):
            places.append(row)
            solution = e_queens(n, places)
            if solution:
                return places
            places.pop()
        row += 1
    return None


def is_safe(row: int, places: list[int]) -> bool:
    colum = len(places)
    if colum == 0:
        return True
    for _colum, _row in enumerate(places):
        if row == _row:
            return False
        __row = abs(row - _row)
        __colum = abs(colum - _colum)
        if __row == __colum:
            return False
    return True


if __name__ == "__main__":
    print(e_queens(16, []))
