import pydealer as pd
# import random as rd
# from utils import new_ranks

new_ranks = {
    "values": {
        "Joker": 14,
        "2": 13,
        "Ace": 12,
        "King": 11,
        "Queen": 10,
        "Jack": 9,
        "10": 8,
        "9": 7,
        "8": 6,
        "7": 5,
        "6": 4,
        "5": 3,
        "4": 2,
        "3": 1
    },
    "suits" : {
        "JOKER": 2,
        "Joker": 1,
        "Spades": 0,
        "Hearts": 0,
        "Clubs": 0,
        "Diamonds": 0
    }
}
def getList(hand, inp):
    list = inp.split(" ")
    if(len(hand.find_list(list, limit=1))==len(list)):
        return hand.get_list(list, limit=1)
    return None


deck = pd.Deck(rebuild=True, re_shuffle=True, ranks=new_ranks)
print(deck)
print(deck.size)
deck.shuffle()

players = [[pd.Stack(), "You"], [pd.Stack(), "P1"], [pd.Stack(), "P2"]]

players[0][0].add(deck.deal(7))
hand = players[0][0]

print((hand.find(term=hand[0].value)))