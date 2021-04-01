def rev_int(number):
    if str(number)[0] == '-':
        return int('-' + str(number)[:0:-1])
    return int(str(number)[::-1])

print(rev_int(-10020033))