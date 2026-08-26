"""
Journey to the West: Assets Generator
Generates high quality spritesheets, portraits, icons, and textures for Sun Wukong roguelite game.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ASSETS_DIR = "assets_webp"
os.makedirs(ASSETS_DIR, exist_ok=True)

# Helper function to create radial glow
def draw_radial_glow(draw, center, radius, color_rgb, max_alpha=200):
    cx, cy = center
    for r in range(radius, 0, -2):
        factor = 1.0 - (r / radius)
        alpha = int(max_alpha * (factor ** 1.5))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(color_rgb[0], color_rgb[1], color_rgb[2], alpha))

def draw_cloud(draw, x, y, size, color=(255, 255, 255, 180)):
    # Chinese traditional auspicious cloud swirl
    s = size
    draw.ellipse([x - s*0.6, y - s*0.3, x + s*0.2, y + s*0.4], fill=color)
    draw.ellipse([x - s*0.2, y - s*0.5, x + s*0.5, y + s*0.3], fill=color)
    draw.ellipse([x + s*0.1, y - s*0.2, x + s*0.7, y + s*0.4], fill=color)
    draw.arc([x - s*0.4, y, x + s*0.4, y + s*0.6], 0, 180, fill=(255, 215, 0, 220), width=3)

# 1. Generate all_10_gods.webp (1280x512, 5 cols x 2 rows, each 256x256)
def generate_gods_sheet():
    img = Image.new("RGBA", (1280, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    gods_info = [
        # Row 0
        {"name": "Erlang Shen", "title": "God of Retribution", "bg": (20, 30, 60), "glow": (250, 204, 21), "col": 0, "row": 0, "sym": "EYE"},
        {"name": "Guanyin", "title": "Bodhisattva of Mercy", "bg": (20, 50, 40), "glow": (52, 211, 153), "col": 1, "row": 0, "sym": "LOTUS"},
        {"name": "Nezha", "title": "Third Lotus Prince", "bg": (60, 20, 20), "glow": (249, 115, 22), "col": 2, "row": 0, "sym": "RING"},
        {"name": "Taishang Laojun", "title": "Supreme Daoist Lord", "bg": (50, 25, 60), "glow": (236, 72, 153), "col": 3, "row": 0, "sym": "BAGUA"},
        {"name": "Ao Guang", "title": "East Sea Dragon King", "bg": (15, 40, 70), "glow": (56, 189, 248), "col": 4, "row": 0, "sym": "DRAGON"},
        # Row 1
        {"name": "Bull Demon King", "title": "Great Sage Pacifying Heaven", "bg": (45, 20, 10), "glow": (234, 88, 12), "col": 0, "row": 1, "sym": "HORNS"},
        {"name": "Princess Iron Fan", "title": "Mistress of the Gale", "bg": (20, 45, 35), "glow": (74, 222, 128), "col": 1, "row": 1, "sym": "FAN"},
        {"name": "Lady White Bone", "title": "Skeletal Spectre", "bg": (30, 20, 45), "glow": (192, 132, 252), "col": 2, "row": 1, "sym": "SKULL"},
        {"name": "King Yanluo", "title": "Sovereign of Diyu", "bg": (35, 15, 20), "glow": (239, 68, 68), "col": 3, "row": 1, "sym": "BOOK"},
        {"name": "Chang'e & Jade Rabbit", "title": "Moon Goddess", "bg": (25, 30, 65), "glow": (147, 197, 253), "col": 4, "row": 1, "sym": "MOON"},
    ]

    for g in gods_info:
        gx = g["col"] * 256
        gy = g["row"] * 256
        cx = gx + 128
        cy = gy + 128

        # Background circular portal
        draw_radial_glow(draw, (cx, cy), 110, g["glow"], max_alpha=180)
        draw.ellipse([gx + 16, gy + 16, gx + 240, gy + 240], fill=g["bg"] + (230,), outline=(255, 215, 0, 240), width=4)

        # Chinese decorative border ring
        for angle_deg in range(0, 360, 30):
            rad = math.radians(angle_deg)
            px = cx + math.cos(rad) * 105
            py = cy + math.sin(rad) * 105
            draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 220, 100, 255))

        # Aura wisps
        for _ in range(12):
            ang = random.uniform(0, math.pi * 2)
            dist = random.uniform(30, 85)
            draw.ellipse([cx + math.cos(ang)*dist - 6, cy + math.sin(ang)*dist - 6,
                          cx + math.cos(ang)*dist + 6, cy + math.sin(ang)*dist + 6],
                         fill=g["glow"] + (140,))

        # Central Divine Symbol Rendering
        sym = g["sym"]
        if sym == "EYE": # Erlang Shen
            # Third Eye with silver celestial trident
            draw.ellipse([cx - 50, cy - 25, cx + 50, cy + 25], outline=(255, 255, 255, 240), fill=(10, 20, 40, 220), width=3)
            draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(255, 215, 0, 255), outline=(255, 255, 255, 255), width=2)
            draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 60, 0, 255))
            # Spear blade
            draw.polygon([(cx, cy - 80), (cx - 18, cy - 35), (cx + 18, cy - 35)], fill=(220, 230, 255, 255), outline=(255, 215, 0, 255))
            draw.polygon([(cx, cy + 80), (cx - 12, cy + 35), (cx + 12, cy + 35)], fill=(200, 210, 240, 255))
        elif sym == "LOTUS": # Guanyin
            # Radiant Lotus Throne & Jade Vase
            for petal in range(8):
                pang = petal * (math.pi / 4)
                px = cx + math.cos(pang) * 45
                py = cy + math.sin(pang) * 45
                draw.ellipse([px - 22, py - 22, px + 22, py + 22], fill=(240, 253, 244, 200), outline=(52, 211, 153, 240), width=2)
            # Pure vase
            draw.ellipse([cx - 20, cy - 10, cx + 20, cy + 35], fill=(220, 252, 231, 255), outline=(255, 215, 0, 255), width=2)
            draw.rectangle([cx - 10, cy - 30, cx + 10, cy - 10], fill=(220, 252, 231, 255))
            draw.arc([cx - 30, cy - 50, cx + 20, cy - 10], 200, 360, fill=(34, 197, 94, 255), width=4) # Willow branch
        elif sym == "RING": # Nezha
            # Universe Ring & Wind-Fire Wheels
            draw.ellipse([cx - 55, cy - 55, cx + 55, cy + 55], outline=(255, 215, 0, 255), width=8)
            # Fire spikes on wheels
            for f in range(12):
                fang = f * (math.pi / 6)
                fx1 = cx + math.cos(fang) * 55
                fy1 = cy + math.sin(fang) * 55
                fx2 = cx + math.cos(fang) * 78
                fy2 = cy + math.sin(fang) * 78
                draw.line([(fx1, fy1), (fx2, fy2)], fill=(239, 68, 68, 255), width=4)
            # Red Armillary Sash ribbon
            draw.arc([cx - 65, cy - 40, cx + 65, cy + 40], 30, 210, fill=(239, 68, 68, 220), width=6)
            draw.arc([cx - 50, cy - 60, cx + 50, cy + 60], 190, 350, fill=(244, 63, 94, 220), width=6)
        elif sym == "BAGUA": # Taishang Laojun
            # Yin-Yang Bagua Crucible
            draw.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], fill=(255, 255, 255, 240), outline=(255, 215, 0, 255), width=4)
            draw.pieslice([cx - 50, cy - 50, cx + 50, cy + 50], 90, 270, fill=(20, 20, 20, 240))
            draw.ellipse([cx - 25, cy - 50, cx + 25, cy], fill=(255, 255, 255, 255))
            draw.ellipse([cx - 25, cy, cx + 25, cy + 50], fill=(20, 20, 20, 255))
            draw.ellipse([cx - 8, cy - 33, cx + 8, cy - 17], fill=(20, 20, 20, 255))
            draw.ellipse([cx - 8, cy + 17, cx + 8, cy + 33], fill=(255, 255, 255, 255))
            # Samadhi fire flames around
            draw_radial_glow(draw, (cx, cy), 65, (244, 63, 94), max_alpha=120)
        elif sym == "DRAGON": # Ao Guang
            # Imperial Dragon Horns & Ocean Crest
            draw.arc([cx - 60, cy - 30, cx + 60, cy + 50], 0, 180, fill=(56, 189, 248, 255), width=8)
            # Dragon horns
            draw.polygon([(cx - 30, cy - 20), (cx - 60, cy - 70), (cx - 20, cy - 40)], fill=(224, 242, 254, 255), outline=(255, 215, 0, 255))
            draw.polygon([(cx + 30, cy - 20), (cx + 60, cy - 70), (cx + 20, cy - 40)], fill=(224, 242, 254, 255), outline=(255, 215, 0, 255))
            # Dragon pearl
            draw.ellipse([cx - 18, cy - 10, cx + 18, cy + 26], fill=(255, 255, 255, 255), outline=(56, 189, 248, 255), width=4)
        elif sym == "HORNS": # Bull Demon King
            # Massive Minotaur / Ox Horns & Earth Breaker
            draw.arc([cx - 75, cy - 70, cx + 75, cy + 50], 200, 340, fill=(245, 158, 11, 255), width=16)
            draw.polygon([(cx - 75, cy - 40), (cx - 85, cy - 75), (cx - 50, cy - 55)], fill=(255, 255, 255, 255), outline=(245, 158, 11, 255))
            draw.polygon([(cx + 75, cy - 40), (cx + 85, cy - 75), (cx + 50, cy - 55)], fill=(255, 255, 255, 255), outline=(245, 158, 11, 255))
            # War mask
            draw.polygon([(cx, cy + 55), (cx - 40, cy - 15), (cx + 40, cy - 15)], fill=(60, 20, 10, 255), outline=(234, 88, 12, 255), width=3)
        elif sym == "FAN": # Princess Iron Fan
            # Celestial Plantain Fan
            draw.pieslice([cx - 65, cy - 80, cx + 65, cy + 50], 210, 330, fill=(34, 197, 94, 220), outline=(255, 215, 0, 255), width=4)
            draw.line([(cx, cy + 60), (cx, cy - 40)], fill=(120, 53, 15, 255), width=6)
            for fa in range(220, 330, 20):
                farad = math.radians(fa)
                draw.line([(cx, cy - 20), (cx + math.cos(farad)*60, cy - 20 + math.sin(farad)*60)], fill=(255, 255, 255, 180), width=2)
        elif sym == "SKULL": # Lady White Bone
            # Skeletal Specter & Spirit Flames
            draw.ellipse([cx - 35, cy - 45, cx + 35, cy + 15], fill=(243, 244, 246, 240), outline=(192, 132, 252, 255), width=3)
            draw.rectangle([cx - 20, cy + 5, cx + 20, cy + 35], fill=(243, 244, 246, 240), outline=(192, 132, 252, 255), width=2)
            draw.ellipse([cx - 22, cy - 25, cx - 8, cy - 5], fill=(88, 28, 135, 255))
            draw.ellipse([cx + 8, cy - 25, cx + 22, cy - 5], fill=(88, 28, 135, 255))
            draw.polygon([(cx, cy + 5), (cx - 6, cy - 5), (cx + 6, cy - 5)], fill=(88, 28, 135, 255))
        elif sym == "BOOK": # King Yanluo
            # Book of Life and Death & Ghost Sovereign Seal
            draw.rectangle([cx - 45, cy - 55, cx + 45, cy + 45], fill=(153, 27, 27, 240), outline=(255, 215, 0, 255), width=4)
            draw.line([(cx, cy - 55), (cx, cy + 45)], fill=(255, 215, 0, 255), width=4)
            # Runic characters
            draw.rectangle([cx - 35, cy - 40, cx - 10, cy - 30], fill=(254, 240, 138, 255))
            draw.rectangle([cx - 35, cy - 20, cx - 10, cy - 10], fill=(254, 240, 138, 255))
            draw.rectangle([cx + 10, cy - 40, cx + 35, cy - 30], fill=(254, 240, 138, 255))
            draw.rectangle([cx + 10, cy - 20, cx + 35, cy - 10], fill=(254, 240, 138, 255))
        elif sym == "MOON": # Chang'e & Jade Rabbit
            # Radiant Full Moon & Celestial Rabbit silhouette
            draw.ellipse([cx - 55, cy - 55, cx + 55, cy + 55], fill=(241, 245, 249, 250), outline=(255, 255, 255, 255), width=4)
            draw.ellipse([cx - 65, cy - 40, cx + 35, cy + 60], fill=(203, 213, 225, 200)) # Moon crater shadow
            # Lunar halo
            draw_radial_glow(draw, (cx, cy), 70, (186, 230, 253), max_alpha=100)

        # Bottom banner with Chinese deity title
        draw.rectangle([gx + 20, gy + 215, gx + 236, gy + 245], fill=(10, 8, 18, 230), outline=(255, 215, 0, 200), width=1)

    img.save(os.path.join(ASSETS_DIR, "all_10_gods.webp"), "WEBP", quality=92)
    print("Generated all_10_gods.webp")

# 2. Generate reward_icons.webp (512x512, 2x2 grid of 256x256 icons)
def generate_reward_icons():
    img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # (0,0): Heavenly Peach of Immortality (蟠桃 - Replaces Pom of Power)
    cx, cy = 128, 128
    draw_radial_glow(draw, (cx, cy), 110, (244, 63, 94), max_alpha=180)
    draw.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], fill=(30, 10, 20, 220), outline=(255, 215, 0, 255), width=4)
    # Peach Leaves (Jade Green)
    draw.pieslice([cx - 80, cy - 70, cx, cy - 10], 180, 270, fill=(34, 197, 94, 255), outline=(20, 83, 45, 255), width=2)
    draw.pieslice([cx, cy - 70, cx + 80, cy - 10], 270, 360, fill=(34, 197, 94, 255), outline=(20, 83, 45, 255), width=2)
    # Peach Fruit (Lush Pink, Golden Tip)
    draw.polygon([(cx, cy - 40), (cx - 60, cy - 10), (cx - 55, cy + 50), (cx, cy + 65), (cx + 55, cy + 50), (cx + 60, cy - 10)],
                 fill=(244, 63, 94, 255), outline=(255, 228, 230, 255))
    draw.ellipse([cx - 45, cy - 25, cx, cy + 45], fill=(251, 113, 133, 255))
    draw.ellipse([cx, cy - 25, cx + 45, cy + 45], fill=(244, 63, 94, 255))
    # Golden tip point
    draw.polygon([(cx, cy - 45), (cx - 10, cy - 30), (cx + 10, cy - 30)], fill=(253, 224, 71, 255))

    # (1,0): Dragon King's Treasury / Earth God Shrine (Shop)
    cx, cy = 384, 128
    draw_radial_glow(draw, (cx, cy), 110, (234, 179, 8), max_alpha=180)
    draw.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], fill=(25, 20, 10, 220), outline=(255, 215, 0, 255), width=4)
    # Dragon Pearl & Gold Ingot (元宝)
    draw.polygon([(cx - 50, cy + 10), (cx + 50, cy + 10), (cx + 65, cy + 45), (cx - 65, cy + 45)],
                 fill=(234, 179, 8, 255), outline=(255, 255, 255, 255), width=2)
    draw.ellipse([cx - 30, cy - 5, cx + 30, cy + 25], fill=(250, 204, 21, 255), outline=(202, 138, 4, 255), width=2)
    # Shimmering Pearl
    draw.ellipse([cx - 25, cy - 50, cx + 25, cy], fill=(255, 255, 255, 255), outline=(56, 189, 248, 255), width=3)
    draw_radial_glow(draw, (cx, cy - 25), 35, (255, 255, 255), max_alpha=160)

    # (0,1): Immortal Ginseng Fruit / Millennial Lingzhi (Heart / Max HP)
    cx, cy = 128, 384
    draw_radial_glow(draw, (cx, cy), 110, (34, 197, 94), max_alpha=180)
    draw.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], fill=(10, 25, 15, 220), outline=(255, 215, 0, 255), width=4)
    # Radiant Ginseng Fruit / Lingzhi Mushroom Cap
    draw.ellipse([cx - 60, cy - 40, cx + 60, cy + 10], fill=(220, 38, 38, 255), outline=(254, 202, 202, 255), width=3)
    draw.arc([cx - 55, cy - 35, cx + 55, cy + 5], 0, 180, fill=(254, 240, 138, 255), width=4)
    draw.rectangle([cx - 15, cy + 5, cx + 15, cy + 50], fill=(254, 243, 199, 255), outline=(217, 119, 6, 255), width=2)
    # Glowing life essence droplets
    draw.ellipse([cx - 4, cy - 20, cx + 4, cy - 10], fill=(255, 255, 255, 255))

    # (1,1): Karma Spirit Ashes / Altar of 72 Transformations (Meta Currency)
    cx, cy = 384, 384
    draw_radial_glow(draw, (cx, cy), 110, (168, 85, 247), max_alpha=180)
    draw.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], fill=(20, 10, 30, 220), outline=(255, 215, 0, 255), width=4)
    # Taoist Incense Tripod / Bagua Alchemy Ash Urn
    draw.ellipse([cx - 50, cy - 15, cx + 50, cy + 35], fill=(71, 85, 105, 255), outline=(255, 215, 0, 255), width=3)
    draw.rectangle([cx - 35, cy + 25, cx - 20, cy + 55], fill=(51, 65, 85, 255)) # Tripod leg 1
    draw.rectangle([cx + 20, cy + 25, cx + 35, cy + 55], fill=(51, 65, 85, 255)) # Tripod leg 2
    # Golden Taoist Talisman floating above
    draw.rectangle([cx - 20, cy - 65, cx + 20, cy - 15], fill=(250, 204, 21, 255), outline=(220, 38, 38, 255), width=2)
    draw.line([(cx, cy - 60), (cx, cy - 20)], fill=(220, 38, 38, 255), width=2)
    draw.line([(cx - 12, cy - 40), (cx + 12, cy - 40)], fill=(220, 38, 38, 255), width=2)

    img.save(os.path.join(ASSETS_DIR, "reward_icons.webp"), "WEBP", quality=92)
    print("Generated reward_icons.webp")

# 3. Generate hero.webp (Sun Wukong Spritesheet: 1024x1024)
def generate_hero_sheet():
    img = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 4x4 Grid of 256x256 cells showing Monkey King in various combat states
    # (Row 0): Idle / Running with Ruyi Bang
    # (Row 1): 3-Hit Staff Combo (Sweep 1, Sweep 2, Overhead Slam)
    # (Row 2): Somersault Cloud Dash & Whirlwind Special
    # (Row 3): Awakened Great Sage (法天象地) Golden Avatar Form

    def draw_wukong_body(cx, cy, scale=1.0, staff_angle=45, staff_extend=1.0, is_awakened=False):
        s = scale
        # Aura
        if is_awakened:
            draw_radial_glow(draw, (cx, cy), int(100*s), (250, 204, 21), max_alpha=220)
            # Golden dragon halo
            draw.ellipse([cx - 70*s, cy - 70*s, cx + 70*s, cy + 70*s], outline=(255, 255, 255, 255), width=int(4*s))
        else:
            draw_radial_glow(draw, (cx, cy), int(60*s), (234, 179, 8), max_alpha=100)

        # Somersault Cloud underneath if dashing or awakened
        draw_cloud(draw, cx, cy + 50*s, 40*s, color=(255, 248, 220, 220))

        # Golden Armor Body
        armor_color = (234, 179, 8, 255) if not is_awakened else (255, 245, 150, 255)
        draw.ellipse([cx - 24*s, cy - 20*s, cx + 24*s, cy + 30*s], fill=armor_color, outline=(180, 83, 9, 255), width=2)
        # Red Silk Cape
        draw.polygon([(cx - 20*s, cy - 10*s), (cx - 38*s, cy + 45*s), (cx, cy + 40*s)], fill=(220, 38, 38, 255))
        draw.polygon([(cx + 20*s, cy - 10*s), (cx + 38*s, cy + 45*s), (cx, cy + 40*s)], fill=(220, 38, 38, 255))
        # Tiger Pelt Kilt
        draw.polygon([(cx - 22*s, cy + 15*s), (cx + 22*s, cy + 15*s), (cx + 18*s, cy + 40*s), (cx - 18*s, cy + 40*s)],
                     fill=(217, 119, 6, 255), outline=(0, 0, 0, 255), width=2)

        # Monkey King Head & Golden Circlet
        head_y = cy - 35*s
        draw.ellipse([cx - 18*s, head_y - 18*s, cx + 18*s, head_y + 18*s], fill=(180, 83, 9, 255)) # Brown fur
        draw.ellipse([cx - 13*s, head_y - 10*s, cx + 13*s, head_y + 12*s], fill=(254, 202, 202, 255)) # Face skin
        # Fiery Golden Eyes (火眼金睛)
        eye_color = (255, 255, 0, 255) if not is_awakened else (255, 60, 0, 255)
        draw.ellipse([cx - 8*s, head_y - 6*s, cx - 2*s, head_y + 2*s], fill=eye_color)
        draw.ellipse([cx + 2*s, head_y - 6*s, cx + 8*s, head_y + 2*s], fill=eye_color)

        # Phoenix Feather Cap (凤翅紫金冠)
        draw.arc([cx - 16*s, head_y - 20*s, cx + 16*s, head_y], 0, 180, fill=(250, 204, 21, 255), width=3) # Golden headband
        # Two tall curved phoenix feathers
        draw.arc([cx - 25*s, head_y - 60*s, cx, head_y - 10*s], 180, 340, fill=(220, 38, 38, 255), width=int(3*s))
        draw.arc([cx, head_y - 60*s, cx + 25*s, head_y - 10*s], 200, 360, fill=(220, 38, 38, 255), width=int(3*s))

        # Ruyi Jingu Bang (如意金箍棒)
        rad = math.radians(staff_angle)
        length = 90 * s * staff_extend
        thickness = 7 * s
        dx = math.cos(rad) * (length / 2)
        dy = math.sin(rad) * (length / 2)
        x1, y1 = cx - dx, cy - dy
        x2, y2 = cx + dx, cy + dy

        # Crimson Central Staff
        draw.line([(x1, y1), (x2, y2)], fill=(185, 28, 28, 255), width=int(thickness))
        # Golden Dragon Hoops at both ends (金箍)
        cap_len = 16 * s
        cx1, cy1 = x1 + math.cos(rad)*cap_len, y1 + math.sin(rad)*cap_len
        cx2, cy2 = x2 - math.cos(rad)*cap_len, y2 - math.sin(rad)*cap_len
        draw.line([(x1, y1), (cx1, cy1)], fill=(250, 204, 21, 255), width=int(thickness + 3*s))
        draw.line([(cx2, cy2), (x2, y2)], fill=(250, 204, 21, 255), width=int(thickness + 3*s))

    # Render grid of hero animations
    for row in range(4):
        for col in range(4):
            cx = col * 256 + 128
            cy = row * 256 + 128
            if row == 0:
                # Idle & Running
                draw_wukong_body(cx, cy, scale=1.0, staff_angle=col * 30 + 30)
            elif row == 1:
                # Staff Attack Combos (Sweep, Thrust, Overhead Slam)
                draw_wukong_body(cx, cy, scale=1.1, staff_angle=-45 + col * 50, staff_extend=1.2 + col * 0.2)
            elif row == 2:
                # Somersault Cloud Dash & Whirlwind
                draw_wukong_body(cx, cy, scale=1.05, staff_angle=col * 90, staff_extend=1.4)
            elif row == 3:
                # Awakened Great Sage Form (法天象地)
                draw_wukong_body(cx, cy, scale=1.35, staff_angle=col * 45 - 20, staff_extend=1.8, is_awakened=True)

    img.save(os.path.join(ASSETS_DIR, "hero.webp"), "WEBP", quality=92)
    print("Generated hero.webp")

# 4. Generate enemy & boss sheets if needed, or tiles
def generate_seamless_floor():
    img = Image.new("RGB", (1024, 1024), (20, 16, 28))
    draw = ImageDraw.Draw(img)
    # Eastern stone court tiles with gold inlay seams
    tile_size = 128
    for y in range(0, 1024, tile_size):
        for x in range(0, 1024, tile_size):
            base_col = random.randint(22, 32)
            draw.rectangle([x, y, x + tile_size, y + tile_size], fill=(base_col, base_col - 4, base_col + 8))
            draw.rectangle([x, y, x + tile_size, y + tile_size], outline=(45, 38, 55), width=2)
            # Gold inlay corner motifs
            draw.line([(x + 8, y + 8), (x + 24, y + 8)], fill=(180, 140, 50), width=1)
            draw.line([(x + 8, y + 8), (x + 8, y + 24)], fill=(180, 140, 50), width=1)

    img.save(os.path.join(ASSETS_DIR, "seamless_floor.webp"), "WEBP", quality=90)
    print("Generated seamless_floor.webp")

# Copy remaining existing assets from serene-turing if they exist and are useful
def copy_supplementary_assets():
    source_dir = r"c:\Users\chung\Documents\antigravity\serene-turing\assets_webp"
    if os.path.exists(source_dir):
        for f in os.listdir(source_dir):
            target = os.path.join(ASSETS_DIR, f)
            if not os.path.exists(target):
                src = os.path.join(source_dir, f)
                with open(src, "rb") as sfp, open(target, "wb") as dfp:
                    dfp.write(sfp.read())
                print(f"Copied {f}")

if __name__ == "__main__":
    generate_gods_sheet()
    generate_reward_icons()
    generate_hero_sheet()
    generate_seamless_floor()
    copy_supplementary_assets()
    print("All Journey to the West visual assets successfully generated!")
