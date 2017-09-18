import math

import matplotlib.pyplot as plt

from simpy import model

ax1 = plt.subplot(111)

model_sin = model.TimedFunctionModel(math.sin)
scope = model.ScopeModel(ax1)

def run():
    scope(model_sin())
