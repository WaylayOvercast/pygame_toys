from re import A
import pygame
import Assets
import Function




class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel
    
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return Function.collide(obj, self)
    
    def get_width(self):
        return self.img.get_width() #might not work




class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down = 0
    
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(Assets.WINDOW_SIZE[1]):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down >= self.COOLDOWN:
            self.cool_down = 0
        elif self.cool_down > 0:
            self.cool_down += 1

    def shoot(self):
        if self.cool_down == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.sprites = [Assets.YELLOW_SPACE_SHIP, Assets.YELLOW_SPACE_SHIP_KNOCKOUT]
        self.current_sprite = 0.0
        self.ship_img = self.sprites[int(self.current_sprite)]
        self.laser_img = Assets.YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score = 0

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(Assets.WINDOW_SIZE[1]):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.score += 80
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    
    #def knockout(self, time):
        #needs work

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (0,Assets.WINDOW_SIZE[1]-20,Assets.WINDOW_SIZE[0], 20)) # both need work
        pygame.draw.rect(window, (0,255,0), (0, Assets.WINDOW_SIZE[1]-20, Assets.WINDOW_SIZE[0] * (self.health / self.max_health), 20)) 


class Enemy(Ship):
    COLOR_MAP = {
        "red": (Assets.RED_SPACE_SHIP, Assets.RED_LASER),
        "green": (Assets.GREEN_SPACE_SHIP, Assets.GREEN_LASER),
        "blue": (Assets.BLUE_SPACE_SHIP, Assets.BLUE_LASER),
    }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel):
        self.y += vel
    
    def shoot(self):
        if self.cool_down == 0:
            laser = Laser((self.x - self.laser_img.get_width()/2) + self.ship_img.get_width()/2 , self.y, self.laser_img) #WINDOW_SIZE[0]/2 - lost_label.get_width()/2 needs to be centered
            self.lasers.append(laser)
            self.cool_down = 1


class Health:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health_img = Assets.HEALTH_CANISTER
        self.mask = pygame.mask.from_surface(self.health_img)

    def move(self, vel):
        self.y += vel

    def draw(self, window):
        window.blit(self.health_img, (self.x, self.y))
    
    def get_width(self):
        return self.health_img.get_width()

    def get_height(self):
        return self.health_img.get_height()