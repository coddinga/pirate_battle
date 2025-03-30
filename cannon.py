import pygame
from pygame.sprite import Sprite

class Cannon(Sprite):
    #manages cannons
    def __init__(self, pb_game):
        super().__init__()
        self.screen = pb_game.screen
        self.settings = pb_game.settings
        self.color = self.settings.cannon_color

        #cannon rect
        self.rect = pygame.Rect(0, 0, self.settings.cannon_width, self.settings.cannon_height)
        self.rect.midtop = pb_game.ship.rect.midtop

        #cannon position as a decimal
        self.y = float(self.rect.y)

    def update(self):
        #move cannons up
        self.y -= self.settings.cannon_speed
        #update rect
        self.rect.y = self.y

    def draw_cannon(self):
        pygame.draw.rect(self.screen, self.color, self.rect)