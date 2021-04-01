def do_sth(a,b):
    print(a + b)
    return "hunrys"


def before(fun):
    def wraper(a,b):
        print("do sth before")
        return fun(a,b)
    print("do it now!")
    return wraper
# print(do_sth())

one_more_thing = before(do_sth)

print(one_more_thing("one ", "more thing"))