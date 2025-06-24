import pydealer as pd
import random as rd
from 'utils.py' import new_ranks, Human, simpleAI



    
def playRandCards(hand):
    
    

if __name__ == '__main__':
    deck = pd.Deck(rebuild=True, re_shuffle=True, ranks=new_ranks)
    joker_big = pd.Card("Joker", "JOKER")
    joker_small = pd.Card("Joker", "Joker")
    deck.add(joker_big)
    deck.add(joker_small)

    while(input("Any key to play. 'q' to quit.")!='q'):
    # while(True):
        play = None
        table = None
        seed = rd.randint(0, 2)
        deck.shuffle()
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
            players[i].hand.sort()
            
        turn = 1
        winCondition = True
        
        while(winCondition):
            for i in range(3):
                print(f"{curr_player.name}'s turn.")
                if(type(curr_player)=="Human"):
                    print(f"\n___________________________________________________________________________________________________________________________________________________________")
                    print(f"\nTurn {turn}:        p1 has {players[1][0].size} cards left.        p2 has {players[2][0].size} cards left.      You have {players[0][0].size} cards left.")
                
                print(f"{curr_player.name} has played {curr_player.select()}")
                if(curr_player.getEmpty()):
                    print(f"{curr_player.name} won!")
                    winCondition=False
                player_turn = (player_turn+1) % len(players)
                curr_player = players[player_turn]
            turn+=1
        deck.empty()