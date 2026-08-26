"""
Process newly generated Journey to the West assets:
- Wukong hero sprite sheet
- 10 Chinese Gods portraits
- Tian Ting Heavenly Court floor tiles
- Heavenly Peaches and Relics
- Tianbing, Giant Spirit God, Bagua Golem, Demon and Ghost enemies
"""

import os
from PIL import Image, ImageOps, ImageFilter

BRAIN_DIR = r"C:\Users\chung\.gemini\antigravity\brain\36a6f007-4ecb-43da-999f-0581a275fe1c"
OUTPUT_DIR = "assets_webp"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def find_latest_image(prefix):
    matches = [f for f in os.listdir(BRAIN_DIR) if f.startswith(prefix) and f.endswith(".jpg")]
    if not matches:
        raise FileNotFoundError(f"No image starting with {prefix} found in {BRAIN_DIR}")
    matches.sort(key=lambda x: os.path.getmtime(os.path.join(BRAIN_DIR, x)), reverse=True)
    return os.path.join(BRAIN_DIR, matches[0])

# Keying function for dark backgrounds on sprites
def key_dark_background(img, threshold=28, softness=18):
    img = img.convert("RGBA")
    data = img.getdata()
    newData = []
    for item in data:
        r, g, b, a = item
        brightness = max(r, g, b)
        if brightness < threshold:
            newData.append((r, g, b, 0))
        elif brightness < threshold + softness:
            factor = (brightness - threshold) / softness
            newData.append((r, g, b, int(255 * factor)))
        else:
            newData.append((r, g, b, 255))
    img.putdata(newData)
    return img

def process_all():
    print("Processing new Journey to the West assets...")

    # 1. Hero: Sun Wukong
    wukong_path = find_latest_image("wukong_hero_sheet")
    print(f"Loading Wukong hero sheet: {wukong_path}")
    with Image.open(wukong_path) as img:
        # Convert to 1024x1024 keyed RGBA
        hero_keyed = key_dark_background(img, threshold=24, softness=16)
        hero_keyed = hero_keyed.resize((1024, 1024), Image.Resampling.LANCZOS)
        hero_keyed.save(os.path.join(OUTPUT_DIR, "hero.webp"), "WEBP", quality=92)
        print("-> Saved new hero.webp")

    # 2. Chinese Gods (10 Deities, 5x2 grid)
    gods_path = find_latest_image("chinese_gods_portraits")
    print(f"Loading Chinese Gods portraits: {gods_path}")
    with Image.open(gods_path) as img:
        # Resize to 1280x512 (5 cols x 2 rows of 256x256)
        gods_resized = img.convert("RGBA").resize((1280, 512), Image.Resampling.LANCZOS)
        gods_resized.save(os.path.join(OUTPUT_DIR, "all_10_gods.webp"), "WEBP", quality=92)
        gods_resized.save(os.path.join(OUTPUT_DIR, "gods.webp"), "WEBP", quality=92)
        print("-> Saved new all_10_gods.webp and gods.webp")

    # 3. Heavenly Court Tian Ting Floor
    floor_path = find_latest_image("tianting_heaven_tiles")
    print(f"Loading Tian Ting floor: {floor_path}")
    with Image.open(floor_path) as img:
        floor_resized = img.convert("RGB").resize((1024, 1024), Image.Resampling.LANCZOS)
        floor_resized.save(os.path.join(OUTPUT_DIR, "seamless_floor.webp"), "WEBP", quality=92)
        floor_resized.save(os.path.join(OUTPUT_DIR, "consistent_tiles.webp"), "WEBP", quality=92)
        floor_resized.save(os.path.join(OUTPUT_DIR, "tiles.webp"), "WEBP", quality=92)
        print("-> Saved new seamless_floor.webp, consistent_tiles.webp, and tiles.webp")

    # 4. Peaches & Relics (2x2 grid)
    peach_path = find_latest_image("peach_and_relics")
    print(f"Loading Peaches and Relics: {peach_path}")
    with Image.open(peach_path) as img:
        peach_keyed = key_dark_background(img, threshold=20, softness=15)
        peach_keyed = peach_keyed.resize((512, 512), Image.Resampling.LANCZOS)
        peach_keyed.save(os.path.join(OUTPUT_DIR, "reward_icons.webp"), "WEBP", quality=92)
        print("-> Saved new reward_icons.webp")

    # 5. Tianbing, Giant Spirit God, Bagua Golem, and Mythic Enemies
    enemies_path = find_latest_image("tianbing_enemies")
    print(f"Loading Enemies sprite sheet: {enemies_path}")
    with Image.open(enemies_path) as img:
        enemies_keyed = key_dark_background(img, threshold=22, softness=16)
        enemies_keyed = enemies_keyed.resize((1024, 1024), Image.Resampling.LANCZOS)
        enemies_keyed.save(os.path.join(OUTPUT_DIR, "monsters_beasts.webp"), "WEBP", quality=92)
        enemies_keyed.save(os.path.join(OUTPUT_DIR, "undead_cultists.webp"), "WEBP", quality=92)
        enemies_keyed.save(os.path.join(OUTPUT_DIR, "minibosses.webp"), "WEBP", quality=92)
        enemies_keyed.save(os.path.join(OUTPUT_DIR, "shade.webp"), "WEBP", quality=92)
        enemies_keyed.save(os.path.join(OUTPUT_DIR, "witch.webp"), "WEBP", quality=92)
        enemies_keyed.save(os.path.join(OUTPUT_DIR, "chronos.webp"), "WEBP", quality=92)
        print("-> Saved new monsters_beasts.webp, undead_cultists.webp, minibosses.webp, and enemy sheets")

    print("\nAll brand new Journey to the West assets processed successfully!")

if __name__ == "__main__":
    process_all()
