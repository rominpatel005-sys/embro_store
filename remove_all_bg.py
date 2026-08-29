import os
import collections
from PIL import Image

def remove_bg(img_path, tolerance=40):
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size
    pixels = img.load()
    
    # Reference background colors from top corners
    ref_points = [(10, 10), (w - 10, 10)]
    ref_colors = [pixels[pt[0], pt[1]] for pt in ref_points]
    
    # Generate candidate seeds along top, left, and right borders (avoiding bottom border)
    candidate_seeds = []
    
    # Top border seeds
    for x in range(10, w - 10, 20):
        candidate_seeds.append((x, 10))
        
    # Left and right border seeds (up to 80% height to avoid pants/bottom edge)
    for y in range(10, int(h * 0.8), 20):
        candidate_seeds.append((10, y))
        candidate_seeds.append((w - 10, y))
        
    # Validate seeds: only start flood fill on seeds that match reference colors
    seeds = []
    for s in candidate_seeds:
        r, g, b, a = pixels[s[0], s[1]]
        is_valid = False
        for ref in ref_colors:
            dist = ((r - ref[0])**2 + (g - ref[1])**2 + (b - ref[2])**2)**0.5
            if dist < tolerance:
                is_valid = True
                break
        if is_valid:
            seeds.append(s)
            
    # Queue validated seeds
    queue = collections.deque()
    visited = set()
    for s in seeds:
        queue.append(s)
        visited.add(s)
        
    transparent_count = 0
    
    while queue:
        cx, cy = queue.popleft()
        r, g, b, a = pixels[cx, cy]
        
        # Check distance to any reference colors
        is_bg = False
        for ref in ref_colors:
            dist = ((r - ref[0])**2 + (g - ref[1])**2 + (b - ref[2])**2)**0.5
            if dist < tolerance:
                is_bg = True
                break
                
        if is_bg:
            pixels[cx, cy] = (0, 0, 0, 0)
            transparent_count += 1
            
            # Check 4 neighbors
            for nx, ny in [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]:
                if 0 <= nx < w and 0 <= ny < h:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                        
    img.save(img_path, "PNG")
    print(f"Processed {os.path.basename(img_path)}: made {transparent_count} pixels transparent.")

def process_all():
    path = "media/products"
    for f in sorted(os.listdir(path)):
        if f.endswith('.png') and not f.endswith('_test.png') and not f.endswith('default.png'):
            remove_bg(os.path.join(path, f))

if __name__ == "__main__":
    process_all()
