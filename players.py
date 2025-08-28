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
        play = encodeSelection(self.hand, inp)
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
            play = encodeSelection(self.hand, inp)
            
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
            table_cards, table_type, table_trash = ['Null'], None, None
        else:
            table_cards, table_type, table_trash = table[CARDS], table[CARD_TYPE], table[TRASH_TYPE]
            
        play = np.random.choice(getAllPlays(self.hand, table_cards, table_type))
        if('aaa' in play.card_type and not table): 
            play.trash = (rd.choice['', 'a', 'aa'], int(len(play.card_type)/3))
        removed = removeCards(self.hand, play)
        if not removed: 
            print(f"{self.name} has skipped turn")
            return None
        print(f"{self.name} has played {removed}")
        return play
        
        if table_trash: play.  getTrash(self.hand, table_trash, play)
        
        if not play:
            print(f"{self.name} has skipped turn")
            return None
        
        
        
        if not table: 
            card, type, trash = None, None, None
        else:
            card, type, trash = table[CARD], table[CARD_TYPE], table[TRASH_TYPE]
        combo = getPlay(self.hand, card, type, trash, getComboList(self.hand))
        play = playCards(self.hand, combo)
        
        message = ''
        for card in self.hand.get_list(combo.split(" "), limit=1, sort=True, ranks=new_ranks):
            message+=f"{card}, "
        print(f"{self.name} has played {message}")
        return play
    


    def getEmpty(self):
        return not self.hand.size
    
    def __str__(self):
        return f"\n{self.name} (simpleAI)\n{self.hand}\n"
    
# class SmartAI(SimpleAI):
#     def __init__(self, name):
#         super().__init__(name)

#     def select(self, table):