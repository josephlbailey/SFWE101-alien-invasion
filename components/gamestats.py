class GameStats:
    """ Class to track statistics about the game as it's being played """
    def __init__(self, ai_game):
        self.settings = ai_game.settings

        self.aliens_eliminated_total = 0
        self.game_active = True
        self.remaining_ships = self.settings.ship_limit
