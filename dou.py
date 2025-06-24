import pydealer as pd
import random as rd



def playCards(hand, choice):
    try: 
        return hand.get(hand.find(choice)[0])
    except:
        return None
    
def playRandCards(hand):
    return hand.get(hand.find(hand[rd.randint(0, hand.size-1)].value)[0])
    

if __name__ == '__main__':
    
    new_ranks = {
        "values": {
            "Joker": 14,
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
            "JOKER": 6,
            "Joker": 5,
            "Spades": 4,
            "Hearts": 3,
            "Clubs": 2,
            "Diamonds": 1
        }
    }
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
        players = [[pd.Stack(ranks=new_ranks), "You"], [pd.Stack(ranks=new_ranks), "P1"], [pd.Stack(ranks=new_ranks), "P2"]]
        player_turn = 0
        for i in range(len(players)):
            if(seed==i):
                players[i][0].add(deck.deal(20))
                player_turn = i
            else:
                players[i][0].add(deck.deal(17))
            players[i][0].sort()
            
        turn = 1
        
        
        print(f"\n___________________________________________________________________________________________________________________")
        print(f"\nTurn {turn}:        p1 has {players[1][0].size} cards left.        p2 has {players[2][0].size} cards left.      You have {players[0][0].size} cards left.")
        while(True):
            while(player_turn>0):
                print(f"{players[player_turn][1]}'s turn.")
                play = playRandCards(players[player_turn][0])
                print(f"{players[player_turn][1]} has played {play}")
                if(not players[player_turn][0].size):
                    print(f"{players[player_turn][1]} won!")
                    break
                player_turn = (player_turn+1) % len(players)
                
            
            play = playCards(players[0][0], input(f"Your turn: \n{players[0][0]} \nSelect a card: "))
            while (not play):
                play = playCards(players[0][0], input("INVALID card! Try again: "))
            
            print(f"You have played {play}.")
            if(not players[player_turn][0].size):
                print(f"{players[player_turn][1]} won!")
                break
            player_turn = (player_turn+1) % len(players)
            turn+=1
            print(f"\n___________________________________________________________________________________________________________________")
            print(f"\nTurn {turn}:        p1 has {players[1][0].size} cards left.        p2 has {players[2][0].size} cards left.      You have {players[0][0].size} cards left.")
        deck.empty()