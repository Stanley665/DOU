import pydealer as pd
import random as rd

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
        "3": 1
    },
    "suits" : {
        "Joker": 1,
        "Spades": 0,
        "Hearts": 0,
        "Clubs": 0,
        "Diamonds": 0
    }
}

combos = ['a', 'aa', 'aaa', 'aaab', 'aaabb', 'aaaa', 'aabbcc', 'aaabbb', 'aaabbbcd', 'aaabbbccdd']

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
        
    maxDupe, dupeCard, numDupes = maxDupes(cards)
    
    if(maxDupe==1):
        combo = 'a'
        if(cards.size==1): return (cards[0], combo)
        if(cards.size>=5 and not len(cards.find('Joker'))):
            for i in range(cards.size-1):
                if(not isConsecutive(cards[i], cards[i+1])):
                    return None
                combo+=chr(ord(combo[-1]) + 1)
            return (cards[0], combo)
    
    if(maxDupe==2):
        combo = 'aa'
        if(cards.size==2): return (cards[0], combo)
        if(cards.size>=6 and cards.size%numDupes==0 and not len(cards.find('Joker'))):
            for i in range(int(1.0*cards.size/2)-1):
                if(not isConsecutive(cards[i*2], cards[(i+1)*2])):
                    return None
                combo+=chr(ord(combo[len(combo)-1]) + 1)*2
            return (cards[0], combo)
    
    if(maxDupe==3 and not len(cards.find('Joker'))):
        combo = 'aaa'
        card = dupeCard
        tripples = []
        tripples.append(cards.get(dupeCard.value)[0])
        for i in range(numDupes-1):
            maxDupe, dupeCard, numDupes = maxDupes(cards)
            tripples.append(cards.get(dupeCard.value)[0])
            if(not isConsecutive(tripples[-1], tripples[-2])): return None
            combo+=chr(ord(combo[-1]) + 1)*3
        maxDupe, dupeCard, numDupes = maxDupes(cards)
        if(numDupes==len(tripples)):
            if(maxDupe==1):
                for i in range(len(tripples)):
                    combo+=chr(ord(combo[-1])+1)
                return (card, combo)
            elif(maxDupe==2):
                for i in range(len(tripples)):
                    combo+=chr(ord(combo[-1])+1)*2
                return (card, combo)
        elif(not cards.size): return (card, combo)
    
    if(maxDupe==4 and cards.size==4):
        return (dupeCard, 'aaaa')
    return None



def canPlay(play, table):
    if(play):
        if(not table): return True
        if(play[1]=='aaaa' and table[1]!='aaaa'): return True
        if(play[1]==table[1] and play[0].gt(table[0], new_ranks)): return True
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
            
        #admin commands ////////
        if(inp=="show"):
            return (None, "********")
        #///////////////////////
        
        play = playCards(self.hand, inp)
        while (not canPlay(play, table)):
            inp = input("INVALID card! Try again: ")
            if(inp=='' or inp==" "):
                play = None
                print(f"{self.name} have skipped turn")
                break
            
            #admin commands ////////
            elif(inp=="show"):
                return (None, "********")
            #///////////////////////
            
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
        combo = self.getCombo(table)
        play = playCards(self.hand, combo)
        if(not play):
            print(f"{self.name} has skipped turn")
            return play
        message = ''
        for card in self.hand.get_list(combo.split(" "), limit=1, sort=True, ranks=new_ranks):
            message+=f"{card}, "
        print(f"{self.name} has played {message}")
        return play
    
    def getSimpleCombo(self, hand, combo):
        combo = "aa"
        hand = copy wihout duplicates
        comboList = sorted([self.getCombos(card.value) for card in hand if not any('aaaa' in playCards(self.hand, c) for c in self.getCombos(card.value)) or not not any('2' in c for c in self.getCombos(card.value))], key=len)
        if(len(trash[0])==2): comboList = [arr for arr in comboList if len(arr)>=2]
        
        
         
    
    def getCombo(self, table):
        if(not table):
            idx = 0
            combos = self.getCombos(self.hand[idx].value)
            while(any('aaaa' in playCards(self.hand(combo)) for combo in combos)):
                idx+=1
                combos = self.getCombos(self.hand[idx].value)
            print(combos)
            return max(combos, key=len)
        
        i = 0
        while(i<self.hand.size):
            curr = self.hand[i]
            if(curr.gt(table[0], new_ranks)):
                combos = self.getCombos(curr.value)
                if(not any('aaaa' in combo for combo in combos)):
                    triplets, trash = self.getTrash(table)
                    print(f'tripplets: {triplets}, trash: {trash}')
                    for combo in combos:
                        if(playCards(self.hand, combo)[1]==table[1] or playCards(self.hand, combo)[1]==triplets):                   
                            if(trash):
                                add = self.addTrash(combo, trash)
                                print(f'trash: {trash}, add: {add}')
                                combo+=add
                            return combo
            i+=1
            
        if(table[1]!='aaaa'):
            i = 0
            while(combo=='' and i<self.hand.size):
                curr = self.hand[i]
                combos = self.getCombos(curr.value)
                for combo in combos:
                    if(playCards(self.hand, combo)=='aaaa'):
                        print(combos)
                        return combo
                i+=1
        return ''
    
    def getEmpty(self):
        return not self.hand.size
    
    def getTrash(self, table):
        trash = []
        triplets = table[1]
        if('aaa' in triplets):
            while(triplets[-3]!=triplets[-1]):
                if(triplets[-2]==triplets[-1]):
                    trash.append('aa')
                    triplets = triplets[:-2]
                else:
                    trash.append('a')
                    triplets = triplets[:-1]
        return triplets, trash
    
    def addTrash(self, combo, trash):
        totalTrash = ''
        copy = pd.Stack(cards=self.hand, sort=True, ranks=new_ranks)
        copy.get_list(combo.split(" ")+['2', 'Small', 'Big'], sort=True, ranks=new_ranks)
        for curr in trash:
            totalTrash += ' '+self.getSimpleCombo(copy, curr)
        return totalTrash
            
            
            
            
            val = None
            i = 0
            while(not val and i < len(comboList)):
                j = 0
                arr = comboList[i]
                    while(not val and i < len(arr)):
                        if(playCards(copy, val))
                    j+=1
                i+=1
            
            
            for arr in comboList:
                if(any(playCards(copy, c)[1]==curr for c in arr)):
                    val = arr[0][0]
                    break
            copy.get_list(combo.split(" "), limit=1, sort=True, ranks=new_ranks)
            comboList = sorted([self.getCombos(card.value) for card in copy if not any('aaaa' in c for c in self.getCombos(card.value))], key=len)
        
        
        
        
        while(trash!=''):
            removed = 'a'
            trash = trash[:-1]
            if(trash!='' and trash[-1]==removed):
                trash = trash[:-1]
                removed+='a'
            add = ''
            i = 0
            while(add=='' and i < len(comboList)):
                j = 0
                while(add=='' and j < len(comboList[i])):
                    c = comboList[i][j]
                    if(playCards(c)[1]==removed):
                        add = c
                    j+=1
                i+=1
            totalTrash+= ' '+add
        return totalTrash
    
    def getCombos(self, card):
        combos = []
        cap = new_ranks['values']['2']
        combo = card
        for j in range(len(self.hand.find(card))):
            combos.append(combo)
            if(j==0):
                next = nextVal(card)
                chain = combo
                count = 1
                while(next and self.hand.find(next) and new_ranks['values'][next]<cap):
                    count+=1
                    chain+=" "+next
                    if(count>=5):
                        combos.append(chain)
                    next = nextVal(next)
            elif(j==1):
                next = nextVal(card)
                chain = combo
                count = 1
                while(next and self.hand.find(next) and new_ranks['values'][next]<cap and len(self.hand.find(next))>=2):
                    count+=1
                    chain+=" "+next+" "+next
                    if(count>=3):
                        combos.append(chain)
                    next = nextVal(next)
            elif(j==2):
                next = nextVal(card)
                chain = combo
                while(next and self.hand.find(next) and new_ranks['values'][next]<cap and len(self.hand.find(next))>=3):
                    chain+=" "+next+" "+next+" "+next
                    combos.append(chain)
                    next = nextVal(next)
                    
            combo+=" "+card
        return combos