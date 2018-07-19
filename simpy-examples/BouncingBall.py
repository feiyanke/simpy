from simpy.lib import *

def _fall(t, x):
    return [-9.81, x[0]]

fall = smodel(_fall, [10,100])
scope = scope()
scope.set_time_len(250)

def run():
    v,s=fall()
    if s < 0:
        fall.set_state([-0.8*v, 0])
    scope(v,s)

env.real = True
simulate(run, 120)

