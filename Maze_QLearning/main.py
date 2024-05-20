import pygame
import numpy as np
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("10x10 Grid Navigation with Q-learning")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font for displaying text
font = pygame.font.SysFont(None, 24)

# Grid dimensions
GRID_SIZE = 10
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE

# Grid definition (1 means path is clear, 0 means blockage)
grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [0, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1]
]

# Q-learning parameters
n_states = GRID_SIZE * GRID_SIZE
n_actions = 4  # Actions: [Up, Down, Left, Right]
learning_rate = 0.8
discount_factor = 0.95
exploration_prob = 0
epochs = 1000
time_limit = 20  # Time limit in seconds

# Initialize Q-table with zeros
Q_table = np.zeros((n_states, n_actions))

# Player and target positions
player_pos = [0, 0]
target_pos = [9, 9]

# Function to convert grid position to state index
def pos_to_state(pos):
    return pos[0] * GRID_SIZE + pos[1]

# Function to convert state index to grid position
def state_to_pos(state):
    return [state // GRID_SIZE, state % GRID_SIZE]

# Function to draw the grid and Q-values
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE if grid[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            state = pos_to_state([row, col])
            q_values = Q_table[state]
            q_text = font.render(f"{q_values.max():.2f}", True, GREEN if grid[row][col] == 1 else RED)
            screen.blit(q_text, (col * CELL_SIZE + 5, row * CELL_SIZE + 5))

# Function to draw the player and target
def draw_entities():
    pygame.draw.rect(screen, BLUE, pygame.Rect(player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(target_pos[1] * CELL_SIZE, target_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to choose an action using epsilon-greedy strategy
def choose_action(state):
    if np.random.rand() < exploration_prob:
        return np.random.randint(n_actions)  # Explore
    else:
        return np.argmax(Q_table[state])  # Exploit

# Function to apply an action and return the new state and reward
def apply_action(state, action):
    pos = state_to_pos(state)
    if action == 0 and pos[0] > 0:  # Up
        pos[0] -= 1
    elif action == 1 and pos[0] < GRID_SIZE - 1:  # Down
        pos[0] += 1
    elif action == 2 and pos[1] > 0:  # Left
        pos[1] -= 1
    elif action == 3 and pos[1] < GRID_SIZE - 1:  # Right
        pos[1] += 1
    new_state = pos_to_state(pos)
    if pos == target_pos:
        reward = 10  # Reward for reaching the target
    elif grid[pos[0]][pos[1]] == 0:
        reward = -10  # Heavy penalty for hitting a blockage
        return new_state, reward, True  # Episode ends
    else:
        reward = -0.1  # Small penalty for each move
    return new_state, reward, False  # Episode continues

# Main loop for Q-learning
for epoch in range(epochs):
    player_pos = [0, 0]
    state = pos_to_state(player_pos)
    total_reward = 0  # Track the total reward for the episode
    start_time = pygame.time.get_ticks()
    elapsed_time = 0

    while elapsed_time < time_limit * 1000:
        action = choose_action(state)
        new_state, reward, done = apply_action(state, action)
        total_reward += reward

        # Q-learning update rule
        Q_table[state, action] += learning_rate * (reward + discount_factor * np.max(Q_table[new_state]) - Q_table[state, action])
        state = new_state

        # Update player position
        player_pos = state_to_pos(state)

        # Drawing
        screen.fill(WHITE)
        draw_grid()
        draw_entities()
        pygame.display.flip()

        # Check if target is reached or player hit a blockage
        if player_pos == target_pos or done:
            break

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        elapsed_time = pygame.time.get_ticks() - start_time
        pygame.time.delay(100)  # Delay to slow down the movement for visualization

    print(f"Episode {epoch + 1}: Total Reward: {total_reward}")

print("Learned Q-table:")
print(Q_table)

# After training, you can use the Q-table to control the player
running = True
player_pos = [0, 0]
state = pos_to_state(player_pos)

while running:
    action = choose_action(state)
    new_state, _, done = apply_action(state, action)
    state = new_state

    # Update player position
    player_pos = state_to_pos(state)

    # Drawing
    screen.fill(WHITE)
    draw_grid()
    draw_entities()
    pygame.display.flip()

    # Check if target is reached or player hit a blockage
    if player_pos == target_pos or done:
        print("Target reached!" if player_pos == target_pos else "Player hit a blockage!")
        running = False

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    pygame.time.delay(100)  # Delay to slow down the movement for visualization
