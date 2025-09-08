import pydealer as pd
import random as rd
import numpy as np

CARDS = 0
CARD_TYPE = 1
TRASH_TYPE = 2

DUPE_TRASH = 0
NUM_TRASH = 1

new_ranks = {
    "values": {
        "Big": 15,
        "Small": 14,
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
        "3": 1,
        "Null": 0
    },
    "suits" : {
        "Joker": 1,
        "Spades": 0,
        "Hearts": 0,
        "Clubs": 0,
        "Diamonds": 0
    }
}

NULL = pd.Card('Null', any)
CAP = new_ranks['values']['2']




def isConsecutive(card1, card2):
    return abs(new_ranks["values"][card1.value]-new_ranks["values"][card2.value])==1


def nextVal(value):
    ranks = list(new_ranks['values'].keys())[::-1]
    try:
        return ranks[ranks.index(value)+1]
    except (ValueError, IndexError):
        return None
    

def prevVal(value):
    ranks = list(new_ranks['values'].keys())[::-1]
    try:
        return ranks[ranks.index(value)-1]
    except (ValueError, IndexError):
        return None
    

def canPlay(play, table):
    if(play):
        if(not table.cards.size or not table.card_type): return True
        if(play.card_type=='aaaa' and table.card_type!='aaaa'): return True
        if(play.card_type==table.card_type and play>table and play.trash==table.trash): return True
        if(play.card_type=='aaaa' and table.card_type!='aaaa'): return True
    return False


def maxDupes(cards):
    copy = pd.Stack(cards=cards, sort=True, ranks=new_ranks)
    copy.sort()
    maxDupe = 0
    dupeCard = None
    numDupes = 0
    while(copy.size):
        dupeSize = len(copy.find(copy[CARDS].value))
        if(maxDupe<dupeSize): 
            maxDupe = dupeSize
            dupeCard = copy[0]
            numDupes = 1
        elif(maxDupe==dupeSize):
            numDupes+=1
        copy.get(copy[CARDS].value)
    return (maxDupe, dupeCard, numDupes)
        
    
def encodeSelection(hand, selection):
    copy = pd.Stack(cards=hand, sort=True, ranks=new_ranks)
    cards = pd.Stack(cards=copy.get_list(selection, limit=1), sort=True, ranks=new_ranks)
    if(cards.size!=selection.size): 
        return None
    trash = None
    maxDupe, dupeCard, numDupes = maxDupes(cards)
    
    if(maxDupe==1):
        combo = 'a'
        if(cards.size==1): return Play(cards, combo, trash)
        if(cards.size>=5 and not len(cards.find('Joker'))):
            for i in range(cards.size-1):
                if(not isConsecutive(cards[i], cards[i+1])):
                    return None
                combo+=chr(ord(combo[-1]) + 1)
            return Play(cards, combo, trash)
    
    if(maxDupe==2):
        combo = 'aa'
        if(cards.size==2): return Play(cards, combo, trash)
        if(cards.size>=6 and cards.size%numDupes==0 and not len(cards.find('Joker'))):
            for i in range(int(1.0*cards.size/2)-1):
                if(not isConsecutive(cards[i*2], cards[(i+1)*2])):
                    return None
                combo+=chr(ord(combo[-1]) + 1)*2
            return Play(cards, combo, trash)
    
    if(maxDupe==3 and not len(cards.find('Joker'))):
        leftovers = pd.Stack(cards=cards, sort=True, ranks=new_ranks)
        combo = 'aaa'
        tripples = []
        tripples.append(leftovers.get(dupeCard.value)[CARDS])
        for i in range(numDupes-1):
            maxDupe, dupeCard, numDupes = maxDupes(leftovers)
            tripples.append(leftovers.get(dupeCard.value)[CARDS])
            if(not isConsecutive(tripples[-1], tripples[-2])): return None
            combo+=chr(ord(combo[-1]) + 1)*3
        maxDupe, _, numTrash = maxDupes(leftovers)
        if(not leftovers.size):
            return Play(cards, combo, trash)
        if(numTrash==len(tripples)): 
            return Play(cards, combo, Trash(np.array([x.value for x in leftovers]), 'a'*maxDupe, numTrash))
        if(not numTrash): return Play(cards, combo, trash)
    
    if((maxDupe==4 and cards.size==4) or (maxDupe==1 and cards.size==2 and dupeCard.value=='Small')):
        return Play(cards, 'aaaa', trash)
    return None


def getCardPlays(hand, card, table_type):
    combos = np.array([])
    combo = np.array([card.value])
    for size in range(1, len(hand.find(card.value))+1):
        move = encodeSelection(hand, combo)
        if(move and move.card_type==table_type or not table_type): combos = np.append(combos, move)
        if(size==1):
            next = nextVal(card.value)
            chain = combo
            count = 1
            while(next and hand.find(next) and new_ranks['values'][next]<CAP):
                count+=1
                if(next): chain = np.append(chain, next)
                if(count>=5):
                    move = encodeSelection(hand, chain)
                    if(move and move.card_type==table_type or not table_type): combos = np.append(combos, move)
                next = nextVal(next)
        elif(size==2):
            next = nextVal(card.value)
            chain = combo
            count = 1
            while(next and hand.find(next) and new_ranks['values'][next]<CAP and len(hand.find(next))>=2):
                count+=1
                if(next): chain = np.append(chain, [next, next])
                if(count>=3):
                    move = encodeSelection(hand, chain)
                    if(move.card_type==table_type or not table_type): combos = np.append(combos, move)
                next = nextVal(next)
        elif(size==3):
            next = nextVal(card.value)
            chain = combo
            while(next and hand.find(next) and new_ranks['values'][next]<CAP and len(hand.find(next))>=3):
                if(next): chain = np.append(chain, [next, next, next])
                move = encodeSelection(hand, chain)
                if(move and move.card_type==table_type or not table_type): combos = np.append(combos, move)
                next = nextVal(next)
                
        if(card.value): combo = np.append(combo, card.value)
    return combos


def getAllPlays(hand, table_cards, table_type):
    plays = np.array([])
    prev = None
    for card in hand:
        if(not table_cards.size or card.gt(table_cards[0], new_ranks) and (not prev or prev.value!=card.value)):
            cardPlays = getCardPlays(hand, card, table_type)
            plays = np.concatenate((plays, cardPlays))
        prev = card
    return plays

def getAllTrash(hand, play):
    copy = pd.Stack(cards=hand, sort=True, ranks=new_ranks)
    copy.get_list([x.value for x in play.cards], sort=True, ranks=new_ranks)
    if(not play.trash): 
        return np.array([])
    possibleTrash = getAllPlays(copy, np.array([NULL]), play.trash.trash_type)
    return possibleTrash


def removeCards(hand, play):
    if not play:
        return np.array([])
    removed = np.array(hand.get_list(np.array([card.value for card in play.cards]), limit=1, sort=True, ranks=new_ranks))
    if(play.trash):
        removed = np.concatenate((removed, np.array(hand.get_list(np.array([card.value for card in play.trash.cards]), limit=1, sort=True, ranks=new_ranks))))
    return np.array([x.value for x in removed])

class Trash:
    def __init__(self, cards=np.array([]), trash_type=None, size=0):
        self.cards = np.array(cards)
        self.trash_type = trash_type
        self.size = size
        
    def __eq__(self, other):
        if other.trash_type==self.trash_type and other.size==self.size:
            return True
        return False
    
    def __str__(self):
        return f"{self.cards}, {self.trash_type}, {self.size}"


class Play:
    def __init__(self, cards=None, card_type=None, trash=Trash()):
        self.cards = cards
        self.card_type = card_type
        self.trash = trash
        
    def __gt__(self, other):
        if not other: return True
        if(self.card_type=='aaaa' and other.card_type!='aaaa'): return True
        if(self.card_type==other.card_type and self.trash==other.trash and self.cards[0].gt(other.cards[0], new_ranks)): return True
        return False
    
    def __add__(self, other):
        if not other:
            return self.cards
        return np.concatenate((self.cards, other.cards))
    
    def __eq__(self, other):
        return other and self.card_type==other.card_type

    def __str__(self):
        return f"{self.cards}, {self.card_type}, {self.trash}"