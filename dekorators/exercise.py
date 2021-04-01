def add_arg(func):
    a = 5

    def wraper(a, *args):
        print('start')
        print(*args)
        value = func(a, *args)
        print('end')
        return value

    return wraper


@add_arg
def fun(a, b=None):
    if not b:
        return a
    else:
        return a + b


def a(func):
    def b():
        print('1')
        func()
        return 5

    return b


# print(fun(5))
@a
def inner():
    print('dzikus!')
    return 10


# print(inner())  # d = a(inner)()  skrocony zapis


def b(func):
    def b(*args, **kwargs):
        print('1')
        func(*args, **kwargs)
        return 5

    return b


@b
def inner2(*args, **kwargs):
    print('dzikus!')
    return 10


# deko = inner2
# print(deko(5,3,4))  # d = a(inner)()  skrocony zapis
# print(deko.__name__)
# print(help(deko))

# to resolve problem with naming:

import functools


def decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value

    return wrapper_decorator


# c = a()()
# d = a(inner)
# print(d())
# print(c)


# napisz dekorator twice

def few_times(func):
    def inner(*args, **kwargs):
        print('start')
        func(*args, **kwargs)
        func(*args, **kwargs)
        print('koniec')

    return inner


#@few_times

def hello(k='hejoo!!'):
    print(k)



a = few_times(hello)
a('siemka sciemka')


