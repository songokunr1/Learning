from collections import namedtuple
from enum import Enum

class HairColor(Enum):
    blonde = 1
    brown = 2
    black = 3
    red = 4

Person = namedtuple('Person', ['name','age','hair_color'])
bert = Person('Bert', 5, HairColor.black)