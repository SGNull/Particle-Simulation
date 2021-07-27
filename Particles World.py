from graphics import Point, Circle, GraphWin
import keyboard
from time import sleep
from random import random
from math import floor

# TODO: Figure out how to properly add a version number to the document.
# Window settings
WINDOW_NAME = "Particle Simulation 0.0.4"
WINDOW_DIMENSIONS = [900,700]

# Universe settings
SIM_DELAY = 0
BACKGROUND_COLOR = "black"
WRAP_AROUND = False

# Particle specific settings
PARTICLE_COUNT = 220
PARTICLE_SPEED = 10
PARTICLE_RADIUS = 5
PARTICLE_COLOR = "cyan"

# Important variables which should be global in scope.
Universe = []  # Global because it contains every object in the universe, which needs to be acted on in nearly every function
Running = True   # Global because it controls main, but also needs to be altered by key presses.

# Objects
class Particle():
    def __init__(self, xPos = 0, yPos = 0) -> None:
        self._pos = [xPos, yPos]
        self._prev = [0,0]
        self._vel = [0,0]
        self._graphic = Circle(Point(self._pos[0], self._pos[1]), PARTICLE_RADIUS)
        self._graphic.setFill(PARTICLE_COLOR)
        self._graphic.setOutline(PARTICLE_COLOR)
        self._is_drawn = False

    def set_velocity(self, deltaX, deltaY):
        self._vel = [deltaX, deltaY]

    def phys_update(self):

        #This goes at the end of any force calculations
        for i in range(2):
            new_pos = (self._pos[i] + self._vel[i]) % WINDOW_DIMENSIONS[i]

            if not WRAP_AROUND:
                ratio = (self._pos[i] + self._vel[i]) / WINDOW_DIMENSIONS[i]
                if floor(ratio) % 2 == 1:
                    new_pos = WINDOW_DIMENSIONS[i] - new_pos
                    self._vel[i] = -self._vel[i]

            self._pos[i] = new_pos

    def draw(self, window):
        if not self._is_drawn:
            self._graphic.draw(window)
            self._is_drawn = True
        else:
            self._graphic.move(self._pos[0] - self._prev[0], self._pos[1] - self._prev[1])

        self._prev[0] = self._pos[0]
        self._prev[1] = self._pos[1]
        

# Functions
def init_universe():
    for i in range(PARTICLE_COUNT):
        newParticle = Particle(random()*WINDOW_DIMENSIONS[0], random()*WINDOW_DIMENSIONS[1])
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

def print_info():
    print("")
    print(WINDOW_NAME)
    print("Running " + str(WINDOW_DIMENSIONS[0]) + "x" + str(WINDOW_DIMENSIONS[1]) + " with " + str(SIM_DELAY/1000) + " seconds of extra delay")
    print("Particle color: " + PARTICLE_COLOR + ". Background color: " + BACKGROUND_COLOR + ".")
    print("")

# Main
def main():
    print("Generating universe...")
    init_universe()
    window = GraphWin(WINDOW_NAME, WINDOW_DIMENSIONS[0], WINDOW_DIMENSIONS[1])
    window.setBackground(BACKGROUND_COLOR)

    print("Starting simulation. Close the window to exit the simulation.")
    global Running
    while Running and window.isOpen():
        sleep(SIM_DELAY/1000)
        phys_step()
        draw_universe(window)

    window.close()

# Example keyboard listener
#def stop_main(event):
#    global Running
#    Running = False
#keyboard.on_press_key("a", stop_main)

# Starting/Ending code
print_info()
main()
keyboard.unhook_all()
