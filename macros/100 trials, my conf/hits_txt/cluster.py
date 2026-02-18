import numpy as np

def find_clusters_extended(hits, search_range=5):
    """
    hits: Dictionary {(x, y): amplitude}
    search_range: Distance in pixels to search for neighbors (default 1)
    """
    visited = set()
    clusters = []

    for pixel in hits:
        if pixel not in visited:
            current_cluster = []
            stack = [pixel]
            visited.add(pixel)
            
            while stack:
                curr_x, curr_y = stack.pop()
                current_cluster.append((curr_x, curr_y, hits[(curr_x, curr_y)]))
                
                # Search within the defined range
                for dx in range(-search_range, search_range + 1):
                    for dy in range(-search_range, search_range + 1):
                        if dx == 0 and dy == 0: continue
                        
                        neighbor = (curr_x + dx, curr_y + dy)
                        
                        if neighbor in hits and neighbor not in visited:
                            visited.add(neighbor)
                            stack.append(neighbor)
            
            clusters.append(current_cluster)
    return clusters
def process_detector_data(filename):
    # 1. Load data from text file (assumes format: x y amplitude)
    data = np.loadtxt(filename)
    hits = {(int(x), int(y)): amp for x, y, amp in data}
    
    # 2. Run Clustering
    clusters = find_clusters_extended(hits)
    
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
