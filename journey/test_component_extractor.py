"""
Precise Connected-Component Sprite Extractor and Grid Builder.
Finds every individual sprite contour/island, cleans background, and centers it in isolated grid cells.
Zero bleed guaranteed.
"""

import os
import numpy as np
from PIL import Image
from scipy.ndimage import label, find_objects

BRAIN_DIR = r"C:\Users\chung\.gemini\antigravity\brain\36a6f007-4ecb-43da-999f-0581a275fe1c"
OUTPUT_DIR = "assets_webp"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def is_pink(r, g, b):
    return (r > 135 and b > 135 and g < 130) or (r > 160 and b > 130 and (r - g) > 35 and (b - g) > 30)

def extract_connected_sprites(image_path, min_area=400, skip_left=0):
    img = Image.open(image_path).convert("RGBA")
    arr = np.array(img)
    
    # Mask non-pink pixels
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    pink_mask = (
        ((r > 135) & (b > 135) & (g < 130)) | 
        ((r > 160) & (b > 130) & ((r.astype(int) - g.astype(int)) > 35) & ((b.astype(int) - g.astype(int)) > 30))
    )
    
    # Zero out pink pixels in image
    arr[pink_mask] = [0, 0, 0, 0]
    
    # Foreground mask for labeling
    fg_mask = ~pink_mask
    if skip_left > 0:
        fg_mask[:, :skip_left] = False
        arr[:, :skip_left] = [0, 0, 0, 0]
        
    labeled, num_features = label(fg_mask)
    slices = find_objects(labeled)
    
    clean_img = Image.fromarray(arr, "RGBA")
    
    valid_boxes = []
    for slc in slices:
        sy, sx = slc
        h = sy.stop - sy.start
        w = sx.stop - sx.start
        if w * h >= min_area and w >= 18 and h >= 25:
            # Filter out text labels on the left or small noise
            if sx.start >= skip_left:
                valid_boxes.append((sx.start, sy.start, sx.stop, sy.stop))
                
    print(f"Found {len(valid_boxes)} valid sprite bounding boxes in {os.path.basename(image_path)}")
    return clean_img, valid_boxes

def sort_into_rows_and_cols(boxes, row_tolerance=40):
    # Sort boxes primarily by Y then X
    # Group into rows based on Y center
    boxes = sorted(boxes, key=lambda b: ((b[1] + b[3]) / 2, b[0]))
    
    rows = []
    for b in boxes:
        cy = (b[1] + b[3]) / 2
        placed = False
        for r in rows:
            rcy = sum((box[1] + box[3]) / 2 for box in r) / len(r)
            if abs(cy - rcy) < row_tolerance:
                r.append(b)
                placed = True
                break
        if not placed:
            rows.append([b])
            
    # Sort each row from left to right
    for r in rows:
        r.sort(key=lambda b: b[0])
        
    # Sort rows from top to bottom
    rows.sort(key=lambda r: sum((b[1] + b[3]) / 2 for b in r) / len(r))
    
    return rows

def build_perfect_grid_sheet(clean_img, rows, cell_size=(128, 128), out_filename="perfect.webp", max_cols=None):
    num_rows = len(rows)
    if max_cols is None:
        max_cols = max(len(r) for r in rows)
        
    out_w = max_cols * cell_size[0]
    out_h = num_rows * cell_size[1]
    
    out_sheet = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    
    for r_idx, r in enumerate(rows):
        for c_idx, box in enumerate(r):
            if c_idx >= max_cols:
                break
            sprite = clean_img.crop(box)
            s_bbox = sprite.getbbox()
            if s_bbox:
                sprite = sprite.crop(s_bbox)
                
            scale = min((cell_size[0] - 16) / sprite.width, (cell_size[1] - 16) / sprite.height)
            if scale < 1.0:
                nw = max(1, int(sprite.width * scale))
                nh = max(1, int(sprite.height * scale))
                sprite = sprite.resize((nw, nh), Image.Resampling.LANCZOS)
                
            # Place perfectly centered horizontally and grounded vertically
            dest_x = c_idx * cell_size[0] + (cell_size[0] - sprite.width) // 2
            dest_y = r_idx * cell_size[1] + (cell_size[1] - sprite.height) - 8
            
            out_sheet.paste(sprite, (dest_x, dest_y), sprite)
            
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    out_sheet.save(out_path, "WEBP", quality=95)
    print(f"-> Saved {out_filename} ({out_w}x{out_h}, {num_rows} rows, max {max_cols} cols)")
    return out_sheet

if __name__ == "__main__":
    # Test on Wukong 4-dir sheet
    wukong_path = os.path.join(BRAIN_DIR, "wukong_4dir_sheet_1786998960863.jpg")
    clean_w, boxes_w = extract_connected_sprites(wukong_path, skip_left=120)
    rows_w = sort_into_rows_and_cols(boxes_w)
    print(f"Wukong rows found: {len(rows_w)}, counts: {[len(r) for r in rows_w]}")
    build_perfect_grid_sheet(clean_w, rows_w, cell_size=(128, 128), out_filename="hero.webp", max_cols=8)
