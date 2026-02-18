import math
import numpy as np


def find_clusters_euclidean(hits, distance_threshold=2):
    """
    hits: Dictionary {(x, y): amplitude}
    distance_threshold: Max Euclidean distance to link pixels
    """
    visited = set()
    final_clusters = []
    
    # We still use a bounding box for performance, then verify with Euclidean
    search_range = math.ceil(distance_threshold)

    for pixel in hits:
        if pixel not in visited:
            current_cluster = []
            stack = [pixel]
            visited.add(pixel)
            
            while stack:
                curr_x, curr_y = stack.pop()
                current_cluster.append((curr_x, curr_y, hits[(curr_x, curr_y)]))
                
                # Check pixels within the bounding box range
                for dx in range(-search_range, search_range + 1):
                    for dy in range(-search_range, search_range + 1):
                        if dx == 0 and dy == 0: continue
                        
                        # Calculate Euclidean Distance
                        dist = math.sqrt(dx**2 + dy**2)
                        
                        if dist <= distance_threshold:
                            neighbor = (curr_x + dx, curr_y + dy)
                            if neighbor in hits and neighbor not in visited:
                                visited.add(neighbor)
                                stack.append(neighbor)
            
            # Exclusion logic: Only keep clusters with more than 1 hit
            if len(current_cluster) > 1:
                final_clusters.append(current_cluster)
                
    return final_clusters
def process_detector_data(filename):
    # 1. Load data from text file (assumes format: x y amplitude)
    data = np.loadtxt(filename)
    hits = {(int(x), int(y)): amp for x, y, amp in data}
    
    # 2. Run Clustering
    clusters = find_clusters_euclidean(hits)
    
    # 3. Analyze Clusters
    print(f"Found {len(clusters)} clusters.\n")
    print(f"{'ID':<5} | {'Size':<5} | {'Total Amp':<10} | {'Centroid (X, Y)':<20}")
    print("-" * 55)
    
    for i, clus in enumerate(clusters):
        total_amp = sum(p[2] for p in clus)
        # Center of Gravity calculation
        avg_x = sum(p[0] * p[2] for p in clus) / total_amp
        avg_y = sum(p[1] * p[2] for p in clus) / total_amp
        
        print(f"{i:<5} | {len(clus):<5} | {total_amp:<10.2f} | ({avg_x:.2f}, {avg_y:.2f})")

# Example usage:
process_detector_data("hits.txt")