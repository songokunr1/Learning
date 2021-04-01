# write fib, silnia rekurencjjnie
# nastepnie iteracyjnie
# 0 1 1 2 3 5
def fib(n):
    if n < 0:
        return None
    if n == 0:
        return 0
    if n == 1 or n == 2:
        return 1
    return fib(n - 1) + fib(n - 2)


def silnia(n):
    if n < 0:
        return None
    if n <= 1:
        return 1
    return silnia(n - 1) * n


def fib_iter(n):
    if n < 0:
        return None
    tab = [value for value in [0, 1, 1]]
    for element in range(3, n + 1):
        tab.append(tab[element - 1] + tab[element - 2])
    return tab[n]


def silnia_iter(n):
    if n < 0:
        return None
    tab = [1, 1]
    for element in range(2, n + 1):
        tab.append(tab[element - 1] * element)
    return tab[n]


def fib_memory(n):
    if n < 0:
        return None
    if n == 0:
        return 0
    if n == 1 or n == 2:
        return 1
    a = 1
    b = 1
    result = 1
    for _ in range(3, n + 1):
        b = a
        a = result
        result = a + b
    return result


def silnia_memory(n):
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    before = 1
    for x in range(2, n + 1):
        curent = x * before
    return curent
