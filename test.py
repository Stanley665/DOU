import pydealer as pd
# import random as rd
from utils import new_ranks, simpleAI


def getList(hand, inp):
    list = inp.split(" ")
    if(len(hand.find_list(list, limit=1))==len(list)):
        return hand.get_list(list, limit=1)
    return None


deck = pd.Deck(rebuild=True, re_shuffle=True, ranks=new_ranks)
# print(deck)
# print(deck.size)
deck.shuffle()

# ai = simpleAI('ai')
# ai.hand.add(deck.deal(20))
# ai.hand.sort()
# print(ai.hand)
two = deck.get('2')[0]
three = deck.get('3')[0]
print(f"{two}, {three}")
print(two.lt(three, new_ranks))