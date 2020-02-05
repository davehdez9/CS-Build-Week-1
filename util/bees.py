import math
from random import random


class Bee():
    def __init__(self, name):
        self.name = name
        self.honeyGained = 2
        self.honeyLost = 1
        self.xp = 1

    def initializeBee(self):
        # Determine a difficulty for the monster
        multiplier = self.getDifficulty()

        # Use that difficulty to calculate a honey gained, lost and xp
        self.honeyGained = multiplier * 5
        self.honeyLost = multiplier * 2
        self.xp = multiplier

    # helper method
    def getDifficulty(self):
        difficulty = math.ceil(random() * 100)

        if difficulty < 50:
            return 3
        elif difficulty >= 50 and difficulty < 80:
            return 6
        elif difficulty >= 80 and difficulty < 95:
            return 8
        else:
            return 10

    def getName():
        names = ['Venus Fly Trap', 'Killer Bee', 'Bumble Bee', 'Carpenter Bee', 'Yellow Jacket',
                 'Queen Bee', 'Honey Bee', 'Digger Bee', 'Mining Bee', 'LeafCutter Bee']


class VenusFlyTrap(Bee):
    def __init__(self, name="Venus Fly Trap"):
        super().__init__(name)
