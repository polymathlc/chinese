"""
Extract and standardize 4-directional Sun Wukong sprite sheet:
- Down / South: Front View (Row 0 walk, Row 3 attack)
- Up / North: Back View (Row 1 walk, Row 4 attack)
- Right / East: Side View (Row 2 walk/attack)
- Left / West: Side View mirrored (facing = -1)
- Dash / Somersault Cloud: Row 5 & 6
"""

import os
from PIL import Image

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

def create_4dir_hero_sheet():
    src_path = os.path.join(BRAIN_DIR, "wukong_4dir_sheet_1786998960863.jpg")
    raw_img = Image.open(src_path)
    keyed = key_magenta(raw_img)
    
    # 7 rows, 8 frames each (skipping x < 135 to avoid left labels)
    row_defs = [
        (0, 146, 8, 135, 1024),   # Row 0: Front View Walk (South)
        (146, 292, 8, 135, 1024), # Row 1: Back View Walk (North)
        (292, 438, 8, 135, 1024), # Row 2: Side View Walk & Thrust (East/West)
        (438, 585, 8, 135, 1024), # Row 3: Front View Attack & Smash (South)
        (585, 731, 8, 135, 1024), # Row 4: Back View Attack & Smash (North)
        (731, 877, 8, 135, 1024), # Row 5: Somersault Cloud Dash
        (877, 1024, 8, 135, 1024) # Row 6: Awakened & Cloud Special
    ]
    
    cell_size = (128, 128)
    num_rows = len(row_defs)
    num_cols = 8
    out_w = num_cols * cell_size[0]
    out_h = num_rows * cell_size[1]
    
    out_sheet = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    
    for row_idx, (y_min, y_max, n_frames, x_min, x_max) in enumerate(row_defs):
        row_w = (x_max - x_min) / n_frames
        for frame_idx in range(n_frames):
            fx0 = int(x_min + frame_idx * row_w)
            fx1 = int(x_min + (frame_idx + 1) * row_w)
            
            frame = keyed.crop((fx0, y_min, fx1, y_max))
            bbox = frame.getbbox()
            if bbox:
                cropped = frame.crop(bbox)
                scale = min((cell_size[0] - 12) / cropped.width, (cell_size[1] - 12) / cropped.height)
                if scale < 1.0:
                    nw = max(1, int(cropped.width * scale))
                    nh = max(1, int(cropped.height * scale))
                    cropped = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
                
                dest_x = frame_idx * cell_size[0] + (cell_size[0] - cropped.width) // 2
                dest_y = row_idx * cell_size[1] + (cell_size[1] - cropped.height) - 6
                out_sheet.paste(cropped, (dest_x, dest_y), cropped)
                
    out_path = os.path.join(OUTPUT_DIR, "hero.webp")
    out_sheet.save(out_path, "WEBP", quality=95)
    print(f"Created 4-directional hero.webp: {out_w}x{out_h} (8 cols x 7 rows)")

if __name__ == "__main__":
    create_4dir_hero_sheet()
