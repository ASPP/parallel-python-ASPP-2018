import numpy as np

N = 50

positions = np.random.rand(N, 3) * 80 - 40
velocities = np.random.rand(N, 3) * 2 - 1
masses = np.random.rand(N) * 0.05

positions[0, :] = 0
masses[0] = 10

np.savetxt('initial_positions.txt', positions)

np.savetxt('initial_velocities.txt', velocities)

np.savetxt('masses.txt', masses)

