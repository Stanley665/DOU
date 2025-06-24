import pydealer as pd
import random as rd

deck = pd.Deck(rebuild=True, re_shuffle=True)
print(deck)
print(deck.size)
deck.shuffle()

players = [[pd.Stack(), "You"], [pd.Stack(), "P1"], [pd.Stack(), "P2"]]

players[0][0].add(deck.deal(7))
print(players[0][0])
try: 
    print(players[0][0].get(players[0][0].find(input())[0]))
except:
    print(")
print(players[0][0])
