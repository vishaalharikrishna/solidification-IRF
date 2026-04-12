import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def eagar_tsai_sane(t, P, eta, rho, cp, k, sigma, V, T0, x_start):
    kappa = k / (rho * cp)
    coeff = (P * eta) / (rho * cp * np.power(4 * np.pi * kappa, 1.5))
    
    # x_rel is the current distance between laser and point
    x_rel = x_start - V * t

    def integrand(u):
        # Physical buffer: heat cannot diffuse faster than the spot size allows
        # This prevents the 7e7 K spike
        denom = (4 * kappa * u + 2 * sigma**2)
        exponent = -(x_rel**2) / denom
        return (1.0 / (np.sqrt(u) * denom)) * np.exp(exponent)

    # We integrate from a tiny epsilon to t to avoid the 1/sqrt(0) singularity
    val, _ = quad(integrand, 1e-7, t if t > 1e-7 else 1e-6, limit=100)
    return T0 + coeff * val

# --- Parameters (Optimized for Tool Steel) ---
P, eta = 250, 0.45      # 250W, 45% absorption
rho, cp, k = 7000, 939, 32 
sigma, V = 110e-6, 0.6
T0 = 473
x_start = 0.003        # Laser starts 3mm away

# --- Generation ---
t_vec = np.linspace(0, 0.015, 1000) # 0 to 15ms
T_vec = [eagar_tsai_sane(t, P, eta, rho, cp, k, sigma, V, T0, x_start) for t in t_vec]

# --- Dual-View Plotting ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Plot 1: Full View (to see the peak)
ax1.plot(t_vec * 1000, T_vec, color='gray', alpha=0.5)
ax1.set_title("Full Thermal History (Peak View)")
ax1.set_ylabel("Temp (K)")
ax1.set_ylim(300, 5000) # Capped at 5000K (Boiling point range)

# Plot 2: Solidification View (THE IMPORTANT ONE)
ax2.plot(t_vec * 1000, T_vec, color='red', lw=2)
ax2.axhline(1689, color='blue', ls='--', label='Liquidus (1689 K)')
ax2.axhline(1524, color='green', ls='--', label='Solidus (1524 K)')

# Focus exactly on your area of interest
ax2.set_ylim(1400, 1800) 
ax2.set_title("Zoomed Solidification Range (1400 - 1800 K)")
ax2.set_xlabel("Time (ms)")
ax2.set_ylabel("Temp (K)")
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()