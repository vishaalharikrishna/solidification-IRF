import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_csv("F:\Vishaal\Misc\Python_codes\solidification-IRF\KGT\IITDS\KGT_IITDS_gamma\KGT_IITDS_Gamma.csv")
df2 = pd.read_csv("F:\Vishaal\Misc\Python_codes\solidification-IRF\KGT\IITDS\KGT_IITDS_delta\KGT_IITDS_Delta.csv")

plt.figure(figsize=(10, 6), dpi=600)

plt.plot(df1['v'], df1['T'], label='Alloy 1 (IITDS - Gamma)', color='blue', linewidth=2)

plt.plot(df2['v'], df2['T'], label='Alloy 2 (IITDS - Delta)', color='red', linewidth=2)

plt.xscale('log')
plt.xlabel('Solidification Velocity (m/s)', fontsize=14)
plt.ylabel('Tip Temperature (K)', fontsize=14)
plt.title('KGT Model Comparison: Dendrite Tip Temperature', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.5)

plt.tight_layout()
plt.savefig("F:\Vishaal\Misc\Python_codes\solidification-IRF\KGT\IITDS\Combined_plot.jpg", dpi=600)
plt.show()