import pygame.font

class Button:
    def __init__(self, pb_game, msg):
        #initialize button attributes
        self.screen = pb_game.screen
        self.screen_rect = self.screen.get_rect()

        #set dimentions and properties
        self.width, self.height = 200, 50
        self.button_color = (255, 255, 0)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 50)

        #build rect and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #button is prepped once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        #turn msg to rendered image and center text on bottom
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #draw button, then message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)