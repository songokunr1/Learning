from dekorators.module.dekorators import do_twice

@do_twice
def say(a='hello!'):
    print(f'{a}')

