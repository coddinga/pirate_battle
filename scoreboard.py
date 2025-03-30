import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    #Initialize
    def __init__(self, pb_game):
        self.pb_game = pb_game
        self.screen = pb_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = pb_game.settings
        self.stats = pb_game.stats

        #scoring info settings
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 40)

        #initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        #make image
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bd_color)

        #top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        #make image
        with open(self.stats.filename) as f:
            high_score = round(int(f.read()), -1)
            
        #high_score = round(self.stats.score, -1)
        high_score_str = "High Score: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bd_color)

        #top middle of screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        #draw to screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen) #draw level of ships to screen

    def check_high_score(self):
        #check if high score has been passed
        if self.stats.score > self.stats.high_score:
            with open(self.stats.filename, 'w') as f:
                f.write(str(self.stats.score))
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        #turn level into rendered image
        level_str = "Level: " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bd_color)

        #level is below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_num in range(self.stats.ships_left):
            ship = Ship(self.pb_game)
            ship.rect.x = 10 + ship_num * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)