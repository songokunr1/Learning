import collections
import dis
import asyncio
Card = collections.namedtuple('Card', ['rank', 'suit'])


class Deck():
    numbers = [number for number in range(2, 11)] + list("JQKA")
    ranks = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._card = [Card(rank, suit) for suit in self.numbers for rank in self.ranks]

    def __repr__(self):
        return 'Card(%r, %r)' % (10, 15)

    def __len__(self):
        return len(self._card)

    def __getitem__(self, item):
        return self._card[item]

cards = Deck()
print(dis.dis(Deck))

