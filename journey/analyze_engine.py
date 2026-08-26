import os
import re

source_path = r'c:\Users\chung\Documents\antigravity\serene-turing\generate_game.py'
with open(source_path, 'r', encoding='utf-8') as f:
    text = f.read()

print("=== HTML MODALS & OVERLAYS ===")
for m in re.finditer(r'<div\s+id=["\']([^"\']+)["\'][^>]*class=["\']([^"\']+)["\']', text):
    div_id = m.group(1)
    if 'modal' in div_id or 'screen' in div_id or 'menu' in div_id or 'hud' in div_id or 'overlay' in div_id or 'altar' in div_id or 'shop' in div_id or 'codex' in div_id or 'pom' in div_id:
        print(f"ID: {div_id:<25} Class: {m.group(2)}")

print("\n=== SOUND ENGINE ===")
sound_match = re.search(r'class SoundEngine\s*\{(.*?)\n  \}', text, re.DOTALL)
if sound_match:
    methods = re.findall(r'(\w+)\s*\([^)]*\)\s*\{', sound_match.group(1))
    print("Sound methods:", methods)

print("\n=== PLAYER CLASS DETAILS ===")
player_match = re.search(r'class Player\s*\{(.*?)\n  \}', text, re.DOTALL)
if player_match:
    methods = re.findall(r'(\w+)\s*\([^)]*\)\s*\{', player_match.group(1))
    print("Player methods:", methods)

print("\n=== ENEMY CLASS & TYPES ===")
enemy_match = re.search(r'class Enemy\s*\{(.*?)\n  \}', text, re.DOTALL)
if enemy_match:
    methods = re.findall(r'(\w+)\s*\([^)]*\)\s*\{', enemy_match.group(1))
    print("Enemy methods:", methods)

print("\n=== CHAMBER PROGRESSION & BOSSES ===")
for m in re.finditer(r'(boss|Boss|chamber|Chamber|biomes|BIOMES|CHAMBERS|STAGES)', text):
    start = max(0, m.start() - 20)
    end = min(len(text), m.end() + 60)
    line = text[start:end].replace('\n', ' ')
    # sample some interesting lines
    if any(k in line.lower() for k in ['biome', 'boss_types', 'spawn_boss', 'chronos', 'hecate', 'cerberus', 'scylla']):
        print(line.strip()[:100])
