import numpy as np
import math

def find_clusters_euclidean(hits, distance_threshold=1.5):
    visited = set()
    final_clusters = []
    search_range = math.ceil(distance_threshold)

    # Convert dictionary keys to a list to iterate
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
                        
                        dist = math.sqrt(dx**2 + dy**2)
                        if dist <= distance_threshold:
                            neighbor = (curr_x + dx, curr_y + dy)
                            if neighbor in hits and neighbor not in visited:
                                visited.add(neighbor)
                                stack.append(neighbor)
            
            #if len(current_cluster) > 1:
            final_clusters.append(current_cluster)
                
    return final_clusters

def batch_process_hits(num_files=100):
    for i in range(1, num_files + 1):
        input_file = f"hits_{i}.txt"
        output_file = f"results_{i}.txt"
        
        try:
            # 1. Load data
            # Assumes format: x y amplitude
            data = np.loadtxt(input_file)
            hits = {(int(row[0]), int(row[1])): row[2] for row in data}
            
            # 2. Run clustering
            clusters = find_clusters_euclidean(hits, distance_threshold=1.5)
            
            # 3. Prepare results for saving (excluding centroid)
            with open(output_file, "w") as f:
                f.write(f"{'ID':<5} {'Size':<5} {'Total_Amp':<10}\n")
                f.write("-" * 25 + "\n")
                
                for idx, clus in enumerate(clusters):
                    total_amp = sum(p[2] for p in clus)
                    size = len(clus)
                    f.write(f"{idx:<5} {size:<5} {total_amp:<10.2f}\n")
            
            print(f"Successfully processed {input_file} -> {output_file}")
            
        except FileNotFoundError:
            print(f"Warning: {input_file} not found. Skipping...")
        except Exception as e:
            print(f"Error processing {input_file}: {e}")

# Run the batch process
if __name__ == "__main__":
    batch_process_hits(100)