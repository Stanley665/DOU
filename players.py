from utils import *


SKIP = Play(None, "SKIP", None)
SHOW = Play(None, "SHOW", None)
GIVE = Play(None, "GIVE", None)

class Human:
    def __init__(self, name):
        self.hand = pd.Stack(sort=True, ranks=new_ranks)
        self.name = name
        self.score = 0
    

    def select(self, table):
        print(f"Your turn: \n{self.hand} \nSelect cards or 'enter' to skip: ")
        play = self.getPlay(table)
        while (play!=SKIP and play!=SHOW and play!=GIVE and ((table and not canPlay(play, table)) or not play)):
            print("INVALID cards! Try again: ")
            play = self.getPlay(table)
        if(play==SKIP):
            print(f"{self.name} has skipped turn\n")
            return None
        if(play==GIVE):
            print()
            return play
            
        message = ''
        for card in self.hand.get_list([x.value for x in play.cards], limit=1, sort=True, ranks=new_ranks):
            message+=f"{card}, "
        print(f"\n{self.name} have played: {message}\n")
        return play
    
    
    def getPlay(self, table):
        inp = input()
        play = encodeSelection(self.hand, np.array(inp.split(" ")))
        if(inp=='' and table):
            return SKIP
        #admin commands ///////////////////////////////////////////////////////////////////////////////////////////
        if(inp=="show"):
            return Play(None, "********", None)
        if("give" in inp[:4].lower()):
            arr = inp[4:].split(" ")
            Player = arr[0]
            return Play(
                            pd.Stack(np.array([pd.Card(x, "Clubs") for x in arr[1:]]), sort=True, ranks=new_ranks), 
                            "GIVE", 
                            None
                        )
        #//////////////////////////////////////////////////////////////////////////////////////////////////////////
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
            table_cards, table_type, table_trash = np.array([NULL]), None, None
        else:
            table_cards, table_type, table_trash = table.cards, table.card_type, table.trash
            
        allPlays = getAllPlays(self.hand, table_cards, table_type)
        if(allPlays.size):
            play = max(allPlays, key=lambda x: len(x.cards))
        else:
            play = None
        
        if (play): play.trash = self.getTrash(play, table, table_trash)
        
        removed = removeCards(self.hand, play)
        if not removed.size: 
            print(f"{self.name} has skipped turn")
            return None
        print(f"{self.name} has played {removed}")
        print(f"{self.name} has {self.hand.size} cards.\n")
        return play

    
    def getTrash(self, play, table, table_trash):
        trash = None
        if(play and 'aaa' in play.card_type and play.card_type!='aaaa'):
            num_trash = int(len(play.card_type)/3)
            if(not table):
                trash = Trash(np.array([]), 'aa', num_trash)
                allTrash = getAllTrash(self.hand, play)
                
                if(len(allTrash)<num_trash):
                    trash = Trash(np.array([]), 'a', num_trash)
                    allTrash = getAllTrash(self.hand, play)
                    
                if(len(allTrash)<num_trash):
                    trash = None
            else:
                trash = table_trash
                allTrash = getAllTrash(self.hand, play)
                if(table_trash and len(allTrash)<num_trash):
                    play = None
            
            if(play and trash):
                trash.cards = np.array([])
                for _ in range(trash.size):
                    idx = rd.randint(0, len(allTrash)-1)
                    trash.cards = np.append(trash.cards, allTrash[idx].cards)
                    allTrash = np.delete(allTrash, idx)
        return trash


    def getEmpty(self):
        return not self.hand.size
    
    
    def __str__(self):
        return f"\n{self.name} (simpleAI)\n{self.hand}\n"
    
    
    
    
    
# class SmartAI(SimpleAI):
#     def __init__(self, name):
#         super().__init__(name)

#     def select(self, table):