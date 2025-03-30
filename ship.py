import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, pb_game):
        #initialize ship
        super().__init__()
        self.screen = pb_game.screen
        self.settings = pb_game.settings
        self.screen_rect = pb_game.screen.get_rect()

        #Load ship and get rectangle
        self.image = pygame.image.load('images/ship1.bmp')
        self.rect = self.image.get_rect()

        #set ship to bottom center
        self.rect.midbottom = self.screen_rect.midbottom

        #horizontal position of ship is a float
        self.x = float(self.rect.x)

        #check if moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #update ship position in the direction of keyprress
        if self.moving_right and self.rect.right < self.screen_rect.right: #make sure ship doesn't move off screen
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0: #make sure ship doesn't move off screen
            self.x -= self.settings.ship_speed

        #update rect
        self.rect.x = self.x

    def blitme(self):
        #draw ship
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        #set ship to bottom center
        self.rect.midbottom = self.screen_rect.midbottom

        #horizontal position of ship is a float
        self.x = float(self.rect.x)