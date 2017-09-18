import math

import matplotlib.pyplot as plt

from simpy import model

ax1 = plt.subplot(121)
ax2 = plt.subplot(122)

model_sin = model.TimedFunctionModel(math.sin)
model_cos = model.TimedFunctionModel(math.cos)
scope = model.ScopeModel(ax1, ax2)


def run():
    scope(model_sin(), model_cos())
