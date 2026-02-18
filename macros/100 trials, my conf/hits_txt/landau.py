import numpy as np
from scipy.stats import moyal
import matplotlib.pyplot as plt

def apply_landau_fit_and_save(input_file="all_results.txt", output_stats="landau_stats.txt"):
    amplitudes = []
    
    # 1. Parse amplitudes from the master results file
    try:
        with open(input_file, "r") as f:
            for line in f:
                parts = line.split()
                # Skip headers/summary lines and ensure it's a data row
                if len(parts) >= 4 and not parts[0].startswith(("Source", "-", "=", "GLOBAL")):
                    try:
                        amplitudes.append(float(parts[3])) # Index 3 is Total_Amp
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
        return

    if len(amplitudes) < 5:
        print("Not enough data points to perform a Landau fit.")
        return

    # 2. Perform the Fit using Moyal (Approximation of Landau)
    # loc = Most Probable Value (MPV), scale = Width (sigma)
    mpv, sigma = moyal.fit(amplitudes)

    # 3. Save the results to a file
    with open(output_stats, "w") as out_f:
        out_f.write("LANDAU (MOYAL) FIT RESULTS\n")
        out_f.write("=" * 30 + "\n")
        out_f.write(f"Source File:           {input_file}\n")
        out_f.write(f"Number of Clusters:    {len(amplitudes)}\n")
        out_f.write(f"Most Probable Value (MPV): {mpv:.4f}\n")
        out_f.write(f"Width (Sigma):         {sigma:.4f}\n")
        out_f.write("=" * 30 + "\n")

    # 4. Generate Plot for verification
    x = np.linspace(min(amplitudes), max(amplitudes), 500)
    pdf = moyal.pdf(x, mpv, sigma)
    
    plt.figure(figsize=(8, 6))
    plt.hist(amplitudes, bins=50, density=True, alpha=0.5, color='gray', label='Data')
    plt.plot(x, pdf, 'r-', lw=2, label=f'Fit (MPV={mpv:.2f})')
    plt.xlabel("Total Amplitude")
    plt.ylabel("Normalized Frequency")
    plt.title("Landau Distribution Fit")
    plt.legend()
    plt.savefig("landau_fit_plot.png")
    
    print(f"Stats saved to {output_stats}")
    print("Plot saved to landau_fit_plot.png")

# Run the analysis
if __name__ == "__main__":
    apply_landau_fit_and_save()