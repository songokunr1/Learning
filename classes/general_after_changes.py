
class MathematicFunctions:
    @staticmethod
    def add_two_numbers(a, b):
        return a + b



class Point:
    def __init__(self, initX, initY):
        self.x = initX
        self.y = initY
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    def distance_from_origin(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5

    def __str__(self):
        return "x = {}, y = {}".format(self.x, self.y)
    def halfway(self, target):
        mx = MathematicFunctions.add_two_numbers(self.x, target.x)/2
        my = MathematicFunctions.add_two_numbers(self.y, target.y)/2
        return Point(mx, my)

# point1_x = 5
# point1_y = 4
# print("x = {}, y = {}".format(point1_x, point1_y))
#
# point2_x = 3
# point2_y = 5
# print("x = {}, y = {}".format(point2_x, point2_y))


point = Point(5, 4)
point2 = Point(3, 3)
half = point.halfway(point2)
print(half)



# q = Point(5, 12)
# mid = p.halfway(q)
# # note that you would have exactly the same result if you instead wrote
# # mid = q.halfway(p)
# # because they are both Point objects, and the middle is the same no matter what
#
# print(mid)
# print(mid.get_x())
# print(mid.get_y())
