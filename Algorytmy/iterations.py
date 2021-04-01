def fib(n):
    bottom_up = [None]
    bottom_up.append(1)
    bottom_up.append(1)
    for i in range(3, n+1):
        bottom_up.append(bottom_up[-1] + bottom_up [-2])
    return bottom_up[-1]

print (fib(500))

