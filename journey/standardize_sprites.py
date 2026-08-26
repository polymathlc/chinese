"""
Extract, isolate, and standardize every sprite into a pixel-perfect uniform grid with 0 bleed.
"""

import os
from PIL import Image, ImageOps

BRAIN_DIR = r"C:\Users\chung\.gemini\antigravity\brain\36a6f007-4ecb-43da-999f-0581a275fe1c"
OUTPUT_DIR = "assets_webp"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def is_pink(r, g, b):
    return (r > 140 and b > 140 and g < 130) or (r > 165 and b > 135 and (r - g) > 40 and (b - g) > 35)

def key_magenta(img):
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for r, g, b, a in data:
        if is_pink(r, g, b):
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append((r, g, b, 255))
    img.putdata(new_data)
    return img

def create_standard_sheet(src_img_path, row_defs, cell_size=(128, 128), out_filename="standard.webp"):
    """
    row_defs: list of tuples: (row_y_min, row_y_max, num_frames, col_x_min, col_x_max)
    """
    raw_img = Image.open(src_img_path)
    keyed = key_magenta(raw_img)
    
    num_rows = len(row_defs)
    max_cols = max(r[2] for r in row_defs)
    
    out_w = max_cols * cell_size[0]
    out_h = num_rows * cell_size[1]
    out_sheet = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    
    for row_idx, (y_min, y_max, n_frames, x_min, x_max) in enumerate(row_defs):
        row_w = (x_max - x_min) / n_frames
        for frame_idx in range(n_frames):
            fx0 = int(x_min + frame_idx * row_w)
            fx1 = int(x_min + (frame_idx + 1) * row_w)
            
            # Crop frame
            frame = keyed.crop((fx0, y_min, fx1, y_max))
            
            # Find non-transparent bounding box
            bbox = frame.getbbox()
            if bbox:
                cropped_sprite = frame.crop(bbox)
                # Fit inside cell_size with padding
                scale = min((cell_size[0] - 12) / cropped_sprite.width, (cell_size[1] - 12) / cropped_sprite.height)
                if scale < 1.0:
                    new_w = max(1, int(cropped_sprite.width * scale))
                    new_h = max(1, int(cropped_sprite.height * scale))
                    cropped_sprite = cropped_sprite.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                # Center sprite at bottom of cell (foot baseline alignment)
                dest_x = frame_idx * cell_size[0] + (cell_size[0] - cropped_sprite.width) // 2
                dest_y = row_idx * cell_size[1] + (cell_size[1] - cropped_sprite.height) - 6
                out_sheet.paste(cropped_sprite, (dest_x, dest_y), cropped_sprite)
    
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    out_sheet.save(out_path, "WEBP", quality=95)
    print(f"Generated standardized sheet: {out_filename} ({out_w}x{out_h}) with {num_rows} rows x {max_cols} cols.")
    return out_sheet

def process_all():
    print("Processing standardized sprite sheets...")
    
    # 1. WUKONG HERO SHEET (1024x1024 -> 10 cols x 7 rows, 128x128 per cell)
    wukong_path = os.path.join(BRAIN_DIR, "wukong_pink_sheet_1786998019840.jpg")
    wukong_rows = [
        (0, 146, 7, 0, 716),     # Row 0: Idle (7 frames)
        (146, 292, 10, 0, 1024), # Row 1: Run (10 frames)
        (292, 438, 8, 0, 819),   # Row 2: Combo 1 Sweep (8 frames)
        (438, 585, 10, 0, 1024), # Row 3: Combo 2 360 Spin (10 frames)
        (585, 731, 10, 0, 1024), # Row 4: Combo 3 Leap & Smash (10 frames)
        (731, 877, 9, 0, 921),   # Row 5: Dash (9 frames)
        (877, 1024, 10, 0, 1024) # Row 6: Stance & Awakened (10 frames)
    ]
    create_standard_sheet(wukong_path, wukong_rows, cell_size=(128, 128), out_filename="hero.webp")
    
    # 2. BOSSES SHEET (1024x1024 -> 6 cols x 6 rows, 160x160 per cell)
    bosses_path = os.path.join(BRAIN_DIR, "bosses_pink_sheet_1786998590130.jpg")
    bosses_rows = [
        (0, 170, 5, 0, 830),     # Row 0: Spider Demon (5 frames)
        (170, 341, 6, 0, 1024),  # Row 1: Lady White Bone & Skeleton (6 frames)
        (341, 512, 6, 0, 1024),  # Row 2: Golden & Silver Horn Kings (6 frames)
        (512, 682, 6, 0, 1024),  # Row 3: Erlang Shen & Hound (6 frames)
        (682, 853, 6, 0, 1024),  # Row 4: Tathagata Buddha (6 frames)
        (853, 1024, 6, 0, 1024)  # Row 5: Tongbei Yuanhou & Giant Demon Ape (6 frames)
    ]
    create_standard_sheet(bosses_path, bosses_rows, cell_size=(160, 160), out_filename="infinite_bosses_a.webp")
    create_standard_sheet(bosses_path, bosses_rows, cell_size=(160, 160), out_filename="infinite_bosses_b.webp")
    
    # 3. ENEMIES SHEET (1024x1024 -> 5 cols x 6 rows, 128x128 per cell, skipping left text area x < 125)
    enemies_path = os.path.join(BRAIN_DIR, "enemies_pink_sheet_1786998746386.jpg")
    enemies_rows = [
        (0, 170, 4, 125, 1024),   # Row 0: Demon Ape (4 frames)
        (170, 341, 5, 125, 1024),  # Row 1: Toxic Spiderling (5 frames)
        (341, 512, 5, 125, 1024),  # Row 2: Nether Ghost (5 frames)
        (512, 682, 5, 125, 1024),  # Row 3: Heavenly Spear Soldier (5 frames)
        (682, 853, 5, 125, 1024),  # Row 4: Celestial Archer (5 frames)
        (853, 1024, 4, 125, 1024)  # Row 5: Daoist Bagua Golem (4 frames)
    ]
    create_standard_sheet(enemies_path, enemies_rows, cell_size=(128, 128), out_filename="monsters_beasts.webp")
    
    print("All standardized sheets created!")

if __name__ == "__main__":
    process_all()
