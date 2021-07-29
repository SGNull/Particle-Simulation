from graphics import Point, Circle, GraphWin
import keyboard
from time import sleep
from random import random, randint
from math import floor, sqrt

# TODO: Figure out how to properly add a version number to the document.
# Window settings
WINDOW_NAME = "Particle Simulation 0.1.0"
WINDOW_DIMENSIONS = (900,700)

# Universe settings
SIM_DELAY_MS = 0
WRAP_AROUND = False

# Particle specific settings
PARTICLE_COUNT = 50
PARTICLE_SPEED = 10
PARTICLE_RADIUS = 5

# Particle interactions settings
COLOR_COUNT = 3
MAX_FORCE_STRENGTH = 1
MAX_NORMAL_FORCE = 10
FORCE_START_RATIO = 3/4

#Aesthetics settings
PARTICLE_COLORS = ["cyan", "red", "yellow", "magenta", "blue", "purple", "green", "orange", "pink", "gray", "brown", "white"]
BACKGROUND_COLOR = "black"
PARTICLE_OUTLINE = False


# Important variables which should be global in scope.
Universe = []
Interactions_Matrix = []
Running = True

# The main component equations for the force (THESE PROBABLY NEED ADJUSTED)
normal_mult = lambda distance, radius: sqrt(-distance/radius + 1)
weak_force_mult = lambda distance, radius, ratio: (distance - (radius*ratio))/(radius*(1 - ratio))
force_mult = lambda distance, radius: 1/(distance - radius + 1)


# Objects
class Particle():
    def __init__(self, xPos = 0, yPos = 0, color = 0) -> None:
        self._pos = [xPos, yPos]
        self._prev = [0,0]
        self._vel = [0,0]
        self._radius = PARTICLE_RADIUS
        self._color = color
        self._graphic = Circle(Point(self._pos[0], self._pos[1]), self._radius)
        self._graphic.setFill(PARTICLE_COLORS[color])

        if not PARTICLE_OUTLINE:
            self._graphic.setOutline(PARTICLE_COLORS[color])

        self._is_drawn = False

    # Getters and Setters
    def set_velocity(self, deltaX, deltaY):
        self._vel = [deltaX, deltaY]
    def get_pos(self):
        return self._pos
    def get_color(self):
        return self._color

    # Physics
    def interact_with_particle(self, other_particle):   # This has a certain smell to it. It feels like this function might be doing too much. Ex: the if, elif, else statement
        distance = get_particle_distance(self, other_particle)
        interaction_force = Interactions_Matrix[self._color][other_particle.get_color()]

        if distance <= self._radius * FORCE_START_RATIO:
            net_force = normal_mult(distance, self._radius) * MAX_NORMAL_FORCE
        elif distance <= self._radius:
            net_force = normal_mult(distance, self._radius) * MAX_NORMAL_FORCE + weak_force_mult(distance, self._radius, FORCE_START_RATIO) * interaction_force
        else:
            net_force = force_mult(distance, self._radius) * interaction_force
        
        other_pos = other_particle.get_pos()
        norm_vector = ((other_pos[0] - self._pos[0])/distance, (other_pos[1] - self._pos[1])/distance)

        self._vel[0] += norm_vector[0] * net_force
        self._vel[1] += norm_vector[1] * net_force

    def position_update(self):   # This comes after all force calculations
        for i in range(2):
            new_pos = (self._pos[i] + self._vel[i]) % WINDOW_DIMENSIONS[i]

            if not WRAP_AROUND:
                ratio = (self._pos[i] + self._vel[i]) / WINDOW_DIMENSIONS[i]
                if floor(ratio) % 2 == 1:
                    new_pos = WINDOW_DIMENSIONS[i] - new_pos
                    self._vel[i] = -self._vel[i]

            self._pos[i] = new_pos

    # Graphics
    def draw(self, window):
        if not self._is_drawn:
            self._graphic.draw(window)
            self._is_drawn = True
        else:
            self._graphic.move(self._pos[0] - self._prev[0], self._pos[1] - self._prev[1])

        self._prev[0] = self._pos[0]
        self._prev[1] = self._pos[1]


# Functions
rand_mag = lambda x : 2*x*random() - x

def init_universe():
    for i in range(PARTICLE_COUNT):
        newParticle = Particle(random()*WINDOW_DIMENSIONS[0], random()*WINDOW_DIMENSIONS[1], randint(0, COLOR_COUNT - 1))
        newParticle.set_velocity(rand_mag(PARTICLE_SPEED), rand_mag(PARTICLE_SPEED))
        Universe.append(newParticle)

def init_colorp_field():
    for i in range(COLOR_COUNT):
        new_row = []
        for j in range(COLOR_COUNT):
            new_row.append(rand_mag(MAX_FORCE_STRENGTH))
        Interactions_Matrix.append(new_row)

def phys_step():
    for aparticle in Universe:
        for bparticle in Universe:
            if aparticle != bparticle:
                aparticle.interact_with_particle(bparticle)
        aparticle.position_update()

def draw_universe(window):
    for particle in Universe:
        particle.draw(window)

def get_particle_distance(aparticle, bparticle):
    apos = aparticle.get_pos()
    bpos = bparticle.get_pos()
    x_dist_squared = (bpos[0] - apos[0])**2
    y_dist_squared = (bpos[1] - apos[1])**2
    return sqrt(x_dist_squared + y_dist_squared)

def print_info():
    print("")
    print(WINDOW_NAME)
    print("Running " + str(WINDOW_DIMENSIONS[0]) + "x" + str(WINDOW_DIMENSIONS[1]) + " with " + str(SIM_DELAY_MS/1000) + " seconds of extra delay")
    print("Number of colors: " + str(COLOR_COUNT) + "Background color: " + BACKGROUND_COLOR + ".")
    print("")

# Main
def main():
    print_info()

    print("Generating universe...")
    init_universe()
    init_colorp_field()

    window = GraphWin(WINDOW_NAME, WINDOW_DIMENSIONS[0], WINDOW_DIMENSIONS[1])
    window.setBackground(BACKGROUND_COLOR)

    print("Starting simulation. Close the window to exit the simulation.")
    global Running
    while Running and window.isOpen():
        sleep(SIM_DELAY_MS/1000)
        phys_step()
        draw_universe(window)

    window.close()

# Example keyboard listener
#def stop_main(event):
#    global Running
#    Running = False
#keyboard.on_press_key("a", stop_main)

# Code which MUST fall outside of functions
main()
keyboard.unhook_all()
