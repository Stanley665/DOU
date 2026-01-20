import supersuit as ss
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy
from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.policies import MaskableMlpPolicy

# 1. Define your PettingZoo AEC Environment function (replace with your actual import)
# This should be a function that returns an instance of your AEC environment
# Example: from your_dou_dizhu_module import raw_env as DouDizhuEnv
# For this example, let's use a placeholder. You'd use the one you built.
from pettingzoo.classic import tictactoe_v3 as tictactoe

def make_dou_dizhu_env(render_mode=None):
    # This function should instantiate your PettingZoo AEC environment
    # For a real project, you would use: env = DouDizhuEnv(...)
    # Using TicTacToe as a working example since it is a turn-based AEC game:
    env = tictactoe.raw_env(render_mode=render_mode)
    return env

# --- TRAINING SETUP ---
NUM_ENVS = 4  # Number of parallel environments (for faster training)
NUM_CPUS = 2  # Number of CPU cores to use for multiprocessing

# 2. Build the SuperSuit Wrapper Pipeline
def get_wrapped_env():
    # 1. Instantiate the PettingZoo AEC Environment
    env = make_dou_dizhu_env()
    
    # Optional: Other preprocessing wrappers (e.g., ss.pad_action_space_v0, ss.frame_stack_v1)
    
    # 2. Convert AEC to Parallel API (often simpler for the next step)
    # Dou Dizhu is naturally turn-based, but SuperSuit handles the transition well.
    env = ss.pettingzoo_action_space_v0(env) # Pads action spaces if they are heterogeneous
    
    # 3. Convert the Parallel PettingZoo environment into a vectorized Gymnasium environment
    # This stacks all agent observations/actions into single vectors. (Parameter Sharing)
    env = ss.pettingzoo_env_to_vec_env_v1(env)
    
    # 4. Concatenate multiple copies of the vectorized environment for faster training
    env = ss.concat_vec_envs_v1(env, NUM_ENVS, num_cpus=NUM_CPUS, base_class="stable_baselines3")
    
    return env

# --- TRAINING ---
env = get_wrapped_env()

# For a game like Dou Dizhu, which has complex discrete actions and invalid moves, 
# you MUST use MaskablePPO from sb3-contrib.
# You also need to ensure your PettingZoo environment's observation space 
# includes an 'action_mask' key for this to work!

model = MaskablePPO(
    MaskableMlpPolicy,  # Use the Maskable policy wrapper
    env,
    verbose=1,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    gamma=0.99,
    # You will need to tune these hyper-parameters
)

print("Starting training with MaskablePPO...")
model.learn(total_timesteps=10_000)

model.save("dou_dizhu_ppo_model")
print("Training finished and model saved.")

env.close()