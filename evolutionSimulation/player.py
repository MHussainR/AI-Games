import pygame
import constants
import random
from utils import weights_to_color

class Player(pygame.sprite.Sprite):
    def __init__(self, network):
        super(Player, self).__init__()
        self.image = pygame.Surface((constants.PLAYER_WIDTH, constants.PLAYER_HEIGHT))
        self.image.fill(weights_to_color(network.weights_ih[0]))
        self.rect = self.image.get_rect()
         # Set initial position randomly on the edges of the screen
        if random.choice([True, False]):  # Randomly choose horizontal or vertical placement
            if random.choice([True, False]):  # Randomly choose left or right side
                self.rect.left = 0
            else:
                self.rect.right = constants.SCREEN_WIDTH
            self.rect.centery = random.randint(0, constants.SCREEN_HEIGHT)
        else:
            if random.choice([True, False]):  # Randomly choose top or bottom side
                self.rect.top = 0
            else:
                self.rect.bottom = constants.SCREEN_HEIGHT
            self.rect.centerx = random.randint(0, constants.SCREEN_WIDTH)
        self.image.set_alpha(255)
        self.has_eaten = False
        self.network = network
        self.alive = True
    
    def update(self, action):
        if not self.alive:
            self.image.set_alpha(150)
            return
        
        if action == 0:
            self.rect.x -= constants.PLAYER_SPEED
        elif action == 1:
            self.rect.x += constants.PLAYER_SPEED
        elif action == 2:
            self.rect.y -= constants.PLAYER_SPEED
        elif action == 3:
            self.rect.y += constants.PLAYER_SPEED

        # Prevent the player from moving out of the screen
        if self.rect.left < 0:  # Left boundary
            self.rect.left = 0
        if self.rect.right > constants.SCREEN_WIDTH:  # Right boundary
            self.rect.right = constants.SCREEN_WIDTH
        if self.rect.top < 0:  # Top boundary
            self.rect.top = 0
        if self.rect.bottom > constants.SCREEN_HEIGHT:  # Bottom boundary
            self.rect.bottom = constants.SCREEN_HEIGHT