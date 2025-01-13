# from sim_class import Simulation

# # Initialize the simulation with a specified number of agents
# sim = Simulation(num_agents=1)  # For one robot

# # Example action: Move joints with specific velocities
# velocity_x = -0.3
# velocity_y = -0.3    
# velocity_z = -0.1
# drop_command = 0
# actions = [[velocity_x, velocity_y, velocity_z, drop_command]]

# velocity_x = 0.3
# velocity_y = 0.0    
# velocity_z = 0.0
# drop_command = 0
# actions_2 = [[velocity_x, velocity_y, velocity_z, drop_command]]

# velocity_x = 0.0
# velocity_y = 0.3    
# velocity_z = 0.0
# drop_command = 0
# actions_3 = [[velocity_x, velocity_y, velocity_z, drop_command]]

# velocity_x = -0.3
# velocity_y = 0.0    
# velocity_z = 0.0
# drop_command = 0
# actions_4 = [[velocity_x, velocity_y, velocity_z, drop_command]]

# velocity_x = 0.0
# velocity_y = -0.3    
# velocity_z = 0.0
# drop_command = 0
# actions_5 = [[velocity_x, velocity_y, velocity_z, drop_command]]

# # Run the simulation for a specified number of steps
# sim.run(actions, num_steps=1000)
# sim.run(actions_2, num_steps=1000)
# sim.run(actions_3, num_steps=1000)
# sim.run(actions_4, num_steps=1000)
# sim.run(actions_5, num_steps=1000)


# state = sim.run(actions)

# print(state)
from sim_class import Simulation

# Initialize simulation
sim = Simulation(num_agents=1)

# Define actions to move to 8 corners of the cube
actions_list = [
    [0.1, 0.1, 0.1, 0],   # Corner 1: (+x, +y, +z)
    [-0.1, 0.1, 0.1, 0],  # Corner 2: (-x, +y, +z)
    [-0.1, -0.1, 0.1, 0], # Corner 3: (-x, -y, +z)
    [0.1, -0.1, 0.1, 0],  # Corner 4: (+x, -y, +z)
    [0.1, 0.1, -0.1, 0],  # Corner 5: (+x, +y, -z)
    [-0.1, 0.1, -0.1, 0], # Corner 6: (-x, +y, -z)
    [-0.1, -0.1, -0.1, 0],# Corner 7: (-x, -y, -z)
    [0.1, -0.1, -0.1, 0]  # Corner 8: (+x, -y, -z)
]

envelope_coords = []

# Move pipette and record positions sequentially
for action in actions_list:
    # Run each action individually with a defined number of steps
    state = sim.run([action], num_steps=1000)
    print("State structure:", state)  # Debugging

    # Directly access pipette position
    if "robotId_1" in state and "pipette_position" in state["robotId_1"]:
        pipette_position = state["robotId_1"]["pipette_position"]
        envelope_coords.append(pipette_position)
    else:
        print("Pipette position not found in state:", state)

# Save data
with open("working_envelope.txt", mode="w") as file:
    for coord in envelope_coords:
        file.write(f"{coord}\n")



