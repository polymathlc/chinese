import re

source_path = r'c:\Users\chung\Documents\antigravity\serene-turing\generate_game.py'
with open(source_path, 'r', encoding='utf-8') as f:
    text = f.read()

print("=== DRAW METHODS ===")
for m in re.finditer(r'draw\w*\s*\([^)]*\)\s*\{', text):
    print(m.group(0))

print("\n=== PLAYER DRAW METHOD ===")
p_draw = re.search(r'draw\s*\([^)]*ctx[^)]*\)\s*\{.*?(?=\n  [a-zA-Z]|\Z)', text[text.find('class Player'):], re.DOTALL)
if p_draw:
    print(p_draw.group(0)[:600])

print("\n=== ENEMY DRAW METHOD ===")
e_draw = re.search(r'draw\s*\([^)]*ctx[^)]*\)\s*\{.*?(?=\n  [a-zA-Z]|\Z)', text[text.find('class Enemy'):], re.DOTALL)
if e_draw:
    print(e_draw.group(0)[:600])
