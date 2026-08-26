"""
Process giant colossal Buddha sprite sheet.
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

def create_standard_sheet(src_img_path, row_defs, cell_size=(256, 256), out_filename="standard.webp"):
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
                scale = min((cell_size[0] - 16) / cropped.width, (cell_size[1] - 16) / cropped.height)
                if scale < 1.0:
                    nw = max(1, int(cropped.width * scale))
                    nh = max(1, int(cropped.height * scale))
                    cropped = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
                
                dest_x = frame_idx * cell_size[0] + (cell_size[0] - cropped.width) // 2
                dest_y = row_idx * cell_size[1] + (cell_size[1] - cropped.height) - 10
                out_sheet.paste(cropped, (dest_x, dest_y), cropped)
    
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    out_sheet.save(out_path, "WEBP", quality=95)
    return out_sheet

def process_buddha():
    buddha_path = os.path.join(BRAIN_DIR, "buddha_giant_sheet_1786999931812.jpg")
    buddha_rows = [
        (0, 256, 5, 0, 1024),   # Row 0: Giant Buddha Seated on Lotus
        (256, 512, 6, 0, 1024), # Row 1: Colossal Golden Palm Slam (如来神掌)
        (512, 768, 6, 0, 1024), # Row 2: Lotus Chakra Waves
        (768, 1024, 7, 0, 1024) # Row 3: Buddha Blessing & Approval Mudra
    ]
    create_standard_sheet(buddha_path, buddha_rows, cell_size=(256, 256), out_filename="buddha_colossal.webp")
    print("-> Created colossal buddha_colossal.webp (7 cols x 4 rows, 256x256 per cell)")

if __name__ == "__main__":
    process_buddha()
