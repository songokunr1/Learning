class Burger:
    def __int__(self):
        self.buns = None
        self.patty = None
        self.cheese = None

    def set_buns(self, bunStyle):
        self.buns = bunStyle

    def set_patty(self, pattyStyle):
        self.buns = pattyStyle

    def set_cheese(self, cheeseStyle):
        self.buns = cheeseStyle


class BurgerBuilder:
    def __int__(self):
        self.burger = Burger()

    def add_buns(self, bunStyle):
        self.burger.set_buns(bunStyle)
        return self

    def add_patty(self, pattyStyle):
        self.burger.set_buns(pattyStyle)
        return self

    def add_cheese(self, cheeseStyle):
        self.burger.set_buns(cheeseStyle)
        return self

    def build(self):
        return self.burger


burger = BurgerBuilder() \
    .add_cheese("some") \
    .add_patty('little') \
    .build()
