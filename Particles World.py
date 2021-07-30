from graphics import Point, Circle, GraphWin
from time import perf_counter_ns
from random import random, randint
from math import sqrt
import numpy as np

# TODO: Figure out how to properly add a version number to the document.
# Window settings
WINDOW_NAME = "Particle Simulation 0.5.0"
WINDOW_DIMENSIONS = np.array([1000,800])

# Universe settings
WRAP_AROUND = True
COLOR_COUNT = 4
FRICTION = 0.07

# Particle specific settings
PARTICLE_COUNT = 50
PARTICLE_RADIUS = 5

# Particle force settings
MAX_FORCE_STRENGTH = 0.7
MAX_NORMAL_FORCE = 10
MIN_FORCE_START = PARTICLE_RADIUS * 2.2
MAX_FORCE_START = PARTICLE_RADIUS * 3.5
MIN_FORCE_DIST = 30
MAX_FORCE_DIST = 130

#Aesthetics settings
PARTICLE_COLORS = ["cyan", "red", "yellow", "magenta", "blue", "purple", "green", "orange", "pink", "gray", "brown", "white"]
BACKGROUND_COLOR = "black"
PARTICLE_OUTLINE = False


# Important variables which should be global in scope.
Universe = []
Universe_Pie = []
Interactions_Matrix = []   # Format: (force_magnitude, force_start, force_length)
Running = True


# Objects
class Particle():
    def __init__(self, xPos = 0, yPos = 0, color = 0) -> None:
        self.pos = np.array([xPos, yPos])
        self.prev = np.array([0,0])
        self.vel = np.array([0,0])
        self.radius = PARTICLE_RADIUS
        self.color = color
        self.graphic = Circle(Point(self.pos[0], self.pos[1]), self.radius)
        self.graphic.setFill(PARTICLE_COLORS[color])

        if not PARTICLE_OUTLINE:
            self.graphic.setOutline(PARTICLE_COLORS[color])

        self.is_drawn = False

    # Physics
    def interact_with_particle(self, other_particle):
        distance_vector = other_particle.pos - self.pos
        interaction = Interactions_Matrix[self.color][other_particle.color]

        if WRAP_AROUND:
            for i, dim in enumerate(distance_vector):
                if abs(dim) > WINDOW_DIMENSIONS[i]/2:   # If this is true, the other direction is shorter
                    distance_vector[i] = (WINDOW_DIMENSIONS[i] - abs(dim)) * sign_of_int(dim)   # Go around the other direction

        distance = mag_of_v(distance_vector)
        if distance < interaction[1] + interaction[2]:
            norm_vector = distance_vector/distance
            if (distance < interaction[1]):
                net_force = MAX_NORMAL_FORCE * normal_equation(distance,interaction[1])
            else:
                net_force = interaction[0] * force_equation(distance, interaction[1], interaction[2])

            self.vel = self.vel - net_force*norm_vector

    def position_update(self):   # This comes after all force calculations
        new_pos = np.mod(self.pos + self.vel, WINDOW_DIMENSIONS)

        if not WRAP_AROUND:
            ratios = (self.pos + self.vel) // WINDOW_DIMENSIONS
            for i in range(2):
                if ratios[i] % 2 == 1:
                    new_pos[i] = WINDOW_DIMENSIONS[i] - new_pos[i]
        self.pos = new_pos
        self.vel = self.vel*(1-FRICTION)

    # Graphics
    def draw(self, window):
        if not self.is_drawn:
            self.graphic.draw(window)
            self.is_drawn = True
        else:
            self.graphic.move(self.pos[0] - self.prev[0], self.pos[1] - self.prev[1])

        self.prev = np.copy(self.pos)


# Functions
rand_mag = lambda x : 2*x*random() - x
rand_range = lambda start, end: (end-start)*random()+start
sign_of_int = lambda a: int(a>0) - int(a<0)   # SO ref: https://www.quora.com/How-do-I-get-sign-of-integer-in-Python
mag_of_v = lambda x: sqrt(x[0]**2 + x[1]**2)

# The main component equations for the force, recreated from the image shown in Code Parade's video
# Desmos graph: https://www.desmos.com/calculator/ubemfmpbg6
normal_equation = lambda distance, contact_radius: -sqrt(distance)/sqrt(contact_radius) + 1
force_equation = lambda distance, contact_radius, force_distance: -(2)/distance*abs(distance-contact_radius-force_distance/2) + 1

def init_universe():
    for i in range(PARTICLE_COUNT):
        newParticle = Particle(random()*WINDOW_DIMENSIONS[0], random()*WINDOW_DIMENSIONS[1], randint(0, COLOR_COUNT - 1))
        Universe.append(newParticle)

def init_interactions_matrix():
    for i in range(COLOR_COUNT):
        new_row = []
        for j in range(COLOR_COUNT):
            force_mag = rand_mag(MAX_FORCE_STRENGTH)
            force_start = rand_range(MIN_FORCE_START, MAX_FORCE_START)
            force_distance = rand_range(MIN_FORCE_DIST, MAX_FORCE_DIST)
            new_row.append((force_mag, force_start, force_distance))
        Interactions_Matrix.append(new_row)

def bake_universe_pie():
    for i in range(len(Universe)):
        for j in range(i +1, len(Universe)):
            Universe_Pie.append((Universe[i],Universe[j]))

def print_info():
    print("")
    print(WINDOW_NAME)
    print("Running " + str(WINDOW_DIMENSIONS[0]) + "x" + str(WINDOW_DIMENSIONS[1]))
    print("Number of colors: " + str(COLOR_COUNT) + " Background color: " + BACKGROUND_COLOR + ".")
    print("")

# Main
def main():
    print_info()

    print("Generating universe...")
    init_universe()
    init_interactions_matrix()

    window = GraphWin(WINDOW_NAME, WINDOW_DIMENSIONS[0], WINDOW_DIMENSIONS[1])
    window.setBackground(BACKGROUND_COLOR)

    print("Baking a pie...")
    bake_universe_pie()

    print("Starting simulation. Close the window to exit the simulation.")
    global Running
    while Running and window.isOpen():
        for slice in Universe_Pie:
            slice[0].interact_with_particle(slice[1])
            slice[1].interact_with_particle(slice[0])

        for particle in Universe:
            particle.position_update()
            particle.draw(window)
    window.close()

# Example keyboard listener
#def stop_main(event):
#    global Running
#    Running = False
#keyboard.on_press_key("a", stop_main)

# Code which MUST fall outside of functions
main()
