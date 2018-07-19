import math
from simpy import *


def sin_wave(amp=1.0, freq=1.0, phase=0.0, bias=0.0):
    return lambda t:amp*math.sin(freq*t+phase)+bias


def integrator_model(u0):
    return smodel(lambda t, x, u: u, u0)
