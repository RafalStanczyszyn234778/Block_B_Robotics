# from stable_baselines3.common.env_checker import check_env
# from ot2_gym_wrapper import OT2Env  # Ensure this is your custom wrapper

# # Instantiate your custom environment
# wrapped_env = OT2Env()  # Modify this to match your wrapper class

# # Check the environment to ensure it complies with Gym API
# check_env(wrapped_env)

# # import gymnasium as gym
# # import numpy as np

# # # Load your custom environment
# # env = gym.make(wrapped_env)  # Replace "YourCustomEnv-v0" with your registered environment name

# # # Number of episodes
# # num_episodes = 5

# # for episode in range(num_episodes):
# #     obs = env.reset()
# #     done = False
# #     step = 0

# #     while not done:
# #         # Take a random action from the environment's action space
# #         action = env.action_space.sample()
# #         obs, reward, terminated, truncated, info = env.step(action)

# #         print(f"Episode: {episode + 1}, Step: {step + 1}, Action: {action}, Reward: {reward}")

# #         step += 1

# #         # Check if the episode should terminate
# #         done = terminated or truncated
# #         if done:
# #             print(f"Episode finished after {step} steps. Info: {info}")
# #             break

from stable_baselines3.common.env_checker import check_env
from ot2_gym_wrapper import OT2Env  # Ensure this is your custom wrapper

# Instantiate your custom environment
wrapped_env = OT2Env()  # Modify this to match your wrapper class

# Number of episodes
num_episodes = 5

for episode in range(num_episodes):
    obs = wrapped_env.reset()
    done = False
    step = 0

    while not done:
        # Take a random action from the environment's action space
        action = wrapped_env.action_space.sample()
        obs, reward, terminated, truncated, info = wrapped_env.step(action)

        print(f"Episode: {episode + 1}, Step: {step + 1}, Action: {action}, Reward: {reward}")

        step += 1

        # Check if the episode should terminate
        done = terminated or truncated
        if done:
            print(f"Episode finished after {step} steps. Info: {info}")
            break
