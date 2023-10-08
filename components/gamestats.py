class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings

        self.level = 1
        self.aliens_eliminated_total = 0
        self.game_active = True
        self.ships_left = self.settings.ship_limit

    def new_level(self):
        self.level += 1
