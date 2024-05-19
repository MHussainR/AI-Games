import pygame
import constants
import random

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        self.image = pygame.Surface((constants.FOOD_WIDTH, constants.FOOD_HEIGHT))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        # Set the initial position of the food within the inner box
        self.rect.x = random.randint(constants.SCREEN_WIDTH // 2 - constants.SCREEN_WIDTH // 4 + constants.FOOD_WIDTH, constants.SCREEN_WIDTH // 2 + constants.SCREEN_WIDTH // 4 - constants.FOOD_WIDTH)
        self.rect.y = random.randint(constants.SCREEN_HEIGHT // 2 - constants.SCREEN_HEIGHT // 4 + constants.FOOD_HEIGHT, constants.SCREEN_HEIGHT // 2 + constants.SCREEN_HEIGHT // 4 - constants.FOOD_HEIGHT)

    def update(self, players):
        # Check for collision with players
        collided_players = pygame.sprite.spritecollide(self, players, True)  # True removes collided players
        if collided_players:
            self.kill()  # "Kill" the food when it collides with a player