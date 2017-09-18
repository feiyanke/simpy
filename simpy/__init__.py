import simpy.env as env
import simpy.model as sm

simulate = env.simulate

def fmodel(f):
    return sm.FunctionModel(f)


def tmodel(f):
    return sm.TimedFunctionModel(f)


def smodel(f, u0, jac=None, integrator=None, **integrator_params):
    return sm.StateFunctionModel(f, u0, jac, integrator, **integrator_params)

def scope(*axs):
    return sm.ScopeModel(*axs)