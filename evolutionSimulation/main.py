import pygame  # Import the Pygame library
import constants
from player import Player
from food import Food
from neuralNetworks import NeuralNetwork
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from geneticAlgo import next_generation



# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))  # Create the Pygame display surface
pygame.display.set_caption("Evolution Simulation")  # Set the window title
# Font for displaying text
font = pygame.font.SysFont(None, 36)

# Clock to control the frame rate
clock = pygame.time.Clock()

def evaluate_population(population, generation):
    players = [Player(network) for network in population]
    predefined_food = [Food() for _ in range(25)]
    player_group = pygame.sprite.Group(players)
    food_group = pygame.sprite.Group(predefined_food)  # Initialize with predefined food objects
    scores = [0] * len(players)
    previous_positions = [(player.rect.x, player.rect.y) for player in players]  # Initialize previous positions
    frames = 0
    max_time_without_food = 1200  # 30 seconds at 60 FPS

    while frames < 1500:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Update players and food
        for i, player in enumerate(players):
            if player.alive:
                # Calculate distances
                if len(food_group) > 0:
                    nearest_food = min(food_group, key=lambda food: (food.rect.x - player.rect.x)**2 + (food.rect.y - player.rect.y)**2)
                else:
                    nearest_food = None

                # Calculate the nearest edge distance
                edge_distances = {
                    'left': player.rect.x,
                    'right': SCREEN_WIDTH - player.rect.right,
                    'top': player.rect.y,
                    'bottom': SCREEN_HEIGHT - player.rect.bottom
                }
                nearest_edge_key = min(edge_distances, key=edge_distances.get)
                nearest_edge_x, nearest_edge_y = {
                    'left': (0, player.rect.y),
                    'right': (SCREEN_WIDTH, player.rect.y),
                    'top': (player.rect.x, 0),
                    'bottom': (player.rect.x, SCREEN_HEIGHT)
                }[nearest_edge_key]
                has_eaten = player.has_eaten

                # Normalize distances for the network input
                normalized_player_x = player.rect.x / SCREEN_WIDTH
                normalized_player_y = player.rect.y / SCREEN_HEIGHT
                normalized_nearest_food_x = (nearest_food.rect.x / SCREEN_WIDTH) if nearest_food else 0
                normalized_nearest_food_y = (nearest_food.rect.y / SCREEN_HEIGHT) if nearest_food else 0
                
                # Find distances to the nearest 3 foods
                all_food_distances = sorted([(food, ((food.rect.x - player.rect.x)**2 + (food.rect.y - player.rect.y)**2)**0.5) for food in food_group], key=lambda x: x[1])
                nearest_foods_dists = [dist for _, dist in all_food_distances[:3]]
                normalized_nearest_foods_dists = [dist / ((SCREEN_WIDTH**2 + SCREEN_HEIGHT**2)**0.5) for dist in nearest_foods_dists]
                # Ensure we have exactly 3 distances
                while len(normalized_nearest_foods_dists) < 3:
                    normalized_nearest_nearest_foods_dists.append(0)

                normalized_nearest_edge_x = nearest_edge_x / SCREEN_WIDTH
                normalized_nearest_edge_y = nearest_edge_y / SCREEN_HEIGHT

                state = [
                    normalized_player_x, 
                    normalized_player_y, 
                    normalized_nearest_food_x, 
                    normalized_nearest_food_y, 
                    *normalized_nearest_foods_dists,  # Unpack the list of distances to nearest foods
                    normalized_nearest_edge_x, 
                    normalized_nearest_edge_y, 
                    int(has_eaten)
                ]
                action = player.network.get_action(state)
                player.update(action)

                # Scoring and survival logic
                if nearest_food and pygame.sprite.collide_rect(player, nearest_food):
                    if not player.has_eaten:
                        player.has_eaten = True
                        scores[i] += 100  # Score increase for eating the food
                        nearest_food.kill()
                    else:
                        nearest_food.kill()
                        scores[i] -= 150  # Negative score for eating more than one food
                elif player.has_eaten:
                    if nearest_edge_key == 'left' and player.rect.left == 0 or \
                       nearest_edge_key == 'right' and player.rect.right == SCREEN_WIDTH or \
                       nearest_edge_key == 'top' and player.rect.top == 0 or \
                       nearest_edge_key == 'bottom' and player.rect.bottom == SCREEN_HEIGHT:
                        scores[i] += 100  # Score increase for reaching the edge after eating
                        scores[i] += (1200 - frames) * 0.01
                        player.alive = False  # Mark the player as not alive
                        player.image.set_alpha(150)  # Optional: Make the player semi-transparent or change its appearance
                elif not player.has_eaten and (frames > max_time_without_food):
                    player.alive = False  # Kill player if they haven't eaten within the time limit
                    player.image.set_alpha(150)  # Optional: Make the player semi-transparent or change its appearance

                # Check if the player has moved
                current_position = (player.rect.x, player.rect.y)
                if current_position == previous_positions[i]:
                    scores[i] -= 1  # Deduct points for not moving
                previous_positions[i] = current_position  # Update previous position

        # Draw everything
        screen.fill(WHITE)
        player_group.draw(screen)
        food_group.draw(screen)

        # Display generation and time info
        gen_text = font.render(f'Generation: {generation}', True, (0, 0, 0))
        max_score = max(scores)
        max_score_text = font.render(f'Max Score: {max_score}', True, (0, 0, 0))
        time_passed = frames // 60  # Convert frames to seconds
        time_text = font.render(f'Time: {time_passed}s', True, (0, 0, 0))
        screen.blit(gen_text, (10, 10))
        screen.blit(max_score_text, (10, 50))
        screen.blit(time_text, (10, 90))

        # Flip the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)
        frames += 1

    return scores

# Evolutionary algorithm
population_size = 25
input_size = 10  # [player x, nearest object x, nearest object y]
hidden_size = 10
output_size = 4  # [left, right]
generations = 20

# Initialize population
population = [NeuralNetwork(input_size, hidden_size, output_size) for _ in range(population_size)]

for generation in range(generations):
    fitnesses = evaluate_population(population, generation + 1)
    max_fitness = max(fitnesses)
    print(f"Generation {generation + 1}: Max Score = {max_fitness}")
    population = next_generation(population, fitnesses)

pygame.quit()