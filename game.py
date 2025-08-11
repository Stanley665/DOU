import pydealer as pd
import random as rd
import time
from utils import *
from players import Human, SimpleAI


class Game:
    def __init__(self, player_1, player_2, player_3, delay=0):
        self.players = [player_1, player_2, player_3]
        self.delay = delay

    def start(self):
        deck = pd.Deck(rebuild=True, re_shuffle=True, ranks=new_ranks)
        joker_big = pd.Card("Big", "Joker")
        joker_small = pd.Card("Small", "Joker")
        # while(input("Any key to play. 'q' to quit.")!='q'):
        while(True):
            print("\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ GAME BEGIN $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
            play = (None, "")
            seed = rd.randint(0, 2)
            deck.empty()
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
            
            print(f"{self.players[seed].name} is the LANDLORD. {self.players[2].name} and {self.players[0].name} are the TENANTS. They must defeat the Landlord!\n")
            for player in self.players:
                print(f"{self.players[1].name}'s SCORE: {self.players[1].score}")
            while(winCondition):

                print(f"\n\nTurn {turn}")
                
                while(True):
                    time.sleep(self.delay)
                    print(f"{curr_player.name}'s turn.")
                    if(type(curr_player)==Human):
                        print(f"\n___________________________________________________________________________________________________________________________________________________________")
                        print(f"\nTurn {turn}:        p1 has {self.players[1].hand.size} cards left.        p2 has {self.players[2].hand.size} cards left.      You have {self.players[0].hand.size} cards left.")
                    
                    play = curr_player.select(table)
                    if(curr_player.getEmpty()):
                        winCondition = False
                        break
                    #admin commands ////////
                    while(play and play[1]=="********"):
                        self.show()
                        play = curr_player.select(table)
                    #///////////////////////
                    
                    if(not play):
                        priority_turn = (player_turn-1) % len(self.players)
                        player_turn = (player_turn+1) % len(self.players)
                        curr_player = self.players[player_turn]
                        time.sleep(self.delay)
                        print(f"{curr_player.name}'s turn.")
                        if(type(curr_player)==Human):
                            print(f"\n___________________________________________________________________________________________________________________________________________________________")
                            print(f"\nTurn {turn}:        p1 has {self.players[1].hand.size} cards left.        p2 has {self.players[2].hand.size} cards left.      You have {self.players[0].hand.size} cards left.")
                        play = curr_player.select(table)
                        if(curr_player.getEmpty()):
                            winCondition = False
                            break
                        #admin commands ////////
                        while(play and play[1]=="********"):
                            self.show()
                            play = curr_player.select(table)
                        #///////////////////////
                        
                        
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
                        if(play[CARD_TYPE]=='aaaa'):
                            print("B O O O O O O O O O O O O O O O M M M M M M M M M M M M M M!")
                        table = play
                        player_turn = (player_turn+1) % len(self.players)
                        curr_player = self.players[player_turn]
                turn+=1
            
            print(f"{curr_player.name} won!")
            curr_player.score+=1*2**(player_turn==seed)
            for player in self.players:
                player.hand.empty()
            deck.empty()
            
    def show(self):
        for player in self.players:
            if(type(player)!=Human):
                print(player)