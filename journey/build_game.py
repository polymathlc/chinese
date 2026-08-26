"""
Journey to the West: Havoc in Heaven (西游记·大闹天宫)
Game Build Script: Compiles the full game with base64 assets and procedural sound into index.html
"""

import os
import json
import base64

assets_keys = [
    'hero', 'shade', 'witch', 'chronos',
    'consistent_tiles', 'seamless_floor', 'props', 'ui',
    'clean_fx', 'attack_fx_vfx', 'combo_special_vfx', 'elemental_spells_vfx',
    'all_10_gods', 'monsters_beasts', 'undead_cultists', 'new_projectiles',
    'minibosses', 'reward_icons',
    'infinite_bosses_a', 'infinite_bosses_b', 'infinite_bosses_c'
]

b64_data = {}
assets_dir = "assets_webp"
for k in assets_keys:
    webp_path = os.path.join(assets_dir, f"{k}.webp")
    if os.path.exists(webp_path):
        with open(webp_path, 'rb') as fp:
            enc = base64.b64encode(fp.read()).decode('utf-8')
            b64_data[k] = f"data:image/webp;base64,{enc}"
    else:
        print(f"Warning: asset {k}.webp not found in {assets_dir}")

print(f"Loaded {len(b64_data)} assets into memory.")

with open("generate_game.py", "w", encoding="utf-8") as f:
    f.write(f'''# Auto-generated build file
import json
import base64
import os

b64_data = {json.dumps(b64_data)}
print(f"Loaded {{len(b64_data)}} embedded assets.")
''')

print("Base setup ready.")
