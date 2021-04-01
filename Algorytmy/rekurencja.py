def silnia(n):
    if n == 1:
        return 1
    return silnia(n - 1) * n


def fib(n):
    mem = [1, 1]
    if n == 1:
        return mem[:1]
    if n == 2:
        return mem
    for _ in range(n - 2):
        mem.append(mem[-1] + mem[-2])
    return mem


print(fib(12))
