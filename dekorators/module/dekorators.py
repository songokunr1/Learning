from datetime import datetime
import functools


def x(a):
    def y(b):
        def z(c):
            return a + b + c

        return z

    return y


abc = x(1)(2)(3)


def time_test_full(func):
    def function_wrapper(*arg, **kw):
        before = datetime.now()
        df = func(*arg, **kw)
        after = datetime.now()
        difference = after - before
        print(difference.total_seconds(), 'seconds per one day')
        return df

    return function_wrapper


def do_twice(func):
    def wrapper(*arg, **kw):
        func(*arg, **kw)
        func(*arg, **kw)

    return wrapper


# def do_twice(func):
#     @functools.wraps(func)
#     def wrapper_do_twice(*args, **kwargs):
#         func(*args, **kwargs)
#         return func(*args, **kwargs)
#     return wrapper_do_twice