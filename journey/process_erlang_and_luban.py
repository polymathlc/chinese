"""
Process Buff Heavily Armored Erlang Shen & Xiao Tian Quan, and Lu Ban In-Game Avatar Character.
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

def process_all():
    print("Processing Buff Erlang Shen, Xiao Tian Quan, and Lu Ban in-game avatar...")
    
    # 1. LUBAN AVATAR SHEET (8 cols x 4 rows, 128x128 per cell)
    luban_avatar_path = os.path.join(BRAIN_DIR, "luban_avatar_sheet_1786999799774.jpg")
    luban_rows = [
        (0, 256, 8, 0, 1024),   # Row 0: Idle & Walk avatar
        (256, 512, 8, 0, 1024), # Row 1: Hammering anvil with forge sparks
        (512, 768, 8, 0, 1024), # Row 2: Gear runes & weapon mastery
        (768, 1024, 4, 0, 1024) # Row 3: Golden anvil & forge station
    ]
    create_standard_sheet(luban_avatar_path, luban_rows, cell_size=(128, 128), out_filename="luban_avatar.webp")
    print("-> Created luban_avatar.webp")

    # 2. ERLANG SHEN & XIAO TIAN QUAN SHEET (4 cols x 5 rows, 160x160 per cell)
    erlang_path = os.path.join(BRAIN_DIR, "erlang_and_dog_sheet_1786999371485.jpg")
    erlang_rows = [
        (0, 204, 4, 0, 1024),   # Row 0: Buff Erlang Trident Spear stance
        (204, 409, 4, 0, 1024), # Row 1: Erlang Trident Spear lightning slash
        (409, 614, 4, 0, 1024), # Row 2: Erlang command & smash attack
        (614, 819, 4, 0, 1024), # Row 3: Xiao Tian Quan Hound running & leaping
        (819, 1024, 4, 0, 1024) # Row 4: Xiao Tian Quan Hound pouncing & biting
    ]
    create_standard_sheet(erlang_path, erlang_rows, cell_size=(160, 160), out_filename="erlang_and_dog.webp")
    print("-> Created erlang_and_dog.webp")

    # 3. Update Bosses Sheet with Buff Erlang Shen & Trident
    bosses_path = os.path.join(BRAIN_DIR, "bosses_pink_sheet_1786998590130.jpg")
    bosses_rows = [
        (0, 170, 5, 0, 830),     # Row 0: Spider Demon (5 frames)
        (170, 341, 6, 0, 1024),  # Row 1: Lady White Bone & Skeleton (6 frames)
        (341, 512, 6, 0, 1024),  # Row 2: Golden & Silver Horn Kings (6 frames)
        (512, 682, 6, 0, 1024),  # Row 3: Erlang Shen & Hound
        (682, 853, 6, 0, 1024),  # Row 4: Tathagata Buddha (6 frames)
        (853, 1024, 6, 0, 1024)  # Row 5: Tongbei Yuanhou & Giant Demon Ape (6 frames)
    ]
    create_standard_sheet(bosses_path, bosses_rows, cell_size=(160, 160), out_filename="infinite_bosses_a.webp")
    create_standard_sheet(bosses_path, bosses_rows, cell_size=(160, 160), out_filename="infinite_bosses_b.webp")
    print("-> Updated infinite_bosses_a.webp")

if __name__ == "__main__":
    process_all()
