#1. Reverse Integer
a = -123
wynik = str(a)[::-1] if str(a)[0] != '-' else '-' + str(a)[:0:-1]

# 2. Average words length
a = 'Ala ma Kota'
b = a.split(" ")
sum([len(element) for element in b])/len(b)
all(b) # unction that returns True if all items in an iterative are true, otherwise it returns False.