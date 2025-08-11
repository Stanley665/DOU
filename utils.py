import pydealer as pd
import random as rd
import numpy as np

CARD = 0
CARD_TYPE = 1
TRASH_TYPE = 2

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


def maxDupes(cards):
    copy = pd.Stack(cards=cards, sort=True, ranks=new_ranks)
    copy.sort()
    maxDupe = 0
    dupeCard = None
    numDupes = 0
    while(copy.size):
        dupeSize = len(copy.find(copy[CARD].value))
        if(maxDupe<dupeSize): 
            maxDupe = dupeSize
            dupeCard = copy[0]
            numDupes = 1
        elif(maxDupe==dupeSize):
            numDupes+=1
        copy.get(copy[CARD].value)
    return (maxDupe, dupeCard, numDupes)
        
    
def playCards(hand, choice):
    list = [c for c in choice.split(" ") if c]
    copy = pd.Stack(cards=hand, sort=True, ranks=new_ranks)
    cards = pd.Stack(cards=copy.get_list(list, limit=1), sort=True, ranks=new_ranks)
    if(cards.size!=len(list)): 
        return None
    trash = ''
    maxDupe, dupeCard, numDupes = maxDupes(cards)
    
    if(maxDupe==1):
        combo = 'a'
        if(cards.size==1): return (cards[CARD], combo, trash)
        if(cards.size>=5 and not len(cards.find('Joker'))):
            for i in range(cards.size-1):
                if(not isConsecutive(cards[i], cards[i+1])):
                    return None
                combo+=chr(ord(combo[-1]) + 1)
            return (cards[CARD], combo, trash)
    
    if(maxDupe==2):
        combo = 'aa'
        if(cards.size==2): return (cards[CARD], combo, trash)
        if(cards.size>=6 and cards.size%numDupes==0 and not len(cards.find('Joker'))):
            for i in range(int(1.0*cards.size/2)-1):
                if(not isConsecutive(cards[i*2], cards[(i+1)*2])):
                    return None
                combo+=chr(ord(combo[-1]) + 1)*2
            return (cards[CARD], combo, trash)
    
    if(maxDupe==3 and not len(cards.find('Joker'))):
        combo = 'aaa'
        card = dupeCard
        tripples = []
        tripples.append(cards.get(dupeCard.value)[CARD])
        for i in range(numDupes-1):
            maxDupe, dupeCard, numDupes = maxDupes(cards)
            tripples.append(cards.get(dupeCard.value)[CARD])
            if(not isConsecutive(tripples[-1], tripples[-2])): return None
            combo+=chr(ord(combo[-1]) + 1)*3
        maxDupe, trashCard, numTrash = maxDupes(cards)
        if(numTrash==len(tripples)): return (card, combo, 'a'*maxDupe+' '+str(numTrash))
        if(not numTrash): return (card, combo, trash)
    
    if((maxDupe==4 and cards.size==4) or (maxDupe==1 and cards.size==2 and dupeCard.value=='Small')):
        return (dupeCard, 'aaaa', trash)
    return None


def canPlay(play, card, combo, trash):
    if(play):
        if(play[CARD_TYPE]=='aaaa' and combo!='aaaa'): return True
        if(play[CARD_TYPE]==combo and play[TRASH_TYPE]==trash and play[CARD].gt(card, new_ranks)): return True
    return False


def getCombos(hand, value):
    combos = np.array([])
    cap = new_ranks['values']['2']
    combo = value
    for j in range(len(hand.find(value))):
        combos = np.append(combos, combo)
        if(j==0):
            next = nextVal(value)
            chain = combo
            count = 1
            while(next and hand.find(next) and new_ranks['values'][next]<cap):
                count+=1
                chain+=" "+next
                if(count>=5):
                    combos = np.append(combos, chain)
                next = nextVal(next)
        elif(j==1):
            next = nextVal(value)
            chain = combo
            count = 1
            while(next and hand.find(next) and new_ranks['values'][next]<cap and len(hand.find(next))>=2):
                count+=1
                chain+=" "+next+" "+next
                if(count>=3):
                    combos = np.append(combos, chain)
                next = nextVal(next)
        elif(j==2):
            next = nextVal(value)
            chain = combo
            while(next and hand.find(next) and new_ranks['values'][next]<cap and len(hand.find(next))>=3):
                chain+=" "+next+" "+next+" "+next
                combos = np.append(combos, chain)
                next = nextVal(next)
                
        combo+=" "+value
    return combos


def getComboList(hand):
    comboList = {}
    if(hand.size==0): return comboList
    prev = None
    for card in hand:
        curr = card.value
        if(curr!=prev): comboList[curr] = getCombos(hand, curr)
        prev = curr
    return comboList


def getTrash(hand, combo, trash, comboList):
    totalTrash = ''
    if(trash==''): return totalTrash
    decode = trash.split(' ')
    dupe, num = decode[0], int(decode[1])
    copy = pd.Stack(cards=hand, sort=True, ranks=new_ranks)
    copy.get_list(combo.split(" "), limit=1, sort=True, ranks=new_ranks)
    if(dupe and num):
        getTrash = getPlay(copy, NULL, dupe, '', comboList)
        copy.get_list(getTrash.split(" "), limit=1, sort=True, ranks=new_ranks)
        totalTrash+=getTrash
        for i in range(num-1):
            getTrash = getPlay(copy, NULL, dupe, '', comboList)
            if(getTrash==''): return None
            copy.get_list(getTrash.split(" "), limit=1, sort=True, ranks=new_ranks)
            totalTrash+=' '+getTrash
    return totalTrash


def getPlay(hand, card, type, trash, comboList):
    if(not card and not type and not trash): 
        combo = max(comboList[hand[0].value], key=len)
        play = playCards(hand, combo)
        if('aaa' in play[CARD_TYPE] and play[CARD_TYPE]!='aaaa'):
            choice = rd.choice(['a', 'aa'])+' '+str(int(len(play[CARD_TYPE])/3))
            newCombo = combo+' '+getTrash(hand, combo, choice, comboList)
            if(playCards(hand, newCombo)): return newCombo
        return combo
    
    for curr in hand:
        if(curr.gt(card, new_ranks)):
            for combo in comboList[curr.value]:
                if(canPlay(playCards(hand, combo), card, type, '')):
                    return combo+' '+getTrash(hand, combo, trash, comboList)
                
    if(type!='aaaa'): return getPlay(hand, NULL, 'aaaa', '', comboList)
    return ''