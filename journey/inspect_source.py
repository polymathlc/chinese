import os
import re

source_path = r'c:\Users\chung\Documents\antigravity\serene-turing\generate_game.py'
with open(source_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=== ASSET KEYS ===")
m = re.search(r'assets_keys = \[(.*?)\]', content, re.DOTALL)
if m:
    print(m.group(1))

print("\n=== GODS FOUND ===")
for match in re.finditer(r'(\w+):\s*\{\s*name:\s*[\'"]([^\'"]+)[\'"],\s*title:\s*[\'"]([^\'"]+)[\'"]', content):
    print(f"God: {match.group(1)} -> {match.group(2)} ({match.group(3)})")

print("\n=== ENEMIES / BOSSES ===")
for match in re.finditer(r'(bossTypes|BOSS_NAMES|const ENEMIES|const BOSSES|ENEMY_DEFS)\s*=\s*[\{\[](.*?)[\}\]]', content, re.DOTALL):
    print(match.group(0)[:300])

print("\n=== REWARDS / BOON TYPES ===")
for match in re.finditer(r'(const REWARDS|const CHAMBER_TYPES|REWARD_TYPES)\s*=\s*[\{\[](.*?)[\}\]]', content, re.DOTALL):
    print(match.group(0)[:300])

print("\n=== SCRIPT LENGTH & STATS ===")
print("Total characters:", len(content))
print("Total lines:", content.count('\n'))
