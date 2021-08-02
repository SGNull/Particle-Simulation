# Imports
from time import perf_counter
from tkinter import Tk, Canvas
import Vector2Math as VMath
from random import random, randint
from math import sqrt



# Settings
VERSION = "1.1.2"
WIN_DIMS = [800,660]
WIN_COLOR = "black"

WRAP_AROUND = True
TESTING = False         # Whether to exit the program after a specified number of steps
TEST_STEPS = 300        # The amount of steps to run before exiting
TIME_STEP_MS = 1        # The time between steps (has to be 1 or Tkinter will meltdown)
PARTICLE_COUNT = 201    # The total number of particles in the universe (as of v1.1.1, this should be about 265 at most)
PARTICLE_RADIUS = 5.2   # The visual radius of the particles (does not affect physics calculations by default)
COLORS = 5              # The number of different colors (interactions are defined by color, ie. (red,blue) is different from (blue,red))

MAX_CONTACT_DIST = 20   # Maximum distance that particles will make contact
MIN_CONTACT_DIST = 12   # Minimum distance that particles will make contact
NORMAL_FORCE = 15       # How "hard" particles make contact
REPULSE_MAX = 3		    # Maximum repulsive force
ATTRACT_MAX = 2	    # Maximum attractive force
MAX_FORCE_DIST = MAX_CONTACT_DIST + 80  # Maximum distance that the particles will interact
MIN_FORCE_DIST = MAX_CONTACT_DIST + 30  # Minimum distance that the particles will interact at
FRICTION = 0.45          # Friction is really important, actually. Without a sufficient friction value, the universe will be too energetic to be interesting.
#                       # Velocity is multiplied by (1-FRICTION) each step.



# Global variables
Universe = []
Universe_Pie = []
Interactions_Matrix = []   # Format: (force_magnitude, force_start, force_end)
Color_List = ['red', 'green', 'blue', 'cyan', 'yellow', 'magenta', 'orange', 'purple', 'white']
Steps = 0

# init canvas
root = Tk()
my_canvas = Canvas(root, height=WIN_DIMS[1], width=WIN_DIMS[0], bg=WIN_COLOR)
my_canvas.pack()



# Particle object (really convenient if it's here and not in a seperate file cause of all the settings)
class Particle (object):
    '''The main object for the simulation'''
    def __init__(self, pos, color):
        self.pos = list(pos)
        self.color = color
        self.radius = PARTICLE_RADIUS
        self.vel = [0,0]
        self.graphic = my_canvas.create_oval(pos[0]-self.radius, pos[1]-self.radius, pos[0]+self.radius, pos[1]+self.radius, outline=Color_List[color])

# Functions
rand_mag = lambda x : 2*x*random() - x   # Returns a random number between -x and x
rand_range = lambda start, end: (end-start)*random()+start
sign_of_int = lambda a: int(a>0) - int(a<0)   # SO ref: https://www.quora.com/How-do-I-get-sign-of-integer-in-Python

# The main component equations for the force, recreated from the image shown in Code Parade's video
# Desmos graph: https://www.desmos.com/calculator/ubemfmpbg6
normal_equation = lambda distance, contact_radius: -sqrt(distance)/sqrt(contact_radius) + 1
force_equation = lambda distance, contact_dst, force_dst: -2/(force_dst-contact_dst)*abs(distance-(contact_dst+force_dst)/2)+1

def Export_Universe():
    pass

def Import_Universe():
    pass

def Init_Universe():
    for i in range(PARTICLE_COUNT):
        random_pos = [random()*WIN_DIMS[0], random()*WIN_DIMS[1]]
        color = randint(0,COLORS-1)
        new_particle = Particle(random_pos, color)
        Universe.append(new_particle)

def Init_Interactions_Matrix():
    for i in range(COLORS):
        new_row = []
        for j in range(COLORS):
            force = rand_range(-ATTRACT_MAX, REPULSE_MAX)
            contact = rand_range(MIN_CONTACT_DIST, MAX_CONTACT_DIST)
            force_range = rand_range(contact,MAX_FORCE_DIST)
            new_interaction = (force, contact, force_range)
            new_row.append(new_interaction)
        Interactions_Matrix.append(new_row)
            
def Bake_Universe_Pie():
    for i in range(PARTICLE_COUNT):
        for j in range(i+1, PARTICLE_COUNT):
            Universe_Pie.append((Universe[i], Universe[j]))

def Simulate_Slice(slice):
    part_a = slice[0]
    part_b = slice[1]

    dist_vect = VMath.Distance_Vector(part_a.pos, part_b.pos)

    if WRAP_AROUND == True:
            for i, dim in enumerate(dist_vect):
                if abs(dim) > WIN_DIMS[i]/2:   # If this is true, the other direction is shorter
                    dist_vect[i] = (WIN_DIMS[i] - abs(dim)) * -1 * sign_of_int(dim)   # Go around the other direction
    
    distance = VMath.Magnitude(dist_vect)
    if distance < MAX_FORCE_DIST: # big check to see if particles could even possibly be in range.
        intr_a = Interactions_Matrix[part_a.color][part_b.color]
        intr_b = Interactions_Matrix[part_b.color][part_a.color]
        if distance < intr_a[2]:
            # Do part_a calculations
            norm_vect = [dist_vect[0]/distance, dist_vect[1]/distance]
            contact = intr_a[1]
            if (distance < contact):
                force = NORMAL_FORCE * normal_equation(distance,contact)
            else:
                force = intr_a[0] * force_equation(distance, contact, intr_a[2])
        
            part_a.vel = VMath.Addition(part_a.vel, VMath.Scal_Mult(norm_vect, -force))

        if distance < intr_b[2]:
            # Do part_b calculations
            contact = intr_b[1]
            norm_vect = [dist_vect[0]/distance, dist_vect[1]/distance]
            if (distance < contact):
                force = NORMAL_FORCE * normal_equation(distance,contact)
            else:
                force = intr_b[0] * force_equation(distance, contact, intr_b[2])
        
            part_b.vel = VMath.Addition(part_b.vel, VMath.Scal_Mult(norm_vect, force))

def Update_Position(particle):   # This comes after all force calculations
        particle.vel = VMath.Scal_Mult(particle.vel,(1-FRICTION))   # Friction application. It either goes here or at the end.
        new_pos = VMath.Vect_Modulo(VMath.Addition(particle.pos, particle.vel), WIN_DIMS)

        if WRAP_AROUND is False:
            #ratios = (self.pos + self.vel) // WIN_DIMS
            ratios = VMath.Floor_Div(VMath.Addition(particle.pos, particle.vel), WIN_DIMS)
            for i in range(2):
                if ratios[i] % 2 == 1:
                    new_pos[i] = WIN_DIMS[i] - new_pos[i]

        my_canvas.move(particle.graphic, new_pos[0] - particle.pos[0], new_pos[1] - particle.pos[1])
        particle.pos = new_pos
        #particle.vel = VMath.Scal_Mult(particle.vel,(1-FRICTION))

# The function which runs at each step
def Time_Step():
    global Steps
    Steps += 1
    if TESTING and Steps >= TEST_STEPS:
        root.after(1, root.destroy)

    for slice in Universe_Pie:
        Simulate_Slice(slice)
    
    for particle in Universe:
        Update_Position(particle)

    root.after(TIME_STEP_MS, Time_Step)

def Print_Info():
    print("")
    print("Running simulation version " + VERSION + " at " + str(WIN_DIMS[0]) + "x" + str(WIN_DIMS[1]) + " with a canvas delay of " + str(TIME_STEP_MS) +"ms")
    print("Particles: " + str(PARTICLE_COUNT) + ", Colors: " + str(COLORS) + ", Friction: " + str(FRICTION) + ", Normal force: " + str(NORMAL_FORCE))
    print("")

Running = True
if __name__ == "__main__":
    Print_Info()
    init_start_time = perf_counter()

    print("Creating the universe...")
    Init_Universe()
    Init_Interactions_Matrix()

    print("Baking a pie...")
    Bake_Universe_Pie()

    init_time = perf_counter() - init_start_time
    print("Init time: " + str(init_time * 1000) + "ms")
    print("")

    if not TESTING:
        print("Starting the simulation...")
    else:
        print("Starting test simulation for " + str(TEST_STEPS) + " steps...")
    start_time = perf_counter()

    root.after(TIME_STEP_MS, Time_Step)
    root.mainloop()

    time = perf_counter() - start_time
    print("Sim Time: " + str(time) + "s, Time Steps: " + str(Steps))
    print("Time per step: " + str(time/Steps * 1000) + "ms")
    print("")
