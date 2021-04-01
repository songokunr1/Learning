import timeit

list_to_test = """
L = []
x = range(50000)
for item in x:
    L.append(item)
"""

tuple_to_test = """
T = ()
x = range(50000)
for item in x:
    T = T + (item,)
"""

elapsed_time_list = timeit.timeit(tuple_to_test, number=2) / 2
elapsed_time_tuple = timeit.timeit(tuple_to_test, number=2) / 2

print(f'execution time for list it is: {elapsed_time_list}')
print(f'execution time for tuple it is: {elapsed_time_tuple}')


