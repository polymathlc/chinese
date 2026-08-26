"""
Pure Python + PIL + Numpy Perfect Sprite Segmenter and Grid Packager.
Finds row bands using horizontal pixel projection, then finds column sprites using vertical projection.
Zero bleed, perfect centering in isolated grid cells.
"""

import os
import numpy as np
from PIL import Image

BRAIN_DIR = r"C:\Users\chung\.gemini\antigravity\brain\36a6f007-4ecb-43da-999f-0581a275fe1c"
OUTPUT_DIR = "assets_webp"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def is_pink(r, g, b):
    # Pink chroma-key condition
    return (r > 135 and b > 135 and g < 130) or (r > 160 and b > 130 and (r - g) > 35 and (b - g) > 30)

def key_image(img):
    img = img.convert("RGBA")
    arr = np.array(img)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    pink_mask = (
        ((r > 135) & (b > 135) & (g < 130)) | 
        ((r > 160) & (b > 130) & ((r.astype(int) - g.astype(int)) > 35) & ((b.astype(int) - g.astype(int)) > 30))
    )
    arr[pink_mask] = [0, 0, 0, 0]
    return Image.fromarray(arr, "RGBA"), pink_mask

def segment_sprites_by_projection(keyed_img, pink_mask, skip_left=0, min_w=20, min_h=25):
    arr = np.array(keyed_img)
    alpha = arr[:, :, 3] > 0
    
    if skip_left > 0:
        alpha[:, :skip_left] = False
        
    # 1. Horizontal projection (sum of active pixels along each row)
    row_counts = np.sum(alpha, axis=1)
    
    # Find contiguous row bands
    row_bands = []
    in_band = False
    start_y = 0
    for y, count in enumerate(row_counts):
        if count > 15 and not in_band:
            in_band = True
            start_y = y
        elif count <= 15 and in_band:
            in_band = False
            if y - start_y >= min_h:
                row_bands.append((start_y, y))
    if in_band and len(row_counts) - start_y >= min_h:
        row_bands.append((start_y, len(row_counts)))
        
    print(f"Detected {len(row_bands)} row bands:")
    for i, (y0, y1) in enumerate(row_bands):
        print(f"  Row {i}: y={y0}..{y1} (height={y1-y0})")
        
    # 2. For each row band, perform vertical projection
    segmented_rows = []
    for (y0, y1) in row_bands:
        band_alpha = alpha[y0:y1, :]
        col_counts = np.sum(band_alpha, axis=0)
        
        sprites_in_row = []
        in_sprite = False
        start_x = 0
        for x, count in enumerate(col_counts):
            if count > 5 and not in_sprite:
                in_sprite = True
                start_x = x
            elif count <= 5 and in_sprite:
                in_sprite = False
                if x - start_x >= min_w:
                    # Found a sprite box!
                    sprite_crop = keyed_img.crop((start_x, y0, x, y1))
                    bbox = sprite_crop.getbbox()
                    if bbox:
                        # Exact tight bounding box
                        tight_box = (start_x + bbox[0], y0 + bbox[1], start_x + bbox[2], y0 + bbox[3])
                        sprites_in_row.append(tight_box)
        if in_sprite and len(col_counts) - start_x >= min_w:
            sprite_crop = keyed_img.crop((start_x, y0, len(col_counts), y1))
            bbox = sprite_crop.getbbox()
            if bbox:
                tight_box = (start_x + bbox[0], y0 + bbox[1], start_x + bbox[2], y0 + bbox[3])
                sprites_in_row.append(tight_box)
                
        print(f"  -> Found {len(sprites_in_row)} sprites in row")
        segmented_rows.append(sprites_in_row)
        
    return segmented_rows

def build_grid_from_segments(keyed_img, segmented_rows, cell_size=(128, 128), out_filename="grid.webp", pad_bottom=8):
    num_rows = len(segmented_rows)
    max_cols = max(len(r) for r in segmented_rows) if num_rows > 0 else 1
    
    out_w = max_cols * cell_size[0]
    out_h = num_rows * cell_size[1]
    
    out_sheet = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    
    for r_idx, row_boxes in enumerate(segmented_rows):
        for c_idx, box in enumerate(row_boxes):
            sprite = keyed_img.crop(box)
            
            # Scale proportionally to fit inside cell with padding
            max_avail_w = cell_size[0] - 16
            max_avail_h = cell_size[1] - 16
            
            scale = min(max_avail_w / sprite.width, max_avail_h / sprite.height)
            if scale < 1.0:
                nw = max(1, int(sprite.width * scale))
                nh = max(1, int(sprite.height * scale))
                sprite = sprite.resize((nw, nh), Image.Resampling.LANCZOS)
                
            dest_x = c_idx * cell_size[0] + (cell_size[0] - sprite.width) // 2
            dest_y = r_idx * cell_size[1] + (cell_size[1] - sprite.height) - pad_bottom
            
            out_sheet.paste(sprite, (dest_x, dest_y), sprite)
            
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    out_sheet.save(out_path, "WEBP", quality=95)
    print(f"Packaged {out_filename} -> {out_w}x{out_h} ({num_rows} rows, {max_cols} cols)")
    return out_sheet

if __name__ == "__main__":
    wukong_path = os.path.join(BRAIN_DIR, "wukong_4dir_sheet_1786998960863.jpg")
    img = Image.open(wukong_path)
    keyed, mask = key_image(img)
    rows = segment_sprites_by_projection(keyed, mask, skip_left=120)
    build_grid_from_segments(keyed, rows, cell_size=(128, 128), out_filename="hero.webp")
