import sys

import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    # Overall class to manage game assets and behavior

    def __init__(self):
        # Initialize the game, and create game resources
        pygame.init()
        self.settings = Settings()
        # TODO: Replace this with pygame.FULLSCREEN before submitting the final version
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Joseph\'s Alien Invasion")

        self.ship = Ship(self)

    def run_game(self):
        # Start the main loop for the game

        while True:
            # Call method to check for keyboard events
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        """ Respond to key presses and mouse events"""
        for event in pygame.event.get():
            is_keydown = event.type == pygame.KEYDOWN

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

    def _check_keyup_events(self, event):
        # Did the player stop holding down either arrow key?
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        # Redraw the screen each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()

quit()
