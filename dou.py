from game import Game
from players import Human, SimpleAI


if __name__ == '__main__':
    game = Game(SimpleAI("P3"), SimpleAI("P1"), SimpleAI("P2"), 1)
    game.start()
    