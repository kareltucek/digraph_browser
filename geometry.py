import numpy as np
import math

def vector(x, y):
    return np.array([x,y])

def zerovector():
    return vector(0.0, 0.0)

def length(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def scale_to(vec, l):
    return vec/length(vec)*l


