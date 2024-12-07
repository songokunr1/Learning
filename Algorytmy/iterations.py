def fib(n):
    bottom_up = [None]
    bottom_up.append(1)
    bottom_up.append(1)
    for i in range(3, n+1):
        bottom_up.append(bottom_up[-1] + bottom_up [-2])
    return bottom_up[-1]

print (fib(500))


def fib(n):
    if n == 1 or n == 0:
        return 1
    return fib(n-1) + fib(n-2)

print(fib(10))