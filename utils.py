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

combos = ['a', 'aa', 'aaa', 'aaab', 'aaabb', 'aaaa', 'aabbcc', 'aaabbb', 'aaabbbcd', 'aaabbbccdd']

def oneDiff(card1, card2):
    return abs(new_ranks["values"][card1.value]-new_ranks["values"][card2.value])==1

def maxDupes(cards):
    copy = pd.Stack(cards=cards, sort=True, ranks=new_ranks)
    maxDupe = 0
    dupeCard = None
    numDupes = 0
    while(copy.size):
        dupeSize = len(copy.find(copy[0].value))
        if(maxDupe<dupeSize): 
            maxDupe = dupeSize
            dupeCard = copy[0]
            numDupes = 1
        elif(maxDupe==dupeSize):
            numDupes+=1
        copy.get(copy[0].value)
    return (maxDupe, dupeCard, numDupes)
        
        
    
def playCards(hand, choice):
    list = choice.split(" ")
    copy = pd.Stack(cards=hand, sort=True, ranks=new_ranks)
    if(len(copy.find_list(list, limit=1))!=len(list)):
        return None
    cards = pd.Stack(cards=copy.get_list(list, limit=1), sort=True, ranks=new_ranks)
    
    if(cards.size==1):
        return (cards[0], 'a')
    
    if(cards.size==2 and cards[0].value==cards[1].value):
        if(cards[0].value=="Joker"):
            return (cards[0], 'aaaa')
        return (cards[0], 'aa')
    
    maxDupe, dupeCard, numDupes = maxDupes(cards)
    if(maxDupe==3):
        if(cards.size==3):
            return (dupeCard, 'aaa')
        if(cards.size==4):
            return (dupeCard, 'aaab')
        if(cards.size==5):
            return (dupeCard, 'aaabb')
        
    if(maxDupe==4 and cards.size==4):
        return (dupeCard, 'aaaa')
    
    if((maxDupe==2 and numDupes==3 and cards.size==6) and (oneDiff(cards[0], cards[2]) and oneDiff(cards[2], cards[4]))):
        return (cards[0], 'aabbcc')
    
    if(maxDupe==3 and numDupes==2 and cards.size>=6):
        dupe_1 = cards.get(dupeCard.value)[0]
        
        maxDupe, dupeCard, numDupes = maxDupes(cards)

        
        if(dupeCard.lt(dupe_1, new_ranks)):
            dupe_2 = dupe_1
            dupe_1 = cards.get(dupeCard.value)[0]
        else: 
            dupe_2 = cards.get(dupeCard.value)[0]
        if(maxDupe==3):
            if(oneDiff(dupe_1, dupe_2)):
                if(not cards.size):
                    return (dupe_1, 'aaabbb')
                if(cards.size==2 and cards[0].ne(cards[1], new_ranks)):
                    return (dupe_1, 'aaabbbcd')
                if(cards.size==4 and cards[0].eq(cards[1], new_ranks) and cards[2].eq(cards[3], new_ranks) and cards[1].ne(cards[2], new_ranks)):
                    return (dupe_1, 'aaabbbccdd')
        
    if(maxDupe==4 and cards.size==4):
        return (dupeCard, 'aaaa')
    
    if(maxDupe==1 and cards.size>=5):
        for i in range(cards.size-1):
            if(not oneDiff(cards[i], cards[i+1])):
                return None
        return (cards[0], cards.size)
    
    return None

class Human:
    def __init__(self, name):
        self.hand = pd.Stack(ranks=new_ranks)
        self.name = name
    
    def select(self, table):
        inp = input(f"Your turn: \n{self.hand} \nSelect a card: ")
        play = playCards(self.hand, inp)
        while (not play):
            inp = input("INVALID card! Try again: ")
            play = playCards(self.hand, inp)
        self.hand.get_list(inp.split(" "), limit=1, sort=True, ranks=new_ranks)
        print(f"{self.name} have played {play}")
        return play
    
    def getEmpty(self):
        return not self.hand.size
        
        
class simpleAI:
    def __init__(self, name):
        self.hand = pd.Stack(ranks=new_ranks)
        self.name = name
    
    def select(self, table):
        play = self.hand.random_card(remove=True)
        print(f"{self.name} has played {play}")
        return None
    
    def getEmpty(self):
        return not self.hand.size
        