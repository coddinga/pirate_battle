import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from cannon import Cannon
from pirate import Pirate

class PirateBattle:
    """Overal class for the game"""

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("This is War!")

        #create games stats
        self.stats = GameStats(self)
        self.score = Scoreboard(self)
    
        self.ship = Ship(self)
        self.cannons = pygame.sprite.Group()
        self.pirates = pygame.sprite.Group()

        self._create_fleet()

        #make play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        #Start game loop
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_cannons()
                self._update_pirates()
            self._update_screen()

    def _check_events(self):
        #keyboard and mouse 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup(event)
    
    def _check_keydown(self, event):
        if event.key == pygame.K_RIGHT:
            #moves ship right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            #moves ship left
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_cannon()
        elif event.key == pygame.K_SPACE and not self.stats.game_active:
            mouse_pos = pygame.mouse.get_pos()
            self._check_play_button(mouse_pos)
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        #start new game when button is pressed
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if (button_clicked or pygame.K_SPACE) and not self.stats.game_active:
            #reset game settings
            self.settings.initialize_dynamic_settings()
            #Reset game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.score.prep_score()
            self.score.prep_level()
            self.score.prep_ships()

            #remove remaining objects
            self.pirates.empty()
            self.cannons.empty()

            #create fleet and csenter ship
            self._create_fleet()
            self.ship.center_ship()

            #hide mouse cursor
            pygame.mouse.set_visible(False)

    def _create_fleet(self):
        #make pirate
        pirate = Pirate(self)
        pirate_width, pirate_height = pirate.rect.size
        space_x = self.settings.screen_width - (2 * pirate_width)
        num_pirates_x = space_x // (2 * pirate_width)
        #rows of pirates
        ship_height = self.ship.rect.height
        space_y = (self.settings.screen_height - (8 * pirate_height) - ship_height)
        num_rows = space_y // (2 * pirate_height)

        #pirate fleet
        for row_num in range(num_rows):
            for pirate_num in range(num_pirates_x):
                self._create_pirate(pirate_num, row_num)

    def _fleet_edge_check(self):
        for pirate in self.pirates.sprites():
            check_edge = pirate.edge_check()
            if check_edge:
                #pirate.rect.y += self.settings.fleet_down_speed
                #self.settings.fleet_direction *= -1
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        #fleet moves forward and changes direction

        for pirate in self.pirates.sprites():
            pirate.rect.y += self.settings.fleet_down_speed
        self.settings.fleet_direction *= -1

    def _create_pirate(self, pirate_num, row_num):
            pirate = Pirate(self)
            if row_num != 0:
                #place in row
                pirate_width, pirate_height = pirate.rect.size
                pirate.x = pirate_width + 2 * pirate_width * pirate_num
                pirate.rect.x = pirate.x
                pirate.rect.y = pirate_height + 2 * pirate.rect.height * row_num
                pirate.row_even = row_num % 2
                #pirate.rect.y = pirate.y
                self.pirates.add(pirate)

    def _update_pirates(self):
        #is fleet at edge
        self._fleet_edge_check()
        #update position
        self.pirates.update()

        #check if ships collided
        if pygame.sprite.spritecollideany(self.ship, self.pirates):
            self._ship_sunk()

        #check if pirates reached the other end
        self._check_pirates_arrived()

    def _fire_cannon(self):
        #create and add cannon to the cannon group
        if len(self.cannons) < self.settings.cannons_fired:
            new_cannon = Cannon(self)
            self.cannons.add(new_cannon)

    def _update_cannons(self):
        #update position
        self.cannons.update()
        
        #cannons update
        for cannon in self.cannons.copy():
            if cannon.rect.bottom <= 0:
                self.cannons.remove(cannon)
        #print(len(self.cannons))
        self._check_collision()

    def _check_collision(self):
        #cannon hit the ship
        collisions = pygame.sprite.groupcollide(self.cannons, self.pirates, True, True)

        if collisions:
            for pirates in collisions.values():
                self.stats.score += self.settings.pirate_points * len(pirates)
            self.score.prep_score()
            self.score.check_high_score()

        if not self.pirates:
            #destroy cannons and create a new fleet
            self.cannons.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #increase level
            self.stats.level += 1
            self.score.prep_level()

    def _check_pirates_arrived(self):
        #check if pirates reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for pirate in self.pirates.sprites():
            if pirate.rect.bottom >= screen_rect.bottom:
                #same as if ship sunk
                self._ship_sunk()
                break

    def _update_screen(self):
        #redraw screen
        self.screen.fill(self.settings.bd_color)
        self.ship.blitme()
        for cannon in self.cannons.sprites():
            cannon.draw_cannon()
        self.pirates.draw(self.screen)

        #draw score info
        self.score.show_score()

        #draw play button when game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        
        #view most recent screen
        pygame.display.flip()

    def _ship_sunk(self):
        if self.stats.ships_left > 0:
            #decrease ships left and update scoreboard
            self.stats.ships_left -= 1
            self.score.prep_ships()

            #remove all remaining ships and cannons
            self.pirates.empty()
            self.cannons.empty()

            #create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)
        
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

if __name__ == '__main__':
    #make game instance and run game
    pb = PirateBattle()
    pb.run_game()