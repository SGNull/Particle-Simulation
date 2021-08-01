# Imports
from time import perf_counter
import tkinter as tk
import Vector2Math as VMath
from random import random, randint
from math import sqrt



# Settings
VERSION = "1.0.0"
WIN_DIMS = [900,700]
WIN_COLOR = "black"

WRAP_AROUND = True
TESTING = False
TIME_STEP_MS = 1
PARTICLE_COUNT = 220
PARTICLE_RADIUS = 5
COLORS = 4

CONTACT_DIST = PARTICLE_RADIUS *2.5
NORMAL_FORCE = 10
MAX_FORCE = 0.6
MAX_FORCE_DIST = 150
MIN_FORCE_DIST = 50
FRICTION = 0.13



# Global variables
Running = True
Universe = []
Universe_Pie = []
Interactions_Matrix = []   # Format: (force_magnitude, force_start, force_end)
Color_List = ['red', 'green', 'blue', 'cyan', 'yellow', 'magenta', 'orange', 'purple', 'white']

# init canvas
root = tk.Tk()
tk.title = "Python Particles " + VERSION
my_canvas = tk.Canvas(root, height=WIN_DIMS[1], width=WIN_DIMS[0], bg=WIN_COLOR)
my_canvas.pack()



# Particle object (really convenient if it's here and not in a seperate file cause of all the settings)
class Particle (object):
    '''The main object for the simulation'''
    def __init__(self, pos, color):
        self.pos = list(pos)
        self.color = color
        self.radius = PARTICLE_RADIUS
        self.vel = [0,0]
        self.graphic = my_canvas.create_oval(pos[0]-self.radius, pos[1]-self.radius, pos[0]+self.radius, pos[1]+self.radius, fill=Color_List[color])
    
    def Update_Position(self):   # This comes after all force calculations
        new_pos = VMath.Vect_Modulo(VMath.Addition(self.pos, self.vel), WIN_DIMS)

        if WRAP_AROUND != True:
            #ratios = (self.pos + self.vel) // WIN_DIMS
            ratios = VMath.Floor_Div(VMath.Addition(self.pos, self.vel), WIN_DIMS)
            for i in range(2):
                if ratios[i] % 2 == 1:
                    new_pos[i] = WIN_DIMS[i] - new_pos[i]

        my_canvas.move(self.graphic, new_pos[0] - self.pos[0], new_pos[1] - self.pos[1])
        self.pos = new_pos
        self.vel = VMath.Scal_Mult(self.vel,(1-FRICTION))



# Functions
rand_mag = lambda x : 2*x*random() - x   # Returns a random number between -x and x
rand_range = lambda start, end: (end-start)*random()+start
sign_of_int = lambda a: int(a>0) - int(a<0)   # SO ref: https://www.quora.com/How-do-I-get-sign-of-integer-in-Python

# The main component equations for the force, recreated from the image shown in Code Parade's video
# Desmos graph: https://www.desmos.com/calculator/ubemfmpbg6
normal_equation = lambda distance, contact_radius: -sqrt(distance)/sqrt(contact_radius) + 1
force_equation = lambda distance, contact_dst, force_dst: -2/(force_dst-contact_dst)*abs(distance-(contact_dst+force_dst)/2)+1

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
            new_interaction = (rand_mag(MAX_FORCE), CONTACT_DIST, rand_range(CONTACT_DIST,MAX_FORCE_DIST))
            new_row.append(new_interaction)
        Interactions_Matrix.append(new_row)
            
def Bake_Universe_Pie():
    for i in range(PARTICLE_COUNT):
        for j in range(i+1, PARTICLE_COUNT):
            Universe_Pie.append((Universe[i], Universe[j]))

def Observe_Slice(slice):
    part_a = slice[0]
    part_b = slice[1]

    dist_vect = VMath.Distance_Vector(part_a.pos, part_b.pos)
    intr_a = Interactions_Matrix[part_a.color][part_b.color]
    intr_b = Interactions_Matrix[part_b.color][part_a.color]

    if WRAP_AROUND == True:
            for i, dim in enumerate(dist_vect):
                if abs(dim) > WIN_DIMS[i]/2:   # If this is true, the other direction is shorter
                    dist_vect[i] = (WIN_DIMS[i] - abs(dim)) * -1 * sign_of_int(dim)   # Go around the other direction
    
    distance = VMath.Magnitude(dist_vect)

    if distance < intr_a[2]:
        # Do part_a calculations
        norm_vect = VMath.Normalize(dist_vect)
        if (distance < intr_a[1]):
            force = NORMAL_FORCE * normal_equation(distance,intr_a[1])
        else:
            force = intr_a[0] * force_equation(distance, intr_a[1], intr_a[2])
        
        part_a.vel = VMath.Addition(part_a.vel, VMath.Scal_Mult(norm_vect, -force))

    if distance < intr_b[2]:
        # Do part_b calculations
        norm_vect = VMath.Normalize(dist_vect)
        if (distance < intr_b[1]):
            force = NORMAL_FORCE * normal_equation(distance,intr_b[1])
        else:
            force = intr_b[0] * force_equation(distance, intr_b[1], intr_b[2])
        
        part_b.vel = VMath.Addition(part_b.vel, VMath.Scal_Mult(norm_vect, force))

# The function which runs at each step
def Time_Step():
    for slice in Universe_Pie:
        Observe_Slice(slice)
    
    for particle in Universe:
        particle.Update_Position()

    root.after(TIME_STEP_MS, Time_Step)

def Print_Info():
    print("")
    print("Running simulation version " + VERSION + " at " + str(WIN_DIMS[0]) + "x" + str(WIN_DIMS[1]))
    print("Time step: " + str(TIME_STEP_MS) +"ms. Particles: " + str(PARTICLE_COUNT) + ".")
    print("")

if __name__ == "__main__":
    Print_Info()
    init_start_time = perf_counter()

    print("Creating the universe...")
    Init_Universe()
    Init_Interactions_Matrix()

    print("Baking a pie...")
    Bake_Universe_Pie()

    init_stop_time = perf_counter()
    print("Init time: " + str(init_stop_time - init_start_time) + "s")

    print("Starting the simulation...")
    start_time = perf_counter()

    root.after(TIME_STEP_MS, Time_Step)
    root.mainloop()

    stop_time = perf_counter()
    print("Sim time: " + str(stop_time - start_time) + "s")