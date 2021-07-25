from graphics import Point, Circle, GraphWin
from time import sleep
from random import random

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1200
SIM_SPEED = 1
PARTICLE_COUNT = 3
PARTICLE_SPEED = 2
PARTICLE_SIZE = 5

Universe = list

class Particle():
    def __init__(self, xPos = 0, yPos = 0) -> None:
        self._pos = [xPos, yPos]
        self._prev = [0,0]
        self._vel = [0,0]
        self._graphic = Circle(Point(self._pos[0], self._pos[1]), PARTICLE_SIZE).setFill("black")
        self._drawn = False

    def set_velocity(self, deltaX, deltaY):
        self._vel = [deltaX, deltaY]

    def phys_update(self):
        self._pos[0] = (self._pos[0] + self._vel[0]) % SCREEN_WIDTH
        self._pos[1] = (self._pos[1] + self._vel[1]) % SCREEN_HEIGHT

    def draw(self, window):
        # This one-time if-else statement costs us about 0.04 microseconds on average, probably less given processor optimizations (prediction algorithms).
        # Source: https://stackoverflow.com/questions/2522005/cost-of-exception-handlers-in-python
        if not self._drawn:
            self._graphic.draw(window)
            self._drawn = True
        else:
            self._graphic.move(self._xPos - self._xPrev, self._yPos - self._yPrev)

        self._prev[0] = self._pos[0]
        self._prev[1] = self._pos[1]
        

def init_universe():
    for i in range(PARTICLE_COUNT):
        newParticle = Particle(random()*SCREEN_WIDTH, random()*SCREEN_HEIGHT)
        newParticle.set_velocity(random()*PARTICLE_SPEED, random()*PARTICLE_SPEED)
        Universe.append()

def phys_step():
    for particle in Universe:
        particle.phys_update()

def draw_universe(window):
    for particle in Universe:
        particle.draw(window)


def main():
    print("Generating universe...")
    init_universe()
    window = GraphWin(SCREEN_WIDTH, SCREEN_HEIGHT)

    print("Starting simulation")
    running = True
    while running:
        sleep(1/(10*SIM_SPEED))
        phys_step()
        draw_universe(window)


main()