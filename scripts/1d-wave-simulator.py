
import numpy as np
import matplotlib.pyplot as plt

def simulate_wave_1d():
    # 1. Setup Parameters
    nx = 200        # Number of grid points
    dx = 1.0        # Distance between points (m)
    c = 300.0       # Wave speed (m/s)
    dt = 0.002      # Time step (s)
    nt = 500        # Number of time steps to simulate
    
    # Calculate Courant number (must be <= 1 for stability)
    C = c * dt / dx 
    print(f"Courant Number: {C:.2f}")
    if C > 1:
        raise ValueError("Unstable simulation! Reduce dt or increase dx.")

    # 2. Initialize Arrays
    u = np.zeros(nx)       # Current time step
    u_prev = np.zeros(nx)  # Previous time step
    u_next = np.zeros(nx)  # Next time step

    # 3. Initial Condition (Gaussian Pulse)
    # Start the wave in the middle of the domain
    x = np.linspace(0, nx*dx, nx)
    u = np.exp(-0.5 * ((x - nx*dx/2) / 5)**2)
    u_prev = np.copy(u) # Assume initial velocity is 0

    # Setup plotting
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot(x, u)
    ax.set_ylim(-1.5, 1.5)
    ax.set_title("1D Wave Simulation")

    # 4. Time Loop
    for n in range(nt):
        # Vectorized update (much faster than a for-loop in Python)
        # u[1:-1] refers to points 1 to N-1 (excluding boundaries)
        # u[0:-2] is left neighbor (i-1)
        # u[2:]   is right neighbor (i+1)
        
        u_next[1:-1] = 2*u[1:-1] - u_prev[1:-1] + \
                       (C**2) * (u[2:] - 2*u[1:-1] + u[0:-2])

        # Boundary Conditions (Reflective: Fixed at 0)
        u_next[0] = 0
        u_next[-1] = 0

        # Update arrays for next step
        u_prev[:] = u[:]
        u[:] = u_next[:]

        # Visualization (update every 10 steps)
        if n % 10 == 0:
            line.set_ydata(u)
            plt.pause(0.01)

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    simulate_wave_1d()
