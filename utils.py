import pydealer as pd
import random as rd

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


def playCards(hand, choice):
    
    try:
        cards = [hand.find(card) for card in choice.split(" ")]
        indices = hand.find(cards)
    except:
        return None
    if(len(cards)==1):
        return hand.get(hand.find(choice)[0])
    if(len(cards)==2 and ):
        return hand.get(hand.find(choice)[0])

class Human:
    def __init__(self, name):
        self.hand = pd.Stack(ranks=new_ranks)
        self.name = name
    
    def select(self):
        play = playCards(self.hand, input(f"Your turn: \n{self.hand} \nSelect a card: "))
        while (not play):
            play = playCards(self.hand, input("INVALID card! Try again: "))
        return play
        
        
class simpleAI:
    def __init__(self, name):
        self.hand = pd.Stack(ranks=new_ranks)
        self.name = name
    
    def select(self):
        return self.hand.get(self.hand.find(self.hand[rd.randint(0, self.hand.size-1)].value)[0])