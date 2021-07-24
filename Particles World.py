from graphics import Point, Circle, GraphWin
from time import sleep
from random import random

HEIGHT = 800
WIDTH = 1200
PSIZE = 5
SIMSPEED = 1
NUMPARTICLES = 3
MAXSPEED = 2

Universe = list

class Particle():
    def __init__(self, xPos = 0, yPos = 0) -> None:
        self._xPos = xPos
        self._yPos = yPos
        self._xPrev = 0
        self._yPrev = 0
        self._vel = [0,0]
        self._graphic = Circle(Point(self._xPos, self._yPos), PSIZE).setFill("black")
        self._drawn = False

    def set_velocity(self, deltaX, deltaY):
        self._vel = [deltaX, deltaY]

    def apply_velocity(self):
        self._xPos += self._vel[0]
        self._yPos += self._vel[1]

    def draw(self, window):
        if not self._drawn:
            self._graphic.draw(window)
            self._drawn = True
        else:
            self._graphic.move(self._xPos - self._xPrev, self._yPos - self._yPrev)
            
        self._xPrev = self._xPos
        self._yPrev = self._yPos
        

def init_universe():
    for i in range(NUMPARTICLES):
        newParticle = Particle(random()*WIDTH, random()*HEIGHT)
        newParticle.set_velocity(random()*MAXSPEED, random()*MAXSPEED)
        Universe.append()

def timestep():
    for particle in Universe:
        particle.applyVel()


def main():
    print("Generating universe...")
    init_universe()

    print("Starting simulation")
    running = True
    while running:
        sleep(1/(10*SIMSPEED))
        timestep()

main()