import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2R Manipulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Link lengths
LINK1_LENGTH = 150
LINK2_LENGTH = 150

# Position of the base
base = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Angles (in radians)
theta1 = math.radians(0)
theta2 = math.radians(0)

# # Constraints to keep the angles within a valid range
# theta1 = max(min(theta1, math.pi), -math.pi)
# theta2 = max(min(theta2, math.pi), -math.pi)

# Function to calculate the position of the end effector
def calculate_positions(theta1, theta2):
    x1 = base[0] + LINK1_LENGTH * math.cos(theta1)
    y1 = base[1] + LINK1_LENGTH * math.sin(theta1)
    x2 = x1 + LINK2_LENGTH * math.cos(theta1 + theta2)
    y2 = y1 + LINK2_LENGTH * math.sin(theta1 + theta2)
    return (x1, y1), (x2, y2)

# Function to draw the manipulator
def draw_manipulator(screen, joint, end_effector):
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, base, joint, 5)
    pygame.draw.line(screen, BLACK, joint, end_effector, 5)
    pygame.draw.circle(screen, RED, (int(base[0]), int(base[1])), 10)
    pygame.draw.circle(screen, BLUE, (int(joint[0]), int(joint[1])), 10)
    pygame.draw.circle(screen, BLUE, (int(end_effector[0]), int(end_effector[1])), 10)
    pygame.display.flip()
    

# # Calculate positions and ensure they stay within screen bounds
# def calculate_positions(theta1, theta2):
#     x1 = LINK1_LENGTH * math.cos(theta1)
#     y1 = LINK1_LENGTH * math.sin(theta1)
#     x2 = x1 + LINK2_LENGTH * math.cos(theta1 + theta2)
#     y2 = y1 + LINK2_LENGTH * math.sin(theta1 + theta2)
#     x1, y1 = min(max(x1, -SCREEN_WIDTH//2), SCREEN_WIDTH//2), min(max(y1, -SCREEN_HEIGHT//2), SCREEN_HEIGHT//2)
#     x2, y2 = min(max(x2, -SCREEN_WIDTH//2), SCREEN_WIDTH//2), min(max(y2, -SCREEN_HEIGHT//2), SCREEN_HEIGHT//2)
#     return (x1, y1), (x2, y2)


# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        theta1 -= 0.01
    if keys[pygame.K_RIGHT]:
        theta1 += 0.01
    if keys[pygame.K_UP]:
        theta2 -= 0.01
    if keys[pygame.K_DOWN]:
        theta2 += 0.01

    # Calculate positions
    joint, end_effector = calculate_positions(theta1, theta2)

    # Draw manipulator
    draw_manipulator(screen, joint, end_effector)

    clock.tick(60)

pygame.quit()
