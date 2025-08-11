from game import Game
from players import Human, SimpleAI


if __name__ == '__main__':
    game = Game(Human("You"), SimpleAI("P1"), SimpleAI("P2"))
    game.start()
    