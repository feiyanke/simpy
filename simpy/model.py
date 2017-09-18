import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import ode
import simpy.env as env


def is_model(x):
    return hasattr(x, "run")


class Model(object):
    def __init__(self):
        self._time = -1.0
        self._y = 0.0
        pass

    def __call__(self, *args, **kwargs):
        if env.sim_time == 0.0:
            self.start(*args, **kwargs)
        if env.sim_time > self._time:
            self._y = self.run(*args, **kwargs)
            self._time = env.sim_time
        if env.sim_last:
            self.end(*args, **kwargs)
        return self._y

    def start(self, *args, **kwargs):
        pass

    def end(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        raise Exception("not implement run")


class FunctionModel(Model):
    def __init__(self, f):
        Model.__init__(self)
        if hasattr(f, '__call__'):
            self._f = f;
        else:
            raise Exception("not function")

    def run(self, *args, **kwargs):
        return self._f(*args, **kwargs)


class TimedFunctionModel(FunctionModel):
    def run(self, *args, **kwargs):
        return self._f(env.sim_time, *args, **kwargs)


class StateFunctionModel(Model):
    def __init__(self, f, u0, jac=None, integrator_name=None, **integrator_params):
        Model.__init__(self)
        if hasattr(f, '__call__'):
            self._r = ode(f, jac)
            if integrator_name:
                self._r.set_integrator(integrator_name, **integrator_params)
            else:
                self._r.set_integrator(env.integrator, **env.integrator_params)
            self._r.set_initial_value(u0)
            self._time = 0.0
            self._y = u0
        else:
            raise Exception("not function")

    def set_state(self, u):
        self._r.set_initial_value(u, env.sim_time)

    def run(self, *args, **kwargs):
        self._r.set_f_params(*args)
        self._r.set_jac_params(*args)
        return self._r.integrate(env.sim_time)


class ScopeModel(Model):
    def __init__(self, *axs):
        Model.__init__(self)
        self._axs = list(axs)
        self._canvas = set()
        self._y_data = []
        self._x_data = []
        self._lines = []
        self._data_len = 0
        self._x_rlimit = 5.0

    def set_data_len(self, data_len):
        self._data_len = data_len
        self._x_rlimit = data_len*env.sim_time_step
        return self

    def set_time_len(self, time_len):
        self._data_len = int(time_len/env.sim_time_step+1)
        self._x_rlimit = time_len
        return self

    def __flat(self, *xs):
        flat_xs = []
        for x in xs:
            if hasattr(x, '__iter__'):
                for xx in x:
                    flat_xs.append(xx)
            else:
                flat_xs.append(x)
        return flat_xs

    def start(self, *xs):
        for i, x in enumerate(xs):

            if i >= len(self._axs):
                plt.figure()
                ax = plt.subplot()
                self._axs.append(ax)

            if hasattr(x, '__iter__'):
                for xx in x:
                    l, = self._axs[i].plot([], [])
                    self._lines.append(l)
            else:
                l, = self._axs[i].plot([], [])
                self._lines.append(l)

        self._canvas = set(ax.figure.canvas for ax in self._axs)

    def end(self, *xs):
        if not env.real:
            y_data = np.array(self._y_data)

            for i, line in enumerate(self._lines):
                line.set_data(self._x_data, y_data[:, i])

            for ax in self._axs:
                ax.relim()
                ax.autoscale_view()
                if env.sim_time < self._x_rlimit:
                    ax.set_xlim(0, self._x_rlimit)
                else:
                    ax.set_autoscalex_on(True)

            for c in self._canvas:
                c.draw_idle()

    def run(self, *xs):

        self._y_data.append(self.__flat(*xs))
        if len(self._y_data) > self._data_len > 0:
            self._y_data.pop(0)
            self._x_data = env.time_x[-self._data_len-1:-1:1]
        else:
            self._x_data = env.time_x

        if env.real:

            y_data = np.array(self._y_data)

            for i, line in enumerate(self._lines):
                line.set_data(self._x_data, y_data[:, i])

            for ax in self._axs:
                ax.relim()
                ax.autoscale_view()
                if env.sim_time < self._x_rlimit:
                    ax.set_xlim(0, self._x_rlimit)
                else:
                    ax.set_autoscalex_on(True)

            for c in self._canvas:
                c.draw_idle()
