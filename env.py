from quopri import encode
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pydealer as pd
from pettingzoo.utils.env import AECEnv
from utils import *

suits = {
    "Joker": 4,
    "Spades": 3,
    "Hearts": 2,
    "Clubs": 1,
    "Diamonds": 0
}

table_types = {
    "a": 1,
    "aa": 2,
    "aaa": 3,
    "aaaa": 4,
    "aaa": 5,
    "ab": 6,
}

MAX_MOVES = 200
STATE_VECTOR_SIZE = 128
DECK_SIZE = 54
HAND_SIZE = 20

class SmartAIEnv(AECEnv):
    def __init__(self, render_mode=None):
        super().__init__()
        self._PASS_ACTION_INDEX = 0
        self.possible_agents = ['player_0', 'player_1', 'player_2']
        self.action_space = spaces.Box(low=new_ranks['values']['NULL'], high=new_ranks['values']['Big'], shape=(HAND_SIZE,), dtype=np.int8) 
        self.hand_space = spaces.Box(DECK_SIZE, shape=(HAND_SIZE,), dtype=np.int8) 
        self.table_space = spaces.Discrete(low=new_ranks['values']['NULL'], high=new_ranks['values']['Big'], dtype=np.int8) 
        self.table_type_space = spaces.Discrete(len(table_types), dtype=np.int8) 
        self.turn_space = spaces.Discrete(3, dtype=np.int8)
        self.op_resources_space_0 = spaces.Discrete(20, dtype=np.int8)
        self.op_resources_space_1 = spaces.Discrete(20, dtype=np.int8)
        
        self.observation_space = spaces.Dict({
            "hand":self.hand_space, 
            "table":self.table_space, 
            "table_type":self.table_type_space,
            "turn":self.turn_space,
            "num_op_1":self.op_resources_space_0, 
            "num_op_2":self.op_resources_space_1
        })

    def _get_obs(self):
        return np.array([self.hand_space, self.table_space, self.turn_space, self.op_resources_space[0], self.op_resources_space[1]], dtype=np.float32)

    def _get_info(self):
        return {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        deck = np.arange(54)
        self.np_random.shuffle(deck)
        
        self._agent_hands = {
            'player_0': list(deck[0:17]),
            'player_1': list(deck[17:34]),
            'player_2': list(deck[34:51]),
        }
        self._landlord_cards = list(deck[51:54])
        
        self._landlord = self.possible_agents[self.np_random.integers(0, 3)]
        self._agent_hands[self._landlord].extend(self._landlord_cards)
        
        self._turns = 0
        self._game_over = False
        self.agent_selection = self._landlord

        self.rewards = {agent: 0 for agent in self.possible_agents}
        self.terminations = {agent: False for agent in self.possible_agents}
        self.truncations = {agent: False for agent in self.possible_agents}
        self.infos = {agent: {} for agent in self.possible_agents}
        pass




    def _is_action_legal(self, agent, action):
        hand = self.decode_hand(agent)
        play = self.decode_action(action)
        table, table_type = self.decode_table(self._last_played_combination)
        agent_play = encode(hand, play)
        all_plays = getAllPlays(hand, table, table_type)
        return agent_play in all_plays
    
    def decode_table(self, table_combination):
        if not table_combination or table_combination==self._PASS_ACTION_INDEX:
            return np.array([]), None
        table_play = self.decode_action(table_combination)
        table_stack = pd.Stack(cards=table_play, sort=True, ranks=new_ranks)
        table_type = table_play.card_type
        return table_stack.cards, table_type
    
    def decode_hand(self, agent):
        cards = [new_ranks["values"].keys()[a] for a in self._agent_hands[agent] if a!=new_ranks['values']['NULL']]
        return pd.Stack(cards=cards, sort=True, ranks=new_ranks)
    
    def decode_action(self, action):
        decoded = [self.decode_value(a) for a in action if a!=new_ranks['values']['NULL']]
        if not decoded:
            return None
        return decoded
    
    def decode_value(self, val):
        if(val==54):
            return "big"
        if(val==53):
            return "small"
        return list(new_ranks['values'].keys())[val%13+1]
    
    
    
    def _handle_illegal_move(self, agent):
        penalty = -1
        self.rewards[agent] += penalty
        # print(f"Agent {agent} penalized {penalty} for illegal move.")
        
    def _handle_game_end(self, winner):
        # print(f"Agent {winner} has won the game!")
        for agent in self.possible_agents:
            if agent == winner:
                self.rewards[agent] += 10 * (2 if agent == self._landlord else 1)
            else:
                self.rewards[agent] -= 5 * (2 if agent == self._landlord else 1) 
        self._game_over = True
        
    def _check_truncation(self):
        return self._turns >= MAX_MOVES

    def _check_win_condition(self, agent):
        return len(self._agent_hands[agent]) == 0

    def _next_player(self):
        current_index = self.possible_agents.index(self.agent_selection)
        next_index = (current_index + 1) % len(self.possible_agents)
        self.agent_selection = self.possible_agents[next_index]

    def _get_cards_from_action(self, action):
        if action == self._PASS_ACTION_INDEX:
            return []
        return [self.decode_value(a) for a in action if a != new_ranks['values']['NULL']]
    
    def _update_hand(self, agent, cards_played):
        hand = self._agent_hands[agent]
        for card in cards_played:
            card_value = new_ranks['values'][card]
            hand.remove(card_value)
        self._agent_hands[agent] = hand

    def get_action_id(self, play):
        if play is None:
            return self._PASS_ACTION_INDEX
        
        # Get the rank of the primary card (e.g., in a Triple+Single, it's the Triple's rank)
        # Using your new_ranks: '3' is 1, so we subtract 1 to start at 0
        main_rank = new_ranks['values'][play.cards[0].value] - 1
        ctype = play.card_type
        
        if ctype == 'a':       return 1 + main_rank
        if ctype == 'aa':      return 16 + main_rank
        if ctype == 'aaa':     return 31 + main_rank
        if ctype == 'aaab':    return 46 + main_rank # Triple + Single
        if ctype == 'aaabb':   return 61 + main_rank # Triple + Pair
        if ctype == 'aaaa':    return 76 + main_rank # Bomb
        
        # Special case: Rocket (Big + Small Joker)
        if len(play.cards) == 2 and "Big" in str(play.cards) and "Small" in str(play.cards):
            return 151

        # For Straights, you can simplify or assign remaining IDs (91-150)
        # based on the starting rank.
        if 'abcd' in ctype:    return 91 + main_rank 
        
        return self._PASS_ACTION_INDEX # Fallback

    
    def _generate_action_mask(self, agent):
        # 1. Initialize a mask of zeros (all moves illegal by default)
        mask = np.zeros(MAX_MOVES, dtype=np.int8)
        
        # 2. Get the current state of the table
        # We need the last combination played to know what we must beat
        table_stack, table_type = self.decode_table(self._last_played_combination)
        
        # 3. Use your utility to find all legal Play objects
        hand_stack = self.decode_hand(agent)
        legal_plays = getAllPlays(hand_stack, table_stack, table_type)
        
        # 4. Always allow 'Pass' unless the agent is the one who started the round
        # Assuming index 0 is PASS
        if self._last_played_agent != agent:
            mask[self._PASS_ACTION_INDEX] = 1
        
        # 5. Map the Play objects to your MAX_MOVES indices
        for play in legal_plays:
            # You need a function 'get_action_id(play)' that returns 0-199
            action_id = self.get_action_id(play) 
            if action_id < MAX_MOVES:
                mask[action_id] = 1
                
        return mask

    def step(self, action):
        if self.terminations[self.agent_selection] or self.truncations[self.agent_selection]:
            self._was_dead_step(action)
            return
        
        current_agent = self.agent_selection
        
        if not self._is_action_legal(current_agent, action):
            print(f"Agent {current_agent} took an illegal action: {action}")
            self._handle_illegal_move(current_agent)
            self._next_player()
            return
        
        cards_played = self._get_cards_from_action(action)
        self._update_hand(current_agent, cards_played) 
        if action != self._PASS_ACTION_INDEX:
            self._last_played_agent = current_agent
            self._last_played_combination = action
            self._pass_counter = 0
        else:
            self._pass_counter += 1
        self._turns += 1

        terminated = self._check_win_condition(current_agent)
        
        if terminated:
            self._handle_game_end(winner=current_agent) 
            
        truncated = self._check_truncation() 
        
        instant_reward = 0 
        
        self.rewards[current_agent] = instant_reward
        self.terminations[current_agent] = terminated
        self.truncations[current_agent] = truncated
        self.infos[current_agent] = {}
        
        
        self._next_player()
        
        
        
        
    def render(self):
        # Optional: Implement visualization
        pass

    def close(self):
        # Optional: Clean up resources
        pass

# You can now instantiate and test your environment:
# env = CustomEnv()
# check_env(env) # (If you install gymnasium[testing])