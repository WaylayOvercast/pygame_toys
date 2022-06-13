import pygame as pg
import win32api
import random
import math

vec2, vec3 = pg.math.Vector2, pg.math.Vector3

RES = WIDTH, HEIGHT = 1600, 900
NUM_STARS = 2400
CENTER = vec2(WIDTH // 2, HEIGHT // 2)
COLORS = 'red green blue orange purple cyan'.split()
Z_DIST = 40

class Star:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3d = self.fetch_pos3d()
        self.vel = random.uniform(0.05, 0.25)
        self.color = random.choice(COLORS)
        self.screen_pos = vec2(0, 0)
        self.size = 10

    def fetch_pos3d(self, scale_pos = 35):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // scale_pos, HEIGHT) * scale_pos
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, Z_DIST)

    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = self.fetch_pos3d() if self.pos3d.z < 1 else self.pos3d
        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (Z_DIST - self.pos3d.z) / (0.2 * self.pos3d.z)

    def draw(self):
        pg.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))

class Starfield:
    def __init__(self, app):
        self.stars = [Star(app) for x in range(NUM_STARS)]

    def run(self):
        [star.update() for star in self.stars]
        self.stars.sort(key= lambda star: star.pos3d.z, reverse= True)
        [star.draw() for star in self.stars]


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.starfield = Starfield(self)

    def fetchRefreshRate(device):
        try:
            rate = getattr(win32api.EnumDisplaySettings(device.DeviceName, -1), 'DisplayFrequency')

        except Exception as e:
            rate = 30
        return rate

    def run(self):
        while True:
            self.screen.fill('black')
            self.starfield.run()

            pg.display.flip()
            [exit() for x in pg.event.get() if x.type == pg.QUIT]
            self.clock.tick(App.fetchRefreshRate(win32api.EnumDisplayDevices()))

if __name__ == '__main__':
    app = App()
    app.run()
