# visualise.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Constants used to interpret the grid
MAX_STACK = 64
INVENTORY_SIZE = 36
UNREACHABLE = MAX_STACK + 1

# Function to map (baggage, act) to index
def index_interpreter(baggage, act, max_stack=MAX_STACK):
    return act + (max_stack + 1) * baggage

# Read and parse the optimals data
def read_optimals(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return [int(line.strip()) for line in lines]

# Plotting function
def plot_3d_optimals(optimals, max_stack=MAX_STACK, inv_length=INVENTORY_SIZE):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xs, ys, zs = [], [], []

    for baggage in range(inv_length + 1):
        for act in range(max_stack + 1):
            idx = index_interpreter(baggage, act, max_stack)
            val = optimals[idx]
            if val != UNREACHABLE:
                xs.append(act)
                ys.append(baggage)
                zs.append(val)

    xs = np.array(xs)
    ys = np.array(ys)
    zs = np.array(zs)

    scatter = ax.scatter(xs, ys, zs, c=zs, cmap='inferno', s=50)

    ax.set_xlabel('Items on cursor')
    ax.set_ylabel('Used inventory slots')
    ax.set_zlabel('Clicks Required')
    plt.title('Optimal clicks')
    fig.colorbar(scatter, label='Clicks Required')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    optimals = read_optimals("optimals_data.txt")
    plot_3d_optimals(optimals)
