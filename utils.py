import pydealer as pd
import random as rd

CARD_VALUE = 0
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
        dupeSize = len(copy.find(copy[CARD_VALUE].value))
        if(maxDupe<dupeSize): 
            maxDupe = dupeSize
            dupeCard = copy[0]
            numDupes = 1
        elif(maxDupe==dupeSize):
            numDupes+=1
        copy.get(copy[CARD_VALUE].value)
    return (maxDupe, dupeCard, numDupes)
        
    
def playCards(hand, choice):
    list = choice.split(" ")
    copy = pd.Stack(cards=hand, sort=True, ranks=new_ranks)
    if(len(copy.find_list(list, limit=1))!=len(list)):
        return None
    cards = pd.Stack(cards=copy.get_list(list, limit=1), sort=True, ranks=new_ranks)
    trash = '0 0'
    maxDupe, dupeCard, numDupes = maxDupes(cards)
    
    if(maxDupe==1):
        combo = 'a'
        if(cards.size==1): return (cards[CARD_VALUE], combo, trash)
        if(cards.size>=5 and not len(cards.find('Joker'))):
            for i in range(cards.size-1):
                if(not isConsecutive(cards[i], cards[i+1])):
                    return None
                combo+=chr(ord(combo[-1]) + 1)
            return (cards[CARD_VALUE], combo, trash)
    
    if(maxDupe==2):
        combo = 'aa'
        if(cards.size==2): return (cards[CARD_VALUE], combo, trash)
        if(cards.size>=6 and cards.size%numDupes==0 and not len(cards.find('Joker'))):
            for i in range(int(1.0*cards.size/2)-1):
                if(not isConsecutive(cards[i*2], cards[(i+1)*2])):
                    return None
                combo+=chr(ord(combo[-1]) + 1)*2
            return (cards[CARD_VALUE], combo, trash)
    
    if(maxDupe==3 and not len(cards.find('Joker'))):
        combo = 'aaa'
        card = dupeCard
        tripples = []
        tripples.append(cards.get(dupeCard.value)[CARD_VALUE])
        for i in range(numDupes-1):
            maxDupe, dupeCard, numDupes = maxDupes(cards)
            tripples.append(cards.get(dupeCard.value)[CARD_VALUE])
            if(not isConsecutive(tripples[-1], tripples[-2])): return None
            combo+=chr(ord(combo[-1]) + 1)*3
        maxDupe, dupeCard, numDupes = maxDupes(cards)
        if(numDupes==len(tripples)): return (card, combo, 'a'*maxDupe+' '+str(numDupes))
    
    if(maxDupe==4 and cards.size==4):
        return (dupeCard, 'aaaa', trash)
    return None


def canPlay(play, table):
    if(play):
        if(not table): return True
        if(play[CARD_TYPE]=='aaaa' and table[CARD_TYPE]!='aaaa'): return True
        if(play[CARD_TYPE]==table[CARD_TYPE] and play[CARD_VALUE].gt(table[CARD_VALUE], new_ranks)): return True
    return False




class Human:
    def __init__(self, name):
        self.hand = pd.Stack(sort=True, ranks=new_ranks)
        self.name = name
    

    def select(self, table):
        inp = input(f"Your turn: \n{self.hand} \nSelect cards or 'enter' to skip: ")
        if(inp=='' or inp==" "):
            print(f"{self.name} have skipped turn")
            return None
        #admin commands ///////////////////////////////////////////////////////////////////////////////////////////
        if(inp=="show"):
            return (None, "********")
        #//////////////////////////////////////////////////////////////////////////////////////////////////////////
        play = playCards(self.hand, inp)
        while (not canPlay(play, table)):
            inp = input("INVALID card! Try again: ")
            if(inp=='' or inp==" "):
                play = None
                print(f"{self.name} have skipped turn")
                break
            #admin commands ///////////////////////////////////////////////////////////////////////////////////////
            elif(inp=="show"):
                return (None, "********")
            #//////////////////////////////////////////////////////////////////////////////////////////////////////
            play = playCards(self.hand, inp)
            
        message = ''
        for card in self.hand.get_list(inp.split(" "), limit=1, sort=True, ranks=new_ranks):
            message+=f"{card}, "
        print(f"\n{self.name} have played: {message}")
        return play
    

    def getEmpty(self):
        return not self.hand.size



        
class simpleAI:
    def __init__(self, name):
        self.hand = pd.Stack(sort=True, ranks=new_ranks)
        self.name = name
    

    def select(self, table):
        if(not table):
            idx = 0
            while(any('aaaa'==combo[CARD_TYPE] for combo in comboList)):
                comboList = self.getComboList(self.hand[idx].value)
                idx+=1
            print(comboList)
            combo = max(comboList, key=len)
        else:
            combo = self.getCombo(table[CARD_VALUE], table[CARD_TYPE], table[TRASH_TYPE])
        if(combo=='' and table[CARD_TYPE]!='aaaa'): combo = self.getCombo(NULL, 'aaaa', '')
        play = playCards(self.hand, combo)

        if(not play):
            print(f"{self.name} has skipped turn")
            return play
        
        message = ''
        for card in self.hand.get_list(combo.split(" "), limit=1, sort=True, ranks=new_ranks):
            message+=f"{card}, "
        print(f"{self.name} has played {message}")
        return play
    

    def getCombo(self, value, type, trash):
        for card in self.hand:
            if(card.gt(value, new_ranks)):
                comboList = self.getComboList(card.value)
                for combo in comboList:
                    if(playCards(self.hand, combo)[CARD_TYPE]==type and (type=='aaaa' or not any('aaaa'==c[CARD_TYPE] for c in comboList))):
                        totalTrash = self.getTrash(combo, trash)
                        if(totalTrash): return combo+totalTrash
        return ''
    

    def getEmpty(self):
        return not self.hand.size
    

    def getTrash(self, combo, trash):
        totalTrash = ''
        decode = trash.split(' ')
        dupe, num = decode[0], int(decode[1])
        copy = pd.Stack(cards=self.hand, sort=True, ranks=new_ranks)
        copy.get_list(combo.split(" "), limit=1, sort=True, ranks=new_ranks)
        
        if(dupe and num):
            getTrash = self.getTrash(NULL, dupe, '')
            copy.get_list(getTrash.split(" "), limit=1, sort=True, ranks=new_ranks)
            totalTrash+=getTrash
            for i in range(num-1):
                getTrash = self.getTrash(NULL, dupe, '')
                if(getTrash==''): return None
                copy.get_list(getTrash.split(" "), limit=1, sort=True, ranks=new_ranks)
                totalTrash+=' '+getTrash
        return totalTrash
    

    def getComboList(self, card):
        comboList = []
        cap = new_ranks['values']['2']
        combo = card
        for j in range(len(self.hand.find(card))):
            comboList.append(combo)
            if(j==0):
                next = nextVal(card)
                chain = combo
                count = 1
                while(next and self.hand.find(next) and new_ranks['values'][next]<cap):
                    count+=1
                    chain+=" "+next
                    if(count>=5):
                        comboList.append(chain)
                    next = nextVal(next)
            elif(j==1):
                next = nextVal(card)
                chain = combo
                count = 1
                while(next and self.hand.find(next) and new_ranks['values'][next]<cap and len(self.hand.find(next))>=2):
                    count+=1
                    chain+=" "+next+" "+next
                    if(count>=3):
                        comboList.append(chain)
                    next = nextVal(next)
            elif(j==2):
                next = nextVal(card)
                chain = combo
                while(next and self.hand.find(next) and new_ranks['values'][next]<cap and len(self.hand.find(next))>=3):
                    chain+=" "+next+" "+next+" "+next
                    comboList.append(chain)
                    next = nextVal(next)
                    
            combo+=" "+card
        return comboList