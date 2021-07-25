from graphics import Point, Circle, GraphWin
import keyboard
from time import sleep
from random import random

# TODO: Figure out how to properly add a version number to the document.
# Screen settings
SCREEN_NAME = "Particle Simulation 0.0.1"
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1200
SCREEN_COLOR = "black"

# Universe settings
SIM_SPEED = 3

# Particle specific settings
PARTICLE_COUNT = 3
PARTICLE_SPEED = 5
PARTICLE_SIZE = 5
PARTICLE_COLOR = "white"

# Important variables which should be global in scope.
Universe = []  # Global because it contains every object in the universe, which needs to be acted on in nearly every function
Running = True   # Global because it controls main, but also needs to be altered by key presses.

class Particle():
    def __init__(self, xPos = 0, yPos = 0) -> None:
        self._pos = [xPos, yPos]
        self._prev = [0,0]
        self._vel = [0,0]
        self._graphic = Circle(Point(self._pos[0], self._pos[1]), PARTICLE_SIZE)
        self._graphic.setFill("black")
        self._drawn = False

    def set_velocity(self, deltaX, deltaY):
        self._vel = [deltaX, deltaY]

    def phys_update(self):
        self._pos[0] = (self._pos[0] + self._vel[0]) % SCREEN_WIDTH
        self._pos[1] = (self._pos[1] + self._vel[1]) % SCREEN_HEIGHT

    def draw(self, window):
        # I was debating a lot on whether this single-use if-else statement is a good idea. It makes drawing the particles easier, but I was concerned about speed.
        # It costs us about 0.04 microseconds on average, probably less given predictive branching in the processor (just a guess, not sure how python->machine-code works).
        # Source: https://stackoverflow.com/questions/2522005/cost-of-exception-handlers-in-python
        if not self._drawn:
            self._graphic.draw(window)
            self._drawn = True
        else:
            self._graphic.move(self._pos[0] - self._prev[0], self._pos[1] - self._prev[1])

        self._prev[0] = self._pos[0]
        self._prev[1] = self._pos[1]
        

def init_universe():
    for i in range(PARTICLE_COUNT):
        newParticle = Particle(random()*SCREEN_WIDTH, random()*SCREEN_HEIGHT)
        newParticle.set_velocity(rand_between(-PARTICLE_SPEED, PARTICLE_SPEED), rand_between(-PARTICLE_SPEED, PARTICLE_SPEED))
        Universe.append(newParticle)

def phys_step():
    for particle in Universe:
        particle.phys_update()

def draw_universe(window):
    for particle in Universe:
        particle.draw(window)

def rand_between(start, end):
    output = random()*(end - start)
    output += start
    return output


def main():
    print("Generating universe...")
    init_universe()
    window = GraphWin(SCREEN_NAME, SCREEN_WIDTH, SCREEN_HEIGHT)

    print("Starting simulation. Press a to quit")
    global Running
    while Running:
        sleep(1/(10*SIM_SPEED))
        phys_step()
        draw_universe(window)

    window.close()

# THIS WORKS!!! AND IT ISN'T A COPYPASTE FROM STACKOVERFLOW!!
def stop_main(event):
    global Running
    Running = False
keyboard.on_press_key("a", stop_main)

# Starting/Ending code
main()
keyboard.unhook_all()