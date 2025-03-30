class GameStats:
    #game statistics
    def __init__(self, pb_game):
        self.settings = pb_game.settings
        self.reset_stats()
        #starts in active state
        self.game_active = False

        #remember high score
        self.filename = 'high_score.txt'
        with open(self.filename) as f:
            self.high_score = int(f.read())

    def reset_stats(self):
        #initialize stats 
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
