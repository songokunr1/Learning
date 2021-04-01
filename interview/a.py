from random import randint


class Game:

    def __init__(self):
        self.secret_number = str(randint(1000, 10000))
        print(self.secret_number)
        self.guesses = 0

    def guess(self):
        self.guesses += 1
        number = str(input())
        cows = 0
        bulls = 0
        for user_digit, secret_digit in zip(number, self.secret_number):
            if user_digit == secret_digit:
                cows += 1
                continue
            elif user_digit in self.secret_number:
                bulls += 1
        print('{} cows, {} bulls'.format(cows, bulls))
        if cows == 4:
            print('Game over, {} guesses'.format(self.guesses))
            return
        else:
            self.guess()


Game().guess()
