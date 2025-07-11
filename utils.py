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

def oneDiff(card1, card2):
    return abs(new_ranks["values"][card1.value]-new_ranks["values"][card2.value])==1

def nextVal(value):
    ranks = list(new_ranks['values'].keys())[::-1]
    try:
        idx = ranks.index(value)
        return ranks[idx+1]
    except (ValueError, IndexError):
        return None

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
    
    if(maxDupe==1 and cards.size>=5 and not len(cards.find('Joker'))):
        combo = 'a'
        for i in range(cards.size-1):
            if(not oneDiff(cards[i], cards[i+1])):
                return None
            combo+=chr(ord(combo[len(combo)-1]) + 1)
        return (cards[0], combo)
    
    if(maxDupe==2 and cards.size>=6 and cards.size%numDupes==0 and not len(cards.find('Joker'))):
        combo = 'aa'
        for i in range(int(1.0*cards.size/2)-1):
            if(not oneDiff(cards[i*2], cards[(i+1)*2])):
                return None
            combo+=chr(ord(combo[len(combo)-1]) + 1)+chr(ord(combo[len(combo)-1]) + 1)
        return (cards[0], combo)
    
    
    return None




class Human:
    def __init__(self, name):
        self.hand = pd.Stack(sort=True, ranks=new_ranks)
        self.name = name
    
    def select(self, table):
        inp = input(f"Your turn: \n{self.hand} \nSelect cards or 'space' to skip: ")
        if(inp=='space' or inp==" "):
            play = None
            print(f"{self.name} have skipped turn")
            
        #admin commands ////////
        elif(inp=="show"):
            return (None, "********")
        #///////////////////////
        
        else:
            play = playCards(self.hand, inp)
            while (not play or (table and play[0].le(table[0], new_ranks))):
                inp = input("INVALID card! Try again: ")
                if(inp=='space' or inp==" "):
                    play = None
                    print(f"{self.name} have skipped turn")
                    break
                play = playCards(self.hand, inp)
                
            message = ''
            for card in self.hand.get_list(inp.split(" "), limit=1, sort=True, ranks=new_ranks):
                message+=f"{card}, "
            print(f"\n{self.name} have played: {message}")
            return play
    
    def getEmpty(self):
        return not self.hand.size



        
class simpleAI:
    def __init__(self, name,):
        self.hand = pd.Stack(sort=True, ranks=new_ranks)
        self.name = name
    
    def select(self, table):
        combo = ''
        play = None
        if(not table):
            combo = rd.choice(self.getCombos(self.hand[0].value))
            play = playCards(self.hand, combo)
        else:
            i = 0
            while(i<self.hand.size-1):
                curr = self.hand[i]
                if(curr.gt(table[0], new_ranks)):
                    combos = self.getCombos(curr.value)
                    for combo in combos:
                        if(playCards(self.hand, combo)[1]==table[1]):
                            play = playCards(self.hand, combo)
                            break
                    break
                i+=1
        
        if(not play):
            print(f"{self.name} has skipped turn")
        else:
            message = ''
            for card in self.hand.get_list(combo.split(" "), limit=1, sort=True, ranks=new_ranks):
                message+=f"{card}, "
            print(f"{self.name} has played {message}")
        return play
    
    def getEmpty(self):
        return not self.hand.size
    
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
                while(self.hand.find(next) and new_ranks['values'][next]<cap):
                    count+=1
                    chain+=" "+next
                    if(count>=5):
                        combos.append(chain)
                    next = nextVal(next)
            elif(j==1):
                next = nextVal(card)
                chain = combo
                count = 1
                while(self.hand.find(next) and new_ranks['values'][next]<cap and len(self.hand.find(next))>=2):
                    count+=1
                    chain+=" "+next+" "+next
                    if(count>=3):
                        combos.append(chain)
                    next = nextVal(next)
            elif(j==2):
                next = nextVal(card)
                chain = combo
                while(self.hand.find(next) and new_ranks['values'][next]<cap and len(self.hand.find(next))>=3):
                    chain+=" "+next+" "+next+" "+next
                    combos.append(chain)
                    next = nextVal(next)
                    
            combo+=" "+card
        
        return combos
        