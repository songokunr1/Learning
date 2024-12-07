def outer():
    class innerClass:
        def a(self):
            raise ValueError
    return innerClass()



def calc():
    class_inst = outer()
    result = class_inst.a()
    return result


