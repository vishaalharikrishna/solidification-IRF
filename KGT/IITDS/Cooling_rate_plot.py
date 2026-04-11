import numpy as np
import matplotlib.pyplot as plt

# Define constants from your equation
b = 2472
tau = 0.0012

# Define time range requested (0.1ms to 2ms)
t = np.linspace(0.1e-3, 2e-3, 500)

# Calculate the instantaneous cooling rate (magnitude)
# Formula: |dT/dt| = (2472 / 0.0012) * exp(-t / 0.0012)
cooling_rate = 2.06*1000000 * np.exp(-t / tau)

# Create the plot
plt.figure(figsize=(8, 5))
plt.plot(t * 1000, cooling_rate, color='blue', linewidth=2)

# Formatting
plt.xlabel('Time (ms)', fontsize=12)
plt.ylabel('Cooling Rate |$\dot{T}$| (K/s)', fontsize=12)
plt.title('Instantaneous Cooling Rate vs. Time', fontsize=14)
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

# Display plot
plt.tight_layout()
#plt.savefig('cooling_rate_plot.png')
plt.show()