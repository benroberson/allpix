import numpy as np
import math

def find_clusters_euclidean(hits, distance_threshold=1.5):
    """Clusters hits using Euclidean distance and excludes single-hit clusters."""
    visited = set()
    final_clusters = []
    search_range = math.ceil(distance_threshold)
    pixels = list(hits.keys())

    for pixel in pixels:
        if pixel not in visited:
            current_cluster = []
            stack = [pixel]
            visited.add(pixel)
            while stack:
                curr_x, curr_y = stack.pop()
                current_cluster.append((curr_x, curr_y, hits[(curr_x, curr_y)]))
                for dx in range(-search_range, search_range + 1):
                    for dy in range(-search_range, search_range + 1):
                        if dx == 0 and dy == 0: continue
                        if math.sqrt(dx**2 + dy**2) <= distance_threshold:
                            neighbor = (curr_x + dx, curr_y + dy)
                            if neighbor in hits and neighbor not in visited:
                                visited.add(neighbor)
                                stack.append(neighbor)
            # Filter: Exclude single-hit noise
            #if len(current_cluster) > 1:
            final_clusters.append(current_cluster)
    return final_clusters

def batch_process_hits(num_files=100):
    master_filename = "all_results.txt"
    global_stats = {"total_clusters": 0, "total_hits": 0, "total_amp": 0.0}
    
    with open(master_filename, "w") as master_f:
        # Header for the master file
        master_f.write(f"{'Source_File':<15} {'ID':<5} {'Size':<5} {'Total_Amp':<10}\n")
        master_f.write("-" * 45 + "\n")

        for i in range(1, num_files + 1):
            input_file = f"hits_{i}.txt"
            output_file = f"results_{i}.txt"
            
            try:
                data = np.loadtxt(input_file)
                if data.ndim == 1: data = data.reshape(1, -1)
                hits = {(int(row[0]), int(row[1])): row[2] for row in data}
                
                clusters = find_clusters_euclidean(hits)

                # Individual result file (Vertical format)
                with open(output_file, "w") as ind_f:
                    ind_f.write(f"{'ID':<5} {'Size':<5} {'Total_Amp':<10}\n")
                    ind_f.write("-" * 25 + "\n")
                    for idx, c in enumerate(clusters):
                        size = len(c)
                        amp = sum(p[2] for p in c)
                        ind_f.write(f"{idx:<5} {size:<5} {amp:.2f}\n")
                        
                        # Add to Master File
                        master_f.write(f"{input_file:<15} {idx:<5} {size:<5} {amp:.2f}\n")
                        
                        # Update Stats
                        global_stats["total_clusters"] += 1
                        global_stats["total_hits"] += size
                        global_stats["total_amp"] += amp
                
                print(f"Processed {input_file}")

            except Exception as e:
                print(f"Skipping {input_file}: {e}")

        # Final Summary Block
        if global_stats["total_clusters"] > 0:
            avg_size = global_stats["total_hits"] / global_stats["total_clusters"]
            master_f.write("\n" + "="*45 + "\n")
            master_f.write("GLOBAL SUMMARY STATISTICS\n")
            master_f.write(f"Total Clusters Found:  {global_stats['total_clusters']}\n")
            master_f.write(f"Average Cluster Size:   {avg_size:.2f} pixels\n")
            master_f.write(f"Total Energy Collected: {global_stats['total_amp']:.2f}\n")
            master_f.write("="*45 + "\n")
if __name__ == "__main__":
    batch_process_hits(100)