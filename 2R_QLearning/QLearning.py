import numpy as np

# Q-learning parameters
n_states = 100  # Discretize the angle space
n_actions = 4  # Actions: [Increase theta1, Decrease theta1, Increase theta2, Decrease theta2]
learning_rate = 0.8
discount_factor = 0.95
exploration_prob = 0.2
epochs = 1000
time_limit = 20  # Time limit in seconds

# Initialize Q-table with zeros
Q_table = np.zeros((n_states, n_states, n_actions))