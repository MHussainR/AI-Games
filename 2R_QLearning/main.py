import pygame
import math
import numpy as np
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2R Manipulator with Q-learning")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Font for displaying text
font = pygame.font.SysFont(None, 36)

# Link lengths
LINK1_LENGTH = 150
LINK2_LENGTH = 150

# Position of the base
base = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Angles (in radians)
theta1 = 0
theta2 = 0

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

# Function to draw the manipulator
def draw_manipulator(screen, joint, end_effector, target, remaining_time, episode, reward):
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, base, joint, 5)
    pygame.draw.line(screen, BLACK, joint, end_effector, 5)
    pygame.draw.circle(screen, RED, (int(base[0]), int(base[1])), 10)
    pygame.draw.circle(screen, BLUE, (int(joint[0]), int(joint[1])), 10)
    pygame.draw.circle(screen, BLUE, (int(end_effector[0]), int(end_effector[1])), 10)
    pygame.draw.circle(screen, GREEN, (int(target[0]), int(target[1])), 10)
    
    # Display remaining time
    time_text = font.render(f'Time: {remaining_time:.1f}s', True, BLACK)
    screen.blit(time_text, (10, 10))
    
    # Display target and end effector positions
    target_text = font.render(f'Target: ({int(target[0])}, {int(target[1])})', True, BLACK)
    end_effector_text = font.render(f'End Effector: ({int(end_effector[0])}, {int(end_effector[1])})', True, BLACK)
    screen.blit(target_text, (10, 50))
    screen.blit(end_effector_text, (10, 90))
    
    # Display episode number and reward
    episode_text = font.render(f'Episode: {episode}', True, BLACK)
    reward_text = font.render(f'Reward: {reward:.2f}', True, BLACK)
    screen.blit(episode_text, (10, 130))
    screen.blit(reward_text, (10, 170))

    pygame.display.flip()


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

for epoch in range(epochs):
    theta1 = 0
    theta2 = 0
    target = generate_random_target()
    state = get_state(theta1, theta2)
    start_time = time.time()
    running = True
    clock = pygame.time.Clock()
    total_reward = 0  # Track the total reward for the episode

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

        action = choose_action(state, exploration_prob)
        apply_action(action)
        new_state = get_state(theta1, theta2)
        
        joint, end_effector = calculate_positions(theta1, theta2)
        distance_to_target = calculate_distance(end_effector, target)
        elapsed_time = time.time() - start_time
        remaining_time = time_limit - elapsed_time

        if distance_to_target < 10:  # If the end effector is close to the target
            reward = 1
            running = False  # End episode when the target is reached
        elif remaining_time <= 0:  # Time limit exceeded
            reward = -1
            running = False  # End episode when time limit is exceeded
        else:
            reward = -distance_to_target / 100.0  # Negative reward based on distance to target

        total_reward += reward  # Accumulate reward for the episode

        # Update Q-value using the Q-learning update rule
        Q_table[state][action] += learning_rate * (reward + discount_factor * np.max(Q_table[new_state]) - Q_table[state][action])
        state = new_state

        # Draw manipulator and display time
        draw_manipulator(screen, joint, end_effector, target, remaining_time, epoch + 1, total_reward)
        clock.tick(60)

print("Learned Q-table:")
print(Q_table)

# After training, you can use the Q-table to control the manipulator
running = True
state = get_state(theta1, theta2)
start_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()

    action = choose_action(state, 0)  # Exploit learned policy
    apply_action(action)
    state = get_state(theta1, theta2)

    joint, end_effector = calculate_positions(theta1, theta2)
    distance_to_target = calculate_distance(end_effector, target)
    elapsed_time = time.time() - start_time
    remaining_time = time_limit - elapsed_time

    if remaining_time <= 0:
        running = False  # End if time runs out

    # Draw manipulator and display time
    draw_manipulator(screen, joint, end_effector, target, remaining_time)
    clock.tick(60)
