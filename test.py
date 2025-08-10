import pydealer as pd
import random as rd
from utils import new_ranks, simpleAI, getTrash, getComboList


def getList(hand, inp):
    list = inp.split(" ")
    if(len(hand.find_list(list, limit=1))==len(list)):
        return hand.get_list(list, limit=1)
    return None


deck = pd.Deck(rebuild=True, re_shuffle=True, ranks=new_ranks)
joker_big = pd.Card("Big", "Joker")
joker_small = pd.Card("Small", "Joker")
deck.add(joker_big)
deck.add(joker_small)
deck.shuffle()

ai = simpleAI('ai')
ai.hand.add(deck.deal(20))
ai.hand.sort()

print(ai.hand)
while(True):
    print(getTrash(ai.hand, input('combo: '), input("trashType:"), getComboList(ai.hand)))
