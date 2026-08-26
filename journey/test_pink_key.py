"""
Test chroma-keying for the pink background sprite sheets
"""

import os
from PIL import Image

BRAIN_DIR = r"C:\Users\chung\.gemini\antigravity\brain\36a6f007-4ecb-43da-999f-0581a275fe1c"
OUTPUT_DIR = "assets_webp"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def find_latest_image(prefix):
    matches = [f for f in os.listdir(BRAIN_DIR) if f.startswith(prefix) and f.endswith(".jpg")]
    if not matches:
        raise FileNotFoundError(f"No image starting with {prefix} found in {BRAIN_DIR}")
    matches.sort(key=lambda x: os.path.getmtime(os.path.join(BRAIN_DIR, x)), reverse=True)
    return os.path.join(BRAIN_DIR, matches[0])

def key_pink_background(img):
    img = img.convert("RGBA")
    data = img.getdata()
    newData = []
    for item in data:
        r, g, b, a = item
        # Magenta pink check: high R, high B, low G
        is_pink = (r > 150 and b > 150 and g < 120) or (r > 170 and b > 140 and (r - g) > 50 and (b - g) > 40)
        if is_pink:
            newData.append((0, 0, 0, 0))
        else:
            newData.append((r, g, b, 255))
    img.putdata(newData)
    return img

def process():
    print("Testing Pink Chroma Keying...")

    # 1. Wukong
    wukong_path = find_latest_image("wukong_pink_sheet")
    print(f"Processing Wukong: {wukong_path}")
    with Image.open(wukong_path) as img:
        keyed = key_pink_background(img)
        keyed.save(os.path.join(OUTPUT_DIR, "hero.webp"), "WEBP", quality=95)
        print("-> Saved clean hero.webp")

    # 2. Bosses
    bosses_path = find_latest_image("bosses_pink_sheet")
    print(f"Processing Bosses: {bosses_path}")
    with Image.open(bosses_path) as img:
        keyed = key_pink_background(img)
        keyed.save(os.path.join(OUTPUT_DIR, "infinite_bosses_a.webp"), "WEBP", quality=95)
        keyed.save(os.path.join(OUTPUT_DIR, "infinite_bosses_b.webp"), "WEBP", quality=95)
        print("-> Saved clean bosses sheets")

    # 3. Enemies
    enemies_path = find_latest_image("enemies_pink_sheet")
    print(f"Processing Enemies: {enemies_path}")
    with Image.open(enemies_path) as img:
        # Crop out left margin (0 to 110) where text was, then key
        w, h = img.size
        # Crop text on left: replace x from 0 to 125 with pure pink if it's text, or crop
        # Let's key first
        keyed = key_pink_background(img)
        # Clear the left text margin (x < 120) so no text remains
        pix = keyed.load()
        for y in range(h):
            for x in range(min(125, w)):
                # If there are non-transparent pixels in the text margin, clear them
                pix[x, y] = (0, 0, 0, 0)
        keyed.save(os.path.join(OUTPUT_DIR, "monsters_beasts.webp"), "WEBP", quality=95)
        print("-> Saved clean monsters_beasts.webp")

    print("All pink-keyed assets processed successfully!")

if __name__ == "__main__":
    process()
