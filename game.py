import pydealer as pd
import random as rd
import time
from utils import *
from players import *


class Game:
    def __init__(self, player_1, player_2, player_3, delay=None):
        self.players = [player_1, player_2, player_3]
        self.delay = delay
        self.numGames = 1

    def start(self, seed):
        deck = pd.Deck(rebuild=True, re_shuffle=True, ranks=new_ranks)
        joker_big = pd.Card("Big", "Joker")
        joker_small = pd.Card("Small", "Joker")
        print("\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ GAME BEGIN $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
        play = (None, "")
        deck.add(joker_big)
        deck.add(joker_small)
        deck.shuffle()
        table = None
        
        
        player_turn = 0
        curr_player = None
        for i in range(len(self.players)):
            if(seed==i):
                self.players[i].hand.add(deck.deal(20))
                player_turn = i 
                curr_player = self.players[player_turn]
            else:
                self.players[i].hand.add(deck.deal(17))
            self.players[i].hand.sort(ranks=new_ranks)
            
        turn = 1
        winCondition = True
        
        print(f"GAME {self.numGames} ::: {self.players[seed].name} is the LANDLORD. {self.players[2].name} and {self.players[0].name} are the TENANTS. They must defeat the Landlord!\n")
        self.numGames+=1
        for player in self.players:
            print(f"{player.name}'s SCORE: {player.score}")
        while(winCondition):
            checkPrint = f"\n___________________________________________________________________________________________________________________________________________________________\n"
            for player in self.players:
                checkPrint+=f"{player.name} has {player.hand.size} cards left.        "
            print(checkPrint)
            while(True):
                play, win = self.playerSelection(curr_player, table)
                if(win): 
                    self.playerWon(player_turn, curr_player, seed)
                    return curr_player
                if(not play):
                    priority_turn = (player_turn-1) % len(self.players)
                    player_turn = (player_turn+1) % len(self.players)
                    curr_player = self.players[player_turn]
                    
                    play, win = self.playerSelection(curr_player, table)
                    if(win): 
                        self.playerWon(player_turn, curr_player, seed)
                        return curr_player
                    
                    if(not play):
                        if(curr_player.getEmpty()):
                            winCondition = False
                            break
                        player_turn = priority_turn
                        curr_player = self.players[player_turn]
                        table = None
                        break
                    else:
                        if(curr_player.getEmpty()):
                            winCondition = False
                            break
                        player_turn = (player_turn+1) % len(self.players)
                        curr_player = self.players[player_turn]
                        table = play
                else:
                    if(play.card_type=='aaaa'):
                        print("B O O O O O O O O O O O O O O O M M M M M M M M M M M M M M!")
                    table = play
                    player_turn = (player_turn+1) % len(self.players)
                    curr_player = self.players[player_turn]
            turn+=1
        
        
            
            
    def playerWon(self, player_turn, curr_player, seed):
        print(f"{curr_player.name} won!")
        for i in range(len(self.players)):
            player = self.players[i]
            if(player_turn==seed):
                if(i==player_turn):
                    player.score+=2
                else:
                    player.score-=1
            else:
                if(i!=seed):
                    player.score+=1
                else:
                    player.score-=2
            player.hand.empty()
        self.show()
    
    def playerSelection(self, curr_player, table):
        self.delayGame()
        print(f"{curr_player.name}'s turn.")
        play = curr_player.select(table)
        win = False
        if(curr_player.getEmpty()):
            win = True
        #admin commands ////////
        while(play and (play==SHOW or play==GIVE)):
            if(play==SHOW):
                self.show()
            if(play==GIVE):
                self.give(play.cards, play.trash)
            play = curr_player.select(table)
        #///////////////////////
        return play, win
    
    def give(self, player, cards):
        recipient = self.players[np.where(self.players.name==player)]
        recipient.hand.add(cards)
        
    def delayGame(self):
        if not self.delay:
            time.sleep(rd.randint(50,150)*1.0/100)
        else:
            time.sleep(self.delay)
        
    
    def show(self):
        for player in self.players:
            print(player)