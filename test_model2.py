import math
from simpy import *

def f1(t, x):
    return math.cos(t)

def f2(t, u, v):
    return [u[1]/v, 3.*(1. - u[0]*u[0])*u[1] - u[0]]

scope = scope()
sfun1 = smodel(f1, 0.0)
sfun2 = smodel(f2, [2.0, 0.0])
sint = tmodel(math.sin)


def run():
    scope(sfun2(sint()))

simulate(run)


