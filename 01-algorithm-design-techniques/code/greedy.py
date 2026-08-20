def coins(money: int, coins: list[int]) -> list[int]:
    coins = sorted(coins, reverse=True)
    result = []

    for coin in coins:
        while money >= coin:
            money -= coin
            result.append(coin)

    if money == 0:
        return result
    else:
        return []


def coinsplus(money: int, coins: list[int]) -> list[int]:
    result = []

    for coin in sorted(coins, reverse=True):
        if money == 0:
            break

        count, money = divmod(money, coin)
        if count:
            result.extend([coin] * count)

    return result if money == 0 else []
