import math
from simpy import *
from simpy.lib import *

sin = tmodel(sin_wave())

integrator = integrator_model(0.1)

scope1 = scope()

def run():
    s1 = sin()
    s2 = integrator(s1)
    scope1([s1, s2])

simulate(run)
