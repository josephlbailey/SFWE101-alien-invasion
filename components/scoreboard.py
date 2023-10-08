from pygame import Surface, draw, transform
from pygame.font import Font

from components.gamestats import GameStats


class ScoreBoard:
    """ Class to handle rendering the scoreboard """

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.scoreboard_bg_rect = None

    def update_score(self, new_stats: GameStats):
        self._draw_bg()
        self._draw_scores(new_stats)

    def _draw_bg(self):
        """ Draw the gradient background on which the score will be displayed """
        scoreboard_bg = Surface((2, 2))
        draw.line(scoreboard_bg, (0, 0, 0), (0, 0), (0, 1))
        draw.line(scoreboard_bg, self.settings.bg_color, (1, 0), (1, 1))
        scoreboard_bg = transform.smoothscale(scoreboard_bg, (400, 65))

        self.scoreboard_bg_rect = scoreboard_bg.get_rect()
        self.scoreboard_bg_rect.left = self.screen.get_rect().left
        self.scoreboard_bg_rect.bottom = self.screen.get_rect().bottom
        self.screen.blit(scoreboard_bg, self.scoreboard_bg_rect)

    def _draw_scores(self, stats):
        """ Draw the score and ships remaining """
        # Create the font instance used to render the score text
        text = Font(None, 30)
        scoreboard_label_text = f'Aliens eliminated: {stats.aliens_eliminated_total}'
        label = text.render(scoreboard_label_text, 1, self.settings.game_board_text_color)

        label_rect = self.scoreboard_bg_rect
        label_rect.x += 15
        label_rect.y += 10

        # Draw the first line of the scoreboard text
        self.screen.blit(label, label_rect)

        scoreboard_label_text = f'Ships remaining: {stats.remaining_ships}'
        label = text.render(scoreboard_label_text, 1, self.settings.game_board_text_color)

        label_rect.y += 25

        # Draw the last line of the scoreboard label text
        self.screen.blit(label, label_rect)
