class Settings:
    """ A class to store all settings for Alien Invasion """

    def __init__(self):
        """ Initialise the game settings """
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 17, 51)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings
        # Bullets travel slower than the ship
        self.bullet_speed = 1.5
        # Bullets are 3 pixels wide
        self.bullet_width = 3
        # Bullets are 15 pixels high
        self.bullet_height = 15
        # Bullets are dark grey
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        # Fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
