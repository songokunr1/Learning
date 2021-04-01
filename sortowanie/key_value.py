slownik = {"a": 3, "b": 2, "c": 1}
dict(sorted(slownik.items(), key=lambda e: e[1]))
# or
new_slownik = {k: v for k, v in sorted(slownik.items(), key=lambda item: item[1], reverse=True)}

lista = [1,2,3]
list(map(lambda x:x+2, lista))
list(filter(lambda x:x%2, lista))

[(lambda x:x+2)(single) for single in lista]