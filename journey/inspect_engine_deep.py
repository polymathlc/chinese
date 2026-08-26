import re

source_path = r'c:\Users\chung\Documents\antigravity\serene-turing\generate_game.py'
with open(source_path, 'r', encoding='utf-8') as f:
    text = f.read()

def find_all(pattern):
    return re.findall(pattern, text)

print("=== CANVAS SETUP & ENGINE ===")
for match in re.finditer(r'const canvas = document\.getElementById\(["\']gameCanvas["\']\);(.*?)(?=class |function )', text, re.DOTALL):
    print(match.group(0)[:500])

print("\n=== PROJECTILE CLASS ===")
p_match = re.search(r'class Projectile\s*\{(.*?)\n  \}', text, re.DOTALL)
if p_match:
    print(p_match.group(0)[:400])

print("\n=== ANIMATED FX CLASSES ===")
fx_classes = re.findall(r'class Animated\w+\s*\{', text)
print("FX Classes:", fx_classes)

print("\n=== REWARD TYPES ===")
rew_match = re.search(r'function getRewardType\w*\(.*?\)\s*\{(.*?)\n  \}', text, re.DOTALL)
if rew_match:
    print(rew_match.group(0))

print("\n=== GAME OVER & SAVE STATE ===")
save_matches = re.findall(r'localStorage\.\w+\([^)]+\)', text)
print("LocalStorage usage:", set(save_matches))
