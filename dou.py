from game import Game
from players import Human, SimpleAI
import random as rd


if __name__ == '__main__':
    game = Game(Human("P1"), SimpleAI("P2"), SimpleAI("P3"))
    while(True):
        game.start(rd.randint(0, 2))
    