import sys
from time import sleep

import pygame

from components.alien import Alien
from components.bullet import Bullet
from components.gamestats import GameStats
from components.scoreboard import ScoreBoard
from components.ship import Ship
from config.settings import Settings


class AlienInvasion:
    # Overall class to manage game assets and behavior

    def __init__(self):
        # Initialize the game, and create game resources
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Joseph\'s Alien Invasion")

        self.stats = GameStats(self)

        self.scoreboard = ScoreBoard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        # Start the main loop for the game

        while True:
            # Call method to check for keyboard events
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_screen()

    def _check_events(self):
        """ Respond to key presses and mouse events"""
        for event in pygame.event.get():
            # Did the player quit the game?
            if event.type == pygame.QUIT:
                sys.exit()
            # Did the player press a key?
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # Did the player release a key?
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # Is the key the right arrow or is it the left arrow?
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # Did the player hit the Q key to quit the game?
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        # Did the player stop holding down either arrow key?
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # Update positions of the bullets and get rid of old bullets
        self.bullets.update()

        # Get rid of bullets that have disappeared off the screen because they still exist in the game and take up
        # memory and execution time
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        self.stats.aliens_eliminated_total += len(collisions.values())

        # All aliens have been eliminated, new level
        if not self.aliens:
            # Make the aliens slightly faster each level
            self.settings.alien_speed *= 1.15
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """ Create the fleet of aliens"""
        # Make a single alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Determine the available screen space for aliens
        available_space_x = self.settings.screen_width - (2 * alien_width)
        alien_count = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        row_count = min(available_space_y // (2 * alien_height), 5)

        for row_number in range(row_count):
            for alien_number in range(alien_count):
                self._create_alien(alien_number, row_number)

        self.stats.initial_alien_count = len(self.aliens)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2 * alien_width * alien_number)
        alien.rect.x = alien.x
        alien.rect.y = alien_height + (2 * alien.rect.height * row_number)
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _ship_hit(self):

        if self.stats.remaining_ships > 0:
            self.stats.remaining_ships -= 1

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        # Redraw the screen each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Make the most recently drawn screen visible

        self.aliens.draw(self.screen)
        self.scoreboard.update_score(self.stats)
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()

quit()
