import pydealer as pd
import random as rd
from utils import new_ranks, Human, simpleAI



if __name__ == '__main__':
    deck = pd.Deck(rebuild=True, re_shuffle=True, ranks=new_ranks)
    joker_big = pd.Card("Joker", "JOKER")
    joker_small = pd.Card("Joker", "Joker")
    deck.add(joker_big)
    deck.add(joker_small)

    # while(input("Any key to play. 'q' to quit.")!='q'):
    while(True):
        print("\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ GAME BEGIN $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
        play = (None, "")
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
                if(type(curr_player)==Human):
                    print(f"\n___________________________________________________________________________________________________________________________________________________________")
                    print(f"\nTurn {turn}:        p1 has {players[1].hand.size} cards left.        p2 has {players[2].hand.size} cards left.      You have {players[0].hand.size} cards left.")
                
                play = curr_player.select(play)
                if(curr_player.getEmpty()):
                    print(f"{curr_player.name} won!")
                    winCondition=False
                    break
                player_turn = (player_turn+1) % len(players)
                curr_player = players[player_turn]
            turn+=1
        deck.empty()