import pydealer as pd
import random as rd
from utils import *
from players import SimpleAI
import numpy as np


def getList(hand, inp):
    list = inp.split(" ")
    if(len(hand.find_list(list, limit=1))==len(list)):
        return hand.get_list(list, limit=1)
    return None


deck = pd.Deck(rebuild=True, re_shuffle=True, ranks=new_ranks)
joker_big = pd.Card("big", "Joker")
joker_small = pd.Card("small", "Joker")
deck.add(joker_big)
deck.add(joker_small)
deck.shuffle()

ai = SimpleAI('ai')
ai.hand.add(deck.deal(20))
ai.hand.sort()
print(ai.hand)
print('\n')
print(deck.size)
deck.empty()
print('\n')
print(deck.size)

ai.hand.add(deck.deal(20))
ai.hand.sort()
print(ai.hand.size)

# table_cards = pd.Stack(cards = [pd.Card(x, 'Clubs') for x in input("Table Cards: ").split(' ')])
# plays = getAllPlays(ai.hand, table_cards, input("Table Type: "))
# for play in plays:
#     print(play)
# while(True):
#     pass