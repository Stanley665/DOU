from utils import *

class Human:
    def __init__(self, name):
        self.hand = pd.Stack(sort=True, ranks=new_ranks)
        self.name = name
        self.score = 0
    

    def select(self, table):
        inp = input(f"Your turn: \n{self.hand} \nSelect cards or 'enter' to skip: ")
        if(inp=='' and table):
            print(f"{self.name} have skipped turn")
            return None
        #admin commands ///////////////////////////////////////////////////////////////////////////////////////////
        if(inp=="show"):
            return (None, "********")
        #//////////////////////////////////////////////////////////////////////////////////////////////////////////
        play = playCards(self.hand, inp)
        while ((table and not canPlay(play, table[CARD], table[CARD_TYPE], table[TRASH_TYPE])) or not play):
            inp = input("INVALID card! Try again: ")
            if(inp=='' and table):
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



        
class SimpleAI:
    def __init__(self, name):
        self.hand = pd.Stack(sort=True, ranks=new_ranks)
        self.name = name
        self.score = 0
        
        

    def select(self, table):
        if not table: 
            card, type, trash = None, None, None
        else:
            card, type, trash = table[CARD], table[CARD_TYPE], table[TRASH_TYPE]
        combo = getPlay(self.hand, card, type, trash, getComboList(self.hand))
        play = playCards(self.hand, combo)
        if(not play):
            print(f"{self.name} has skipped turn")
            return play
        message = ''
        for card in self.hand.get_list(combo.split(" "), limit=1, sort=True, ranks=new_ranks):
            message+=f"{card}, "
        print(f"{self.name} has played {message}")
        return play


    def getEmpty(self):
        return not self.hand.size