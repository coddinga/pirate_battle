import pygame
from pygame.sprite import Sprite

class Pirate(Sprite):
    #represents an enemy pirate
    def __init__(self, pb_game):
        #initialize and set position
        super().__init__()
        self.screen = pb_game.screen
        self.settings = pb_game.settings

        #load image and set rect attribute
        self.image = pygame.image.load('images/sloop1.bmp')
        self.rect = self.image.get_rect()

        #start at top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store position
        self.x = float(self.rect.x)

        #direction of row
        row_even = 0

    def edge_check(self):
        #True if pirate reached an edge
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
        #if self.rect.right >= self.screen.screen_width or self.rect.left <= 0:
            return True

    def update(self):
        #Move the pirate
        if self.row_even:
            self.x += (self.settings.pirate_speed * self.settings.fleet_direction)
        else:
            self.x -= (self.settings.pirate_speed * self.settings.fleet_direction)
        self.rect.x = self.x