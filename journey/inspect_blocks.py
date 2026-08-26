import re

source_path = r'c:\Users\chung\Documents\antigravity\serene-turing\generate_game.py'
with open(source_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("File line count:", len(lines))

def get_block(start_str, end_str=None, max_l=100):
    recording = False
    out = []
    for l in lines:
        if not recording and start_str in l:
            recording = True
        if recording:
            out.append(l)
            if end_str and end_str in l and len(out) > 1:
                break
            if len(out) >= max_l:
                break
    return ''.join(out)

print("=== ENEMY TYPES ===")
print(get_block("const ENEMY_TYPES =", "};", 120))

print("\n=== REWARDS & GATES ===")
print(get_block("function setupExitGates", "function openGodBoonModal", 80))

print("\n=== POM MODAL ===")
print(get_block("function openPomModal", "function openCharonShop", 80))

print("\n=== ALTAR OF ASHES / ARCANA ===")
print(get_block("function openAltarOfAshes", "function updateHUD", 80))
