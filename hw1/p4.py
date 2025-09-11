import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh

class CoupledOscillators:
    def __init__(self, N, M, K, arg, T, P, X0):
        self.N = N             #number of oscillators
        self.M = M             #mass
        self.K = K             #spring constant
        self.T = np.array(T)   #time vector
        self.P = np.array(P)   #phase
        self.X0 = np.array(X0) #initial positions
        self.arg = arg

        if arg == 1:  # fixed ends
            L = 2*np.eye(N) - np.diag(np.ones(N-1), 1) - np.diag(np.ones(N-1), -1)
        elif arg == -1:  # free ends
            L = 2*np.eye(N) - np.diag(np.ones(N-1), 1) - np.diag(np.ones(N-1), -1)
            L[0, 0] = 1
            L[-1, -1] = 1
        elif arg == 0:  # periodic
            L = 2*np.eye(N) - np.diag(np.ones(N-1), 1) - np.diag(np.ones(N-1), -1)
            L[0, -1] = -1
            L[-1, 0] = -1
        else:
            raise ValueError("arg must be -1, 0, or 1")

        self.L = L

    def frequency(self):
        #solve eigenvalue problem
        w, _ = eigh(self.K * self.L, self.M * np.eye(self.N))
        omega = np.sqrt(np.real(w))  # take sqrt to get freqs
        return omega

    def displacement(self):
        omega = self.frequency()
        t = self.T[:, None] 
        X = self.X0 * np.cos(omega * t + self.P)
        return X

    def plot_osc(self):
        X = self.displacement()
        plt.figure(figsize=(8, 5))
        plt.plot(self.T, X)
        plt.xlabel("Time")
        plt.ylabel("Displacement")
        plt.title("Coupled Oscillators Displacement")
        plt.grid(True)
        plt.show()


# Parameters
N = 5    # number of oscillators
m = 1    # mass
K = 1    # spring constant
T = np.linspace(0, 2*np.pi*10, 1000)  # time vector
P = np.random.rand(N)   # random phases
X0 = np.random.rand(N)  # random initial positions

# Create system
sys = CoupledOscillators(N, m, K, 1, T, P, X0)

# Compute frequencies and displacements
freqs = sys.frequency()
posit = sys.displacement()

# Plot results
sys.plot_osc()
