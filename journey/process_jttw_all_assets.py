"""
Comprehensive Asset Processor for Journey to the West:
Processes:
- Sun Wukong Hero sheet
- 10 Chinese Immortals portraits
- Tian Ting Heavenly Court seamless floor
- Peaches & Relics icons
- Tianbing, Demons, and Regular Enemies
- Boss Sheet 1: Spider Demon, White Bone, Golden/Silver Horn, Erlang Shen
- Boss Sheet 2: Tathagata Buddha, Tongbei Yuanhou (Evil Twin Final Boss)
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

def key_dark_background(img, threshold=24, softness=16):
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
    print("Processing all JTTW assets...")

    # 1. Hero
    wukong_path = find_latest_image("wukong_hero_sheet")
    with Image.open(wukong_path) as img:
        hero_keyed = key_dark_background(img, threshold=24, softness=16).resize((1024, 1024), Image.Resampling.LANCZOS)
        hero_keyed.save(os.path.join(OUTPUT_DIR, "hero.webp"), "WEBP", quality=92)
        print("-> Saved hero.webp")

    # 2. Chinese Gods
    gods_path = find_latest_image("chinese_gods_portraits")
    with Image.open(gods_path) as img:
        gods_resized = img.convert("RGBA").resize((1280, 512), Image.Resampling.LANCZOS)
        gods_resized.save(os.path.join(OUTPUT_DIR, "all_10_gods.webp"), "WEBP", quality=92)
        gods_resized.save(os.path.join(OUTPUT_DIR, "gods.webp"), "WEBP", quality=92)
        print("-> Saved all_10_gods.webp")

    # 3. Floor
    floor_path = find_latest_image("tianting_heaven_tiles")
    with Image.open(floor_path) as img:
        floor_resized = img.convert("RGB").resize((1024, 1024), Image.Resampling.LANCZOS)
        floor_resized.save(os.path.join(OUTPUT_DIR, "seamless_floor.webp"), "WEBP", quality=92)
        floor_resized.save(os.path.join(OUTPUT_DIR, "consistent_tiles.webp"), "WEBP", quality=92)
        floor_resized.save(os.path.join(OUTPUT_DIR, "tiles.webp"), "WEBP", quality=92)
        print("-> Saved seamless_floor.webp")

    # 4. Peaches & Relics
    peach_path = find_latest_image("peach_and_relics")
    with Image.open(peach_path) as img:
        peach_keyed = key_dark_background(img, threshold=20, softness=15).resize((512, 512), Image.Resampling.LANCZOS)
        peach_keyed.save(os.path.join(OUTPUT_DIR, "reward_icons.webp"), "WEBP", quality=92)
        print("-> Saved reward_icons.webp")

    # 5. Enemies (Tianbing, Archers, Golems, Demons, Ghosts)
    enemies_path = find_latest_image("tianbing_enemies")
    with Image.open(enemies_path) as img:
        enemies_keyed = key_dark_background(img, threshold=22, softness=16).resize((1024, 1024), Image.Resampling.LANCZOS)
        enemies_keyed.save(os.path.join(OUTPUT_DIR, "monsters_beasts.webp"), "WEBP", quality=92)
        enemies_keyed.save(os.path.join(OUTPUT_DIR, "undead_cultists.webp"), "WEBP", quality=92)
        enemies_keyed.save(os.path.join(OUTPUT_DIR, "shade.webp"), "WEBP", quality=92)
        enemies_keyed.save(os.path.join(OUTPUT_DIR, "witch.webp"), "WEBP", quality=92)
        print("-> Saved monsters_beasts.webp & enemy sheets")

    # 6. Boss Sheet 1 (Spider Demon, White Bone, Golden/Silver Horn, Erlang Shen)
    boss1_path = find_latest_image("jttw_bosses_sheet1")
    with Image.open(boss1_path) as img:
        boss1_keyed = key_dark_background(img, threshold=24, softness=16).resize((1024, 1024), Image.Resampling.LANCZOS)
        boss1_keyed.save(os.path.join(OUTPUT_DIR, "infinite_bosses_a.webp"), "WEBP", quality=92)
        boss1_keyed.save(os.path.join(OUTPUT_DIR, "minibosses.webp"), "WEBP", quality=92)
        print("-> Saved infinite_bosses_a.webp & minibosses.webp")

    # 7. Boss Sheet 2 (Tathagata Buddha, Tongbei Yuanhou Final Boss)
    boss2_path = find_latest_image("jttw_bosses_sheet2")
    with Image.open(boss2_path) as img:
        boss2_keyed = key_dark_background(img, threshold=24, softness=16).resize((1024, 1024), Image.Resampling.LANCZOS)
        boss2_keyed.save(os.path.join(OUTPUT_DIR, "infinite_bosses_b.webp"), "WEBP", quality=92)
        boss2_keyed.save(os.path.join(OUTPUT_DIR, "infinite_bosses_c.webp"), "WEBP", quality=92)
        boss2_keyed.save(os.path.join(OUTPUT_DIR, "chronos.webp"), "WEBP", quality=92)
        print("-> Saved infinite_bosses_b.webp & boss sheets")

    print("\nAll assets processed into WebP successfully!")

if __name__ == "__main__":
    process_all()
