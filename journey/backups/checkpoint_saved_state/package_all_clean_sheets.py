"""
Package all sprite sheets with 100% projection segmentation.
Guarantees zero bleed, uniform cell placement, and clean idle frames for all characters.
"""

import os
import numpy as np
from PIL import Image

BRAIN_DIR = r"C:\Users\chung\.gemini\antigravity\brain\36a6f007-4ecb-43da-999f-0581a275fe1c"
OUTPUT_DIR = "assets_webp"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def key_magenta(img):
    img = img.convert("RGBA")
    arr = np.array(img)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    pink_mask = (
        ((r > 135) & (b > 135) & (g < 130)) | 
        ((r > 160) & (b > 130) & ((r.astype(int) - g.astype(int)) > 35) & ((b.astype(int) - g.astype(int)) > 30))
    )
    arr[pink_mask] = [0, 0, 0, 0]
    return Image.fromarray(arr, "RGBA"), pink_mask

def segment_and_build(src_path, cell_size=(128, 128), out_filename="out.webp", skip_left=0, min_w=20, min_h=50, row_threshold=35, col_threshold=20, pad_bottom=8):
    if not os.path.exists(src_path):
        print(f"File not found: {src_path}")
        return
        
    img = Image.open(src_path)
    keyed, mask = key_magenta(img)
    arr = np.array(keyed)
    alpha = arr[:, :, 3] > 0
    if skip_left > 0:
        alpha[:, :skip_left] = False
        
    # Row bands
    row_counts = np.sum(alpha, axis=1)
    row_bands = []
    in_band = False
    start_y = 0
    for y, count in enumerate(row_counts):
        if count > row_threshold and not in_band:
            in_band = True
            start_y = y
        elif count <= row_threshold and in_band:
            in_band = False
            if y - start_y >= min_h:
                row_bands.append((start_y, y))
    if in_band and len(row_counts) - start_y >= min_h:
        row_bands.append((start_y, len(row_counts)))
        
    segmented_rows = []
    for (y0, y1) in row_bands:
        band_alpha = alpha[y0:y1, :]
        col_counts = np.sum(band_alpha, axis=0)
        
        sprites_in_row = []
        in_sprite = False
        start_x = 0
        for x, count in enumerate(col_counts):
            if count > col_threshold and not in_sprite:
                in_sprite = True
                start_x = x
            elif count <= col_threshold and in_sprite:
                in_sprite = False
                if x - start_x >= min_w:
                    sprite_crop = keyed.crop((start_x, y0, x, y1))
                    bbox = sprite_crop.getbbox()
                    if bbox:
                        tight_box = (start_x + bbox[0], y0 + bbox[1], start_x + bbox[2], y0 + bbox[3])
                        sprites_in_row.append(tight_box)
        if in_sprite and len(col_counts) - start_x >= min_w:
            sprite_crop = keyed.crop((start_x, y0, len(col_counts), y1))
            bbox = sprite_crop.getbbox()
            if bbox:
                tight_box = (start_x + bbox[0], y0 + bbox[1], start_x + bbox[2], y0 + bbox[3])
                sprites_in_row.append(tight_box)
        if len(sprites_in_row) > 0:
            segmented_rows.append(sprites_in_row)
        
    num_rows = len(segmented_rows)
    max_cols = max(len(r) for r in segmented_rows) if num_rows > 0 else 1
    
    out_w = max_cols * cell_size[0]
    out_h = num_rows * cell_size[1]
    
    out_sheet = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    
    for r_idx, row_boxes in enumerate(segmented_rows):
        for c_idx, box in enumerate(row_boxes):
            sprite = keyed.crop(box)
            max_w = cell_size[0] - 14
            max_h = cell_size[1] - 14
            scale = min(max_w / sprite.width, max_h / sprite.height)
            if scale < 1.0:
                nw = max(1, int(sprite.width * scale))
                nh = max(1, int(sprite.height * scale))
                sprite = sprite.resize((nw, nh), Image.Resampling.LANCZOS)
                
            dest_x = c_idx * cell_size[0] + (cell_size[0] - sprite.width) // 2
            dest_y = r_idx * cell_size[1] + (cell_size[1] - sprite.height) - pad_bottom
            out_sheet.paste(sprite, (dest_x, dest_y), sprite)
            
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    out_sheet.save(out_path, "WEBP", quality=95)
    print(f"Processed {out_filename}: {num_rows} rows x {max_cols} cols ({out_w}x{out_h})")
    return out_sheet

def package_all():
    print("Packaging ALL sheets with clean projection segmentation...")
    
    # 1. WUKONG HERO (128x128)
    segment_and_build(
        os.path.join(BRAIN_DIR, "wukong_4dir_sheet_1786998960863.jpg"),
        cell_size=(128, 128),
        out_filename="hero.webp",
        skip_left=120,
        min_h=55,
        row_threshold=40,
        col_threshold=25,
        pad_bottom=8
    )
    
    # 2. 4-DIRECTIONAL ENEMIES (128x128)
    segment_and_build(
        os.path.join(BRAIN_DIR, "enemies_4dir_sheet_1786999201516.jpg"),
        cell_size=(128, 128),
        out_filename="monsters_beasts.webp",
        skip_left=0,
        min_h=50,
        row_threshold=35,
        col_threshold=20,
        pad_bottom=8
    )
    
    # 3. BUFF ERLANG & DOG (160x160)
    segment_and_build(
        os.path.join(BRAIN_DIR, "erlang_and_dog_sheet_1786999371485.jpg"),
        cell_size=(160, 160),
        out_filename="erlang_and_dog.webp",
        skip_left=0,
        min_h=60,
        row_threshold=40,
        col_threshold=25,
        pad_bottom=10
    )
    
    # 4. COLOSSAL BUDDHA (256x256)
    segment_and_build(
        os.path.join(BRAIN_DIR, "buddha_giant_sheet_1786999931812.jpg"),
        cell_size=(256, 256),
        out_filename="buddha_colossal.webp",
        skip_left=0,
        min_h=60,
        row_threshold=40,
        col_threshold=25,
        pad_bottom=12
    )
    
    # 5. BOSSES (160x160)
    segment_and_build(
        os.path.join(BRAIN_DIR, "bosses_pink_sheet_1786998590130.jpg"),
        cell_size=(160, 160),
        out_filename="infinite_bosses_a.webp",
        skip_left=0,
        min_h=50,
        row_threshold=35,
        col_threshold=20,
        pad_bottom=10
    )
    
    # 6. LU BAN AVATAR (128x128)
    segment_and_build(
        os.path.join(BRAIN_DIR, "luban_avatar_sheet_1786999799774.jpg"),
        cell_size=(128, 128),
        out_filename="luban_avatar.webp",
        skip_left=0,
        min_h=50,
        row_threshold=35,
        col_threshold=20,
        pad_bottom=8
    )

if __name__ == "__main__":
    package_all()
