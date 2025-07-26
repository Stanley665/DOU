import pydealer as pd
import random as rd
import time
from utils import new_ranks, Human, simpleAI

def show(arr):
    for player in arr:
        if(type(player)!=Human):
            print()
            print(player.name)
            print()
            print(player.hand)
            print("\n")
        
    

if __name__ == '__main__':
    deck = pd.Deck(rebuild=True, re_shuffle=True, ranks=new_ranks)
    joker_big = pd.Card("Big", "Joker")
    joker_small = pd.Card("Small", "Joker")
    deck.add(joker_big)
    deck.add(joker_small)

    # while(input("Any key to play. 'q' to quit.")!='q'):
    while(True):
        print("\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ GAME BEGIN $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
        play = (None, "")
        seed = rd.randint(0, 2)
        deck.shuffle()
        table = None
        players = [Human("You"), simpleAI("P1"), simpleAI("P2")]
        player_turn = 0
        curr_player = None
        for i in range(len(players)):
            if(seed==i):
                players[i].hand.add(deck.deal(20))
                player_turn = i 
                curr_player = players[player_turn]
            else:
                players[i].hand.add(deck.deal(17))
            players[i].hand.sort(ranks=new_ranks)
            
        turn = 1
        winCondition = True
        
        while(winCondition):
            print(f"\n\nTurn {turn}")
            while(True):
                time.sleep(1)
                print(f"{curr_player.name}'s turn.")
                if(type(curr_player)==Human):
                    print(f"\n___________________________________________________________________________________________________________________________________________________________")
                    print(f"\nTurn {turn}:        p1 has {players[1].hand.size} cards left.        p2 has {players[2].hand.size} cards left.      You have {players[0].hand.size} cards left.")
                
                play = curr_player.select(table)
                
                #admin commands ////////
                while(play and play[1]=="********"):
                    show(players)
                    play = curr_player.select(table)
                #///////////////////////
                
                if(not play):
                    priority_turn = (player_turn-1) % len(players)
                    player_turn = (player_turn+1) % len(players)
                    curr_player = players[player_turn]
                    time.sleep(1)
                    print(f"{curr_player.name}'s turn.")
                    if(type(curr_player)==Human):
                        print(f"\n___________________________________________________________________________________________________________________________________________________________")
                        print(f"\nTurn {turn}:        p1 has {players[1].hand.size} cards left.        p2 has {players[2].hand.size} cards left.      You have {players[0].hand.size} cards left.")
                    play = curr_player.select(table)
                    
                    #admin commands ////////
                    while(play and play[1]=="********"):
                        show(players)
                        play = curr_player.select(table)
                    #///////////////////////
                    
                    
                    if(not play):
                        player_turn = priority_turn
                        curr_player = players[player_turn]
                        table = None
                        break
                    else:
                        player_turn = (player_turn+1) % len(players)
                        curr_player = players[player_turn]
                        table = play
                        if(curr_player.getEmpty()):
                            print(f"{curr_player.name} won!")
                            winCondition=False
                            break
                        
                else:
                    table = play
                    player_turn = (player_turn+1) % len(players)
                    curr_player = players[player_turn]
                    if(curr_player.getEmpty()):
                        print(f"{curr_player.name} won!")
                        winCondition=False
                        break
                
            turn+=1
        deck.empty()