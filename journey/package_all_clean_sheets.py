"""
Package all sprite sheets with 100% projection segmentation.
Guarantees zero bleed, uniform cell placement, zero cut edges, and clean idle frames for all characters.
"""

import os
import hashlib
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

try:
    import cv2
except ImportError:  # A pure-Python fallback below keeps rebuilds deterministic.
    cv2 = None

BRAIN_DIR = r"C:\Users\chung\.gemini\antigravity\brain\36a6f007-4ecb-43da-999f-0581a275fe1c"
OUTPUT_DIR = "assets_webp"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CUTSCENE_SOURCE_DIR = os.path.join("assets_sources", "cutscenes")
CUTSCENE_STORYBOARD_DIR = os.path.join("assets_sources", "cutscene_storyboards")
ERLANG_SOURCE_DIR = os.path.join("assets_sources", "erlang_shen")
ERLANG_FENGSHEN_DIR = os.path.join("assets_sources", "erlang_fengshen")
NG_PLUS_ENEMY_SOURCE_DIR = os.path.join("assets_sources", "ng_plus_enemies")
NG_PLUS_ENEMY_ATLASES = {
    "ng_plus_enemies_1": [
        "ngp_stoneback_macaque_v1_source.png",
        "ngp_wind_scout_v1_source.png",
        "ngp_jade_sword_adept_v1_source.png",
        "ngp_thunder_talisman_v1_source.png",
        "ngp_bronze_guardian_v1_source.png",
    ],
    "ng_plus_enemies_2": [
        "ngp_coral_sentinel_v1_source.png",
        "ngp_pearl_siren_v1_source.png",
        "ngp_abyssal_shell_v1_source.png",
        "ngp_cloud_lancer_v1_source.png",
        "ngp_star_fire_archer_v1_source.png",
    ],
    "ng_plus_enemies_3": [
        "ngp_thunder_drum_colossus_v1_source.png",
        "ngp_nether_chain_warden_v1_source.png",
        "ngp_white_bone_stalker_v1_source.png",
        "ngp_web_cocoon_hexer_v1_source.png",
        "ngp_flame_cloud_spearling_v1_source.png",
    ],
    "ng_plus_enemies_4": [
        "ngp_iron_fan_witch_v1_source.png",
        "ngp_lion_fang_brute_v1_source.png",
        "ngp_shadow_mouse_v1_source.png",
        "ngp_frost_hare_v1_source.png",
        "ngp_dustbreaker_v1_source.png",
    ],
}
CUTSCENE_ART_NAMES = [
    "cutscene_flower_fruit", "cutscene_kunlun", "cutscene_dragon_palace",
    "cutscene_havoc_heaven", "cutscene_five_finger", "cutscene_pilgrims",
    "cutscene_bone_spider", "cutscene_flaming_mountain", "cutscene_mid_trials",
    "cutscene_lion_camel", "cutscene_late_trials", "cutscene_vulture_peak",
]

CUTSCENE_STORYBOARD_SOURCES = {
    "cutscene_flower_fruit": "flower_fruit_storyboard_v1.png",
    "cutscene_kunlun": "kunlun_storyboard_v1.png",
    "cutscene_dragon_palace": "dragon_palace_storyboard_v1.png",
    "cutscene_havoc_heaven": "havoc_heaven_storyboard_v1.png",
    "cutscene_five_finger": "five_finger_storyboard_v1.png",
    "cutscene_pilgrims": "pilgrims_storyboard_v1.png",
    "cutscene_bone_spider": "bone_spider_storyboard_v1.png",
    "cutscene_flaming_mountain": "flaming_mountain_storyboard_v1.png",
    "cutscene_mid_trials": "mid_trials_storyboard_v1.png",
    "cutscene_lion_camel": "lion_camel_storyboard_v1.png",
    "cutscene_late_trials": "late_trials_storyboard_v1.png",
    "cutscene_vulture_peak": "vulture_peak_storyboard_v1.png",
}

ALIGNMENT_ANIMATION_SOURCES = {
    "wukong_good_1": "wukong_good_1_source.png",
    "wukong_good_2": "wukong_good_2_source.png",
    "wukong_good_3": "wukong_good_3_source.png",
    "wukong_evil_1": "wukong_evil_1_source.png",
    "wukong_evil_2": "wukong_evil_2_source.png",
    "wukong_evil_3": "wukong_evil_3_source.png",
}

EVIL_RUYI_COMBO_SOURCES = [
    "evil_ruyi_arc_strip_v1.png",
    "evil_ruyi_ring_strip_v1.png",
    "evil_ruyi_slam_strip_v1.png",
]

COMBO_MOVE_ANIMATION_SOURCES = {
    "wukong_combo_moves_neutral": "wukong_combo_neutral_source.png",
    "wukong_combo_moves_good": "wukong_combo_good_source.png",
    "wukong_combo_moves_evil": "wukong_combo_evil_source.png",
}

RUYI_CONTACT_ATTACK_SOURCE_DIR = os.path.join("assets_sources", "ruyi_contact_attacks")
RUYI_CONTACT_ATTACK_SOURCES = [
    "ruyi_contact_arc_v1_source.png",
    "ruyi_contact_thrust_v1_source.png",
    "ruyi_contact_slam_v1_source.png",
    "ruyi_contact_rising_spin_v1_source.png",
]
RUYI_CONTACT_WEAPON_SOURCES = [
    "ruyi_weapon_arc_v1_source.png",
    "ruyi_weapon_thrust_v1_source.png",
    "ruyi_weapon_slam_v1_source.png",
    "ruyi_weapon_spin_v1_source.png",
]
RUYI_BODYONLY_DIRECTION_SOURCE = "wukong_bodyonly_8dir_contact_v1_source.png"
RUYI_TEMPORAL_SOURCE_DIR = os.path.join("assets_sources", "ruyi_contact_temporal")
RUYI_TEMPORAL_MOVES = ("arc", "thrust", "slam", "spin")
RUYI_TEMPORAL_DIRECTIONS = ("e", "ne", "n", "nw", "w", "sw", "s", "se")
RUYI_GRIP_ANCHOR_MANIFEST = os.path.join(RUYI_TEMPORAL_SOURCE_DIR, "wukong_ruyi_grip_anchors_v1.json")
RUYI_TEMPORAL_SOURCES = [
    f"{move}_{direction}_v1_source.png"
    for move in RUYI_TEMPORAL_MOVES
    for direction in RUYI_TEMPORAL_DIRECTIONS
]

RUYI_WEAPON_QA_REACH = {"arc": 132, "thrust": 154, "slam": 142, "spin": 138}
RUYI_WEAPON_QA_SEGMENTS = {
    "arc": [
        (81,207,295,207),(94,213,279,96),(83,208,272,59),(100,246,292,156),
        (91,208,302,203),(98,178,306,313),(135,220,304,114),(97,207,298,207),
    ],
    "thrust": [
        (83,291,235,290),(199,293,339,296),(198,296,340,286),(41,294,218,289),
        (43,287,329,274),(63,292,338,272),(216,296,339,282),(174,287,331,287),
    ],
    "slam": [
        (158,116,172,329),(129,177,217,311),(159,42,160,250),(128,158,207,328),
        (113,154,216,346),(130,190,219,343),(201,125,139,328),(217,135,132,330),
    ],
    "spin": [
        (303,211,122,214),(302,241,185,97),(272,256,265,52),(173,243,307,94),
        (96,221,306,211),(192,124,302,255),(183,127,189,331),(193,125,92,256),
    ],
}


def package_cutscene_art():
    """Package ImageGen-authored 16:9 story paintings for the dialogue player."""
    packaged = 0
    for name in CUTSCENE_ART_NAMES:
        source_path = os.path.join(CUTSCENE_SOURCE_DIR, f"{name}.png")
        if not os.path.exists(source_path):
            continue
        image = Image.open(source_path).convert("RGB")
        source_ratio = image.width / image.height
        target_ratio = 16 / 9
        if source_ratio > target_ratio:
            crop_width = round(image.height * target_ratio)
            left = (image.width - crop_width) // 2
            image = image.crop((left, 0, left + crop_width, image.height))
        elif source_ratio < target_ratio:
            crop_height = round(image.width / target_ratio)
            top = (image.height - crop_height) // 2
            image = image.crop((0, top, image.width, top + crop_height))
        image.resize((1280, 720), Image.Resampling.LANCZOS).save(
            os.path.join(OUTPUT_DIR, f"{name}.webp"),
            "WEBP", quality=86, method=6,
        )
        packaged += 1
    print(f"Processed {packaged} cinematic story paintings (1280x720)")


def _trim_storyboard_gutter(panel):
    """Remove ImageGen's near-white storyboard gutters without clipping artwork."""
    rgb = np.asarray(panel.convert("RGB"))
    non_gutter = np.min(rgb, axis=2) < 244
    active_rows = np.where(non_gutter.mean(axis=1) > 0.08)[0]
    active_cols = np.where(non_gutter.mean(axis=0) > 0.08)[0]
    if active_rows.size and active_cols.size:
        return panel.crop((
            int(active_cols[0]), int(active_rows[0]),
            int(active_cols[-1] + 1), int(active_rows[-1] + 1),
        ))
    inset = max(12, round(min(panel.size) * 0.015))
    return panel.crop((inset, inset, panel.width - inset, panel.height - inset))


def _cinematic_canvas(panel, size=(1280, 720)):
    """Keep the whole generated panel visible over a soft 16:9 extension."""
    panel = panel.convert("RGB")
    target_w, target_h = size
    cover_scale = max(target_w / panel.width, target_h / panel.height)
    cover_size = (round(panel.width * cover_scale), round(panel.height * cover_scale))
    background = panel.resize(cover_size, Image.Resampling.LANCZOS)
    left = (background.width - target_w) // 2
    top = (background.height - target_h) // 2
    background = background.crop((left, top, left + target_w, top + target_h))
    background = background.filter(ImageFilter.GaussianBlur(radius=24))
    background = Image.blend(background, Image.new("RGB", size, (10, 9, 16)), 0.26)

    contain_scale = min(target_w / panel.width, target_h / panel.height)
    foreground_size = (round(panel.width * contain_scale), round(panel.height * contain_scale))
    foreground = panel.resize(foreground_size, Image.Resampling.LANCZOS)
    x = (target_w - foreground.width) // 2
    y = (target_h - foreground.height) // 2
    background.paste(foreground, (x, y))
    return background


def package_cutscene_storyboard_frames():
    """Split twelve authored storyboards into four unique slide paintings each."""
    packaged = 0
    for asset_base, filename in CUTSCENE_STORYBOARD_SOURCES.items():
        source_path = os.path.join(CUTSCENE_STORYBOARD_DIR, filename)
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Missing required cutscene storyboard: {source_path}")
        storyboard = Image.open(source_path).convert("RGB")
        mid_x, mid_y = storyboard.width // 2, storyboard.height // 2
        quadrants = [
            (0, 0, mid_x, mid_y),
            (mid_x, 0, storyboard.width, mid_y),
            (0, mid_y, mid_x, storyboard.height),
            (mid_x, mid_y, storyboard.width, storyboard.height),
        ]
        frame_hashes = set()
        for slide, box in enumerate(quadrants, start=1):
            panel = _trim_storyboard_gutter(storyboard.crop(box))
            frame = _cinematic_canvas(panel)
            pixel_hash = hashlib.sha256(frame.tobytes()).hexdigest()
            if pixel_hash in frame_hashes:
                raise ValueError(f"Duplicate generated panel in {filename}: slide {slide}")
            frame_hashes.add(pixel_hash)
            frame.save(
                os.path.join(OUTPUT_DIR, f"{asset_base}_slide_{slide}.webp"),
                "WEBP", quality=86, method=6,
            )
            packaged += 1
    print(f"Processed {packaged} unique cinematic slide paintings (1280x720)")

def key_magenta(img):
    img = img.convert("RGBA")
    arr = np.array(img)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    pink_mask = (
        ((r > 135) & (b > 135) & (g < 130)) | 
        ((r > 160) & (b > 130) & ((r.astype(int) - g.astype(int)) > 35) & ((b.astype(int) - g.astype(int)) > 30))
    )
    arr[pink_mask] = [0, 0, 0, 0]
    return Image.fromarray(arr, "RGBA"), pink_mask

def key_black_smooth(img):
    img = img.convert("RGBA")
    arr = np.array(img).astype(float)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    max_c = np.maximum(np.maximum(r, g), b)
    alpha = np.clip((max_c - 14.0) / 40.0, 0.0, 1.0) * 255.0
    arr[:, :, 3] = alpha
    return Image.fromarray(arr.astype(np.uint8), "RGBA")

def key_pure_magenta_smooth(img):
    """Remove ImageGen's flat #ff00ff stage while preserving purple spell art."""
    arr = np.array(img.convert("RGBA")).astype(float)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    border = np.concatenate((arr[:24, :, :3].reshape(-1, 3), arr[-24:, :, :3].reshape(-1, 3), arr[:, :24, :3].reshape(-1, 3), arr[:, -24:, :3].reshape(-1, 3)))
    target = np.median(border, axis=0)
    distance = np.sqrt((r - target[0]) ** 2 + (g - target[1]) ** 2 + (b - target[2]) ** 2)
    magenta_family = (r > 145) & (b > 145) & (g < 145) & (np.abs(r - b) < 95)
    matte_alpha = np.clip((distance - 22.0) / 62.0, 0.0, 1.0) * 255.0
    arr[:, :, 3] = np.minimum(arr[:, :, 3], np.where(magenta_family, matte_alpha, 255.0))
    arr[arr[:, :, 3] < 3] = [0, 0, 0, 0]
    return Image.fromarray(arr.astype(np.uint8), "RGBA")

def key_light_checkerboard(img):
    """Recover transparency when an image generator bakes its checker preview into the PNG."""
    arr = np.array(img.convert("RGBA")).astype(float)
    rgb = arr[:, :, :3]
    min_c = rgb.min(axis=2)
    max_c = rgb.max(axis=2)
    chroma = max_c - min_c
    # The generated checker is neutral white/gray. Orange character pixels have
    # strong chroma, while rocks and dust are darker than the checker.
    color_signal = np.clip(chroma / 38.0, 0.0, 1.0)
    dark_signal = np.clip((235.0 - min_c) / 38.0, 0.0, 1.0)
    alpha = np.maximum(color_signal, dark_signal) * 255.0
    # Checker tiles and their antialiased edges remain neutral even where the
    # preview darkens them. Character armor/dust is strongly orange-brown.
    neutral_bright = (min_c >= 170) & (chroma <= 18)
    alpha[neutral_bright] = 0
    arr[:, :, 3] = np.minimum(arr[:, :, 3], alpha)
    arr[arr[:, :, 3] < 3] = [0, 0, 0, 0]
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def key_checkerboard_cell_flood(img):
    """Remove a baked checker from cell edges without erasing white armor."""
    rgba = np.array(img.convert("RGBA"))
    rgb = rgba[:, :, :3].astype(np.int16)
    min_c = rgb.min(axis=2)
    max_c = rgb.max(axis=2)
    neutral_checker = (min_c >= 164) & ((max_c - min_c) <= 24)
    if cv2 is None:
        return key_light_checkerboard(img)
    count, labels = cv2.connectedComponents(neutral_checker.astype(np.uint8), 8)
    if count <= 1:
        return Image.fromarray(rgba, "RGBA")
    edge_labels = set(labels[0, :]) | set(labels[-1, :]) | set(labels[:, 0]) | set(labels[:, -1])
    edge_labels.discard(0)
    background = np.isin(labels, list(edge_labels))
    rgba[background] = [0, 0, 0, 0]
    if background.any():
        soft_edge = cv2.dilate(background.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1) > 0
        fringe = soft_edge & ~background & (min_c >= 185) & ((max_c - min_c) <= 32)
        rgba[fringe, 3] = np.minimum(rgba[fringe, 3], 70)
    return Image.fromarray(rgba, "RGBA")


def key_erlang_checkerboard_cell(img):
    """Extract blue-white Erlang without retaining ImageGen checker bands.

    His robe contains real near-white regions, so color-keying all neutral pixels
    destroys the character. Instead, dark/chromatic ink supplies a foreground
    silhouette, edge-connected residue is rejected, and enclosed white cloth is
    filled back inside that silhouette.
    """
    rgba = np.array(img.convert("RGBA"))
    rgb = rgba[:, :, :3].astype(np.int16)
    min_c = rgb.min(axis=2)
    max_c = rgb.max(axis=2)
    chroma = max_c - min_c
    # The checker preview contains broad neutral gray compression bands down to
    # roughly 180 luminance. Keep chromatic blue/purple/silver shading and only
    # genuinely dark neutral ink; pale neutral robe interiors are recovered by
    # the surrounding cool-blue texture rather than admitting those bands.
    seed = ((max_c <= 150) | (chroma >= 14)).astype(np.uint8)
    if cv2 is None:
        return key_checkerboard_cell_flood(img)

    seed = cv2.morphologyEx(seed, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=1)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(seed, 8)
    keep = np.zeros(seed.shape, dtype=np.uint8)
    for label in range(1, count):
        x, y, width, height, area = stats[label]
        touches_edge = x == 0 or y == 0 or x + width >= seed.shape[1] or y + height >= seed.shape[0]
        if area >= 6 and not touches_edge:
            keep[labels == label] = 1

    # Do not geometrically fill holes: a horizontal spear or lightning stroke
    # can divide the checker field and make a whole background band appear
    # enclosed. The robe's cool-blue shading is already part of the seed mask.
    keep = cv2.dilate(keep, np.ones((3, 3), np.uint8), iterations=1)

    rgba[keep == 0] = [0, 0, 0, 0]
    rgba[keep > 0, 3] = 255
    return Image.fromarray(rgba.astype(np.uint8), "RGBA")


def key_alignment_checkerboard(img, strict=False):
    """Extract colored/inked sprites from ImageGen's neutral checker preview."""
    rgba = np.array(img.convert("RGBA"))
    rgb = rgba[:, :, :3].astype(np.int16)
    min_c = rgb.min(axis=2)
    max_c = rgb.max(axis=2)
    chroma = max_c - min_c
    # Gold, red, blue, purple, dark ink, and armor texture form the foreground
    # seed. Expand a few pixels to retain white cloth enclosed by those details,
    # while broad gray/white checker tiles remain transparent.
    # Neutral checker tiles range from near-white down through mid-gray after
    # ImageGen antialiasing. Keep chromatic costume/effect pixels and only the
    # genuinely dark ink outline; accepting mid-gray here creates the visible
    # square blocks that the game previously showed around Wukong.
    if strict:
        # Reject the generated near-white checker before dilation, but retain
        # dark neutral armor. The old cleanup deleted those low-chroma armor
        # pixels and produced a hole-filled Evil Wukong body in game.
        checker = (min_c >= 208) & (chroma <= 46)
        seed = (((chroma >= 18) & (min_c < 242)) | (max_c <= 132)) & ~checker
    else:
        seed = (chroma >= 20) | (max_c <= 45)
    if cv2 is not None:
        keep = cv2.dilate(seed.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1) > 0
    else:
        keep = seed
    rgba[~keep] = [0, 0, 0, 0]
    return Image.fromarray(rgba, "RGBA")


def package_alignment_animation_atlases():
    """Pack six ImageGen karma forms into deterministic 3x6 animation grids."""
    source_dir = os.path.join("assets_sources", "alignment_sprites")
    cell_size = 240
    rows, cols, padding = 3, 6, 56
    inner = cell_size - padding * 2
    for asset_name, filename in ALIGNMENT_ANIMATION_SOURCES.items():
        source_path = os.path.join(source_dir, filename)
        if not os.path.exists(source_path):
            print(f"WARNING: missing alignment animation source {source_path}")
            continue
        source = Image.open(source_path).convert("RGBA")
        row_sprites = []
        for row in range(rows):
            sprites = []
            y0 = int(round(row * source.height / rows))
            y1 = int(round((row + 1) * source.height / rows))
            for col in range(cols):
                x0 = int(round(col * source.width / cols))
                x1 = int(round((col + 1) * source.width / cols))
                # ImageGen returned an RGB checker preview rather than real alpha.
                # Remove the neutral checker globally; the authored white armor is
                # edged in blue/gold and remains connected to the colored body.
                frame = key_alignment_checkerboard(
                    source.crop((x0, y0, x1, y1)),
                    strict=asset_name.startswith("wukong_evil_"),
                )
                frame = clean_cell_components(frame, isolate_primary=True, threshold=12)
                alpha = np.array(frame.getchannel("A"))
                ys, xs = np.where(alpha > 4)
                if not len(xs):
                    sprites.append(None)
                    continue
                sprites.append(frame.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)))
            row_sprites.append(sprites)

        atlas = Image.new("RGBA", (cols * cell_size, rows * cell_size), (0, 0, 0, 0))
        for row, sprites in enumerate(row_sprites):
            visible = [sprite for sprite in sprites if sprite is not None]
            if not visible:
                continue
            row_scale = min(
                inner / max(sprite.width for sprite in visible),
                inner / max(sprite.height for sprite in visible),
            )
            for col, sprite in enumerate(sprites):
                if sprite is None:
                    continue
                resized = sprite.resize(
                    (max(1, int(round(sprite.width * row_scale))), max(1, int(round(sprite.height * row_scale)))),
                    Image.Resampling.LANCZOS,
                )
                dx = col * cell_size + (cell_size - resized.width) // 2
                dy = row * cell_size + cell_size - padding - resized.height
                atlas.paste(resized, (dx, dy), resized)
        atlas_arr = np.array(atlas)
        atlas_rgb = atlas_arr[:, :, :3].astype(np.int16)
        atlas_min = atlas_rgb.min(axis=2)
        atlas_chroma = atlas_rgb.max(axis=2) - atlas_min
        atlas_mean = atlas_rgb.mean(axis=2)
        checker_remnant = (atlas_arr[:, :, 3] > 0) & (atlas_mean > 218) & (atlas_chroma < 34)
        atlas_arr[checker_remnant] = [0, 0, 0, 0]
        atlas = Image.fromarray(atlas_arr, "RGBA")
        out_path = os.path.join(OUTPUT_DIR, f"{asset_name}.webp")
        atlas.save(out_path, "WEBP", quality=96, method=6)
        print(f"Packaged {asset_name}.webp: 3x6 authored karma animations with {padding}px gutters")


def package_wukong_combo_move_atlases():
    """Pack three ImageGen-authored 7x7 body-motion atlases with stable pivots.

    Every row keeps one shared crop and scale so airborne kicks remain airborne,
    overhead anticipation remains tall, and contact/recovery do not pump in size.
    The generated Good/Evil references contain a baked checker preview; remove it
    cell-by-cell from the outer flood while preserving enclosed white/dark armor.
    """
    source_dir = os.path.join("assets_sources", "combo_moves")
    rows = cols = 7
    cell_size, padding = 256, 48
    inner = cell_size - padding * 2

    for asset_name, filename in COMBO_MOVE_ANIMATION_SOURCES.items():
        source_path = os.path.join(source_dir, filename)
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Missing generated combo animation source: {source_path}")
        source = Image.open(source_path).convert("RGBA")
        output = Image.new("RGBA", (cols * cell_size, rows * cell_size), (0, 0, 0, 0))

        for row in range(rows):
            frames = []
            for col in range(cols):
                x0 = int(round(col * source.width / cols))
                x1 = int(round((col + 1) * source.width / cols))
                y0 = int(round(row * source.height / rows))
                y1 = int(round((row + 1) * source.height / rows))
                frame = source.crop((x0, y0, x1, y1))
                if asset_name.endswith("neutral"):
                    rgba = np.array(frame)
                    rgba[rgba[:, :, 3] < 8] = [0, 0, 0, 0]
                    frame = Image.fromarray(rgba, "RGBA")
                else:
                    frame = key_checkerboard_cell_flood(frame)
                    rgba = np.array(frame)
                    rgb = rgba[:, :, :3].astype(np.int16)
                    min_c = rgb.min(axis=2)
                    chroma = rgb.max(axis=2) - min_c
                    # Remove disconnected mid-gray checker islands trapped by
                    # painted glows. Costume pixels are gold/blue/red/purple
                    # (chromatic) or genuinely dark ink, so this does not erase
                    # the authored Good white cloth or Evil black armor outline.
                    checker_remnant = (min_c > 80) & (chroma < 28)
                    rgba[checker_remnant] = [0, 0, 0, 0]
                    frame = Image.fromarray(rgba, "RGBA")
                frame = clean_cell_components(frame, isolate_primary=False, threshold=8)
                frames.append(frame)

            bounds = []
            for frame in frames:
                alpha = np.array(frame.getchannel("A"))
                ys, xs = np.where(alpha > 8)
                if len(xs):
                    bounds.append((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
            if len(bounds) != cols:
                raise ValueError(f"{asset_name} row {row} has {len(bounds)}/{cols} nonempty authored frames")

            # A common row crop preserves authored movement within each source
            # cell instead of pinning every airborne frame back to the ground.
            union = (
                min(box[0] for box in bounds), min(box[1] for box in bounds),
                max(box[2] for box in bounds), max(box[3] for box in bounds),
            )
            union_w = union[2] - union[0]
            union_h = union[3] - union[1]
            row_scale = min(inner / union_w, inner / union_h)
            target_size = (max(1, round(union_w * row_scale)), max(1, round(union_h * row_scale)))

            for col, frame in enumerate(frames):
                shared_crop = frame.crop(union).resize(target_size, Image.Resampling.LANCZOS)
                dx = col * cell_size + (cell_size - target_size[0]) // 2
                dy = row * cell_size + cell_size - padding - target_size[1]
                output.paste(shared_crop, (dx, dy), shared_crop)

        output.save(os.path.join(OUTPUT_DIR, f"{asset_name}.webp"), "WEBP", quality=96, method=6)
        print(f"Packaged {asset_name}.webp: 7 distinct 7-frame combo moves with {padding}px gutters")


def _prepare_generated_contact_strip(source):
    """Return true-alpha contact art without admitting a baked checker preview."""
    source = source.convert("RGBA")
    alpha_min, alpha_max = source.getchannel("A").getextrema()
    if alpha_min == alpha_max == 255:
        rgba = np.array(source)
        rgb = rgba[:, :, :3].astype(np.int16)
        red, green, blue = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]

        # Image generation can flatten its transparent preview into a single
        # chroma field.  The contact sources deliberately use an otherwise
        # absent pure-green background, so key that family before doing any
        # component cleanup.  A short feather keeps staff/glow silhouettes
        # antialiased without retaining a green rectangular halo.
        green_dominance = green - np.maximum(red, blue)
        looks_like_green_screen = (
            int(np.median(green[:8, :8])) > 180
            and int(np.median(red[:8, :8])) < 90
            and int(np.median(blue[:8, :8])) < 90
        )
        if looks_like_green_screen:
            # Hard-key before downsampling.  The source is much larger than the
            # runtime atlas, so the later LANCZOS resize recreates a clean
            # antialiased edge.  Leaving semi-transparent chroma here causes
            # long green/color bands when a strip is reduced into its cell.
            green_family = (green > 70) & (green_dominance > 8)
            rgba[green_family] = [0, 0, 0, 0]
            source = Image.fromarray(rgba, "RGBA")
        else:
            source = key_alignment_checkerboard(source, strict=False)
    rgba = np.array(source)
    rgba[rgba[:, :, 3] < 5] = [0, 0, 0, 0]
    return Image.fromarray(rgba, "RGBA")


def _pack_fixed_eight_frame_rows(source_names, output_name, cell_size=384, padding=40, source_dir=None):
    """Pack four authored eight-frame strips while retaining their local pivots.

    Each source is already staged in eight equal slots.  Cleaning a slot after
    cutting it severs any low-alpha bridge to a neighboring picture, and a
    shared row crop/scale prevents animation pumping or a changing staff reach.
    """
    cols = 8
    output = Image.new("RGBA", (cols * cell_size, len(source_names) * cell_size), (0, 0, 0, 0))
    source_dir = source_dir or RUYI_CONTACT_ATTACK_SOURCE_DIR
    for row, filename in enumerate(source_names):
        source_path = os.path.join(source_dir, filename)
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Missing generated Ruyi contact source: {source_path}")
        source = _prepare_generated_contact_strip(Image.open(source_path))
        frames = []
        boxes = []
        for col in range(cols):
            x0 = int(round(col * source.width / cols))
            x1 = int(round((col + 1) * source.width / cols))
            frame = clean_cell_components(
                source.crop((x0, 0, x1, source.height)),
                isolate_primary=True,
                threshold=8,
            )
            bbox = frame.getbbox()
            if bbox is None:
                raise ValueError(f"{filename} frame {col} is empty after contact cleanup")
            frames.append(frame)
            boxes.append(bbox)

        # Preserve authored locomotion inside the logical slot.  A union crop
        # maintains the same coordinate system for guard, contact, and recoil.
        union = (
            min(box[0] for box in boxes), min(box[1] for box in boxes),
            max(box[2] for box in boxes), max(box[3] for box in boxes),
        )
        union_w, union_h = union[2] - union[0], union[3] - union[1]
        inner = cell_size - padding * 2
        row_scale = min(inner / union_w, inner / union_h)
        target = (max(1, round(union_w * row_scale)), max(1, round(union_h * row_scale)))
        for col, frame in enumerate(frames):
            packed = frame.crop(union).resize(target, Image.Resampling.LANCZOS)
            dx = col * cell_size + (cell_size - target[0]) // 2
            dy = row * cell_size + cell_size - padding - target[1]
            # Alpha-composite once. Image.paste(..., mask=RGBA) squares the
            # source alpha and can retain stretched RGB in nominally empty
            # pixels, which some canvas/GPU paths expose as colored bands.
            output.alpha_composite(packed, (dx, dy))

    output_path = os.path.join(OUTPUT_DIR, output_name)
    output_rgba = np.array(output)
    output_rgba[output_rgba[:, :, 3] < 4] = [0, 0, 0, 0]
    output = Image.fromarray(output_rgba, "RGBA")
    output.save(output_path, "WEBP", lossless=True, method=6)
    print(f"Processed {output_name}: {len(source_names)} authored rows x 8 frames with stable pivots")
    return output


def _derive_ruyi_karma_palette(source, path):
    """Bake clearly distinct Good/Evil armor colors into temporal bitmap art."""
    rgba = np.array(source.convert("RGBA"))
    rgb = rgba[:, :, :3].astype(np.float32)
    red, green, blue = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    visible = rgba[:, :, 3] > 8
    cape_red = visible & (red > 105) & ((red - green) > 42) & ((red - blue) > 34)
    cloth_blue = visible & (blue > 70) & ((blue - red) > 18) & ((blue - green) > 8)
    if path == "good":
        strength = np.clip((red - green - 35) / 120, 0, 1)
        rgb[:, :, 0] = np.where(cape_red, red * (1 - strength) + 218 * strength, red)
        rgb[:, :, 1] = np.where(cape_red, green * (1 - strength) + 235 * strength, green)
        rgb[:, :, 2] = np.where(cape_red, blue * (1 - strength) + 255 * strength, blue)
        rgb[:, :, 0] = np.where(cloth_blue, np.maximum(red, 90), rgb[:, :, 0])
        rgb[:, :, 1] = np.where(cloth_blue, np.minimum(255, green * 1.18 + 38), rgb[:, :, 1])
        rgb[:, :, 2] = np.where(cloth_blue, np.minimum(255, blue * 1.16 + 48), rgb[:, :, 2])
    elif path == "evil":
        rgb[:, :, 0] = np.where(cape_red, red * .46 + 32, red)
        rgb[:, :, 1] = np.where(cape_red, green * .24, green)
        rgb[:, :, 2] = np.where(cape_red, np.maximum(blue * .72, red * .52), blue)
        rgb[:, :, 0] = np.where(cloth_blue, np.maximum(red * .55, blue * .58), rgb[:, :, 0])
        rgb[:, :, 1] = np.where(cloth_blue, green * .32, rgb[:, :, 1])
        rgb[:, :, 2] = np.where(cloth_blue, np.minimum(255, blue * 1.08 + 24), rgb[:, :, 2])
    rgba[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def _affine_weapon_at_grip(weapon, pivot, source_tip, grip, desired_angle, reach, tile_size=384):
    """Render one measured source staff with its pivot exactly on `grip`."""
    source_angle = math.atan2(source_tip[1] - pivot[1], source_tip[0] - pivot[0])
    source_length = math.hypot(source_tip[0] - pivot[0], source_tip[1] - pivot[1])
    scale = reach / max(1.0, source_length)
    rotation = desired_angle - source_angle
    cosine, sine = math.cos(rotation), math.sin(rotation)
    gx, gy = grip
    # PIL affine coefficients map each output pixel back into the weapon cell.
    coefficients = (
        cosine / scale,
        sine / scale,
        pivot[0] - (cosine * gx + sine * gy) / scale,
        -sine / scale,
        cosine / scale,
        pivot[1] - (-sine * gx + cosine * gy) / scale,
    )
    return weapon.transform(
        (tile_size, tile_size),
        Image.Transform.AFFINE,
        coefficients,
        resample=Image.Resampling.BICUBIC,
    )


def _write_ruyi_combined_anchor_qa(neutral):
    """Prove all 256 measured pivots against body and weapon simultaneously."""
    with open(RUYI_GRIP_ANCHOR_MANIFEST, "r", encoding="utf-8") as anchor_fp:
        manifest = json.load(anchor_fp)
    anchors = manifest["anchors"]
    if any(len(anchors[move]) != 8 or any(len(row) != 8 for row in anchors[move]) for move in RUYI_TEMPORAL_MOVES):
        raise ValueError("Ruyi grip-anchor QA requires exactly 4 x 8 x 8 measurements")
    weapon_atlas = Image.open(os.path.join(OUTPUT_DIR, "ruyi_contact_weapon_paths.webp")).convert("RGBA")
    body_scale = .90
    tile_size = 384
    base_angles = (0, -math.pi/4, -math.pi/2, -3*math.pi/4, math.pi, 3*math.pi/4, math.pi/2, math.pi/4)
    for move_index, move in enumerate(RUYI_TEMPORAL_MOVES):
        qa = Image.new("RGBA", (tile_size * 8, tile_size * 8), (42, 48, 58, 255))
        for direction_index, base_angle in enumerate(base_angles):
            row = move_index * 8 + direction_index
            for frame in range(8):
                tile = Image.new("RGBA", (tile_size, tile_size), (42, 48, 58, 255))
                body = neutral.crop((frame * 192, row * 192, (frame + 1) * 192, (row + 1) * 192))
                body = body.resize((round(192 * body_scale), round(192 * body_scale)), Image.Resampling.LANCZOS)
                body_x = round(tile_size / 2 - 96 * body_scale)
                body_y = round(240 - 160 * body_scale)
                tile.alpha_composite(body, (body_x, body_y))

                source_anchor = anchors[move][direction_index][frame]
                grip = (body_x + source_anchor[0] * body_scale, body_y + source_anchor[1] * body_scale)
                segment = RUYI_WEAPON_QA_SEGMENTS[move][frame]
                pivot, tip = segment[:2], segment[2:]
                weapon = weapon_atlas.crop((frame * 384, move_index * 384, (frame + 1) * 384, (move_index + 1) * 384))
                desired_angle = base_angle - math.pi + frame * math.pi / 4 if move == "spin" else base_angle
                weapon_layer = _affine_weapon_at_grip(
                    weapon, pivot, tip, grip, desired_angle, RUYI_WEAPON_QA_REACH[move], tile_size,
                )
                tile.alpha_composite(weapon_layer)

                marker = ImageDraw.Draw(tile)
                x, y = round(grip[0]), round(grip[1])
                marker.ellipse((x - 7, y - 7, x + 7, y + 7), outline=(0, 255, 136, 255), width=2)
                marker.line((x - 10, y, x + 10, y), fill=(255, 255, 255, 255), width=1)
                marker.line((x, y - 10, x, y + 10), fill=(255, 255, 255, 255), width=1)
                qa.alpha_composite(tile, (frame * tile_size, direction_index * tile_size))
        qa.convert("RGB").save(
            os.path.join(OUTPUT_DIR, f"wukong_ruyi_combined_anchor_qa_{move}.jpg"),
            "JPEG", quality=92, optimize=True,
        )


def package_ruyi_temporal_bodies():
    """Pack 256 body-only generated poses and baked Good/Evil identities."""
    neutral = _pack_fixed_eight_frame_rows(
        RUYI_TEMPORAL_SOURCES,
        "wukong_ruyi_temporal_neutral.webp",
        cell_size=192,
        padding=32,
        source_dir=RUYI_TEMPORAL_SOURCE_DIR,
    )
    for path in ("good", "evil"):
        variant = _derive_ruyi_karma_palette(neutral, path)
        variant.save(
            os.path.join(OUTPUT_DIR, f"wukong_ruyi_temporal_{path}.webp"),
            "WEBP",
            lossless=True,
            method=6,
        )

    # Reviewer-facing contact-pose sheet: four moves by eight directions.
    # Each tile is composited over charcoal, so transparent gaps, cropping and
    # identity drift are visible without relying on an image viewer's matte.
    contact_frames = (4, 4, 5, 5)
    qa = Image.new("RGBA", (8 * 192, 4 * 192), (42, 48, 58, 255))
    for move_index, contact_frame in enumerate(contact_frames):
        for direction_index in range(8):
            row = move_index * 8 + direction_index
            frame = neutral.crop((contact_frame * 192, row * 192, (contact_frame + 1) * 192, (row + 1) * 192))
            qa.alpha_composite(frame, (direction_index * 192, move_index * 192))
    qa.convert("RGB").save(
        os.path.join(OUTPUT_DIR, "wukong_ruyi_temporal_contact_qa.jpg"),
        "JPEG", quality=92, optimize=True,
    )
    _write_ruyi_combined_anchor_qa(neutral)


def package_ruyi_contact_attacks():
    """Publish body-contact and rotatable weapon-path atlases for melee attacks."""
    _pack_fixed_eight_frame_rows(RUYI_CONTACT_ATTACK_SOURCES, "wukong_ruyi_contact_attacks.webp")
    if all(os.path.exists(os.path.join(RUYI_CONTACT_ATTACK_SOURCE_DIR, name)) for name in RUYI_CONTACT_WEAPON_SOURCES):
        _pack_fixed_eight_frame_rows(RUYI_CONTACT_WEAPON_SOURCES, "ruyi_contact_weapon_paths.webp")
    direction_path = os.path.join(RUYI_CONTACT_ATTACK_SOURCE_DIR, RUYI_BODYONLY_DIRECTION_SOURCE)
    if os.path.exists(direction_path):
        _pack_fixed_eight_frame_rows([RUYI_BODYONLY_DIRECTION_SOURCE], "wukong_ruyi_bodyonly_8dir.webp")

    # Explicit all-frame QA proof: 32 body frames over checkerboard followed by
    # 32 weapon-path frames over dark gray. Alpha is composited, so hidden RGB
    # cannot be mistaken for a visible chroma rectangle during review.
    qa_cell = 192
    qa_array = np.zeros((qa_cell * 8, qa_cell * 8, 4), dtype=np.uint8)
    yy, xx = np.indices((qa_cell * 4, qa_cell * 8))
    checker = ((xx // 16 + yy // 16) % 2).astype(bool)
    qa_array[:qa_cell * 4, :, :3] = np.where(checker[:, :, None], 72, 42)
    qa_array[qa_cell * 4:, :, :3] = [42, 48, 58]
    qa_array[:, :, 3] = 255
    qa = Image.fromarray(qa_array, "RGBA")
    for atlas_index, atlas_name in enumerate(("wukong_ruyi_contact_attacks.webp", "ruyi_contact_weapon_paths.webp")):
        atlas = Image.open(os.path.join(OUTPUT_DIR, atlas_name)).convert("RGBA")
        for row in range(4):
            for col in range(8):
                frame = atlas.crop((col * 384, row * 384, (col + 1) * 384, (row + 1) * 384))
                frame = frame.resize((qa_cell, qa_cell), Image.Resampling.LANCZOS)
                qa.alpha_composite(frame, (col * qa_cell, (row + atlas_index * 4) * qa_cell))
    qa.convert("RGB").save(os.path.join(OUTPUT_DIR, "ruyi_contact_all_frames_qa.jpg"), "JPEG", quality=92, optimize=True)


def package_evil_ruyi_combo_fx():
    """Pack three generated seven-frame demonic strike shapes into one atlas."""
    source_dir = os.path.join("assets_sources", "combat_fx")
    cell_size, cols, rows, padding = 256, 7, 3, 60
    output = Image.new("RGBA", (cols * cell_size, rows * cell_size), (0, 0, 0, 0))
    for row, filename in enumerate(EVIL_RUYI_COMBO_SOURCES):
        source_path = os.path.join(source_dir, filename)
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Missing generated Evil Ruyi VFX strip: {source_path}")
        source = Image.open(source_path).convert("RGBA")
        # The peak frames are intentionally wider than their neighbors. Extract
        # complete alpha islands before packing so fixed source slices cannot
        # cut a crescent or admit part of the next picture.
        frames = extract_ordered_alpha_components(source, cols, threshold=10, min_pixels=300)
        if len(frames) != cols:
            raise ValueError(f"Expected {cols} complete Evil Ruyi frames in {filename}; found {len(frames)}")
        shared_scale = min(
            (cell_size - padding * 2) / max(frame.width for frame in frames),
            (cell_size - padding * 2) / max(frame.height for frame in frames),
        )
        for col, frame in enumerate(frames):
            resized = frame.resize(
                (max(1, round(frame.width * shared_scale)), max(1, round(frame.height * shared_scale))),
                Image.Resampling.LANCZOS,
            )
            dx = col * cell_size + (cell_size - resized.width) // 2
            dy = row * cell_size + (cell_size - resized.height) // 2
            output.paste(resized, (dx, dy), resized)
    output.save(os.path.join(OUTPUT_DIR, "evil_ruyi_combo_fx.webp"), "WEBP", quality=96, method=6)
    print("Processed evil_ruyi_combo_fx.webp: authored arc, 360 ring, and slam rows")

def keep_largest_alpha_component(image, threshold=20):
    """Remove neighboring-frame fragments from a generated transparent grid cell."""
    arr = np.array(image.convert("RGBA"))
    mask = arr[:, :, 3] > threshold
    visited = np.zeros(mask.shape, dtype=bool)
    best = []
    height, width = mask.shape
    for yy in range(height):
        for xx in range(width):
            if not mask[yy, xx] or visited[yy, xx]:
                continue
            stack = [(yy, xx)]
            visited[yy, xx] = True
            component = []
            while stack:
                cy, cx = stack.pop()
                component.append((cy, cx))
                for ny in range(max(0, cy - 1), min(height, cy + 2)):
                    for nx in range(max(0, cx - 1), min(width, cx + 2)):
                        if mask[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((ny, nx))
            if len(component) > len(best):
                best = component
    keep = np.zeros(mask.shape, dtype=bool)
    for yy, xx in best:
        keep[yy, xx] = True
    arr[~keep] = [0, 0, 0, 0]
    return Image.fromarray(arr, "RGBA")

def segment_and_build(src_path, cell_size=(128, 128), out_filename="out.webp", skip_left=0, min_w=15, min_h=40, row_threshold=25, col_threshold=15, pad_bottom=8):
    if not os.path.exists(src_path):
        print(f"File not found: {src_path}")
        return
        
    img = Image.open(src_path)
    keyed, mask = key_magenta(img)
    arr = np.array(keyed)
    alpha = arr[:, :, 3] > 0
    if skip_left > 0:
        alpha[:, :skip_left] = False
        
    row_counts = np.sum(alpha, axis=1)
    row_bands = []
    in_band = False
    start_y = 0
    for y, count in enumerate(row_counts):
        if count > row_threshold and not in_band:
            in_band = True
            start_y = y
        elif count <= row_threshold and in_band:
            in_band = False
            if y - start_y >= min_h:
                row_bands.append((start_y, y))
    if in_band and len(row_counts) - start_y >= min_h:
        row_bands.append((start_y, len(row_counts)))
        
    segmented_rows = []
    for (y0, y1) in row_bands:
        band_alpha = alpha[y0:y1, :]
        col_counts = np.sum(band_alpha, axis=0)
        
        sprites_in_row = []
        in_sprite = False
        start_x = 0
        for x, count in enumerate(col_counts):
            if count > col_threshold and not in_sprite:
                in_sprite = True
                start_x = x
            elif count <= col_threshold and in_sprite:
                in_sprite = False
                if x - start_x >= min_w:
                    sx = max(0, start_x - 14)
                    ex = min(keyed.width, x + 14)
                    sy = max(0, y0 - 14)
                    ey = min(keyed.height, y1 + 14)
                    sprite_crop = keyed.crop((sx, sy, ex, ey))
                    bbox = sprite_crop.getbbox()
                    if bbox:
                        tight_box = (sx + bbox[0], sy + bbox[1], sx + bbox[2], sy + bbox[3])
                        sprites_in_row.append(tight_box)
        if in_sprite and len(col_counts) - start_x >= min_w:
            sx = max(0, start_x - 14)
            ex = min(keyed.width, len(col_counts) + 14)
            sy = max(0, y0 - 14)
            ey = min(keyed.height, y1 + 14)
            sprite_crop = keyed.crop((sx, sy, ex, ey))
            bbox = sprite_crop.getbbox()
            if bbox:
                tight_box = (sx + bbox[0], sy + bbox[1], sx + bbox[2], sy + bbox[3])
                sprites_in_row.append(tight_box)
        if len(sprites_in_row) > 0:
            segmented_rows.append(sprites_in_row)
        
    num_rows = len(segmented_rows)
    max_cols = max(len(r) for r in segmented_rows) if num_rows > 0 else 1
    
    out_w = max_cols * cell_size[0]
    out_h = num_rows * cell_size[1]
    
    out_sheet = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    
    for r_idx, row_boxes in enumerate(segmented_rows):
        for c_idx, box in enumerate(row_boxes):
            sprite = keyed.crop(box)
            max_w = cell_size[0] - 12
            max_h = cell_size[1] - 12
            scale = min(max_w / sprite.width, max_h / sprite.height)
            if scale < 1.0:
                nw = max(1, int(sprite.width * scale))
                nh = max(1, int(sprite.height * scale))
                sprite = sprite.resize((nw, nh), Image.Resampling.LANCZOS)
                
            dest_x = c_idx * cell_size[0] + (cell_size[0] - sprite.width) // 2
            dest_y = r_idx * cell_size[1] + (cell_size[1] - sprite.height) - pad_bottom
            out_sheet.paste(sprite, (dest_x, dest_y), sprite)
            
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    out_sheet.save(out_path, "WEBP", quality=95)
    print(f"Processed {out_filename}: {num_rows} rows x {max_cols} cols ({out_w}x{out_h})")
    return out_sheet

def pad_grid_sheet(src_img_path, grid_rows, grid_cols, cell_w, cell_h, out_filename, padding=14, key_mode="black"):
    if not os.path.exists(src_img_path): return
    img = Image.open(src_img_path)
    keyed = key_magenta(img)[0] if key_mode == "magenta" else key_black_smooth(img)
    
    src_cell_w = keyed.width / grid_cols
    src_cell_h = keyed.height / grid_rows
    
    out_w = grid_cols * cell_w
    out_h = grid_rows * cell_h
    out_sheet = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    
    for r in range(grid_rows):
        for c in range(grid_cols):
            x0 = int(c * src_cell_w)
            y0 = int(r * src_cell_h)
            x1 = int((c + 1) * src_cell_w)
            y1 = int((r + 1) * src_cell_h)
            
            cell = keyed.crop((x0, y0, x1, y1))
            bbox = cell.getbbox()
            if bbox:
                cropped = cell.crop(bbox)
                max_w = cell_w - (padding * 2)
                max_h = cell_h - (padding * 2)
                scale = min(max_w / cropped.width, max_h / cropped.height)
                if scale < 1.0 or scale > 1.0:
                    nw = max(1, int(cropped.width * scale))
                    nh = max(1, int(cropped.height * scale))
                    cropped = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
                
                dest_x = c * cell_w + (cell_w - cropped.width) // 2
                dest_y = r * cell_h + (cell_h - cropped.height) // 2
                out_sheet.paste(cropped, (dest_x, dest_y), cropped)

    if key_mode == "magenta":
        # Generated source grids contain dark-purple guides and detached slices from
        # neighboring cells. Remove the guide color and retain the primary connected
        # silhouette in each authored frame.
        out_arr = np.array(out_sheet)
        red, green, blue, alpha = (out_arr[:, :, i] for i in range(4))
        guide = (
            (alpha > 0) & (red < 125) & (blue < 125) & (green < 38)
            & (np.abs(red.astype(int) - blue.astype(int)) < 34)
        )
        out_arr[guide] = [0, 0, 0, 0]

        def largest_component(mask):
            visited = np.zeros(mask.shape, dtype=bool)
            best = []
            height, width = mask.shape
            for yy in range(height):
                for xx in range(width):
                    if not mask[yy, xx] or visited[yy, xx]:
                        continue
                    stack = [(yy, xx)]
                    visited[yy, xx] = True
                    component = []
                    while stack:
                        cy, cx = stack.pop()
                        component.append((cy, cx))
                        for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                            if 0 <= ny < height and 0 <= nx < width and mask[ny, nx] and not visited[ny, nx]:
                                visited[ny, nx] = True
                                stack.append((ny, nx))
                    if len(component) > len(best):
                        best = component
            keep = np.zeros(mask.shape, dtype=bool)
            for yy, xx in best:
                keep[yy, xx] = True
            return keep

        for row in range(grid_rows):
            for col in range(grid_cols):
                y0, y1 = row * cell_h, (row + 1) * cell_h
                x0, x1 = col * cell_w, (col + 1) * cell_w
                cell_alpha = out_arr[y0:y1, x0:x1, 3]
                keep = largest_component(cell_alpha > 24)
                out_arr[y0:y1, x0:x1][~keep] = [0, 0, 0, 0]
        out_sheet = Image.fromarray(out_arr, "RGBA")
                
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    out_sheet.save(out_path, "WEBP", quality=95)
    print(f"Processed padded grid {out_filename}: {grid_rows} rows x {grid_cols} cols ({out_w}x{out_h}) with padding={padding}")

def extract_ordered_alpha_components(image, expected_count, threshold=20, min_pixels=800):
    """Return isolated silhouettes ordered left-to-right, even when their boxes overlap."""
    rgba = np.array(image.convert("RGBA"))
    alpha = rgba[:, :, 3]
    components = []

    if cv2 is not None:
        count, labels, stats, centroids = cv2.connectedComponentsWithStats((alpha > threshold).astype(np.uint8), 8)
        candidates = [
            label for label in range(1, count)
            if int(stats[label, cv2.CC_STAT_AREA]) >= min_pixels
        ]
        if len(candidates) > expected_count:
            candidates = sorted(candidates, key=lambda label: int(stats[label, cv2.CC_STAT_AREA]), reverse=True)[:expected_count]
        candidates.sort(key=lambda label: float(centroids[label][0]))
        if len(candidates) != expected_count:
            return []

        kernel = np.ones((3, 3), np.uint8)
        for label in candidates:
            core = labels == label
            # Restore the antialiased fringe without re-admitting another pose.
            expanded = cv2.dilate(core.astype(np.uint8), kernel, iterations=1) > 0
            mask = expanded & (alpha > 0) & ((labels == 0) | core)
            ys, xs = np.where(mask)
            if not len(xs):
                continue
            isolated = np.zeros_like(rgba)
            isolated[mask] = rgba[mask]
            components.append(Image.fromarray(isolated[min(ys):max(ys)+1, min(xs):max(xs)+1], "RGBA"))
        return components if len(components) == expected_count else []

    # Dependency-free fallback used only when OpenCV is unavailable.
    mask = alpha > threshold
    visited = np.zeros(mask.shape, dtype=bool)
    found = []
    height, width = mask.shape
    for yy in range(height):
        for xx in range(width):
            if not mask[yy, xx] or visited[yy, xx]:
                continue
            stack = [(yy, xx)]
            visited[yy, xx] = True
            points = []
            while stack:
                cy, cx = stack.pop()
                points.append((cy, cx))
                for ny in range(max(0, cy - 1), min(height, cy + 2)):
                    for nx in range(max(0, cx - 1), min(width, cx + 2)):
                        if mask[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((ny, nx))
            if len(points) >= min_pixels:
                found.append(points)
    if len(found) > expected_count:
        found = sorted(found, key=len, reverse=True)[:expected_count]
    found.sort(key=lambda points: sum(point[1] for point in points) / len(points))
    if len(found) != expected_count:
        return []
    for points in found:
        ys = [point[0] for point in points]
        xs = [point[1] for point in points]
        isolated = np.zeros_like(rgba)
        for yy, xx in points:
            isolated[yy, xx] = rgba[yy, xx]
        components.append(Image.fromarray(isolated[min(ys):max(ys)+1, min(xs):max(xs)+1], "RGBA"))
    return components

def pack_component_row(sprites, cell_size, padding, align="bottom"):
    out = Image.new("RGBA", (len(sprites) * cell_size, cell_size), (0, 0, 0, 0))
    for col, sprite in enumerate(sprites):
        bbox = sprite.getbbox()
        if not bbox:
            continue
        sprite = sprite.crop(bbox)
        scale = min((cell_size - padding * 2) / sprite.width, (cell_size - padding * 2) / sprite.height)
        sprite = sprite.resize(
            (max(1, int(sprite.width * scale)), max(1, int(sprite.height * scale))),
            Image.Resampling.LANCZOS,
        )
        dx = col * cell_size + (cell_size - sprite.width) // 2
        dy = (cell_size - sprite.height) // 2 if align == "center" else cell_size - padding - sprite.height
        out.paste(sprite, (dx, dy), sprite)
    return out


def repack_known_source_grid(
    src_path,
    source_rows,
    source_cols,
    dest_cols,
    cell_size,
    out_filename,
    padding,
    align="bottom",
):
    """Pack an authored contact sheet without projection-splitting its poses.

    Several legacy sheets are regular grids even though their poses contain
    detached weapons, projectiles, or wide slash trails. Projection-based
    segmentation interpreted those legitimate pieces as independent frames,
    which produced half bodies and weapon-only cells. Crop the known logical
    cells first, then shrink every complete cell into a generously padded
    destination cell. Rows with fewer authored poses repeat their final stable
    pose so every renderer-accessible slot remains complete.
    """
    if not os.path.exists(src_path):
        print(f"File not found: {src_path}")
        return None

    source = key_pure_magenta_smooth(Image.open(src_path))
    row_counts = [source_cols] * source_rows if isinstance(source_cols, int) else list(source_cols)
    if len(row_counts) != source_rows:
        raise ValueError(f"{out_filename}: expected {source_rows} source row counts, received {len(row_counts)}")

    output = Image.new("RGBA", (dest_cols * cell_size, source_rows * cell_size), (0, 0, 0, 0))
    source_row_h = source.height / source_rows

    for row, count in enumerate(row_counts):
        source_cell_w = source.width / count
        cells = []
        y0 = int(round(row * source_row_h))
        y1 = int(round((row + 1) * source_row_h))
        for col in range(count):
            x0 = int(round(col * source_cell_w))
            x1 = int(round((col + 1) * source_cell_w))
            cell = source.crop((x0, y0, x1, y1))
            # The crop is already the logical authored frame. Keep detached
            # weapons and spell accents that belong to that frame.
            cleaned = clean_cell_components(cell, isolate_primary=False, threshold=12)
            bbox = cleaned.getbbox()
            cells.append(cleaned.crop(bbox) if bbox else None)

        visible = [cell for cell in cells if cell is not None]
        if not visible:
            continue
        row_scale = min(
            (cell_size - padding * 2) / max(cell.width for cell in visible),
            (cell_size - padding * 2) / max(cell.height for cell in visible),
        )

        for dest_col in range(dest_cols):
            source_index = min(dest_col, len(cells) - 1)
            cell = cells[source_index]
            if cell is None:
                # Search the same row for the closest complete authored pose.
                candidates = [idx for idx, candidate in enumerate(cells) if candidate is not None]
                if not candidates:
                    continue
                source_index = min(candidates, key=lambda idx: abs(idx - source_index))
                cell = cells[source_index]
            resized = cell.resize(
                (max(1, int(round(cell.width * row_scale))), max(1, int(round(cell.height * row_scale)))),
                Image.Resampling.LANCZOS,
            )
            dx = dest_col * cell_size + (cell_size - resized.width) // 2
            dy = (
                row * cell_size + cell_size - padding - resized.height
                if align == "bottom"
                else row * cell_size + (cell_size - resized.height) // 2
            )
            output.paste(resized, (dx, dy), resized)

    out_path = os.path.join(OUTPUT_DIR, out_filename)
    output.save(out_path, "WEBP", quality=95, method=6)
    print(
        f"Grid-repacked {out_filename}: {source_rows} rows -> {dest_cols} cols, "
        f"{padding}px four-sided gutters"
    )
    return output

def package_ruyi_boomerang_special():
    """Split the generated throw/catch sheet into actor and spinning-staff atlases."""
    source_path = os.path.join(OUTPUT_DIR, "ruyi_boomerang_special_v1.png")
    if not os.path.exists(source_path):
        return

    source = key_light_checkerboard(Image.open(source_path))
    # This generated source arrived with a baked white/gray transparency preview.
    # Its actors and weapon are deliberately saturated red, gold, and blue, so a
    # stricter neutral-matte pass removes rectangular preview tiles without
    # erasing the dark colored outline or the golden motion arcs.
    rgba = np.array(source.convert("RGBA"))
    rgb = rgba[:, :, :3].astype(int)
    min_c = rgb.min(axis=2)
    chroma = rgb.max(axis=2) - min_c
    neutral_preview = (rgba[:, :, 3] > 0) & (min_c > 10) & (chroma < 20)
    rgba[neutral_preview] = [0, 0, 0, 0]
    # Pixel sprites should have crisp coverage. Low-alpha checker remnants become
    # dark rectangular ghosts over the arena, so discard that preview fringe and
    # remap the real colored silhouette back to a clean antialiased edge.
    alpha = rgba[:, :, 3].astype(float)
    rgba[:, :, 3] = np.clip((alpha - 82.0) / 88.0, 0.0, 1.0) * 255.0
    rgba[rgba[:, :, 3] < 3] = [0, 0, 0, 0]
    source = Image.fromarray(rgba, "RGBA")
    specs = [
        (0, "wukong_ruyi_throw.webp", "bottom", 5000),
        (1, "ruyi_boomerang_spin.webp", "center", 1000),
    ]
    for row, filename, align, min_pixels in specs:
        y0 = int(round(row * source.height / 2))
        y1 = int(round((row + 1) * source.height / 2))
        sprites = extract_ordered_alpha_components(
            source.crop((0, y0, source.width, y1)),
            expected_count=7,
            threshold=20,
            min_pixels=min_pixels,
        )
        if len(sprites) != 7:
            print(f"WARNING: {filename} yielded {len(sprites)}/7 generated frames")
            continue
        atlas = pack_component_row(sprites, cell_size=220, padding=34, align=align)
        atlas.save(os.path.join(OUTPUT_DIR, filename), "WEBP", quality=95, method=6)
        print(f"Processed {filename}: 1 row x 7 frames with 34px four-sided gutters")

def remove_generated_gradient_background(cell):
    """Recover a transparent character from ImageGen's smooth illustrated backdrop.

    The Four Heavenly Kings source is an exact grid, but ImageGen returned a
    low-frequency colored gradient.  A quadratic background model built only
    from the clear cell perimeter separates that matte without color-keying
    away teal robes, red fire, white hair, or blue spell effects.
    """
    rgb = np.array(cell.convert("RGB"), dtype=np.float32)
    height, width = rgb.shape[:2]
    yy, xx = np.mgrid[0:height, 0:width]
    xn = (xx.astype(np.float32) / max(1, width - 1)) * 2.0 - 1.0
    yn = (yy.astype(np.float32) / max(1, height - 1)) * 2.0 - 1.0
    basis = np.stack((
        np.ones_like(xn), xn, yn, xn * xn, xn * yn, yn * yn,
        xn * xn * xn, yn * yn * yn,
    ), axis=-1)
    rim_x = max(18, int(round(width * 0.14)))
    rim_y = max(16, int(round(height * 0.14)))
    sample_mask = (xx < rim_x) | (xx >= width - rim_x) | (yy < rim_y) | (yy >= height - rim_y)
    sample_basis = basis[sample_mask]
    predicted = np.empty_like(rgb)
    for channel in range(3):
        coefficients, *_ = np.linalg.lstsq(sample_basis, rgb[:, :, channel][sample_mask], rcond=None)
        predicted[:, :, channel] = np.tensordot(basis, coefficients, axes=([2], [0]))

    color_distance = np.linalg.norm(rgb - predicted, axis=2)
    if cv2 is not None:
        # Fine-grained saliency distinguishes an illustrated silhouette from the
        # smooth matte even when robe and background share a hue.  Local detail
        # rescues dark armor interiors and thin weapons; closing fills the body.
        saliency_detector = cv2.saliency.StaticSaliencyFineGrained_create()
        ok, saliency = saliency_detector.computeSaliency(rgb.astype(np.uint8))
        if not ok:
            saliency = np.zeros((height, width), dtype=np.float32)
        gray = cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_RGB2GRAY)
        grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        detail = cv2.magnitude(grad_x, grad_y)
        # Flood the low-gradient matte inward from every edge. Unlike a global
        # color threshold, this follows the changing backdrop while stopping at
        # the crisp silhouette boundary.
        lab = cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
        edge_strength = np.zeros((height, width), dtype=np.float32)
        for channel in range(3):
            channel_x = cv2.Sobel(lab[:, :, channel], cv2.CV_32F, 1, 0, ksize=3)
            channel_y = cv2.Sobel(lab[:, :, channel], cv2.CV_32F, 0, 1, ksize=3)
            edge_strength = np.maximum(edge_strength, cv2.magnitude(channel_x, channel_y))
        barrier = (edge_strength > 13.0).astype(np.uint8)
        barrier = cv2.morphologyEx(barrier, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=1)
        barrier = cv2.dilate(barrier, np.ones((3, 3), np.uint8), iterations=1)
        passable = (barrier == 0).astype(np.uint8)
        _, flood_labels = cv2.connectedComponents(passable, connectivity=8)
        border_labels = np.unique(np.concatenate((flood_labels[0, :], flood_labels[-1, :], flood_labels[:, 0], flood_labels[:, -1])))
        flooded_background = np.isin(flood_labels, border_labels)

        candidate = ((saliency > 0.075) | (edge_strength > 13.0) | ((color_distance > 30.0) & (detail > 5.0))).astype(np.uint8)
        candidate = cv2.morphologyEx(candidate, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8), iterations=2)
        candidate = cv2.dilate(candidate, np.ones((5, 5), np.uint8), iterations=1)
        mask = np.full((height, width), cv2.GC_PR_BGD, dtype=np.uint8)
        mask[candidate > 0] = cv2.GC_PR_FGD
        mask[flooded_background] = cv2.GC_BGD
        mask[(candidate > 0) & ((saliency > 0.35) | (detail > 55.0))] = cv2.GC_FGD
        seam = max(4, int(round(min(width, height) * 0.025)))
        mask[:seam, :] = cv2.GC_BGD
        mask[-seam:, :] = cv2.GC_BGD
        mask[:, :seam] = cv2.GC_BGD
        mask[:, -seam:] = cv2.GC_BGD
        background_model = np.zeros((1, 65), np.float64)
        foreground_model = np.zeros((1, 65), np.float64)
        try:
            cv2.grabCut(rgb.astype(np.uint8), mask, None, background_model, foreground_model, 4, cv2.GC_INIT_WITH_MASK)
            foreground = ((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD)).astype(np.uint8)
        except cv2.error:
            foreground = candidate
        foreground = cv2.morphologyEx(foreground, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=2)
        # Crisp pixel-art interiors with a two-pixel antialiased edge.
        soft = cv2.GaussianBlur(foreground.astype(np.float32) * 255.0, (0, 0), 0.85)
        alpha = np.clip(soft, 0, 255).astype(np.uint8)
    else:
        alpha = np.clip((color_distance - 14.0) / 24.0, 0.0, 1.0) * 255.0
        alpha = alpha.astype(np.uint8)

    rgba = np.dstack((rgb.astype(np.uint8), alpha))
    rgba[rgba[:, :, 3] < 3] = [0, 0, 0, 0]
    return Image.fromarray(rgba, "RGBA")

def package_four_heavenly_kings():
    """Publish four separate 7-state bosses with generous transparent gutters."""
    transparent_source = os.path.join(OUTPUT_DIR, "four_heavenly_kings_v2.png")
    source_path = transparent_source if os.path.exists(transparent_source) else os.path.join(OUTPUT_DIR, "four_heavenly_kings_v1.png")
    if not os.path.exists(source_path):
        return
    source_image = Image.open(source_path)
    has_authored_alpha = source_path == transparent_source and source_image.mode == "RGBA"
    source = source_image.convert("RGBA" if has_authored_alpha else "RGB")
    rows, cols, cell_size, padding = 4, 7, 200, 30
    output = Image.new("RGBA", (cols * cell_size, rows * cell_size), (0, 0, 0, 0))
    if has_authored_alpha:
        source_rgba = np.array(source.convert("RGBA"))
        authored_alpha = source_rgba[:, :, 3].astype(np.float32)
        authored_alpha = np.clip((authored_alpha - 42.0) / 150.0, 0.0, 1.0) * 255.0
        max_rgb = source_rgba[:, :, :3].max(axis=2).astype(np.float32)
        black_matte_alpha = np.clip((max_rgb - 14.0) / 42.0, 0.0, 1.0) * 255.0
        source_rgba[:, :, 3] = np.minimum(authored_alpha, black_matte_alpha).astype(np.uint8)
        source_rgba[source_rgba[:, :, 3] < 3] = [0, 0, 0, 0]
        keyed_source = Image.fromarray(source_rgba, "RGBA")
        complete_rows = []
        for row in range(rows):
            y0 = int(round(row * keyed_source.height / rows))
            y1 = int(round((row + 1) * keyed_source.height / rows))
            sprites = extract_ordered_alpha_components(
                keyed_source.crop((0, y0, keyed_source.width, y1)),
                expected_count=cols,
                threshold=54,
                min_pixels=500,
            )
            if len(sprites) != cols:
                complete_rows = []
                print(f"WARNING: Four Kings row {row} yielded {len(sprites)}/{cols} complete poses; using fixed-cell fallback")
                break
            complete_rows.append(pack_component_row(sprites, cell_size, padding, align="bottom"))
        if len(complete_rows) == rows:
            for row, packed_row in enumerate(complete_rows):
                output.paste(packed_row, (0, row * cell_size), packed_row)
            output_path = os.path.join(OUTPUT_DIR, "four_heavenly_kings.webp")
            output.save(output_path, "WEBP", quality=95, method=6)
            print("Processed four_heavenly_kings.webp: extracted 28 complete isolated poses with 30px gutters")
            return
    for row in range(rows):
        for col in range(cols):
            x0 = int(round(col * source.width / cols))
            x1 = int(round((col + 1) * source.width / cols))
            y0 = int(round(row * source.height / rows))
            y1 = int(round((row + 1) * source.height / rows))
            pose = source.crop((x0, y0, x1, y1))
            if has_authored_alpha:
                # ImageGen supplied real alpha, but also a very faint whole-cell
                # preview haze. Remove that low-opacity matte before component
                # isolation so no rectangular shadow can appear over the arena.
                pose_rgba = np.array(pose.convert("RGBA"))
                authored_alpha = pose_rgba[:, :, 3].astype(np.float32)
                authored_alpha = np.clip((authored_alpha - 42.0) / 150.0, 0.0, 1.0) * 255.0
                max_rgb = pose_rgba[:, :, :3].max(axis=2).astype(np.float32)
                black_matte_alpha = np.clip((max_rgb - 14.0) / 42.0, 0.0, 1.0) * 255.0
                pose_rgba[:, :, 3] = np.minimum(authored_alpha, black_matte_alpha).astype(np.uint8)
                pose_rgba[pose_rgba[:, :, 3] < 3] = [0, 0, 0, 0]
                pose = Image.fromarray(pose_rgba, "RGBA")
                pose = clean_cell_components(pose, isolate_primary=True, threshold=18)
            else:
                pose = remove_generated_gradient_background(pose)
            bbox = pose.getbbox()
            if not bbox:
                print(f"WARNING: empty Four Kings frame row={row} col={col}")
                continue
            pose = pose.crop(bbox)
            scale = min((cell_size - padding * 2) / pose.width, (cell_size - padding * 2) / pose.height)
            pose = pose.resize(
                (max(1, int(round(pose.width * scale))), max(1, int(round(pose.height * scale)))),
                Image.Resampling.LANCZOS,
            )
            dx = col * cell_size + (cell_size - pose.width) // 2
            dy = row * cell_size + cell_size - padding - pose.height
            output.paste(pose, (dx, dy), pose)
    output_path = os.path.join(OUTPUT_DIR, "four_heavenly_kings.webp")
    output.save(output_path, "WEBP", quality=95, method=6)
    print("Processed four_heavenly_kings.webp: 4 distinct bosses x 7 animated states with 30px gutters")

def package_boss_skill_fx():
    """Convert the generated black-stage projectile/AOE/mobility sheet to alpha."""
    source_path = os.path.join(OUTPUT_DIR, "boss_skill_fx_v1.png")
    if not os.path.exists(source_path):
        return
    source = key_black_smooth(Image.open(source_path))
    rows, cols, cell_size, padding = 3, 7, 256, 40
    output = Image.new("RGBA", (cols * cell_size, rows * cell_size), (0, 0, 0, 0))
    for row in range(rows):
        for col in range(cols):
            x0 = int(round(col * source.width / cols))
            x1 = int(round((col + 1) * source.width / cols))
            y0 = int(round(row * source.height / rows))
            y1 = int(round((row + 1) * source.height / rows))
            effect = source.crop((x0, y0, x1, y1))
            bbox = effect.getbbox()
            if not bbox:
                continue
            effect = effect.crop(bbox)
            scale = min((cell_size - padding * 2) / effect.width, (cell_size - padding * 2) / effect.height)
            effect = effect.resize(
                (max(1, int(round(effect.width * scale))), max(1, int(round(effect.height * scale)))),
                Image.Resampling.LANCZOS,
            )
            dx = col * cell_size + (cell_size - effect.width) // 2
            dy = row * cell_size + (cell_size - effect.height) // 2
            output.paste(effect, (dx, dy), effect)
    output.save(os.path.join(OUTPUT_DIR, "boss_skill_fx.webp"), "WEBP", quality=94, method=6)
    print("Processed boss_skill_fx.webp: projectile, large-AOE, and mobility animation rows")

def repack_alpha_strip(src_img_path, grid_cols, cell_size, out_filename, padding=10):
    """Normalize an overlapping alpha strip by extracting complete silhouettes first."""
    if not os.path.exists(src_img_path):
        return
    img = Image.open(src_img_path).convert("RGBA")
    sprites = extract_ordered_alpha_components(img, grid_cols)
    if len(sprites) != grid_cols:
        print(f"WARNING: component extraction failed for {out_filename}; refusing to publish chopped frames")
        return
    out = pack_component_row(sprites, cell_size, padding)
    out.save(os.path.join(OUTPUT_DIR, out_filename), "WEBP", quality=95, method=6)
    print(f"Processed isolated generated strip {out_filename}: 1 row x {grid_cols} complete silhouettes")
    return out


def package_xiaotianquan_empowered_slam():
    """Publish the seven-frame ImageGen hound launch/slam with real alpha.

    The generated source contains a very light neutral checkerboard instead of
    authored transparency.  Color distance from that neutral matte preserves
    the blue-violet lightning and gold markings, while projection gaps recover
    the deliberately uneven spacing between complete poses without slicing a
    tail, shockwave, or dive trail at a mathematical grid boundary.
    """
    source_path = os.path.join(ERLANG_FENGSHEN_DIR, "xiaotianquan_empowered_slam_v1_source.png")
    if not os.path.exists(source_path):
        return None

    source_rgb = np.array(Image.open(source_path).convert("RGB"), dtype=np.float32)
    maximum = source_rgb.max(axis=2)
    minimum = source_rgb.min(axis=2)
    chroma = maximum - minimum
    luminance = source_rgb.mean(axis=2)
    # The matte is 246-255 neutral gray.  Either meaningful darkness or color
    # saturation is enough to retain pale lightning and antialiased gold edges.
    strength = np.maximum((247.0 - luminance) / 72.0, (chroma - 3.0) / 32.0)
    coverage = np.clip((strength - 0.025) / 0.25, 0.0, 1.0)
    coverage = coverage * coverage * (3.0 - 2.0 * coverage)
    alpha = np.clip(coverage * 255.0, 0, 255).astype(np.uint8)
    rgba = np.dstack((source_rgb.astype(np.uint8), alpha))
    rgba[alpha < 3] = [0, 0, 0, 0]
    keyed = Image.fromarray(rgba, "RGBA")

    projection = (alpha > 8).sum(axis=0)
    active = np.where(projection > 0)[0]
    bands = []
    if active.size:
        start = previous = int(active[0])
        for coordinate in active[1:]:
            coordinate = int(coordinate)
            if coordinate - previous > 6:
                bands.append((start, previous + 1))
                start = coordinate
            previous = coordinate
        bands.append((start, previous + 1))
    if len(bands) != 7:
        raise ValueError(f"Xiaotianquan empowered slam expected 7 isolated poses; found {len(bands)}")

    sprites = []
    for left, right in bands:
        pose = keyed.crop((max(0, left - 3), 0, min(keyed.width, right + 3), keyed.height))
        bbox = pose.getbbox()
        if not bbox:
            raise ValueError("Xiaotianquan empowered slam contains an empty pose")
        sprites.append(pose.crop(bbox))

    cell_size = 240
    padding = 42
    shared_scale = min(
        (cell_size - padding * 2) / max(sprite.width for sprite in sprites),
        (cell_size - padding * 2) / max(sprite.height for sprite in sprites),
    )
    output = Image.new("RGBA", (cell_size * 7, cell_size), (0, 0, 0, 0))
    for column, sprite in enumerate(sprites):
        resized = sprite.resize(
            (max(1, round(sprite.width * shared_scale)), max(1, round(sprite.height * shared_scale))),
            Image.Resampling.LANCZOS,
        )
        x = column * cell_size + (cell_size - resized.width) // 2
        y = cell_size - padding - resized.height
        output.paste(resized, (x, y), resized)

    output_path = os.path.join(OUTPUT_DIR, "xiaotianquan_empowered_slam.webp")
    output.save(output_path, "WEBP", lossless=True, method=6)
    print("Processed xiaotianquan_empowered_slam.webp: 7 isolated power, leap, dive, slam, and recovery poses")
    return output

def repack_component_grid(src_img_path, grid_rows, grid_cols, cell_size, out_filename, padding=6):
    """Normalize rows whose generated silhouettes overlap neighboring logical cells."""
    if not os.path.exists(src_img_path):
        return
    source = Image.open(src_img_path).convert("RGBA")
    out = source.resize((grid_cols * cell_size, grid_rows * cell_size), Image.Resampling.LANCZOS)
    isolated_rows = 0
    for row in range(grid_rows):
        y0 = int(round(row * source.height / grid_rows))
        y1 = int(round((row + 1) * source.height / grid_rows))
        sprites = extract_ordered_alpha_components(source.crop((0, y0, source.width, y1)), grid_cols, threshold=24, min_pixels=8000)
        if len(sprites) != grid_cols:
            continue
        normalized = pack_component_row(sprites, cell_size, padding)
        out.paste(Image.new("RGBA", normalized.size, (0, 0, 0, 0)), (0, row * cell_size))
        out.paste(normalized, (0, row * cell_size), normalized)
        isolated_rows += 1
    out.save(os.path.join(OUTPUT_DIR, out_filename), "WEBP", quality=94, method=6)
    print(f"Processed {out_filename}: isolated {isolated_rows}/{grid_rows} rows into safe {cell_size}px cells")
    return out

def repack_direct_alpha_grid(src_img_path, grid_rows, grid_cols, cell_size, out_filename, padding=32):
    """Pack an already-spaced transparent ImageGen board without merging its VFX."""
    if not os.path.exists(src_img_path):
        return
    source = Image.open(src_img_path).convert("RGBA")
    output = Image.new("RGBA", (grid_cols * cell_size, grid_rows * cell_size), (0, 0, 0, 0))
    for row in range(grid_rows):
        cells = []
        for col in range(grid_cols):
            x0 = int(round(col * source.width / grid_cols))
            x1 = int(round((col + 1) * source.width / grid_cols))
            y0 = int(round(row * source.height / grid_rows))
            y1 = int(round((row + 1) * source.height / grid_rows))
            cell = source.crop((x0, y0, x1, y1))
            bbox = cell.getbbox()
            cells.append(cell.crop(bbox) if bbox else None)

        visible = [cell for cell in cells if cell is not None]
        if not visible:
            continue
        # A shared scale per row prevents the authored effect from pumping in size.
        scale = min(
            (cell_size - padding * 2) / max(cell.width for cell in visible),
            (cell_size - padding * 2) / max(cell.height for cell in visible),
        )
        for col, cell in enumerate(cells):
            if cell is None:
                continue
            resized = cell.resize(
                (max(1, int(round(cell.width * scale))), max(1, int(round(cell.height * scale)))),
                Image.Resampling.LANCZOS,
            )
            dx = col * cell_size + (cell_size - resized.width) // 2
            dy = row * cell_size + (cell_size - resized.height) // 2
            output.paste(resized, (dx, dy), resized)

    output.save(os.path.join(OUTPUT_DIR, out_filename), "WEBP", quality=95, method=6)
    print(f"Processed {out_filename}: {grid_rows}x{grid_cols} isolated VFX cells with {padding}px gutters")
    return output

def package_erlang_player_actions():
    """Publish the definitive blue-white Erlang board as isolated 7x5 clips.

    The v2 ImageGen source deliberately uses bright white robes, so global neutral
    color keying would erase his costume. Each logical cell instead flood-removes
    only checker pixels connected to that cell's outer edge. A shared row scale
    and 56px gutter keep the three-pointed spear and every divine effect isolated.
    """
    source_path = os.path.join(ERLANG_SOURCE_DIR, "erlang_player_actions_v2_source.png")
    if not os.path.exists(source_path):
        print(f"WARNING: missing Erlang v2 animation source {source_path}")
        return None
    source = Image.open(source_path).convert("RGBA")

    rows, cols, cell_size, padding = 5, 7, 240, 56
    output = Image.new("RGBA", (cols * cell_size, rows * cell_size), (0, 0, 0, 0))
    for row in range(rows):
        sprites = []
        for col in range(cols):
            # ImageGen left a half-cell safety margin around the entire board:
            # seven poses occupy the middle seven slots of an eight-slot width,
            # and five rows occupy the middle five slots of a six-slot height.
            # Cropping the full canvas into 7x5 equal pieces cuts both adjacent
            # rows and is the historical source of frame fragments in-game.
            x0 = int(round((col + 0.5) * source.width / (cols + 1)))
            x1 = int(round((col + 1.5) * source.width / (cols + 1)))
            y0 = int(round((row + 0.5) * source.height / (rows + 1)))
            y1 = int(round((row + 1.5) * source.height / (rows + 1)))
            cell = key_erlang_checkerboard_cell(source.crop((x0, y0, x1, y1)))
            cell = clean_cell_components(cell, isolate_primary=False, threshold=12)
            bbox = cell.getbbox()
            sprites.append(cell.crop(bbox) if bbox else None)
        visible = [sprite for sprite in sprites if sprite is not None]
        if not visible:
            continue
        row_scale = min(
            (cell_size - padding * 2) / max(sprite.width for sprite in visible),
            (cell_size - padding * 2) / max(sprite.height for sprite in visible),
            1.0,
        )
        for col, sprite in enumerate(sprites):
            if sprite is None:
                continue
            resized = sprite.resize(
                (max(1, int(round(sprite.width * row_scale))), max(1, int(round(sprite.height * row_scale)))),
                Image.Resampling.LANCZOS,
            )
            dx = col * cell_size + (cell_size - resized.width) // 2
            dy = row * cell_size + cell_size - padding - resized.height
            output.paste(resized, (dx, dy), resized)
    # Lossless output prevents WebP ringing from rebuilding pale boxes around
    # the white robe and keeps the small cyan third eye crisp at game scale.
    output.save(os.path.join(OUTPUT_DIR, "erlang_player_actions.webp"), "WEBP", lossless=True, method=6)
    print("Processed erlang_player_actions.webp: 5 rows x 7 isolated frames with 56px gutters")
    return output


def package_erlang_combo_actions():
    """Publish five dedicated seven-frame Erlang combo clips.

    The generated board uses a baked light checkerboard, but its five authored
    rows include unequal outer margins. Dividing the canvas into five equal
    slices cuts row zero at the feet, shifts every later clip down a row, and
    leaves most of rows three/four empty. Detect the seven pose columns and five
    animation rows from the keyed artwork itself, then cut at the transparent
    midpoints. Detached lightning and Xiaotianquan poses are deliberately kept.
    """
    source_path = os.path.join(ERLANG_FENGSHEN_DIR, "erlang_combo_actions_v1_source.png")
    if not os.path.exists(source_path):
        print(f"WARNING: missing Erlang combo source {source_path}")
        return None
    source = Image.open(source_path).convert("RGBA")
    rows, cols, cell_size, padding = 5, 7, 240, 48
    keyed_board = key_alignment_checkerboard(source, strict=True)
    board_alpha = np.array(keyed_board.getchannel("A")) > 12

    def projection_bands(counts, expected):
        active = np.where(counts > 20)[0]
        raw_bands = []
        if active.size:
            start = previous = int(active[0])
            for coordinate in active[1:]:
                coordinate = int(coordinate)
                if coordinate > previous + 1:
                    raw_bands.append((start, previous))
                    start = coordinate
                previous = coordinate
            raw_bands.append((start, previous))
        # Ignore isolated keyed checker specks between the real pose lanes.
        bands = [
            (start, end) for start, end in raw_bands
            if end - start + 1 >= 8 and int(counts[start:end + 1].sum()) >= 500
        ]
        if len(bands) != expected:
            raise RuntimeError(
                f"Erlang combo board yielded {len(bands)}/{expected} authored bands: {bands}"
            )
        return bands

    row_bands = projection_bands(board_alpha.sum(axis=1), rows)
    col_bands = projection_bands(board_alpha.sum(axis=0), cols)

    def band_edges(bands, limit):
        edges = [0]
        for (_, previous_end), (next_start, _) in zip(bands, bands[1:]):
            edges.append((previous_end + next_start + 1) // 2)
        edges.append(limit)
        return edges

    row_edges = band_edges(row_bands, source.height)
    col_edges = band_edges(col_bands, source.width)
    output = Image.new("RGBA", (cols * cell_size, rows * cell_size), (0, 0, 0, 0))
    for row in range(rows):
        sprites = []
        for col in range(cols):
            x0, x1 = col_edges[col], col_edges[col + 1]
            y0, y1 = row_edges[row], row_edges[row + 1]
            cell = keyed_board.crop((x0, y0, x1, y1))
            # The hound-pin row intentionally contains two actors, while other
            # rows include detached lightning. Preserve all in-lane components;
            # the projection midpoint has already isolated neighboring frames.
            cell = clean_cell_components(cell, isolate_primary=False, threshold=12)
            bbox = cell.getbbox()
            sprites.append(cell.crop(bbox) if bbox else None)
        visible = [sprite for sprite in sprites if sprite is not None]
        if not visible:
            continue
        row_scale = min(
            (cell_size - padding * 2) / max(sprite.width for sprite in visible),
            (cell_size - padding * 2) / max(sprite.height for sprite in visible),
            1.0,
        )
        for col, sprite in enumerate(sprites):
            if sprite is None:
                continue
            resized = sprite.resize(
                (max(1, round(sprite.width * row_scale)), max(1, round(sprite.height * row_scale))),
                Image.Resampling.LANCZOS,
            )
            dx = col * cell_size + (cell_size - resized.width) // 2
            dy = row * cell_size + cell_size - padding - resized.height
            output.paste(resized, (dx, dy), resized)
    output.save(os.path.join(OUTPUT_DIR, "erlang_combo_actions.webp"), "WEBP", lossless=True, method=6)
    print("Processed erlang_combo_actions.webp: 5 complete combo clips x 7 frames with 48px gutters")
    return output


def package_fengshen_bosses():
    """Normalize five ImageGen-authored Fengshen bosses to the 7x5 campaign contract."""
    source_path = os.path.join(ERLANG_FENGSHEN_DIR, "fengshen_bosses_v1_source.png")
    if not os.path.exists(source_path):
        print(f"WARNING: missing Fengshen boss source {source_path}")
        return None
    source = Image.open(source_path).convert("RGBA")
    rows, cols, cell_size, padding = 5, 7, 200, 34
    authored_seed = np.array(source.getchannel("A")) > 30

    def projection_bands(counts, threshold, expected):
        active = np.where(counts > threshold)[0]
        bands = []
        if active.size:
            start = previous = int(active[0])
            for coordinate in active[1:]:
                coordinate = int(coordinate)
                if coordinate - previous > 5:
                    bands.append((start, previous))
                    start = coordinate
                previous = coordinate
            bands.append((start, previous))
        if len(bands) != expected:
            raise ValueError(f"Fengshen atlas expected {expected} separated pose bands; found {len(bands)}")
        boundaries = [0]
        boundaries.extend((bands[index][1] + bands[index + 1][0]) // 2 for index in range(expected - 1))
        boundaries.append(len(counts))
        return boundaries

    # ImageGen deliberately left unequal outer margins around the board. Derive
    # the real pose bands instead of cutting a mathematical grid through heads,
    # clouds, and subdued poses.
    x_bounds = projection_bands(authored_seed.sum(axis=0), 15, cols)
    y_bounds = projection_bands(authored_seed.sum(axis=1), 25, rows)
    output = Image.new("RGBA", (cols * cell_size, rows * cell_size), (0, 0, 0, 0))
    for row in range(rows):
        sprites = []
        for col in range(cols):
            x0, x1 = x_bounds[col], x_bounds[col + 1]
            y0, y1 = y_bounds[row], y_bounds[row + 1]
            cell = source.crop((x0, y0, x1, y1)).convert("RGBA")
            cell = clean_cell_components(cell, isolate_primary=True, threshold=12)
            bbox = cell.getbbox()
            sprites.append(cell.crop(bbox) if bbox else None)
        visible = [sprite for sprite in sprites if sprite is not None]
        if not visible:
            continue
        row_scale = min(
            (cell_size - padding * 2) / max(sprite.width for sprite in visible),
            (cell_size - padding * 2) / max(sprite.height for sprite in visible),
            1.0,
        )
        for col, sprite in enumerate(sprites):
            if sprite is None:
                continue
            resized = sprite.resize(
                (max(1, round(sprite.width * row_scale)), max(1, round(sprite.height * row_scale))),
                Image.Resampling.LANCZOS,
            )
            dx = col * cell_size + (cell_size - resized.width) // 2
            dy = row * cell_size + cell_size - padding - resized.height
            output.paste(resized, (dx, dy), resized)
    output.save(os.path.join(OUTPUT_DIR, "fengshen_bosses.webp"), "WEBP", lossless=True, method=6)
    print("Processed fengshen_bosses.webp: five bosses x seven isolated combat states")
    return output


def package_ng_plus_enemies():
    """Pack twenty ImageGen-authored NG+ enemies into four safe 5x7 atlases.

    Every source is one seven-pose horizontal strip. Some built-in ImageGen
    results have genuine alpha while others contain a baked neutral checker;
    both paths converge on the same 200px cell, 48px gutter, and shared row
    scale. Keeping one identity per source prevents cross-character fragments.
    """
    cell_size, padding, cols = 200, 48, 7
    built = []
    for atlas_name, source_names in NG_PLUS_ENEMY_ATLASES.items():
        output = Image.new("RGBA", (cols * cell_size, len(source_names) * cell_size), (0, 0, 0, 0))
        for row, source_name in enumerate(source_names):
            source_path = os.path.join(NG_PLUS_ENEMY_SOURCE_DIR, source_name)
            if not os.path.exists(source_path):
                raise FileNotFoundError(f"Missing NG+ enemy source: {source_path}")
            source = Image.open(source_path).convert("RGBA")
            source_alpha = np.array(source.getchannel("A"))
            has_real_transparency = float((source_alpha < 250).mean()) > 0.05
            keyed = source if has_real_transparency else key_alignment_checkerboard(source, strict=True)

            sprites = []
            for col in range(cols):
                x0 = int(round(col * keyed.width / cols))
                x1 = int(round((col + 1) * keyed.width / cols))
                cell = keyed.crop((x0, 0, x1, keyed.height))
                cell = clean_cell_components(cell, isolate_primary=False, threshold=12)
                alpha = np.array(cell.getchannel("A"))
                ys, xs = np.where(alpha > 8)
                if not len(xs):
                    raise RuntimeError(f"Empty NG+ pose {source_name} column {col}")
                sprites.append(cell.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)))

            row_scale = min(
                (cell_size - padding * 2) / max(sprite.width for sprite in sprites),
                (cell_size - padding * 2) / max(sprite.height for sprite in sprites),
            )
            for col, sprite in enumerate(sprites):
                resized = sprite.resize(
                    (max(1, int(round(sprite.width * row_scale))), max(1, int(round(sprite.height * row_scale)))),
                    Image.Resampling.LANCZOS,
                )
                dx = col * cell_size + (cell_size - resized.width) // 2
                dy = row * cell_size + cell_size - padding - resized.height
                # Alpha-composite preserves the authored antialiasing exactly;
                # PIL's masked paste multiplies translucent edge alpha twice.
                output.alpha_composite(resized, dest=(dx, dy))

        output_path = os.path.join(OUTPUT_DIR, f"{atlas_name}.webp")
        # Some ImageGen PNGs contain bright RGB residue under fully transparent
        # pixels. Canvas rendering respects alpha, but zeroing that hidden color
        # also makes every decoder/preview safe and prevents resampling fringes.
        output_rgba = np.array(output)
        output_rgba[output_rgba[:, :, 3] == 0, :3] = 0
        output = Image.fromarray(output_rgba, "RGBA")
        output.save(output_path, "WEBP", lossless=True, method=6)
        built.append(output_path)
        print(f"Processed {atlas_name}.webp: 5 NG+ identities x 7 complete combat states")
    return built


def package_fengshen_enemies():
    """Build four unique seven-state minion rows for Erlang's chronicle."""
    sources = (
        "fengshen_mirror_disciple_v1_source.png",
        "fengshen_soul_guard_v1_source.png",
        "fengshen_array_adept_v1_source.png",
        "fengshen_meishan_raider_v1_source.png",
    )
    cell_size = 200
    padding = 48
    output = Image.new("RGBA", (cell_size * 7, cell_size * len(sources)), (0, 0, 0, 0))
    for row, filename in enumerate(sources):
        source_path = os.path.join(ERLANG_FENGSHEN_DIR, filename)
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Missing Fengshen enemy animation source: {source_path}")
        source = Image.open(source_path).convert("RGBA")
        sprites = []
        for column in range(7):
            x0 = int(round(column * source.width / 7))
            x1 = int(round((column + 1) * source.width / 7))
            # Each ImageGen strip uses a baked neutral checker. Retain the
            # chromatic/dark ink seed and its antialiased edge; a flood-only key
            # can trap checker rectangles inside circular mirrors and banners.
            frame = key_alignment_checkerboard(source.crop((x0, 0, x1, source.height)), strict=True)
            frame = clean_cell_components(frame, isolate_primary=False, threshold=10)
            bbox = frame.getbbox()
            if not bbox:
                raise ValueError(f"Empty Fengshen enemy frame {filename} c{column}")
            sprites.append(frame.crop(bbox))

        row_scale = min(
            (cell_size - padding * 2) / max(sprite.width for sprite in sprites),
            (cell_size - padding * 2) / max(sprite.height for sprite in sprites),
        )
        for column, sprite in enumerate(sprites):
            resized = sprite.resize(
                (max(1, round(sprite.width * row_scale)), max(1, round(sprite.height * row_scale))),
                Image.Resampling.LANCZOS,
            )
            x = column * cell_size + (cell_size - resized.width) // 2
            y = row * cell_size + cell_size - padding - resized.height
            output.paste(resized, (x, y), resized)

    output_path = os.path.join(OUTPUT_DIR, "fengshen_enemies.webp")
    output.save(output_path, "WEBP", lossless=True, method=6)
    print("Processed fengshen_enemies.webp: 4 unique enemies x 7 complete combat states")
    return output


def package_fengshen_cutscenes():
    """Split two Erlang-perspective Fengshen storyboards into eight cinematic slides."""
    sources = {
        "cutscene_fengshen_act1": "fengshen_cutscenes_act1_source.png",
        "cutscene_fengshen_act2": "fengshen_cutscenes_act2_source.png",
    }
    packaged = 0
    for asset_base, filename in sources.items():
        source_path = os.path.join(ERLANG_FENGSHEN_DIR, filename)
        if not os.path.exists(source_path):
            print(f"WARNING: missing Fengshen cutscene source {source_path}")
            continue
        storyboard = Image.open(source_path).convert("RGB")
        mid_x, mid_y = storyboard.width // 2, storyboard.height // 2
        quadrants = (
            (0, 0, mid_x, mid_y),
            (mid_x, 0, storyboard.width, mid_y),
            (0, mid_y, mid_x, storyboard.height),
            (mid_x, mid_y, storyboard.width, storyboard.height),
        )
        first_frame = None
        for slide, box in enumerate(quadrants, start=1):
            panel = _trim_storyboard_gutter(storyboard.crop(box))
            frame = _cinematic_canvas(panel)
            frame.save(os.path.join(OUTPUT_DIR, f"{asset_base}_slide_{slide}.webp"), "WEBP", quality=88, method=6)
            if first_frame is None:
                first_frame = frame
            packaged += 1
        if first_frame is not None:
            first_frame.save(os.path.join(OUTPUT_DIR, f"{asset_base}.webp"), "WEBP", quality=88, method=6)
    print(f"Processed {packaged} Erlang-perspective Fengshen cutscene slides")

def clean_cell_components(cell, isolate_primary=False, threshold=20):
    """Remove matte specks and foreign-frame fragments from one logical atlas cell."""
    rgba = np.array(cell.convert("RGBA"))
    alpha = rgba[:, :, 3]
    mask = alpha > threshold
    height, width = mask.shape
    if not mask.any():
        return Image.new("RGBA", cell.size, (0, 0, 0, 0))

    # A two-pixel transparent seam breaks effects that physically bridge two
    # neighboring cells in crowded generated contact sheets.
    seam = 2
    mask[:seam, :] = False
    mask[-seam:, :] = False
    mask[:, :seam] = False
    mask[:, -seam:] = False

    if cv2 is None:
        cleaned = keep_largest_alpha_component(Image.fromarray(rgba, "RGBA"), threshold)
        return cleaned if isolate_primary else Image.fromarray(rgba, "RGBA")

    count, labels, stats, centroids = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    components = []
    for label in range(1, count):
        area = int(stats[label, cv2.CC_STAT_AREA])
        if area < 8:
            continue
        x = int(stats[label, cv2.CC_STAT_LEFT])
        y = int(stats[label, cv2.CC_STAT_TOP])
        w = int(stats[label, cv2.CC_STAT_WIDTH])
        h = int(stats[label, cv2.CC_STAT_HEIGHT])
        cx, cy = centroids[label]
        edge_gap = min(x, y, width - (x + w), height - (y + h))
        center_distance = np.hypot(cx - width / 2, cy - height / 2) / max(1, np.hypot(width / 2, height / 2))
        score = area * (1.25 - min(1.0, center_distance) * 0.35)
        components.append({
            "label": label, "area": area, "bbox": (x, y, x + w, y + h),
            "edge_gap": edge_gap, "score": score,
        })

    if not components:
        return Image.new("RGBA", cell.size, (0, 0, 0, 0))

    primary = max(components, key=lambda item: item["score"])
    keep_labels = {primary["label"]}
    px0, py0, px1, py1 = primary["bbox"]
    near_limit = max(width, height) * 0.12

    for component in components:
        if component is primary:
            continue
        x0, y0, x1, y1 = component["bbox"]
        gap_x = max(0, max(px0 - x1, x0 - px1))
        gap_y = max(0, max(py0 - y1, y0 - py1))
        bbox_gap = np.hypot(gap_x, gap_y)
        is_edge_fragment = component["edge_gap"] <= seam and component["area"] < primary["area"] * 0.55

        if isolate_primary == "strict":
            continue
        if isolate_primary:
            # Preserve nearby sparks, weapons, and spell accents belonging to the
            # primary pose, but reject distant pieces entering from another cell.
            # A second component approaching the body's area is another actor,
            # never an accent (the old rule produced a two-golem walk frame).
            is_useful_accent = component["area"] >= max(12, primary["area"] * 0.004)
            is_not_second_actor = component["area"] < primary["area"] * 0.35
            if is_useful_accent and is_not_second_actor and bbox_gap <= near_limit and not is_edge_fragment:
                keep_labels.add(component["label"])
        elif not is_edge_fragment:
            keep_labels.add(component["label"])

    keep = np.isin(labels, list(keep_labels))
    # Restore one pixel of antialiasing around accepted components without
    # restoring rejected labels or the original cell boundary.
    expanded = cv2.dilate(keep.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1) > 0
    keep = expanded & (alpha > 0) & ((labels == 0) | keep)
    keep[:seam, :] = False
    keep[-seam:, :] = False
    keep[:, :seam] = False
    keep[:, -seam:] = False
    rgba[~keep] = [0, 0, 0, 0]
    return Image.fromarray(rgba, "RGBA")

def replace_atlas_row_from_generated_strip(atlas_path, strip_path, row_index, cols=7, cell_size=200, padding=30):
    """Install a complete, widely separated generated row into an existing atlas."""
    if not os.path.exists(atlas_path) or not os.path.exists(strip_path):
        return False
    keyed = key_light_checkerboard(Image.open(strip_path))
    sprites = extract_ordered_alpha_components(keyed, cols, threshold=20, min_pixels=5000)
    if len(sprites) != cols:
        print(f"WARNING: generated strip {os.path.basename(strip_path)} yielded {len(sprites)}/{cols} poses")
        return False
    row = pack_component_row(sprites, cell_size, padding)
    atlas = Image.open(atlas_path).convert("RGBA")
    if atlas.width != cols * cell_size or (row_index + 1) * cell_size > atlas.height:
        return False
    atlas.paste(Image.new("RGBA", row.size, (0, 0, 0, 0)), (0, row_index * cell_size))
    atlas.paste(row, (0, row_index * cell_size), row)
    atlas.save(atlas_path, "WEBP", quality=95, method=6)
    print(f"Installed regenerated row {row_index} from {os.path.basename(strip_path)} with {padding}px gutters")
    return True

def repack_safe_atlas(path, rows, cols, cell_w, cell_h, padding, isolate_primary, align="bottom"):
    """Rebuild an atlas with a uniform transparent gutter and stable row scale."""
    if not os.path.exists(path):
        return
    source = Image.open(path).convert("RGBA")
    expected_size = (cols * cell_w, rows * cell_h)
    if source.size != expected_size:
        print(f"WARNING: skipping safe repack for {os.path.basename(path)}: {source.size} != {expected_size}")
        return

    rows_of_sprites = []
    for row in range(rows):
        sprites = []
        for col in range(cols):
            cell = source.crop((col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h))
            cleaned = clean_cell_components(cell, isolate_primary=isolate_primary)
            alpha = np.array(cleaned.getchannel("A"))
            ys, xs = np.where(alpha > 4)
            if not len(xs):
                sprites.append(None)
                continue
            sprites.append(cleaned.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)))
        rows_of_sprites.append(sprites)

    output = Image.new("RGBA", expected_size, (0, 0, 0, 0))
    inner_w = cell_w - padding * 2
    inner_h = cell_h - padding * 2
    for row, sprites in enumerate(rows_of_sprites):
        visible = [sprite for sprite in sprites if sprite is not None]
        if not visible:
            continue
        # One scale per animation row prevents body-size pumping between frames.
        row_scale = min(
            inner_w / max(sprite.width for sprite in visible),
            inner_h / max(sprite.height for sprite in visible),
        )
        for col, sprite in enumerate(sprites):
            if sprite is None:
                continue
            resized = sprite.resize(
                (max(1, int(round(sprite.width * row_scale))), max(1, int(round(sprite.height * row_scale)))),
                Image.Resampling.LANCZOS,
            )
            dx = col * cell_w + (cell_w - resized.width) // 2
            if align == "bottom":
                dy = row * cell_h + cell_h - padding - resized.height
            else:
                dy = row * cell_h + (cell_h - resized.height) // 2
            output.paste(resized, (dx, dy), resized)

    output.save(path, "WEBP", quality=95, method=6)
    print(f"Safe-repacked {os.path.basename(path)}: {rows}x{cols}, gutter>={padding}px")

def normalize_all_animation_atlases():
    """Apply the same no-bleed contract to every animation atlas consumed by the game."""
    # filename, rows, cols, cell width, cell height, gutter, isolate character pose, alignment
    atlas_specs = [
        ("hero.webp", 7, 7, 128, 128, 28, True, "bottom"),
        ("monsters_beasts.webp", 6, 10, 128, 128, 28, True, "bottom"),
        ("erlang_and_dog.webp", 5, 6, 160, 160, 38, True, "bottom"),
        ("erlang_player_actions.webp", 5, 7, 240, 240, 56, True, "bottom"),
        ("xiaotianquan_attack.webp", 1, 5, 220, 220, 52, True, "bottom"),
        ("xiaotianquan_empowered_slam.webp", 1, 7, 240, 240, 56, True, "bottom"),
        ("buddha_colossal.webp", 4, 7, 256, 256, 60, True, "bottom"),
        ("infinite_bosses_a.webp", 6, 9, 160, 160, 38, True, "bottom"),
        ("luban_avatar.webp", 4, 8, 128, 128, 28, True, "bottom"),
        ("wukong_real_anims.webp", 5, 7, 160, 160, 38, True, "bottom"),
        ("enemies_real_anims.webp", 6, 7, 160, 160, 38, True, "bottom"),
        ("bosses_real_anims.webp", 4, 8, 160, 160, 38, True, "bottom"),
        ("elemental_slashes.webp", 5, 9, 160, 160, 38, False, "center"),
        ("special_enemies_anims.webp", 6, 8, 160, 160, 38, True, "bottom"),
        ("wukong_combat_combos.webp", 4, 7, 220, 220, 52, True, "bottom"),
        ("wukong_ruyi_throw.webp", 1, 7, 220, 220, 52, False, "bottom"),
        ("ruyi_boomerang_spin.webp", 1, 7, 220, 220, 52, False, "center"),
        ("wukong_hair_clones.webp", 4, 6, 200, 200, 48, False, "bottom"),
        ("ruyi_staff_slashes.webp", 4, 6, 200, 200, 48, False, "center"),
        ("hades_magic_circles.webp", 4, 6, 200, 200, 48, False, "center"),
        ("wukong_72_forms.webp", 5, 7, 200, 200, 48, True, "bottom"),
        ("wukong_72_form_attacks.webp", 5, 7, 200, 200, 48, True, "bottom"),
        ("ruyi_special_slam.webp", 4, 7, 200, 200, 48, False, "center"),
        ("gods_boon_slashes.webp", 5, 8, 160, 160, 38, False, "center"),
        ("ruyi_impact_burst.webp", 2, 4, 256, 256, 60, False, "center"),
        ("campaign_characters_act1.webp", 5, 7, 200, 200, 48, True, "bottom"),
        ("campaign_characters_act2.webp", 5, 7, 200, 200, 48, True, "bottom"),
        ("campaign_characters_act3.webp", 7, 7, 200, 200, 48, True, "bottom"),
        ("campaign_characters_act4.webp", 6, 7, 200, 200, 48, True, "bottom"),
        ("campaign_characters_act5.webp", 6, 7, 200, 200, 48, True, "bottom"),
        ("campaign_characters_act6.webp", 7, 7, 200, 200, 48, True, "bottom"),
        ("four_heavenly_kings.webp", 4, 7, 200, 200, 48, True, "bottom"),
        ("fengshen_enemies.webp", 4, 7, 200, 200, 48, True, "bottom"),
        ("boss_skill_fx.webp", 3, 7, 256, 256, 60, False, "center"),
        ("ruyi_melee_combo_fx.webp", 3, 7, 256, 256, 60, False, "center"),
    ]
    for filename, rows, cols, cell_w, cell_h, padding, isolate_primary, align in atlas_specs:
        repack_safe_atlas(
            os.path.join(OUTPUT_DIR, filename), rows, cols, cell_w, cell_h,
            padding, isolate_primary, align,
        )

def repair_hero_incomplete_source_frames():
    """Replace known label/fragment slots from the legacy hero contact sheet."""
    path = os.path.join(OUTPUT_DIR, "hero.webp")
    if not os.path.exists(path):
        return
    cell = 128
    sheet = Image.open(path).convert("RGBA")
    replacements = {
        (2, 6): (2, 5),  # missing final side-run frame
        (3, 0): (3, 1),  # source title/label intruded into the first attack cell
        (3, 4): (3, 3),  # source contained only a detached slash fragment
        (4, 0): (4, 1),  # source title/label intruded into the first combo cell
        (4, 6): (4, 5),  # source contained only the end of a staff
    }
    for (dest_row, dest_col), (src_row, src_col) in replacements.items():
        source_frame = sheet.crop((src_col * cell, src_row * cell, (src_col + 1) * cell, (src_row + 1) * cell))
        sheet.paste(Image.new("RGBA", (cell, cell), (0, 0, 0, 0)), (dest_col * cell, dest_row * cell))
        sheet.paste(source_frame, (dest_col * cell, dest_row * cell), source_frame)
    sheet.save(path, "WEBP", quality=95, method=6)
    print(f"Repaired {len(replacements)} incomplete legacy hero frames with complete neighboring poses")


def repair_campaign_defeat_identity_frames():
    """Prevent three act-3 bosses from turning into a different character on defeat."""
    path = os.path.join(OUTPUT_DIR, "campaign_characters_act3.webp")
    if not os.path.exists(path):
        return
    cell = 200
    sheet = Image.open(path).convert("RGBA")
    # The generated contact sheet's final three defeat cells were shifted up by
    # one character row. Reuse each character's complete hurt/subdued pose; the
    # runtime already supplies the death rise, dissolve, and fade animation.
    repaired_rows = (1, 2, 3)
    for row in repaired_rows:
        source_frame = sheet.crop((5 * cell, row * cell, 6 * cell, (row + 1) * cell))
        sheet.paste(Image.new("RGBA", (cell, cell), (0, 0, 0, 0)), (6 * cell, row * cell))
        sheet.paste(source_frame, (6 * cell, row * cell), source_frame)
    sheet.save(path, "WEBP", quality=95, method=6)
    print(f"Repaired {len(repaired_rows)} act-3 defeat cells with same-character poses")


def repair_campaign_sparse_body_frames():
    """Replace effect-only campaign slots that shrink the actor to a fragment."""
    repairs = {
        # The authored release cell contains a tiny receding body plus a spear.
        # Campaign projectiles are drawn separately, so retain the complete
        # wind-up body at contact instead of making the minion visibly collapse.
        "campaign_characters_act6.webp": {(6, 3): (6, 2)},
    }
    repaired = 0
    for filename, replacements in repairs.items():
        path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(path):
            continue
        cell = 200
        sheet = Image.open(path).convert("RGBA")
        for (dest_row, dest_col), (src_row, src_col) in replacements.items():
            source_frame = sheet.crop((src_col * cell, src_row * cell, (src_col + 1) * cell, (src_row + 1) * cell))
            sheet.paste(Image.new("RGBA", (cell, cell), (0, 0, 0, 0)), (dest_col * cell, dest_row * cell))
            sheet.paste(source_frame, (dest_col * cell, dest_row * cell), source_frame)
            repaired += 1
        sheet.save(path, "WEBP", quality=95, method=6)
    print(f"Repaired {repaired} sparse campaign body frame with a complete same-character pose")

def clean_hero_grid(sheet):
    """Remove label/fragment columns and publish the exact 7x7 grid used by the renderer."""
    if sheet is None:
        return
    cell = 128
    cleaned = Image.new("RGBA", (cell * 7, cell * 7), (0, 0, 0, 0))
    for row in range(min(7, sheet.height // cell)):
        source_start = 1 if row == 2 and sheet.width >= cell * 8 else 0
        for col in range(7):
            sx = (source_start + col) * cell
            if sx + cell <= sheet.width:
                frame = sheet.crop((sx, row * cell, sx + cell, (row + 1) * cell))
                cleaned.paste(frame, (col * cell, row * cell), frame)
    cleaned.save(os.path.join(OUTPUT_DIR, "hero.webp"), "WEBP", quality=95, method=6)
    print("Cleaned hero.webp to the renderer contract: 7 rows x 7 cols (896x896)")

def package_all():
    print("Packaging ALL sheets with clean projection segmentation and zero clipping...")
    # ImageGen-authored Good / Neutral / Evil Wukong presentation art. The
    # transparent PNG is the durable project source; CSS crops its three equal
    # horizontal panels, so retain the authored spacing instead of segmenting it.
    alignment_portraits = os.path.join(OUTPUT_DIR, "wukong_alignment_portraits_v1.png")
    if os.path.exists(alignment_portraits):
        portrait_sheet = Image.open(alignment_portraits).convert("RGBA")
        portrait_sheet.save(
            os.path.join(OUTPUT_DIR, "wukong_alignment_portraits.webp"),
            "WEBP", quality=94, method=6
        )
        print("Processed wukong_alignment_portraits.webp: Good / Neutral / Evil")

    package_cutscene_art()
    package_cutscene_storyboard_frames()
    package_alignment_animation_atlases()
    package_wukong_combo_move_atlases()
    package_evil_ruyi_combo_fx()
    package_ruyi_contact_attacks()
    package_ruyi_temporal_bodies()
    
    # 1. WUKONG HERO (128x128)
    hero_sheet = segment_and_build(
        os.path.join(BRAIN_DIR, "wukong_4dir_sheet_1786998960863.jpg"),
        cell_size=(128, 128),
        out_filename="hero.webp",
        skip_left=120,
        min_h=55,
        row_threshold=40,
        col_threshold=25,
        pad_bottom=8
    )
    clean_hero_grid(hero_sheet)
    
    # 2. 4-DIRECTIONAL ENEMIES (128x128)
    # The source is a real logical grid. Projection segmentation used to split
    # spears, bows, and a second golem into neighboring frames.
    repack_known_source_grid(
        os.path.join(BRAIN_DIR, "enemies_4dir_sheet_1786999201516.jpg"),
        source_rows=6,
        source_cols=[8, 8, 8, 8, 8, 4],
        dest_cols=10,
        cell_size=128,
        out_filename="monsters_beasts.webp",
        padding=28,
    )
    
    # 3. ERLANG SHEN & XIAOTIAN DOG (160x160)
    repack_known_source_grid(
        os.path.join(BRAIN_DIR, "erlang_and_dog_sheet_1786999371485.jpg"),
        source_rows=5,
        source_cols=4,
        dest_cols=6,
        cell_size=160,
        out_filename="erlang_and_dog.webp",
        padding=38,
    )
    
    # 4. GIANT BUDDHA (256x256)
    segment_and_build(
        os.path.join(BRAIN_DIR, "buddha_giant_sheet_1786999931812.jpg"),
        cell_size=(256, 256),
        out_filename="buddha_colossal.webp",
        skip_left=0,
        min_h=60,
        row_threshold=40,
        col_threshold=20,
        pad_bottom=8
    )
    
    # 5. INFINITE BOSSES SET A (160x160)
    repack_known_source_grid(
        os.path.join(BRAIN_DIR, "bosses_pink_sheet_1786998590130.jpg"),
        source_rows=6,
        source_cols=[6, 6, 8, 6, 6, 6],
        dest_cols=9,
        cell_size=160,
        out_filename="infinite_bosses_a.webp",
        padding=38,
    )
    
    # 6. LUBAN AVATAR (128x128)
    segment_and_build(
        os.path.join(BRAIN_DIR, "luban_avatar_sheet_1786999799774.jpg"),
        cell_size=(128, 128),
        out_filename="luban_avatar.webp",
        skip_left=0,
        min_h=35,
        row_threshold=30,
        col_threshold=15,
        pad_bottom=8
    )
    
    # 7. 11 GODS PORTRAITS (Exact 6 cols x 2 rows = 1536x512)
    gods_path = os.path.join(BRAIN_DIR, "chinese_gods_portraits_1786995883867.jpg")
    if os.path.exists(gods_path):
        img = Image.open(gods_path)
        keyed, _ = key_magenta(img)
        resized = keyed.resize((1536, 512), Image.Resampling.LANCZOS)
        resized.save(os.path.join(OUTPUT_DIR, "gods_atlas.webp"), "WEBP", quality=95)
        print("-> Packaged 11 Gods Atlas (1536x512) with exact 6x2 grid alignment")
        
    # 8. WUKONG REAL COMBAT ANIMATIONS (160x160)
    wukong_anim_path = os.path.join(BRAIN_DIR, "wukong_real_anims_1787032432502.jpg")
    if os.path.exists(wukong_anim_path):
        repack_known_source_grid(
            wukong_anim_path,
            source_rows=5,
            source_cols=6,
            dest_cols=7,
            cell_size=160,
            out_filename="wukong_real_anims.webp",
            padding=38,
        )

    # 9. ENEMIES REAL COMBAT ANIMATIONS (160x160)
    enemies_anim_path = os.path.join(BRAIN_DIR, "enemies_real_anims_1787032494143.jpg")
    if os.path.exists(enemies_anim_path):
        repack_known_source_grid(
            enemies_anim_path,
            source_rows=6,
            source_cols=6,
            dest_cols=7,
            cell_size=160,
            out_filename="enemies_real_anims.webp",
            padding=38,
        )

    # 10. BOSSES REAL COMBAT ANIMATIONS (160x160)
    bosses_anim_path = os.path.join(BRAIN_DIR, "bosses_real_anims_1787033016899.jpg")
    if os.path.exists(bosses_anim_path):
        repack_known_source_grid(
            bosses_anim_path,
            source_rows=4,
            source_cols=6,
            dest_cols=8,
            cell_size=160,
            out_filename="bosses_real_anims.webp",
            padding=38,
        )

    # 11. ELEMENTAL SLASHES ANIMATIONS (160x160)
    slashes_path = os.path.join(BRAIN_DIR, "elemental_slashes_1787069480161.jpg")
    if os.path.exists(slashes_path):
        segment_and_build(
            slashes_path,
            cell_size=(160, 160),
            out_filename="elemental_slashes.webp",
            skip_left=0,
            min_h=40,
            row_threshold=25,
            col_threshold=15,
            pad_bottom=10
        )

    # 12. SPECIALIZED ENEMIES & MINI-BOSSES ANIMATIONS (160x160)
    special_path = os.path.join(BRAIN_DIR, "special_enemies_anims_1787070099023.jpg")
    if os.path.exists(special_path):
        repack_known_source_grid(
            special_path,
            source_rows=6,
            source_cols=6,
            dest_cols=8,
            cell_size=160,
            out_filename="special_enemies_anims.webp",
            padding=38,
        )

    # 13. WUKONG COMBAT COMBOS & LEAP SMASH (220x220 - Magenta keyed & clean projection)
    combos_path = os.path.join(BRAIN_DIR, "wukong_combat_combos_1787070977933.jpg")
    if os.path.exists(combos_path):
        segment_and_build(
            combos_path,
            cell_size=(220, 220),
            out_filename="wukong_combat_combos.webp",
            skip_left=0,
            min_h=40,
            min_w=15,
            row_threshold=20,
            col_threshold=12,
            pad_bottom=10
        )

    # 14. WUKONG BLOW HAIR & MONKEY CLONE ARMY (200x200 - Magenta keyed & clean projection)
    hair_path = os.path.join(BRAIN_DIR, "wukong_hair_clones_1787071568312.jpg")
    if os.path.exists(hair_path):
        segment_and_build(
            hair_path,
            cell_size=(200, 200),
            out_filename="wukong_hair_clones.webp",
            skip_left=0,
            min_h=40,
            min_w=15,
            row_threshold=20,
            col_threshold=12,
            pad_bottom=10
        )

    # 15. HADES-STYLE PURE RUYI STAFF DIVINE SLASHES (200x200 - PURE VFX ONLY, NO HUMANOID FIGURE)
    slashes_vfx_path = os.path.join(BRAIN_DIR, "pure_staff_slashes_1787074847236.jpg")
    if os.path.exists(slashes_vfx_path):
        img = Image.open(slashes_vfx_path).convert("RGBA")
        arr = np.array(img).astype(float)
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        max_c = np.maximum(np.maximum(r, g), b)
        arr[:, :, 3] = np.clip((max_c - 14.0) / 40.0, 0.0, 1.0) * 255.0
        keyed = Image.fromarray(arr.astype(np.uint8), "RGBA").resize((1200, 800), Image.Resampling.LANCZOS)
        keyed.save(os.path.join(OUTPUT_DIR, "ruyi_staff_slashes.webp"), "WEBP", quality=95)
        print("Processed PURE ruyi_staff_slashes.webp: 4 rows x 6 cols (1200x800) with NO humanoid figures")

    # 16. HADES-STYLE MAGIC CIRCLES & CIRCULAR 360 NOVA AOE (200x200)
    magic_vfx_path = os.path.join(BRAIN_DIR, "hades_magic_circles_1787073127168.jpg")
    if os.path.exists(magic_vfx_path):
        img = Image.open(magic_vfx_path).convert("RGBA")
        arr = np.array(img).astype(float)
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        max_c = np.maximum(np.maximum(r, g), b)
        arr[:, :, 3] = np.clip((max_c - 16.0) / 45.0, 0.0, 1.0) * 255.0
        keyed = Image.fromarray(arr.astype(np.uint8), "RGBA").resize((1200, 800), Image.Resampling.LANCZOS)
        keyed.save(os.path.join(OUTPUT_DIR, "hades_magic_circles.webp"), "WEBP", quality=95)
        print("Processed hades_magic_circles.webp: 4 rows x 6 cols (1200x800)")

    # 17. 72 TRANSFORMATIONS BEAST FORMS (200x200)
    forms_path = os.path.join(BRAIN_DIR, "wukong_72_forms_1787073714459.jpg")
    if os.path.exists(forms_path):
        pad_grid_sheet(
            forms_path,
            grid_rows=4,
            grid_cols=7,
            cell_w=200,
            cell_h=200,
            out_filename="wukong_72_forms.webp",
            padding=30,
            key_mode="magenta"
        )

    # 18. RUYI JINGU BANG SPECIAL SLAM & DING HAI SHEN ZHEN (200x200)
    special_slam_path = os.path.join(BRAIN_DIR, "ruyi_special_slam_1787074607931.jpg")
    if os.path.exists(special_slam_path):
        img = Image.open(special_slam_path).convert("RGBA")
        arr = np.array(img).astype(float)
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        max_c = np.maximum(np.maximum(r, g), b)
        arr[:, :, 3] = np.clip((max_c - 16.0) / 45.0, 0.0, 1.0) * 255.0
        keyed = Image.fromarray(arr.astype(np.uint8), "RGBA").resize((1400, 800), Image.Resampling.LANCZOS)
        keyed.save(os.path.join(OUTPUT_DIR, "ruyi_special_slam.webp"), "WEBP", quality=95)
        print("Processed ruyi_special_slam.webp: 4 rows x 7 cols (1400x800)")

    # 19. 11 GODS & ELEMENTAL BOON ATTACK SLASHES (160x160)
    gods_slashes_path = os.path.join(BRAIN_DIR, "gods_boon_slashes_1787075095023.jpg")
    if os.path.exists(gods_slashes_path):
        img = Image.open(gods_slashes_path).convert("RGBA")
        arr = np.array(img).astype(float)
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        max_c = np.maximum(np.maximum(r, g), b)
        arr[:, :, 3] = np.clip((max_c - 12.0) / 38.0, 0.0, 1.0) * 255.0
        keyed = Image.fromarray(arr.astype(np.uint8), "RGBA").resize((1280, 800), Image.Resampling.LANCZOS)
        keyed.save(os.path.join(OUTPUT_DIR, "gods_boon_slashes.webp"), "WEBP", quality=95)
        print("Processed gods_boon_slashes.webp: 5 rows x 8 cols (1280x800)")

    # 20. PROJECT-BOUND GENERATED ART: title key art, progressive karma title art,
    # impact animation, and Xuanwu form. Keep the full 16:9 title masters intact:
    # CSS positions them by height so ultrawide displays never crop Wukong's head.
    title_png = os.path.join(OUTPUT_DIR, "title_key_art.png")
    if os.path.exists(title_png):
        Image.open(title_png).convert("RGB").save(
            os.path.join(OUTPUT_DIR, "title_key_art.webp"), "WEBP", quality=88, method=6
        )
        print("Processed title_key_art.webp")

    karma_title_names = (
        "title_karma_neutral",
        "title_karma_good_1", "title_karma_good_2", "title_karma_good_3",
        "title_karma_evil_1", "title_karma_evil_2", "title_karma_evil_3",
    )
    for karma_title_name in karma_title_names:
        karma_title_png = os.path.join(OUTPUT_DIR, f"{karma_title_name}.png")
        if not os.path.exists(karma_title_png):
            continue
        Image.open(karma_title_png).convert("RGB").save(
            os.path.join(OUTPUT_DIR, f"{karma_title_name}.webp"),
            "WEBP", quality=88, method=6
        )
        print(f"Processed {karma_title_name}.webp")

    impact_png = os.path.join(OUTPUT_DIR, "ruyi_impact_burst.png")
    if os.path.exists(impact_png):
        Image.open(impact_png).convert("RGBA").resize((1024, 512), Image.Resampling.LANCZOS).save(
            os.path.join(OUTPUT_DIR, "ruyi_impact_burst.webp"), "WEBP", quality=92, method=6
        )
        print("Processed ruyi_impact_burst.webp: 2 rows x 4 cols (1024x512)")

    # Dedicated ImageGen-authored left-click combo effects. The character body is
    # intentionally absent; the renderer keeps the canonical hero sheet visible.
    repack_direct_alpha_grid(
        os.path.join(OUTPUT_DIR, "ruyi_melee_combo_fx_source.png"),
        grid_rows=3,
        grid_cols=7,
        cell_size=256,
        out_filename="ruyi_melee_combo_fx.webp",
        padding=40,
    )

    package_ruyi_boomerang_special()
    package_erlang_player_actions()
    package_erlang_combo_actions()
    package_xiaotianquan_empowered_slam()
    package_fengshen_bosses()
    package_fengshen_enemies()
    package_ng_plus_enemies()
    package_fengshen_cutscenes()
    package_four_heavenly_kings()
    package_boss_skill_fx()

    # ImageGen-authored Xiaotianquan pounce/bite strip. Isolate all five full
    # silhouettes into fixed cells so tails and paws cannot bleed across frames.
    repack_alpha_strip(
        os.path.join(OUTPUT_DIR, "xiaotianquan_attack_strip_v1.png"),
        5,
        220,
        "xiaotianquan_attack.webp",
        padding=34,
    )

    generated_forms = [
        ("dragon_form_strip.png", "dragon_form_strip.webp"),
        ("tiger_form_strip.png", "tiger_form_strip.webp"),
        ("roc_form_strip.png", "roc_form_strip.webp"),
        ("ape_form_strip.png", "ape_form_strip.webp"),
        ("tortoise_form_strip.png", "tortoise_form_strip.webp"),
    ]
    form_rows = []
    for png_name, webp_name in generated_forms:
        row = repack_alpha_strip(os.path.join(OUTPUT_DIR, png_name), 7, 200, webp_name, padding=30)
        if row is not None:
            form_rows.append(row)
    if len(form_rows) == 5:
        atlas = Image.new("RGBA", (1400, 1000), (0, 0, 0, 0))
        for row_index, row in enumerate(form_rows):
            atlas.paste(row, (0, row_index * 200), row)
        atlas.save(os.path.join(OUTPUT_DIR, "wukong_72_forms.webp"), "WEBP", quality=95, method=6)
        print("Replaced legacy transformation atlas with five generated 7-frame rows (1400x1000)")

    # ImageGen-authored combat counterpart to the locomotion-only form atlas.
    # Keep the raw transparent PNG as the durable project source and deterministically
    # package it to the renderer's exact 7 x 5, 200px-cell contract on every build.
    form_attacks_png = os.path.join(OUTPUT_DIR, "wukong_72_form_attacks_v2.png")
    if os.path.exists(form_attacks_png):
        repack_component_grid(
            form_attacks_png,
            grid_rows=5,
            grid_cols=7,
            cell_size=200,
            out_filename="wukong_72_form_attacks.webp",
            padding=30,
        )
        replace_atlas_row_from_generated_strip(
            os.path.join(OUTPUT_DIR, "wukong_72_form_attacks.webp"),
            os.path.join(OUTPUT_DIR, "ape_form_attack_strip_v2.png"),
            row_index=3,
            cols=7,
            cell_size=200,
            padding=30,
        )

    # 21. IMAGEGEN-AUTHORED STORY CAMPAIGN: nine arenas and every named
    # Journey-to-the-West encounter in a deterministic compact state atlas.
    campaign_biomes_png = os.path.join(OUTPUT_DIR, "campaign_biomes_v1.png")
    if os.path.exists(campaign_biomes_png):
        Image.open(campaign_biomes_png).convert("RGB").resize(
            (1536, 1536), Image.Resampling.LANCZOS
        ).save(
            os.path.join(OUTPUT_DIR, "campaign_biomes.webp"),
            "WEBP", quality=90, method=6
        )
        print("Processed campaign_biomes.webp: 3 rows x 3 arenas (1536x1536)")

    pilgrimage_biomes_png = os.path.join(OUTPUT_DIR, "campaign_pilgrimage_biomes_v1.png")
    if os.path.exists(pilgrimage_biomes_png):
        Image.open(pilgrimage_biomes_png).convert("RGB").resize(
            (1536, 1536), Image.Resampling.LANCZOS
        ).save(
            os.path.join(OUTPUT_DIR, "campaign_pilgrimage_biomes.webp"),
            "WEBP", quality=90, method=6
        )
        print("Processed campaign_pilgrimage_biomes.webp: 3 rows x 3 arenas (1536x1536)")

    final_biomes_png = os.path.join(OUTPUT_DIR, "campaign_final_biomes_v1.png")
    if os.path.exists(final_biomes_png):
        Image.open(final_biomes_png).convert("RGB").resize(
            (1536, 1536), Image.Resampling.LANCZOS
        ).save(
            os.path.join(OUTPUT_DIR, "campaign_final_biomes.webp"),
            "WEBP", quality=90, method=6
        )
        print("Processed campaign_final_biomes.webp: 3 rows x 3 late-pilgrimage arenas (1536x1536)")

    campaign_character_specs = [
        ("campaign_characters_act1_v1.png", "campaign_characters_act1.webp", (1400, 1000), "5 characters x 7 states"),
        ("campaign_characters_act2_v1.png", "campaign_characters_act2.webp", (1400, 1000), "5 characters x 7 states"),
        ("campaign_characters_act3_v1.png", "campaign_characters_act3.webp", (1400, 1400), "7 characters x 7 states"),
        ("campaign_characters_act4_v1.png", "campaign_characters_act4.webp", (1400, 1200), "6 characters x 7 states"),
        ("campaign_characters_act5_v1.png", "campaign_characters_act5.webp", (1400, 1200), "6 characters x 7 states"),
        ("campaign_characters_act6_v1.png", "campaign_characters_act6.webp", (1400, 1400), "7 characters x 7 states"),
    ]
    for source_name, output_name, size, label in campaign_character_specs:
        source_path = os.path.join(OUTPUT_DIR, source_name)
        if not os.path.exists(source_path):
            continue
        keyed = key_pure_magenta_smooth(Image.open(source_path)).resize(size, Image.Resampling.LANCZOS)
        keyed.save(os.path.join(OUTPUT_DIR, output_name), "WEBP", quality=93, method=6)
        print(f"Processed {output_name}: {label} ({size[0]}x{size[1]})")

    # Final renderer contract: every animated cell receives a real transparent
    # gutter, stable per-row scaling, and foreign-fragment cleanup. This runs
    # after all source-specific packaging so future builds cannot restore the
    # tightly packed/contact-sheet behavior.
    normalize_all_animation_atlases()
    repair_hero_incomplete_source_frames()
    repair_campaign_defeat_identity_frames()
    repair_campaign_sparse_body_frames()

if __name__ == "__main__":
    package_all()
