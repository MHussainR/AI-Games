import math
from constants import base, LINK1_LENGTH, LINK2_LENGTH, theta1, theta2
import numpy as np
from QLearning import n_actions, Q_table


# Function to discretize the continuous angle space
def discretize_angle(angle, bins=100):
    return int(((angle + math.pi) / (2 * math.pi)) * bins) % bins

# Function to calculate the position of the end effector
def calculate_positions(theta1, theta2):
    x1 = base[0] + LINK1_LENGTH * math.cos(theta1)
    y1 = base[1] + LINK1_LENGTH * math.sin(theta1)
    x2 = x1 + LINK2_LENGTH * math.cos(theta1 + theta2)
    y2 = y1 + LINK2_LENGTH * math.sin(theta1 + theta2)
    return (x1, y1), (x2, y2)

# Function to get the state from angles
def get_state(theta1, theta2):
    return discretize_angle(theta1), discretize_angle(theta2)

# Function to choose an action using epsilon-greedy strategy
def choose_action(state, exploration_prob):
    if np.random.rand() < exploration_prob:
        return np.random.randint(n_actions)  # Explore
    else:
        return np.argmax(Q_table[state])  # Exploit

# Function to apply an action
def apply_action(action):
    global theta1, theta2
    if action == 0:
        theta1 += 0.1
    elif action == 1:
        theta1 -= 0.1
    elif action == 2:
        theta2 += 0.1
    elif action == 3:
        theta2 -= 0.1

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to generate a random target within the workspace of the manipulator
def generate_random_target():
    radius = LINK1_LENGTH + LINK2_LENGTH
    angle = np.random.uniform(0, 2 * math.pi)
    r = np.random.uniform(0, radius)
    x = base[0] + r * math.cos(angle)
    y = base[1] + r * math.sin(angle)
    return x, y