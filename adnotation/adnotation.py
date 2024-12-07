def dodawanie(a: int, b: int) -> int:
    return a + b


b = '555'

# print(dodawanie(5, b))


def dodawanie(a: int, b: int) -> int:

    return a + b


class Animal:
    pass


class Pies:
    pass


def owczarek(pies: Pies) -> Animal:
    return Animal()


def convert_input_into_string(value: str)-> int:
    try:
        return int(value)
    except ValueError:
        print(f'niestety nie dam rady przekonwertowac {value}')



while True:
    liczba_od_gracza = convert_input_into_string(input('Podaj liczbe'))
    if liczba_od_gracza:
        break


print(dodawanie(liczba_od_gracza, 5))
