import time
import matplotlib.pyplot as plt
import numpy as np

sim_time = 0.0
sim_last = False

sim_time_step = 0.04
sim_count = 0
time_x = np.array([])

integrator = 'dopri5'  # 'vode','zvode','lsoda','dopri5','dop853'
integrator_params = {}

real = False


def simulate(model, t=10.0):
    if real:
        simulate_real_time(model, t)
    else:
        simulate_fast(model, t)


def simulate_real_time(model, t=10.0):

    if hasattr(model, "run"):
        run = model.run
    elif hasattr(model, "__call__"):
        run = model
    else:
        raise Exception("invalid model")

    global time_x, sim_time, sim_time_step, sim_count, sim_last
    plt.show(block=False)
    start_time = time.time()
    sim_time = 0.0
    sim_count = 1
    sim_last = False

    print("simulation start")

    while sim_time < t:

        print("simulation time: %f" % sim_time)
        time_x = np.linspace(0.0, sim_time, sim_count)
        run()
        sim_time += sim_time_step
        sim_count += 1

        interval = time.time() - start_time
        if interval < sim_time:
            plt.pause(sim_time - interval)
        else:
            for i in plt.get_fignums():
                plt.figure(i).canvas.flush_events()

    sim_last = True
    sim_time = t
    time_x = np.append(time_x, t)
    run()
    interval = time.time() - start_time
    if interval < sim_time:
        plt.pause(sim_time - interval)
    else:
        for i in plt.get_fignums():
            plt.figure(i).canvas.flush_events()

    print("simulation end, time: %f s" % (time.time() - start_time))


def simulate_fast(model, t=10.0):

    if hasattr(model, "run"):
        run = model.run
    elif hasattr(model, "__call__"):
        run = model
    else:
        raise Exception("invalid model")

    global time_x, sim_time, sim_time_step, sim_count, sim_last

    sim_time = 0.0
    sim_count = 1
    sim_last = False

    print("simulation start")
    start_time = time.time()

    while sim_time < t:
        # print("simulation time: %f" % sim_time)
        time_x = np.linspace(0.0, sim_time, sim_count)
        if sim_time + sim_time_step >= t:
            sim_last = True
        run()
        sim_time += sim_time_step
        sim_count += 1

    sim_last = True
    sim_time = t
    time_x = np.append(time_x, t)
    run()

    print("simulation end, time: %f s" % (time.time() - start_time))

    plt.show()
