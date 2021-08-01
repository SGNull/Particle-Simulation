from math import floor, sqrt

def Scal_Mult (vector, scalar):
    '''Scalar multiplication.'''
    new_vect = [0,0]
    new_vect[0] = vector[0] * scalar
    new_vect[1] = vector[1] * scalar
    return new_vect

def Floor_Div(vector_a, vector_b):
    '''Element-wise division, but also does the floor() function'''
    new_vect = [0,0]
    new_vect[0] = floor(vector_a[0]/vector_b[0])
    new_vect[1] = floor(vector_a[1]/vector_b[1])
    return new_vect

def Scal_Modulo (vector, mod):
    '''Mod each element of vector by "mod"'''
    new_vect = [0,0]
    new_vect[0] = vector[0] % mod
    new_vect[1] = vector[1] % mod
    return new_vect

def Vect_Modulo (vector, vector_mod):
    '''Element-wise modulo operation.'''
    new_vect = [0,0]
    new_vect[0] = vector[0] % vector_mod[0]
    new_vect[1] = vector[1] % vector_mod[1]
    return new_vect

def Addition (vect_a, vect_b):
    '''Vector addition'''
    new_vect = [0,0]
    new_vect[0] = vect_a[0] + vect_b[0]
    new_vect[1] = vect_a[1] + vect_b[1]
    return new_vect

def Distance_Vector (point_a, point_b):
    '''Returns the distance vector from point_a to point_b'''
    new_vect = [0,0]
    new_vect[0] = point_b[0] - point_a[0]
    new_vect[1] = point_b[1] - point_a[1]
    return new_vect

def Distance(point_a, point_b):
    '''Returns the distance from point_a to point_b'''
    x = (point_b[0]-point_a[0])**2
    y = (point_b[1]-point_a[1])**2
    return sqrt(x+y)

def Magnitude (vector):
    '''Returns the magnitude of a given vector'''
    return sqrt(vector[0]**2 + vector[1]**2)

def Normalize (vector):
    '''Returns the normalized form of the vector'''
    magnitude = sqrt(vector[0]**2 + vector[1]**2)
    new_vect = [0,0]
    new_vect[0] = vector[0]/magnitude
    new_vect[1] = vector[1]/magnitude
    return new_vect