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
        if(not table.cards or not table.card_type): return True
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
    list = [c for c in selection if c]
    copy = pd.Stack(cards=hand, sort=True, ranks=new_ranks)
    cards = pd.Stack(cards=copy.get_list(list, limit=1), sort=True, ranks=new_ranks)
    if(cards.size!=len(list)): 
        return None
    trash = ('', 0)
    maxDupe, dupeCard, numDupes = maxDupes(cards)
    
    if(maxDupe==1):
        combo = 'a'
        if(cards.size==1): return Play(selection, combo, trash)
        if(cards.size>=5 and not len(cards.find('Joker'))):
            for i in range(cards.size-1):
                if(not isConsecutive(cards[i], cards[i+1])):
                    return None
                combo+=chr(ord(combo[-1]) + 1)
            return Play(selection, combo, trash)
    
    if(maxDupe==2):
        combo = 'aa'
        if(cards.size==2): return (selection, combo, trash)
        if(cards.size>=6 and cards.size%numDupes==0 and not len(cards.find('Joker'))):
            for i in range(int(1.0*cards.size/2)-1):
                if(not isConsecutive(cards[i*2], cards[(i+1)*2])):
                    return None
                combo+=chr(ord(combo[-1]) + 1)*2
            return Play(selection, combo, trash)
    
    if(maxDupe==3 and not len(cards.find('Joker'))):
        combo = 'aaa'
        tripples = []
        tripples.append(cards.get(dupeCard.value)[CARDS])
        for i in range(numDupes-1):
            maxDupe, dupeCard, numDupes = maxDupes(cards)
            tripples.append(cards.get(dupeCard.value)[CARDS])
            if(not isConsecutive(tripples[-1], tripples[-2])): return None
            combo+=chr(ord(combo[-1]) + 1)*3
        maxDupe, _, numTrash = maxDupes(cards)
        if(numTrash==len(tripples)): return Play(selection, combo, ('a'*maxDupe, numTrash))
        if(not numTrash): return Play(selection, combo, trash)
    
    if((maxDupe==4 and cards.size==4) or (maxDupe==1 and cards.size==2 and dupeCard.value=='Small')):
        return Play(selection, 'aaaa', trash)
    return None




def getCardPlays(hand, card, table_type):
    combos = np.array([])
    cap = new_ranks['values']['2']
    combo = card.value
    for size in range(1, len(hand.find(card.value))+1):
        move = encodeSelection(hand, combo)
        if(move.card_type==table_type): combos = np.append(combos, move)
        if(size==1):
            next = nextVal(card)
            chain = combo
            count = 1
            while(next and hand.find(next) and new_ranks['values'][next]<cap):
                count+=1
                chain = np.append(chain, next)
                if(count>=5):
                    move = encodeSelection(hand, chain)
                    if(move[1]==table_type): combos = np.append(combos, move)
                next = nextVal(next)
        elif(size==2):
            next = nextVal(card)
            chain = combo
            count = 1
            while(next and hand.find(next) and new_ranks['values'][next]<cap and len(hand.find(next))>=2):
                count+=1
                chain = np.append(chain, [next, next])
                if(count>=3):
                    move = encodeSelection(hand, chain)
                    if(move[1]==table_type): combos = np.append(combos, move)
                next = nextVal(next)
        elif(size==3):
            next = nextVal(card)
            chain = combo
            while(next and hand.find(next) and new_ranks['values'][next]<cap and len(hand.find(next))>=3):
                chain = np.append(chain, [next, next, next])
                move = encodeSelection(hand, chain)
                if(move[1]==table_type): combos = np.append(combos, move)
                next = nextVal(next)
                
        combo+=card.value
    return combos


# def getComboList(hand):
#     comboList = {}
#     if(hand.size==0): return comboList
#     prev = None
#     for card in hand:
#         curr = card.value
#         if(curr!=prev): comboList[curr] = getMoves(hand, curr)
#         prev = curr
#     return comboList


# def getTrash(hand, combo, trash, comboList):
#     totalTrash = ''
#     if(trash==''): return totalTrash
#     decode = trash.split(' ')
#     dupe, num = decode[0], int(decode[1])
#     copy = pd.Stack(cards=hand, sort=True, ranks=new_ranks)
#     copy.get_list(combo.split(" "), limit=1, sort=True, ranks=new_ranks)
#     if(dupe and num):
#         getTrash = getPlay(copy, NULL, dupe, '', comboList)
#         copy.get_list(getTrash.split(" "), limit=1, sort=True, ranks=new_ranks)
#         totalTrash+=getTrash
#         for _ in range(num-1):
#             getTrash = getPlay(copy, NULL, dupe, '', comboList)
#             if(getTrash==''): return None
#             copy.get_list(getTrash.split(" "), limit=1, sort=True, ranks=new_ranks)
#             totalTrash+=' '+getTrash
#     return totalTrash


# def getPlay(hand, card, type, trash, comboList):
#     if(not card and not type and not trash): 
#         combo = max(comboList[hand[0].value], key=len)
#         play = encodeCards(hand, combo)
#         if('aaa' in play[CARD_TYPE] and play[CARD_TYPE]!='aaaa'):
#             choice = rd.choice(['a', 'aa'])+' '+str(int(len(play[CARD_TYPE])/3))
#             newCombo = combo+' '+getTrash(hand, combo, choice, comboList)
#             if(encodeCards(hand, newCombo)): return newCombo
#         return combo
    
#     for curr in hand:
#         if(curr.gt(card, new_ranks)):
#             for combo in comboList[curr.value]:
#                 if(canPlay(encodeCards(hand, combo), card, type, '')):
#                     return combo+' '+getTrash(hand, combo, trash, comboList)
                
#     if(type!='aaaa'): return getPlay(hand, NULL, 'aaaa', '', comboList)
#     return ''


def getAllPlays(hand, table_cards, table_type):
    plays = np.array([])
    if(hand.size==0): return plays
    prev = None
    for card in hand:
        if(not table_cards or (new_ranks['values'][card.value]>new_ranks['values'][table_cards[0]] and (not prev or prev.value!=card.value))):
            plays = np.concatenate(plays, getCardPlays(hand, card, table_type))
        prev = card
    return plays

def getTrash(hand, play):
    copy = pd.Stack(cards=hand, sort=True, ranks=new_ranks)
    copy.get_list(play.cards, limit=1, sort=True, ranks=new_ranks)
    possibleTrash = getAllPlays(copy, ['Null'], play.trash[0])
    trash = Play()
    for _ in range(play.trash[1]):
        idx = np.random.randint(len(possibleTrash))
        trash+=possibleTrash[idx]
        possibleTrash = np.delete(possibleTrash, idx)
    return trash


def removeCards(hand, play):
    if not play or not hand: return None
    trash = getTrash(hand, play)
    return np.concatenate(np.array(hand.get_list(play.cards, limit=1, sort=True, ranks=new_ranks)), 
                          (np.array(hand.get_list(trash.cards, limit=1, sort=True, ranks=new_ranks))))


class Play:
    def __init__(self, cards=np.array([]), card_type=None, trash=None):
        self.cards = np.array(cards)
        self.card_type = card_type
        self.trash = trash
        
    def __gt__(self, other, ranks):
        if not other: return True
        if(self.card_type=='aaaa' and other.card_type!='aaaa'): return True
        if(self.card_type==other.card_type and self.trash_type==other.trash_type and ranks[self.cards[0]]>ranks[other.cards[0]]): return True
        return False
    
    def __add__(self, other):
        if not other:
            return self.cards
        return np.concatenate(self.cards, other.cards)

    def __str__(self):
        return f"{self.cards} {self.card_type} {self.trash_type}"
    
    # def __eq__(self, other):
    #     if len(self.cards)!=len(other.cards): return False
    #     if self.card_type!=other.card_type: return False
    #     if self.rtash!=other.trash: return False
    #     for i in range(len(self.cards)):
    #         if self.cards[i]!=other.cards[i]: return False