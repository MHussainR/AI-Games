import pygame
import math
import numpy as np
import random

# Pygame Initialization
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Inverted Pendulum with Q-learning")

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

GRAVITY = 9.81
MASS_PENDULUM = 1.0
MASS_CART = 1.0
LENGTH = 200  # Length of the pendulum
TIME_STEP = 0.02
FORCE_MAGNITUDE = 200

# Q-learning Parameters
ALPHA = 0.1  # Learning rate
GAMMA = 0.99  # Discount factor
EPSILON = 0.1  # Exploration factor
NUM_BUCKETS = (1, 1, 6, 3)  # Discretization of the state space
NUM_ACTIONS = 3  # Actions: push left, no push, push right

# Pendulum and Cart State
cart_x = 400
cart_y = 300
cart_velocity = 0
pendulum_angle = math.pi / 4  # 45 degrees
pendulum_angular_velocity = 0

# Q-table
Q_table = np.zeros(NUM_BUCKETS + (NUM_ACTIONS,))

def discretize_state(cart_x, cart_velocity, pendulum_angle, pendulum_angular_velocity):
    discrete_state = [
        min(int(cart_x / 800 * NUM_BUCKETS[0]), NUM_BUCKETS[0] - 1),
        min(int((cart_velocity + 5) / 10 * NUM_BUCKETS[1]), NUM_BUCKETS[1] - 1),
        min(int((pendulum_angle + math.pi / 2) / math.pi * NUM_BUCKETS[2]), NUM_BUCKETS[2] - 1),
        min(int((pendulum_angular_velocity + 5) / 10 * NUM_BUCKETS[3]), NUM_BUCKETS[3] - 1)
    ]
    return tuple(discrete_state)

def choose_action(state):
    if random.uniform(0, 1) < EPSILON:
        return random.randint(0, NUM_ACTIONS - 1)
    else:
        return np.argmax(Q_table[state])

def update_q_table(state, action, reward, next_state):
    best_next_action = np.argmax(Q_table[next_state])
    td_target = reward + GAMMA * Q_table[next_state][best_next_action]
    td_error = td_target - Q_table[state][action]
    Q_table[state][action] += ALPHA * td_error

def calculate_reward(pendulum_angle):
    return -abs(pendulum_angle)  # Reward is higher for angles closer to zero

def physics_step(cart_x, cart_velocity, pendulum_angle, pendulum_angular_velocity, action):
    if action == 0:
        force = -FORCE_MAGNITUDE
    elif action == 2:
        force = FORCE_MAGNITUDE
    else:
        force = 0

    sin_theta = math.sin(pendulum_angle)
    cos_theta = math.cos(pendulum_angle)
    total_mass = MASS_CART + MASS_PENDULUM
    pendulum_acceleration = (GRAVITY * sin_theta + cos_theta * (-force - MASS_PENDULUM * LENGTH * (pendulum_angular_velocity ** 2) * sin_theta) / total_mass) / (LENGTH * (4/3 - MASS_PENDULUM * cos_theta ** 2 / total_mass))
    cart_acceleration = (force + MASS_PENDULUM * LENGTH * (pendulum_angular_velocity ** 2 * sin_theta - pendulum_acceleration * cos_theta)) / total_mass

    # Update states
    cart_velocity += cart_acceleration * TIME_STEP
    cart_x += cart_velocity * TIME_STEP
    pendulum_angular_velocity += pendulum_acceleration * TIME_STEP
    pendulum_angle += pendulum_angular_velocity * TIME_STEP

    # Constraints
    if cart_x < 25:
        cart_x = 25
        cart_velocity = 0
    elif cart_x > 775:
        cart_x = 775
        cart_velocity = 0

    return cart_x, cart_velocity, pendulum_angle, pendulum_angular_velocity

def draw_cart(cart_x, cart_y):
    pygame.draw.rect(screen, BLUE, [cart_x - 25, cart_y - 10, 50, 20])

def draw_pendulum(cart_x, cart_y, angle):
    end_x = cart_x + LENGTH * math.sin(angle)
    end_y = cart_y + LENGTH * math.cos(angle)
    pygame.draw.line(screen, RED, (cart_x, cart_y), (end_x, end_y), 5)
    pygame.draw.circle(screen, RED, (int(end_x), int(end_y)), 10)

def main():
    global cart_x, cart_velocity, pendulum_angle, pendulum_angular_velocity

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        state = discretize_state(cart_x, cart_velocity, pendulum_angle, pendulum_angular_velocity)
        action = choose_action(state)
        cart_x, cart_velocity, pendulum_angle, pendulum_angular_velocity = physics_step(
            cart_x, cart_velocity, pendulum_angle, pendulum_angular_velocity, action)
        reward = calculate_reward(pendulum_angle)
        next_state = discretize_state(cart_x, cart_velocity, pendulum_angle, pendulum_angular_velocity)
        update_q_table(state, action, reward, next_state)

        # Clear the screen
        screen.fill(WHITE)

        # Draw cart and pendulum
        draw_cart(cart_x, cart_y)
        draw_pendulum(cart_x, cart_y, pendulum_angle)

        # Flip the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
