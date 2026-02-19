import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

def plot_cluster_sizes_from_file(filename="all_results.txt"):
    sizes = []
    
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines, headers, separators, and summary sections
            if not line or line.startswith("Source_File") or line.startswith("-") or line.startswith("=") or line.startswith("GLOBAL"):
                continue
            
            parts = line.split()
            if len(parts) >= 3:
                try:
                    # Column mapping: 0=File, 1=ID, 2=Size, 3=Amp
                    size = int(parts[2])
                    sizes.append(size)
                except (ValueError, IndexError):
                    continue
                
    if not sizes:
        print("No cluster data found.")
        return

    # Calculate frequencies for discrete bars
    unique_sizes, counts = np.unique(sizes, return_counts=True)

    # Create the plot
    plt.bar(unique_sizes, counts, color='forestgreen', edgecolor='black', alpha=0.7)
    plt.title("Distribution of Cluster Sizes (All Files)", fontsize=14)
    plt.xlabel("Cluster Size (Pixels)", fontsize=12)
    plt.ylabel("Number of Clusters", fontsize=12)
    plt.xticks(unique_sizes)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.savefig("cluster_size_histogram.png")
    print(f"Histogram successfully saved as cluster_size_histogram.png")

# Usage

plot_cluster_sizes_from_file("all_results.txt")

def plot_amplitude_by_size(filename="all_results.txt"):
    # Dictionaries to hold amplitudes for each category
    data_map = {
        "Size 1": [],
        "Size 2": [],
        "Size 3+": []
    }
    
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or any(line.startswith(s) for s in ["Source", "-", "=", "GLOBAL"]):
                continue
            
            parts = line.split()
            if len(parts) >= 4:
                try:
                    size = int(parts[2])
                    amp = float(parts[3])
                    
                    if size == 1:
                        data_map["Size 1"].append(amp)
                    elif size == 2:
                        data_map["Size 2"].append(amp)
                    else:
                        data_map["Size 3+"].append(amp)
                except (ValueError, IndexError):
                    continue

    # Plotting configuration
    categories = ["Size 1", "Size 2", "Size 3+"]
    colors = ['#3498db', '#e67e22', '#e74c3c']
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=False)
    fig.suptitle("Amplitude Distribution per Cluster Size", fontsize=16)

    for i, cat in enumerate(categories):
        dataset = data_map[cat]
        if dataset:
            axes[i].hist(dataset, bins=20, color=colors[i], edgecolor='black', alpha=0.7)
            axes[i].set_title(f"{cat} (N={len(dataset)})")
            axes[i].set_xlabel("Total Amplitude")
            if i == 0:
                axes[i].set_ylabel("Frequency")
        else:
            axes[i].text(0.5, 0.5, "No Data", ha='center')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("amplitude_by_size.png")
    print("Plot saved as amplitude_by_size.png")

# Usage
plot_amplitude_by_size("all_results.txt")