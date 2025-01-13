import gymnasium as gym
from gymnasium import spaces
import numpy as np
from sim_class import Simulation

class OT2Env(gym.Env):
    def __init__(self, render=False, max_steps=1000):
        super(OT2Env, self).__init__()
        self.render = render
        self.max_steps = max_steps

        # Create the simulation environment
        self.sim = Simulation(num_agents=1)

        # Define the action space
        # Normalized to [-1, 1] for three pipette dimensions (x, y, z)
        self.action_space = spaces.Box(low=np.array([-1, -1, -1]), 
                                       high=np.array([1, 1, 1]), 
                                       dtype=np.float32)

        # Define the observation space
        # Observation consists of the pipette position (3 values) and the goal position (3 values)
        # Both are bounded by the working area limits derived from the simulation logs
        self.observation_space = spaces.Box(
            low=np.array([-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf], dtype=np.float32),
            high=np.array([np.inf, np.inf, np.inf, np.inf, np.inf, np.inf], dtype=np.float32),
        )

        # self.observation_space = spaces.Box(
        #     low=np.array([-0.1871, -0.1705, 0.1695, -0.1871, -0.1705, 0.1695]),
        #     high=np.array([0.253, 0.2197, 0.2897, 0.253, 0.2197, 0.2897]),
        #     dtype=np.float32
        # )
        # Keep track of the number of steps
        self.steps = 0

    def reset(self, seed=None):
        # being able to set a seed is required for reproducibility
        if seed is not None:
            np.random.seed(seed)

        # Reset the state of the environment to an initial state
        # set a random goal position for the agent, consisting of x, y, and z coordinates within the working area (you determined these values in the previous datalab task)
        self.goal_position = np.random.uniform(low=[-0.1871, -0.1705, 0.1695], 
                                               high=[0.253, 0.2197, 0.2897], 
                                               size=(3,))
        self.initial_position = np.random.uniform(low=[-0.1871, -0.1705, 0.1695], 
                                              high=[0.253, 0.2197, 0.2897], 
                                              size=(3,))        
      
        # Call the environment reset function
        observation = self.sim.reset(num_agents=1)
        # now we need to process the observation and extract the relevant information, the pipette position, convert it to a numpy array, and append the goal position and make sure the array is of type np.float32
        # Process the observation: extract pipette position and append goal position
        robot_key = list(observation.keys())[0]  # Dynamically fetch the first robot key (e.g., 'robotId_1')
        observation[robot_key]["pipette_position"] = self.initial_position.tolist()
        
        pipette_position = np.array(observation[robot_key]["pipette_position"], dtype=np.float32)        
        observation = np.concatenate((pipette_position, self.goal_position), dtype=np.float32)
        #Reset the number of steps
        self.steps = 0

        info = {}

        return observation, info

    def step(self, action):
        # Execute one time step within the environment
        # since we are only controlling the pipette position, we accept 3 values for the action and need to append 0 for the drop action
        action = np.append(action, [0])  # Append 0 for the drop action # YOUR CODE HERE

        # Call the environment step function
        observation = self.sim.run([action]) # Why do we need to pass the action as a list? Think about the simulation class.

        # now we need to process the observation and extract the relevant information, the pipette position, convert it to a numpy array, and append the goal position and make sure the array is of type np.float32
        # Dynamically fetch the robot key
        robot_key = list(observation.keys())[0]  # Extract the first robot key (e.g., 'robotId_1')

        # Extract the pipette position for the relevant robot
        pipette_position = np.array(observation[robot_key]["pipette_position"], dtype=np.float32)

        # Combine pipette position with the goal position
        observation = np.concatenate((pipette_position, self.goal_position), dtype=np.float32)

        # Calculate the reward, this is something that you will need to experiment with to get the best results
        distance_to_goal = np.linalg.norm(pipette_position - self.goal_position)
        reward = -distance_to_goal  # Negative reward proportional to distance
                
        # next we need to check if the if the task has been completed and if the episode should be terminated
        # To do this we need to calculate the distance between the pipette position and the goal position and if it is below a certain threshold, we will consider the task complete. 
        # What is a reasonable threshold? Think about the size of the pipette tip and the size of the plants.

        # YOUR CODE HERE:
        success_threshold = 0.01 
        if distance_to_goal < success_threshold:
            terminated = True
            # we can also give the agent a positive reward for completing the task
            reward += 10
        else:
            terminated = False

        # next we need to check if the episode should be truncated, we can check if the current number of steps is greater than the maximum number of steps
        if self.steps >= self.max_steps:
            truncated = True
        else:
            truncated = False

        info = {} # we don't need to return any additional information

        # increment the number of steps
        self.steps += 1

        return observation, reward, terminated, truncated, info

    def render(self, mode='human'):
        pass
    
    def close(self):
        self.sim.close()
