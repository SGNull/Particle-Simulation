VERSION_NUMBER = "0.6.0"

from graphics import Point, Circle, GraphWin
from time import perf_counter, perf_counter_ns
from random import random, randint
from math import sqrt
import numpy as np

# Window settings
WINDOW_NAME = "Particle Simulation " + VERSION_NUMBER
WIN_DIM = np.array([1000,800])

# Universe settings
WRAP_AROUND = True
COLOR_COUNT = 4
FRICTION = 0.1

# Particle specific settings
PARTICLE_COUNT = 80
PARTICLE_RADIUS = 5.5

# Particle force settings
MAX_FORCE_STRENGTH = 1
MAX_NORMAL_FORCE = 10
MIN_FORCE_START = PARTICLE_RADIUS * 2.2
MAX_FORCE_START = PARTICLE_RADIUS * 3.5
MIN_FORCE_DIST = 30
MAX_FORCE_DIST = 200

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

    # Physics
    def position_update(self):   # This comes after all force calculations
        new_pos = np.mod(self.pos + self.vel, WIN_DIM)

        if not WRAP_AROUND:
            ratios = (self.pos + self.vel) // WIN_DIM
            for i in range(2):
                if ratios[i] % 2 == 1:
                    new_pos[i] = WIN_DIM[i] - new_pos[i]

        self.pos = new_pos
        self.vel = self.vel*(1-FRICTION)

        self.graphic.move(self.vel[0], self.vel[1])

    # Graphics
    def draw(self, window):
        self.graphic.draw(window)

# Functions
rand_mag = lambda x : 2*x*random() - x
rand_range = lambda start, end: (end-start)*random()+start
sign_of_int = lambda a: int(a>0) - int(a<0)   # SO ref: https://www.quora.com/How-do-I-get-sign-of-integer-in-Python
mag_of_v = lambda x: sqrt(x[0]**2 + x[1]**2)

# The main component equations for the force, recreated from the image shown in Code Parade's video
# Desmos graph: https://www.desmos.com/calculator/ubemfmpbg6
normal_equation = lambda distance, contact_radius: -sqrt(distance)/sqrt(contact_radius) + 1
force_equation = lambda distance, contact_radius, force_distance: -(2)/distance*abs(distance-contact_radius-force_distance/2) + 1

def observe_slice(pie_slice):
    part_a = pie_slice[0]
    part_b = pie_slice[1]

    dist_vect = part_b.pos - part_a.pos
    intr_a = Interactions_Matrix[part_a.color][part_b.color]
    intr_b = Interactions_Matrix[part_b.color][part_a.color]

    if WRAP_AROUND:
            for i, dim in enumerate(dist_vect):
                if abs(dim) > WIN_DIM[i]/2:   # If this is true, the other direction is shorter
                    dist_vect[i] = (WIN_DIM[i] - abs(dim)) * sign_of_int(dim)   # Go around the other direction
    
    distance = mag_of_v(dist_vect)

    if distance < intr_a[1] + intr_a[2]:
        # Do part_a calculations
        norm_vect = -dist_vect/distance
        if (distance < intr_a[1]):
            force = MAX_NORMAL_FORCE * normal_equation(distance,intr_a[1])
        else:
            force = intr_a[0] * force_equation(distance, intr_a[1], intr_a[2])
        
        part_a.vel = part_a.vel + force*norm_vect

    if distance < intr_b[1] + intr_b[2]:
        # Do part_b calculations
        norm_vect = dist_vect/distance
        if (distance < intr_b[1]):
            force = MAX_NORMAL_FORCE * normal_equation(distance,intr_b[1])
        else:
            force = intr_b[0] * force_equation(distance, intr_b[1], intr_b[2])
        
        part_b.vel = part_b.vel + force*norm_vect

def init_universe():
    for i in range(PARTICLE_COUNT):
        newParticle = Particle(random()*WIN_DIM[0], random()*WIN_DIM[1], randint(0, COLOR_COUNT - 1))
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
    print("Running " + str(WIN_DIM[0]) + "x" + str(WIN_DIM[1]))
    print("Number of colors: " + str(COLOR_COUNT) + " Background color: " + BACKGROUND_COLOR + ".")
    print("")

# Main
def main():
    print_info()

    print("Generating universe...")
    init_universe()
    init_interactions_matrix()

    window = GraphWin(WINDOW_NAME, WIN_DIM[0], WIN_DIM[1])
    window.setBackground(BACKGROUND_COLOR)

    print("Baking a pie...")
    bake_universe_pie()

    print("Starting simulation. Close the window to exit the simulation.")
    
    for particle in Universe:
        particle.draw(window)

    global Running
    time_start = perf_counter()
    while Running and window.isOpen():
        for slice in Universe_Pie:
            observe_slice(slice)

        for particle in Universe:
            particle.position_update()

    time_end = perf_counter()
    window.close()
    print("Elapsed time: " + str(time_end - time_start))

# Example keyboard listener
#def stop_main(event):
#    global Running
#    Running = False
#keyboard.on_press_key("a", stop_main)

# Code which MUST fall outside of functions
main()
