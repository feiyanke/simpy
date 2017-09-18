from simpy.lib import *

integrator1 = integrator_model(0.25)
integrator2 = integrator_model(0.25)
scope = scope()
scope.set_time_len(20)

x2 = 0
def run():
    global x2
    x1 = integrator1(x2)
    if x1 > 0.0:
        s = -1.0
    elif x1 < 0.0:
        s = 1.0
    else:
        s = 0.0
    x2 = integrator2(s)
    scope([x1,x2])

env.real = True
simulate(run, 120)