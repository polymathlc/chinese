"""
Build 11 Gods (including Lu Ban God of Blacksmiths) and 4-Directional Enemies & Bosses.
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

def create_standard_sheet(src_img_path, row_defs, cell_size=(128, 128), out_filename="standard.webp"):
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
    
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    out_sheet.save(out_path, "WEBP", quality=95)
    return out_sheet

def build_all():
    print("Building 4-directional sprite sheets and Lu Ban God of Blacksmith...")
    
    # 1. 4-DIRECTIONAL ENEMIES SHEET (1024x768 -> 8 cols x 6 rows)
    # Each row has 8 frames:
    # 0,1: Front view (Down)
    # 2,3: Back view (Up)
    # 4,5: Right side view (Right)
    # 6,7: Left side view (Left)
    enemies_path = os.path.join(BRAIN_DIR, "enemies_4dir_sheet_1786999201516.jpg")
    enemies_rows = [
        (0, 170, 8, 0, 1024),   # Row 0: Demon Ape (8 frames)
        (170, 341, 8, 0, 1024), # Row 1: Heavenly Spear Soldier (8 frames)
        (341, 512, 8, 0, 1024), # Row 2: Celestial Archer (8 frames)
        (512, 682, 8, 0, 1024), # Row 3: Nether Ghost (8 frames)
        (682, 853, 8, 0, 1024), # Row 4: Daoist Bagua Golem (8 frames)
        (853, 1024, 4, 0, 1024) # Row 5: Cave Spider (4 frames)
    ]
    create_standard_sheet(enemies_path, enemies_rows, cell_size=(128, 128), out_filename="monsters_beasts.webp")
    print("-> Processed 4-directional monsters_beasts.webp")
    
    # 2. 4-DIRECTIONAL WUKONG HERO
    wukong_path = os.path.join(BRAIN_DIR, "wukong_4dir_sheet_1786998960863.jpg")
    wukong_rows = [
        (0, 146, 8, 135, 1024),   # Row 0: Front View Walk (South)
        (146, 292, 8, 135, 1024), # Row 1: Back View Walk (North)
        (292, 438, 8, 135, 1024), # Row 2: Side View Walk & Thrust (East/West)
        (438, 585, 8, 135, 1024), # Row 3: Front View Attack & Smash (South)
        (585, 731, 8, 135, 1024), # Row 4: Back View Attack & Smash (North)
        (731, 877, 8, 135, 1024), # Row 5: Somersault Cloud Dash
        (877, 1024, 8, 135, 1024) # Row 6: Awakened Great Sage & Cloud
    ]
    create_standard_sheet(wukong_path, wukong_rows, cell_size=(128, 128), out_filename="hero.webp")
    print("-> Processed 4-directional hero.webp")

    # 3. BOSSES SHEET
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
    print("-> Processed bosses sheets")

    # 4. GODS ATLAS INCLUDING LU BAN (11 Gods: 6 cols x 2 rows, 256x256 per portrait)
    gods_path = os.path.join(BRAIN_DIR, "chinese_gods_portraits_1786995883867.jpg")
    luban_path = os.path.join(BRAIN_DIR, "luban_blacksmith_god_1786999068452.jpg")
    
    gods_img = Image.open(gods_path).convert("RGBA").resize((1280, 512), Image.Resampling.LANCZOS)
    luban_img = Image.open(luban_path).convert("RGBA").resize((256, 256), Image.Resampling.LANCZOS)
    luban_keyed = key_magenta(luban_img)
    
    # 6 cols x 2 rows = 1536 x 512
    atlas = Image.new("RGBA", (1536, 512), (0, 0, 0, 0))
    atlas.paste(gods_img, (0, 0)) # First 10 gods (5 per row)
    
    # Place Lu Ban at col 5, row 0 (x = 1280, y = 0)
    atlas.paste(luban_keyed, (1280, 0), luban_keyed)
    atlas.save(os.path.join(OUTPUT_DIR, "all_10_gods.webp"), "WEBP", quality=95)
    print("-> Processed 11 Gods atlas including Lu Ban at index 10")

if __name__ == "__main__":
    build_all()
