class Settings:
    def __init__(self):
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bd_color = (0, 162, 232) #Backdrop
        #self.speed = 0

        #ship speed
        self.ship_limit = 3

        #cannon settings
        self.cannon_width = 10
        self.cannon_height = 5
        self.cannon_color = (60, 60, 60)
        self.cannons_fired = 10 #max cannons allowed

        #pirate settings
        self.fleet_down_speed = 10

        self.speedup_scale = 1.1

        #pirate point value increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.0
        self.cannon_speed = 0.1
        self.pirate_speed = .3
        
        #direction 1 is right, -1 is left
        self.fleet_direction = 1

        #scoring
        self.pirate_points = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.cannon_speed *= self.speedup_scale
        self.pirate_speed *= self.speedup_scale

        #increase point and speed
        self.pirate_points = int(self.pirate_points * self.score_scale)
        #print(self.pirate_points)
