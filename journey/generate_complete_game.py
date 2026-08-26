"""
Journey to the West: Complete Single-File HTML5 Game Generator
Properly structured HTML head, CSS style, HTML body, DOM elements, and JavaScript.
"""

import os
import json
import base64

OUTPUT_DIR = "assets_webp"
RUYI_GRIP_ANCHOR_MANIFEST_PATH = os.path.join(
    "assets_sources", "ruyi_contact_temporal", "wukong_ruyi_grip_anchors_v1.json"
)

with open(RUYI_GRIP_ANCHOR_MANIFEST_PATH, "r", encoding="utf-8") as anchor_fp:
    ruyi_grip_anchor_manifest = json.load(anchor_fp)
ruyi_grip_anchors = ruyi_grip_anchor_manifest["anchors"]
if set(ruyi_grip_anchors) != {"arc", "thrust", "slam", "spin"}:
    raise ValueError("Ruyi grip manifest must contain the four temporal moves")
if not all(
    len(directions) == 8 and all(len(frames) == 8 for frames in directions)
    for directions in ruyi_grip_anchors.values()
):
    raise ValueError("Ruyi grip manifest must contain 4 x 8 x 8 measured anchors")

# Package all sheets cleanly
import package_all_clean_sheets
if os.environ.get("JTW_SKIP_ASSET_PACKAGING") != "1":
    package_all_clean_sheets.package_all()

assets_keys = [
    'hero', 'seamless_floor', 'all_10_gods', 'monsters_beasts',
    'reward_icons', 'infinite_bosses_a', 'infinite_bosses_b',
    'luban_avatar', 'erlang_and_dog', 'erlang_player_actions', 'erlang_combo_actions', 'xiaotianquan_attack', 'xiaotianquan_empowered_slam', 'buddha_colossal',
    'wukong_real_anims', 'enemies_real_anims', 'bosses_real_anims',
    'elemental_slashes', 'special_enemies_anims', 'wukong_combat_combos', 'ruyi_melee_combo_fx', 'evil_ruyi_combo_fx',
    'wukong_ruyi_contact_attacks', 'ruyi_contact_weapon_paths',
    'wukong_ruyi_temporal_neutral', 'wukong_ruyi_temporal_good', 'wukong_ruyi_temporal_evil',
    'wukong_combo_moves_neutral', 'wukong_combo_moves_good', 'wukong_combo_moves_evil',
    'wukong_hair_clones', 'ruyi_staff_slashes', 'hades_magic_circles',
    'wukong_72_forms', 'wukong_72_form_attacks', 'ruyi_special_slam', 'gods_boon_slashes',
    'wukong_ruyi_throw', 'ruyi_boomerang_spin',
    'title_key_art', 'title_karma_neutral',
    'title_karma_good_1', 'title_karma_good_2', 'title_karma_good_3',
    'title_karma_evil_1', 'title_karma_evil_2', 'title_karma_evil_3',
    'ruyi_impact_burst', 'boss_skill_fx', 'four_heavenly_kings', 'fengshen_bosses', 'fengshen_enemies',
    'ng_plus_enemies_1', 'ng_plus_enemies_2', 'ng_plus_enemies_3', 'ng_plus_enemies_4',
    'campaign_biomes', 'campaign_pilgrimage_biomes', 'campaign_final_biomes',
    'campaign_characters_act1', 'campaign_characters_act2', 'campaign_characters_act3',
    'campaign_characters_act4', 'campaign_characters_act5', 'campaign_characters_act6',
    'wukong_alignment_portraits',
    'wukong_good_1', 'wukong_good_2', 'wukong_good_3',
    'wukong_evil_1', 'wukong_evil_2', 'wukong_evil_3',
    'cutscene_flower_fruit', 'cutscene_kunlun', 'cutscene_dragon_palace',
    'cutscene_havoc_heaven', 'cutscene_five_finger', 'cutscene_pilgrims',
    'cutscene_bone_spider', 'cutscene_flaming_mountain', 'cutscene_mid_trials',
    'cutscene_lion_camel', 'cutscene_late_trials', 'cutscene_vulture_peak',
    'cutscene_fengshen_act1', 'cutscene_fengshen_act2'
]

CUTSCENE_STORY_ARCS = [
    'cutscene_flower_fruit', 'cutscene_kunlun', 'cutscene_dragon_palace',
    'cutscene_havoc_heaven', 'cutscene_five_finger', 'cutscene_pilgrims',
    'cutscene_bone_spider', 'cutscene_flaming_mountain', 'cutscene_mid_trials',
    'cutscene_lion_camel', 'cutscene_late_trials', 'cutscene_vulture_peak',
    'cutscene_fengshen_act1', 'cutscene_fengshen_act2',
]
for cutscene_arc in CUTSCENE_STORY_ARCS:
    assets_keys.extend(f'{cutscene_arc}_slide_{slide}' for slide in range(1, 5))

b64_data = {}
for k in assets_keys:
    webp_path = os.path.join(OUTPUT_DIR, f"{k}.webp")
    if os.path.exists(webp_path):
        with open(webp_path, 'rb') as fp:
            enc = base64.b64encode(fp.read()).decode('utf-8')
            b64_data[k] = f"data:image/webp;base64,{enc}"

print(f"Loaded {len(b64_data)} assets into Base64.")

html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <title>西游记：孙悟空正传 (100章动作肉鸽)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@600;700;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --gold-primary: #e6b450;
      --gold-light: #fff2a8;
      --gold-dark: #8c5b16;
      --bronze: #5a3818;
      --obsidian: #08060d;
      --crimson-primary: #ef4444;
      --crimson-dark: #991b1b;
      --jade-green: #10b981;
      --jade-dark: #065f46;
      --qi-purple: #a855f7;
      --qi-glow: #d8b4fe;
      --peach-pink: #fb7185;
      --peach-glow: #fda4af;
      --sky-blue: #38bdf8;
      --font-chinese: 'Ma Shan Zheng', 'Noto Serif SC', serif;
      --font-title: 'Noto Serif SC', 'Ma Shan Zheng', serif;
      --font-body: 'Noto Serif SC', sans-serif;
      --font-en-display: Georgia, Cambria, 'Times New Roman', serif;
      --font-en-ui: 'Segoe UI', Inter, Arial, sans-serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-select: none;
    }

    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background-color: #06040a;
      font-family: var(--font-body);
      color: #f1e9da;
    }

    html[lang="en"] {
      --font-chinese: var(--font-en-ui);
      --font-title: var(--font-en-display);
      --font-body: var(--font-en-ui);
    }

    html[lang="en"] .start-title,
    html[lang="en"] .hero-name,
    html[lang="en"] .chamber-title,
    html[lang="en"] .boss-name,
    html[lang="en"] .modal-title,
    html[lang="en"] .boon-name,
    html[lang="en"] .node-title,
    html[lang="en"] .gameover-title,
    html[lang="en"] #dialogue-boss-name,
    html[lang="en"] #dialogue-mode-title {
      font-family: var(--font-en-display) !important;
      letter-spacing: 0.02em;
    }

    html[lang="en"] .hero-title,
    html[lang="en"] .chamber-subtitle,
    html[lang="en"] .bar-text,
    html[lang="en"] .currency-item,
    html[lang="en"] .action-slot,
    html[lang="en"] button,
    html[lang="en"] .modal-subtitle,
    html[lang="en"] .modal-quote,
    html[lang="en"] #dialogue-speaker-tag,
    html[lang="en"] #dialogue-text-body {
      font-family: var(--font-en-ui) !important;
      letter-spacing: 0.01em;
    }

    html[lang="en"] .hero-name { font-size: 16px; }
    html[lang="en"] .chamber-title { font-size: 20px; }
    html[lang="en"] .chamber-subtitle { font-size: 13px; max-width: 520px; line-height: 1.35; }
    html[lang="en"] .action-slot .key-badge { font-size: 10px; }

    @media (max-width: 1180px) {
      html[lang="en"] .hero-title { display: none; }
    }

    #game-container {
      position: relative;
      width: 100vw;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: radial-gradient(circle at center, #1c1228 0%, #050308 100%);
    }

    canvas#gameCanvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      display: block;
      cursor: crosshair;
      z-index: 1;
    }

    #ui-layer {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 20px;
      z-index: 10;
    }

    .top-hud {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      width: 100%;
    }

    .player-bars {
      display: flex;
      flex-direction: column;
      gap: 8px;
      width: 420px;
      filter: drop-shadow(0 4px 14px rgba(0,0,0,0.95));
    }

    .hero-tag {
      display: flex;
      align-items: center;
      gap: 10px;
      width: 100%;
      min-width: 0;
      margin-bottom: 2px;
    }

    .hero-name {
      font-family: var(--font-chinese);
      font-size: 22px;
      font-weight: 900;
      color: var(--gold-light);
      letter-spacing: 2px;
      text-shadow: 0 0 10px rgba(230, 180, 80, 0.8);
      white-space: nowrap;
      flex: 0 1 auto;
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .hero-title {
      font-family: var(--font-chinese);
      font-size: 14px;
      color: #f87171;
      margin-left: 4px;
      white-space: nowrap;
      flex: 1 1 0;
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .bar-wrapper {
      position: relative;
      height: 24px;
      background: #110e18;
      border: 2px solid var(--gold-dark);
      border-radius: 6px;
      overflow: hidden;
      box-shadow: inset 0 2px 8px rgba(0,0,0,0.95);
    }

    .bar-fill {
      height: 100%;
      width: 100%;
      transition: width 0.15s cubic-bezier(0.2, 0.9, 0.4, 1.1);
    }

    .bar-fill.health {
      background: linear-gradient(90deg, #991b1b, #ef4444, #f87171);
      box-shadow: 0 0 14px rgba(239, 68, 68, 0.8);
    }

    .bar-fill.qi {
      background: linear-gradient(90deg, #6b21a8, #a855f7, #c084fc);
      box-shadow: 0 0 14px rgba(168, 85, 247, 0.8);
    }

    .bar-fill.awakening {
      background: linear-gradient(90deg, #b45309, #f59e0b, #fef08a);
      box-shadow: 0 0 14px rgba(245, 158, 11, 0.9);
    }

    .bar-text {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 10px;
      font-family: var(--font-chinese);
      font-size: 12px;
      font-weight: 700;
      color: #fff;
      text-shadow: 0 1px 3px #000, 0 0 6px #000;
      letter-spacing: 0.5px;
    }

    .top-center-hud {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }

    .chamber-title {
      font-family: var(--font-chinese);
      font-size: 24px;
      font-weight: 900;
      color: var(--gold-light);
      letter-spacing: 2px;
      max-width: 100%;
      line-height: 1.15;
      white-space: nowrap;
      text-shadow: 0 0 14px rgba(230, 180, 80, 0.8);
    }

    .chamber-subtitle {
      font-family: var(--font-chinese);
      font-size: 16px;
      color: #e2e8f0;
      letter-spacing: 1.5px;
      margin-top: 3px;
    }

    .banner-clear-alert {
      margin-top: 6px;
      background: rgba(230, 180, 80, 0.25);
      border: 1px solid var(--gold-primary);
      color: var(--gold-light);
      padding: 4px 16px;
      border-radius: 20px;
      font-family: var(--font-chinese);
      font-size: 14px;
      display: none;
      animation: pulseAlert 1s infinite alternate;
    }

    @keyframes pulseAlert {
      from { transform: scale(0.98); opacity: 0.85; }
      to { transform: scale(1.02); opacity: 1; text-shadow: 0 0 10px #facc15; }
    }

    .currency-panel {
      display: flex;
      align-items: center;
      gap: 16px;
      background: rgba(14, 13, 19, 0.88);
      border: 2px solid var(--gold-dark);
      border-radius: 8px;
      padding: 6px 16px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.8);
    }

    .currency-item {
      display: flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font-chinese);
      font-size: 15px;
      font-weight: 700;
    }

    .currency-item.gold { color: #facc15; }
    .currency-item.ashes { color: #c084fc; }
    .currency-item.peaches { color: #fb7185; }
    .currency-item.lives { color: #4ade80; }

    .boss-bar-container {
      position: absolute;
      top: 75px;
      left: 50%;
      transform: translateX(-50%);
      width: 620px;
      display: none;
      flex-direction: column;
      align-items: center;
      filter: drop-shadow(0 4px 20px rgba(0,0,0,0.95));
      pointer-events: none;
    }

    .boss-name {
      font-family: var(--font-chinese);
      font-size: 20px;
      font-weight: 900;
      color: #fbbf24;
      letter-spacing: 2px;
      margin-bottom: 4px;
      text-shadow: 0 0 12px rgba(251, 191, 36, 0.8);
    }

    .boss-bar-wrapper {
      position: relative;
      width: 100%;
      height: 26px;
      background: #110e18;
      border: 2px solid #d97706;
      border-radius: 6px;
      overflow: hidden;
      box-shadow: inset 0 2px 8px rgba(0,0,0,0.95);
    }

    .boss-bar-fill {
      height: 100%;
      width: 100%;
      background: linear-gradient(90deg, #b91c1c, #f59e0b, #ef4444);
      box-shadow: 0 0 16px rgba(239, 68, 68, 0.9);
      transition: width 0.1s linear;
    }

    .bottom-hud {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      width: 100%;
    }

    .action-slots {
      display: flex;
      gap: 12px;
    }

    .action-slot {
      position: relative;
      width: 72px;
      height: 72px;
      background: rgba(18, 14, 26, 0.9);
      border: 2px solid var(--gold-dark);
      border-radius: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 14px rgba(0,0,0,0.8);
      transition: border-color 0.2s, transform 0.1s;
    }

    .action-slot.active {
      border-color: var(--gold-primary);
      box-shadow: 0 0 12px rgba(230, 180, 80, 0.7);
    }

    .action-slot .key-badge {
      position: absolute;
      top: -8px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--gold-primary);
      color: #000;
      font-family: var(--font-chinese);
      font-size: 11px;
      font-weight: 900;
      padding: 1px 6px;
      border-radius: 4px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.6);
      white-space: nowrap;
    }

    .action-slot .slot-label {
      font-family: var(--font-chinese);
      font-size: 12px;
      font-weight: 700;
      color: #e2e8f0;
      margin-top: 4px;
    }

    .action-slot .slot-boon {
      font-family: var(--font-chinese);
      font-size: 12px;
      color: var(--gold-light);
      margin-top: 2px;
      text-align: center;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 66px;
    }

    .quick-buttons {
      display: flex;
      gap: 10px;
      pointer-events: auto;
    }

    .btn-hud {
      background: linear-gradient(180deg, #2a1f3d, #140d21);
      border: 2px solid var(--gold-dark);
      color: var(--gold-light);
      font-family: var(--font-chinese);
      font-size: 14px;
      font-weight: 700;
      padding: 8px 16px;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      box-shadow: 0 4px 12px rgba(0,0,0,0.7);
    }

    .btn-hud:hover {
      border-color: var(--gold-primary);
      transform: translateY(-2px);
      box-shadow: 0 0 14px rgba(230, 180, 80, 0.5);
    }

    .modal-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(4, 2, 8, 0.92);
      backdrop-filter: blur(8px);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 100;
      pointer-events: auto;
      animation: fadeIn 0.25s ease-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: scale(0.97); }
      to { opacity: 1; transform: scale(1); }
    }

    .modal-box {
      position: relative;
      background: radial-gradient(circle at top, #24143a 0%, #0c0816 100%);
      border: 3px solid var(--gold-primary);
      border-radius: 14px;
      padding: 28px;
      width: 880px;
      max-width: 95vw;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: 0 10px 40px rgba(0,0,0,0.95), 0 0 30px rgba(230, 180, 80, 0.3);
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .boss-dialogue-box {
      width: min(1280px, 96vw);
      max-width: none;
      height: min(920px, 94dvh);
      max-height: 94dvh;
      padding: 14px;
      overflow: hidden;
      align-items: stretch;
      border-color: #facc15;
      background: linear-gradient(180deg, rgba(5,4,11,.99), rgba(18,10,29,.99));
      box-shadow: 0 0 54px rgba(250,204,21,.34), 0 18px 70px rgba(0,0,0,.94);
    }
    .cutscene-topbar { min-height:54px; display:grid; grid-template-columns:minmax(0,1fr) auto minmax(0,1fr); align-items:center; gap:14px; padding:4px 8px 10px; }
    .cutscene-chapter-meta { min-width:0; text-align:left; }
    #dialogue-boss-name { overflow:hidden; color:#fef3c7; font:900 21px/1.15 var(--font-title); white-space:nowrap; text-overflow:ellipsis; }
    #dialogue-boss-title { overflow:hidden; color:#fca5a5; font:700 12px/1.25 var(--font-body); white-space:nowrap; text-overflow:ellipsis; }
    #dialogue-mode-title { color:#facc15; font:900 19px/1 var(--font-title); text-shadow:0 0 16px rgba(250,204,21,.72); white-space:nowrap; }
    #dialogue-slide-counter { justify-self:end; color:#cbd5e1; font:800 12px/1 var(--font-body); letter-spacing:.08em; }
    .cutscene-frame { position:relative; flex:1 1 auto; min-height:0; overflow:hidden; border:2px solid rgba(250,204,21,.68); border-radius:10px; background:#05030a; box-shadow:inset 0 0 50px rgba(0,0,0,.75); }
    .cutscene-frame::after { content:''; position:absolute; inset:0; pointer-events:none; background:linear-gradient(180deg,rgba(0,0,0,.04) 55%,rgba(4,2,8,.68) 100%),radial-gradient(ellipse at center,transparent 46%,rgba(2,1,5,.38) 100%); }
    .cutscene-frame img { width:100%; height:100%; object-fit:cover; object-position:center; transform:scale(1.035); filter:saturate(1.04) contrast(1.03); transition:transform 5.5s ease-out,object-position .6s ease; }
    .cutscene-frame.focus-narrator img { object-position:center; transform:scale(1.035); }
    .cutscene-frame.focus-boss img { object-position:68% center; transform:scale(1.10); }
    .cutscene-frame.focus-wukong img { object-position:30% center; transform:scale(1.10); }
    .cutscene-frame.slide-enter img { animation:cutsceneReveal .38s ease-out; }
    @keyframes cutsceneReveal { from { opacity:.2; filter:saturate(.7) contrast(1.12); } to { opacity:1; filter:saturate(1.04) contrast(1.03); } }
    .cutscene-art-label { position:absolute; z-index:2; left:16px; bottom:12px; max-width:75%; color:#fff7d6; font:800 13px/1.25 var(--font-body); text-shadow:0 2px 8px #000; }
    #dialogue-speech-card, #buddha-speech-card { flex:0 0 auto; min-height:132px; margin-top:10px; padding:14px 18px; border:1px solid rgba(250,204,21,.65); border-radius:10px; background:rgba(13,8,23,.97); text-align:left; }
    #dialogue-speaker-tag { display:inline-block; margin-bottom:7px; padding:3px 12px; border:1px solid #ef4444; border-radius:999px; background:rgba(239,68,68,.25); color:#fca5a5; font:800 13px/1.35 var(--font-body); }
    #dialogue-text-body { color:#fef9c3; font:650 17px/1.58 var(--font-body); letter-spacing:.01em; }
    .cutscene-controls { display:flex; justify-content:space-between; align-items:center; gap:12px; padding:10px 4px 0; }
    .cutscene-hint { color:#94a3b8; font:700 12px/1.3 var(--font-body); }
    .cutscene-actions { display:flex; gap:10px; }
    .buddha-cinematic-box { width:min(1120px,96vw); }
    .buddha-cutscene-heading { min-width:0; }
    #buddha-cutscene-title { color:#facc15; font:900 20px/1.15 var(--font-title); }
    #buddha-cutscene-subtitle { color:#fef08a; font:700 12px/1.3 var(--font-body); }

    .modal-header {
      text-align: center;
      margin-bottom: 20px;
      position: relative;
      width: 100%;
    }

    .modal-god-portrait {
      width: 120px;
      height: 120px;
      border-radius: 50%;
      border: 3px solid var(--gold-primary);
      box-shadow: 0 0 24px rgba(230, 180, 80, 0.8);
      margin: 0 auto 12px;
      background-size: cover;
      background-position: center;
    }

    .modal-title {
      font-family: var(--font-chinese);
      font-size: 28px;
      font-weight: 900;
      color: var(--gold-light);
      letter-spacing: 2px;
      text-shadow: 0 0 12px rgba(230, 180, 80, 0.7);
    }

    .modal-subtitle {
      font-family: var(--font-chinese);
      font-size: 16px;
      color: #94a3b8;
      margin-top: 4px;
    }

    .modal-quote {
      font-family: var(--font-chinese);
      font-style: italic;
      color: #cbd5e1;
      font-size: 14px;
      margin-top: 8px;
      max-width: 620px;
      margin-left: auto;
      margin-right: auto;
      line-height: 1.5;
    }

    .boon-cards-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      width: 100%;
      margin-top: 10px;
    }

    .shop-resource-summary {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      width: 100%;
      margin: 0 0 10px;
    }

    .shop-resource-item {
      min-width: 0;
      padding: 10px 12px;
      border: 1px solid rgba(250, 204, 21, 0.34);
      border-radius: 8px;
      background: linear-gradient(180deg, rgba(52, 37, 76, 0.86), rgba(18, 13, 31, 0.92));
      text-align: center;
      box-shadow: inset 0 1px rgba(255,255,255,.05);
    }

    .shop-resource-label {
      display: block;
      color: #aeb8cc;
      font: 700 11px var(--font-body);
      line-height: 1.25;
    }

    .shop-resource-value {
      display: block;
      margin-top: 3px;
      color: #fff2a8;
      font: 900 18px var(--font-body);
      overflow-wrap: anywhere;
    }

    .shop-resource-item.health .shop-resource-value { color: #86efac; }
    .shop-resource-item.lives .shop-resource-value { color: #fda4af; }
    .shop-resource-item.merit .shop-resource-value { color: #d8b4fe; }
    .shop-resource-item.critical { border-color: rgba(248, 113, 113, .72); background: rgba(82, 24, 40, .72); }

    .boon-card {
      position: relative;
      background: linear-gradient(180deg, rgba(38, 26, 58, 0.9), rgba(16, 12, 24, 0.95));
      border: 2px solid var(--gold-dark);
      border-radius: 10px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      cursor: pointer;
      transition: all 0.2s;
      min-height: 210px;
      box-shadow: 0 6px 16px rgba(0,0,0,0.8);
      width: 100%;
      color: inherit;
      font: inherit;
      text-align: left;
    }

    .boon-card:hover {
      border-color: var(--gold-primary);
      transform: translateY(-4px);
      box-shadow: 0 0 20px rgba(230, 180, 80, 0.6);
      background: linear-gradient(180deg, rgba(55, 36, 85, 0.95), rgba(22, 16, 35, 0.95));
    }

    .boon-card.unaffordable {
      border-color: #5b5268;
      opacity: .72;
      cursor: not-allowed;
    }

    .boon-card.unaffordable:hover { transform: none; box-shadow: 0 6px 16px rgba(0,0,0,.8); }
    .boon-card.unaffordable .boon-action-btn { background: linear-gradient(180deg, #4b5563, #29313d); border-color: #718096; color: #e2e8f0; }
    .boon-card.purchased-this-visit { border-color:#4ade80; opacity:.68; cursor:not-allowed; }
    .boon-card.purchased-this-visit:hover { transform:none; box-shadow:0 6px 16px rgba(0,0,0,.8); }
    .boon-card.purchased-this-visit .boon-action-btn { background:linear-gradient(180deg,#166534,#14532d); border-color:#4ade80; color:#dcfce7; }

    .tree-node-select { width: 100%; margin-bottom: 10px; padding: 8px 10px; border: 1px solid rgba(250,204,21,.45); border-radius: 6px; background: #151020; color: #fff3bf; font: 700 13px var(--font-body); }
    .permanent-passives { margin: 14px 0; padding: 12px; border: 1px solid rgba(250,204,21,.28); border-radius: 8px; background: rgba(7,5,15,.55); }
    .permanent-passives-title { display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:8px; color:#fff2a8; font:700 15px var(--font-chinese); }
    .local-save-badge { color:#86efac; font:700 10px var(--font-body); white-space:nowrap; }
    .passive-skill-list { display:grid; gap:7px; }
    .passive-skill-row { display:grid; grid-template-columns:1fr auto; gap:8px; align-items:center; padding:8px; border:1px solid rgba(255,255,255,.08); border-radius:6px; background:rgba(32,22,49,.78); }
    .passive-skill-name { color:#f8fafc; font:700 12px var(--font-body); }
    .passive-skill-effect { color:#a7f3d0; font:600 11px var(--font-body); margin-top:2px; }
    .passive-invest-btn { min-width:88px; padding:7px 8px; border:1px solid #d6a43a; border-radius:5px; background:linear-gradient(180deg,#774c12,#3b240b); color:#fff2a8; font:800 11px var(--font-body); cursor:pointer; }
    .passive-invest-btn:disabled { opacity:.45; cursor:not-allowed; }

    .boon-slot-tag {
      align-self: flex-start;
      font-family: var(--font-chinese);
      font-size: 12px;
      font-weight: 700;
      background: rgba(230, 180, 80, 0.2);
      border: 1px solid var(--gold-primary);
      color: var(--gold-light);
      padding: 2px 8px;
      border-radius: 4px;
      margin-bottom: 8px;
    }

    .boon-name {
      font-family: var(--font-chinese);
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 6px;
    }

    .boon-desc {
      font-family: var(--font-body);
      font-size: 12px;
      color: #cbd5e1;
      line-height: 1.5;
      flex-grow: 1;
    }

    .boon-upgrade-preview {
      margin-top: 10px;
      padding: 9px 10px;
      border: 1px solid rgba(251, 113, 133, .24);
      border-radius: 8px;
      background: rgba(251, 113, 133, .10);
      color: #fecdd3;
      font: 700 12px/1.4 var(--font-body);
    }

    .boon-upgrade-heading { color: #fff1f2; font-weight: 900; margin-bottom: 5px; }
    .boon-upgrade-stat { padding: 4px 0; border-top: 1px solid rgba(251, 207, 232, .10); }
    .boon-upgrade-stat:first-of-type { border-top: 0; }
    .boon-upgrade-stat strong { color: #fff7ed; font-weight: 900; }
    .boon-upgrade-note { margin-top: 5px; color: #fde68a; font-size: 11px; }

    .boon-action-btn {
      margin-top: 14px;
      background: linear-gradient(180deg, #b45309, #78350f);
      border: 1px solid var(--gold-light);
      color: #fff;
      font-family: var(--font-chinese);
      font-size: 13px;
      font-weight: 700;
      padding: 6px 12px;
      border-radius: 6px;
      text-align: center;
    }

    /* 72 TRANSFORMATIONS SKILL TREE MODAL */
    .tree-modal-box {
      width: 95vw;
      max-width: 1440px;
      height: 90vh;
      display: flex;
      flex-direction: column;
      background: radial-gradient(circle at center, #1a102a 0%, #0c0816 100%);
      border: 2px solid var(--gold-primary);
      box-shadow: 0 0 50px rgba(230, 180, 80, 0.4);
      padding: 16px 20px;
      overflow: hidden;
      position: relative;
    }

    .tree-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 10px;
      border-bottom: 1px solid rgba(230, 180, 80, 0.3);
    }

    .tree-main-area {
      display: flex;
      flex-grow: 1;
      gap: 16px;
      margin-top: 10px;
      overflow: hidden;
      position: relative;
    }

    .tree-canvas-wrapper {
      flex: 1;
      height: 100%;
      position: relative;
      overflow: hidden;
      border: 1px solid rgba(230, 180, 80, 0.25);
      border-radius: 8px;
      background: #090513;
      cursor: grab;
    }

    .tree-canvas-wrapper:active {
      cursor: grabbing;
    }

    #skill-tree-canvas {
      display: block;
      width: 100%;
      height: 100%;
      touch-action: none;
    }
    .tree-hit-layer { position:absolute; inset:0; z-index:3; pointer-events:none; overflow:hidden; }
    .tree-node-hit { position:absolute; width:46px; height:46px; padding:0; transform:translate(-50%,-50%); border:1px solid transparent; border-radius:50%; background:transparent; color:transparent; pointer-events:auto; cursor:pointer; }
    .tree-node-hit.form-hit { width:58px; height:58px; }
    .tree-node-hit:hover { border-color:rgba(250,204,21,.55); background:rgba(250,204,21,.08); }
    .tree-node-hit:focus-visible { outline:3px solid #fde68a; outline-offset:2px; background:rgba(250,204,21,.14); }

    .tree-inspector-panel {
      width: 380px;
      background: rgba(22, 14, 38, 0.95);
      border: 2px solid var(--gold-dark);
      border-radius: 8px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 6px 20px rgba(0,0,0,0.8);
      overflow: hidden;
    }

    .tree-inspector-scroll { min-height: 0; overflow-y: auto; padding-right: 4px; }
    .tree-inspector-actions { flex: 0 0 auto; padding-top: 10px; background: linear-gradient(180deg, rgba(22,14,38,0), rgba(22,14,38,.98) 22%); }

    .node-header-badge {
      display: inline-block;
      font-family: var(--font-chinese);
      font-size: 12px;
      padding: 3px 10px;
      border-radius: 4px;
      margin-bottom: 8px;
    }

    .node-title {
      font-family: var(--font-chinese);
      font-size: 22px;
      font-weight: 700;
      color: var(--gold-light);
      margin-bottom: 6px;
    }

    .node-rank-badge {
      font-family: var(--font-chinese);
      font-size: 14px;
      color: #4ade80;
      margin-bottom: 12px;
    }

    .node-desc-box {
      font-family: var(--font-body);
      font-size: 13px;
      color: #cbd5e1;
      line-height: 1.6;
      background: rgba(0,0,0,0.4);
      padding: 12px;
      border-radius: 6px;
      border: 1px solid rgba(255,255,255,0.08);
      margin-bottom: 14px;
    }

    .tree-branch-nav {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }

    .branch-btn {
      font-family: var(--font-chinese);
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 4px;
      background: rgba(30, 20, 50, 0.8);
      border: 1px solid rgba(230, 180, 80, 0.4);
      color: #f1e9da;
      cursor: pointer;
      transition: all 0.2s;
    }

    .branch-btn:hover, .branch-btn.active {
      border-color: var(--gold-primary);
      background: rgba(80, 50, 120, 0.9);
      box-shadow: 0 0 10px rgba(230, 180, 80, 0.5);
    }

    .codex-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      width: 100%;
      margin-top: 14px;
      max-height: 480px;
      overflow-y: auto;
      padding-right: 8px;
    }

    .codex-card {
      background: rgba(22, 16, 35, 0.9);
      border: 2px solid var(--gold-dark);
      border-radius: 8px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .codex-god-title {
      font-family: var(--font-chinese);
      font-size: 18px;
      font-weight: 700;
      color: var(--gold-light);
    }

    .codex-boon-list {
      font-family: var(--font-body);
      font-size: 12px;
      color: #cbd5e1;
      line-height: 1.5;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .modal-close-btn {
      margin-top: 20px;
      background: linear-gradient(180deg, #374151, #1f2937);
      border: 1px solid #9ca3af;
      color: #f3f4f6;
      font-family: var(--font-chinese);
      font-size: 14px;
      font-weight: 700;
      padding: 8px 26px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .modal-close-btn:hover {
      background: #4b5563;
      border-color: #fff;
    }

    .gameover-box {
      text-align: center;
      max-width: 620px;
    }

    .gameover-title {
      font-family: var(--font-chinese);
      font-size: 38px;
      font-weight: 900;
      letter-spacing: 3px;
      margin-bottom: 10px;
    }

    .gameover-title.victory {
      color: #facc15;
      text-shadow: 0 0 20px rgba(250, 204, 21, 0.8);
    }

    .gameover-title.defeat {
      color: #ef4444;
      text-shadow: 0 0 20px rgba(239, 68, 68, 0.8);
    }

    .stats-summary {
      background: rgba(14, 10, 20, 0.8);
      border: 1px solid var(--gold-dark);
      border-radius: 8px;
      padding: 16px;
      width: 100%;
      margin: 16px 0;
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-family: var(--font-chinese);
      font-size: 15px;
    }

    .stat-row {
      display: flex;
      justify-content: space-between;
      color: #cbd5e1;
    }

    .stat-val {
      color: var(--gold-light);
      font-weight: 700;
    }

    .action-slot.unavailable {
      opacity: 0.48;
      filter: saturate(0.35);
    }

    button:focus-visible, [tabindex]:focus-visible {
      outline: 3px solid #fff2a8;
      outline-offset: 3px;
      box-shadow: 0 0 0 6px rgba(230, 180, 80, 0.28);
    }

    .start-screen {
      position: absolute;
      inset: 0;
      z-index: 220;
      display: flex;
      align-items: center;
      padding: clamp(24px, 6vw, 92px);
      background-color: #07050d;
      background-size: auto 100%;
      background-position: right center;
      background-repeat: no-repeat;
      isolation: isolate;
      transition: background-image 420ms ease, background-color 420ms ease;
    }

    .start-screen::before {
      content: '';
      position: absolute;
      inset: 0;
      z-index: -1;
      background: linear-gradient(90deg, rgba(5, 4, 11, 0.98) 0%, rgba(7, 5, 13, 0.9) 36%, rgba(7, 5, 13, 0.34) 65%, rgba(7, 5, 13, 0.12) 100%),
                  linear-gradient(0deg, rgba(5, 4, 10, 0.78), transparent 44%);
    }

    .start-panel {
      width: min(610px, 54vw);
      max-height: calc(100dvh - 48px);
      overflow-y: auto;
      padding: clamp(22px, 3vw, 42px);
      border: 1px solid rgba(230, 180, 80, 0.58);
      border-left: 4px solid var(--gold-primary);
      border-radius: 6px 20px 20px 6px;
      background: linear-gradient(135deg, rgba(14, 10, 24, 0.96), rgba(15, 9, 25, 0.72));
      box-shadow: 0 24px 80px rgba(0,0,0,0.68), inset 0 1px rgba(255,255,255,0.06);
      backdrop-filter: blur(12px);
    }

    .start-kicker {
      font: 700 13px var(--font-body);
      color: #f3c96c;
      letter-spacing: 0.28em;
      text-transform: uppercase;
    }

    .title-karma-state {
      display: inline-flex;
      align-items: center;
      width: fit-content;
      max-width: 100%;
      min-height: 34px;
      margin-top: 14px;
      padding: 6px 12px;
      border: 1px solid rgba(250, 204, 21, 0.5);
      border-radius: 999px;
      background: rgba(41, 27, 54, 0.76);
      color: #fff2a8;
      font: 800 13px/1.35 var(--font-body);
      letter-spacing: 0.04em;
      box-shadow: 0 0 18px rgba(230, 180, 80, 0.16);
    }

    .start-screen[data-karma-path="good"] { background-color: #071522; }
    .start-screen[data-karma-path="good"]::before {
      background: linear-gradient(90deg, rgba(4,12,24,0.98) 0%, rgba(7,21,35,0.9) 36%, rgba(7,28,45,0.28) 68%, rgba(255,244,183,0.04) 100%),
                  linear-gradient(0deg, rgba(3,12,24,0.7), transparent 44%);
    }
    .start-screen[data-karma-path="good"] .start-panel {
      border-color: rgba(125, 211, 252, 0.7);
      border-left-color: #fef08a;
      box-shadow: 0 24px 80px rgba(0,0,0,0.58), 0 0 34px rgba(96,165,250,0.14), inset 0 1px rgba(255,255,255,0.08);
    }
    .title-karma-state.good {
      border-color: rgba(125,211,252,0.72);
      background: rgba(8,47,73,0.78);
      color: #e0f2fe;
      box-shadow: 0 0 20px rgba(96,165,250,0.3);
    }

    .start-screen[data-karma-path="evil"] { background-color: #10030e; }
    .start-screen[data-karma-path="evil"]::before {
      background: linear-gradient(90deg, rgba(12,2,13,0.99) 0%, rgba(21,3,20,0.92) 36%, rgba(45,4,35,0.34) 67%, rgba(46,5,15,0.1) 100%),
                  linear-gradient(0deg, rgba(12,2,12,0.78), transparent 44%);
    }
    .start-screen[data-karma-path="evil"] .start-panel {
      border-color: rgba(192,38,211,0.68);
      border-left-color: #ef4444;
      box-shadow: 0 24px 80px rgba(0,0,0,0.72), 0 0 38px rgba(168,85,247,0.16), inset 0 1px rgba(255,255,255,0.05);
    }
    .title-karma-state.evil {
      border-color: rgba(244,63,94,0.72);
      background: rgba(64,8,42,0.8);
      color: #fecdd3;
      box-shadow: 0 0 20px rgba(225,29,72,0.3);
    }

    .start-title {
      margin-top: 12px;
      font: 900 clamp(40px, 5vw, 72px)/0.96 var(--font-chinese);
      color: #fff2a8;
      letter-spacing: 0.06em;
      text-shadow: 0 0 28px rgba(230,180,80,0.46), 0 3px 0 #6f390f;
    }

    .start-subtitle {
      margin-top: 16px;
      max-width: 520px;
      font: 700 clamp(14px, 1.4vw, 18px)/1.65 var(--font-body);
      color: #d7d4df;
    }

    .start-controls {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px 18px;
      margin: 24px 0;
      color: #e9e5ef;
      font: 600 13px/1.45 var(--font-body);
    }

    .start-controls kbd {
      display: inline-flex;
      min-width: 42px;
      justify-content: center;
      margin-right: 8px;
      padding: 3px 7px;
      border: 1px solid #b98735;
      border-bottom-width: 3px;
      border-radius: 5px;
      background: #181120;
      color: #fff2a8;
      font: 700 11px var(--font-body);
    }

    .hero-choice { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 9px; margin: 12px 0 16px; }
    .hero-option { min-height: 54px; padding: 9px 12px; border: 1px solid rgba(230,180,80,.42); border-radius: 9px; background: rgba(18,12,30,.84); color: #eee8f5; cursor: pointer; text-align: left; font: 800 13px/1.25 var(--font-body); }
    .hero-option span { display: block; margin-top: 3px; color: #a9a1b5; font-size: 11px; font-weight: 600; }
    .hero-option.active { border-color: #facc15; color: #fff2a8; background: linear-gradient(135deg, rgba(132,75,11,.7), rgba(46,27,62,.82)); box-shadow: 0 0 18px rgba(250,204,21,.18); }
    .hero-option:disabled, .start-primary:disabled { cursor: not-allowed; opacity: .5; filter: grayscale(.55); }
    .start-actions { display: flex; flex-wrap: wrap; gap: 10px; }
    .language-choice { display: flex; gap: 8px; margin: 12px 0 4px; align-items: center; color: #d8cbe8; font: 700 13px var(--font-body); }
    .language-choice button { min-height: 38px; padding: 7px 14px; border: 1px solid rgba(230,180,80,.48); border-radius: 9px; background: rgba(18,12,30,.86); color: #e9ddf6; font: 800 13px var(--font-body); cursor: pointer; }
    .language-choice button.active { border-color: #facc15; color: #fff2a8; background: rgba(145,88,12,.52); box-shadow: 0 0 14px rgba(250,204,21,.22); }
    .start-primary {
      min-height: 48px;
      padding: 11px 26px;
      border: 1px solid #ffe59a;
      border-radius: 7px;
      background: linear-gradient(180deg, #d98b16, #86400d);
      color: #fffdf2;
      cursor: pointer;
      font: 900 18px var(--font-chinese);
      letter-spacing: 0.08em;
      box-shadow: 0 8px 28px rgba(217,139,22,0.28);
    }

    .start-secondary {
      min-height: 48px;
      padding: 11px 18px;
      border: 1px solid #6f5b82;
      border-radius: 7px;
      background: rgba(22,15,34,0.88);
      color: #eee8f5;
      cursor: pointer;
      font: 700 14px var(--font-body);
    }

    .start-status { margin-top: 14px; color: #9f97ad; font: 600 12px var(--font-body); }

    .tutorial-card {
      position: absolute;
      left: 50%;
      bottom: 124px;
      z-index: 35;
      display: none;
      width: min(560px, calc(100vw - 32px));
      transform: translateX(-50%);
      padding: 11px 18px;
      border: 1px solid rgba(230,180,80,0.65);
      border-radius: 999px;
      background: rgba(8,6,14,0.9);
      color: #fff4c4;
      text-align: center;
      font: 700 13px var(--font-body);
      box-shadow: 0 8px 30px rgba(0,0,0,0.6);
      pointer-events: none;
    }

    .pause-box { width: min(520px, calc(100vw - 32px)); text-align: center; }
    .pause-actions { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-top: 20px; }
    .pause-checkpoint-info { margin:14px 0 4px; padding:11px 14px; border:1px solid rgba(96,165,250,.48); border-radius:9px; background:rgba(15,35,66,.55); color:#dbeafe; font:700 13px/1.5 var(--font-body); }
    .save-exit-button { background:linear-gradient(180deg,#2563eb,#1e3a8a); border-color:#93c5fd; }

    .touch-controls { display: none; }

    @media (max-width: 1180px) {
      #ui-layer { padding: 12px; }
      .player-bars { width: min(32vw, 300px); flex-shrink: 0; }
      .hero-title, .chamber-subtitle { display: none; }
      .top-center-hud { position: absolute; top: 10px; left: 50%; width: min(34vw, 390px); transform: translateX(-50%); }
      .chamber-title { font-size: 16px; letter-spacing: 0; white-space: normal; overflow-wrap: anywhere; line-height: 1.2; }
      .currency-panel { max-width: 31vw; gap: 7px; padding: 5px 8px; flex-wrap: wrap; justify-content: flex-end; }
      .boon-cards-grid { grid-template-columns: repeat(auto-fit, minmax(min(230px, 100%), 1fr)); }
      .modal-overlay { padding: 12px; overflow: auto; }
      .modal-box { width: min(880px, calc(100vw - 24px)); }
    }

    @media (max-width: 900px), (hover: none) and (pointer: coarse) {
      #ui-layer { padding: max(10px, env(safe-area-inset-top)) max(10px, env(safe-area-inset-right)) max(10px, env(safe-area-inset-bottom)) max(10px, env(safe-area-inset-left)); }
      .top-hud { gap: 8px; }
      .player-bars { width: min(50vw, 300px); flex-shrink: 0; }
      .hero-title, .chamber-subtitle { display: none; }
      .hero-name { font-size: 16px; }
      .bar-wrapper { height: 20px; }
      .bar-text { font-size: 10px; padding: 0 6px; }
      .top-center-hud { position: absolute; top: 112px; left: 12px; right: 12px; width: auto; transform: none; }
      .chamber-title { font-size: 15px; letter-spacing: 0; }
      .banner-clear-alert { max-width: calc(100vw - 24px); border-radius: 10px; }
      .currency-panel { gap: 8px; padding: 5px 8px; flex-wrap: wrap; justify-content: flex-end; max-width: 34vw; }
      .currency-item { font-size: 11px; }
      .currency-item span:first-child { font-size: 0; }
      .currency-item span:first-child::first-letter { font-size: 13px; }
      .bottom-hud { align-items: flex-end; }
      .action-slots { display: none; }
      .quick-buttons { position: absolute; right: max(12px, env(safe-area-inset-right)); bottom: max(154px, calc(env(safe-area-inset-bottom) + 154px)); margin: 0; }
      .quick-buttons .btn-hud { padding: 7px 9px; min-width: 44px; min-height: 44px; font-size: 0; }
      .quick-buttons .btn-hud::before { font-size: 18px; line-height: 1; }
      .quick-buttons .btn-hud:nth-child(1)::before { content: '📜'; }
      .quick-buttons .btn-hud:nth-child(2)::before { content: '📖'; }
      .quick-buttons .btn-hud:nth-child(3)::before { content: '⚔'; }
      .quick-buttons .btn-hud:nth-child(4)::before { content: '⏸'; }
      .boss-bar-container { width: min(88vw, 620px); top: 160px; }
      .boon-cards-grid { grid-template-columns: 1fr; }
      .shop-resource-summary { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .modal-box { padding: 18px; max-height: 94dvh; }
      .tree-modal-box { width: 98vw; height: 96dvh; padding: 10px; overflow-y: auto; }
      .tree-header { align-items: flex-start; gap: 8px; flex-direction: column; width: 100%; }
      .tree-header > div:last-child { width: 100%; flex-wrap: wrap; gap: 8px !important; }
      .tree-branch-nav { width: 100%; }
      .tree-header .modal-subtitle { display: none; }
      .tree-main-area { flex-direction: column; min-height: 0; overflow-y: auto; }
      .tree-canvas-wrapper { min-height: 46dvh; }
      .tree-inspector-panel { width: 100%; min-height: 280px; }
      .start-screen { align-items: flex-end; padding: 16px; background-position: right center; background-size: auto 100%; }
      .start-screen::before { background: linear-gradient(0deg, rgba(5,4,11,0.99) 0%, rgba(5,4,11,0.92) 55%, rgba(5,4,11,0.2) 100%); }
      .start-panel { width: 100%; max-height: 72dvh; overflow-y: auto; padding: 20px; }
      .start-title { font-size: clamp(34px, 12vw, 52px); }
      .start-subtitle { font-size: 13px; }
      .start-controls { grid-template-columns: 1fr 1fr; margin: 16px 0; font-size: 11px; }
      .touch-controls { position: absolute; inset: 0; z-index: 30; display: block; pointer-events: none; }
      .touch-stick { position: absolute; left: max(18px, env(safe-area-inset-left)); bottom: max(24px, env(safe-area-inset-bottom)); width: 118px; height: 118px; border: 2px solid rgba(255,242,168,0.45); border-radius: 50%; background: rgba(10,7,18,0.42); pointer-events: auto; touch-action: none; }
      .touch-stick-knob { position: absolute; left: 37px; top: 37px; width: 44px; height: 44px; border-radius: 50%; background: rgba(230,180,80,0.82); box-shadow: 0 0 20px rgba(230,180,80,0.5); transform: translate(0,0); }
      .touch-actions { position: absolute; right: max(16px, env(safe-area-inset-right)); bottom: max(20px, env(safe-area-inset-bottom)); display: grid; grid-template-columns: repeat(3, 54px); gap: 8px; align-items: end; pointer-events: auto; }
      .touch-action { width: 54px; height: 54px; border: 1px solid rgba(255,242,168,0.72); border-radius: 50%; background: rgba(35,21,48,0.84); color: #fff3bf; font: 900 12px var(--font-body); box-shadow: 0 4px 16px rgba(0,0,0,0.55); touch-action: manipulation; }
      .touch-action.primary { width: 66px; height: 66px; margin-left: -6px; background: linear-gradient(180deg, rgba(201,110,15,0.96), rgba(111,43,12,0.96)); font-size: 14px; }
      .tutorial-card { bottom: 220px; border-radius: 10px; }
      .boss-dialogue-box { width:98vw; height:96dvh; max-height:96dvh; padding:9px; }
      .cutscene-topbar { min-height:44px; grid-template-columns:minmax(0,1fr) auto; gap:8px; padding:2px 4px 7px; }
      #dialogue-mode-title { display:none; }
      #dialogue-boss-name { font-size:16px; }
      #dialogue-boss-title { font-size:10px; }
      .cutscene-frame { flex:0 0 auto; width:100%; aspect-ratio:16/9; }
      .cutscene-art-label { left:9px; bottom:7px; max-width:88%; font-size:10px; }
      #dialogue-speech-card, #buddha-speech-card { min-height:0; margin-top:7px; padding:10px 12px; }
      #dialogue-text-body { font-size:14px; line-height:1.48; }
      .cutscene-controls { flex-direction:column; align-items:stretch; gap:7px; padding-top:7px; }
      .cutscene-hint { display:none; }
      .cutscene-actions { display:grid; grid-template-columns:1fr auto; }
      .cutscene-actions .btn-hud { justify-content:center; padding:9px 12px !important; font-size:13px !important; }
      #buddha-cutscene-title { font-size:15px; }
      #buddha-cutscene-subtitle { font-size:10px; }
    }

    @media (max-width: 600px) {
      html[lang="en"] .hero-name { font-size: 13px; letter-spacing: 0; }
      .codex-grid { grid-template-columns: 1fr; }
      .start-actions > button { width: 100%; }
      .hero-choice { grid-template-columns: 1fr; }
      .modal-title { font-size: 22px; letter-spacing: .5px; }
      .start-panel { max-height: 86dvh; }
      .player-bars { width: min(58vw, 230px); }
      .currency-panel { max-width: 38vw; }
    }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { animation-duration: 0.001ms !important; animation-iteration-count: 1 !important; transition-duration: 0.001ms !important; }
    }

    /* Persistent karmic alignment progression. */
    .alignment-meter { width:100%; border:0; color:#f8fafc; background:transparent; font:700 10px var(--font-body); cursor:pointer; pointer-events:auto; }
    .alignment-labels { display:grid; grid-template-columns:1fr 1fr 1fr; margin-bottom:2px; opacity:.9; }
    .alignment-labels span:first-child { color:#f87171; text-align:left; }
    .alignment-labels span:nth-child(2) { color:#d8b4fe; text-align:center; }
    .alignment-labels span:last-child { color:#93c5fd; text-align:right; }
    .alignment-track { display:block; height:12px; position:relative; overflow:hidden; border:1px solid rgba(255,255,255,.34); border-radius:999px; background:linear-gradient(90deg,#2a0716,#261736 46%,#201f35 54%,#09263b); box-shadow:inset 0 1px 5px rgba(0,0,0,.8); }
    .alignment-center-line { position:absolute; left:50%; top:0; bottom:0; width:2px; background:#fff; opacity:.65; }
    .alignment-fill { position:absolute; top:1px; bottom:1px; width:0; transition:width .35s,left .35s; }
    #alignment-evil-fill { right:50%; background:linear-gradient(90deg,#7f1d1d,#a855f7); box-shadow:0 0 10px #ef4444; }
    #alignment-good-fill { left:50%; background:linear-gradient(90deg,#60a5fa,#fde68a); box-shadow:0 0 10px #93c5fd; }
    .alignment-marker { position:absolute; top:50%; left:50%; width:10px; height:10px; border-radius:50%; background:#fff; border:2px solid #facc15; transform:translate(-50%,-50%); box-shadow:0 0 10px #fff; transition:left .35s; }
    .alignment-readout { margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
    .alignment-modal-box { width:min(1180px,96vw); height:min(860px,92dvh); overflow:hidden; padding:20px; }
    .alignment-summary { display:grid; grid-template-columns:120px 1fr; align-items:center; gap:16px; margin-bottom:14px; }
    .alignment-portrait { width:120px; height:120px; background-repeat:no-repeat; background-size:300% 100%; filter:drop-shadow(0 0 16px currentColor); }
    .alignment-portrait.good { color:#93c5fd; background-position:0% 50%; }
    .alignment-portrait.neutral { color:#facc15; background-position:50% 50%; }
    .alignment-portrait.evil { color:#a855f7; background-position:100% 50%; }
    .alignment-tree-tabs { display:flex; gap:8px; flex-wrap:wrap; margin:10px 0; }
    .alignment-tree-tabs button { flex:1; min-width:130px; justify-content:center; }
    .alignment-skill-grid { height:calc(100% - 245px); overflow:auto; display:grid; grid-template-columns:repeat(3,minmax(260px,1fr)); gap:12px; padding:4px 6px 20px 2px; }
    .alignment-path-column { border:1px solid rgba(255,255,255,.16); border-radius:12px; padding:12px; background:rgba(6,4,13,.64); }
    .alignment-path-column.good { border-color:rgba(96,165,250,.5); }
    .alignment-path-column.neutral { border-color:rgba(250,204,21,.45); }
    .alignment-path-column.evil { border-color:rgba(168,85,247,.55); }
    .alignment-path-title { position:sticky; top:-12px; z-index:2; padding:10px; margin:-12px -12px 10px; background:rgba(12,8,23,.96); font:900 20px var(--font-title); }
    .alignment-skill { margin:9px 0; padding:11px; border:1px solid #475569; border-radius:9px; background:rgba(15,12,27,.9); }
    .alignment-skill.active { border-color:#4ade80; box-shadow:0 0 10px rgba(74,222,128,.2); }
    .alignment-skill.dormant { opacity:.62; border-color:#be123c; }
    .alignment-skill.locked { opacity:.48; }
    .alignment-skill-name { font:900 15px var(--font-title); color:#fef3c7; }
    .alignment-skill-meta { margin:3px 0 6px; color:#c4b5fd; font-size:11px; }
    .alignment-skill-desc { color:#cbd5e1; font:600 12px/1.45 var(--font-body); min-height:52px; }
    .neutral-rank-track { position:relative; height:8px; margin:8px 0 2px; overflow:hidden; border:1px solid rgba(250,204,21,.45); border-radius:999px; background:#090613; }
    .neutral-rank-track > i { display:block; height:100%; background:linear-gradient(90deg,#f8fafc 0%,#facc15 48%,#8b5cf6 52%,#312e81 100%); box-shadow:0 0 10px rgba(250,204,21,.55); transition:width .22s ease; }
    .neutral-rank-milestones { display:flex; justify-content:space-between; color:#a5b4fc; font:700 9px/1.2 var(--font-body); }
    .alignment-skill button { width:100%; justify-content:center; margin-top:8px; min-height:38px; }
    .combo-chain-readout { position:absolute; left:50%; bottom:116px; transform:translateX(-50%); min-width:210px; padding:6px 12px; border:1px solid rgba(250,204,21,.55); border-radius:999px; background:rgba(8,5,16,.82); color:#fef3c7; text-align:center; font:800 12px var(--font-body); letter-spacing:1.5px; opacity:.84; transition:transform .16s ease, border-color .16s ease, color .16s ease; }
    .combo-chain-readout.complete { transform:translateX(-50%) scale(1.06); border-color:#facc15; color:#ffffff; box-shadow:0 0 18px rgba(250,204,21,.38); }
    .combo-modal-box { width:min(980px,95vw); max-height:90dvh; overflow:auto; }
    .combo-help { margin:8px auto 16px; max-width:780px; color:#cbd5e1; font:650 14px/1.55 var(--font-body); text-align:center; }
    .combo-list-grid { display:grid; grid-template-columns:repeat(2,minmax(280px,1fr)); gap:12px; }
    .combo-card { padding:14px; border:1px solid rgba(250,204,21,.38); border-radius:11px; background:linear-gradient(145deg,rgba(29,20,45,.95),rgba(10,7,18,.95)); }
    .combo-card.good { border-color:rgba(96,165,250,.65); }
    .combo-card.evil { border-color:rgba(192,38,211,.65); }
    .combo-card-name { color:#fef3c7; font:900 18px var(--font-title); }
    .combo-badge { display:inline-block; margin-left:8px; padding:2px 7px; border:1px solid #4ade80; border-radius:999px; color:#bbf7d0; font:800 10px var(--font-body); vertical-align:middle; }
    .combo-pattern { display:flex; flex-wrap:wrap; gap:6px; margin:8px 0; }
    .combo-token { min-width:38px; padding:4px 8px; border:1px solid #facc15; border-radius:6px; background:#26162f; color:#fff7ae; text-align:center; font:900 12px var(--font-body); }
    .combo-token.right { border-color:#c084fc; background:#2e1065; color:#e9d5ff; }
    .combo-card-desc { color:#cbd5e1; font:600 13px/1.45 var(--font-body); }
    .erlang-tree-box { width:min(1180px,96vw); max-height:92dvh; overflow:auto; border-color:#60a5fa; background:linear-gradient(155deg,#071526,#120b2b 55%,#07111f); }
    .erlang-tree-header { display:flex; justify-content:space-between; gap:18px; align-items:flex-start; margin-bottom:16px; }
    .erlang-tree-merit { flex:0 0 auto; padding:8px 14px; border:1px solid #60a5fa; border-radius:8px; background:rgba(37,99,235,.18); color:#dbeafe; font:900 14px var(--font-body); }
    .erlang-tree-grid { display:grid; grid-template-columns:repeat(3,minmax(260px,1fr)); gap:14px; }
    .erlang-branch { padding:12px; border:1px solid rgba(96,165,250,.42); border-radius:12px; background:rgba(4,13,28,.72); }
    .erlang-branch-title { position:sticky; top:-1px; z-index:2; margin:-4px -4px 10px; padding:9px; border-radius:8px; background:#102044; color:#bfdbfe; font:900 18px var(--font-title); }
    .erlang-branch-title small { display:block; margin-top:3px; color:#93c5fd; font:650 11px/1.35 var(--font-body); }
    .erlang-skill-card { margin:9px 0; padding:11px; border:1px solid rgba(147,197,253,.28); border-radius:9px; background:rgba(15,23,42,.86); }
    .erlang-skill-card.active { border-color:#22d3ee; box-shadow:0 0 13px rgba(34,211,238,.16); }
    .erlang-skill-card.locked { opacity:.58; }
    .erlang-skill-name { color:#f8fafc; font:900 15px var(--font-title); }
    .erlang-skill-meta { margin:3px 0 6px; color:#93c5fd; font:800 11px var(--font-body); }
    .erlang-skill-desc { min-height:48px; color:#cbd5e1; font:600 12px/1.45 var(--font-body); }
    .erlang-skill-current { margin-top:7px; padding:7px 8px; border-radius:7px; background:rgba(30,64,175,.18); color:#a5f3fc; font:700 11px/1.4 var(--font-body); }
    .erlang-rank-track { height:6px; margin:7px 0; overflow:hidden; border-radius:999px; background:#172554; }
    .erlang-rank-track i { display:block; height:100%; background:linear-gradient(90deg,#2563eb,#22d3ee,#facc15); }
    .erlang-skill-card .btn-hud { width:100%; margin-top:8px; padding:7px; font-size:12px; }
    .boss-outcome-box { width:min(980px,94vw); max-height:92dvh; overflow:auto; text-align:center; border-color:#c084fc; }
    .boss-outcome-story { margin:12px auto 18px; max-width:820px; padding:14px 18px; border:1px solid rgba(250,204,21,.4); border-radius:10px; background:rgba(20,15,35,.86); font:600 15px/1.65 var(--font-body); color:#fef9c3; }
    .boss-outcome-lock { min-height:34px; margin:10px auto 12px; padding:7px 12px; border:1px solid rgba(248,113,113,.48); border-radius:9px; background:rgba(69,10,10,.42); color:#fecaca; font:800 13px/1.35 var(--font-body); }
    .boss-outcome-lock.ready { border-color:rgba(74,222,128,.48); background:rgba(5,46,22,.42); color:#bbf7d0; }
    .boss-outcome-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
    .outcome-choice { min-height:190px; padding:16px; text-align:left; border:2px solid; border-radius:12px; color:#f8fafc; cursor:pointer; font-family:var(--font-body); }
    .outcome-choice:disabled { cursor:not-allowed; pointer-events:none; opacity:.48; filter:grayscale(.38); transform:none; box-shadow:none; }
    .outcome-choice.good { background:linear-gradient(160deg,#102a43,#12344d); border-color:#60a5fa; }
    .outcome-choice.neutral { background:linear-gradient(160deg,#30260b,#2a1d0d); border-color:#facc15; }
    .outcome-choice.evil { background:linear-gradient(160deg,#3b0a19,#25103c); border-color:#a855f7; }
    .outcome-choice strong { display:block; font:900 19px var(--font-title); margin-bottom:8px; }
    .outcome-choice small { display:block; margin-top:10px; color:#e2e8f0; font-size:12px; }
    @media (max-width:900px) {
      .alignment-skill-grid { grid-template-columns:1fr; height:calc(100% - 230px); }
      .boss-outcome-grid { grid-template-columns:1fr; }
      .outcome-choice { min-height:130px; }
      .alignment-summary { grid-template-columns:84px 1fr; }
      .alignment-portrait { width:84px; height:84px; }
      .quick-buttons .btn-hud:nth-child(1)::before { content:'☯'; }
      .quick-buttons .btn-hud:nth-child(2)::before { content:'📜'; }
      .quick-buttons .btn-hud:nth-child(3)::before { content:'📖'; }
      .quick-buttons .btn-hud:nth-child(4)::before { content:'⚔'; }
      .quick-buttons .btn-hud:nth-child(5)::before { content:'⏸'; }
      .combo-list-grid { grid-template-columns:1fr; }
      .erlang-tree-grid { grid-template-columns:1fr; }
      .erlang-tree-header { flex-direction:column; }
    }
  </style>
</head>
<body>
  <div id="game-container">
    <canvas id="gameCanvas" role="img" tabindex="0" aria-label="西游记动作战场：使用方向键移动，鼠标与快捷键战斗。">您的浏览器需要支持 HTML5 Canvas 才能游玩。</canvas>

    <section id="start-screen" class="start-screen" role="dialog" aria-modal="true" aria-labelledby="start-title">
      <div class="start-panel">
        <div class="start-kicker">Journey to the West · Action Roguelite</div>
        <div id="title-karma-state" class="title-karma-state neutral" aria-live="polite">☯ 中道未定 · 因果 0</div>
        <h1 id="start-title" class="start-title">西游记 · 齐天西行</h1>
        <p class="start-subtitle">从花果山石猴启程，求变化、取金箍棒、大闹天宫，再护送唐三藏一路西行至灵山成佛。完整一百章连续推进，不分篇章重开。</p>
        <div class="language-choice" aria-label="语言选择">
          <span>语言 / Language</span>
          <button id="lang-zh-btn" type="button" onclick="setGameLanguage('zh')">中文</button>
          <button id="lang-en-btn" type="button" onclick="setGameLanguage('en')">English</button>
        </div>
        <div class="start-controls" aria-label="核心操作">
          <div><kbd>WASD</kbd>移动</div>
          <div><kbd>左键 + 右键</kbd>混合棍法连招</div>
          <div><kbd>Q / 单独右键</kbd>飞棒去回</div>
          <div><kbd>E</kbd>吹毛成兵</div>
          <div><kbd>空格</kbd>闪避</div>
          <div><kbd>R/F · G</kbd>变身 · 觉醒</div>
          <div><kbd>Esc</kbd>菜单 / 保存退出</div>
        </div>
        <div id="hero-choice" class="hero-choice" aria-label="可玩角色选择">
          <button id="hero-wukong-btn" class="hero-option active" type="button" onclick="selectPlayableHero('wukong')">🐒 孙悟空<span>金箍棒 · 七十二变 · 吹毛成兵</span></button>
          <button id="hero-erlang-btn" class="hero-option" type="button" onclick="selectPlayableHero('erlang')" disabled>👁 二郎神 · 尚未解锁<span>通关完整百章西游后解锁天眼、三尖枪与哮天犬</span></button>
        </div>
        <div class="start-actions">
          <button id="start-game-btn" class="start-primary" type="button" onclick="startOrContinueJourney()">西游全篇 · 第 1–100 章</button>
          <button id="start-fresh-btn" class="start-secondary" type="button" onclick="startFreshJourney()" hidden>从第 1 章重新开始</button>
          <button id="start-ngplus-btn" class="start-primary" type="button" onclick="startNewGamePlus()" disabled>✦ 新游戏+ · 天镜再战 (1–100)</button>
          <button id="training-title-btn" class="start-secondary" type="button" onclick="openAltarFromTitle()">七十二变</button>
          <button id="title-audio-btn" class="start-secondary" type="button" onclick="toggleMute()">🔊 音效开启</button>
        </div>
        <div id="run-checkpoint-status" class="start-status" aria-live="polite"></div>
        <div id="asset-load-status" class="start-status" aria-live="polite">正在召集天兵神将…</div>
      </div>
    </section>

    <div id="ui-layer">
      <div class="top-hud">
        <div class="player-bars">
          <div class="hero-tag">
            <span class="hero-name">齐天大圣 · 孙悟空</span>
            <span class="hero-title" id="weapon-style-title">如意金箍棒 · 一万三千五百斤</span>
          </div>
          <div class="bar-wrapper">
            <div id="hp-bar" class="bar-fill health" style="width: 100%;"></div>
            <div class="bar-text"><span id="hp-label">气血值 (生命) · 🛡 0</span><span id="hp-text">100 / 100</span></div>
          </div>
          <div class="bar-wrapper">
            <div id="qi-bar" class="bar-fill qi" style="width: 100%;"></div>
            <div class="bar-text"><span>混元真气 (法力)</span><span id="qi-text">50 / 50</span></div>
          </div>
          <div class="bar-wrapper" style="height: 16px;">
            <div id="awaken-bar" class="bar-fill awakening" style="width: 0%;"></div>
            <div class="bar-text" style="font-size: 10px;"><span>大闹天宫觉醒</span><span id="awaken-text">蓄力中 · 满后按 [G]</span></div>
          </div>
          <button id="alignment-meter" class="alignment-meter" type="button" onclick="openAlignmentTree()" aria-label="善恶中道因果平衡与技能树">
            <span class="alignment-labels"><span>恶 −100</span><span>中道 0</span><span>善 +100</span></span>
            <span class="alignment-track"><span id="alignment-evil-fill" class="alignment-fill"></span><span id="alignment-good-fill" class="alignment-fill"></span><span class="alignment-center-line"></span><span id="alignment-marker" class="alignment-marker"></span></span>
            <span id="alignment-readout" class="alignment-readout">中道 · 因果 0</span>
          </button>
        </div>

        <div class="top-center-hud">
          <div id="chamber-name" class="chamber-title">花果山·水帘洞 · 第 1 章 / 100 章</div>
          <div id="chamber-sub" class="chamber-subtitle">仙石初辟悟大道 · 降妖除魔登九霄</div>
          <div id="chamber-clear-alert" class="banner-clear-alert">✨ 本章战罢！请走向阵门继续 · 战后气血与真气回复已暂停 ✨</div>
        </div>

        <div class="currency-panel">
          <div class="currency-item gold">
            <span>🪙 灵石:</span>
            <span id="gold-val">0</span>
          </div>
          <div class="currency-item ashes">
            <span>✨ 功德:</span>
            <span id="ashes-val">0</span>
          </div>
          <div class="currency-item peaches">
            <span>🍑 蟠桃:</span>
            <span id="peaches-val">0</span>
          </div>
          <div class="currency-item lives">
            <span>❤️ 金身:</span>
            <span id="lives-val">1</span>
          </div>
        </div>
      </div>

      <div id="boss-hud" class="boss-bar-container">
        <div id="boss-name-text" class="boss-name">大日雷音寺·大日如来佛祖 (如来神掌)</div>
        <div class="boss-bar-wrapper">
          <div id="boss-bar-fill" class="boss-bar-fill" style="width: 100%;"></div>
        </div>
      </div>

      <div class="bottom-hud">
        <div class="action-slots">
          <div class="action-slot active" id="slot-attack">
            <div class="key-badge">左键 + 右键</div>
            <div class="slot-label">金箍混合棍法</div>
            <div class="slot-boon" id="boon-tag-attack">按 [C] 查看连招</div>
          </div>
          <div class="action-slot" id="slot-special">
            <div class="key-badge">Q / 单独右键</div>
            <div class="slot-label">如意飞棒</div>
            <div class="slot-boon" id="boon-tag-special">去回双击</div>
          </div>
          <div class="action-slot" id="slot-cast">
            <div class="key-badge">E/法术 (75真气)</div>
            <div class="slot-label">吹毛成兵</div>
            <div class="slot-boon" id="boon-tag-cast">猴王分身</div>
          </div>
          <div class="action-slot" id="slot-dash">
            <div class="key-badge">空格/闪避</div>
            <div class="slot-label">筋斗云遁</div>
            <div class="slot-boon" id="boon-tag-dash">浮光掠影</div>
          </div>
          <div class="action-slot" id="slot-hex">
            <div class="key-badge">R/F/神兽化身</div>
            <div class="slot-label" id="slot-hex-label">苍龙真形</div>
            <div class="slot-boon" id="boon-tag-hex">水雷御海</div>
          </div>
        </div>

        <div class="quick-buttons">
          <button id="alignment-hud-btn" class="btn-hud" onclick="openAlignmentTree()">☯ 因果善恶神通树</button>
          <button id="training-hud-btn" class="btn-hud" onclick="openAltarOfTransformations()">📜 七十二变地煞树</button>
          <button class="btn-hud" onclick="openSkillCodex()">📖 西游万神伏魔录</button>
          <button id="combo-hud-btn" class="btn-hud" onclick="openComboList()">⚔ [C] 金箍棒连招谱</button>
          <button class="btn-hud" onclick="showPauseMenu()">⏸ [Esc] 菜单 · 保存退出</button>
        </div>
      </div>
    </div>

    <div id="combo-chain-readout" class="combo-chain-readout" aria-live="polite">连招输入：—</div>

    <div id="tutorial-card" class="tutorial-card" role="status" aria-live="polite">天光护体 10 秒 · 左右键混合连招 · 按 [C] 查看连招谱 · 按 [Esc] 打开菜单与保存退出</div>

    <div id="touch-controls" class="touch-controls" aria-label="触控操作">
      <div id="touch-stick" class="touch-stick" aria-label="移动摇杆"><div id="touch-stick-knob" class="touch-stick-knob"></div></div>
      <div class="touch-actions">
        <button class="touch-action" type="button" data-touch-action="dash">闪</button>
        <button class="touch-action" type="button" data-touch-action="special">飞</button>
        <button class="touch-action primary" type="button" data-touch-action="attack">攻</button>
        <button class="touch-action" type="button" data-touch-action="cast">法</button>
        <button class="touch-action" type="button" data-touch-action="transform">变</button>
        <button class="touch-action" type="button" data-touch-action="awaken">觉</button>
      </div>
    </div>

    <!-- Modals -->
    <div id="boon-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-label="仙圣赐福">
      <div class="modal-box">
        <div class="modal-header">
          <div id="god-portrait" class="modal-god-portrait"></div>
          <div id="god-name" class="modal-title">二郎显圣真君·杨戬</div>
          <div id="god-title" class="modal-subtitle">天眼洞察 · 执掌九天刑罚神律</div>
          <div id="god-quote" class="modal-quote">“泼猴，接本君三尖两刃枪之威！荡尽三界妖邪，休得阻碍西行正道！”</div>
        </div>
        <div id="boon-choices-container" class="boon-cards-grid"></div>
      </div>
    </div>

    <div id="pom-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-label="蟠桃强化">
      <div class="modal-box">
        <div class="modal-header">
          <div id="peach-modal-icon" style="width: 110px; height: 110px; border-radius: 50%; border: 3px solid var(--peach-pink); box-shadow: 0 0 24px rgba(251, 113, 133, 0.8); margin: 0 auto 12px; background-size: 200%; background-position: 0 0;"></div>
          <div class="modal-title" style="color: var(--peach-pink);">王母天庭蟠桃盛宴 (仙桃延寿)</div>
          <div class="modal-subtitle">三千年一熟，人吃了体健身轻，道法大进</div>
          <div class="modal-quote">“服食一枚仙桃，顿增三千年道行功力！请选择一项已修习的神通提升品阶境界。”</div>
        </div>
        <div id="pom-choices-container" class="boon-cards-grid"></div>
      </div>
    </div>

    <div id="shop-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-label="龙宫珍宝阁">
      <div class="modal-box">
        <div class="modal-header">
          <div style="font-size: 52px; margin-bottom: 8px;">🏮</div>
          <div class="modal-title" style="color: #facc15;">东海龙宫珍宝阁与土地神坛</div>
          <div class="modal-subtitle">以灵石换取仙家丹药与通天至宝</div>
        </div>
        <div id="shop-resource-summary" class="shop-resource-summary" aria-live="polite" aria-label="当前资源">
          <div class="shop-resource-item currency">
            <span class="shop-resource-label" id="shop-gold-label">🪙 当前灵石</span>
            <strong class="shop-resource-value" id="shop-gold-value">0</strong>
          </div>
          <div class="shop-resource-item health" id="shop-health-item">
            <span class="shop-resource-label" id="shop-health-label">❤️ 当前气血</span>
            <strong class="shop-resource-value" id="shop-health-value">0 / 0</strong>
          </div>
          <div class="shop-resource-item lives" id="shop-lives-item">
            <span class="shop-resource-label" id="shop-lives-label">💗 剩余金身</span>
            <strong class="shop-resource-value" id="shop-lives-value">0</strong>
          </div>
          <div class="shop-resource-item merit">
            <span class="shop-resource-label" id="shop-merit-label">✨ 功德灵砂</span>
            <strong class="shop-resource-value" id="shop-merit-value">0</strong>
          </div>
        </div>
        <div id="shop-choices-container" class="boon-cards-grid"></div>
        <button class="modal-close-btn" onclick="closeShopModal()">离开宝阁</button>
      </div>
    </div>

    <!-- 72 TRANSFORMATIONS INTERACTIVE SKILL TREE MODAL -->
    <div id="altar-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-label="七十二变技能树">
      <div class="tree-modal-box">
        <div class="tree-header">
          <div>
            <div class="modal-title" style="color: #c084fc; font-size: 26px;">📜 七十二变 · 地煞天罡神木树</div>
            <div class="modal-subtitle" style="font-size: 13px;">参悟七十二变地煞神通 · 解锁苍龙、白虎、大鹏、魔猿、玄武五大神兽真身 (按 [R] 开启化身)</div>
          </div>
          <div style="display: flex; align-items: center; gap: 16px;">
            <div id="tree-ashes-badge" style="font-family: var(--font-chinese); font-size: 16px; color: var(--gold-light); background: rgba(230, 180, 80, 0.15); border: 1px solid var(--gold-primary); padding: 4px 14px; border-radius: 6px;">
              ✨ 功德灵砂: <span id="tree-ashes-val" style="color: #facc15; font-weight: 700;">0</span>
            </div>
            <div class="tree-branch-nav">
              <button class="branch-btn active" onclick="focusTreeBranch('all')">全景天罡</button>
              <button class="branch-btn" onclick="focusTreeBranch('dragon')">🐲 苍龙神变</button>
              <button class="branch-btn" onclick="focusTreeBranch('tiger')">🐯 白虎战煞</button>
              <button class="branch-btn" onclick="focusTreeBranch('roc')">🦅 金翅大鹏</button>
              <button class="branch-btn" onclick="focusTreeBranch('ape')">🦍 法天象地</button>
              <button class="branch-btn" onclick="focusTreeBranch('tortoise')">🐢 玄武不灭</button>
            </div>
          </div>
        </div>

        <div class="tree-main-area">
          <div class="tree-canvas-wrapper" id="tree-canvas-container">
            <canvas id="skill-tree-canvas" width="1800" height="1200"></canvas>
            <div id="tree-hit-layer" class="tree-hit-layer" aria-label="七十二变可选神通节点"></div>
            <div style="position: absolute; bottom: 10px; left: 14px; font-size: 12px; color: #94a3b8; pointer-events: none;">
              💡 拖拽平移 · 单击选择节点 · 双击可直接参悟 1 级 · 右侧按钮也可投资
            </div>
          </div>

          <div class="tree-inspector-panel" id="tree-inspector">
            <div class="tree-inspector-scroll">
              <label for="tree-node-select" style="display:block;font:700 12px var(--font-body);color:#c8bfd5;margin-bottom:5px;">键盘神通目录</label>
              <select id="tree-node-select" class="tree-node-select" aria-label="选择七十二变神通节点"></select>
              <div id="inspect-branch-badge" class="node-header-badge" style="background: rgba(192, 132, 252, 0.2); border: 1px solid #c084fc; color: #c084fc;">
                混元祖根
              </div>
              <div id="inspect-name" class="node-title">混元仙石·灵根初现</div>
              <div id="inspect-rank" class="node-rank-badge">当前境界: 已圆满 (1/1)</div>
              <div id="inspect-desc" class="node-desc-box">
                花果山顶受日月精华，得道体仙胎。全属性基础平衡。
              </div>
              <div id="inspect-stats-bonus" style="font-family: var(--font-body); font-size: 12px; color: #4ade80; margin-bottom: 12px; line-height: 1.5;">
                • 基础气血: 100 | 基础真气: 100
              </div>
              <section class="permanent-passives" aria-labelledby="permanent-passives-title">
                <div class="permanent-passives-title">
                  <span id="permanent-passives-title">✨ 永久被动修行</span>
                  <span id="meta-save-status" class="local-save-badge">浏览器已保存</span>
                </div>
                <div id="passive-skill-list" class="passive-skill-list"></div>
              </section>
            </div>

            <div class="tree-inspector-actions">
              <button id="inspect-equip-btn" class="btn-hud" style="width: 100%; margin-bottom: 8px; font-size: 14px; padding: 8px; background: linear-gradient(180deg, #e11d48, #9f1239); border-color: #fb7185; display: none;" onclick="equipActiveFormFromInspector()">
                ⭐ 装备为 [R] 变身真身
              </button>
              <button id="inspect-upgrade-btn" class="btn-hud" style="width: 100%; margin-bottom: 8px; font-size: 14px; padding: 8px; background: linear-gradient(180deg, #7c3aed, #4c1d95); border-color: #c084fc;" onclick="upgradeNodeFromInspector()">
                参悟提升境界 (消耗 20 灵砂)
              </button>
              <div style="display: flex; gap: 8px;">
                <button class="btn-hud" style="flex: 1; font-size: 12px; padding: 6px; background: rgba(239, 68, 68, 0.2); border-color: #f87171; color: #fca5a5;" onclick="resetAllSkillTreePoints()">
                  🔄 仅重置神木节点
                </button>
                <button class="btn-hud" style="flex: 1; font-size: 12px; padding: 6px; background: linear-gradient(180deg, #d97706, #78350f); border-color: #facc15;" onclick="closeAltarModal()">
                  启程西行 ➔
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ERLANG SHEN PERMANENT FENGSHEN SKILL TREE -->
    <div id="erlang-skill-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="erlang-tree-title">
      <div class="modal-box erlang-tree-box">
        <div class="erlang-tree-header">
          <div>
            <div id="erlang-tree-title" class="modal-title">👁 清源妙道 · 二郎封神修行</div>
            <div id="erlang-tree-subtitle" class="modal-subtitle">天眼、三尖两刃枪、哮天犬与八九玄功 · 每项永久修至 20 重</div>
          </div>
          <div id="erlang-tree-merit" class="erlang-tree-merit">✨ 功德灵砂：0</div>
        </div>
        <div id="erlang-skill-grid" class="erlang-tree-grid" aria-live="polite"></div>
        <button id="erlang-tree-close" class="modal-close-btn" type="button" onclick="closeErlangSkillTree()">保存修行 · 返回</button>
      </div>
    </div>

    <div id="codex-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-label="西游万神伏魔录">
      <div class="modal-box">
        <div class="modal-header">
          <div class="modal-title">西游万神伏魔录 (仙圣仙缘宝典)</div>
          <div class="modal-subtitle">收录三界十一大仙圣神明与神兵重铸秘术</div>
        </div>
        <div id="codex-cards-container" class="codex-grid"></div>
        <button class="modal-close-btn" onclick="closeSkillCodex()">合上宝典</button>
      </div>
    </div>

    <div id="combo-list-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="combo-list-title">
      <div class="modal-box combo-modal-box">
        <div class="modal-header">
          <div id="combo-list-title" class="modal-title">⚔ 如意金箍棒 · 混合连招谱</div>
          <div id="combo-list-subtitle" class="modal-subtitle">连续三次左键为新手三连：弧斩、周身横扫、裂地收棍。右键接在左键连段后为重棍；单独右键仍投掷金箍棒。</div>
        </div>
        <div id="combo-list-help" class="combo-help">每次输入需在 1.35 秒内衔接。攻击期间输入会自动缓冲，不再吞键。善恶境界会改变悟空的整套动作、兵甲与收招特效。</div>
        <div id="combo-list-grid" class="combo-list-grid"></div>
        <button id="combo-list-close" class="modal-close-btn" onclick="closeComboList()">合上连招谱 · 返回战斗</button>
      </div>
    </div>

    <!-- BUDDHA APPROVAL CUTSCENE MODAL -->
    <div id="buddha-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-label="如来佛祖过场">
      <div class="modal-box boss-dialogue-box buddha-cinematic-box">
        <div class="cutscene-topbar">
          <div class="buddha-cutscene-heading">
            <div id="buddha-cutscene-title">如来佛祖 · 掌中佛国</div>
            <div id="buddha-cutscene-subtitle">狂心未歇 · 五指化山</div>
          </div>
          <div id="buddha-cutscene-mode" class="cutscene-art-label" style="position:static;max-width:none;text-align:center;">🎞 五指山影卷</div>
          <div id="buddha-cutscene-counter" class="cutscene-hint" style="text-align:right;">1 / 3</div>
        </div>
        <div id="buddha-cutscene-frame" class="cutscene-frame focus-narrator">
          <img id="buddha-cutscene-image" alt="如来佛祖与五指山剧情插画" />
          <div id="buddha-cutscene-art-label" class="cutscene-art-label">如来神掌 · 五指化山</div>
        </div>
        <div id="buddha-speech-card">
          <div id="buddha-cutscene-speaker" style="color:#fde68a;font:800 13px var(--font-body);margin-bottom:6px;">如来佛祖</div>
          <div id="buddha-cutscene-quote" style="color:#fef9c3;font:650 17px/1.58 var(--font-body);"></div>
          <div id="buddha-cutscene-reward" style="display:none;margin-top:8px;color:#86efac;font:800 13px/1.4 var(--font-body);"></div>
        </div>
        <div class="cutscene-controls">
          <div id="buddha-cutscene-hint" class="cutscene-hint">战斗保持暂停 · 悟空不会受到攻击</div>
          <div class="cutscene-actions">
            <button id="buddha-cutscene-btn" class="btn-hud" style="font-size:16px;padding:10px 30px;background:linear-gradient(180deg,#d97706,#78350f);border-color:#facc15;" onclick="nextBuddhaCutsceneStep()">下一幕 ➔</button>
          </div>
        </div>
      </div>
    </div>

    <!-- BOSS ENCOUNTER AUTHENTIC DIALOGUE MODAL -->
    <div id="boss-dialogue-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-label="首领对话">
      <div class="modal-box boss-dialogue-box">
        <div class="cutscene-topbar">
          <div class="cutscene-chapter-meta">
            <div id="dialogue-boss-name">百眼魔君</div>
            <div id="dialogue-boss-title">盘丝岭黄花观首领</div>
          </div>
          <div id="dialogue-mode-title">🎞 西游影卷</div>
          <div id="dialogue-slide-counter" aria-live="polite">1 / 3</div>
        </div>

        <div id="dialogue-cinematic-frame" class="cutscene-frame focus-narrator">
          <img id="dialogue-cinematic-image" alt="西游记剧情过场插画" />
          <div id="dialogue-art-label" class="cutscene-art-label"></div>
        </div>

        <div id="dialogue-speech-card">
          <div id="dialogue-speaker-tag">章回旁白</div>
          <div id="dialogue-text-body"></div>
        </div>

        <div class="cutscene-controls">
          <div id="dialogue-control-hint" class="cutscene-hint">[空格 / Enter] 下一幕 · 战斗全程暂停</div>
          <div class="cutscene-actions">
            <button id="dialogue-next-btn" class="btn-hud" style="font-size:16px;padding:10px 32px;background:linear-gradient(180deg,#d97706,#92400e);" onclick="nextBossDialogueStep()">下一幕 ➔</button>
            <button id="dialogue-skip-btn" class="btn-hud" style="font-size:14px;padding:10px 24px;background:rgba(100,116,139,.4);border-color:#64748b;" onclick="skipBossDialogue()">跳过影卷</button>
          </div>
        </div>
      </div>
    </div>

    <div id="alignment-tree-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="alignment-tree-title">
      <div class="modal-box alignment-modal-box">
        <div class="alignment-summary">
          <div id="alignment-tree-portrait" class="alignment-portrait neutral"></div>
          <div>
            <div id="alignment-tree-title" class="modal-title">☯ 悟空因果道 · 善、恶、中道神通树</div>
            <div id="alignment-tree-score" class="modal-subtitle">因果平衡 0 · 中道</div>
            <div id="alignment-tree-help" style="font:600 13px/1.55 var(--font-body);color:#cbd5e1;margin-top:7px;">每位首领败阵后只能选择非致死结局。善 +1、恶 −1；跨越门槛会令不再满足前提的神通休眠，但永久等级不会丢失。</div>
            <div id="alignment-tree-merit" style="color:#fde68a;margin-top:5px;">✨ 功德灵砂：0</div>
          </div>
        </div>
        <div id="alignment-skill-grid" class="alignment-skill-grid"></div>
        <button class="modal-close-btn" onclick="closeAlignmentTree()">保存于浏览器 · 返回西游</button>
      </div>
    </div>

    <div id="boss-outcome-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="boss-outcome-title">
      <div class="modal-box boss-outcome-box">
        <div id="boss-outcome-title" class="modal-title" tabindex="-1">首领已经伏地 · 决定他的命运</div>
        <div id="boss-outcome-subtitle" class="modal-subtitle">没有任何选择会杀死首领</div>
        <div id="boss-outcome-lock" class="boss-outcome-lock" role="status" aria-live="polite">请先阅读剧情，选项即将开放。</div>
        <div id="boss-outcome-story" class="boss-outcome-story"></div>
        <div class="boss-outcome-grid">
          <button id="outcome-good" class="outcome-choice good" type="button" onclick="resolveBossOutcome('good')"></button>
          <button id="outcome-neutral" class="outcome-choice neutral" type="button" onclick="resolveBossOutcome('neutral')"></button>
          <button id="outcome-evil" class="outcome-choice evil" type="button" onclick="resolveBossOutcome('evil')"></button>
        </div>
      </div>
    </div>

    <div id="transformation-choice-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="transformation-choice-title">
      <div class="modal-box" style="max-width: 940px; border-color:#c084fc; box-shadow:0 0 55px rgba(192,132,252,.55);">
        <div class="modal-header">
          <div id="transformation-choice-title" class="modal-title">元始天尊 · 三乘变化之问</div>
          <div class="modal-subtitle">此选择维持整次西游征途，并改变战斗专长。</div>
        </div>
        <div class="boon-cards-grid">
          <button class="boon-card" type="button" onclick="chooseTransformationDoctrine('18')">
            <div class="boon-name">十八般变化 · 斗战</div><div class="boon-slot">刚猛攻伐</div>
            <div class="boon-desc">普通与特殊攻击伤害 +35%。变化较少，棍下无双。</div>
          </button>
          <button class="boon-card" type="button" onclick="chooseTransformationDoctrine('36')">
            <div class="boon-name">三十六变 · 天罡</div><div class="boon-slot">攻守圆融</div>
            <div class="boon-desc">伤害 +15%，气血上限 +30，变化持续时间 +3 秒。</div>
          </button>
          <button class="boon-card" type="button" onclick="chooseTransformationDoctrine('72')">
            <div class="boon-name">七十二变 · 地煞</div><div class="boon-slot">千变万化</div>
            <div class="boon-desc">变化持续 +6 秒、冷却 -25%，并获 36 功德灵砂。</div>
          </button>
        </div>
      </div>
    </div>

    <div id="gameover-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="gameover-title">
      <div class="modal-box gameover-box">
        <div id="gameover-title" class="gameover-title defeat">道消身殒</div>
        <div id="gameover-sub" class="modal-subtitle">形骸虽散，神魂不灭。且回花果山水帘洞潜心参悟七十二变！</div>
        <div class="stats-summary">
          <div class="stat-row"><span>已破重天关卡:</span><span id="stat-chambers" class="stat-val">1</span></div>
          <div class="stat-row"><span>降伏妖魔与首领:</span><span id="stat-kills" class="stat-val">0</span></div>
          <div class="stat-row"><span>领悟仙圣神通:</span><span id="stat-boons" class="stat-val">0</span></div>
          <div class="stat-row"><span>服食天庭蟠桃:</span><span id="stat-peaches" class="stat-val">0</span></div>
          <div class="stat-row"><span>积攒功德灵砂:</span><span id="stat-ashes" class="stat-val">0</span></div>
        </div>
        <div style="display: flex; gap: 12px; justify-content: center; margin-top: 10px;">
          <button id="training-gameover-btn" class="btn-hud" style="font-size: 15px; padding: 10px 24px; background: linear-gradient(180deg, #7c3aed, #4c1d95); border-color: #c084fc; box-shadow: 0 0 20px rgba(192, 132, 252, 0.6);" onclick="openTrainingFromGameOver()">📜 领悟地煞七十二变神木树 (修炼加点)</button>
          <button class="btn-hud" style="font-size: 15px; padding: 10px 28px; background: linear-gradient(180deg, #d97706, #78350f);" onclick="restartRun()">再战三界 · 重塑金身启程</button>
        </div>
      </div>
    </div>

    <div id="pause-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="pause-title">
      <div class="modal-box pause-box">
        <div id="pause-title" class="modal-title">云头小憩 · Esc 菜单</div>
        <div class="modal-subtitle">战斗已暂停。保存退出后，下次将从本章开头继续。</div>
        <div id="pause-checkpoint-info" class="pause-checkpoint-info"></div>
        <div class="pause-actions">
          <button class="start-primary" type="button" onclick="resumeGame()">继续战斗</button>
          <button class="start-primary save-exit-button" type="button" onclick="saveAndExitToTitle()">💾 保存并退出</button>
          <button id="pause-audio-btn" class="start-secondary" type="button" onclick="toggleMute()">🔊 音效开启</button>
          <button id="combo-title-btn" class="start-secondary" type="button" onclick="openComboList(true)">⚔ 查看金箍棒连招谱</button>
          <button class="start-secondary" type="button" onclick="restartCurrentChapter()">本章重新开始</button>
        </div>
      </div>
    </div>

  </div>

  <script>
    const ASSETS = %ASSETS_JSON%;
    const loadedImages = {};
    // Animation cells now reserve roughly one quarter of every edge as a
    // transparent safety zone. These factors preserve the former on-screen
    // character size while the source pictures remain much farther apart.
    const PACKED_VISUAL_SCALE_128 = 92 / 72;
    const PACKED_VISUAL_SCALE_160 = 112 / 84;
    const PACKED_VISUAL_SCALE_200 = 140 / 104;
    const PACKED_VISUAL_SCALE_220 = 152 / 116;
    const PACKED_VISUAL_SCALE_240 = 164 / 128;
    const PACKED_VISUAL_SCALE_256 = 176 / 136;
    let loadedCount = 0;
    const totalAssets = Object.keys(ASSETS).length;

    const startScreen = document.getElementById('start-screen');
    if (ASSETS.title_karma_neutral || ASSETS.title_key_art) {
      startScreen.style.backgroundImage = `url("${ASSETS.title_karma_neutral || ASSETS.title_key_art}")`;
    }

    function updateAssetLoadStatus() {
      const status = document.getElementById('asset-load-status');
      const startButton = document.getElementById('start-game-btn');
      if (!status || !startButton) return;
      if (loadedCount >= totalAssets) {
        status.innerText = '诸天就位 · 可挥棒启程';
        startButton.disabled = false;
      } else {
        status.innerText = `正在召集天兵神将… ${loadedCount} / ${totalAssets}`;
      }
    }

    for (let key in ASSETS) {
      const img = new Image();
      img.src = ASSETS[key];
      img.onload = () => {
        loadedCount++;
        updateAssetLoadStatus();
      };
      img.onerror = () => {
        loadedCount++;
        updateAssetLoadStatus();
      };
      loadedImages[key] = img;
    }
    updateAssetLoadStatus();

    // Sound Synthesizer
    class SoundEngine {
      constructor() {
        this.ctx = null;
        this.muted = false;
      }

      init() {
        if (!this.ctx) {
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          this.ctx = new AudioContext();
        }
        if (!this.muted && this.ctx.state === 'suspended') {
          this.ctx.resume();
        }
      }

      playStaffSwing(combo = 0, isHeavy = false) {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          const filter = this.ctx.createBiquadFilter();

          osc.type = isHeavy ? 'sawtooth' : 'sine';
          const startF = isHeavy ? 220 : (combo === 2 ? 450 : (combo === 1 ? 380 : 320));
          const dur = isHeavy ? 0.32 : 0.16;
          osc.frequency.setValueAtTime(startF, t);
          osc.frequency.exponentialRampToValueAtTime(60, t + dur);

          filter.type = 'lowpass';
          filter.frequency.setValueAtTime(isHeavy ? 600 : 1000, t);

          gain.gain.setValueAtTime(isHeavy ? 0.55 : 0.35, t);
          gain.gain.linearRampToValueAtTime(0.01, t + dur);

          osc.connect(filter);
          filter.connect(gain);
          gain.connect(this.ctx.destination);

          osc.start(t);
          osc.stop(t + dur);
        } catch(e) {}
      }

      playStaffHit(isHeavy = false) {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const osc1 = this.ctx.createOscillator();
          const gain1 = this.ctx.createGain();
          osc1.type = isHeavy ? 'square' : 'triangle';
          osc1.frequency.setValueAtTime(isHeavy ? 350 : 620, t);
          osc1.frequency.exponentialRampToValueAtTime(110, t + 0.22);
          gain1.gain.setValueAtTime(isHeavy ? 0.65 : 0.45, t);
          gain1.gain.exponentialRampToValueAtTime(0.001, t + 0.22);
          osc1.connect(gain1);
          gain1.connect(this.ctx.destination);
          osc1.start(t);
          osc1.stop(t + 0.22);
        } catch(e) {}
      }

      playStaffSmash(isTitanic = false) {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(isTitanic ? 180 : 260, t);
          osc.frequency.exponentialRampToValueAtTime(20, t + (isTitanic ? 0.7 : 0.45));

          gain.gain.setValueAtTime(isTitanic ? 0.9 : 0.65, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + (isTitanic ? 0.7 : 0.45));

          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(t);
          osc.stop(t + (isTitanic ? 0.7 : 0.45));
        } catch(e) {}
      }

      playHoundBark() {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(420, t);
          osc.frequency.exponentialRampToValueAtTime(180, t + 0.14);
          gain.gain.setValueAtTime(0.5, t);
          gain.gain.exponentialRampToValueAtTime(0.01, t + 0.14);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(t);
          osc.stop(t + 0.14);
        } catch(e) {}
      }

      playAnvilClang() {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(987.77, t);
          osc.frequency.exponentialRampToValueAtTime(440, t + 0.35);
          gain.gain.setValueAtTime(0.5, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.35);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(t);
          osc.stop(t + 0.35);
        } catch(e) {}
      }

      playBowShoot() {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(680, t);
          osc.frequency.exponentialRampToValueAtTime(140, t + 0.18);
          gain.gain.setValueAtTime(0.45, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.18);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(t);
          osc.stop(t + 0.18);
        } catch(e) {}
      }

      playGong() {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const freqs = [180, 260, 390, 520];
          freqs.forEach((freq, idx) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = idx % 2 === 0 ? 'sine' : 'triangle';
            osc.frequency.setValueAtTime(freq, t);
            osc.frequency.exponentialRampToValueAtTime(freq * 0.96, t + 2.2);

            gain.gain.setValueAtTime(0.35 / (idx + 1), t);
            gain.gain.exponentialRampToValueAtTime(0.0001, t + 2.2);

            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(t);
            osc.stop(t + 2.2);
          });
        } catch(e) {}
      }

      playJadeChime() {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const freqs = [523.25, 659.25, 783.99, 1046.5];
          freqs.forEach((f, i) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(f, t + i * 0.06);

            gain.gain.setValueAtTime(0.25, t + i * 0.06);
            gain.gain.exponentialRampToValueAtTime(0.001, t + i * 0.06 + 1.2);

            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(t + i * 0.06);
            osc.stop(t + i * 0.06 + 1.2);
          });
        } catch(e) {}
      }

      playPeachBite() {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const bufferSize = this.ctx.sampleRate * 0.12;
          const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
          const data = buffer.getChannelData(0);
          for (let i = 0; i < bufferSize; i++) {
            data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.3));
          }
          const noise = this.ctx.createBufferSource();
          noise.buffer = buffer;
          const gain = this.ctx.createGain();
          gain.gain.setValueAtTime(0.45, t);
          gain.gain.exponentialRampToValueAtTime(0.01, t + 0.12);
          noise.connect(gain);
          gain.connect(this.ctx.destination);
          noise.start(t);

          setTimeout(() => this.playJadeChime(), 100);
        } catch(e) {}
      }

      playDash() {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(650, t);
          osc.frequency.exponentialRampToValueAtTime(180, t + 0.2);
          gain.gain.setValueAtTime(0.28, t);
          gain.gain.linearRampToValueAtTime(0.001, t + 0.2);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(t);
          osc.stop(t + 0.2);
        } catch(e) {}
      }

      playLightning() {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(480, t);
          osc.frequency.exponentialRampToValueAtTime(70, t + 0.25);
          gain.gain.setValueAtTime(0.48, t);
          gain.gain.exponentialRampToValueAtTime(0.01, t + 0.25);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(t);
          osc.stop(t + 0.25);
        } catch(e) {}
      }

      playFire() {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(260, t);
          osc.frequency.linearRampToValueAtTime(100, t + 0.3);
          gain.gain.setValueAtTime(0.38, t);
          gain.gain.exponentialRampToValueAtTime(0.01, t + 0.3);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(t);
          osc.stop(t + 0.3);
        } catch(e) {}
      }

      playAwaken() {
        if (!this.ctx) return;
        this.playGong();
        setTimeout(() => this.playJadeChime(), 150);
      }
    }

    const sound = new SoundEngine();
    window.addEventListener('click', () => sound.init(), { once: true });
    window.addEventListener('keydown', () => sound.init(), { once: true });

    function toggleMute() {
      sound.muted = !sound.muted;
      if (sound.ctx) {
        if (sound.muted) sound.ctx.suspend();
        else sound.ctx.resume();
      }
      const label = sound.muted
        ? (gameState.language === 'en' ? '🔇 Sound Off' : '🔇 音效关闭')
        : (gameState.language === 'en' ? '🔊 Sound On' : '🔊 音效开启');
      ['title-audio-btn', 'pause-audio-btn'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = label;
      });
    }

    // 11 Chinese Deities with 100% accurate grid coordinates
    const GODS = {
      luban: {
        name: '巧圣仙师·鲁班',
        title: '百工至圣·神兵天铸仙师',
        portraitCol: 5,
        portraitRow: 0,
        isAvatar: true,
        color: '#f59e0b',
        quotes: [
          '“如意金箍棒乃太上道祖与老夫巧匠神锤所铸！大圣，且看老夫为你淬火重铸神兵真型！”',
          '“千锤百炼出神兵，神机天工夺造化！定叫金箍棒重现万丈神威！”'
        ],
        boons: [
          { id: 'luban_heavy_forge', name: '巨灵重岳重铸', slot: '神兵重铸', weaponForm: 'titan', desc: '【神兵形态】金箍棒化为重岳千钧体：飞棒更重、回旋端震裂大地，但飞行稍慢。' },
          { id: 'luban_extend_reach', name: '如意千钧延展', slot: '神兵重铸', weaponForm: 'extend', desc: '【神兵形态】金箍棒化为擎天长锋：飞棒射程 +65%，连续贯穿不同妖魔时逐步提升伤害。' },
          { id: 'luban_chain_staff', name: '锁龙九节铸', slot: '神兵重铸', weaponForm: 'chain', desc: '【神兵形态】金箍棒化为九节锁龙棍，飞至尽头后环旋一周，可对每个敌人追加一次有上限的回旋命中。' },
          { id: 'luban_anvil_strike', name: '神工百炼击', slot: '普通攻击', desc: '【普攻】金箍棒挥击迸发天工淬火锤芒，造成 55 点真实穿甲伤害并破除敌人护甲。' },
          { id: 'luban_divine_gear', name: '天工八卦齿轮阵', slot: '法术法阵', desc: '【法阵】显化精钢八卦齿轮大阵，高速旋转绞杀阵内妖魔并反弹所有敌方弹幕。' },
          { id: 'luban_clockwork_kite', name: '神机木鸢仙宠', slot: '被动·仙宠', desc: '【被动】召唤机关木鸢在空中盘旋，每 3 秒投掷一枚神机霹雳飞弹，造成 90 点范围火伤。' },
          { id: 'luban_masterwork', name: '巧夺天工神威', slot: '被动·淬火', desc: '【被动】每服食一枚天庭蟠桃额外获得 +50% 属性效果，且常驻获得 50 点护甲。' }
        ]
      },
      erlangshen: {
        name: '二郎显圣真君·杨戬',
        title: '灌江口昭惠显圣二郎真君',
        portraitCol: 0,
        portraitRow: 0,
        color: '#facc15',
        quotes: ['“泼猴，接本君三尖两刃枪之威！啸天犬，咬住泼猴，休得阻碍西行正道！”'],
        boons: [
          { id: 'erlang_strike', name: '三尖破军击', slot: '普通攻击', desc: '【普攻】金箍棒挥击召唤三尖两刃枪芒与九天真雷神矛，造成 45 点额外神圣穿甲真实伤害。' },
          { id: 'erlang_ring', name: '天眼真光阵', slot: '法术法阵', desc: '【法阵】法阵内显化天眼神威，使敌方受到的所有伤害提升 40%，并不停发射天眼极光脉冲。' },
          { id: 'erlang_dash', name: '疾雷瞬身步', slot: '闪避身法', desc: '【闪避】施展筋斗云时在原地降下惩戒神雷，对周围造成 40 点雷电范围伤害。' },
          { id: 'erlang_special', name: '裂天三尖旋', slot: '特殊攻击', desc: '【飞棒】金箍棒去回两程贯穿敌阵，每次命中追加天眼神雷与三尖枪芒。' },
          { id: 'erlang_hound', name: '哮天犬噬魂', slot: '被动·仙宠', desc: '【被动】常驻召唤啸天神犬跟随悟空作战！自主追击、撕咬扑杀敌人，造成 80 点伤害与强制眩晕。' },
          { id: 'erlang_truesight', name: '火眼天眼合一', slot: '被动·暴击', desc: '【被动】全攻击暴击几率提升 25%，暴击伤害提升 50%。' }
        ]
      },
      guanyin: {
        name: '南海大悲观世音菩萨',
        title: '大慈大悲救苦救难观世音',
        portraitCol: 1,
        portraitRow: 0,
        color: '#34d399',
        quotes: ['“受此玉净瓶杨柳甘露，愿你金身不坏，西行圆满。”'],
        boons: [
          { id: 'guanyin_strike', name: '净瓶甘露击', slot: '普通攻击', desc: '【普攻】金箍棒命中敌人时恢复自身 1 点气血（每重 +0.5），并瞬间驱散身上所有负面状态。吸血受短时回复上限约束。' },
          { id: 'guanyin_ring', name: '九品莲台阵', slot: '法术法阵', desc: '【法阵】召唤圣洁莲花阵，每秒为悟空恢复 8 点气血，并将阵内敌人移速降低 50%。' },
          { id: 'guanyin_dash', name: '杨柳清风步', slot: '闪避身法', desc: '【闪避】施展筋斗云时获得翡翠玉露护盾，吸收最多 30 点伤害，持续 2.5 秒。' },
          { id: 'guanyin_special', name: '慈悲普度澜', slot: '特殊攻击', desc: '【飞棒】旋转金箍棒反弹飞行路径上的敌方弹幕，并在首次命中时恢复 15 点真气。' },
          { id: 'guanyin_nirvana', name: '涅槃不灭金身', slot: '被动·保命', desc: '【被动】金身复活次数 +1，复活时恢复 70% 最大生命值与全部真气。' }
        ]
      },
      nezha: {
        name: '三坛海会大神·哪吒',
        title: '中坛元帅三太子哪吒',
        portraitCol: 2,
        portraitRow: 0,
        color: '#f97316',
        quotes: ['“大圣！且看小爷的风火轮与你的筋斗云孰快孰慢！”'],
        boons: [
          { id: 'nezha_strike', name: '烈焰火尖枪', slot: '普通攻击', desc: '【普攻】金箍棒附带三昧真火枪意，使敌人陷入烈火灼烧，3 秒内造成 60 点烈焰伤害。' },
          { id: 'nezha_ring', name: '乾坤金圈阵', slot: '法术法阵', desc: '【法阵】法阵内飞出乾坤圈在最多 6 名敌人之间快速弹射，每次造成 35 点重击伤害。' },
          { id: 'nezha_dash', name: '风火飞轮遁', slot: '闪避身法', desc: '【闪避】筋斗云带起熊熊烈火轨迹，踏入火海的敌人每秒受到 50 点火焰伤害。' },
          { id: 'nezha_special', name: '风火回轮棒', slot: '特殊攻击', desc: '【飞棒】去回两程附着三昧真火，灼烧并沿飞行方向击退命中的敌人。' }
        ]
      },
      laojun: {
        name: '太上道祖·太上老君',
        title: '三清道祖道德天尊',
        portraitCol: 3,
        portraitRow: 0,
        color: '#ec4899',
        quotes: ['“老道八卦炉炼就你的火眼金睛，如今且看你道法修至何等境界！”'],
        boons: [
          { id: 'laojun_strike', name: '三昧真火印', slot: '普通攻击', desc: '【普攻】棍法挥洒三昧纯阳真火，造成 50 点道家仙法伤害并永久熔穿敌方护甲。' },
          { id: 'laojun_ring', name: '八卦神炉阵', slot: '法术法阵', desc: '【法阵】在地面显化八卦阴阳炉阵，每 0.3 秒对阵内敌人造成 40 点炼化伤害。' },
          { id: 'laojun_special', name: '九转金丹旋', slot: '特殊攻击', desc: '【飞棒】每次命中引爆一枚九转丹火，追加混元道法重击。' },
          { id: 'laojun_elixir', name: '九转还魂丹', slot: '被动·仙果', desc: '【被动】天庭蟠桃额外赋予 1 次升级效果，且每次吃蟠桃瞬间补满全生命值。' }
        ]
      },
      aoguang: {
        name: '东海龙王·敖广',
        title: '东海四海龙王之首',
        portraitCol: 4,
        portraitRow: 0,
        color: '#38bdf8',
        quotes: ['“你抢了老龙的定海神针铁！今日且叫你见识四海翻腾之狂澜！”'],
        boons: [
          { id: 'aoguang_strike', name: '怒涛狂澜击', slot: '普通攻击', desc: '【普攻】金箍棒附带重水龙威，发射水刃强力击退敌人并造成 40 点额外伤害。' },
          { id: 'aoguang_ring', name: '归墟大漩涡', slot: '法术法阵', desc: '【法阵】召唤汪洋漩涡将全场敌人强力吸附至中心并造成碾压伤害。' },
          { id: 'aoguang_special', name: '蛟龙回海旋', slot: '特殊攻击', desc: '【飞棒】金箍棒裹挟碧水龙流，去程与回程命中皆可冻结妖魔。' }
        ]
      },
      bullking: {
        name: '平天大圣·牛魔王',
        title: '七大圣之首·大力牛魔王',
        portraitCol: 0,
        portraitRow: 1,
        color: '#ea580c',
        quotes: ['“贤弟悟空！七大圣威震天下，今日随俺老牛踏破这灵霄宝殿！”'],
        boons: [
          { id: 'bull_strike', name: '撼地开山击', slot: '普通攻击', desc: '【普攻】金箍棒造成 40% 额外沉重物理打击，并伴随地震波击退敌人。' },
          { id: 'bull_special', name: '破岳混铁旋', slot: '特殊攻击', desc: '【飞棒】大力回旋棍贯穿长线战场，以巨力将敌人沿飞行方向轰退。' },
          { id: 'bull_ironhide', name: '魔王不坏铁躯', slot: '被动·护甲', desc: '【被动】获得 50 点常驻护甲值，未受击 8 秒后自动回复全满。' }
        ]
      },
      ironfan: {
        name: '翠云山·铁扇公主',
        title: '得道仙真·铁扇仙',
        portraitCol: 1,
        portraitRow: 1,
        color: '#4ade80',
        quotes: ['“我这芭蕉宝扇，一扇息火，二扇生风，三扇下雨！”'],
        boons: [
          { id: 'ironfan_strike', name: '芭蕉罡风刃', slot: '普通攻击', desc: '【普攻】棍法劈出锐利青色风刃，穿透敌人造成 35 点风属性穿甲伤害。' },
          { id: 'ironfan_special', name: '席卷乾坤旋', slot: '特殊攻击', desc: '【飞棒】飞棒轨迹卷起芭蕉罡风，减速并持续推开沿途敌人。' }
        ]
      },
      buddha: {
        name: '西天如来·释迦牟尼佛',
        title: '灵山世尊·万法归一',
        portraitCol: 2,
        portraitRow: 1,
        portraitAsset: 'buddha_colossal',
        offerWeight: 1,
        color: '#facc15',
        quotes: ['“一念慈悲，一念降魔。悟空，且将神针化作法轮，照见万法归一。”'],
        boons: [
          { id: 'buddha_palm_strike', name: '五指如来印', slot: '普通攻击', desc: '【普攻】三连终结技降下佛掌，对落点周围造成本次伤害 40% 的额外范围伤害。' },
          { id: 'buddha_dharma_return', name: '妙法轮回', slot: '特殊攻击', desc: '【飞棒】去程命中留下佛印，回程再命中时引爆法轮，每个目标每次飞棒最多触发一次。' },
          { id: 'buddha_equanimity', name: '诸法无我身', slot: '被动·护甲', desc: '【被动】真气高于一半时受到的伤害降低 15%，每重额外提升 3%，最高 24%。' }
        ]
      },
      yanluo: {
        name: '幽冥教主·阎罗王',
        title: '十殿阎君之第五殿阎罗天子',
        portraitCol: 3,
        portraitRow: 1,
        color: '#ef4444',
        quotes: ['“生死簿上早已勾去你的名姓！今日且助大圣勾尽天下妖魔寿元！”'],
        boons: [
          { id: 'yanluo_strike', name: '生死判官笔', slot: '普通攻击', desc: '【普攻】棍法刻下判官朱砂死印，3 秒后在目标身上引爆 70 点幽冥死气伤害。' },
          { id: 'yanluo_special', name: '阎罗索命旋', slot: '特殊攻击', desc: '【飞棒】回旋金箍棒刻下判官死印，直接斩杀命中后低于 15% 气血的非首领敌人。' }
        ]
      },
      change: {
        name: '广寒仙子·嫦娥与玉兔',
        title: '太阴星君广寒月宫之主',
        portraitCol: 4,
        portraitRow: 1,
        color: '#93c5fd',
        quotes: ['“广寒宫月华如水，照彻幽夜。愿此太阴清辉伴大圣扫荡三界。”'],
        boons: [
          { id: 'change_strike', name: '冰魄寒月击', slot: '普通攻击', desc: '【普攻】棍影挥洒广寒月魄玄冰，造成 35 点冰霜伤害并冻结敌人 1.2 秒。' },
          { id: 'change_special', name: '皓月回环旋', slot: '特殊攻击', desc: '【飞棒】金箍棒化作月轮往返，去程短冻、回程长冻沿途敌人。' }
        ]
      }
    };

    // Every reward card must point to both a gameplay implementation and an
    // observable cue. Tests compare this manifest with GODS so a future
    // text-only boon cannot silently ship.
    const BOON_RUNTIME_CONTRACTS = Object.freeze({
      luban_heavy_forge:{mechanic:'ruyi:titan',visual:'mountain staff'},
      luban_extend_reach:{mechanic:'ruyi:extend',visual:'heaven-reaching staff'},
      luban_chain_staff:{mechanic:'ruyi:chain',visual:'nine-section orbit'},
      luban_anvil_strike:{mechanic:'attack:anvil',visual:'anvil slash'},
      luban_divine_gear:{mechanic:'cast:reflect',visual:'clockwork gear array'},
      luban_clockwork_kite:{mechanic:'companion:missile',visual:'orbiting wooden kite'},
      luban_masterwork:{mechanic:'peach:forge',visual:'masterwork cog aura'},
      erlang_strike:{mechanic:'attack:lightning',visual:'three-pointed lightning'},
      erlang_ring:{mechanic:'cast:amplify',visual:'heaven-eye array'},
      erlang_dash:{mechanic:'dash:thunder',visual:'judgment lightning'},
      erlang_special:{mechanic:'ruyi:lightning',visual:'heaven-eye spear'},
      erlang_hound:{mechanic:'companion:hound',visual:'Xiaotianquan actor'},
      erlang_truesight:{mechanic:'passive:crit',visual:'third-eye sigil'},
      guanyin_strike:{mechanic:'attack:heal',visual:'willow dew pulse'},
      guanyin_ring:{mechanic:'cast:heal-slow',visual:'nine-petal lotus'},
      guanyin_dash:{mechanic:'dash:barrier',visual:'jade willow shield'},
      guanyin_special:{mechanic:'ruyi:reflect-heal',visual:'mercy current'},
      guanyin_nirvana:{mechanic:'passive:revive',visual:'nirvana lotus'},
      nezha_strike:{mechanic:'attack:burn',visual:'samadhi flame'},
      nezha_ring:{mechanic:'cast:bounce',visual:'universe-ring chain'},
      nezha_dash:{mechanic:'dash:fire-trail',visual:'wind-fire wheels'},
      nezha_special:{mechanic:'ruyi:burn-knockback',visual:'flaming return'},
      laojun_strike:{mechanic:'attack:alchemy-fire',visual:'furnace flame'},
      laojun_ring:{mechanic:'cast:furnace',visual:'bagua furnace'},
      laojun_special:{mechanic:'ruyi:elixir-burst',visual:'golden-pill explosion'},
      laojun_elixir:{mechanic:'peach:double-rank-heal',visual:'orbiting golden pill'},
      aoguang_strike:{mechanic:'attack:tide',visual:'water-dragon slash'},
      aoguang_ring:{mechanic:'cast:vortex',visual:'ocean whirlpool'},
      aoguang_special:{mechanic:'ruyi:freeze',visual:'returning sea dragon'},
      bull_strike:{mechanic:'attack:quake',visual:'ground fissure'},
      bull_special:{mechanic:'ruyi:launch',visual:'mountain-breaking wake'},
      bull_ironhide:{mechanic:'passive:regenerating-armor',visual:'horned iron armor'},
      ironfan_strike:{mechanic:'attack:wind',visual:'plantain wind blade'},
      ironfan_special:{mechanic:'ruyi:push-slow',visual:'green cyclone wake'},
      buddha_palm_strike:{mechanic:'attack:palm-aoe',visual:'Buddha palm seal'},
      buddha_dharma_return:{mechanic:'ruyi:seal-detonate',visual:'dharma wheel'},
      buddha_equanimity:{mechanic:'passive:damage-reduction',visual:'golden dharma halo'},
      yanluo_strike:{mechanic:'attack:delayed-seal',visual:'life-and-death seal'},
      yanluo_special:{mechanic:'ruyi:execute',visual:'Yama execution mark'},
      change_strike:{mechanic:'attack:freeze',visual:'frost-moon slash'},
      change_special:{mechanic:'ruyi:freeze',visual:'returning moon wheel'}
    });

    function validateBoonRuntimeContracts() {
      const boonIds = Object.values(GODS).flatMap(god => god.boons.map(boon => boon.id));
      const missing = boonIds.filter(id => !BOON_RUNTIME_CONTRACTS[id]);
      const orphaned = Object.keys(BOON_RUNTIME_CONTRACTS).filter(id => !boonIds.includes(id));
      if (missing.length || orphaned.length) {
        throw new Error(`Boon contract mismatch. Missing: ${missing.join(', ') || 'none'}; orphaned: ${orphaned.join(', ') || 'none'}`);
      }
      return boonIds.length;
    }
    validateBoonRuntimeContracts();

    // Canvas Setup
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    let viewWidth = 1280;
    let viewHeight = 720;
    let deviceScale = 1;
    const MAX_CANVAS_BACKING_PIXELS = 4000000;

    function resizeCanvas() {
      viewWidth = window.innerWidth || document.documentElement.clientWidth || 1280;
      viewHeight = window.innerHeight || document.documentElement.clientHeight || 720;
      // A 4K CSS viewport at DPR 2 previously created an almost 20-million-pixel
      // backing canvas. Camera movement then forced that oversized surface to be
      // repainted every frame. DOM HUD text stays native-resolution; only the
      // action canvas is capped to a stable four-million-pixel performance budget.
      const nativeScale = window.devicePixelRatio || 1;
      const budgetScale = Math.max(1, Math.sqrt(MAX_CANVAS_BACKING_PIXELS / Math.max(1, viewWidth * viewHeight)));
      deviceScale = Math.min(1.5, nativeScale, budgetScale);
      canvas.width = Math.round(viewWidth * deviceScale);
      canvas.height = Math.round(viewHeight * deviceScale);
      canvas.style.width = `${viewWidth}px`;
      canvas.style.height = `${viewHeight}px`;
      ctx.imageSmoothingEnabled = false;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // file:// pages can be denied localStorage by browser privacy policies.
    // Storage must never be able to abort game/input initialization.
    let browserStorageAvailable = true;
    const inMemoryStorageFallback = new Map();
    function safeStorageGetItem(key) {
      if (!browserStorageAvailable) return inMemoryStorageFallback.get(key) ?? null;
      try {
        return window.localStorage.getItem(key);
      } catch (error) {
        browserStorageAvailable = false;
        return inMemoryStorageFallback.get(key) ?? null;
      }
    }
    function safeStorageSetItem(key, value) {
      const serialized = String(value);
      inMemoryStorageFallback.set(key, serialized);
      if (!browserStorageAvailable) return false;
      try {
        window.localStorage.setItem(key, serialized);
        return true;
      } catch (error) {
        browserStorageAvailable = false;
        return false;
      }
    }

    function safeStorageRemoveItem(key) {
      inMemoryStorageFallback.delete(key);
      if (!browserStorageAvailable) return false;
      try {
        window.localStorage.removeItem(key);
        return true;
      } catch (error) {
        browserStorageAvailable = false;
        return false;
      }
    }

    const LANGUAGE_SAVE_KEY = 'havocInHeavenLanguageV1';
    const INITIAL_LANGUAGE = safeStorageGetItem(LANGUAGE_SAVE_KEY) === 'en' ? 'en' : 'zh';

    // Game State
    const gameState = {
      chamberIndex: 1,
      totalChambers: 100,
      runStartChapter: 1,
      runEndChapter: 100,
      biome: 1,
      chamberCleared: false,
      chamberType: 'normal',
      gold: 0,
      ashes: 0,
      peachesEaten: 0,
      enemiesKilled: 0,
      boonsCount: 0,
      screenShake: 0,
      keys: {},
      mouse: { x: viewWidth / 2, y: viewHeight / 2, isDown: false, rightDown: false },
      mobileMove: { x: 0, y: 0 },
      isPaused: true,
      dialogueActive: false,
      rewardSelectionActive: false,
      bossOutcomeActive: false,
      bossOutcomeContinuation: null,
      deferredDialogueChapter: null,
      hasStarted: false,
      transformationDoctrine: null,
      ruyiAcquired: false,
      buddhaImprisoned: false,
      campaignBiome: 0,
      reducedMotion: window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches,
      language: INITIAL_LANGUAGE,
      playableHero: 'wukong',
      campaignRoute: 'journey',
      isNewGamePlus: false
    };

    function getCanvasFont(size, weight = 700, display = false) {
      if (gameState.language === 'en') {
        return `${weight} ${size}px ${display ? "Georgia, Cambria, serif" : "'Segoe UI', Arial, sans-serif"}`;
      }
      return `${weight} ${size}px ${display ? "'Noto Serif SC', serif" : "'Ma Shan Zheng', 'Noto Serif SC', serif"}`;
    }

    const EN_TEXT = {
      '西游记：孙悟空正传 (100章动作肉鸽)': 'Journey to the West: The Legend of Sun Wukong (100-Chapter Action Roguelite)',
      '您的浏览器需要支持 HTML5 Canvas 才能游玩。': 'Your browser must support HTML5 Canvas to play.',
      '西游记动作战场：使用方向键移动，鼠标与快捷键战斗。': 'Journey to the West action arena. Move with the directional keys and fight with the mouse and hotkeys.',
      '触控操作': 'Touch controls', '移动摇杆': 'Movement joystick',
      '西游记 · 齐天西行': 'Journey to the West',
      '从花果山石猴启程，求变化、取金箍棒、大闹天宫，再护送唐三藏一路西行至灵山成佛。完整一百章连续推进，不分篇章重开。': 'Begin as the Stone Monkey of Flower-Fruit Mountain, learn the transformations, claim the Ruyi Staff, defy Heaven, and then guard Tang Sanzang all the way to Buddhahood at Vulture Peak. All one hundred chapters form one continuous journey.',
      '西游全篇 · 第 1–100 章': 'Begin Complete Journey (1–100)',
      '可玩角色选择': 'Playable hero selection', '🐒 孙悟空': '🐒 Sun Wukong', '金箍棒 · 七十二变 · 吹毛成兵': 'Ruyi Staff · 72 Transformations · Hair Clones',
      '👁 二郎神 · 尚未解锁': '👁 Erlang Shen · Locked', '通关完整百章西游后解锁天眼、三尖枪与哮天犬': 'Clear the complete 100-chapter journey to unlock the Third Eye, three-pointed spear, and Xiaotianquan.',
      '👁 二郎显圣真君 · 杨戬': '👁 Erlang Shen · Yang Jian', '三尖两刃枪 · 天眼 · 哮天犬': 'Three-Pointed Spear · Third Eye · Xiaotianquan',
      '✦ 新游戏+ · 天镜再战 (1–100)': '✦ New Game+ · Celestial Mirror (1–100)',
      '语言选择': 'Language selection', '语言 / Language': 'Language', '核心操作': 'Core controls', '移动': 'Move', '左键': 'Left click', '三连击': 'Three-hit combo',
      '左键 + 右键': 'Left + Right Click', '混合棍法连招': 'Mixed staff combos', 'Q / 单独右键': 'Q / Single right click',
      '飞棒去回': 'Throw and recall staff', '吹毛成兵': 'Hair-clone spell', '空格': 'Space', '闪避': 'Dodge', '变身 · 觉醒': 'Transform · Awaken',
      '菜单 / 保存退出': 'Menu / Save & Exit', '从第 1 章重新开始': 'Restart from Chapter 1',
      '挥棒启程': 'Begin the Journey', '七十二变': '72 Transformations', '🔊 音效开启': '🔊 Sound On', '🔇 音效关闭': '🔇 Sound Off',
      '正在召集天兵神将…': 'Summoning the celestial host…', '诸天就位 · 可挥棒启程': 'The heavens are ready · Begin when you are ready',
      '齐天大圣 · 孙悟空': 'Great Sage Equal to Heaven · Sun Wukong', '如意金箍棒 · 一万三千五百斤': 'Ruyi Jingu Bang · 13,500 jin',
      '花果山石棍 · 尚未取得定海神珍': 'Flower-Fruit Stone Staff · Ruyi Staff not yet claimed',
      '气血值 (生命)': 'Health', '混元真气 (法力)': 'Qi', '大闹天宫觉醒': 'Havoc Awakening', '蓄力中 · 满后按 [G]': 'Charging · Press [G] when full',
      '✨ 本章战罢！请走向阵门继续 · 战后气血与真气回复已暂停 ✨': '✨ Chapter cleared! Enter a gate to continue · Post-battle Health and Qi regeneration is paused. ✨',
      '🪙 灵石:': '🪙 Spirit Stones:', '✨ 功德:': '✨ Merit:', '🍑 蟠桃:': '🍑 Peaches:', '❤️ 金身:': '❤️ Lives:',
      '左键/连招': 'LMB', '金箍三连击': 'Ruyi Triple Strike', '神针横扫': 'Divine Staff Sweep',
      '金箍混合棍法': 'Mixed Ruyi Staff Arts', '按 [C] 查看连招': 'Press [C] for Combos',
      '右键/Q/特殊': 'RMB / Q', '如意飞棒': 'Flying Ruyi Staff', '去回双击': 'Out-and-Back Double Hit',
      'E/法术 (75真气)': 'E · 75 Qi', '猴王分身': 'Monkey-King Clones', '空格/闪避': 'Space', '筋斗云遁': 'Somersault-Cloud Dash', '浮光掠影': 'Lightstep Afterimage',
      'R/F/神兽化身': 'R / F', '苍龙真形': 'Azure Dragon Form', '水雷御海': 'Storm-Tide Dominion',
      '📜 七十二变地煞树': '📜 72 Transformations Tree', '📖 西游万神伏魔录': '📖 Journey Codex', '⏸ 暂停': '⏸ Pause', '⏸ [Esc] 菜单 · 保存退出': '⏸ [Esc] Menu · Save & Exit',
      '☯ 因果善恶神通树': '☯ Karmic Alignment Tree',
      '⚔ [C] 金箍棒连招谱': '⚔ [C] Ruyi Combo List', '⚔ 查看金箍棒连招谱': '⚔ View Ruyi Combo List',
      '⚔ 如意金箍棒 · 混合连招谱': '⚔ Ruyi Jingu Bang · Mixed Combo List',
      '连续三次左键为新手三连：弧斩、周身横扫、裂地收棍。右键接在左键连段后为重棍；单独右键仍投掷金箍棒。': 'Three left clicks perform the beginner chain: forward arc, all-around sweep, then ground-slam finisher. Right click during a chain is heavy; right click by itself still throws the Ruyi Staff.',
      '每次输入需在 1.35 秒内衔接。攻击期间输入会自动缓冲，不再吞键。善恶境界会改变悟空的整套动作、兵甲与收招特效。': 'Continue each input within 1.35 seconds. Inputs buffer during attacks. Karma changes Wukong’s complete movement, armor, attack animation, and finisher effects.',
      '合上连招谱 · 返回战斗': 'Close Combo List · Return to Battle',
      '连招输入：—': 'Combo Input: —',
      '善恶中道因果平衡与技能树': 'Good, neutral, and evil alignment balance and skill tree',
      '保存于浏览器 · 返回西游': 'Saved in Browser · Return to Journey',
      '降伏妖魔与首领:': 'Enemies and Bosses Subdued:',
      '天光护体 10 秒 · 先移动拉开距离 · 第三段连击可击倒群妖 · 按 [Esc] 打开菜单与保存退出': 'Celestial protection: 10 seconds · Create space first · Combo finisher knocks foes down · Press [Esc] for Menu and Save & Exit',
      '天光护体 10 秒 · 左右键混合连招 · 按 [C] 查看连招谱 · 按 [Esc] 打开菜单与保存退出': 'Celestial protection: 10 seconds · Mix left/right attacks · Press [C] for combos · Press [Esc] for Menu and Save & Exit',
      '云头小憩 · Esc 菜单': 'Cloud Rest · Esc Menu', '战斗已暂停。保存退出后，下次将从本章开头继续。': 'Combat is paused. Save & Exit resumes from the beginning of this chapter next time.',
      '继续战斗': 'Resume Battle', '💾 保存并退出': '💾 Save & Exit', '本章重新开始': 'Restart This Chapter',
      '闪': 'Dodge', '飞': 'Throw', '攻': 'Attack', '法': 'Spell', '变': 'Form', '觉': 'Awaken',
      '仙圣赐福': 'Divine Boon', '蟠桃强化': 'Peach Upgrade', '王母天庭蟠桃盛宴 (仙桃延寿)': 'Queen Mother’s Peach Banquet',
      '三千年一熟，人吃了体健身轻，道法大进': 'Ripens once every three thousand years; greatly strengthens body and cultivation.',
      '“服食一枚仙桃，顿增三千年道行功力！请选择一项已修习的神通提升品阶境界。”': '“Eat one celestial peach and deepen three thousand years of cultivation. Choose a learned ability to upgrade.”',
      '东海龙宫珍宝阁与土地神坛': 'Eastern Sea Treasure Pavilion', '以灵石换取仙家丹药与通天至宝': 'Trade Spirit Stones for celestial medicine and treasures.', '离开宝阁': 'Leave Pavilion',
      '龙宫珍宝阁': 'Dragon-Palace Treasure Pavilion',
      '📜 七十二变 · 地煞天罡神木树': '📜 72 Transformations · Celestial Skill Tree',
      '参悟七十二变地煞神通 · 解锁苍龙、白虎、大鹏、魔猿、玄武五大神兽真身 (按 [R] 开启化身)': 'Cultivate the 72 Earthly Transformations and unlock Azure Dragon, White Tiger, Golden Roc, Titan Ape, and Black Tortoise forms. Press [R] to transform.',
      '✨ 功德灵砂:': '✨ Merit Sand:', '全景天罡': 'Center View', '🐲 苍龙神变': '🐲 Azure Dragon', '🐯 白虎战煞': '🐯 White Tiger', '🦅 金翅大鹏': '🦅 Golden Roc', '🦍 法天象地': '🦍 Titan Ape', '🐢 玄武不灭': '🐢 Black Tortoise',
      '💡 拖拽平移 · 单击选择节点 · 双击可直接参悟 1 级 · 右侧按钮也可投资': '💡 Drag to pan · Click a node to inspect · Double-click to invest one rank · The right panel also invests',
      '键盘神通目录': 'Keyboard Skill List', '混元祖根': 'Primordial Root', '混元仙石·灵根初现': 'Primordial Stone · First Awakening', '当前境界: 已圆满 (1/1)': 'Current Rank: Complete (1/1)',
      '七十二变技能树': '72 Transformations Skill Tree', '七十二变可选神通节点': 'Selectable 72 Transformations skill nodes', '选择七十二变神通节点': 'Choose a 72 Transformations skill node',
      '花果山顶受日月精华，得道体仙胎。全属性基础平衡。': 'Born from a celestial stone atop Flower-Fruit Mountain. Balanced starting attributes.',
      '• 基础气血: 100 | 基础真气: 100': '• Base Health: 100 | Base Qi: 100', '✨ 永久被动修行': '✨ Permanent Passive Training', '浏览器已保存': 'Saved in browser',
      '⭐ 装备为 [R] 变身真身': '⭐ Equip as [R] transformation', '参悟提升境界 (消耗 20 灵砂)': 'Invest Rank (Cost: 20 Merit)', '🔄 仅重置神木节点': '🔄 Reset Tree Nodes Only', '启程西行 ➔': 'Continue West ➔',
      '西游万神伏魔录 (仙圣仙缘宝典)': 'Journey Codex of Gods and Demons', '收录三界十一大仙圣神明与神兵重铸秘术': 'Records the gods, boons, and divine weapon-forging arts of the Three Realms.', '合上宝典': 'Close Codex',
      '西游万神伏魔录': 'Journey Codex', '如来佛祖过场': 'Buddha story scene', '首领对话': 'Boss dialogue',
      '📜 西游章回 📜': '📜 Journey Chapter 📜', '⚔️ 宿命对决 ⚔️': '⚔️ Destined Duel ⚔️', '齐天大圣·孙悟空': 'Great Sage · Sun Wukong', '花果山美猴王': 'Handsome Monkey King of Flower-Fruit Mountain',
      '按 [空格键] 或点击按钮继续对话': 'Press [Space] or click the button to continue', '下一句 ➔': 'Next Line ➔', '跳过对白': 'Skip Dialogue', '继续西行 ➔': 'Continue West ➔', '接棒！开启大战 ⚔️': 'Raise the Staff! Begin Battle ⚔️',
      '元始天尊 · 三乘变化之问': 'Yuanshi Tianzun · The Three Paths of Transformation', '此选择维持整次西游征途，并改变战斗专长。': 'This choice lasts for the entire journey and changes your combat specialty.',
      '十八般变化 · 斗战': '18 Transformations · Warrior', '刚猛攻伐': 'Relentless Offense', '普通与特殊攻击伤害 +35%。变化较少，棍下无双。': 'Normal and special attack damage +35%. Fewer forms, unmatched staff mastery.',
      '三十六变 · 天罡': '36 Transformations · Celestial', '攻守圆融': 'Balanced Offense and Defense', '伤害 +15%，气血上限 +30，变化持续时间 +3 秒。': 'Damage +15%, maximum health +30, transformation duration +3 seconds.',
      '七十二变 · 地煞': '72 Transformations · Earthly', '千变万化': 'Endless Variety', '变化持续 +6 秒、冷却 -25%，并获 36 功德灵砂。': 'Transformation duration +6 seconds, cooldown −25%, and gain 36 Merit Sand.',
      '道消身殒': 'Defeated', '形骸虽散，神魂不灭。且回花果山水帘洞潜心参悟七十二变！': 'The body falls, but the spirit endures. Return to Flower-Fruit Mountain and deepen the 72 Transformations.',
      '已破重天关卡:': 'Chapters Cleared:', '斩灭妖魔法相:': 'Enemies Defeated:', '领悟仙圣神通:': 'Boons Learned:', '服食天庭蟠桃:': 'Peaches Eaten:', '积攒功德灵砂:': 'Merit Sand:',
      '📜 领悟地煞七十二变神木树 (修炼加点)': '📜 Open 72 Transformations Tree', '再战三界 · 重塑金身启程': 'Rebuild the Golden Body · Journey Again',
      '云头小憩': 'Paused on the Clouds', '战斗已暂停。可调整音效，或从本重天重新整顿阵脚。': 'Combat is paused. Adjust audio or restart the journey.', '继续战斗': 'Resume Battle', '重新启程': 'Restart Journey', '返回标题': 'Return to Title',
      '领受仙法神通': 'Accept Divine Boon', '龙宫珍宝': 'Dragon-Palace Treasure', '灵石不足！': 'Not enough Spirit Stones!',
      '天庭蟠桃 (神效精进)': 'Celestial Peach (Boon Upgrade)', '龙宫宝阁 (灵丹妙药)': 'Dragon-Palace Pavilion (Medicine)',
      '万年人参果 (+气血)': 'Ten-Thousand-Year Ginseng Fruit (+Health)', '功德灵砂 (+修为)': 'Merit Sand (+Cultivation)',
      '花果山·水帘洞 · 第 1 章 / 100 章': 'Flower-Fruit Mountain · Water-Curtain Cave · Chapter 1 / 100',
      '仙石初辟悟大道 · 降妖除魔登九霄': 'The celestial stone awakens · Defeat demons and rise toward Heaven',
      '苍龙真身': 'Azure Dragon Form', '引雷控场': 'Storm-control field',
      '普通攻击': 'Normal Attack', '特殊攻击': 'Special Attack', '被动·仙宠': 'Passive · Celestial Companion', '法术': 'Spell', '法术法阵': 'Spell Array', '闪避神通': 'Dodge Boon', '闪避身法': 'Dodge Art', '神兽化身': 'Beast Form', '神兵重铸': 'Weapon Reforging', '被动·淬火': 'Passive · Tempering', '被动·暴击': 'Passive · Critical', '被动·保命': 'Passive · Revival', '被动·仙果': 'Passive · Celestial Fruit', '被动·护甲': 'Passive · Armor'
    };

    const uiText = (zh, en) => gameState.language === 'en' ? en : zh;

    const localizedNodeSources = new WeakMap();
    const localizedAttributeSources = new WeakMap();
    let languageMutationActive = false;

    function translateGameText(value) {
      const raw = String(value ?? '');
      const trimmed = raw.trim();
      if (!trimmed) return raw;
      let translated = EN_TEXT[trimmed];
      if (!translated) {
        translated = trimmed;
        const replacements = Object.entries(EN_TEXT).sort((a, b) => b[0].length - a[0].length);
        replacements.forEach(([zh, en]) => { if (translated.includes(zh)) translated = translated.split(zh).join(en); });
        translated = translated
          .replace(/第\\s*(\\d+)\\s*章\\s*\\/\\s*(\\d+)\\s*章/g, 'Chapter $1 / $2')
          .replace(/第\\s*(\\d+)\\s*章/g, 'Chapter $1')
          .replace(/(\\d+)\\s*\\/\\s*(\\d+)\\s*章/g, '$1 / $2 Chapters')
          .replace(/第\\s*(\\d+)\\s*重/g, 'Lv. $1')
          .replace(/冷却[:：]\\s*/g, 'Cooldown: ')
          .replace(/气血上限/g, 'Max Health')
          .replace(/真气/g, 'Qi');
      }
      const startSpace = raw.match(/^\\s*/)?.[0] || '';
      const endSpace = raw.match(/\\s*$/)?.[0] || '';
      return startSpace + translated + endSpace;
    }

    function localizeTextNode(node) {
      if (!node || !node.nodeValue || !node.nodeValue.trim()) return;
      let source = localizedNodeSources.get(node);
      if (!source || (gameState.language === 'en' && node.nodeValue !== translateGameText(source))) {
        source = node.nodeValue;
        localizedNodeSources.set(node, source);
      }
      const next = gameState.language === 'en' ? translateGameText(source) : source;
      if (node.nodeValue !== next) node.nodeValue = next;
    }

    function applyGameLanguage() {
      languageMutationActive = true;
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode())) localizeTextNode(node);
      document.querySelectorAll('[aria-label], [title], [placeholder]').forEach(element => {
        let sources = localizedAttributeSources.get(element);
        if (!sources) {
          sources = {};
          ['aria-label', 'title', 'placeholder'].forEach(attr => { if (element.hasAttribute(attr)) sources[attr] = element.getAttribute(attr); });
          localizedAttributeSources.set(element, sources);
        }
        Object.entries(sources).forEach(([attr, source]) => element.setAttribute(attr, gameState.language === 'en' ? translateGameText(source) : source));
      });
      document.documentElement.lang = gameState.language === 'en' ? 'en' : 'zh-CN';
      document.title = gameState.language === 'en' ? EN_TEXT['西游记：孙悟空正传 (100章动作肉鸽)'] : '西游记：孙悟空正传 (100章动作肉鸽)';
      document.getElementById('lang-zh-btn')?.classList.toggle('active', gameState.language === 'zh');
      document.getElementById('lang-en-btn')?.classList.toggle('active', gameState.language === 'en');
      languageMutationActive = false;
    }

    function setGameLanguage(language) {
      gameState.language = language === 'en' ? 'en' : 'zh';
      safeStorageSetItem(LANGUAGE_SAVE_KEY, gameState.language);
      applyGameLanguage();
      updateHUD?.();
      if (typeof refreshTitleUnlocks === 'function') refreshTitleUnlocks();
      if (typeof refreshLocalizedSkillTree === 'function') refreshLocalizedSkillTree();
      if (document.getElementById('combo-list-modal')?.style.display === 'flex' && typeof renderComboList === 'function') renderComboList();
    }

    const languageObserver = new MutationObserver(records => {
      if (languageMutationActive) return;
      languageMutationActive = true;
      records.forEach(record => {
        if (record.type === 'characterData') localizeTextNode(record.target);
        record.addedNodes?.forEach(added => {
          if (added.nodeType === Node.TEXT_NODE) localizeTextNode(added);
          else if (added.nodeType === Node.ELEMENT_NODE) {
            const walker = document.createTreeWalker(added, NodeFilter.SHOW_TEXT);
            let child;
            while ((child = walker.nextNode())) localizeTextNode(child);
          }
        });
      });
      languageMutationActive = false;
    });
    languageObserver.observe(document.body, { subtree: true, childList: true, characterData: true });

    function clearHeldCombatInputs() {
      gameState.keys = {};
      gameState.mouse.isDown = false;
      gameState.mouse.rightDown = false;
      gameState.mobileMove.x = 0;
      gameState.mobileMove.y = 0;
      const knob = document.getElementById('touch-stick-knob');
      if (knob) knob.style.transform = 'translate(0, 0)';
      try {
        player.combatInputQueue = [];
        player.clearCombatComboSequence?.();
      } catch (_) {
        // Player is created later during initial script evaluation.
      }
    }

    function isGameplayPaused() {
      return gameState.isPaused || gameState.dialogueActive || gameState.rewardSelectionActive || gameState.bossOutcomeActive;
    }

    function beginDialoguePause() {
      gameState.dialogueActive = true;
      gameState.isPaused = true;
      clearHeldCombatInputs();
    }

    function endDialoguePause(resumeGameplay = true) {
      gameState.dialogueActive = false;
      clearHeldCombatInputs();
      // Prevent a projectile or melee telegraph that was frozen beside Wukong
      // from damaging him on the exact frame the final line closes.
      player.invulnTimer = Math.max(player.invulnTimer, 0.9);
      if (resumeGameplay && gameState.hasStarted) gameState.isPaused = false;
    }

    function beginRewardSelectionPause() {
      gameState.rewardSelectionActive = true;
      gameState.isPaused = true;
      clearHeldCombatInputs();
    }

    function endRewardSelectionPause() {
      gameState.rewardSelectionActive = false;
      clearHeldCombatInputs();
      player.invulnTimer = Math.max(player.invulnTimer, 0.75);
      const deferredChapter = gameState.deferredDialogueChapter;
      gameState.deferredDialogueChapter = null;
      if (deferredChapter !== null && hasCampaignDialogue(deferredChapter)) {
        openBossDialogue(deferredChapter);
        return;
      }
      if (gameState.hasStarted && !gameState.dialogueActive) gameState.isPaused = false;
    }

    function hasCampaignDialogue(chapter) {
      return gameState.campaignRoute === 'fengshen'
        ? Boolean(ERLANG_FENGSHEN_CHAPTERS?.[chapter])
        : Boolean(CAMPAIGN_DIALOGUES[chapter] || BOSS_DIALOGUES[chapter]);
    }

    function openOrDeferBossDialogue(chapter) {
      if (!hasCampaignDialogue(chapter)) return;
      if (gameState.rewardSelectionActive) {
        gameState.deferredDialogueChapter = chapter;
        gameState.isPaused = true;
        return;
      }
      openBossDialogue(chapter);
    }

    const metaUpgrades = {
      stone_monkey: 0,
      golden_eyes: 0,
      somersault: 0,
      hair_clones: 0,
      qi_circulation: 0,
      nirvana_body: 0
    };

    // Shared dialog focus entry and keyboard trap for every overlay. Reward
    // dialogs intentionally require a choice, but they no longer leak focus into combat.
    let modalRestoreTarget = null;
    const getModalFocusables = modal => Array.from(modal.querySelectorAll('button, select, [href], [tabindex]:not([tabindex="-1"])'))
      .filter(el => !el.disabled && el.getClientRects().length > 0);
    const modalObserver = new MutationObserver(records => {
      records.forEach(record => {
        const modal = record.target;
        if (modal.style.display === 'flex') {
          modalRestoreTarget = document.activeElement;
          const focusables = getModalFocusables(modal);
          if (focusables.length) window.setTimeout(() => focusables[0].focus(), 0);
        } else if (modalRestoreTarget && modalRestoreTarget.isConnected) {
          modalRestoreTarget.focus?.();
          modalRestoreTarget = null;
        }
      });
    });
    document.querySelectorAll('.modal-overlay').forEach(modal => modalObserver.observe(modal, { attributes: true, attributeFilter: ['style'] }));
    document.addEventListener('keydown', e => {
      if (e.key !== 'Tab') return;
      const modal = Array.from(document.querySelectorAll('.modal-overlay')).find(el => getComputedStyle(el).display !== 'none');
      if (!modal) return;
      const focusables = getModalFocusables(modal);
      if (!focusables.length) return;
      const first = focusables[0];
      const last = focusables[focusables.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    window.addEventListener('keydown', (e) => {
      gameState.keys[e.key.toLowerCase()] = true;

      const buddhaModal = document.getElementById('buddha-modal');
      if (buddhaModal && buddhaModal.style.display === 'flex' && (e.key === ' ' || e.key === 'Enter')) {
        e.preventDefault();
        nextBuddhaCutsceneStep();
        return;
      }

      const bossModal = document.getElementById('boss-dialogue-modal');
      if (bossModal && bossModal.style.display === 'flex' && (e.key === ' ' || e.key === 'Enter')) {
        e.preventDefault();
        nextBossDialogueStep();
        return;
      }

      if (e.key === 'Escape') {
        e.preventDefault();
        const pauseModal = document.getElementById('pause-modal');
        const alignmentModal = document.getElementById('alignment-tree-modal');
        const comboModal = document.getElementById('combo-list-modal');
        if (comboModal?.style.display === 'flex') closeComboList();
        else if (alignmentModal?.style.display === 'flex') closeAlignmentTree();
        else if (pauseModal.style.display === 'flex') resumeGame();
        else if (gameState.hasStarted && !document.querySelector('.modal-overlay[style*="display: flex"]')) showPauseMenu();
        return;
      }

      if (!gameState.hasStarted || isGameplayPaused()) return;

      if (e.key.toLowerCase() === 'c') {
        e.preventDefault();
        openComboList(false);
        return;
      }

      if ([' ', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) e.preventDefault();

      if (e.key === ' ' || e.key === 'Shift') {
        player.performDash();
      }
      if (e.key.toLowerCase() === 'e') {
        if (activeLubanAvatar) {
          const dist = Math.hypot(player.x - activeLubanAvatar.x, player.y - activeLubanAvatar.y);
          if (dist < 100) {
            openGodBoonModal('luban');
            return;
          }
        }
        player.performCast();
      }
      if (e.key.toLowerCase() === 'q') {
        player.performQSkill();
      }
      if (e.key.toLowerCase() === 'r' || e.key.toLowerCase() === 'f') {
        player.triggerSignature();
      }
      if (e.key.toLowerCase() === 'g') {
        player.triggerAwakening();
      }
    });

    window.addEventListener('keyup', (e) => {
      gameState.keys[e.key.toLowerCase()] = false;
    });

    window.addEventListener('mousemove', (e) => {
      gameState.mouse.x = e.clientX;
      gameState.mouse.y = e.clientY;
    });

    window.addEventListener('mousedown', (e) => {
      if (isGameplayPaused()) return;
      if (e.button === 0) {
        gameState.mouse.isDown = true;
        player.handleCombatInput('L');
      } else if (e.button === 2) {
        gameState.mouse.rightDown = true;
        // R is a contextual combat token for both heroes. With no active
        // chain it keeps its signature behavior (staff throw / dog command),
        // but after L it must reach the combo parser so Erlang's LLR, LRR,
        // and LLRR spear arts are actually possible.
        player.handleCombatInput('R');
      }
    });

    window.addEventListener('mouseup', (e) => {
      if (e.button === 0) gameState.mouse.isDown = false;
      if (e.button === 2) gameState.mouse.rightDown = false;
    });

    window.addEventListener('contextmenu', (e) => e.preventDefault());
    window.addEventListener('blur', () => {
      gameState.keys = {};
      gameState.mouse.isDown = false;
      if (gameState.hasStarted && !gameState.isPaused) showPauseMenu();
    });

    function setMobileAim(x, y) {
      const length = Math.hypot(x, y);
      if (length < 0.08) return;
      gameState.mouse.x = viewWidth / 2 + (x / length) * 260;
      gameState.mouse.y = viewHeight / 2 + (y / length) * 260;
    }

    const touchStick = document.getElementById('touch-stick');
    const touchKnob = document.getElementById('touch-stick-knob');
    let touchStickPointer = null;
    function updateTouchStick(e) {
      const rect = touchStick.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      let dx = e.clientX - centerX;
      let dy = e.clientY - centerY;
      const maxRadius = rect.width * 0.33;
      const distance = Math.hypot(dx, dy);
      if (distance > maxRadius) {
        dx = dx / distance * maxRadius;
        dy = dy / distance * maxRadius;
      }
      gameState.mobileMove.x = dx / maxRadius;
      gameState.mobileMove.y = dy / maxRadius;
      touchKnob.style.transform = `translate(${dx}px, ${dy}px)`;
      setMobileAim(dx, dy);
    }
    touchStick.addEventListener('pointerdown', e => {
      if (!gameState.hasStarted || isGameplayPaused()) return;
      e.preventDefault();
      touchStickPointer = e.pointerId;
      touchStick.setPointerCapture(e.pointerId);
      updateTouchStick(e);
    });
    touchStick.addEventListener('pointermove', e => {
      if (e.pointerId === touchStickPointer) updateTouchStick(e);
    });
    const releaseTouchStick = e => {
      if (e.pointerId !== touchStickPointer) return;
      touchStickPointer = null;
      gameState.mobileMove.x = 0;
      gameState.mobileMove.y = 0;
      touchKnob.style.transform = 'translate(0, 0)';
    };
    touchStick.addEventListener('pointerup', releaseTouchStick);
    touchStick.addEventListener('pointercancel', releaseTouchStick);

    document.querySelectorAll('[data-touch-action]').forEach(button => {
      button.addEventListener('pointerdown', e => {
        e.preventDefault();
        if (!gameState.hasStarted || isGameplayPaused()) return;
        const action = button.dataset.touchAction;
        if (action === 'attack') {
          gameState.mouse.isDown = true;
          player.handleCombatInput('L');
        } else if (action === 'dash') player.performDash();
        else if (action === 'special') player.handleCombatInput('R');
        else if (action === 'cast') player.performCast();
        else if (action === 'transform') player.triggerSignature();
        else if (action === 'awaken') player.triggerAwakening();
      });
      const release = () => {
        if (button.dataset.touchAction === 'attack') gameState.mouse.isDown = false;
      };
      button.addEventListener('pointerup', release);
      button.addEventListener('pointercancel', release);
    });


    // 72 EARTHLY TRANSFORMATIONS (地煞七十二变) COMPLETE NON-OVERLAPPING INTERACTIVE SKILL TREE
    const SKILL_TREE_72 = [
      // 1. ROOT ORIGIN
      { id: 'root', name: '混元仙石·灵根初现', branch: 'core', x: 900, y: 550, maxRank: 1, cost: 0, prereq: [], icon: '🪨', desc: '花果山顶受日月精华，得道体仙胎。全属性基础平衡。' },

      // 2. BRANCH 1: 🐲 苍龙神变 (Azure Dragon - 水雷御海) - 15 nodes
      { id: 'form_dragon', name: '苍龙真身·水雷御海', branch: 'dragon', x: 900, y: 440, maxRank: 1, cost: 20, prereq: ['root'], icon: '🐲', isForm: true, formKey: 'dragon', desc: '【控场真身】爪击引动连锁水雷，同时加速真气恢复；群体控制强，单体爆发适中。按 [R] 开启化身！' },
      { id: 'dragon_dive', name: '潜渊', branch: 'dragon', x: 800, y: 360, maxRank: 5, cost: 12, prereq: ['form_dragon'], icon: '🌊', desc: '每级提升 15 点生命上限与 8% 水属性抗性。' },
      { id: 'dragon_wind', name: '呼风', branch: 'dragon', x: 900, y: 340, maxRank: 5, cost: 15, prereq: ['form_dragon'], icon: '💨', desc: '每级提升 6% 移动速度与 10% 攻击范围。' },
      { id: 'dragon_rain', name: '唤雨', branch: 'dragon', x: 1000, y: 360, maxRank: 5, cost: 12, prereq: ['form_dragon'], icon: '🌧️', desc: '每级提升 0.5/s 混元真气自然回复速度。' },
      { id: 'dragon_scale', name: '龙鳞逆甲', branch: 'dragon', x: 720, y: 260, maxRank: 5, cost: 18, prereq: ['dragon_dive'], icon: '🛡️', desc: '每级获得 5 点永久伤害减免与 10 点护甲。' },
      { id: 'dragon_claw', name: '苍龙雷爪', branch: 'dragon', x: 840, y: 240, maxRank: 5, cost: 20, prereq: ['dragon_dive', 'dragon_wind'], icon: '⚡', desc: '变身苍龙时，爪击有 25% 概率降下九天玄雷轰顶。' },
      { id: 'dragon_breath', name: '九霄龙息', branch: 'dragon', x: 960, y: 240, maxRank: 5, cost: 22, prereq: ['dragon_wind', 'dragon_rain'], icon: '🔥', desc: '变身苍龙攻击时喷涌龙息水火波，造成 40% 额外范围伤害。' },
      { id: 'dragon_sea', name: '覆海大圣', branch: 'dragon', x: 1080, y: 260, maxRank: 5, cost: 18, prereq: ['dragon_rain'], icon: '🌊', desc: '每级提升苍龙变身持续时间 1.5 秒。' },
      { id: 'dragon_thunder', name: '掌雷神印', branch: 'dragon', x: 760, y: 150, maxRank: 5, cost: 25, prereq: ['dragon_scale', 'dragon_claw'], icon: '⚡', desc: '雷系攻击暴击伤害提升 20%/级。' },
      { id: 'dragon_storm', name: '雷霆狂暴', branch: 'dragon', x: 900, y: 130, maxRank: 5, cost: 30, prereq: ['dragon_claw', 'dragon_breath'], icon: '🌩️', desc: '真气满时攻击必定触发范围连锁雷弧。' },
      { id: 'dragon_tsunami', name: '海啸滔天', branch: 'dragon', x: 1040, y: 150, maxRank: 5, cost: 25, prereq: ['dragon_breath', 'dragon_sea'], icon: '🌊', desc: '苍龙第三式普通攻击卷起冲天水龙卷击飞群敌。' },
      { id: 'dragon_subdue', name: '降龙伏波', branch: 'dragon', x: 820, y: 50, maxRank: 5, cost: 35, prereq: ['dragon_thunder', 'dragon_storm'], icon: '👑', desc: '对 Boss 和精英怪造成伤害额外提升 12%/级。' },
      { id: 'dragon_soar', name: '天龙翱翔', branch: 'dragon', x: 980, y: 50, maxRank: 5, cost: 35, prereq: ['dragon_storm', 'dragon_tsunami'], icon: '✨', desc: '闪避时化作游龙电光穿透一切障碍并获得 0.4s 无敌。' },
      { id: 'dragon_water_walk', name: '履水化龙', branch: 'dragon', x: 640, y: 200, maxRank: 5, cost: 20, prereq: ['dragon_scale'], icon: '💧', desc: '受到致命伤害时自动释放水遁护罩，免死一次。' },
      { id: 'dragon_water_know', name: '识水通玄', branch: 'dragon', x: 1160, y: 200, maxRank: 5, cost: 20, prereq: ['dragon_sea'], icon: '🔮', desc: '获得额外 15% 灵石掉落与灵砂收益。' },

      // 3. BRANCH 2: 🐯 白虎战煞 (White Tiger - 庚金杀伐) - 14 nodes
      { id: 'form_tiger', name: '白虎真形·庚金战煞', branch: 'tiger', x: 1030, y: 550, maxRank: 1, cost: 20, prereq: ['root'], icon: '🐯', isForm: true, formKey: 'tiger', desc: '【狩猎真身】攻速、突进与暴击大幅提高，利爪造成持续流血；近身爆发最强。按 [R] 开启化身！' },
      { id: 'tiger_pounce', name: '伏虎纵跃', branch: 'tiger', x: 1150, y: 490, maxRank: 5, cost: 12, prereq: ['form_tiger'], icon: '🐾', desc: '每级增加 15% 突进距离与 8% 攻击速度。' },
      { id: 'tiger_claws', name: '暴煞裂空', branch: 'tiger', x: 1150, y: 610, maxRank: 5, cost: 15, prereq: ['form_tiger'], icon: '⚔️', desc: '每级提升普通攻击伤害 10 点与 4% 基础暴击率。' },
      { id: 'tiger_roar', name: '虎啸撼岳', branch: 'tiger', x: 1270, y: 440, maxRank: 5, cost: 18, prereq: ['tiger_pounce'], icon: '📢', desc: '变身时爆发王者虎啸，震慑周围敌人眩晕 1.5 秒。' },
      { id: 'tiger_frenzy', name: '狂煞饮血', branch: 'tiger', x: 1270, y: 550, maxRank: 5, cost: 20, prereq: ['tiger_pounce', 'tiger_claws'], icon: '🩸', desc: '暴击命中时汲取敌人气血，恢复造成伤害的 1.5%/级（最高 7.5%，并受短时回复上限约束）。' },
      { id: 'tiger_bleed', name: '庚金裂魄', branch: 'tiger', x: 1270, y: 660, maxRank: 5, cost: 18, prereq: ['tiger_claws'], icon: '🗡️', desc: '攻击附加撕裂流血，每秒造成 20 点持续真实伤害。' },
      { id: 'tiger_slay', name: '斩妖诛魔', branch: 'tiger', x: 1390, y: 420, maxRank: 5, cost: 22, prereq: ['tiger_roar'], icon: '⚡', desc: '对生命值低于 40% 的敌人伤害提升 25%/级。' },
      { id: 'tiger_speed', name: '疾风神煞', branch: 'tiger', x: 1390, y: 550, maxRank: 5, cost: 25, prereq: ['tiger_frenzy'], icon: '💨', desc: '连击不中断时，移速与攻速每秒提升 4%，最多叠加 40%。' },
      { id: 'tiger_crit', name: '绝命一击', branch: 'tiger', x: 1390, y: 680, maxRank: 5, cost: 25, prereq: ['tiger_bleed'], icon: '💥', desc: '暴击伤害倍率提升 30%/级。' },
      { id: 'tiger_bloodlust', name: '煞气通玄', branch: 'tiger', x: 1510, y: 480, maxRank: 5, cost: 30, prereq: ['tiger_slay', 'tiger_speed'], icon: '🔥', desc: '击杀敌人使变身持续时间延长 0.8 秒。' },
      { id: 'tiger_execute', name: '白虎斩首', branch: 'tiger', x: 1510, y: 620, maxRank: 5, cost: 32, prereq: ['tiger_speed', 'tiger_crit'], icon: '☠️', desc: '对普通怪物有 15% 概率直接触发一击必杀斩首。' },
      { id: 'tiger_spirit', name: '煞星临凡', branch: 'tiger', x: 1630, y: 550, maxRank: 5, cost: 40, prereq: ['tiger_bloodlust', 'tiger_execute'], icon: '🌟', desc: '白虎变身期间全程霸体免疫击退击晕，伤害提升 50%。' },
      { id: 'tiger_bite', name: '吞刀啖煞', branch: 'tiger', x: 1400, y: 310, maxRank: 5, cost: 20, prereq: ['tiger_slay'], icon: '🗡️', desc: '受到远程弹幕伤害减少 20%/级。' },
      { id: 'tiger_sword', name: '剑解煞神', branch: 'tiger', x: 1400, y: 790, maxRank: 5, cost: 20, prereq: ['tiger_crit'], icon: '⚔️', desc: '棍法挥动带出庚金剑气，攻击距离增加 35%。' },

      // 4. BRANCH 3: 🦅 金翅大鹏 (Golden Roc - 极速破虚) - 14 nodes
      { id: 'form_roc', name: '金翅大鹏·极速破虚', branch: 'roc', x: 990, y: 680, maxRank: 1, cost: 20, prereq: ['root'], icon: '🦅', isForm: true, formKey: 'roc', desc: '【游击真身】获得额外闪避、更快充能与超长穿透风刃；静止输出较低。按 [R] 开启化身！' },
      { id: 'roc_fly', name: '御风翔天', branch: 'roc', x: 1090, y: 770, maxRank: 5, cost: 12, prereq: ['form_roc'], icon: '💨', desc: '闪避充能上限 +1/级，闪避恢复速度加快 15%。' },
      { id: 'roc_feather', name: '凌霄羽刃', branch: 'roc', x: 970, y: 810, maxRank: 5, cost: 15, prereq: ['form_roc'], icon: '🪶', desc: '普通攻击射出 3 道破空金羽飞刃。' },
      { id: 'roc_dash', name: '九万里遁', branch: 'roc', x: 1210, y: 830, maxRank: 5, cost: 18, prereq: ['roc_fly'], icon: '⚡', desc: '闪避瞬移距离提升 30%/级，穿透敌人造成撕裂。' },
      { id: 'roc_vortex', name: '天罡神风', branch: 'roc', x: 1090, y: 890, maxRank: 5, cost: 20, prereq: ['roc_fly', 'roc_feather'], icon: '🌪️', desc: '攻击命中生成持续牵引群敌的罡风漩涡。' },
      { id: 'roc_sky', name: '扶摇直上', branch: 'roc', x: 970, y: 940, maxRank: 5, cost: 18, prereq: ['roc_feather'], icon: '✨', desc: '跃空重击下砸伤害提升 40%/级。' },
      { id: 'roc_talon', name: '撕天金爪', branch: 'roc', x: 1320, y: 890, maxRank: 5, cost: 22, prereq: ['roc_dash'], icon: '🦅', desc: '大鹏变身攻击无视目标 30%/级 护甲与抗性。' },
      { id: 'roc_cyclone', name: '旋风万仞', branch: 'roc', x: 1200, y: 970, maxRank: 5, cost: 25, prereq: ['roc_vortex'], icon: '🌀', desc: '大鹏旋风持续扩散，击退并割裂所有接近的敌人。' },
      { id: 'roc_sight', name: '鹰眼破妄', branch: 'roc', x: 1080, y: 1020, maxRank: 5, cost: 22, prereq: ['roc_vortex', 'roc_sky'], icon: '👁️', desc: '侦测所有敌人弱点，攻击命中弱点必定暴击。' },
      { id: 'roc_solar', name: '追日神光', branch: 'roc', x: 1430, y: 960, maxRank: 5, cost: 30, prereq: ['roc_talon'], icon: '☀️', desc: '击败敌人释放金光净化波，致盲周围所有敌人。' },
      { id: 'roc_sonic', name: '音障破空', branch: 'roc', x: 1310, y: 1040, maxRank: 5, cost: 32, prereq: ['roc_cyclone', 'roc_sight'], icon: '💥', desc: '极速移动时留下残影冲击波，每段造成 80 点伤害。' },
      { id: 'roc_supreme', name: '大鹏金翅', branch: 'roc', x: 1420, y: 1080, maxRank: 5, cost: 40, prereq: ['roc_solar', 'roc_sonic'], icon: '👑', desc: '变身大鹏期间闪避无冷却消耗，化身九天极速主宰！' },
      { id: 'roc_feather_burst', name: '万羽齐发', branch: 'roc', x: 860, y: 920, maxRank: 5, cost: 20, prereq: ['roc_sky'], icon: '🪶', desc: '大鹏展翅时向全屏发射 16 枚追踪穿甲金羽。' },
      { id: 'roc_sky_scout', name: '识地观天', branch: 'roc', x: 1220, y: 730, maxRank: 5, cost: 18, prereq: ['roc_dash'], icon: '🗺️', desc: '每进入新重天，自动探知全场精英怪并标记弱点。' },

      // 5. BRANCH 4: 🦍 法天象地·齐天巨猿 (Colossal Ape - 泰坦崩山) - 14 nodes
      { id: 'form_ape', name: '法天象地·混世魔猿', branch: 'ape', x: 810, y: 680, maxRank: 1, cost: 20, prereq: ['root'], icon: '🦍', isForm: true, formKey: 'ape', desc: '【重装真身】慢速重拳造成巨额伤害、击倒与地震波，并自带霸体减伤；机动性最低。按 [R] 开启化身！' },
      { id: 'ape_might', name: '大力拔山', branch: 'ape', x: 710, y: 770, maxRank: 5, cost: 12, prereq: ['form_ape'], icon: '💪', desc: '每级提升攻击力 15 点与击退力量 30%。' },
      { id: 'ape_quake', name: '地裂天崩', branch: 'ape', x: 830, y: 810, maxRank: 5, cost: 15, prereq: ['form_ape'], icon: '🌋', desc: '普通攻击波及范围扩大 25%/级。' },
      { id: 'ape_mountain', name: '担山赶月', branch: 'ape', x: 590, y: 830, maxRank: 5, cost: 18, prereq: ['ape_might'], icon: '⛰️', desc: '生命上限永久提升 30 点/级，受击硬直减半。' },
      { id: 'ape_titan', name: '万丈法躯', branch: 'ape', x: 710, y: 890, maxRank: 5, cost: 20, prereq: ['ape_might', 'ape_quake'], icon: '🗿', desc: '变身巨猿体型进一步扩大，伤害减免 35%。' },
      { id: 'ape_stone', name: '石破天惊', branch: 'ape', x: 830, y: 940, maxRank: 5, cost: 18, prereq: ['ape_quake'], icon: '💥', desc: '重击命中引发岩崩碎石，对全场敌人造成眩晕击倒。' },
      { id: 'ape_smash', name: '擎天怒砸', branch: 'ape', x: 480, y: 890, maxRank: 5, cost: 22, prereq: ['ape_mountain'], icon: '🔨', desc: '巨猿双拳砸地引发 360° 环形地震波。' },
      { id: 'ape_fist', name: '神拳破岳', branch: 'ape', x: 600, y: 970, maxRank: 5, cost: 25, prereq: ['ape_titan'], icon: '👊', desc: '巨猿挥拳产生空气爆鸣重击，造成 2.5 倍暴击伤害。' },
      { id: 'ape_armor', name: '金刚仙躯', branch: 'ape', x: 720, y: 1020, maxRank: 5, cost: 25, prereq: ['ape_titan', 'ape_stone'], icon: '🛡️', desc: '获得永久护甲 20 点/级，免疫一切毒素与迟缓。' },
      { id: 'ape_roar', name: '齐天魔吼', branch: 'ape', x: 370, y: 960, maxRank: 5, cost: 30, prereq: ['ape_smash'], icon: '🦁', desc: '怒吼驱散全场敌方法术弹幕，并降低敌军 40% 防御。' },
      { id: 'ape_shockwave', name: '混沌震波', branch: 'ape', x: 490, y: 1040, maxRank: 5, cost: 32, prereq: ['ape_smash', 'ape_fist'], icon: '🌊', desc: '每次重击形成连锁冲击波，连续震荡 3 次。' },
      { id: 'ape_overlord', name: '混世魔尊', branch: 'ape', x: 380, y: 1080, maxRank: 5, cost: 40, prereq: ['ape_roar', 'ape_shockwave'], icon: '👑', desc: '变身巨猿期间攻击力翻倍，重击直接击碎任何霸体！' },
      { id: 'ape_stone_boil', name: '煮石炼金', branch: 'ape', x: 940, y: 920, maxRank: 5, cost: 20, prereq: ['ape_stone'], icon: '🍲', desc: '击碎精英怪物必定掉落大块灵石与淬体丹。' },
      { id: 'ape_spit_flame', name: '吐焰焚天', branch: 'ape', x: 580, y: 730, maxRank: 5, cost: 18, prereq: ['ape_might'], icon: '🔥', desc: '法天象地施展时喷吐三昧真火，灼烧大范围敌人。' },

      // 6. BRANCH 5: 🐢 玄武不坏 (Black Tortoise - 幽冥玄甲) - 14 nodes
      { id: 'form_tortoise', name: '玄武真形·幽冥玄甲', branch: 'tortoise', x: 770, y: 550, maxRank: 1, cost: 20, prereq: ['root'], icon: '🐢', isForm: true, formKey: 'tortoise', desc: '【守御真身】高额减伤、单击封顶、持续回复与减速水环；爆发低但生存最强。按 [R] 开启化身！' },
      { id: 'tort_shell', name: '金刚玄甲', branch: 'tortoise', x: 650, y: 490, maxRank: 5, cost: 12, prereq: ['form_tortoise'], icon: '🛡️', desc: '每级增加 25 点生命值与 6 点护甲。' },
      { id: 'tort_spike', name: '地煞荆棘', branch: 'tortoise', x: 650, y: 610, maxRank: 5, cost: 15, prereq: ['form_tortoise'], icon: '🌵', desc: '受击时反弹 35%/级 近战伤害给攻击者。' },
      { id: 'tort_guard', name: '生光护体', branch: 'tortoise', x: 530, y: 440, maxRank: 5, cost: 18, prereq: ['tort_shell'], icon: '✨', desc: '生命低于 30% 时自动生成抵御 150 点伤害的护盾。' },
      { id: 'tort_flow', name: '导引归元', branch: 'tortoise', x: 530, y: 550, maxRank: 5, cost: 20, prereq: ['tort_shell', 'tort_spike'], icon: '☯️', desc: '受击时有 25% 概率将伤害转化为真气回复。' },
      { id: 'tort_regen', name: '辟谷延寿', branch: 'tortoise', x: 530, y: 660, maxRank: 5, cost: 18, prereq: ['tort_spike'], icon: '🌱', desc: '脱离战斗或变身时每秒自动恢复 3 点气血。' },
      { id: 'tort_abyss', name: '幽通九泉', branch: 'tortoise', x: 410, y: 420, maxRank: 5, cost: 22, prereq: ['tort_guard'], icon: '🌊', desc: '变身玄武在脚下生成幽冥寒潭，减速敌人 60%。' },
      { id: 'tort_reflect', name: '借力返虚', branch: 'tortoise', x: 410, y: 550, maxRank: 5, cost: 25, prereq: ['tort_flow'], icon: '🪞', desc: '格挡并反弹所有飞行弹幕并提高其威力 100%。' },
      { id: 'tort_immortal', name: '九转涅槃', branch: 'tortoise', x: 410, y: 680, maxRank: 5, cost: 30, prereq: ['tort_regen'], icon: '♻️', desc: '永久增加 1 次金身复活次数。' },
      { id: 'tort_shield', name: '气禁锁命', branch: 'tortoise', x: 290, y: 480, maxRank: 5, cost: 30, prereq: ['tort_abyss', 'tort_reflect'], icon: '🔒', desc: '变身期间单次受到伤害不会超过生命上限的 8%。' },
      { id: 'tort_whirlpool', name: '太阴水精', branch: 'tortoise', x: 290, y: 620, maxRank: 5, cost: 32, prereq: ['tort_reflect', 'tort_immortal'], icon: '🌀', desc: '玄武周身形成护体水精回旋刃，自动斩杀周围杂兵。' },
      { id: 'tort_supreme', name: '玄武不灭', branch: 'tortoise', x: 170, y: 550, maxRank: 5, cost: 40, prereq: ['tort_shield', 'tort_whirlpool'], icon: '👑', desc: '变身玄武期间免疫致死伤害，反弹 200% 伤害，成就真武不败！' },
      { id: 'tort_cover_sun', name: '掩日避劫', branch: 'tortoise', x: 400, y: 310, maxRank: 5, cost: 20, prereq: ['tort_abyss'], icon: '🌑', desc: '暗影笼罩自身，使敌方远程攻击命中率降低 50%。' },
      { id: 'tort_renew_head', name: '续头再造', branch: 'tortoise', x: 400, y: 790, maxRank: 5, cost: 20, prereq: ['tort_immortal'], icon: '🧬', desc: '每次复活时全状态瞬间恢复至 100% 并获 3 秒无敌。' }
    ];

    const FORM_SKILL_RUNTIME_GROUPS = Object.freeze({
      activation: ['form_dragon','form_tiger','form_roc','form_ape','form_tortoise'],
      normalAttack: [
        'dragon_claw','dragon_thunder','dragon_storm','dragon_tsunami','dragon_subdue',
        'tiger_claws','tiger_frenzy','tiger_bleed','tiger_slay','tiger_crit','tiger_execute',
        'roc_feather','roc_vortex','roc_sky','roc_talon','roc_sight',
        'ape_might','ape_quake','ape_stone','ape_fist','ape_shockwave'
      ],
      special: ['dragon_breath','tiger_sword','roc_feather_burst','ape_spit_flame'],
      spell: ['dragon_dive','dragon_rain','tiger_roar','roc_cyclone','ape_smash','ape_roar','tort_abyss'],
      dash: ['dragon_soar','tiger_pounce','roc_fly','roc_dash','roc_sonic','roc_supreme'],
      defense: [
        'dragon_scale','dragon_water_walk','tiger_bite','ape_mountain','ape_armor',
        'tort_shell','tort_spike','tort_guard','tort_flow','tort_reflect','tort_immortal',
        'tort_shield','tort_supreme','tort_cover_sun','tort_renew_head'
      ],
      kill: ['dragon_water_know','tiger_bloodlust','roc_solar','ape_stone_boil'],
      aura: ['dragon_wind','dragon_sea','tiger_speed','tiger_spirit','roc_sky_scout','ape_titan','ape_overlord','tort_regen','tort_whirlpool']
    });
    const FORM_SKILL_RUNTIME_CONTRACTS = Object.freeze(Object.fromEntries(
      Object.entries(FORM_SKILL_RUNTIME_GROUPS).flatMap(([hook, ids]) => ids.map(id => [id, {
        hook,
        visual: `${id}-animated-cue`,
        form: SKILL_TREE_72.find(node => node.id === id)?.branch
      }]))
    ));
    const AUTHORED_SKILL_EFFECTS = new Set(SKILL_TREE_72.map(node => node.id));

    function validateTransformationSkillContracts() {
      const expected = SKILL_TREE_72.filter(node => node.id !== 'root').map(node => node.id);
      const grouped = Object.values(FORM_SKILL_RUNTIME_GROUPS).flat();
      const missing = expected.filter(id => !FORM_SKILL_RUNTIME_CONTRACTS[id]);
      const duplicates = grouped.filter((id, index) => grouped.indexOf(id) !== index);
      const extras = grouped.filter(id => !expected.includes(id));
      if (missing.length || duplicates.length || extras.length || grouped.length !== expected.length) {
        throw new Error(`Transformation skill contract mismatch: missing=${missing.join(',')}; duplicates=${duplicates.join(',')}; extras=${extras.join(',')}`);
      }
      return expected.length;
    }
    validateTransformationSkillContracts();

    // Karma advances deliberately slowly: each boss outcome moves this shared,
    // browser-persistent score by exactly one point. Purchased ranks stay owned
    // forever, but become dormant whenever their current alignment or prerequisite
    // is no longer satisfied.
    let alignmentScore = 0;
    let alignmentSkillRanks = {};
    const ALIGNMENT_VISUAL_THRESHOLD = 10;
    const KARMA_SKILL_MAX_RANK = 20;
    const ALIGNMENT_SKILLS = [
      { id:'g_benevolent_guard', path:'good', tier:1, threshold:3, maxRank:5, cost:8, prereq:[], icon:'🛡️', nameZh:'仁心护体', nameEn:'Benevolent Guard', descZh:'每级 +5 护甲；善念凝成可见护光。', descEn:'+5 armor per rank; compassion condenses into a visible ward.', effects:{armor:5} },
      { id:'g_pure_body', path:'good', tier:1, threshold:3, maxRank:5, cost:8, prereq:[], icon:'🤍', nameZh:'清净金身', nameEn:'Pure Golden Body', descZh:'每级生命上限 +2%。', descEn:'+2% maximum health per rank.', effects:{hpPct:.02} },
      { id:'g_mercy_aegis', path:'good', tier:2, threshold:8, maxRank:5, cost:11, prereq:['g_benevolent_guard'], icon:'🪷', nameZh:'慈悲莲盾', nameEn:'Lotus Aegis of Mercy', descZh:'每级受到伤害 −1%，闪避后获得护盾。', descEn:'Take 1% less damage per rank and gain a barrier after dashing.', effects:{damageReduction:.01,dashBarrier:8} },
      { id:'g_holy_staff', path:'good', tier:2, threshold:8, maxRank:5, cost:11, prereq:['g_pure_body'], icon:'✨', nameZh:'净世圣棍', nameEn:'World-Cleansing Staff', descZh:'每级 +3% 圣光触发率，命中时净化小范围妖气。', descEn:'+3% holy-proc chance per rank; hits cleanse a small area.', effects:{holyChance:.03} },
      { id:'g_lotus_recovery', path:'good', tier:3, threshold:15, maxRank:5, cost:14, prereq:['g_mercy_aegis'], icon:'🌸', nameZh:'九品回春', nameEn:'Ninefold Lotus Renewal', descZh:'每级真气回复 +0.2/s；善行结局回复生命。', descEn:'+0.2 Qi regeneration per second per rank; merciful outcomes restore health.', effects:{qiRegen:.2,mercyHeal:.03} },
      { id:'g_celestial_mail', path:'good', tier:3, threshold:15, maxRank:5, cost:14, prereq:['g_mercy_aegis','g_holy_staff'], icon:'🪽', nameZh:'天将神铠', nameEn:'Celestial Marshal Mail', descZh:'每级 +8 护甲、生命 +1%。', descEn:'+8 armor and +1% maximum health per rank.', effects:{armor:8,hpPct:.01} },
      { id:'g_guardian_cloud', path:'good', tier:3, threshold:15, maxRank:5, cost:15, prereq:['g_holy_staff'], icon:'☁️', nameZh:'护生祥云', nameEn:'Guardian Cloud', descZh:'闪避护盾每级强化 12 点，并在身后留下圣光。', descEn:'Dash barrier gains 12 points per rank and leaves protective light.', effects:{dashBarrier:12} },
      { id:'g_compassionate_reversal', path:'good', tier:4, threshold:25, maxRank:3, cost:19, prereq:['g_lotus_recovery','g_celestial_mail'], icon:'🙏', nameZh:'慈航逆转', nameEn:'Compassionate Reversal', descZh:'生命低于 25% 时每级获得 6% 额外减伤。', descEn:'Below 25% health, gain 6% additional damage reduction per rank.', effects:{lowHpReduction:.06} },
      { id:'g_sanctified_clones', path:'good', tier:4, threshold:25, maxRank:3, cost:19, prereq:['g_guardian_cloud'], icon:'🐒', nameZh:'护法毫毛', nameEn:'Sanctified Hair Clones', descZh:'吹毛成兵每级伤害 +12%，分身带蓝白圣焰。', descEn:'Hair clones gain 12% damage per rank and carry blue-white holy flame.', effects:{cloneDamage:.12} },
      { id:'g_bodhi_heart', path:'good', tier:4, threshold:25, maxRank:3, cost:20, prereq:['g_celestial_mail','g_guardian_cloud'], icon:'💠', nameZh:'菩提不动心', nameEn:'Unmoving Bodhi Heart', descZh:'每级生命 +4%、真气 +4%。', descEn:'+4% maximum health and Qi per rank.', effects:{hpPct:.04,qiPct:.04} },
      { id:'g_heavenly_judgment', path:'good', tier:5, threshold:40, maxRank:3, cost:26, prereq:['g_compassionate_reversal','g_sanctified_clones'], icon:'⚡', nameZh:'天道降魔', nameEn:'Heavenly Demon-Subduing', descZh:'圣光触发时每级额外造成 18 点范围伤害。', descEn:'Holy procs deal 18 additional area damage per rank.', effects:{holyDamage:18} },
      { id:'g_victorious_buddha', path:'good', tier:6, threshold:60, maxRank:1, cost:45, prereq:['g_bodhi_heart','g_heavenly_judgment'], icon:'☸️', nameZh:'斗战胜佛心印', nameEn:'Victorious Fighting Buddha Seal', descZh:'每级伤害减免 +1%（20级共 +20%）；第三击必定爆发圣光。', descEn:'+1% damage reduction per rank (+20% at rank 20); every combo finisher releases holy light.', effects:{damageReduction:.01,goodCapstone:1} },

      { id:'n_centered_body', path:'neutral', tier:1, maxAbs:18, maxRank:20, cost:8, prereq:[], icon:'☯️', nameZh:'中正道体', nameEn:'Centered Body', descZh:'每级伤害 +1%、生命 +1%；20级共 +20%。', descEn:'+1% damage and maximum health per rank; +20% at rank 20.', effects:{damage:.01,hpPct:.01} },
      { id:'n_tempered_staff', path:'neutral', tier:1, maxAbs:18, maxRank:20, cost:8, prereq:[], icon:'🦯', nameZh:'刚柔如意', nameEn:'Tempered Ruyi', descZh:'每级攻速 +1%、护甲 +2；20级共 +20% 攻速与 +40 护甲。', descEn:'+1% attack speed and +2 armor per rank; +20% and +40 armor at rank 20.', effects:{attackSpeed:.01,armor:2} },
      { id:'n_even_breath', path:'neutral', tier:2, maxAbs:16, maxRank:20, cost:11, prereq:['n_centered_body'], icon:'🌬️', nameZh:'调息归一', nameEn:'Even Breath', descZh:'每级真气回复 +0.12/s、真气 +1%；20级共 +2.4/s 与 +20%。', descEn:'+0.12 Qi regeneration per second and +1% maximum Qi per rank; +2.4/s and +20% at rank 20.', effects:{qiRegen:.12,qiPct:.01} },
      { id:'n_adaptive_guard', path:'neutral', tier:2, maxAbs:16, maxRank:20, cost:11, prereq:['n_tempered_staff'], icon:'🌓', nameZh:'随缘护身', nameEn:'Adaptive Guard', descZh:'每级减伤 +0.5%、伤害 +0.5%；20级各 +10%。', descEn:'+0.5% damage reduction and damage per rank; +10% each at rank 20.', effects:{damageReduction:.005,damage:.005} },
      { id:'n_yinyang_staff', path:'neutral', tier:3, maxAbs:14, maxRank:20, cost:14, prereq:['n_even_breath','n_adaptive_guard'], icon:'⚪', nameZh:'阴阳棍意', nameEn:'Yin-Yang Staff Intent', descZh:'每级 +2% 平衡冲击率，同时造成圣与幽伤害；20级共 +40%。', descEn:'+2% balanced-impact chance per rank, mixing holy and void force; +40% at rank 20.', effects:{balanceChance:.02} },
      { id:'n_flowing_step', path:'neutral', tier:3, maxAbs:14, maxRank:20, cost:14, prereq:['n_adaptive_guard'], icon:'💨', nameZh:'无偏云步', nameEn:'Unbiased Cloudstep', descZh:'每级移速 +1.5%、闪避护盾 +3；20级共 +30% 与 +60 护盾。', descEn:'+1.5% movement speed and +3 dash barrier per rank; +30% and +60 barrier at rank 20.', effects:{speed:.015,dashBarrier:3} },
      { id:'n_measured_force', path:'neutral', tier:3, maxAbs:14, maxRank:20, cost:14, prereq:['n_even_breath'], icon:'🎯', nameZh:'收放有度', nameEn:'Measured Force', descZh:'每级暴击率 +1%、首领伤害 +1%；20级各 +20%。', descEn:'+1% critical chance and boss damage per rank; +20% each at rank 20.', effects:{crit:.01,bossDamage:.01} },
      { id:'n_balanced_return', path:'neutral', tier:4, maxAbs:12, maxRank:20, cost:18, prereq:['n_yinyang_staff','n_flowing_step'], icon:'↩️', nameZh:'去回两仪', nameEn:'Twofold Return', descZh:'飞棒每级伤害 +8%，吸血 +0.1%；20级共 +160% 飞棒伤害与 +2% 吸血。', descEn:'Flying staff gains 8% damage and 0.1% life leech per rank; +160% and +2% at rank 20.', effects:{specialDamage:.08,lifeLeech:.001} },
      { id:'n_dual_aspect', path:'neutral', tier:4, maxAbs:12, maxRank:20, cost:19, prereq:['n_yinyang_staff','n_measured_force'], icon:'🔵', nameZh:'两仪同辉', nameEn:'Dual Aspect', descZh:'每级圣光与幽冥冲击伤害 +10；20级各 +200。', descEn:'Holy and void aspects gain 10 proc damage per rank; +200 each at rank 20.', effects:{holyDamage:10,voidDamage:10} },
      { id:'n_middle_way', path:'neutral', tier:4, maxAbs:10, maxRank:20, cost:20, prereq:['n_flowing_step','n_measured_force'], icon:'⚖️', nameZh:'不偏之道', nameEn:'The Middle Way', descZh:'每级伤害、生命、攻速、减伤各 +1%；20级各 +20%。', descEn:'+1% damage, health, attack speed, and damage reduction per rank; +20% each at rank 20.', effects:{damage:.01,hpPct:.01,attackSpeed:.01,damageReduction:.01} },
      { id:'n_harmony', path:'neutral', tier:5, maxAbs:8, maxRank:20, cost:25, prereq:['n_balanced_return','n_dual_aspect'], icon:'🔄', nameZh:'万法调和', nameEn:'Harmony of Ten Thousand Arts', descZh:'每级 +3% 平衡冲击率；触发时回气并按伤害回复 0.2% 气血，受全局吸血上限约束。', descEn:'+3% balanced-impact chance per rank; procs restore Qi and heal for 0.2% of damage, subject to the global leech cap.', effects:{balanceChance:.03,balanceHeal:.002} },
      { id:'n_sage_between', path:'neutral', tier:6, maxAbs:5, maxRank:20, cost:42, prereq:['n_middle_way','n_harmony'], icon:'🌗', nameZh:'两界齐天圣', nameEn:'Sage Between Two Realms', descZh:'每级伤害 +1%、减伤 +0.5%。5级显现阴阳双环；10级第三击必触发；15级冲击溅射；20级阴阳圆满。', descEn:'Each rank grants +1% damage and +0.5% damage reduction. Rank 5 adds twin rings; rank 10 guarantees a finisher proc; rank 15 splashes nearby enemies; rank 20 perfects the Yin-Yang burst.', effects:{damage:.01,damageReduction:.005,neutralCapstone:1} },

      { id:'e_crimson_might', path:'evil', tier:1, threshold:3, maxRank:5, cost:8, prereq:[], icon:'🩸', nameZh:'赤煞蛮力', nameEn:'Crimson Might', descZh:'每级伤害 +2%。', descEn:'+2% damage per rank.', effects:{damage:.02} },
      { id:'e_demon_haste', path:'evil', tier:1, threshold:3, maxRank:5, cost:8, prereq:[], icon:'👹', nameZh:'魔猿疾杀', nameEn:'Demon-Ape Haste', descZh:'每级攻速 +2%。', descEn:'+2% attack speed per rank.', effects:{attackSpeed:.02} },
      { id:'e_qi_siphon', path:'evil', tier:2, threshold:8, maxRank:5, cost:11, prereq:['e_crimson_might'], icon:'🫀', nameZh:'真炁掠夺', nameEn:'Zhen-Qi Siphon', descZh:'每级造成伤害的 0.15% 转为生命。', descEn:'Convert 0.15% of damage dealt into health per rank.', effects:{lifeLeech:.0015} },
      { id:'e_red_eyes', path:'evil', tier:2, threshold:8, maxRank:5, cost:11, prereq:['e_demon_haste'], icon:'🔴', nameZh:'赤目破妄', nameEn:'Red-Eyed Malice', descZh:'每级暴击率 +2%，双眼永久泛红。', descEn:'+2% critical chance per rank; Wukong’s eyes glow red.', effects:{crit:.02} },
      { id:'e_shadow_step', path:'evil', tier:3, threshold:15, maxRank:5, cost:14, prereq:['e_demon_haste','e_red_eyes'], icon:'🌑', nameZh:'魔影纵横', nameEn:'Demonic Shadowstep', descZh:'每级移速 +2%，闪避后下一击伤害 +5%。', descEn:'+2% movement speed; after dashing, next hit gains 5% damage per rank.', effects:{speed:.02,dashDamage:.05} },
      { id:'e_void_staff', path:'evil', tier:3, threshold:15, maxRank:5, cost:14, prereq:['e_crimson_might','e_qi_siphon'], icon:'🟣', nameZh:'幽冥如意', nameEn:'Nether Ruyi', descZh:'每级 +3% 幽冥爆裂率，金箍棒染成紫黑。', descEn:'+3% void-burst chance per rank; the Ruyi Staff darkens purple-black.', effects:{voidChance:.03} },
      { id:'e_soul_brand', path:'evil', tier:3, threshold:15, maxRank:5, cost:15, prereq:['e_qi_siphon'], icon:'💀', nameZh:'摄魂烙印', nameEn:'Soul Brand', descZh:'每级对首领伤害 +3%。', descEn:'+3% damage against bosses per rank.', effects:{bossDamage:.03} },
      { id:'e_blood_clones', path:'evil', tier:4, threshold:25, maxRank:3, cost:19, prereq:['e_shadow_step','e_void_staff'], icon:'🐵', nameZh:'血毫魔兵', nameEn:'Blood-Hair Legion', descZh:'分身每级伤害 +18%，消散时爆出紫黑煞气。', descEn:'Clones gain 18% damage per rank and burst into purple-black malice.', effects:{cloneDamage:.18,voidDamage:12} },
      { id:'e_ruthless', path:'evil', tier:4, threshold:25, maxRank:3, cost:19, prereq:['e_soul_brand'], icon:'🗡️', nameZh:'无情压制', nameEn:'Ruthless Pressure', descZh:'对半血以下敌人每级伤害 +8%。', descEn:'+8% damage per rank against enemies below half health.', effects:{executeDamage:.08} },
      { id:'e_abyssal_form', path:'evil', tier:4, threshold:25, maxRank:3, cost:20, prereq:['e_void_staff','e_soul_brand'], icon:'🔥', nameZh:'深渊魔躯', nameEn:'Abyssal War Body', descZh:'每级伤害 +4%、攻速 +3%、生命 −2%。', descEn:'+4% damage and +3% attack speed, but −2% maximum health per rank.', effects:{damage:.04,attackSpeed:.03,hpPct:-.02} },
      { id:'e_bloodstorm', path:'evil', tier:5, threshold:40, maxRank:3, cost:26, prereq:['e_blood_clones','e_ruthless'], icon:'🌪️', nameZh:'血海棍风', nameEn:'Bloodstorm Staff Art', descZh:'幽冥触发时每级额外造成 25 点范围伤害。', descEn:'Void procs deal 25 additional area damage per rank.', effects:{voidDamage:25} },
      { id:'e_demon_sage', path:'evil', tier:6, threshold:60, maxRank:1, cost:45, prereq:['e_abyssal_form','e_bloodstorm'], icon:'👑', nameZh:'混世魔圣', nameEn:'World-Defying Demon Sage', descZh:'每级伤害与攻速 +1%、吸血 +0.05%（20级共 +20%、+20%、+1%）；红目魔焰完全显现。', descEn:'+1% damage and attack speed and +0.05% life leech per rank (+20%, +20%, and +1% at rank 20); red-eyed demon flame fully manifests.', effects:{damage:.01,attackSpeed:.01,lifeLeech:.0005,evilCapstone:1} }
    ].map(skill => ({ ...skill, maxRank: KARMA_SKILL_MAX_RANK }));

    function getAlignmentPath(score = alignmentScore) {
      if (score >= ALIGNMENT_VISUAL_THRESHOLD) return 'good';
      if (score <= -ALIGNMENT_VISUAL_THRESHOLD) return 'evil';
      return 'neutral';
    }

    function getAlignmentPalette(score = alignmentScore) {
      const path = getAlignmentPath(score);
      if (path === 'good') return { path, primary:'#dbeafe', secondary:'#60a5fa', accent:'#facc15', dark:'#0c4a6e' };
      if (path === 'evil') return { path, primary:'#ef4444', secondary:'#a855f7', accent:'#111827', dark:'#2e1065' };
      return { path, primary:'#facc15', secondary:'#c084fc', accent:'#f8fafc', dark:'#422006' };
    }

    function getTitleKarmaStage(score = alignmentScore) {
      if (score >= 60) return { id:'good_3', path:'good', asset:'title_karma_good_3', tier:3 };
      if (score >= 25) return { id:'good_2', path:'good', asset:'title_karma_good_2', tier:2 };
      if (score >= 8) return { id:'good_1', path:'good', asset:'title_karma_good_1', tier:1 };
      if (score <= -60) return { id:'evil_3', path:'evil', asset:'title_karma_evil_3', tier:3 };
      if (score <= -25) return { id:'evil_2', path:'evil', asset:'title_karma_evil_2', tier:2 };
      if (score <= -8) return { id:'evil_1', path:'evil', asset:'title_karma_evil_1', tier:1 };
      return { id:'neutral', path:'neutral', asset:'title_karma_neutral', tier:0 };
    }

    function getAlignmentCombatStage(score = alignmentScore) {
      const stage = getTitleKarmaStage(score);
      if (!stage.tier) return null;
      return { ...stage, asset: `wukong_${stage.id}` };
    }

    const RUYI_COMBO_WINDOW = 1.35;
    const RUYI_CONTACT_FRAME_COUNT = 8;
    const RUYI_CONTACT_PROFILES = Object.freeze({
      arc: Object.freeze({ id:'arc', row:0, mode:'arc', contactFrame:4, thickness:12, innerRadius:34, baseReach:132, sourcePivotX:104, sourcePivotY:208, sourceReach:201, sourceAxis:0, bodyPivotX:176, bodyFootY:344 }),
      thrust: Object.freeze({ id:'thrust', row:1, mode:'thrust', contactFrame:4, thickness:10, startOffset:30, baseReach:154, sourcePivotX:40, sourcePivotY:275, sourceReach:304, sourceAxis:.04, bodyPivotX:176, bodyFootY:340 }),
      slam: Object.freeze({ id:'slam', row:2, mode:'slam', contactFrame:5, impactRadius:34, baseReach:142, sourcePivotX:142, sourcePivotY:170, sourceReach:165, sourceAxis:1.24, bodyPivotX:190, bodyFootY:342 }),
      spin: Object.freeze({ id:'spin', row:3, mode:'ring', contactFrame:5, thickness:12, innerRadius:34, baseReach:138, sourcePivotX:192, sourcePivotY:192, sourceReach:115, sourceAxis:0, bodyPivotX:190, bodyFootY:340 }),
    });
    const RUYI_TEMPORAL_MOVE_ROWS = Object.freeze({ arc:0, thrust:1, slam:2, spin:3 });
    // Literal source-cell coordinates measured on every generated body frame:
    // four moves x eight directions x eight time poses = 256 hand pivots.
    // The project-bound JSON is injected here during the single-file build.
    const RUYI_TEMPORAL_GRIP_ANCHORS = Object.freeze(%RUYI_GRIP_ANCHORS%);

    // Explicit source grip/tip endpoints for every generated weapon frame.
    // Image generation deliberately changes the pose between frames, so a
    // single row pivot would create invisible reach (especially during spin).
    // Runtime normalizes each real painted staff segment to the exact gameplay
    // shaft rather than pretending every frame has the same pivot or angle.
    const RUYI_WEAPON_SOURCE_SEGMENTS = Object.freeze({
      arc: Object.freeze([
        [81,207,295,207], [94,213,279,96], [83,208,272,59], [100,246,292,156],
        [91,208,302,203], [98,178,306,313], [135,220,304,114], [97,207,298,207],
      ]),
      thrust: Object.freeze([
        [83,291,235,290], [199,293,339,296], [198,296,340,286], [41,294,218,289],
        [43,287,329,274], [63,292,338,272], [216,296,339,282], [174,287,331,287],
      ]),
      slam: Object.freeze([
        [158,116,172,329], [129,177,217,311], [159,42,160,250], [128,158,207,328],
        [113,154,216,346], [130,190,219,343], [201,125,139,328], [217,135,132,330],
      ]),
      spin: Object.freeze([
        [303,211,122,214], [302,241,185,97], [272,256,265,52], [173,243,307,94],
        [96,221,306,211], [192,124,302,255], [183,127,189,331], [193,125,92,256],
      ]),
    });

    function getRuyiDirectionalBodyFrameForAngle(angle) {
      const sector = ((Math.round(angle / (Math.PI / 4)) % 8) + 8) % 8;
      return [0, 7, 6, 5, 4, 3, 2, 1][sector];
    }

    function getRuyiTemporalFrame(progress) {
      return Math.min(7, Math.floor(Math.max(0, Math.min(.999, progress)) * 8));
    }

    function getRuyiTemporalBodyRow(profile, angle) {
      const moveRow = RUYI_TEMPORAL_MOVE_ROWS[profile?.id] ?? 0;
      return moveRow * 8 + getRuyiDirectionalBodyFrameForAngle(angle);
    }

    function getRuyiTemporalAtlasKey(path = 'neutral') {
      return `wukong_ruyi_temporal_${path === 'good' || path === 'evil' ? path : 'neutral'}`;
    }

    function getRuyiTemporalHandAnchor(angle, profile, progress, scaleFactor = 1) {
      const frame = getRuyiTemporalFrame(progress);
      const direction = getRuyiDirectionalBodyFrameForAngle(angle);
      const sourceAnchor = (RUYI_TEMPORAL_GRIP_ANCHORS[profile?.id] || RUYI_TEMPORAL_GRIP_ANCHORS.arc)[direction][frame];
      const bodyScale = .90 * scaleFactor;
      return {
        x:(sourceAnchor[0] - 96) * bodyScale,
        y:44 + (sourceAnchor[1] - 160) * bodyScale,
      };
    }

    function getRuyiWeaponSourceSegment(profile, frame) {
      const values = (RUYI_WEAPON_SOURCE_SEGMENTS[profile?.id] || RUYI_WEAPON_SOURCE_SEGMENTS.arc)[Math.max(0, Math.min(7, frame | 0))];
      const dx = values[2] - values[0], dy = values[3] - values[1];
      return { pivotX:values[0], pivotY:values[1], tipX:values[2], tipY:values[3], angle:Math.atan2(dy, dx), length:Math.hypot(dx, dy) };
    }

    function ruyiAngleDifference(a, b) {
      let value = Math.abs(a - b) % (Math.PI * 2);
      if (value > Math.PI) value = Math.PI * 2 - value;
      return value;
    }

    function ruyiPointToSegmentDistance(px, py, ax, ay, bx, by) {
      const dx = bx - ax;
      const dy = by - ay;
      const denom = dx * dx + dy * dy;
      if (denom <= .00001) return Math.hypot(px - ax, py - ay);
      const t = Math.max(0, Math.min(1, ((px - ax) * dx + (py - ay) * dy) / denom));
      return Math.hypot(px - (ax + dx * t), py - (ay + dy * t));
    }

    function getRuyiWorldShaft(originX, originY, angle, profile, progress, reach, handAnchor = {x:0,y:0}) {
      const frame = getRuyiTemporalFrame(progress);
      const shaftAngle = profile?.mode === 'ring' ? getRuyiSweepFrameAngle(progress, angle) : angle;
      const gripX = originX + (handAnchor?.x || 0);
      const gripY = originY + (handAnchor?.y || 0);
      const paintedReach = Math.max(1, reach || profile?.baseReach || 1);
      const inner = profile?.mode === 'thrust' ? (profile.startOffset ?? 0) : (profile?.innerRadius ?? 0);
      return {
        frame, angle:shaftAngle, originX:gripX, originY:gripY,
        startX:gripX + Math.cos(shaftAngle) * inner,
        startY:gripY + Math.sin(shaftAngle) * inner,
        endX:gripX + Math.cos(shaftAngle) * paintedReach,
        endY:gripY + Math.sin(shaftAngle) * paintedReach,
        reach:paintedReach,
      };
    }

    function isRuyiContactHit(shape, enemyX, enemyY, enemyRadius = 0) {
      if (shape.mode === 'slam') {
        return Math.hypot(enemyX - shape.endX, enemyY - shape.endY) <= shape.impactRadius + enemyRadius;
      }
      // Arc, thrust and progressive-spin frames expose one exact painted shaft.
      // The authored start/end points are shared with rendering and impact FX.
      return ruyiPointToSegmentDistance(enemyX, enemyY, shape.startX, shape.startY, shape.endX, shape.endY) <= shape.thickness + enemyRadius;
    }

    function getRuyiContactPoint(shape, enemyX, enemyY) {
      if (shape.mode === 'slam') {
        return { x:shape.endX, y:shape.endY };
      }
      const ax = shape.startX, ay = shape.startY;
      const bx = shape.endX, by = shape.endY;
      const segmentX = bx - ax, segmentY = by - ay;
      const t = Math.max(0, Math.min(1, ((enemyX - ax) * segmentX + (enemyY - ay) * segmentY) / Math.max(.00001, segmentX * segmentX + segmentY * segmentY)));
      return { x:ax + segmentX * t, y:ay + segmentY * t };
    }

    function getRuyiSweepFrameAngle(progress, baseAngle = 0) {
      // The generated spin strip has eight authored 45-degree contact poses:
      // left, upper-left, up, upper-right, right, lower-right, down, lower-left.
      // Quantizing collision to the visible frame prevents a hidden continuous
      // ring collider from striking before the painted staff arrives.
      const frame = Math.min(7, Math.floor(Math.max(0, Math.min(.999, progress)) * 8));
      return baseAngle - Math.PI + frame * (Math.PI / 4);
    }

    function verifyRuyiContactGeometryContract() {
      const thrust = { ...getRuyiWorldShaft(0, 0, 0, RUYI_CONTACT_PROFILES.thrust, .5, 140), mode:'thrust', thickness:10 };
      const slam = { ...getRuyiWorldShaft(0, 0, 0, RUYI_CONTACT_PROFILES.slam, .625, 140), mode:'slam', impactRadius:34 };
      const arc = { ...getRuyiWorldShaft(0, 0, 0, RUYI_CONTACT_PROFILES.arc, .5, 132), mode:'arc', thickness:12 };
      const neAnchor = getRuyiTemporalHandAnchor(-Math.PI / 4, RUYI_CONTACT_PROFILES.arc, .5);
      const neShaft = getRuyiWorldShaft(10, 20, -Math.PI / 4, RUYI_CONTACT_PROFILES.arc, .5, 132, neAnchor);
      const measuredGripCount = Object.values(RUYI_TEMPORAL_GRIP_ANCHORS)
        .reduce((total, directions) => total + directions.reduce((subtotal, frames) => subtotal + frames.length, 0), 0);
      return isRuyiContactHit(thrust, 140, 9, 0)
        && !isRuyiContactHit(thrust, 140, 13, 0)
        && isRuyiContactHit(slam, 173, 0, 0)
        && !isRuyiContactHit(slam, 176, 0, 0)
        && isRuyiContactHit(arc, 132, 0, 0)
        && isRuyiContactHit(arc, 96, 0, 0)
        && !isRuyiContactHit(arc, 0, 100, 24)
        && !isRuyiContactHit(arc, 18, 0, 0)
        && !isRuyiContactHit(arc, 157, 0, 0)
        && Math.abs(getRuyiSweepFrameAngle(.51, 0)) < .001
        && getRuyiDirectionalBodyFrameForAngle(-Math.PI / 2) === 2
        && getRuyiTemporalFrame(.61) === 4
        && getRuyiTemporalBodyRow(RUYI_CONTACT_PROFILES.slam, Math.PI / 2) === 22
        && measuredGripCount === 256
        && Math.abs(neShaft.originX - (10 + neAnchor.x)) < .001
        && Math.abs(neShaft.originY - (20 + neAnchor.y)) < .001
        && RUYI_WEAPON_SOURCE_SEGMENTS.spin.length === 8
        && RUYI_WEAPON_SOURCE_SEGMENTS.spin.every((_, frame) => getRuyiWeaponSourceSegment(RUYI_CONTACT_PROFILES.spin, frame).length > 150);
    }
    if (!verifyRuyiContactGeometryContract()) throw new Error('Ruyi contact geometry contract failed');

    function getRuyiContactProfile(currentCombo, comboMove = null) {
      const effect = comboMove?.effect;
      if (effect === 'verdict' || effect === 'pierce') return RUYI_CONTACT_PROFILES.thrust;
      if (effect === 'spin' || effect === 'reversal' || effect === 'launch') return RUYI_CONTACT_PROFILES.spin;
      if (effect === 'fissure' || effect === 'beginner_slam' || currentCombo === 2) return RUYI_CONTACT_PROFILES.slam;
      if (currentCombo === 1) return RUYI_CONTACT_PROFILES.spin;
      return RUYI_CONTACT_PROFILES.arc;
    }

    function getRuyiAuthoredProgress(attackProgress, profile, contactAt) {
      if (!profile) return Math.max(0, Math.min(.999, attackProgress));
      const inputContact = Math.max(.05, Math.min(.95, contactAt ?? (profile.contactFrame / RUYI_CONTACT_FRAME_COUNT)));
      const authoredContact = profile.contactFrame / RUYI_CONTACT_FRAME_COUNT;
      if (attackProgress <= inputContact) {
        return Math.max(0, Math.min(.999, (attackProgress / inputContact) * authoredContact));
      }
      return Math.max(0, Math.min(.999, authoredContact + ((attackProgress - inputContact) / (1 - inputContact)) * (1 - authoredContact)));
    }

    const RUYI_COMBOS = [
      { id:'great_sage_basics', pattern:'LLL', damage:1.18, reach:1.12, duration:1.00, effect:'beginner_slam', animRow:0, contactAt:.68, beginner:true,
        nameZh:'大圣入门三式', nameEn:'Great Sage Beginner Chain', descZh:'连续左键即可施展：前方弧斩、周身横扫、最后跃起过顶裂地。', descEn:'Simply press left three times: forward arc, all-around sweep, then a leaping overhead ground slam.' },
      { id:'rising_dragon', pattern:'LLR', damage:1.24, reach:1.08, duration:1.04, effect:'launch', animRow:1, contactAt:.62,
        nameZh:'腾龙挑岳', nameEn:'Rising-Dragon Ascent', descZh:'两记轻棍接蹲身上挑，从下向上击飞前方妖魔。', descEn:'Two light strikes flow into a low-crouch rising uppercut that launches foes.' },
      { id:'moon_reversal', pattern:'LRR', damage:1.32, reach:1.12, duration:1.08, effect:'reversal', animRow:2, contactAt:.58,
        nameZh:'倒卷残月', nameEn:'Reversing Crescent', descZh:'轻棍诱敌后突然回身飞踢，以金箍棒护住身侧。', descEn:'A light feint reverses into a turning flying kick while the staff guards Wukong’s flank.' },
      { id:'heaven_splitter', pattern:'LLRR', damage:1.48, reach:1.20, duration:1.12, effect:'fissure', animRow:3, contactAt:.66,
        nameZh:'破天四式', nameEn:'Fourfold Heaven Splitter', descZh:'轻轻重重，最终双手高举金箍棒从头顶劈裂地面。', descEn:'Light-light-heavy-heavy, ending in a two-handed overhead blow that splits the ground.' },
      { id:'cloud_weave', pattern:'LRLR', damage:1.40, reach:1.16, duration:.94, effect:'spin', animRow:4, contactAt:.58,
        nameZh:'织云回风', nameEn:'Cloud-Weaving Reversal', descZh:'轻重交替，悟空完整旋身一周，以横扫棍风护住周身。', descEn:'Alternating strikes flow into a complete 360-degree horizontal staff sweep.' },
      { id:'havoc_cascade', pattern:'LLLRR', damage:1.72, reach:1.28, duration:1.18, effect:'nova', animRow:5, contactAt:.60,
        nameZh:'大闹天宫五连', nameEn:'Havoc-in-Heaven Cascade', descZh:'三快两重，最后撑棍腾空飞踢并爆发善光或魔煞震波。', descEn:'Three fast blows and two heavies end in a staff-vault flying kick and karmic shockwave.' },
      { id:'karma_verdict', pattern:'LLRLR', damage:1.66, reach:1.24, duration:1.02, effect:'verdict', animRow:6, contactAt:.62,
        nameZh:'因果判天棍', nameEn:'Karmic Verdict Staff', descZh:'虚实交错的五式棍法，最后将金箍棒笔直突刺，依善恶改变威力。', descEn:'A five-input feinting art ending in a long straight staff thrust whose power follows current karma.' }
    ];

    const ERLANG_COMBO_WINDOW = 1.20;
    const ERLANG_COMBOS = [
      { id:'heaven_piercing_drill', pattern:'LLL', damage:1.22, reach:1.16, duration:.94, effect:'pierce', animRow:0, contactAt:.64, beginner:true,
        nameZh:'贯天三尖钻', nameEn:'Heaven-Piercing Drill', descZh:'三次左键的入门枪路：低势蓄力、连续突刺、以三尖两刃锋贯穿前列。', descEn:'Beginner left-click chain: low guard, driving thrusts, then a piercing three-pointed spear finish.' },
      { id:'crescent_dragon_rise', pattern:'LLR', damage:1.38, reach:1.12, duration:1.02, effect:'launch', animRow:1, contactAt:.66,
        nameZh:'月牙升龙挑', nameEn:'Crescent-Dragon Rise', descZh:'两记快枪接反手月牙上挑，将近身妖将挑至半空。', descEn:'Two fast spear cuts reverse into a crescent uppercut that launches nearby foes.' },
      { id:'hound_master_pin', pattern:'LRL', damage:1.34, reach:1.18, duration:1.04, effect:'hound_pin', animRow:2, contactAt:.62,
        nameZh:'神犬合围锁', nameEn:'Hound-and-Master Pin', descZh:'杨戬佯攻牵制，哮天犬从侧翼扑咬，被命中的目标定身并承受双重夹击。', descEn:'Yang Jian feints while Xiaotianquan pounces from the flank, pinning the target for a two-sided strike.' },
      { id:'guanjiang_heavenly_wheel', pattern:'LRR', damage:1.48, reach:1.30, duration:1.08, effect:'spin', animRow:3, contactAt:.60,
        nameZh:'灌江天轮斩', nameEn:'Guanjiang Heavenly Wheel', descZh:'轻枪引势后双重横扫，完整旋身一周击退四面来敌。', descEn:'A light feint flows into two broad sweeps and a full-body heavenly wheel that clears every side.' },
      { id:'third_eye_judgment', pattern:'LLRR', damage:1.78, reach:1.34, duration:1.16, effect:'third_eye', animRow:4, contactAt:.72,
        nameZh:'天眼诛邪判', nameEn:'Third-Eye Judgment', descZh:'四式终结技：腾空举枪、天眼锁敌、雷霆从天而降。', descEn:'Four-input finisher: airborne spear stance, Third-Eye lock, then a descending bolt of divine judgment.' }
    ];

    function getActiveComboDefinitions() {
      return gameState?.playableHero === 'erlang' ? ERLANG_COMBOS : RUYI_COMBOS;
    }

    function getActiveComboWindow() {
      return gameState?.playableHero === 'erlang' ? ERLANG_COMBO_WINDOW : RUYI_COMBO_WINDOW;
    }

    function getRuyiComboPresentation(combo) {
      const stage = getAlignmentCombatStage();
      if (stage?.path === 'evil') {
        return {
          name: uiText(`魔·${combo.nameZh}`, `Demonic ${combo.nameEn}`),
          desc: uiText(`${combo.descZh} 魔煞收式强化伤害与压制。`, `${combo.descEn} The demonic finish emphasizes damage and ruthless pressure.`)
        };
      }
      if (stage?.path === 'good') {
        return {
          name: uiText(`圣·${combo.nameZh}`, `Sacred ${combo.nameEn}`),
          desc: uiText(`${combo.descZh} 圣光收式强化范围与护身。`, `${combo.descEn} The sacred finish emphasizes reach and protection.`)
        };
      }
      return { name: uiText(combo.nameZh, combo.nameEn), desc: uiText(combo.descZh, combo.descEn) };
    }

    function getActiveComboPresentation(combo) {
      if (gameState?.playableHero === 'erlang') {
        return { name: uiText(combo.nameZh, combo.nameEn), desc: uiText(combo.descZh, combo.descEn) };
      }
      return getRuyiComboPresentation(combo);
    }

    function getTitleKarmaLabel(stage, score = alignmentScore) {
      if (stage.id === 'good_1') return uiText(`🪽 善念初明 · 善 +${score}`, `🪽 Good Karma I · Dawn of Mercy +${score}`);
      if (stage.id === 'good_2') return uiText(`🪷 慈悲护世 · 善 +${score}`, `🪷 Good Karma II · Celestial Guardian +${score}`);
      if (stage.id === 'good_3') return uiText(`☸ 斗战胜佛心 · 善 +${score}`, `☸ Good Karma III · Victorious Buddha Heart +${score}`);
      if (stage.id === 'evil_1') return uiText(`🔻 煞念初生 · 恶 ${score}`, `🔻 Evil Karma I · Rising Malice ${score}`);
      if (stage.id === 'evil_2') return uiText(`🩸 魔猿霸世 · 恶 ${score}`, `🩸 Evil Karma II · Tyrant Monkey King ${score}`);
      if (stage.id === 'evil_3') return uiText(`👑 混世魔圣 · 恶 ${score}`, `👑 Evil Karma III · World-Defying Demon Sage ${score}`);
      const signedScore = score > 0 ? `+${score}` : `${score}`;
      return uiText(`☯ 中道未定 · 因果 ${signedScore}`, `☯ Unwritten Karma · Balance ${signedScore}`);
    }

    function updateTitleKarmaPresentation() {
      if (!startScreen) return;
      const stage = getTitleKarmaStage();
      const titleAsset = ASSETS[stage.asset] || ASSETS.title_karma_neutral || ASSETS.title_key_art;
      if (titleAsset) startScreen.style.backgroundImage = `url("${titleAsset}")`;
      startScreen.dataset.karmaPath = stage.path;
      startScreen.dataset.karmaStage = stage.id;
      const badge = document.getElementById('title-karma-state');
      if (badge) {
        badge.className = `title-karma-state ${stage.path}`;
        badge.innerText = getTitleKarmaLabel(stage);
        badge.setAttribute('aria-label', uiText(`当前因果境界：${badge.innerText}`, `Current karma presentation: ${badge.innerText}`));
      }
    }

    function alignmentThresholdMet(skill) {
      if (skill.path === 'good') return alignmentScore >= skill.threshold;
      if (skill.path === 'evil') return alignmentScore <= -skill.threshold;
      return Math.abs(alignmentScore) <= skill.maxAbs;
    }

    function isAlignmentSkillActive(skillOrId) {
      const skill = typeof skillOrId === 'string' ? ALIGNMENT_SKILLS.find(item => item.id === skillOrId) : skillOrId;
      if (!skill || (alignmentSkillRanks[skill.id] || 0) <= 0 || !alignmentThresholdMet(skill)) return false;
      return (skill.prereq || []).every(id => {
        const prerequisite = ALIGNMENT_SKILLS.find(item => item.id === id);
        return (alignmentSkillRanks[id] || 0) > 0 && alignmentThresholdMet(prerequisite);
      });
    }

    function getActiveAlignmentEffects() {
      const totals = {};
      ALIGNMENT_SKILLS.forEach(skill => {
        const rank = Math.min(skill.maxRank, alignmentSkillRanks[skill.id] || 0);
        if (!rank || !isAlignmentSkillActive(skill)) return;
        Object.entries(skill.effects || {}).forEach(([key, value]) => { totals[key] = (totals[key] || 0) + value * rank; });
      });
      return totals;
    }

    // Each transformation owns a combat loop. God boons remain secondary procs;
    // they never replace the form's movement, timing, or signature attack shape.
    const FORM_COMBAT_PROFILES = {
      dragon: {
        name: '苍龙·引雷控场', damage: 0.92, reach: 1.12, attackTime: 1.00,
        cooldown: 0.95, lunge: 0.75, crit: 0.02, knockback: 0.85, speed: 1.00,
        slashType: 'thunder', color: '#38bdf8', scale: 1.10,
        identity: '爪击串联水雷，擅长群体控制'
      },
      tiger: {
        name: '白虎·爆发狩猎', damage: 1.24, reach: 0.94, attackTime: 0.76,
        cooldown: 0.72, lunge: 1.18, crit: 0.20, knockback: 0.90, speed: 1.12,
        slashType: 'fire', color: '#f59e0b', scale: 1.08,
        identity: '快速扑击与流血，近身爆发最强'
      },
      roc: {
        name: '大鹏·风刃游击', damage: 0.88, reach: 1.34, attackTime: 0.82,
        cooldown: 0.75, lunge: 1.45, crit: 0.08, knockback: 1.20, speed: 1.25,
        slashType: 'wind', color: '#fbbf24', scale: 1.10,
        identity: '超长风刃与更快筋斗云，边走边打'
      },
      ape: {
        name: '魔猿·重拳崩山', damage: 1.62, reach: 1.28, attackTime: 1.34,
        cooldown: 1.25, lunge: 0.58, crit: 0.05, knockback: 1.70, speed: 0.78,
        slashType: 'golden', color: '#ea580c', scale: 1.42,
        identity: '慢速重拳、霸体与破阵震波'
      },
      tortoise: {
        name: '玄武·反击护阵', damage: 0.78, reach: 1.08, attackTime: 1.12,
        cooldown: 1.05, lunge: 0.35, crit: 0.00, knockback: 1.35, speed: 0.72,
        slashType: 'water', color: '#10b981', scale: 1.08,
        identity: '减伤回复、减速水环与重甲反击'
      }
    };

    const GOD_EN = {
      luban: { name: 'Divine Craftsman · Lu Ban', title: 'Patron of All Crafts · Celestial Smith', quote: '“A divine weapon is born from ten thousand hammer blows. Let me restore the Ruyi Staff’s world-shaking power!”', boons: {
        luban_heavy_forge: ['Mountain-Weight Reforging', 'The staff becomes a colossal heavy form: attack speed −35%, base damage +250%, and strikes rupture the ground.'],
        luban_extend_reach: ['Ruyi Infinite Extension', 'The flying staff becomes a narrow heaven-reaching spear: +65% range and rising damage as it pierces new enemies.'],
        luban_chain_staff: ['Nine-Section Dragon Chain', 'The staff circles once at maximum range, granting one capped extra hit per enemy before returning.'],
        luban_anvil_strike: ['Hundred-Forging Strike', 'Normal attacks add 55 armor-piercing damage.'],
        luban_divine_gear: ['Celestial Gear Array', 'Create a rotating Bagua gear array that damages enemies and reflects hostile projectiles.'],
        luban_clockwork_kite: ['Clockwork Kite Companion', 'Summon a wooden celestial kite that fires an explosive missile every 3 seconds.'],
        luban_masterwork: ['Peerless Craftsmanship', 'Peaches grant 50% more attributes and permanently add 50 armor.']
      }},
      erlangshen: { name: 'Erlang, Illustrious Sage · Yang Jian', title: 'Lord of Guanjiang and the All-Seeing Third Eye', quote: '“Face my three-pointed spear! Xiaotianquan, seize the demons that block the western journey!”', boons: {
        erlang_strike: ['Three-Pointed Army Breaker', 'Normal attacks summon spear-lightning for 45 extra armor-piercing damage.'],
        erlang_ring: ['Third-Eye Radiance Array', 'Enemies inside take 40% more damage while the array fires radiant pulses.'],
        erlang_dash: ['Thunderstep', 'Dashing calls down judgment lightning for 40 area damage.'],
        erlang_special: ['Heaven-Rending Spear Spin', 'The flying staff pierces on both passes and calls down Third-Eye lightning.'],
        erlang_hound: ['Xiaotianquan Soul Bite', 'Permanently summon Xiaotianquan to pursue, pounce, bite for 80 damage, and stun enemies.'],
        erlang_truesight: ['Golden Eyes and Third Eye', 'All attacks gain +25% critical chance and +50% critical damage.']
      }},
      guanyin: { name: 'Guanyin, Bodhisattva of Compassion', title: 'Merciful Savior of the Southern Sea', quote: '“Accept the willow dew from this pure vase. May your golden body endure and the western journey succeed.”', boons: {
        guanyin_strike: ['Pure-Vase Dew Strike', 'Normal hits restore 1 health (+0.5 per rank), cleanse negative effects, and obey the short-window healing cap.'],
        guanyin_ring: ['Nine-Grade Lotus Array', 'Restore 8 health per second and slow enemies inside by 50%.'],
        guanyin_dash: ['Willow-Breeze Step', 'Dashing grants a jade shield that absorbs 30 damage for 2.5 seconds.'],
        guanyin_special: ['Compassionate Returning Tide', 'The flying staff reflects hostile projectiles and restores 15 Qi on its first hit.'],
        guanyin_nirvana: ['Undying Nirvana Body', 'Gain one revival; return with 70% maximum health and full Qi.']
      }},
      nezha: { name: 'Third Lotus Prince · Nezha', title: 'Marshal of the Central Altar', quote: '“Great Sage! Let us see whether my Wind-Fire Wheels outrun your Somersault Cloud!”', boons: {
        nezha_strike: ['Blazing Fire-Tip Spear', 'Normal attacks burn enemies for 60 damage over 3 seconds.'],
        nezha_ring: ['Universe-Ring Array', 'Rings ricochet among up to six enemies for 35 heavy damage each.'],
        nezha_dash: ['Wind-Fire Wheel Escape', 'Dashes leave a flame trail dealing 50 damage per second.'],
        nezha_special: ['Wind-Fire Returning Staff', 'Both staff passes inflict Samadhi Fire and knock enemies along the flight path.']
      }},
      laojun: { name: 'Supreme Elder Lord · Taishang Laojun', title: 'Daoist Ancestor · Lord of the Way and Virtue', quote: '“My Eight-Trigram Furnace forged your Fiery Golden Eyes. Show me how far your cultivation has grown!”', boons: {
        laojun_strike: ['Samadhi-Fire Seal', 'Normal attacks add 50 immortal-fire damage and melt enemy armor.'],
        laojun_ring: ['Eight-Trigram Furnace Array', 'The furnace array deals 40 refining damage every 0.3 seconds.'],
        laojun_special: ['Nine-Turn Elixir Spin', 'Every flying-staff hit detonates a Nine-Turn elixir flame.'],
        laojun_elixir: ['Nine-Turn Revival Elixir', 'Peaches gain an extra upgrade and immediately restore all health.']
      }},
      aoguang: { name: 'Ao Guang · Dragon King of the Eastern Sea', title: 'First of the Four Sea Dragon Kings', quote: '“You took the sea-calming iron! Now witness the fury of the Four Seas!”', boons: {
        aoguang_strike: ['Raging-Tide Strike', 'Normal attacks launch water blades for 40 extra damage and strong knockback.'],
        aoguang_ring: ['Abyssal Maelstrom', 'Summon a vortex that drags all enemies toward its center and crushes them.'],
        aoguang_special: ['Sea-Dragon Returning Spin', 'Both flying-staff passes can freeze demons in a coiling water-dragon current.']
      }},
      bullking: { name: 'Bull Demon King · Great Sage Who Pacifies Heaven', title: 'Leader of the Seven Great Sages', quote: '“Brother Wukong! Let the Seven Great Sages shake Lingxiao Palace once more!”', boons: {
        bull_strike: ['Mountain-Shaking Strike', 'Normal attacks deal 40% extra heavy damage and create a knockback quake.'],
        bull_special: ['Mountain-Breaking Iron Spin', 'The returning staff powers through long lines and blasts enemies along its path.'],
        bull_ironhide: ['Demon King Iron Body', 'Gain 50 armor, fully restored after avoiding damage for 8 seconds.']
      }},
      ironfan: { name: 'Princess Iron Fan', title: 'Immortal of Emerald-Cloud Mountain', quote: '“One fan extinguishes fire, the second raises wind, the third summons rain!”', boons: {
        ironfan_strike: ['Plantain-Fan Wind Blade', 'Normal attacks release piercing green wind blades for 35 extra damage.'],
        ironfan_special: ['World-Sweeping Gale', 'The flying staff carries a Plantain gale that slows and continuously pushes enemies.']
      }},
      buddha: { name: 'Tathagata Buddha · Shakyamuni', title: 'World-Honored One of Vulture Peak', quote: '“Compassion in one thought, demon-subduing in the next. Turn the divine needle as the wheel of Dharma.”', boons: {
        buddha_palm_strike: ['Five-Finger Tathagata Seal', 'The combo finisher calls down a palm impact for 40% of its damage in a small area.'],
        buddha_dharma_return: ['Dharma-Wheel Return', 'Outbound hits apply a seal; striking that target on return detonates the seal once per throw.'],
        buddha_equanimity: ['Selfless Dharma Body', 'While above half Qi, take 15% less damage; each rank adds 3%, capped at 24%.']
      }},
      yanluo: { name: 'King Yama · Lord of the Underworld', title: 'Fifth Judge of the Ten Courts', quote: '“Your name was erased from the Book of Life and Death. Now erase the lifespan of every demon!”', boons: {
        yanluo_strike: ['Judge’s Life-and-Death Seal', 'Normal attacks mark targets; after 3 seconds the seal explodes for 70 nether damage.'],
        yanluo_special: ['Yama’s Death-Claiming Spin', 'Flying-staff hits execute non-boss enemies left below 15% health.']
      }},
      change: { name: 'Chang’e and the Jade Rabbit', title: 'Lunar Lady of Guanghan Palace', quote: '“Moonlight washes the endless night. May its clear radiance guide the Great Sage.”', boons: {
        change_strike: ['Frost-Moon Strike', 'Normal attacks add 35 frost damage and freeze for 1.2 seconds.'],
        change_special: ['Bright-Moon Returning Ring', 'The staff becomes a moon wheel: a short freeze outward and a longer freeze on return.']
      }}
    };

    const DEFAULT_GOD_OFFER_WEIGHT = 3;
    const DEITY_SYNERGIES = {
      compassionate_lotus_return: { gods: ['buddha', 'guanyin'], color: '#fde68a' },
      furnace_forged_needle: { gods: ['laojun', 'luban'], color: '#fb923c' },
      wind_calls_rain: { gods: ['aoguang', 'ironfan'], color: '#67e8f9' }
    };

    const RUYI_WEAPON_PROFILES = {
      normal: { id: 'normal', damage: 1, range: 1, radius: 1, travelTime: 1, turnHold: 0 },
      titan: { id: 'titan', damage: 1.54, range: 0.90, radius: 1.35, travelTime: 1.18, turnHold: 0, turnSlam: true },
      extend: { id: 'extend', damage: 0.92, range: 1.65, radius: 0.72, travelTime: 0.82, turnHold: 0, pierceRamp: 0.12 },
      chain: { id: 'chain', damage: 0.78, range: 1.10, radius: 1.05, travelTime: 1, turnHold: 0.42, orbitRadius: 66 }
    };

    function getGodOfferWeight(godKey) {
      const weight = GODS[godKey]?.offerWeight;
      return Number.isFinite(weight) && weight > 0 ? weight : DEFAULT_GOD_OFFER_WEIGHT;
    }

    function pickWeightedGodKey(godKeys, roll = Math.random()) {
      if (!godKeys.length) return null;
      const totalWeight = godKeys.reduce((sum, key) => sum + getGodOfferWeight(key), 0);
      let cursor = Math.max(0, Math.min(1 - Number.EPSILON, roll)) * totalWeight;
      for (const key of godKeys) {
        cursor -= getGodOfferWeight(key);
        if (cursor < 0) return key;
      }
      return godKeys[godKeys.length - 1];
    }

    function takeWeightedGodKey(godKeys, roll = Math.random()) {
      const key = pickWeightedGodKey(godKeys, roll);
      if (key !== null) godKeys.splice(godKeys.indexOf(key), 1);
      return key;
    }

    function getGodDisplayName(godKey) {
      const god = GODS[godKey] || GODS.luban;
      return gameState.language === 'en' && GOD_EN[godKey] ? GOD_EN[godKey].name : god.name;
    }

    function getLocalizedBoon(boon, godKey) {
      if (gameState.language !== 'en') return boon;
      const translated = GOD_EN[godKey]?.boons?.[boon.id];
      return translated ? { ...boon, name: translated[0], desc: translated[1] } : boon;
    }

    function getBoonSlotKey(slot = '') {
      if (slot.includes('神兵') || slot.includes('重铸')) return 'weapon';
      if (slot.includes('普攻') || slot.includes('普通攻击')) return 'attack';
      if (slot.includes('特殊')) return 'special';
      if (slot.includes('法术') || slot.includes('法阵')) return 'cast';
      if (slot.includes('闪避') || slot.includes('身法')) return 'dash';
      if (slot.includes('绝技') || slot.includes('觉醒')) return 'hex';
      return null;
    }

    function getAttackComboPreview(level = 1) {
      const multiplier = 1 + 0.30 * (Math.max(1, level) - 1);
      const baseCombo = player?.weaponStyle === 'titan' ? [140, 190, 380] : [55, 75, 135];
      const staffFactor = player?.hasRuyiStaff === false ? 0.68 : 1;
      return baseCombo.map(value => Math.round(value * multiplier * staffFactor));
    }

    function cleanPreviewNumber(value, digits = 1) {
      const rounded = Math.round(Number(value) * (10 ** digits)) / (10 ** digits);
      return Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(digits);
    }

    function getPeachRankForecast(boon) {
      const level = Math.max(1, boon.level || 1);
      const elixirRanks = player.hasBoon('laojun_elixir') ? player.getBoonLevel('laojun_elixir') : 0;
      const guaranteedGain = 1 + elixirRanks;
      const masterworkChance = player.hasBoon('luban_masterwork') ? 0.5 : 0;
      return {
        level,
        guaranteedGain,
        minLevel: level + guaranteedGain,
        maxLevel: level + guaranteedGain + (masterworkChance > 0 ? 1 : 0),
        masterworkChance
      };
    }

    function previewComparison(labelZh, labelEn, before, afterMin, afterMax = afterMin, suffixZh = '', suffixEn = suffixZh) {
      const label = uiText(labelZh, labelEn);
      const suffix = uiText(suffixZh, suffixEn);
      const minText = `${afterMin}${suffix}`;
      const maxText = `${afterMax}${suffix}`;
      const afterText = String(afterMin) === String(afterMax)
        ? minText
        : `${minText} <span class="boon-upgrade-note">${uiText('（天工触发：', '(Masterwork proc: ')}${maxText}${uiText('）', ')')}</span>`;
      return `<div class="boon-upgrade-stat">${label}: <strong>${before}${suffix} → ${afterText}</strong></div>`;
    }

    function rankPreviewStat(labelZh, labelEn, forecast, valueAtRank, suffixZh = '', suffixEn = suffixZh) {
      return previewComparison(labelZh, labelEn, valueAtRank(forecast.level), valueAtRank(forecast.minLevel), valueAtRank(forecast.maxLevel), suffixZh, suffixEn);
    }

    const rankScaled = (base, step, rank) => cleanPreviewNumber(base * (1 + step * (Math.max(1, rank) - 1)));
    const percentScaled = (base, step, rank, cap = Infinity) => cleanPreviewNumber(Math.min(cap, base + step * (Math.max(1, rank) - 1)));
    const currentWeaponProfile = () => RUYI_WEAPON_PROFILES[player?.weaponStyle] || RUYI_WEAPON_PROFILES.normal;
    const currentWeaponRank = () => Math.max(1, player?.boons?.weapon?.level || 1);
    const currentSpecialRank = () => Math.max(1, player?.boons?.special?.level || 1);
    const hasStaffFactor = () => player?.hasRuyiStaff === false ? 0.68 : 1;
    const flyingStaffHitAtSpecialRank = rank => cleanPreviewNumber(120 * currentWeaponProfile().damage * (1 + 0.18 * (currentWeaponRank() - 1)) * (1 + 0.35 * (rank - 1)) * hasStaffFactor());
    const weaponHitAtRank = (profile, rank) => cleanPreviewNumber(120 * profile.damage * (1 + 0.18 * (rank - 1)) * (1 + 0.35 * (currentSpecialRank() - 1)) * hasStaffFactor());
    const weaponRangeAtRank = (profile, rank) => cleanPreviewNumber(720 * profile.range * (1 + Math.min(0.25, 0.05 * (rank - 1))) * (player?.hasRuyiStaff === false ? 0.72 : 1), 0);

    const BOON_UPGRADE_PREVIEWERS = Object.freeze({
      luban_heavy_forge: f => { const p = RUYI_WEAPON_PROFILES.titan; return [rankPreviewStat('飞棒去程基础伤害', 'Flying-staff outward base hit', f, r => weaponHitAtRank(p, r)), rankPreviewStat('最远射程', 'Maximum range', f, r => weaponRangeAtRank(p, r), ' 像素', ' px'), rankPreviewStat('尽头震地伤害', 'Turn-slam damage', f, r => cleanPreviewNumber(Number(weaponHitAtRank(p, r)) * 0.35))]; },
      luban_extend_reach: f => { const p = RUYI_WEAPON_PROFILES.extend; return [rankPreviewStat('飞棒去程基础伤害', 'Flying-staff outward base hit', f, r => weaponHitAtRank(p, r)), rankPreviewStat('最远射程', 'Maximum range', f, r => weaponRangeAtRank(p, r), ' 像素', ' px'), previewComparison('每贯穿一名新敌人增伤', 'Damage per new pierced target', '12', '12', '12', '%', '%')]; },
      luban_chain_staff: f => { const p = RUYI_WEAPON_PROFILES.chain; return [rankPreviewStat('飞棒去程基础伤害', 'Flying-staff outward base hit', f, r => weaponHitAtRank(p, r)), rankPreviewStat('最远射程', 'Maximum range', f, r => weaponRangeAtRank(p, r), ' 像素', ' px'), previewComparison('尽头环旋追加命中', 'Extra orbit hit at maximum range', '1', '1', '1', ' 次/敌', ' per enemy')]; },

      luban_anvil_strike: f => [rankPreviewStat('百炼穿甲伤害', 'Anvil armor-piercing damage', f, r => rankScaled(55, .35, r))],
      erlang_strike: f => [rankPreviewStat('三尖神雷伤害', 'Three-pointed lightning damage', f, r => rankScaled(45, .35, r)), rankPreviewStat('连锁神雷伤害', 'Chain-lightning damage', f, r => rankScaled(24, .35, r)), rankPreviewStat('最大连锁目标', 'Maximum chain targets', f, r => Math.min(3, r))],
      guanyin_strike: f => [rankPreviewStat('每次命中回复', 'Healing per hit', f, r => GUANYIN_STRIKE_HEAL_BASE + (r - 1) * GUANYIN_STRIKE_HEAL_PER_RANK, ' 气血', ' HP')],
      nezha_strike: f => [rankPreviewStat('三秒灼烧总伤害', 'Total burn damage over 3 seconds', f, r => rankScaled(60, .35, r))],
      laojun_strike: f => [rankPreviewStat('三昧真火额外伤害', 'Samadhi-Fire bonus damage', f, r => rankScaled(50, .35, r))],
      aoguang_strike: f => [rankPreviewStat('重水额外伤害', 'Tidal bonus damage', f, r => rankScaled(40, .35, r)), rankPreviewStat('击退强度', 'Knockback force', f, r => 130 + r * 20)],
      bull_strike: f => [rankPreviewStat('额外重击伤害', 'Extra heavy-hit damage', f, r => percentScaled(40, 10, r), '%', '%')],
      ironfan_strike: f => [rankPreviewStat('罡风穿甲伤害', 'Piercing gale damage', f, r => rankScaled(35, .35, r))],
      buddha_palm_strike: f => [rankPreviewStat('终结佛掌范围伤害', 'Finisher palm area damage', f, r => percentScaled(40, 8, r), '% 本次伤害', '% of hit damage')],
      yanluo_strike: f => [rankPreviewStat('三秒后死印伤害', 'Life-and-Death Seal after 3 seconds', f, r => rankScaled(70, .35, r))],
      change_strike: f => [rankPreviewStat('寒月额外伤害', 'Frost-Moon bonus damage', f, r => rankScaled(35, .35, r)), rankPreviewStat('冻结时间', 'Freeze duration', f, r => cleanPreviewNumber(1.2 + (r - 1) * .15), ' 秒', 's')],

      erlang_special: f => [rankPreviewStat('当前飞棒去程基础伤害', 'Current-loadout outward hit', f, flyingStaffHitAtSpecialRank), rankPreviewStat('每程神雷追加伤害', 'Lightning bonus on each pass', f, r => rankScaled(32, .22, r))],
      guanyin_special: f => [rankPreviewStat('当前飞棒去程基础伤害', 'Current-loadout outward hit', f, flyingStaffHitAtSpecialRank), previewComparison('首次命中回复真气', 'First-hit Qi restored', '15', '15', '15')],
      nezha_special: f => [rankPreviewStat('当前飞棒去程基础伤害', 'Current-loadout outward hit', f, flyingStaffHitAtSpecialRank), rankPreviewStat('每程三昧火灼烧', 'Samadhi burn on each pass', f, r => rankScaled(56, .22, r))],
      laojun_special: f => [rankPreviewStat('当前飞棒去程基础伤害', 'Current-loadout outward hit', f, flyingStaffHitAtSpecialRank), rankPreviewStat('每程金丹爆炸伤害', 'Elixir explosion on each pass', f, r => rankScaled(38, .22, r))],
      aoguang_special: f => [rankPreviewStat('当前飞棒去程基础伤害', 'Current-loadout outward hit', f, flyingStaffHitAtSpecialRank), rankPreviewStat('每次命中冻结', 'Freeze per hit', f, r => cleanPreviewNumber(.65 + .08 * r), ' 秒', 's')],
      bull_special: f => [rankPreviewStat('当前飞棒去程基础伤害', 'Current-loadout outward hit', f, flyingStaffHitAtSpecialRank), previewComparison('每次命中击退强度', 'Knockback per hit', '210', '210', '210')],
      ironfan_special: f => [rankPreviewStat('当前飞棒去程基础伤害', 'Current-loadout outward hit', f, flyingStaffHitAtSpecialRank), previewComparison('减速强度与时间', 'Slow strength and duration', '58% / 1.5s', '58% / 1.5s')],
      buddha_dharma_return: f => [rankPreviewStat('当前飞棒去程基础伤害', 'Current-loadout outward hit', f, flyingStaffHitAtSpecialRank), rankPreviewStat('法轮引爆倍率', 'Dharma-wheel detonation', f, r => cleanPreviewNumber(45 * (1 + .22 * (r - 1))), '% 飞棒伤害', '% of staff damage')],
      yanluo_special: f => [rankPreviewStat('当前飞棒去程基础伤害', 'Current-loadout outward hit', f, flyingStaffHitAtSpecialRank), previewComparison('非首领斩杀线', 'Non-boss execution threshold', '15', '15', '15', '% 气血', '% HP')],
      change_special: f => [rankPreviewStat('当前飞棒去程基础伤害', 'Current-loadout outward hit', f, flyingStaffHitAtSpecialRank), previewComparison('去程 / 回程冻结', 'Outbound / return freeze', '0.55s / 1.05s', '0.55s / 1.05s')],

      luban_divine_gear: f => [rankPreviewStat('每 0.28 秒齿轮伤害', 'Gear damage every 0.28s', f, r => rankScaled(32, .25, r)), previewComparison('反弹弹幕伤害倍率', 'Reflected-projectile damage', '125', '125', '125', '%', '%')],
      erlang_ring: f => [rankPreviewStat('阵内承伤增幅', 'Enemy damage taken inside array', f, r => percentScaled(40, 8, r), '%', '%'), rankPreviewStat('每 0.34 秒天眼伤害', 'Third-Eye damage every 0.34s', f, r => rankScaled(30, .30, r))],
      guanyin_ring: f => [rankPreviewStat('每秒回复气血', 'Health restored per second', f, r => cleanPreviewNumber(8 * (1 + .20 * (r - 1)))), previewComparison('敌人减速', 'Enemy slow', '50', '50', '50', '%', '%')],
      nezha_ring: f => [rankPreviewStat('每次乾坤圈伤害', 'Damage per Universe-Ring hit', f, r => rankScaled(35, .25, r)), rankPreviewStat('最大弹射目标', 'Maximum ricochet targets', f, r => Math.min(6, 3 + r))],
      laojun_ring: f => [rankPreviewStat('每 0.3 秒炉阵伤害', 'Furnace damage every 0.3s', f, r => rankScaled(40, .30, r)), rankPreviewStat('每次附加灼烧', 'Burn applied per pulse', f, r => 24 * r)],
      aoguang_ring: f => [rankPreviewStat('每 0.2 秒漩涡伤害', 'Maelstrom damage every 0.2s', f, r => rankScaled(12, .25, r)), previewComparison('每次吸附距离', 'Pull distance per pulse', '14', '14', '14', ' 像素', ' px')],

      erlang_dash: f => [rankPreviewStat('落点神雷范围伤害', 'Landing lightning area damage', f, r => 40 + 12 * (r - 1))],
      guanyin_dash: f => [rankPreviewStat('玉露护盾值', 'Willow-Dew shield', f, r => 30 + 12 * (r - 1)), rankPreviewStat('护盾持续时间', 'Shield duration', f, r => cleanPreviewNumber(2.5 + .25 * (r - 1)), ' 秒', 's')],
      nezha_dash: f => [rankPreviewStat('火轨每秒灼烧', 'Flame-trail damage per second', f, r => rankScaled(50, .25, r))],

      luban_clockwork_kite: f => [rankPreviewStat('木鸢飞弹爆炸伤害', 'Clockwork missile damage', f, r => rankScaled(90, .30, r)), rankPreviewStat('飞弹间隔', 'Missile interval', f, r => cleanPreviewNumber(Math.max(1.7, 3 - .18 * (r - 1))), ' 秒', 's')],
      luban_masterwork: f => [rankPreviewStat('常驻天工护甲', 'Permanent masterwork armor', f, r => 50 * r), previewComparison('额外升级触发率', 'Chance for one extra Peach rank', '50', '50', '50', '%', '%')],
      erlang_hound: f => [rankPreviewStat('哮天犬撕咬伤害', 'Xiaotianquan bite damage', f, r => rankScaled(80, .30, r)), rankPreviewStat('自动撕咬间隔', 'Automatic bite interval', f, r => cleanPreviewNumber(Math.max(.62, .92 - .06 * (r - 1))), ' 秒', 's')],
      erlang_truesight: f => [rankPreviewStat('普通攻击暴击率', 'Normal-attack critical chance', f, r => percentScaled(25, 5, r, 45), '%', '%'), rankPreviewStat('暴击伤害额外倍率', 'Additional critical-damage multiplier', f, r => percentScaled(50, 10, r, 90), '%', '%')],
      guanyin_nirvana: f => [rankPreviewStat('金身复活次数', 'Golden-body revivals', f, r => r), rankPreviewStat('复活气血', 'Health restored on revival', f, r => percentScaled(70, 5, r, 90), '% 最大气血', '% max HP')],
      laojun_elixir: f => [rankPreviewStat('未来每枚蟠桃额外提升重数', 'Bonus ranks from every future Peach', f, r => r), previewComparison('服桃后气血', 'Health after eating a Peach', '100', '100', '100', '%', '%')],
      bull_ironhide: f => [rankPreviewStat('可再生魔王护甲', 'Regenerating demon armor', f, r => 50 + 25 * (r - 1)), previewComparison('无伤后回满时间', 'Time without damage before refill', '8', '8', '8', ' 秒', 's')],
      buddha_equanimity: f => [rankPreviewStat('半真气以上减伤', 'Damage reduction above half Qi', f, r => percentScaled(15, 3, r, 24), '%', '%')]
    });

    function validateBoonUpgradePreviewers() {
      const boonIds = Object.values(GODS).flatMap(god => god.boons.map(boon => boon.id));
      const previewIds = Object.keys(BOON_UPGRADE_PREVIEWERS);
      const missing = boonIds.filter(id => !previewIds.includes(id));
      const orphaned = previewIds.filter(id => !boonIds.includes(id));
      if (missing.length || orphaned.length) throw new Error(`Boon upgrade preview mismatch. Missing: ${missing.join(', ')}; orphaned: ${orphaned.join(', ')}`);
    }
    validateBoonUpgradePreviewers();

    function getBoonUpgradePreview(boon) {
      const forecast = getPeachRankForecast(boon);
      const previewer = BOON_UPGRADE_PREVIEWERS[boon.id];
      const lines = [];
      if (getBoonSlotKey(boon.slot) === 'attack') {
        lines.push(previewComparison(
          '当前武器三连击基础伤害', 'Current-weapon triple-strike base damage',
          getAttackComboPreview(forecast.level).join('/'),
          getAttackComboPreview(forecast.minLevel).join('/'),
          getAttackComboPreview(forecast.maxLevel).join('/')
        ));
      }
      lines.push(...previewer(forecast));
      const rankRange = forecast.minLevel === forecast.maxLevel ? `${forecast.minLevel}` : `${forecast.minLevel}–${forecast.maxLevel}`;
      const note = forecast.masterworkChance > 0
        ? `<div class="boon-upgrade-note">${uiText('巧夺天工：下列右侧范围包含 50% 额外再升 1 重的结果。', 'Peerless Craftsmanship: right-side ranges include the 50% chance for one additional rank.')}</div>`
        : '';
      return `<div class="boon-upgrade-heading">${uiText(`确定提升：第 ${forecast.level} 重 → 第 ${rankRange} 重`, `Exact upgrade: Rank ${forecast.level} → Rank ${rankRange}`)}</div>${lines.join('')}${note}`;
    }


    const LIFE_LEECH_WINDOW_SECONDS = 0.50;
    const LIFE_LEECH_WINDOW_MAX_HP = 0.04;
    const LIFE_LEECH_PER_HIT_MAX_HP = 0.02;
    const GUANYIN_STRIKE_HEAL_BASE = 1;
    const GUANYIN_STRIKE_HEAL_PER_RANK = 0.5;

    // PLAYER CLASS
    class Player {
      constructor() {
        this.x = 0;
        this.y = 0;
        this.vx = 0;
        this.vy = 0;
        this.facing = 1;
        this.direction = 'down';
        this.radius = 26;
        this.baseSpeed = 250;
        this.speed = 250;
        this.hp = 100;
        this.metaMaxHp = 100;
        this.runMaxHpBonus = 0;
        this.maxHp = 100;
        this.qi = 100;
        this.maxQi = 100;
        this.qiRegen = 2.0;
        this.armor = 0;
        this.bullArmor = 0;
        this.bullArmorMax = 0;
        this.masterworkArmor = 0;
        this.masterworkArmorMax = 0;
        this.timeSinceDamage = 999;
        this.lifeLeechWindowTimer = 0;
        this.lifeLeechWindowHealing = 0;
        this.guanyinBarrier = 0;
        this.guanyinBarrierTimer = 0;
        this.invulnTimer = 0;
        this.weaponStyle = 'normal';
        this.hasRuyiStaff = false;

        this.comboStep = 0;
        this.comboWindowTimer = 0;
        this.comboInputSequence = '';
        this.comboInputTimer = 0;
        this.combatInputQueue = [];
        this.currentAttackToken = 'L';
        this.activeComboMove = null;
        this.isAttacking = false;
        this.attackDuration = 0;
        this.attackMaxDuration = 0.22;
        this.attackAngle = 0;
        this.attackCooldown = 0;
        this.attackLunge = 0;
        this.pendingAttack = null;
        this.animClock = 0;

        this.isCastingSpell = false;
        this.castSpellDuration = 0;
        this.castSpellMaxDuration = 0.55;

        this.isSpecialActive = false;
        this.specialCooldown = 0;
        this.specialDuration = 0;
        this.specialMaxDuration = 0.58;
        this.pendingSpecial = null;
        this.houndCooldown = 0;
        this.hound = null;

        this.isDashing = false;
        this.dashDuration = 0;
        this.dashMaxDuration = 0.26;
        this.dashCooldown = 0;
        this.dashCharges = 2;
        this.maxDashCharges = 2;
        this.dashRechargeTimer = 0;
        this.dashTrail = [];
        this.dashBoonFxTimer = 0;

        this.castActive = null;
        this.castCooldown = 0;

        this.awakenGauge = 0;
        this.maxAwakenGauge = 100;
        this.isAwakened = false;
        this.awakenDuration = 0;

        this.lives = 1;
        this.maxLives = 1;

        this.activeTransformationForm = 'dragon';
        this.isTransformed = false;
        this.transformDuration = 0;
        this.transformMaxDuration = 14.0;
        this.transformCooldown = 0;
        this.formBarrier = 0;
        this.formBarrierMax = 0;
        this.formGuardTriggered = false;
        this.formReviveUsed = false;
        this.formRevivesRemaining = 0;
        this.formFrenzy = 0;
        this.formFrenzyTimer = 0;
        this.formAuraTimer = 0;
        this.formSkillCooldowns = {};
        this.isManifested = false;
        this.manifestDuration = 0;
        this.manifestCooldown = 0;
        this.manifestAnimDuration = 0;

        this.boons = {
          weapon: null,
          attack: null,
          special: null,
          cast: null,
          dash: null,
          hex: null,
          passives: []
        };
        this.boonLevels = {};
      }

      resetForRun() {
        // Health earned from peaches, elixirs, gates, doctrines, and story
        // rewards lasts for the whole journey, but a genuinely new journey
        // starts a fresh run-health ledger. Checkpoint restore reinstates it.
        this.runMaxHpBonus = 0;
        this.applyMetaUpgrades();
        this.hp = this.maxHp;
        this.qi = this.maxQi;
        this.lives = this.maxLives;
        this.dashCharges = this.maxDashCharges;
        this.armor = this.baseArmor || 0;
        this.bullArmor = 0;
        this.bullArmorMax = 0;
        this.masterworkArmor = 0;
        this.masterworkArmorMax = 0;
        this.timeSinceDamage = 999;
        this.lifeLeechWindowTimer = 0;
        this.lifeLeechWindowHealing = 0;
        this.guanyinBarrier = 0;
        this.guanyinBarrierTimer = 0;
        this.awakenGauge = 0;
        this.isAwakened = false;
        this.isCastingSpell = false;
        this.castSpellDuration = 0;
        this.castSpellMaxDuration = 0.55;
        this.comboStep = 0;
        this.comboWindowTimer = 0;
        this.comboInputSequence = '';
        this.comboInputTimer = 0;
        this.combatInputQueue = [];
        this.currentAttackToken = 'L';
        this.activeComboMove = null;
        this.isAttacking = false;
        this.attackDuration = 0;
        this.attackCooldown = 0;
        this.pendingAttack = null;
        this.pendingSpecial = null;
        this.isSpecialActive = false;
        this.specialDuration = 0;
        this.houndCooldown = 0;
        this.hound = null;
        this.direction = 'down';
        this.weaponStyle = 'normal';
        this.hasRuyiStaff = false;
        this.invulnTimer = 2.5;
        this.isDashing = false;
        this.dashDuration = 0;
        this.dashMaxDuration = 0.26;
        this.dashCooldown = 0;
        this.dashBoonFxTimer = 0;
        this.isTransformed = false;
        this.transformDuration = 0;
        this.transformCooldown = 0;
        this.formBarrier = 0;
        this.formBarrierMax = 0;
        this.formGuardTriggered = false;
        this.formReviveUsed = false;
        this.formRevivesRemaining = 0;
        this.formFrenzy = 0;
        this.formFrenzyTimer = 0;
        this.formAuraTimer = 0;
        this.formSkillCooldowns = {};
        this.isManifested = false;
        this.manifestDuration = 0;
        this.manifestCooldown = 0;
        this.manifestAnimDuration = 0;
        this.boons = {
          weapon: null,
          attack: null,
          special: null,
          cast: null,
          dash: null,
          hex: null,
          passives: []
        };
        this.boonLevels = {};
        this.x = 0;
        this.y = 0;
        this.vx = 0;
        this.vy = 0;
        this.castActive = null;
        this.dashTrail = [];
        this.alignmentBarrier = 0;
        this.alignmentDashEmpowered = false;
        this.absorbedBossQi = 0;
        updateHUD();
      }

      getSkillRank(id) {
        return (typeof getSkillRank === 'function') ? getSkillRank(id) : (skillTreeRanks[id] || 0);
      }

      getActiveFormSkillRank(id) {
        if (!this.isTransformed || gameState.playableHero !== 'wukong') return 0;
        const node = SKILL_TREE_72.find(skill => skill.id === id);
        if (!node || node.branch !== this.activeTransformationForm) return 0;
        return this.getSkillRank(id);
      }

      hasActiveFormSkill(id) {
        return this.getActiveFormSkillRank(id) > 0;
      }

      cueFormSkill(id, x = this.x, y = this.y, scale = 1) {
        const rank = this.getActiveFormSkillRank(id);
        if (!rank) return;
        const node = SKILL_TREE_72.find(skill => skill.id === id);
        const profile = FORM_COMBAT_PROFILES[this.activeTransformationForm] || FORM_COMBAT_PROFILES.dragon;
        fxList.push(new FormSkillRuneFX(x, y, node?.icon || '✦', profile.color, scale));
      }

      increaseRunMaxHp(amount, healing = amount) {
        const gain = Math.max(0, Number(amount) || 0);
        if (!gain) return 0;
        this.runMaxHpBonus = Math.max(0, Number(this.runMaxHpBonus) || 0) + gain;
        this.maxHp += gain;
        this.hp = Math.min(this.maxHp, this.hp + Math.max(0, Number(healing) || 0));
        return gain;
      }

      applyMetaUpgrades() {
        // Transformation-tree ranks are techniques, not generic account stats.
        // Only the separate permanent-passive rows and alignment tree affect
        // untransformed Wukong. Every branch node is consumed by form combat.
        const masteryRanks = 0;
        const permanentDamageRank = typeof getPermanentPassiveRank === 'function' ? getPermanentPassiveRank('damage') : 0;
        const permanentVitalityRank = typeof getPermanentPassiveRank === 'function' ? getPermanentPassiveRank('vitality') : 0;
        const permanentQiRegenRank = typeof getPermanentPassiveRank === 'function' ? getPermanentPassiveRank('qi_regen') : 0;
        const permanentPrecisionRank = typeof getPermanentPassiveRank === 'function' ? getPermanentPassiveRank('precision') : 0;
        const alignmentEffects = gameState.playableHero === 'wukong' ? getActiveAlignmentEffects() : {};
        const erlangEffects = gameState.playableHero === 'erlang' && typeof getErlangSkillEffects === 'function' ? getErlangSkillEffects() : {};
        const neutralInvestedRanks = gameState.playableHero === 'wukong' ? ALIGNMENT_SKILLS.reduce((total, skill) => {
          if (skill.path !== 'neutral' || !isAlignmentSkillActive(skill)) return total;
          return total + Math.min(skill.maxRank, getAlignmentSkillRank(skill.id));
        }, 0) : 0;

        this.masteryRanks = masteryRanks;
        this.alignmentEffects = alignmentEffects;
        this.erlangSkillEffects = erlangEffects;
        this.neutralInvestedRanks = neutralInvestedRanks;
        this.metaMaxHp = Math.round(100 * (1 + permanentVitalityRank * 0.01 + (alignmentEffects.hpPct || 0)) + (erlangEffects.maxHp || 0));
        this.maxHp = this.metaMaxHp + Math.max(0, Number(this.runMaxHpBonus) || 0);
        this.maxQi = Math.round(100 * (1 + (alignmentEffects.qiPct || 0)) + (erlangEffects.maxQi || 0));
        this.qiRegen = (2.0 * (1 + permanentQiRegenRank * 0.01)) + (alignmentEffects.qiRegen || 0) + (erlangEffects.qiRegen || 0);
        this.baseSpeed = 250 * (1 + (alignmentEffects.speed || 0) + (erlangEffects.speed || 0));
        this.metaDamageMultiplier = (1 + permanentDamageRank * 0.01) * (1 + (alignmentEffects.damage || 0) + (erlangEffects.damage || 0));
        this.permanentCritBonus = permanentPrecisionRank * 0.002 + (alignmentEffects.crit || 0) + (erlangEffects.crit || 0);
        this.alignmentAttackSpeed = (alignmentEffects.attackSpeed || 0) + (erlangEffects.attackSpeed || 0);
        this.alignmentLifeLeech = Math.min(0.025, alignmentEffects.lifeLeech || 0);
        this.alignmentDamageReduction = Math.min(.48, alignmentEffects.damageReduction || 0);
        this.alignmentLowHpReduction = Math.min(.35, alignmentEffects.lowHpReduction || 0);
        this.alignmentBossDamage = (alignmentEffects.bossDamage || 0) + (erlangEffects.bossDamage || 0);
        this.alignmentExecuteDamage = alignmentEffects.executeDamage || 0;
        this.alignmentSpecialDamage = alignmentEffects.specialDamage || 0;
        this.alignmentDashBarrierMax = alignmentEffects.dashBarrier || 0;
        this.transformMaxDuration = 14;
        this.metaTransformCooldownMultiplier = 1;
        this.maxDashCharges = 2;
        this.maxLives = 1;
        this.baseArmor = (alignmentEffects.armor || 0) + (erlangEffects.armor || 0);
        this.dashCharges = Math.min(this.dashCharges ?? this.maxDashCharges, this.maxDashCharges);
        this.lives = Math.min(this.lives ?? this.maxLives, this.maxLives);
        this.armor = Math.min(this.armor ?? this.baseArmor, this.baseArmor);
      }

      applyLifeLeechHealing(requestedHealing) {
        if (!Number.isFinite(requestedHealing) || requestedHealing <= 0 || this.hp >= this.maxHp) return 0;
        if (this.lifeLeechWindowTimer <= 0) {
          this.lifeLeechWindowTimer = LIFE_LEECH_WINDOW_SECONDS;
          this.lifeLeechWindowHealing = 0;
        }
        const perHitCap = Math.max(1, this.maxHp * LIFE_LEECH_PER_HIT_MAX_HP);
        const windowCap = Math.max(2, this.maxHp * LIFE_LEECH_WINDOW_MAX_HP);
        const remainingBudget = Math.max(0, windowCap - this.lifeLeechWindowHealing);
        const actualHealing = Math.min(requestedHealing, perHitCap, remainingBudget, this.maxHp - this.hp);
        if (actualHealing <= 0) return 0;
        this.hp += actualHealing;
        this.lifeLeechWindowHealing += actualHealing;
        return actualHealing;
      }

      healFromDamage(damage, leechRate) {
        return this.applyLifeLeechHealing(Math.max(0, damage) * Math.max(0, leechRate));
      }

      triggerSignature() {
        if (gameState.playableHero === 'erlang') this.triggerErlangManifestation();
        else this.triggerTransformation();
      }

      triggerErlangManifestation() {
        if (this.isManifested) return;
        if (this.manifestCooldown > 0) {
          floatingTexts.push(new FloatingText(this.x, this.y - 42,
            uiText(`清源法相冷却中 (${this.manifestCooldown.toFixed(1)}s)`, `Manifestation cooldown: ${this.manifestCooldown.toFixed(1)}s`), '#60a5fa'));
          return;
        }
        const training = this.erlangSkillEffects || {};
        this.isManifested = true;
        this.manifestDuration = 12 + (training.manifestDuration || 0);
        this.manifestCooldown = 22 * Math.max(.55, 1 - (training.manifestCooldown || 0));
        this.manifestAnimDuration = 0;
        this.animClock = 0;
        this.invulnTimer = Math.max(this.invulnTimer, 0.8);
        sound.playAwaken();
        createScreenShake(7);
        fxList.push(new HadesMagicCircleAOEFX(this.x, this.y, 120 + (training.manifestDuration || 0) * 2, 1.0, '#60a5fa'));
        floatingTexts.push(new FloatingText(this.x, this.y - 58,
          uiText('👁 清源妙道真君 · 天眼法相！', '👁 Clear-Origin Manifestation · Heaven Eye Unsealed!'), '#fde68a', 20));
      }

      triggerTransformation() {
        if (this.isTransformed) return;
        if (this.transformCooldown > 0) {
          floatingTexts.push(new FloatingText(this.x, this.y - 40,
            uiText(`真身冷却中 (${this.transformCooldown.toFixed(1)}s)!`, `Form cooldown: ${this.transformCooldown.toFixed(1)}s`), '#f87171'));
          return;
        }

        this.isTransformed = true;
        this.animClock = 0;
        const doctrineDuration = gameState.transformationDoctrine === '72' ? 6 : (gameState.transformationDoctrine === '36' ? 3 : 0);
        const doctrineCooldown = gameState.transformationDoctrine === '72' ? 0.75 : (gameState.transformationDoctrine === '36' ? 0.88 : 1);
        const seaDuration = this.activeTransformationForm === 'dragon' ? this.getActiveFormSkillRank('dragon_sea') * 1.5 : 0;
        this.transformDuration = this.transformMaxDuration + doctrineDuration + seaDuration;
        this.transformCooldown = 22.0 * this.metaTransformCooldownMultiplier * doctrineCooldown;
        this.formBarrier = 0;
        this.formBarrierMax = 0;
        this.formGuardTriggered = false;
        this.formReviveUsed = false;
        this.formRevivesRemaining = this.activeTransformationForm === 'tortoise' ? this.getActiveFormSkillRank('tort_immortal') : 0;
        this.formFrenzy = 0;
        this.formFrenzyTimer = 0;
        this.formAuraTimer = 0;

        sound.playAwaken();
        createScreenShake(8);
        fxList.push(new ColossalStaffNovaFX(this.x, this.y, 210, '#facc15'));
        fxList.push(new HadesMagicCircleAOEFX(this.x, this.y, 125, 1.15, '#facc15'));
        this.activateTransformationSkills();

        const formNames = {
          dragon: ['🐲 苍龙显圣 · 水雷御海！', '🐲 Azure Dragon · Storm-Tide Dominion!'],
          tiger: ['🐯 白虎战煞 · 撕天裂地！', '🐯 White Tiger · Rend Heaven and Earth!'],
          roc: ['🦅 金翅大鹏 · 扶摇九万！', '🦅 Golden Roc · Soar Ninety Thousand Li!'],
          ape: ['🦍 法天象地 · 泰坦崩山！', '🦍 Titan Ape · Mountain-Shattering Colossus!'],
          tortoise: ['🐢 玄武真形 · 幽冥玄甲！', '🐢 Black Tortoise · Nether Armor!']
        };
        const formMessage = formNames[this.activeTransformationForm];
        floatingTexts.push(new FloatingText(this.x, this.y - 60,
          formMessage ? uiText(formMessage[0], formMessage[1]) : uiText('七十二变 · 神通显化！', '72 Transformations · Divine Form Manifest!'), '#facc15'));
      }

      activateTransformationSkills() {
        const formNodeId = `form_${this.activeTransformationForm}`;
        this.cueFormSkill(formNodeId, this.x, this.y, 1.35);
        if (this.activeTransformationForm === 'dragon') {
          const scaleRank = this.getActiveFormSkillRank('dragon_scale');
          this.formBarrierMax = scaleRank * 22;
          this.formBarrier = this.formBarrierMax;
          if (scaleRank) this.cueFormSkill('dragon_scale');
        } else if (this.activeTransformationForm === 'tiger') {
          this.invulnTimer = Math.max(this.invulnTimer, 0.35);
        } else if (this.activeTransformationForm === 'roc') {
          const scoutRank = this.getActiveFormSkillRank('roc_sky_scout');
          if (scoutRank) {
            enemies.filter(enemy => enemy.alive && !enemy.isAlly && (enemy.isBoss || enemy.maxHp >= 900)).forEach(enemy => {
              enemy.formWeakPointTimer = this.transformDuration;
              fxList.push(new FormSkillRuneFX(enemy.x, enemy.y - enemy.radius, '◉', '#fbbf24', 0.72));
            });
            this.cueFormSkill('roc_sky_scout');
          }
        } else if (this.activeTransformationForm === 'ape') {
          const mountainRank = this.getActiveFormSkillRank('ape_mountain');
          this.formBarrierMax = mountainRank * 36;
          this.formBarrier = this.formBarrierMax;
          if (mountainRank) this.cueFormSkill('ape_mountain');
        } else if (this.activeTransformationForm === 'tortoise') {
          const shellRank = this.getActiveFormSkillRank('tort_shell');
          this.formBarrierMax = shellRank * 42;
          this.formBarrier = this.formBarrierMax;
          if (shellRank) this.cueFormSkill('tort_shell');
        }
      }

      hasBoon(id) {
        if (this.boons.weapon && this.boons.weapon.id === id) return true;
        if (this.boons.attack && this.boons.attack.id === id) return true;
        if (this.boons.special && this.boons.special.id === id) return true;
        if (this.boons.cast && this.boons.cast.id === id) return true;
        if (this.boons.dash && this.boons.dash.id === id) return true;
        if (this.boons.hex && this.boons.hex.id === id) return true;
        return this.boons.passives.some(b => b.id === id);
      }

      getBoonLevel(id) {
        if (this.boons.weapon && this.boons.weapon.id === id) return this.boons.weapon.level || 1;
        if (this.boons.attack && this.boons.attack.id === id) return this.boons.attack.level || 1;
        if (this.boons.special && this.boons.special.id === id) return this.boons.special.level || 1;
        if (this.boons.cast && this.boons.cast.id === id) return this.boons.cast.level || 1;
        if (this.boons.dash && this.boons.dash.id === id) return this.boons.dash.level || 1;
        if (this.boons.hex && this.boons.hex.id === id) return this.boons.hex.level || 1;
        const p = this.boons.passives.find(b => b.id === id);
        return p ? (p.level || 1) : 1;
      }

      getActiveGodColor() {
        if (gameState.playableHero === 'wukong' && getAlignmentPath() !== 'neutral') {
          return getAlignmentPalette().primary;
        }
        if (this.boons.attack && GODS[this.boons.attack.godKey]) {
          return GODS[this.boons.attack.godKey].color;
        }
        if (this.boons.special && GODS[this.boons.special.godKey]) {
          return GODS[this.boons.special.godKey].color;
        }
        if (this.boons.weapon && GODS[this.boons.weapon.godKey]) {
          return GODS[this.boons.weapon.godKey].color;
        }
        return gameState.playableHero === 'wukong' ? getAlignmentPalette().primary : '#facc15';
      }

      getActiveGodKeys() {
        const keys = new Set();
        ['weapon', 'attack', 'special', 'cast', 'dash', 'hex'].forEach(slot => {
          const godKey = this.boons[slot]?.godKey;
          if (godKey) keys.add(godKey);
        });
        this.boons.passives.forEach(boon => { if (boon.godKey) keys.add(boon.godKey); });
        return keys;
      }

      hasDeitySynergy(synergyKey) {
        const synergy = DEITY_SYNERGIES[synergyKey];
        if (!synergy) return false;
        const activeGods = this.getActiveGodKeys();
        return synergy.gods.every(godKey => activeGods.has(godKey));
      }

      updateTransformationSkills(dt) {
        const passiveRecoveryAllowed = !gameState.chamberCleared;
        Object.keys(this.formSkillCooldowns).forEach(id => {
          this.formSkillCooldowns[id] = Math.max(0, this.formSkillCooldowns[id] - dt);
        });
        if (!this.isTransformed) return;
        this.formAuraTimer -= dt;

        if (this.activeTransformationForm === 'dragon') {
          const rainRank = this.getActiveFormSkillRank('dragon_rain');
          if (rainRank && passiveRecoveryAllowed) this.qi = Math.min(this.maxQi, this.qi + rainRank * 0.5 * dt);
        } else if (this.activeTransformationForm === 'tiger') {
          const speedRank = this.getActiveFormSkillRank('tiger_speed');
          if (speedRank && this.comboWindowTimer > 0) {
            this.formFrenzy = Math.min(0.08 * speedRank, this.formFrenzy + dt * 0.04);
            this.formFrenzyTimer = 1.0;
          } else if (this.formFrenzyTimer > 0) {
            this.formFrenzyTimer -= dt;
          } else {
            this.formFrenzy = Math.max(0, this.formFrenzy - dt * 0.10);
          }
        } else if (this.activeTransformationForm === 'tortoise') {
          const regenRank = this.getActiveFormSkillRank('tort_regen');
          if (regenRank && passiveRecoveryAllowed) this.hp = Math.min(this.maxHp, this.hp + (1.2 + regenRank * 0.75) * dt);

          const whirlRank = this.getActiveFormSkillRank('tort_whirlpool');
          if (whirlRank && this.formAuraTimer <= 0) {
            this.formAuraTimer = Math.max(0.22, 0.55 - whirlRank * 0.04);
            const orbitTargets = enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - this.x, enemy.y - this.y) <= 132 + enemy.radius).slice(0, 5);
            orbitTargets.forEach(enemy => {
              enemy.takeDamage((18 + whirlRank * 10) * (this.metaDamageMultiplier || 1), false, false);
              fxList.push(new ElementalSlashFX(enemy.x, enemy.y, Math.atan2(enemy.y - this.y, enemy.x - this.x), 'water', 72));
            });
            if (orbitTargets.length) this.cueFormSkill('tort_whirlpool', this.x, this.y, 0.72);
          }

          const reflectRank = this.getActiveFormSkillRank('tort_reflect');
          if (reflectRank) {
            projectiles.filter(projectile => projectile.alive && projectile.isEnemy && Math.hypot(projectile.x - this.x, projectile.y - this.y) <= 92 + projectile.radius)
              .forEach(projectile => {
                projectile.alive = false;
                projectiles.push(new Projectile(projectile.x, projectile.y, -projectile.vx, -projectile.vy, projectile.dmg * (1 + 0.35 * reflectRank), '#34d399', false));
                this.cueFormSkill('tort_reflect', projectile.x, projectile.y, 0.58);
              });
          }
        }
      }

      update(dt) {
        this.animClock += dt;
        const passiveRecoveryAllowed = !gameState.chamberCleared;
        if (this.lifeLeechWindowTimer > 0) {
          this.lifeLeechWindowTimer = Math.max(0, this.lifeLeechWindowTimer - dt);
          if (this.lifeLeechWindowTimer <= 0) this.lifeLeechWindowHealing = 0;
        }
        if (passiveRecoveryAllowed && this.qi < this.maxQi) {
          this.qi = Math.min(this.maxQi, this.qi + this.qiRegen * dt);
        }
        const activeForm = this.isTransformed ? FORM_COMBAT_PROFILES[this.activeTransformationForm] : null;
        if (passiveRecoveryAllowed && this.isTransformed && this.activeTransformationForm === 'dragon') {
          this.qi = Math.min(this.maxQi, this.qi + 1.5 * dt);
        }
        if (passiveRecoveryAllowed && this.isTransformed && this.activeTransformationForm === 'tortoise') {
          this.hp = Math.min(this.maxHp, this.hp + 2.5 * dt);
        }
        this.updateTransformationSkills(dt);

        if (this.invulnTimer > 0) this.invulnTimer -= dt;
        this.timeSinceDamage += dt;
        if (this.guanyinBarrierTimer > 0) {
          this.guanyinBarrierTimer = Math.max(0, this.guanyinBarrierTimer - dt);
          if (this.guanyinBarrierTimer <= 0) this.guanyinBarrier = 0;
        }
        if (this.hasBoon('bull_ironhide')) {
          const level = this.getBoonLevel('bull_ironhide');
          this.bullArmorMax = 50 + Math.max(0, level - 1) * 25;
          if (this.timeSinceDamage >= 8 && this.bullArmor < this.bullArmorMax) {
            this.bullArmor = this.bullArmorMax;
            fxList.push(new Shockwave(this.x, this.y, 74, '#ea580c'));
            floatingTexts.push(new FloatingText(this.x, this.y - 48,
              uiText(`魔王铁甲复原 · ${this.bullArmorMax}`, `Demon Iron Armor Restored · ${this.bullArmorMax}`), '#fb923c'));
          }
        } else {
          this.bullArmor = 0;
          this.bullArmorMax = 0;
        }

        if (this.transformCooldown > 0) {
          this.transformCooldown = Math.max(0, this.transformCooldown - dt);
        }
        if (this.isTransformed) {
          this.transformDuration -= dt;
          if (this.transformDuration <= 0) {
            this.isTransformed = false;
            this.transformDuration = 0;
            this.formBarrier = 0;
            this.formBarrierMax = 0;
            this.formFrenzy = 0;
            enemies.forEach(enemy => { enemy.formWeakPointTimer = 0; });
            this.dashCharges = Math.min(this.dashCharges, this.maxDashCharges);
            fxList.push(new Shockwave(this.x, this.y, 130, '#facc15'));
          }
        }

        const rocFlyRank = this.getActiveFormSkillRank('roc_fly');
        if (this.dashCharges < this.maxDashCharges + rocFlyRank) {
          this.dashRechargeTimer += dt;
          const rechargeDelay = rocFlyRank ? Math.max(0.28, 0.75 * (1 - rocFlyRank * 0.10)) : 0.75;
          if (this.dashRechargeTimer >= rechargeDelay) {
            this.dashCharges++;
            this.dashRechargeTimer = 0;
          }
        }

        if (this.isAwakened) {
          this.awakenDuration -= dt;
          if (this.awakenDuration <= 0) {
            this.isAwakened = false;
            this.awakenGauge = 0;
          }
        }

        if (this.isCastingSpell) {
          this.castSpellDuration -= dt;
          if (this.castSpellDuration <= 0) {
            this.isCastingSpell = false;
          }
        }

        if (this.attackCooldown > 0) this.attackCooldown -= dt;
        if (this.specialCooldown > 0) this.specialCooldown -= dt;
        if (this.houndCooldown > 0) this.houndCooldown = Math.max(0, this.houndCooldown - dt);
        if (this.castCooldown > 0) this.castCooldown -= dt;
        if (this.dashCooldown > 0) this.dashCooldown -= dt;
        if (this.manifestCooldown > 0) this.manifestCooldown = Math.max(0, this.manifestCooldown - dt);
        if (this.isManifested) {
          this.manifestDuration -= dt;
          this.manifestAnimDuration += dt;
          if (this.manifestDuration <= 0) {
            this.isManifested = false;
            this.manifestDuration = 0;
            fxList.push(new Shockwave(this.x, this.y, 100, '#60a5fa'));
          }
        }

        if (this.comboWindowTimer > 0) {
          this.comboWindowTimer -= dt;
          if (this.comboWindowTimer <= 0) {
            this.comboStep = 0;
          }
        }
        if (this.comboInputTimer > 0) {
          this.comboInputTimer -= dt;
          if (this.comboInputTimer <= 0) this.clearCombatComboSequence();
        }

        const worldMouseX = gameState.mouse.x - viewWidth / 2 + this.x;
        const worldMouseY = gameState.mouse.y - viewHeight / 2 + this.y;

        let moveX = 0;
        let moveY = 0;
        if (gameState.keys['w'] || gameState.keys['arrowup']) moveY -= 1;
        if (gameState.keys['s'] || gameState.keys['arrowdown']) moveY += 1;
        if (gameState.keys['a'] || gameState.keys['arrowleft']) moveX -= 1;
        if (gameState.keys['d'] || gameState.keys['arrowright']) moveX += 1;
        moveX += gameState.mobileMove.x;
        moveY += gameState.mobileMove.y;

        const len = Math.hypot(moveX, moveY);
        if (len > 0) {
          moveX /= len;
          moveY /= len;

          if (Math.abs(moveY) > Math.abs(moveX)) {
            if (moveY < 0) {
              this.direction = 'up';
              this.facing = 1;
            } else {
              this.direction = 'down';
              this.facing = 1;
            }
          } else {
            if (moveX < 0) {
              this.direction = 'left';
              this.facing = -1;
            } else {
              this.direction = 'right';
              this.facing = 1;
            }
          }
        } else if (this.isAttacking || this.isCastingSpell) {
          const dy = worldMouseY - this.y;
          const dx = worldMouseX - this.x;
          if (Math.abs(dy) > Math.abs(dx)) {
            this.direction = dy < 0 ? 'up' : 'down';
            this.facing = 1;
          } else {
            this.direction = dx < 0 ? 'left' : 'right';
            this.facing = dx < 0 ? -1 : 1;
          }
        }

        if (this.isDashing) {
          this.dashDuration -= dt;
          const dashProgress = Math.max(0, Math.min(1, 1 - this.dashDuration / this.dashMaxDuration));
          const easedDash = 1 - Math.pow(1 - dashProgress, 3);
          this.x = this.dashStartX + (this.dashTargetX - this.dashStartX) * easedDash;
          this.y = this.dashStartY + (this.dashTargetY - this.dashStartY) * easedDash;
          if (this.dashDuration <= 0) {
            this.isDashing = false;
            this.x = this.dashTargetX;
            this.y = this.dashTargetY;
          }
          this.dashTrail.push({
            x: this.x,
            y: this.y,
            alpha: 1.0,
            radius: 24
          });
          if (this.hasBoon('nezha_dash')) {
            this.dashBoonFxTimer -= dt;
            if (this.dashBoonFxTimer <= 0) {
              this.dashBoonFxTimer = 0.075;
              const rankScale = 1 + 0.25 * (this.getBoonLevel('nezha_dash') - 1);
              fxList.push(new AnimatedFireExplosion(this.x, this.y, 46));
              enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - this.x, enemy.y - this.y) <= 58 + enemy.radius)
                .slice(0, 5).forEach(enemy => enemy.applyBurn(50 * rankScale * (this.metaDamageMultiplier || 1), 1.0));
            }
          }
        } else {
          let curSpeed = this.baseSpeed;
          if (this.isAwakened) curSpeed *= 1.4;
          if (gameState.playableHero === 'erlang' && this.isManifested) curSpeed *= 1.12;
          if (activeForm) curSpeed *= activeForm.speed;
          curSpeed *= 1 + this.getActiveFormSkillRank('dragon_wind') * 0.06;
          curSpeed *= 1 + (this.activeTransformationForm === 'tiger' && this.isTransformed ? this.formFrenzy : 0);
          if (this.hasBoon('nezha_speed')) curSpeed *= (1 + 0.35 * this.getBoonLevel('nezha_speed'));
          if (this.hasBoon('ironfan_tailwind')) curSpeed *= 1.25;

          if (this.isAttacking && this.attackLunge > 0) {
            this.x += Math.cos(this.attackAngle) * this.attackLunge * dt;
            this.y += Math.sin(this.attackAngle) * this.attackLunge * dt;
          }

          this.vx = moveX * curSpeed;
          this.vy = moveY * curSpeed;
          this.x += this.vx * dt;
          this.y += this.vy * dt;
        }

        const arenaHalfW = 1160;
        const arenaHalfH = 860;
        if (this.x < -arenaHalfW) { this.x = -arenaHalfW; this.vx = 0; }
        if (this.x > arenaHalfW) { this.x = arenaHalfW; this.vx = 0; }
        if (this.y < -arenaHalfH) { this.y = -arenaHalfH; this.vy = 0; }
        if (this.y > arenaHalfH) { this.y = arenaHalfH; this.vy = 0; }

        for (let i = this.dashTrail.length - 1; i >= 0; i--) {
          this.dashTrail[i].alpha -= dt * 3.5;
          if (this.dashTrail[i].alpha <= 0) {
            this.dashTrail.splice(i, 1);
          }
        }

        if (this.castActive) {
          this.castActive.duration -= dt;
          this.castActive.tickTimer += dt;
          this.castActive.angle += dt * 1.35;
          if (this.castActive.tickTimer >= (this.castActive.pulseInterval || 0.25)) {
            this.castActive.tickTimer = 0;
            this.triggerCastTick();
          }
          if (this.castActive.duration <= 0) {
            this.castActive = null;
          }
        }

        this.tryConsumeCombatInput();
        if (gameState.mouse.isDown && !this.isAttacking && !this.isCastingSpell && this.attackCooldown <= 0 && this.combatInputQueue.length === 0) {
          this.handleCombatInput('L');
        }

        if (this.isAttacking) {
          this.attackDuration -= dt;
          const attackProgress = 1 - (this.attackDuration / this.attackMaxDuration);
          if (this.pendingAttack?.ruyiContactProfile?.mode === 'ring') {
            const authoredSweepProgress = getRuyiAuthoredProgress(
              attackProgress,
              this.pendingAttack.ruyiContactProfile,
              this.pendingAttack.contactAt,
            );
            const sweepStart = .12;
            const sweepEnd = .90;
            if (attackProgress >= sweepStart && attackProgress <= sweepEnd) {
              this.resolvePendingAttack(authoredSweepProgress);
            } else if (attackProgress > sweepEnd) {
              this.resolvePendingAttack(.999);
              this.pendingAttack = null;
            }
          } else if (this.pendingAttack && attackProgress >= this.pendingAttack.contactAt) {
            this.resolvePendingAttack();
          }
          if (this.attackDuration <= 0) {
            if (this.pendingAttack) {
              if (this.pendingAttack.ruyiContactProfile?.mode === 'ring') this.resolvePendingAttack(.999);
              else this.resolvePendingAttack();
            }
            this.pendingAttack = null;
            this.isAttacking = false;
            this.activeComboMove = null;
            this.activeRuyiContactProfile = null;
            this.activeAttackContactAt = 0;
            this.tryConsumeCombatInput();
          }
        }

        if (this.isSpecialActive) {
          this.specialDuration -= dt;
          const specialProgress = 1 - (this.specialDuration / this.specialMaxDuration);
          if (this.pendingSpecial && specialProgress >= this.pendingSpecial.contactAt) this.resolvePendingSpecial();
          if (this.specialDuration <= 0) {
            if (this.pendingSpecial) this.resolvePendingSpecial();
            this.isSpecialActive = false;
          }
        }
      }

      clearCombatComboSequence() {
        this.comboInputSequence = '';
        this.comboInputTimer = 0;
        updateComboReadout('');
      }

      registerCombatInputToken(token) {
        const comboDefinitions = getActiveComboDefinitions();
        const comboWindow = getActiveComboWindow();
        const candidate = `${this.comboInputSequence}${token}`;
        const exact = comboDefinitions.find(combo => combo.pattern === candidate) || null;
        if (exact) {
          // Execute the short finisher now, but retain it when it is also the
          // prefix of a longer art (LLL -> LLLRR, LLR -> LLRR/LLRLR).
          const canExtend = comboDefinitions.some(combo => combo.pattern !== candidate && combo.pattern.startsWith(candidate));
          this.comboInputSequence = canExtend ? candidate : '';
          this.comboInputTimer = canExtend ? comboWindow : 0;
          updateComboReadout('', exact);
          return exact;
        }

        // An invalid continuation begins a fresh chain at the newest input.
        // This makes held/tapped L repeat as clean groups of L-L-L instead of
        // getting stuck on the completed LLL prefix.
        const retained = comboDefinitions.some(combo => combo.pattern.startsWith(candidate))
          ? candidate
          : (comboDefinitions.some(combo => combo.pattern.startsWith(token)) ? token : '');
        this.comboInputSequence = retained;
        this.comboInputTimer = retained ? comboWindow : 0;
        updateComboReadout(retained);
        return null;
      }

      handleCombatInput(token) {
        if (token === 'R' && !this.comboInputSequence) {
          this.performRightClickSkill();
          return;
        }
        const comboMove = this.registerCombatInputToken(token);
        if (this.combatInputQueue.length < 8) this.combatInputQueue.push({ token, comboMove });
        this.tryConsumeCombatInput();
      }

      tryConsumeCombatInput() {
        if (!this.combatInputQueue.length || this.isDashing || this.isAttacking || this.isCastingSpell || this.isSpecialActive || this.attackCooldown > 0) return;
        const next = this.combatInputQueue.shift();
        this.performAttack(next.token, next.comboMove);
      }

      performAttack(attackToken = 'L', comboMove = null) {
        if (this.isDashing || this.isAttacking || this.isCastingSpell || this.isSpecialActive || this.attackCooldown > 0) return false;

        const currentCombo = comboMove ? 2 : (attackToken === 'R' ? 1 : this.comboStep % 2);
        const isErlang = gameState.playableHero === 'erlang';
        this.currentCombo = currentCombo;
        this.currentAttackToken = attackToken;
        this.activeComboMove = comboMove;
        if (attackToken === 'L') this.comboStep = (this.comboStep + 1) % 2;
        const erlangTraining = isErlang ? (this.erlangSkillEffects || {}) : {};
        this.comboWindowTimer = 0.85 + (erlangTraining.comboWindow || 0);

        const isTitan = this.weaponStyle === 'titan';
        const isExtend = this.weaponStyle === 'extend';

        this.isAttacking = true;
        this.animClock = 0;
        this.attackMaxDuration = isErlang
          ? (comboMove ? 0.72 : (currentCombo === 1 ? 0.40 : 0.34))
          : (isTitan ? (currentCombo === 2 ? 0.76 : 0.56) : (currentCombo === 2 ? 0.58 : (currentCombo === 1 ? 0.42 : 0.36)));
        if (isErlang && this.isManifested) this.attackMaxDuration *= 0.82;
        this.attackDuration = this.attackMaxDuration;
        this.attackCooldown = isTitan ? 0.38 : (currentCombo === 2 ? 0.30 : 0.16);

        const worldMouseX = gameState.mouse.x - viewWidth / 2 + this.x;
        const worldMouseY = gameState.mouse.y - viewHeight / 2 + this.y;
        this.attackAngle = Math.atan2(worldMouseY - this.y, worldMouseX - this.x);

        const dy = worldMouseY - this.y;
        const dx = worldMouseX - this.x;
        if (Math.abs(dy) > Math.abs(dx)) {
          this.direction = dy < 0 ? 'up' : 'down';
          this.facing = 1;
        } else {
          this.direction = dx < 0 ? 'left' : 'right';
          this.facing = dx < 0 ? -1 : 1;
        }

        sound.playStaffSwing(currentCombo, isTitan);

        let baseDmg = isErlang ? 50 : (isTitan ? 140 : 55);
        // Wukong melee reach is now the authored staff-tip distance, not a
        // generous invisible sector. Upgrades enlarge the rendered weapon path
        // and this same value drives contact geometry below.
        let reach = isErlang ? 230 : (isTitan ? 160 : RUYI_CONTACT_PROFILES.arc.baseReach);
        let arc = isErlang ? Math.PI * 0.62 : Math.PI * 0.95;
        this.attackLunge = isTitan ? 48 : 60;

        if (currentCombo === 1) {
          baseDmg = isErlang ? 72 : (isTitan ? 190 : 75);
          reach = isErlang ? 265 : (isTitan ? 170 : RUYI_CONTACT_PROFILES.spin.baseReach);
          arc = isErlang ? Math.PI * 1.18 : Math.PI * 2.0;
          this.attackLunge = isTitan ? 55 : 76;
        } else if (currentCombo === 2) {
          baseDmg = isErlang ? 128 : (isTitan ? 380 : 135);
          reach = isErlang ? 355 : (isExtend ? 220 : (isTitan ? 180 : RUYI_CONTACT_PROFILES.slam.baseReach));
          arc = isErlang ? Math.PI * 0.30 : (isExtend ? Math.PI * 0.55 : Math.PI * 1.25);
          this.attackLunge = isTitan ? 52 : 78;
        }

        const formProfile = this.isTransformed ? FORM_COMBAT_PROFILES[this.activeTransformationForm] : null;
        if (formProfile) {
          baseDmg *= formProfile.damage;
          reach *= formProfile.reach;
          arc = Math.min(Math.PI * 2, arc * (this.activeTransformationForm === 'ape' ? 1.45 : 1.05));
          this.attackLunge *= formProfile.lunge;
          this.attackMaxDuration *= formProfile.attackTime;
          this.attackDuration = this.attackMaxDuration;
          this.attackCooldown *= formProfile.cooldown;

          if (this.activeTransformationForm === 'dragon') {
            reach *= 1 + this.getActiveFormSkillRank('dragon_wind') * 0.10;
          } else if (this.activeTransformationForm === 'tiger') {
            const pounceRank = this.getActiveFormSkillRank('tiger_pounce');
            baseDmg += this.getActiveFormSkillRank('tiger_claws') * 10;
            this.attackLunge *= 1 + pounceRank * 0.15;
            this.attackMaxDuration /= 1 + pounceRank * 0.08 + this.formFrenzy;
            this.attackCooldown /= 1 + pounceRank * 0.08 + this.formFrenzy;
            baseDmg *= 1 + this.getActiveFormSkillRank('tiger_spirit') * 0.10;
          } else if (this.activeTransformationForm === 'roc') {
            if (currentCombo === 2) baseDmg *= 1 + this.getActiveFormSkillRank('roc_sky') * 0.40;
          } else if (this.activeTransformationForm === 'ape') {
            baseDmg += this.getActiveFormSkillRank('ape_might') * 15;
            reach *= 1 + this.getActiveFormSkillRank('ape_quake') * 0.18;
            baseDmg *= 1 + this.getActiveFormSkillRank('ape_overlord') * 0.20;
          }
          this.attackDuration = this.attackMaxDuration;
        }

        const alignmentHaste = 1 / (1 + Math.max(0, this.alignmentAttackSpeed || 0));
        this.attackMaxDuration *= alignmentHaste;
        this.attackCooldown *= alignmentHaste;
        this.attackDuration = this.attackMaxDuration;

        if (this.isAwakened) {
          baseDmg *= 2.2;
          reach *= 1.6;
        }
        if (isErlang && this.isManifested) baseDmg *= 1.25;
        if (isErlang) {
          baseDmg *= 1 + (erlangTraining.spearDamage || 0);
          reach *= 1 + (erlangTraining.spearReach || 0);
          if (comboMove) baseDmg *= 1 + (erlangTraining.comboDamage || 0);
          if (comboMove?.effect === 'launch') baseDmg *= 1 + (erlangTraining.launchDamage || 0);
          if (comboMove?.effect === 'spin') {
            baseDmg *= 1 + (erlangTraining.spinDamage || 0);
            reach += erlangTraining.spinRadius || 0;
          }
          if (this.isManifested) baseDmg *= 1 + (erlangTraining.manifestDamage || 0);
        }
        baseDmg *= this.metaDamageMultiplier || 1;
        baseDmg *= 1 + (this.absorbedBossQi || 0) * .015;
        baseDmg *= gameState.transformationDoctrine === '18' ? 1.35 : (gameState.transformationDoctrine === '36' ? 1.15 : 1);
        if (!isErlang && !this.hasRuyiStaff) {
          baseDmg *= 0.68;
          reach *= 0.76;
        }

        if (this.boons.attack) {
          const lvl = this.boons.attack.level || 1;
          baseDmg *= (1 + 0.3 * (lvl - 1));
        }

        if (comboMove) {
          baseDmg *= comboMove.damage;
          reach *= comboMove.reach;
          const karmaStage = isErlang ? null : getAlignmentCombatStage();
          if (karmaStage?.path === 'evil') baseDmg *= 1 + karmaStage.tier * .04;
          if (karmaStage?.path === 'good') reach *= 1 + karmaStage.tier * .03;
          this.attackMaxDuration *= comboMove.duration;
          this.attackDuration = this.attackMaxDuration;
          this.attackLunge *= comboMove.effect === 'spin' ? 0.55 : 0.82;
          const presentation = getActiveComboPresentation(comboMove);
          floatingTexts.push(new FloatingText(this.x, this.y - 62, presentation.name, isErlang ? '#93c5fd' : getAlignmentPalette().primary));
        }

        const fxColor = this.getActiveGodColor();
        const slashType = this.getSlashType();

        const ruyiContactProfile = !isErlang && !formProfile ? getRuyiContactProfile(currentCombo, comboMove) : null;
        const ruyiContactAt = ruyiContactProfile
          ? (comboMove?.contactAt ?? (ruyiContactProfile.contactFrame / RUYI_CONTACT_FRAME_COUNT))
          : (comboMove?.contactAt ?? [0.50, 0.55, 0.68][currentCombo]);
        this.activeRuyiContactProfile = ruyiContactProfile;
        this.activeAttackReach = reach;
        this.activeAttackContactAt = ruyiContactAt;
        this.pendingAttack = {
          baseDmg,
          reach,
          arc,
          currentCombo,
          isTitan,
          isExtend,
          fxColor,
          slashType,
          isErlang,
          formProfile,
          comboMove,
          ruyiContactProfile,
          attackAngle: this.attackAngle,
          contactAt: ruyiContactAt,
        };
        return true;
      }

      resolvePendingAttack(sweepProgress = null) {
        const pending = this.pendingAttack;
        if (!pending) return;
        const { baseDmg, reach, arc, currentCombo, isTitan, isExtend, fxColor, slashType, formProfile, attackAngle, isErlang, comboMove, ruyiContactProfile } = pending;
        const isProgressiveSweep = ruyiContactProfile?.mode === 'ring' && sweepProgress !== null;
        if (!isProgressiveSweep) this.pendingAttack = null;
        if (isProgressiveSweep && !pending.hitTargets) pending.hitTargets = new Set();
        let hitAny = false;
        let impactFxBudget = 3;
        let formProcUsed = false;
        let boonVisualUsed = false;
        let alignmentProcUsed = false;

        // Body, damage and the readable attack trail now meet on the authored
        // contact frame instead of firing as soon as the mouse is pressed.
        const karmaStage = getAlignmentCombatStage();
        const usesAuthoredEvilStrike = !isErlang && karmaStage?.path === 'evil';
        const usesAuthoredRuyiContact = Boolean(ruyiContactProfile);
        if (isErlang) {
          fxList.push(new HadesDivineStaffSlashFX(this.x, this.y, attackAngle, reach, 'thunder', currentCombo === 1, 0.78, 0.70));
          if (currentCombo === 2) fxList.push(new ExtendedStaffBeam(this.x, this.y, attackAngle, reach, '#93c5fd'));
        } else if (!usesAuthoredRuyiContact && !usesAuthoredEvilStrike && currentCombo === 0) {
          this.spawnLayeredStaffSlash(attackAngle, reach, slashType);
          fxList.push(new StaffMotionWaveFX(this.x, this.y, attackAngle, reach, fxColor));
        } else if (!usesAuthoredRuyiContact && !usesAuthoredEvilStrike && currentCombo === 1) {
          this.spawnLayeredStaffSlash(attackAngle, reach, slashType, true);
          this.spawnLayeredStaffSlash(attackAngle + Math.PI, reach, slashType, true);
        } else if (!usesAuthoredRuyiContact && !usesAuthoredEvilStrike) {
          const impactX = this.x + Math.cos(attackAngle) * (reach * 0.42);
          const impactY = this.y + Math.sin(attackAngle) * (reach * 0.42);
          fxList.push(new ColossalStaffNovaFX(impactX, impactY, reach * 0.72, fxColor));
          fxList.push(new GroundFissureFX(impactX, impactY, attackAngle, reach * 0.58, fxColor));
          fxList.push(new KnockdownDustFX(impactX, impactY));
          if (isExtend) fxList.push(new ExtendedStaffBeam(this.x, this.y, attackAngle, reach, fxColor));
        }
        if (comboMove && !usesAuthoredRuyiContact && !usesAuthoredEvilStrike) {
          const comboColor = isErlang ? '#60a5fa' : (karmaStage?.path === 'evil' ? '#a855f7' : (karmaStage?.path === 'good' ? '#93c5fd' : '#facc15'));
          const impactX = this.x + Math.cos(attackAngle) * Math.min(112, reach * .34);
          const impactY = this.y + Math.sin(attackAngle) * Math.min(112, reach * .34);
          if (comboMove.effect === 'spin') {
            fxList.push(new Shockwave(this.x, this.y, Math.min(142, reach * .48), comboColor));
          } else if (comboMove.effect === 'fissure' || comboMove.effect === 'verdict') {
            fxList.push(new GroundFissureFX(impactX, impactY, attackAngle, Math.min(165, reach * .46), comboColor));
          } else if (comboMove.effect === 'nova') {
            fxList.push(new ColossalStaffNovaFX(impactX, impactY, Math.min(150, reach * .48), comboColor));
          } else if (comboMove.effect === 'third_eye') {
            fxList.push(new AnimatedLightningStrike(impactX, impactY));
            fxList.push(new HadesMagicCircleAOEFX(impactX, impactY, Math.min(118, reach * .36), .48, '#93c5fd'));
          } else {
            fxList.push(new StaffMotionWaveFX(this.x, this.y, attackAngle, Math.min(190, reach * .66), comboColor));
          }
          if (karmaStage?.path === 'good') {
            const barrierGain = 8 + karmaStage.tier * 4;
            this.alignmentBarrier = Math.min(80, (this.alignmentBarrier || 0) + barrierGain);
          }
        }
        const contactVisualProgress = ruyiContactProfile
          ? (isProgressiveSweep ? sweepProgress : (ruyiContactProfile.contactFrame / RUYI_CONTACT_FRAME_COUNT))
          : 0;
        const contactHandAnchor = ruyiContactProfile ? this.getRuyiBodyHandAnchor(contactVisualProgress, ruyiContactProfile) : { x:0, y:0 };
        const ruyiWorldShaft = ruyiContactProfile
          ? getRuyiWorldShaft(this.x, this.y, attackAngle, ruyiContactProfile, contactVisualProgress, reach, contactHandAnchor)
          : null;
        const ruyiContactShape = ruyiContactProfile ? {
          ...ruyiContactProfile,
          ...ruyiWorldShaft,
          mode: isProgressiveSweep ? 'arc' : ruyiContactProfile.mode,
        } : null;
        enemies.forEach(enemy => {
          if (!enemy.alive || enemy.isAlly) return;
          if (isProgressiveSweep && pending.hitTargets.has(enemy)) return;
          const dist = Math.hypot(enemy.x - this.x, enemy.y - this.y);
          const isOnVisibleContactPath = ruyiContactShape
            ? isRuyiContactHit(ruyiContactShape, enemy.x, enemy.y, enemy.radius)
            : dist <= reach + enemy.radius;
          if (isOnVisibleContactPath) {
            const angleToEnemy = Math.atan2(enemy.y - this.y, enemy.x - this.x);
            let angleDiff = Math.abs(attackAngle - angleToEnemy);
            while (angleDiff > Math.PI) angleDiff = Math.abs(angleDiff - Math.PI * 2);

            if (ruyiContactShape || currentCombo === 1 || comboMove?.effect === 'spin' || angleDiff <= arc / 2) {
              hitAny = true;
              const visibleContactPoint = ruyiContactShape
                ? getRuyiContactPoint(ruyiContactShape, enemy.x, enemy.y)
                : { x:enemy.x, y:enemy.y };
              let formCritChance = this.getActiveFormSkillRank('tiger_claws') * 0.04;
              formCritChance += this.getActiveFormSkillRank('roc_sight') * 0.08;
              if (this.hasActiveFormSkill('roc_sky_scout') && enemy.formWeakPointTimer > 0) formCritChance += 1;
              if (this.hasActiveFormSkill('ape_fist') && currentCombo === 2) formCritChance += Math.min(1, this.getActiveFormSkillRank('ape_fist') * 0.20);
              const truesightRank = this.hasBoon('erlang_truesight') ? this.getBoonLevel('erlang_truesight') : 0;
              const truesightCritChance = truesightRank ? Math.min(0.45, 0.25 + 0.05 * (truesightRank - 1)) : 0;
              const truesightCritDamage = truesightRank ? Math.min(0.90, 0.50 + 0.10 * (truesightRank - 1)) : 0;
              let crit = Math.random() < (0.15 + (isErlang && this.isManifested ? 0.20 : 0) + (formProfile?.crit || 0) + formCritChance + this.permanentCritBonus + (metaUpgrades.golden_eyes * 0.08) + truesightCritChance);
              const formCritDamage = this.getActiveFormSkillRank('tiger_crit') * 0.30;
              let finalDmg = baseDmg * (crit ? 2.5 + formCritDamage + truesightCritDamage : 1.0);
              if (isErlang && enemy.judgmentMarkTimer > 0) finalDmg *= 1 + (this.erlangSkillEffects?.markDamage || 0);
              if (isErlang) finalDmg *= 1 + (this.erlangSkillEffects?.armorBreak || 0) * 0.35;
              if (enemy.isBoss) finalDmg *= 1 + (this.alignmentBossDamage || 0);
              if (enemy.hp < enemy.maxHp * .5) finalDmg *= 1 + (this.alignmentExecuteDamage || 0);
              if (enemy.isBoss) finalDmg *= 1 + this.getActiveFormSkillRank('dragon_subdue') * 0.12;
              if (enemy.hp < enemy.maxHp * 0.40) finalDmg *= 1 + this.getActiveFormSkillRank('tiger_slay') * 0.25;
              finalDmg *= 1 + this.getActiveFormSkillRank('roc_talon') * 0.08;
              if (this.alignmentDashEmpowered) finalDmg *= 1 + (this.alignmentEffects?.dashDamage || 0);

              const isHeavyHit = currentCombo > 0 || isTitan || this.isAwakened;
              enemy.takeDamage(finalDmg, crit, isHeavyHit);
              if (isProgressiveSweep) pending.hitTargets.add(enemy);
              if (ruyiContactShape) {
                // The enemy holds its authored hurt/defeat silhouette long
                // enough for the staff-tip contact and impact frame to read.
                enemy.hurtTimer = Math.max(enemy.hurtTimer || 0, enemy.hp > 0 ? .20 : .12);
                enemy.meleeContactHoldTimer = Math.max(enemy.meleeContactHoldTimer || 0, enemy.hp > 0 ? .08 : .12);
              }
              if (isErlang && comboMove?.effect === 'launch' && !enemy.isBoss) {
                enemy.applyKnockdown?.(0.8 + (this.erlangSkillEffects?.launchForce || 0) / 100);
                enemy.knockbackX += Math.cos(attackAngle) * (this.erlangSkillEffects?.launchForce || 0);
                enemy.knockbackY += Math.sin(attackAngle) * (this.erlangSkillEffects?.launchForce || 0);
              }
              if (isErlang && comboMove?.effect === 'hound_pin') {
                enemy.applyStun?.(1.15 + (this.erlangSkillEffects?.houndStun || 0));
                this.resolveXiaotianquanCommand({ x: enemy.x, y: enemy.y });
              }
              if (isErlang && comboMove?.effect === 'third_eye') {
                enemy.judgmentMarkTimer = Math.max(enemy.judgmentMarkTimer || 0, 5);
                enemies.filter(target => target !== enemy && target.alive && !target.isAlly && Math.hypot(target.x - enemy.x, target.y - enemy.y) < 175)
                  .slice(0, 3).forEach(target => { target.takeDamage(finalDmg * .32, false, true); fxList.push(new AnimatedLightningStrike(target.x, target.y)); });
              }
              if (crit && this.hasActiveFormSkill('tiger_frenzy')) {
                this.healFromDamage(finalDmg, Math.min(0.075, this.getActiveFormSkillRank('tiger_frenzy') * 0.015));
                this.cueFormSkill('tiger_frenzy', this.x, this.y, 0.62);
              }
              if (!enemy.isBoss && enemy.alive && this.hasActiveFormSkill('tiger_execute') && Math.random() < Math.min(0.75, this.getActiveFormSkillRank('tiger_execute') * 0.15)) {
                this.cueFormSkill('tiger_execute', enemy.x, enemy.y, 0.82);
                enemy.takeDamage(enemy.hp + 1, true, true);
              }
              if (this.alignmentLifeLeech > 0) this.healFromDamage(finalDmg, this.alignmentLifeLeech);

              const knock = (isTitan ? 320 : (currentCombo === 2 ? 260 : 150)) * (formProfile?.knockback || 1);
              enemy.knockbackX += Math.cos(angleToEnemy) * knock;
              enemy.knockbackY += Math.sin(angleToEnemy) * knock;

              if (impactFxBudget > 0) {
                fxList.push(new HadesHitSparkFX(visibleContactPoint.x, visibleContactPoint.y, angleToEnemy, '#ffffff'));
                if (isHeavyHit || ruyiContactShape) fxList.push(new RuyiImpactBurstFX(visibleContactPoint.x, visibleContactPoint.y, currentCombo === 2 ? 0.72 : 0.56));
                impactFxBudget--;
              }

              this.awakenGauge = Math.min(this.maxAwakenGauge, this.awakenGauge + (crit ? 5 : 2.5));
              if (formProfile && !formProcUsed) {
                this.procFormAttackOnHit(enemy, currentCombo, attackAngle);
                formProcUsed = true;
              }
              if (this.boons.attack) {
                this.procAttackBoonOnHit(enemy, this.boons.attack.id, this.boons.attack.level || 1, finalDmg, !boonVisualUsed);
                boonVisualUsed = true;
              }
              if (!alignmentProcUsed) {
                this.procAlignmentOnHit(enemy, currentCombo, finalDmg);
                alignmentProcUsed = true;
              }
            }
          }
        });

        if (hitAny) {
          sound.playStaffHit(isTitan);
          if (currentCombo === 2 || isTitan) sound.playStaffSmash(isTitan);
          if (!pending.contactFeedbackPlayed) {
            createScreenShake(currentCombo === 2 ? (isTitan ? 8 : 5) : (currentCombo === 1 ? 3 : 2));
            beginConfirmedMeleeHitStop(currentCombo === 2 || isTitan ? .095 : .055);
            pending.contactFeedbackPlayed = true;
          }
          this.alignmentDashEmpowered = false;
        }
      }

      procAlignmentOnHit(enemy, combo, dealtDamage) {
        const effects = this.alignmentEffects || {};
        const palette = getAlignmentPalette();
        const roll = Math.random();
        const neutralMasteryRank = Math.max(0, Math.floor(effects.neutralCapstone || 0));
        const goodProc = effects.goodCapstone && combo === 2 ? true : roll < (effects.holyChance || 0);
        const evilProc = effects.evilCapstone && combo === 2 ? true : roll < (effects.voidChance || 0);
        const balanceProc = neutralMasteryRank >= 10 && combo === 2 ? true : roll < Math.min(.85, effects.balanceChance || 0);
        if (goodProc) {
          const holyDamage = 28 + (effects.holyDamage || 0);
          enemies.filter(target => target.alive && !target.isAlly && Math.hypot(target.x - enemy.x, target.y - enemy.y) <= 105 + target.radius).slice(0, 5)
            .forEach(target => { if (target !== enemy) target.takeDamage(holyDamage, false, false); });
          fxList.push(new Shockwave(enemy.x, enemy.y, 105, '#dbeafe'));
          fxList.push(new AnimatedLightningStrike(enemy.x, enemy.y));
        } else if (evilProc) {
          const voidDamage = 34 + (effects.voidDamage || 0);
          enemies.filter(target => target.alive && !target.isAlly && Math.hypot(target.x - enemy.x, target.y - enemy.y) <= 112 + target.radius).slice(0, 5)
            .forEach(target => { if (target !== enemy) target.takeDamage(voidDamage, false, true); });
          fxList.push(new HadesMagicCircleAOEFX(enemy.x, enemy.y, 92, .55, '#a855f7'));
          fxList.push(new Shockwave(enemy.x, enemy.y, 112, '#ef4444'));
        } else if (balanceProc) {
          const masteryMultiplier = 1 + Math.min(.60, neutralMasteryRank * .03);
          const balanceDamage = (22 + Math.max(effects.holyDamage || 0, effects.voidDamage || 0)) * masteryMultiplier;
          enemy.takeDamage(balanceDamage, false, false);
          this.qi = Math.min(this.maxQi, this.qi + 5 + Math.floor(neutralMasteryRank / 5) * 2);
          this.healFromDamage(dealtDamage, effects.balanceHeal || 0);
          fxList.push(new Shockwave(enemy.x, enemy.y, 86, '#facc15'));
          if (neutralMasteryRank >= 5) fxList.push(new Shockwave(enemy.x, enemy.y, 112, '#8b5cf6'));
          if (neutralMasteryRank >= 15) {
            const splashMultiplier = neutralMasteryRank >= 20 ? .50 : .32;
            enemies.filter(target => target !== enemy && target.alive && !target.isAlly && Math.hypot(target.x - enemy.x, target.y - enemy.y) <= 125 + target.radius).slice(0, 4)
              .forEach(target => target.takeDamage(balanceDamage * splashMultiplier, false, false));
          }
          if (neutralMasteryRank >= 20) fxList.push(new HadesMagicCircleAOEFX(enemy.x, enemy.y, 104, .42, palette.secondary));
        }
      }

      getSlashType() {
        if (this.isTransformed) {
          return FORM_COMBAT_PROFILES[this.activeTransformationForm]?.slashType || 'golden';
        }
        return this.getAttackBoonSlashType() || 'golden';
      }

      getAttackBoonSlashType() {
        const id = this.boons.attack?.id;
        if (id === 'nezha_strike' || id === 'bull_strike') return 'fire';
        if (id === 'laojun_strike' || id === 'buddha_palm_strike' || id === 'yanluo_strike') return 'alchemy';
        if (id === 'erlang_strike') return 'thunder';
        if (id === 'aoguang_strike' || id === 'guanyin_strike') return 'water';
        if (id === 'change_strike') return 'ice';
        if (id === 'ironfan_strike') return 'wind';
        if (id === 'luban_anvil_strike') return 'golden';
        return null;
      }

      spawnLayeredStaffSlash(angle, reach, slashType, isFullCircle = false) {
        const boonAccent = this.getAttackBoonSlashType();
        const alignmentPath = getAlignmentPath();
        if (this.isTransformed) {
          // Generated form animation owns the silhouette; this is only its readable
          // elemental contact cue, never a generic golden staff replacement.
          fxList.push(new HadesDivineStaffSlashFX(this.x, this.y, angle, reach, slashType, isFullCircle, 0.62, 0.56));
        } else {
          // Ruyi Jingu Bang's golden signature remains the base under every god boon.
          const alignedBase = alignmentPath === 'evil' ? 'alchemy' : 'golden';
          fxList.push(new HadesDivineStaffSlashFX(this.x, this.y, angle, reach, alignedBase, isFullCircle, 0.88, 0.86));
          if (!boonAccent && alignmentPath === 'good') {
            fxList.push(new HadesDivineStaffSlashFX(this.x, this.y, angle, reach, 'water', isFullCircle, 0.42, 0.42));
          } else if (!boonAccent && alignmentPath === 'evil') {
            fxList.push(new HadesDivineStaffSlashFX(this.x, this.y, angle, reach, 'fire', isFullCircle, 0.38, 0.38));
          }
        }
        if (boonAccent && boonAccent !== (this.isTransformed ? slashType : 'golden')) {
          fxList.push(new HadesDivineStaffSlashFX(this.x, this.y, angle, reach, boonAccent, isFullCircle, 0.48, 0.46));
        }
      }

      procFormAttackOnHit(enemy, combo, attackAngle) {
        const metaPower = this.metaDamageMultiplier || 1;
        if (this.activeTransformationForm === 'dragon') {
          sound.playLightning();
          fxList.push(new AnimatedLightningStrike(enemy.x, enemy.y));
          const thunderRank = this.getActiveFormSkillRank('dragon_thunder');
          enemies.filter(e => e.alive && e !== enemy && Math.hypot(e.x - enemy.x, e.y - enemy.y) < 260)
            .slice(0, combo === 2 ? 3 : 2)
            .forEach(e => {
              e.takeDamage((combo === 2 ? 38 : 24) * (1 + thunderRank * 0.20) * metaPower, false, true);
              fxList.push(new AnimatedLightningStrike(e.x, e.y));
            });
          const clawRank = this.getActiveFormSkillRank('dragon_claw');
          if (clawRank && Math.random() < Math.min(0.85, 0.17 * clawRank)) {
            enemy.takeDamage((34 + clawRank * 14) * metaPower, true, true);
            fxList.push(new AnimatedLightningStrike(enemy.x, enemy.y));
            this.cueFormSkill('dragon_claw', enemy.x, enemy.y, 0.72);
          }
          const stormRank = this.getActiveFormSkillRank('dragon_storm');
          if (stormRank && this.qi >= this.maxQi * 0.92) {
            enemies.filter(target => target.alive && !target.isAlly && Math.hypot(target.x - enemy.x, target.y - enemy.y) <= 230 + target.radius)
              .slice(0, 3 + stormRank).forEach(target => { target.takeDamage((20 + stormRank * 11) * metaPower, false, true); fxList.push(new AnimatedLightningStrike(target.x, target.y)); });
            this.qi = Math.max(0, this.qi - 8);
            this.cueFormSkill('dragon_storm', enemy.x, enemy.y, 0.82);
          }
          const tsunamiRank = this.getActiveFormSkillRank('dragon_tsunami');
          if (tsunamiRank && combo === 2) {
            enemies.filter(target => target.alive && !target.isAlly && Math.hypot(target.x - enemy.x, target.y - enemy.y) <= 175 + target.radius)
              .forEach(target => { target.takeDamage((25 + tsunamiRank * 18) * metaPower, false, true); target.knockbackX += Math.cos(attackAngle) * 280; target.knockbackY += Math.sin(attackAngle) * 280; });
            fxList.push(new TransformationSpellFX('dragon', enemy.x, enemy.y, 175, 0.70));
            this.cueFormSkill('dragon_tsunami', enemy.x, enemy.y, 0.94);
          }
        } else if (this.activeTransformationForm === 'tiger') {
          const bleedRank = this.getActiveFormSkillRank('tiger_bleed');
          enemy.applyBurn(((combo === 2 ? 42 : 26) + bleedRank * 20) * metaPower, 2.4);
          fxList.push(new ElementalSlashFX(enemy.x, enemy.y, attackAngle, 'fire', 110));
          if (bleedRank) this.cueFormSkill('tiger_bleed', enemy.x, enemy.y, 0.54);
        } else if (this.activeTransformationForm === 'roc') {
          enemy.knockbackX += Math.cos(attackAngle) * 180;
          enemy.knockbackY += Math.sin(attackAngle) * 180;
          fxList.push(new ElementalSlashFX(enemy.x, enemy.y, attackAngle, 'wind', 125));
          const featherRank = this.getActiveFormSkillRank('roc_feather');
          if (featherRank) {
            [-0.18, 0, 0.18].forEach(offset => projectiles.push(new FormFeatherProjectile(this.x, this.y - 10, attackAngle + offset, (16 + featherRank * 9) * metaPower, '#fbbf24')));
            this.cueFormSkill('roc_feather', this.x, this.y, 0.64);
          }
          const vortexRank = this.getActiveFormSkillRank('roc_vortex');
          if (vortexRank) {
            enemies.filter(target => target.alive && !target.isAlly && Math.hypot(target.x - enemy.x, target.y - enemy.y) <= 150 + target.radius).forEach(target => {
              target.knockbackX += (enemy.x - target.x) * (1.2 + vortexRank * 0.25);
              target.knockbackY += (enemy.y - target.y) * (1.2 + vortexRank * 0.25);
            });
            fxList.push(new TransformationSpellFX('roc', enemy.x, enemy.y, 145, 0.52));
          }
        } else if (this.activeTransformationForm === 'ape') {
          enemies.filter(e => e.alive && e !== enemy && Math.hypot(e.x - enemy.x, e.y - enemy.y) < 125)
            .slice(0, 5).forEach(e => e.takeDamage(36 * metaPower, false, true));
          fxList.push(new Shockwave(enemy.x, enemy.y, 120, '#ea580c'));
          const stoneRank = this.getActiveFormSkillRank('ape_stone');
          if (stoneRank && combo === 2) {
            fxList.push(new FormPulseDamageFX(enemy.x, enemy.y, 190, 2, (28 + stoneRank * 18) * metaPower, '#a16207', 0.22));
            this.cueFormSkill('ape_stone', enemy.x, enemy.y, 0.92);
          }
          const shockRank = this.getActiveFormSkillRank('ape_shockwave');
          if (shockRank && combo === 2) {
            fxList.push(new FormPulseDamageFX(enemy.x, enemy.y, 145 + shockRank * 12, 3, (18 + shockRank * 12) * metaPower, '#fb923c', 0.18));
            this.cueFormSkill('ape_shockwave', enemy.x, enemy.y, 0.78);
          }
        } else if (this.activeTransformationForm === 'tortoise') {
          enemy.applySlow(0.62, 1.4);
          this.hp = Math.min(this.maxHp, this.hp + 3);
          fxList.push(new Shockwave(enemy.x, enemy.y, 88, '#10b981'));
        }
      }

      onFormEnemyDefeated(enemy) {
        if (!this.isTransformed) return;
        if (this.activeTransformationForm === 'dragon') {
          const rank = this.getActiveFormSkillRank('dragon_water_know');
          if (rank) {
            const bonusGold = Math.max(1, Math.round(2 * rank));
            gameState.gold += bonusGold;
            if (Math.random() < 0.06 * rank) gameState.ashes += 1;
            this.qi = Math.min(this.maxQi, this.qi + rank * 1.5);
            this.cueFormSkill('dragon_water_know', enemy.x, enemy.y, 0.52);
          }
        } else if (this.activeTransformationForm === 'tiger') {
          const rank = this.getActiveFormSkillRank('tiger_bloodlust');
          if (rank) {
            this.transformDuration += 0.8 * rank;
            this.cueFormSkill('tiger_bloodlust', enemy.x, enemy.y, 0.58);
          }
        } else if (this.activeTransformationForm === 'roc') {
          const rank = this.getActiveFormSkillRank('roc_solar');
          if (rank) {
            enemies.filter(target => target.alive && !target.isAlly && Math.hypot(target.x - enemy.x, target.y - enemy.y) <= 150 + target.radius)
              .forEach(target => { target.takeDamage((25 + rank * 18) * (this.metaDamageMultiplier || 1), false, false); target.applySlow(0.35, 1.2); });
            fxList.push(new ColossalStaffNovaFX(enemy.x, enemy.y, 150, '#fde047'));
            this.cueFormSkill('roc_solar', enemy.x, enemy.y, 0.82);
          }
        } else if (this.activeTransformationForm === 'ape') {
          const rank = this.getActiveFormSkillRank('ape_stone_boil');
          if (rank && (enemy.maxHp >= 900 || Math.random() < 0.10 * rank)) {
            gameState.gold += 6 * rank;
            this.hp = Math.min(this.maxHp, this.hp + 4 * rank);
            this.cueFormSkill('ape_stone_boil', enemy.x, enemy.y, 0.62);
          }
        }
      }

      procAttackBoonOnHit(enemy, id, level, dealtDamage, emitFx) {
        const metaPower = this.metaDamageMultiplier || 1;
        const rankScale = 1 + 0.35 * (level - 1);
        if (id === 'luban_anvil_strike') {
          if (emitFx) { sound.playAnvilClang(); fxList.push(new ElementalSlashFX(this.x, this.y, this.attackAngle, 'anvil', 155)); }
          enemy.takeDamage(55 * rankScale * metaPower, true, true);
        } else if (id === 'erlang_strike') {
          if (emitFx) { sound.playLightning(); fxList.push(new AnimatedLightningStrike(enemy.x, enemy.y)); }
          enemy.takeDamage(45 * rankScale * metaPower, false, true);
          if (emitFx) enemies.filter(e => e.alive && e !== enemy && Math.hypot(e.x - enemy.x, e.y - enemy.y) < 280)
            .slice(0, Math.min(3, level)).forEach(e => { e.takeDamage(24 * rankScale * metaPower, false, true); fxList.push(new AnimatedLightningStrike(e.x, e.y)); });
        } else if (id === 'guanyin_strike') {
          this.applyLifeLeechHealing(GUANYIN_STRIKE_HEAL_BASE + (level - 1) * GUANYIN_STRIKE_HEAL_PER_RANK);
          if (emitFx) fxList.push(new Shockwave(this.x, this.y, 58, '#34d399'));
        } else if (id === 'nezha_strike') {
          if (emitFx) { sound.playFire(); fxList.push(new ElementalSlashFX(this.x, this.y, this.attackAngle, 'fire', 150)); }
          enemy.applyBurn(60 * rankScale * metaPower, 3);
        } else if (id === 'laojun_strike') {
          if (emitFx) { sound.playFire(); fxList.push(new ElementalSlashFX(this.x, this.y, this.attackAngle, 'alchemy', 150)); }
          enemy.takeDamage(50 * rankScale * metaPower, false, true);
        } else if (id === 'aoguang_strike') {
          if (emitFx) fxList.push(new ElementalSlashFX(this.x, this.y, this.attackAngle, 'water', 155));
          enemy.takeDamage(40 * rankScale * metaPower, false, true);
          enemy.knockbackX += Math.cos(this.attackAngle) * (130 + level * 20);
          enemy.knockbackY += Math.sin(this.attackAngle) * (130 + level * 20);
        } else if (id === 'change_strike') {
          if (emitFx) fxList.push(new ElementalSlashFX(this.x, this.y, this.attackAngle, 'ice', 145));
          enemy.takeDamage(35 * rankScale * metaPower, false, true);
          enemy.applyFreeze(1.2 + (level - 1) * 0.15);
        } else if (id === 'ironfan_strike') {
          if (emitFx) fxList.push(new ElementalSlashFX(this.x, this.y, this.attackAngle, 'wind', 165));
          enemy.takeDamage(35 * rankScale * metaPower, false, true);
          enemy.knockbackX += Math.cos(this.attackAngle) * 120;
          enemy.knockbackY += Math.sin(this.attackAngle) * 120;
        } else if (id === 'bull_strike') {
          if (emitFx) fxList.push(new GroundFissureFX(this.x, this.y, this.attackAngle, 145, '#ea580c'));
          enemy.takeDamage(dealtDamage * (0.40 + 0.10 * (level - 1)), false, true);
        } else if (id === 'buddha_palm_strike' && this.currentCombo === 2 && emitFx) {
          const palmDamage = dealtDamage * (0.40 + 0.08 * (level - 1));
          enemies.filter(target => target.alive && !target.isAlly && Math.hypot(target.x - enemy.x, target.y - enemy.y) <= 125 + target.radius)
            .forEach(target => target.takeDamage(palmDamage, false, true));
          fxList.push(new ColossalStaffNovaFX(enemy.x, enemy.y, 125, '#facc15'));
          fxList.push(new Shockwave(enemy.x, enemy.y, 125, '#fde68a'));
        } else if (id === 'yanluo_strike') {
          if (emitFx) fxList.push(new ElementalSlashFX(enemy.x, enemy.y, this.attackAngle, 'alchemy', 105));
          const markedTarget = enemy;
          setTimeout(() => { if (markedTarget.alive) markedTarget.takeDamage(70 * rankScale * metaPower, false, true); }, 3000);
        }
      }

      performQSkill() {
        if (gameState.playableHero === 'erlang') this.performErlangEyeLance();
        else this.performSpecial();
      }

      performRightClickSkill() {
        if (gameState.playableHero === 'erlang') this.commandXiaotianquan();
        else this.performSpecial();
      }

      performErlangEyeLance() {
        if (this.specialCooldown > 0 || this.isDashing || this.isCastingSpell || this.isAttacking || this.isSpecialActive) return;
        const training = this.erlangSkillEffects || {};
        const qiCost = 20;
        if (this.qi < qiCost) {
          floatingTexts.push(new FloatingText(this.x, this.y - 40, uiText('真气不足 (天眼需 20 点真气)!', 'Not enough Qi (Third Eye requires 20)!'), '#f87171'));
          return;
        }
        this.qi -= qiCost;
        this.specialCooldown = this.isManifested ? 1.15 : 1.6;
        this.isSpecialActive = true;
        this.specialMaxDuration = 0.62;
        this.specialDuration = this.specialMaxDuration;
        const worldMouseX = gameState.mouse.x - viewWidth / 2 + this.x;
        const worldMouseY = gameState.mouse.y - viewHeight / 2 + this.y;
        const angle = Math.atan2(worldMouseY - this.y, worldMouseX - this.x);
        this.attackAngle = angle;
        this.facing = Math.cos(angle) < 0 ? -1 : 1;
        this.pendingSpecial = {
          kind: 'erlang_eye', angle, range: 780 + (training.eyeRange || 0),
          width: 34 + (training.eyeWidth || 0), chains: training.eyeChains || 0,
          damage: 105 * (1 + (training.eyeDamage || 0)) * (1 + (this.isManifested ? (training.manifestDamage || 0) : 0)) * (this.metaDamageMultiplier || 1), contactAt: 0.48
        };
        sound.playLightning();
      }

      commandXiaotianquan() {
        if (this.houndCooldown > 0 || this.isDashing || this.isAttacking || this.isCastingSpell || this.isSpecialActive) return;
        const houndReduction = this.erlangSkillEffects?.houndCooldown || 0;
        this.houndCooldown = (this.isManifested ? 1.8 : 3.0) * Math.max(.55, 1 - houndReduction);
        this.isSpecialActive = true;
        this.specialMaxDuration = 0.46;
        this.specialDuration = this.specialMaxDuration;
        const worldMouseX = gameState.mouse.x - viewWidth / 2 + this.x;
        const worldMouseY = gameState.mouse.y - viewHeight / 2 + this.y;
        const angle = Math.atan2(worldMouseY - this.y, worldMouseX - this.x);
        this.attackAngle = angle;
        this.facing = Math.cos(angle) < 0 ? -1 : 1;
        const specialRank = Math.max(1, this.boons.special?.level || 1);
        this.pendingSpecial = { kind: 'erlang_hound', x: worldMouseX, y: worldMouseY, specialRank, contactAt: 0.38 };
        sound.playHoundBark();
      }

      resolveErlangEyeLance(pending) {
        const endX = this.x + Math.cos(pending.angle) * pending.range;
        const endY = this.y + Math.sin(pending.angle) * pending.range;
        const lengthSq = pending.range * pending.range;
        const directHits = [];
        enemies.forEach(enemy => {
          if (!enemy.alive || enemy.isAlly) return;
          const along = Math.max(0, Math.min(1, ((enemy.x - this.x) * (endX - this.x) + (enemy.y - this.y) * (endY - this.y)) / lengthSq));
          const hitX = this.x + (endX - this.x) * along;
          const hitY = this.y + (endY - this.y) * along;
          if (Math.hypot(enemy.x - hitX, enemy.y - hitY) > enemy.radius + (pending.width || 34)) return;
          enemy.takeDamage(pending.damage * (this.isManifested ? 1.25 : 1), true, false);
          enemy.judgmentMarkTimer = 4;
          directHits.push(enemy);
          fxList.push(new AnimatedLightningStrike(enemy.x, enemy.y));
        });
        let chainSource = directHits[0];
        const chained = new Set(directHits);
        for (let jump = 0; chainSource && jump < (pending.chains || 0); jump++) {
          const next = enemies.filter(enemy => enemy.alive && !enemy.isAlly && !chained.has(enemy) && Math.hypot(enemy.x - chainSource.x, enemy.y - chainSource.y) <= 230)
            .sort((a, b) => Math.hypot(a.x - chainSource.x, a.y - chainSource.y) - Math.hypot(b.x - chainSource.x, b.y - chainSource.y))[0];
          if (!next) break;
          next.takeDamage(pending.damage * .38, false, true);
          next.judgmentMarkTimer = 4;
          chained.add(next);
          fxList.push(new ExtendedStaffBeam(chainSource.x, chainSource.y, Math.atan2(next.y - chainSource.y, next.x - chainSource.x), Math.hypot(next.x - chainSource.x, next.y - chainSource.y), '#67e8f9'));
          fxList.push(new AnimatedLightningStrike(next.x, next.y));
          chainSource = next;
        }
        fxList.push(new ExtendedStaffBeam(this.x, this.y, pending.angle, pending.range, '#93c5fd'));
        fxList.push(new StaffMotionWaveFX(this.x, this.y, pending.angle, pending.range * 0.86, '#60a5fa'));
        createScreenShake(4);
      }

      resolveXiaotianquanCommand(pending) {
        let hound = enemies.find(enemy => enemy.isAlly && enemy.isHound && enemy.alive);
        if (!hound) {
          hound = new Enemy('xiaotianquan_hound', this.x - this.facing * 46, this.y + 36, true);
          enemies.push(hound);
        }
        this.hound = hound;
        const hostiles = enemies.filter(enemy => enemy.alive && !enemy.isAlly && !enemy.isDying);
        let target = hostiles
          .map(enemy => ({ enemy, distance: Math.hypot(enemy.x - pending.x, enemy.y - pending.y) }))
          .filter(item => item.distance <= 150)
          .sort((a, b) => a.distance - b.distance)[0]?.enemy;
        if (!target) target = hostiles
          .filter(enemy => Math.hypot(enemy.x - this.x, enemy.y - this.y) <= 900)
          .sort((a, b) => Math.hypot(a.x - pending.x, a.y - pending.y) - Math.hypot(b.x - pending.x, b.y - pending.y))[0];
        if (!target) {
          this.houndCooldown = Math.min(this.houndCooldown, 0.6);
          return;
        }
        hound.commandTarget = target;
        hound.commandPoint = { x: pending.x, y: pending.y };
        hound.companionCommandActive = true;
        hound.attackTarget = target;
        hound.attackCooldown = 0.9;
        hound.state = 'hound_empowered_slam';
        hound.isAttacking = true;
        hound.attackDuration = 0.92;
        hound.attackMaxDuration = 0.92;
        hound.shotFired = false;
        hound.animClock = 0;
        hound.houndSlamStartX = hound.x;
        hound.houndSlamStartY = hound.y;
        hound.houndSlamTargetX = target.x;
        hound.houndSlamTargetY = target.y;
        hound.houndSlamRank = Math.max(1, pending.specialRank || 1);
        hound.houndVisualLift = 0;
        hound.attackAngle = Math.atan2(target.y - hound.y, target.x - hound.x);
        hound.facing = Math.cos(hound.attackAngle) < 0 ? -1 : 1;
        fxList.push(new HadesMagicCircleAOEFX(hound.x, hound.y, 64, 0.62, '#8b5cf6'));
        fxList.push(new AnimatedLightningStrike(hound.x, hound.y));
        fxList.push(new HadesMagicCircleAOEFX(target.x, target.y, 76 + hound.houndSlamRank * 4, 0.82, '#60a5fa'));
        floatingTexts.push(new FloatingText(
          target.x, target.y - target.radius - 30,
          uiText(`哮天犬 · 神雷坠（神技 ${hound.houndSlamRank} 重）`, `Xiaotianquan · Divine Thunderfall (Special Lv.${hound.houndSlamRank})`),
          '#fde68a', 16
        ));
      }

      performSpecial() {
        if (this.specialCooldown > 0 || this.isDashing || this.isCastingSpell || this.isAttacking || this.isSpecialActive) return;
        this.specialCooldown = 1.45;
        this.isSpecialActive = true;
        const formProfile = this.isTransformed ? FORM_COMBAT_PROFILES[this.activeTransformationForm] : null;
        this.specialMaxDuration = 1.22;
        this.specialDuration = this.specialMaxDuration;

        const weaponProfile = RUYI_WEAPON_PROFILES[this.weaponStyle] || RUYI_WEAPON_PROFILES.normal;
        const weaponLevel = this.boons.weapon?.level || 1;
        const isTitan = weaponProfile.id === 'titan';
        sound.playStaffSwing(2, isTitan);

        const worldMouseX = gameState.mouse.x - viewWidth / 2 + this.x;
        const worldMouseY = gameState.mouse.y - viewHeight / 2 + this.y;
        const angle = Math.atan2(worldMouseY - this.y, worldMouseX - this.x);
        this.attackAngle = angle;
        const dx = worldMouseX - this.x;
        const dy = worldMouseY - this.y;
        if (Math.abs(dy) > Math.abs(dx)) {
          this.direction = dy < 0 ? 'up' : 'down';
          this.facing = dx < 0 ? -1 : 1;
        } else {
          this.direction = dx < 0 ? 'left' : 'right';
          this.facing = dx < 0 ? -1 : 1;
        }

        let baseDmg = 120 * weaponProfile.damage * (1 + 0.18 * (weaponLevel - 1));
        let maxRange = 720 * weaponProfile.range * (1 + Math.min(0.25, 0.05 * (weaponLevel - 1)));
        if (formProfile) {
          baseDmg *= formProfile.damage;
          maxRange *= Math.min(1.18, formProfile.reach);
          if (this.activeTransformationForm === 'tiger') {
            maxRange *= 1 + this.getActiveFormSkillRank('tiger_sword') * 0.12;
            baseDmg *= 1 + this.getActiveFormSkillRank('tiger_sword') * 0.10;
          }
        }
        if (this.boons.special) {
          const lvl = this.boons.special.level || 1;
          baseDmg *= (1 + 0.35 * (lvl - 1));
        }
        baseDmg *= 1 + (this.alignmentSpecialDamage || 0);
        baseDmg *= this.metaDamageMultiplier || 1;
        baseDmg *= 1 + (this.absorbedBossQi || 0) * .015;
        baseDmg *= gameState.transformationDoctrine === '18' ? 1.35 : (gameState.transformationDoctrine === '36' ? 1.15 : 1);
        if (!this.hasRuyiStaff) {
          baseDmg *= 0.68;
          maxRange *= 0.72;
        }

        const fxColor = this.getActiveGodColor();
        // Frame 2 is the authored release. The projectile then owns its outward
        // and return collision passes while Wukong finishes the catch animation.
        this.pendingSpecial = { angle, maxRange, baseDmg, fxColor, isTitan, weaponProfile, formProfile, contactAt: 0.20 };
      }

      resolvePendingSpecial() {
        const pending = this.pendingSpecial;
        if (!pending) return;
        this.pendingSpecial = null;
        if (pending.kind === 'erlang_eye') {
          this.resolveErlangEyeLance(pending);
          return;
        }
        if (pending.kind === 'erlang_hound') {
          this.resolveXiaotianquanCommand(pending);
          return;
        }
        const { angle, maxRange, baseDmg, fxColor, isTitan, weaponProfile, formProfile } = pending;
        const projectile = new RuyiBoomerangProjectile(this, angle, maxRange, baseDmg, fxColor, weaponProfile, formProfile);
        projectiles.push(projectile);
        this.onRuyiCreated(projectile);
        this.triggerFormSpecialCast(projectile);
        fxList.push(new StaffMotionWaveFX(this.x, this.y, angle, 84, fxColor));
        fxList.push(new RadialSparksFX(this.x + Math.cos(angle) * 34, this.y + Math.sin(angle) * 34, 6, fxColor, 30));
        createScreenShake(isTitan ? 5 : 2);
      }

      triggerFormSpecialCast(source) {
        if (!this.isTransformed) return;
        if (this.activeTransformationForm === 'roc') {
          const rank = this.getActiveFormSkillRank('roc_feather_burst');
          if (rank) {
            const count = 6 + rank * 2;
            for (let i = 0; i < count; i++) {
              const angle = source.angle + (i / Math.max(1, count - 1) - 0.5) * Math.PI * 0.9;
              projectiles.push(new FormFeatherProjectile(this.x, this.y - 18, angle, (22 + rank * 11) * (this.metaDamageMultiplier || 1), '#fde047'));
            }
            this.cueFormSkill('roc_feather_burst', this.x, this.y, 1.0);
          }
        } else if (this.activeTransformationForm === 'tiger' && this.hasActiveFormSkill('tiger_sword')) {
          fxList.push(new ExtendedStaffBeam(source.startX, source.startY, source.angle, Math.min(1080, source.maxRange), '#facc15'));
          this.cueFormSkill('tiger_sword', this.x, this.y, 0.78);
        }
      }

      procFormSpecialOnHit(enemy, isReturn, travelAngle, source) {
        if (!this.isTransformed) return;
        const power = this.metaDamageMultiplier || 1;
        if (this.activeTransformationForm === 'dragon') {
          const rank = this.getActiveFormSkillRank('dragon_breath');
          if (rank) {
            const radius = 82 + rank * 10;
            enemies.filter(target => target.alive && !target.isAlly && Math.hypot(target.x - enemy.x, target.y - enemy.y) <= radius + target.radius)
              .forEach(target => target.takeDamage(source.damage * (0.10 + rank * 0.06), false, true));
            fxList.push(new TransformationSpellFX('dragon', enemy.x, enemy.y, radius, 0.48));
            this.cueFormSkill('dragon_breath', enemy.x, enemy.y, 0.62);
          }
        } else if (this.activeTransformationForm === 'ape') {
          const rank = this.getActiveFormSkillRank('ape_spit_flame');
          if (rank) {
            enemy.applyBurn((45 + rank * 25) * power, 2.2);
            fxList.push(new AnimatedFireExplosion(enemy.x, enemy.y, 58 + rank * 6));
            this.cueFormSkill('ape_spit_flame', enemy.x, enemy.y, 0.62);
          }
        } else if (this.activeTransformationForm === 'tortoise') {
          enemy.applySlow(0.42, isReturn ? 2.2 : 1.2);
          this.formBarrier = Math.min(this.formBarrierMax, this.formBarrier + 4);
        }
      }

      onRuyiCreated(source) {
        if (source.weaponProfile.id === 'extend') {
          fxList.push(new ExtendedStaffBeam(source.startX, source.startY, source.angle, Math.min(source.maxRange, 1180), '#f59e0b'));
        }
      }

      onRuyiTurn(source) {
        if (source.weaponProfile.turnSlam) {
          enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - source.x, enemy.y - source.y) <= 160 + enemy.radius)
            .forEach(enemy => enemy.takeDamage(source.damage * 0.35, false, true));
          fxList.push(new GroundFissureFX(source.x, source.y, source.angle, 160, '#f59e0b'));
          fxList.push(new Shockwave(source.x, source.y, 160, '#fbbf24'));
          createScreenShake(8);
        }
        if (this.hasDeitySynergy('furnace_forged_needle')) {
          enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - source.x, enemy.y - source.y) <= 115 + enemy.radius)
            .forEach(enemy => enemy.takeDamage(source.damage * 0.35, false, true));
          fxList.push(new AnimatedFireExplosion(source.x, source.y, 115));
        }
        if (this.hasDeitySynergy('wind_calls_rain')) {
          enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - source.x, enemy.y - source.y) <= 190 + enemy.radius)
            .forEach(enemy => {
              enemy.takeDamage(source.damage * 0.20, false, true);
              enemy.applySlow(0.70, 2.2);
            });
          fxList.push(new AnimatedWaterWave(source.x, source.y, source.angle));
          fxList.push(new Shockwave(source.x, source.y, 190, '#67e8f9'));
        }
      }

      onRuyiCatch(source) {
        if (source.hitCount <= 0 || !this.hasDeitySynergy('compassionate_lotus_return')) return;
        const heal = Math.min(10, this.maxHp * 0.03);
        this.hp = Math.min(this.maxHp, this.hp + heal);
        enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - this.x, enemy.y - this.y) <= 145 + enemy.radius)
          .forEach(enemy => enemy.takeDamage(source.damage * 0.30, false, true));
        fxList.push(new ColossalStaffNovaFX(this.x, this.y, 145, '#fde68a'));
        fxList.push(new Shockwave(this.x, this.y, 145, '#6ee7b7'));
        floatingTexts.push(new FloatingText(this.x, this.y - 42, gameState.language === 'en' ? `Compassionate Lotus +${Math.round(heal)} HP` : `慈悲莲印 · 气血 +${Math.round(heal)}`, '#6ee7b7'));
      }

      onRuyiReflect(source) {
        if (!this.hasBoon('guanyin_special') || source.reflectedCount > 5) return;
        this.qi = Math.min(this.maxQi, this.qi + 2);
      }

      applySpecialBoonOnHit(enemy, isReturn, travelAngle, source) {
        const boon = this.boons.special;
        if (!boon || !enemy.alive) return;
        const levelScale = 1 + 0.22 * ((boon.level || 1) - 1);
        if (boon.id === 'erlang_special') {
          enemy.takeDamage(32 * levelScale, false, false);
          fxList.push(new AnimatedLightningStrike(enemy.x, enemy.y));
        } else if (boon.id === 'guanyin_special') {
          if (!source.guanyinRestoredQi) {
            source.guanyinRestoredQi = true;
            this.qi = Math.min(this.maxQi, this.qi + 15);
            floatingTexts.push(new FloatingText(this.x, this.y - 42, uiText('慈悲回流 · 真气 +15', 'Compassion Reflow · Qi +15'), '#6ee7b7'));
          }
        } else if (boon.id === 'nezha_special') {
          enemy.applyBurn(56 * levelScale, 2.6);
          enemy.knockbackX += Math.cos(travelAngle) * 90;
          enemy.knockbackY += Math.sin(travelAngle) * 90;
          fxList.push(new AnimatedFireExplosion(enemy.x, enemy.y, 44));
        } else if (boon.id === 'laojun_special') {
          enemy.takeDamage(38 * levelScale, false, true);
          fxList.push(new AnimatedFireExplosion(enemy.x, enemy.y, 42));
        } else if (boon.id === 'aoguang_special') {
          enemy.applyFreeze(0.65 + 0.08 * (boon.level || 1));
          fxList.push(new AnimatedWaterWave(enemy.x, enemy.y, travelAngle));
        } else if (boon.id === 'bull_special') {
          enemy.knockbackX += Math.cos(travelAngle) * 210;
          enemy.knockbackY += Math.sin(travelAngle) * 210;
          fxList.push(new GroundFissureFX(enemy.x, enemy.y, travelAngle, 96, '#ea580c'));
        } else if (boon.id === 'ironfan_special') {
          enemy.applySlow(0.58, 1.5);
          enemy.knockbackX += Math.cos(travelAngle) * 135;
          enemy.knockbackY += Math.sin(travelAngle) * 135;
          fxList.push(new ElementalSlashFX(enemy.x, enemy.y, travelAngle, 'wind', 96));
        } else if (boon.id === 'buddha_dharma_return') {
          if (!isReturn) {
            source.buddhaSeals.add(enemy);
            fxList.push(new Shockwave(enemy.x, enemy.y, 48, '#fde68a'));
          } else if (source.buddhaSeals.has(enemy) && !source.buddhaDetonated.has(enemy)) {
            source.buddhaDetonated.add(enemy);
            enemies.filter(target => target.alive && !target.isAlly && Math.hypot(target.x - enemy.x, target.y - enemy.y) <= 90 + target.radius)
              .forEach(target => target.takeDamage(source.damage * 0.45 * levelScale, false, true));
            fxList.push(new ColossalStaffNovaFX(enemy.x, enemy.y, 90, '#facc15'));
          }
        } else if (boon.id === 'yanluo_special' && !enemy.isBoss && enemy.hp / enemy.maxHp <= 0.15) {
          fxList.push(new ColossalStaffNovaFX(enemy.x, enemy.y, 72, '#ef4444'));
          enemy.takeDamage(enemy.hp + 1, true, true);
        } else if (boon.id === 'change_special') {
          enemy.applyFreeze(isReturn ? 1.05 : 0.55);
          fxList.push(new Shockwave(enemy.x, enemy.y, isReturn ? 66 : 46, '#93c5fd'));
        }
      }

      performErlangJudgmentArray() {
        if (this.castCooldown > 0 || this.isDashing || this.isAttacking || this.isSpecialActive) return;
        const training = this.erlangSkillEffects || {};
        if (this.qi < 65) {
          floatingTexts.push(new FloatingText(this.x, this.y - 40, uiText('真气不足 (审判阵需 65 点真气)!', 'Not enough Qi (Judgment Array requires 65)!'), '#f87171'));
          return;
        }
        this.qi -= 65;
        this.castCooldown = this.isManifested ? 4.1 : 5.5;
        this.isCastingSpell = true;
        this.castSpellDuration = 0.72;
        this.castSpellMaxDuration = 0.72;
        const worldMouseX = gameState.mouse.x - viewWidth / 2 + this.x;
        const worldMouseY = gameState.mouse.y - viewHeight / 2 + this.y;
        const radius = 175 + (training.arrayRadius || 0);
        const duration = 2.4 + (training.arrayDuration || 0);
        this.castActive = { kind: 'erlang_judgment', x: worldMouseX, y: worldMouseY, radius, duration, tickTimer: 0.3, pulseInterval: 0.6, angle: 0, color: '#60a5fa', damageMultiplier: 1 + (training.arrayDamage || 0) };
        fxList.push(new HadesMagicCircleAOEFX(worldMouseX, worldMouseY, radius, duration, '#60a5fa'));
        floatingTexts.push(new FloatingText(worldMouseX, worldMouseY - 50, uiText('灌江口 · 天眼审判阵！', 'Guanjiang Judgment Array!'), '#bfdbfe', 18));
        sound.playLightning();
      }

      performTransformationSpell() {
        if (!this.isTransformed || this.castCooldown > 0 || this.isDashing || this.isAttacking || this.isSpecialActive) return;
        const qiCost = 45;
        if (this.qi < qiCost) {
          floatingTexts.push(new FloatingText(this.x, this.y - 42, uiText('真气不足（真身法术需 45）', 'Not enough Qi (Form Spell requires 45)'), '#f87171'));
          return;
        }
        this.qi -= qiCost;
        this.castCooldown = 4.8;
        this.isCastingSpell = true;
        this.castSpellDuration = 0.78;
        this.castSpellMaxDuration = 0.78;
        const worldMouseX = gameState.mouse.x - viewWidth / 2 + this.x;
        const worldMouseY = gameState.mouse.y - viewHeight / 2 + this.y;
        this.attackAngle = Math.atan2(worldMouseY - this.y, worldMouseX - this.x);
        const profile = FORM_COMBAT_PROFILES[this.activeTransformationForm] || FORM_COMBAT_PROFILES.dragon;
        const power = this.metaDamageMultiplier || 1;
        let spellX = worldMouseX;
        let spellY = worldMouseY;
        let radius = 165;

        if (this.activeTransformationForm === 'dragon') {
          const diveRank = this.getActiveFormSkillRank('dragon_dive');
          const rainRank = this.getActiveFormSkillRank('dragon_rain');
          radius = 135 + diveRank * 15;
          enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - spellX, enemy.y - spellY) <= radius + enemy.radius).forEach(enemy => {
            enemy.takeDamage((55 + diveRank * 28 + rainRank * 10) * power, false, true);
            enemy.applySlow(0.48, 1.6 + rainRank * 0.2);
            fxList.push(new AnimatedLightningStrike(enemy.x, enemy.y));
          });
          this.qi = Math.min(this.maxQi, this.qi + rainRank * 4);
          this.cueFormSkill('dragon_dive', spellX, spellY, 1.0);
          if (rainRank) this.cueFormSkill('dragon_rain', spellX, spellY, 0.72);
        } else if (this.activeTransformationForm === 'tiger') {
          spellX = this.x; spellY = this.y;
          const roarRank = this.getActiveFormSkillRank('tiger_roar');
          radius = 145 + roarRank * 18;
          enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - spellX, enemy.y - spellY) <= radius + enemy.radius).forEach(enemy => {
            const ang = Math.atan2(enemy.y - spellY, enemy.x - spellX);
            enemy.takeDamage((42 + roarRank * 20) * power, false, true);
            enemy.applyFreeze(0.65 + roarRank * 0.18);
            enemy.knockbackX += Math.cos(ang) * 280;
            enemy.knockbackY += Math.sin(ang) * 280;
          });
          this.cueFormSkill('tiger_roar', spellX, spellY, 1.0);
        } else if (this.activeTransformationForm === 'roc') {
          const cycloneRank = this.getActiveFormSkillRank('roc_cyclone');
          radius = 150 + cycloneRank * 18;
          enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - spellX, enemy.y - spellY) <= radius + enemy.radius).forEach(enemy => {
            const dx = spellX - enemy.x, dy = spellY - enemy.y, dist = Math.max(1, Math.hypot(dx, dy));
            enemy.takeDamage((46 + cycloneRank * 24) * power, false, true);
            enemy.knockbackX += dx / dist * 320;
            enemy.knockbackY += dy / dist * 320;
          });
          this.cueFormSkill('roc_cyclone', spellX, spellY, 1.0);
        } else if (this.activeTransformationForm === 'ape') {
          spellX = this.x + Math.cos(this.attackAngle) * 75;
          spellY = this.y + Math.sin(this.attackAngle) * 75;
          const smashRank = this.getActiveFormSkillRank('ape_smash');
          const roarRank = this.getActiveFormSkillRank('ape_roar');
          radius = 165 + smashRank * 20;
          enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - spellX, enemy.y - spellY) <= radius + enemy.radius).forEach(enemy => {
            enemy.takeDamage((75 + smashRank * 36 + roarRank * 12) * power, true, true);
            enemy.applySlow(0.42, 2.0);
          });
          if (roarRank) projectiles.filter(projectile => projectile.alive && projectile.isEnemy).forEach(projectile => { projectile.alive = false; });
          fxList.push(new FormPulseDamageFX(spellX, spellY, radius, 3, (14 + smashRank * 8) * power, '#ea580c', 0.20));
          this.cueFormSkill('ape_smash', spellX, spellY, 1.0);
          if (roarRank) this.cueFormSkill('ape_roar', this.x, this.y, 0.78);
        } else {
          spellX = this.x; spellY = this.y;
          const abyssRank = this.getActiveFormSkillRank('tort_abyss');
          radius = 150 + abyssRank * 20;
          enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - spellX, enemy.y - spellY) <= radius + enemy.radius).forEach(enemy => {
            enemy.takeDamage((34 + abyssRank * 18) * power, false, false);
            enemy.applySlow(0.38, 2.8 + abyssRank * 0.25);
          });
          this.formBarrier = Math.min(this.formBarrierMax + abyssRank * 30, this.formBarrier + abyssRank * 30);
          this.cueFormSkill('tort_abyss', spellX, spellY, 1.0);
        }

        fxList.push(new TransformationSpellFX(this.activeTransformationForm, spellX, spellY, radius, 1.15));
        floatingTexts.push(new FloatingText(spellX, spellY - radius * 0.42,
          uiText('真身法术 · 地煞显化！', 'Form Spell · Earthly Art Manifest!'), profile.color, 17));
        createScreenShake(this.activeTransformationForm === 'ape' ? 10 : 5);
      }

      performCast() {
        if (gameState.playableHero === 'erlang') {
          this.performErlangJudgmentArray();
          return;
        }
        if (this.isTransformed) {
          this.performTransformationSpell();
          return;
        }
        if (this.castCooldown > 0 || this.isDashing || this.isAttacking || this.isSpecialActive) return;
        if (this.qi < 75) {
          floatingTexts.push(new FloatingText(this.x, this.y - 40, uiText('真气不足 (施法需 75 点真气)!', 'Not enough Qi (75 required)!'), '#f87171'));
          return;
        }
        this.qi -= 75;
        this.castCooldown = 1.0;

        sound.playJadeChime();

        const worldMouseX = gameState.mouse.x - viewWidth / 2 + this.x;
        const worldMouseY = gameState.mouse.y - viewHeight / 2 + this.y;

        const dy = worldMouseY - this.y;
        const dx = worldMouseX - this.x;
        if (Math.abs(dy) > Math.abs(dx)) {
          this.direction = dy < 0 ? 'up' : 'down';
          this.facing = 1;
        } else {
          this.direction = dx < 0 ? 'left' : 'right';
          this.facing = dx < 0 ? -1 : 1;
        }

        this.isCastingSpell = true;
        this.castSpellDuration = 0.55;
        this.castSpellMaxDuration = 0.55;

        const fxColor = this.boons.cast && GODS[this.boons.cast.godKey] ? GODS[this.boons.cast.godKey].color : '#facc15';

        const castBoonId = this.boons.cast?.id || 'hair_clone_base';
        const castPulseIntervals = {
          luban_divine_gear: 0.28,
          erlang_ring: 0.34,
          guanyin_ring: 0.25,
          nezha_ring: 0.42,
          laojun_ring: 0.30,
          aoguang_ring: 0.20
        };
        this.castActive = {
          boonId: castBoonId,
          x: worldMouseX,
          y: worldMouseY,
          radius: 190,
          duration: 6.0,
          tickTimer: 0,
          pulseInterval: castPulseIntervals[castBoonId] || 0.25,
          angle: 0,
          color: fxColor
        };

        // Ground Runic Bagua Summoning Array
        fxList.push(new HadesMagicCircleAOEFX(worldMouseX, worldMouseY, 190, 6.0, fxColor));

        for (let i = 0; i < 8; i++) {
          const spawnDelay = i * 0.04;
          setTimeout(() => {
            fxList.push(new GlowingHairTrailFX(this.x, this.y - 15, worldMouseX + (Math.random()*120 - 60), worldMouseY + (Math.random()*120 - 60), fxColor));
          }, spawnDelay * 1000);
        }

        const cloneCount = 7;
        for (let i = 0; i < cloneCount; i++) {
          const ang = (i / cloneCount) * Math.PI * 2 + Math.random() * 0.4;
          const spawnR = 30 + Math.random() * 110;
          const cloneX = worldMouseX + Math.cos(ang) * spawnR;
          const cloneY = worldMouseY + Math.sin(ang) * spawnR;
          setTimeout(() => {
            monkeyClones.push(new HouZhiHouShunClone(cloneX, cloneY, worldMouseX, worldMouseY));
            fxList.push(new RadialSparksFX(cloneX, cloneY, 6, '#facc15', 30));
          }, 180 + i * 40);
        }

        floatingTexts.push(new FloatingText(this.x, this.y - 50, uiText('身外身法 · 吹毛成兵!', 'Hair-Clone Art · Pluck Hair into Soldiers!'), '#facc15'));
      }

      triggerCastTick() {
        if (!this.castActive) return;
        const boonId = this.castActive.boonId || this.boons.cast?.id;
        const rank = this.boons.cast?.level || 1;
        const power = this.metaDamageMultiplier || 1;
        const targets = enemies.filter(enemy => enemy.alive && !enemy.isAlly &&
          Math.hypot(enemy.x - this.castActive.x, enemy.y - this.castActive.y) <= this.castActive.radius + enemy.radius);

        if (boonId === 'guanyin_ring') {
          this.hp = Math.min(this.maxHp, this.hp + 2 * (1 + 0.2 * (rank - 1)));
          targets.forEach(enemy => enemy.applySlow(0.50, 0.45));
          if (Math.floor(this.castActive.duration * 4) % 4 === 0) fxList.push(new Shockwave(this.castActive.x, this.castActive.y, 86, '#34d399'));
          return;
        }

        if (boonId === 'nezha_ring') {
          const chained = targets.sort((a, b) => Math.hypot(a.x - this.castActive.x, a.y - this.castActive.y) - Math.hypot(b.x - this.castActive.x, b.y - this.castActive.y)).slice(0, Math.min(6, 3 + rank));
          chained.forEach((enemy, index) => {
            enemy.takeDamage(35 * (1 + 0.25 * (rank - 1)) * power, false, true);
            const from = index === 0 ? this.castActive : chained[index - 1];
            fxList.push(new GlowingHairTrailFX(from.x, from.y, enemy.x, enemy.y, '#f97316'));
          });
          return;
        }

        if (boonId === 'luban_divine_gear') {
          targets.forEach(enemy => enemy.takeDamage(32 * (1 + 0.25 * (rank - 1)) * power, false, true));
          projectiles.filter(projectile => projectile.alive && projectile.isEnemy && Math.hypot(projectile.x - this.castActive.x, projectile.y - this.castActive.y) <= this.castActive.radius + projectile.radius)
            .forEach(projectile => {
              projectile.alive = false;
              projectiles.push(new Projectile(projectile.x, projectile.y, -projectile.vx * 1.15, -projectile.vy * 1.15, Math.max(35, projectile.dmg * 1.25), '#fbbf24', false));
              fxList.push(new RadialSparksFX(projectile.x, projectile.y, 6, '#fbbf24', 28));
            });
          return;
        }

        if (boonId === 'aoguang_ring') {
          targets.forEach(enemy => {
            const dx = this.castActive.x - enemy.x;
            const dy = this.castActive.y - enemy.y;
            const dist = Math.max(1, Math.hypot(dx, dy));
            enemy.x += dx / dist * 14;
            enemy.y += dy / dist * 14;
            enemy.takeDamage(12 * (1 + 0.25 * (rank - 1)) * power, false, false);
            enemy.applySlow(0.64, 0.35);
          });
          return;
        }

        targets.forEach(enemy => {
          if (!enemy.alive || enemy.isAlly) return;
            if (this.castActive.kind === 'erlang_judgment') {
              enemy.takeDamage(42 * (this.castActive.damageMultiplier || 1) * (this.metaDamageMultiplier || 1) * (this.isManifested ? 1.2 + (this.erlangSkillEffects?.manifestDamage || 0) : 1), false, true);
              enemy.judgmentMarkTimer = 4;
              enemy.applySlow(0.35, 0.8);
              fxList.push(new AnimatedLightningStrike(enemy.x, enemy.y));
              return;
            }
            let dmg = boonId === 'laojun_ring' ? 40 : (boonId === 'erlang_ring' ? 30 : 28);
            dmg *= 1 + 0.30 * Math.max(0, rank - 1);
            dmg *= power;
            enemy.takeDamage(dmg, false);
            if (boonId === 'laojun_ring') enemy.applyBurn(24 * rank * power, 0.7);
            else enemy.applySlow(0.5, 0.4);
        });
      }

      performDash() {
        const freeRocDash = this.hasActiveFormSkill('roc_supreme');
        if (this.isDashing || (this.dashCharges <= 0 && !freeRocDash) || this.isCastingSpell || this.isAttacking || this.isSpecialActive) return;
        if (!freeRocDash) this.dashCharges--;
        this.isDashing = true;
        this.dashMaxDuration = this.isTransformed && this.activeTransformationForm === 'roc' ? 0.20 : 0.26;
        this.dashDuration = this.dashMaxDuration;
        if (this.alignmentDashBarrierMax > 0) {
          this.alignmentBarrier = Math.max(this.alignmentBarrier || 0, this.alignmentDashBarrierMax);
          fxList.push(new Shockwave(this.x, this.y, 64, getAlignmentPalette().secondary));
        }
        if ((this.alignmentEffects?.dashDamage || 0) > 0) this.alignmentDashEmpowered = true;
        sound.playDash();

        let moveX = 0;
        let moveY = 0;
        if (gameState.keys['w'] || gameState.keys['arrowup']) moveY -= 1;
        if (gameState.keys['s'] || gameState.keys['arrowdown']) moveY += 1;
        if (gameState.keys['a'] || gameState.keys['arrowleft']) moveX -= 1;
        if (gameState.keys['d'] || gameState.keys['arrowright']) moveX += 1;

        if (moveX === 0 && moveY === 0) {
          const worldMouseX = gameState.mouse.x - viewWidth / 2 + this.x;
          const worldMouseY = gameState.mouse.y - viewHeight / 2 + this.y;
          const ang = Math.atan2(worldMouseY - this.y, worldMouseX - this.x);
          moveX = Math.cos(ang);
          moveY = Math.sin(ang);
        } else {
          const l = Math.hypot(moveX, moveY);
          moveX /= l;
          moveY /= l;
        }

        let dashDistance = this.isTransformed && this.activeTransformationForm === 'roc' ? 220 : 154;
        dashDistance *= 1 + this.getActiveFormSkillRank('tiger_pounce') * 0.15;
        dashDistance *= 1 + this.getActiveFormSkillRank('roc_dash') * 0.30;
        this.dashStartX = this.x;
        this.dashStartY = this.y;
        this.dashTargetX = Math.max(-1160, Math.min(1160, this.x + moveX * dashDistance));
        this.dashTargetY = Math.max(-860, Math.min(860, this.y + moveY * dashDistance));
        this.vx = moveX * (dashDistance / this.dashMaxDuration);
        this.vy = moveY * (dashDistance / this.dashMaxDuration);

        if (this.isTransformed) {
          const dashAngle = Math.atan2(this.dashTargetY - this.dashStartY, this.dashTargetX - this.dashStartX);
          if (this.activeTransformationForm === 'dragon') {
            const rank = this.getActiveFormSkillRank('dragon_soar');
            if (rank) {
              this.invulnTimer = Math.max(this.invulnTimer, 0.4 + rank * 0.05);
              fxList.push(new ExtendedStaffBeam(this.dashStartX, this.dashStartY, dashAngle, dashDistance, '#38bdf8'));
              this.cueFormSkill('dragon_soar', this.x, this.y, 0.72);
            }
          } else if (this.activeTransformationForm === 'tiger') {
            const rank = this.getActiveFormSkillRank('tiger_pounce');
            if (rank) {
              enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - this.dashTargetX, enemy.y - this.dashTargetY) <= 105 + enemy.radius)
                .forEach(enemy => { enemy.takeDamage((32 + rank * 18) * (this.metaDamageMultiplier || 1), false, true); enemy.applyBurn(20 + rank * 8, 1.5); });
              this.cueFormSkill('tiger_pounce', this.dashTargetX, this.dashTargetY, 0.72);
            }
          } else if (this.activeTransformationForm === 'roc') {
            const dashRank = this.getActiveFormSkillRank('roc_dash');
            const sonicRank = this.getActiveFormSkillRank('roc_sonic');
            if (dashRank || sonicRank) {
              const dxPath = this.dashTargetX - this.dashStartX;
              const dyPath = this.dashTargetY - this.dashStartY;
              const lengthSq = Math.max(1, dxPath * dxPath + dyPath * dyPath);
              enemies.filter(enemy => enemy.alive && !enemy.isAlly).forEach(enemy => {
                const t = Math.max(0, Math.min(1, ((enemy.x - this.dashStartX) * dxPath + (enemy.y - this.dashStartY) * dyPath) / lengthSq));
                const hx = this.dashStartX + dxPath * t, hy = this.dashStartY + dyPath * t;
                if (Math.hypot(enemy.x - hx, enemy.y - hy) <= enemy.radius + 48) enemy.takeDamage((dashRank * 22 + sonicRank * 80) * (this.metaDamageMultiplier || 1), false, true);
              });
              fxList.push(new ExtendedStaffBeam(this.dashStartX, this.dashStartY, dashAngle, dashDistance, '#fde047'));
              if (sonicRank) this.cueFormSkill('roc_sonic', this.dashTargetX, this.dashTargetY, 0.78);
            }
            if (freeRocDash) this.cueFormSkill('roc_supreme', this.x, this.y, 0.54);
          }
        }

        if (gameState.playableHero === 'erlang') {
          const dashDx = this.dashTargetX - this.dashStartX;
          const dashDy = this.dashTargetY - this.dashStartY;
          const dashLengthSq = Math.max(1, dashDx * dashDx + dashDy * dashDy);
          enemies.forEach(enemy => {
            if (!enemy.alive || enemy.isAlly) return;
            const t = Math.max(0, Math.min(1, ((enemy.x - this.dashStartX) * dashDx + (enemy.y - this.dashStartY) * dashDy) / dashLengthSq));
            const hitX = this.dashStartX + dashDx * t;
            const hitY = this.dashStartY + dashDy * t;
            if (Math.hypot(enemy.x - hitX, enemy.y - hitY) <= enemy.radius + 38) {
              enemy.takeDamage(28 * (1 + (this.erlangSkillEffects?.dashDamage || 0)) * (this.metaDamageMultiplier || 1), false, false);
              fxList.push(new AnimatedLightningStrike(enemy.x, enemy.y));
            }
          });
          fxList.push(new StaffMotionWaveFX(this.dashStartX, this.dashStartY, Math.atan2(dashDy, dashDx), dashDistance, '#60a5fa'));
        }

        if (this.boons.dash) {
          const lvl = this.boons.dash.level || 1;
          if (this.boons.dash.id === 'nezha_dash') {
            fxList.push(new AnimatedFireExplosion(this.x, this.y, 80));
          } else if (this.boons.dash.id === 'erlang_dash') {
            fxList.push(new AnimatedLightningStrike(this.x, this.y));
            const damage = (40 + 12 * (lvl - 1)) * (this.metaDamageMultiplier || 1);
            enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - this.x, enemy.y - this.y) <= 105 + enemy.radius)
              .slice(0, 6).forEach(enemy => enemy.takeDamage(damage, false, true));
          } else if (this.boons.dash.id === 'guanyin_dash') {
            this.guanyinBarrier = 30 + 12 * (lvl - 1);
            this.guanyinBarrierTimer = 2.5 + 0.25 * (lvl - 1);
            fxList.push(new HadesMagicCircleAOEFX(this.x, this.y, 62, this.guanyinBarrierTimer, '#34d399'));
            floatingTexts.push(new FloatingText(this.x, this.y - 42,
              uiText(`杨柳玉露盾 · ${this.guanyinBarrier}`, `Willow-Dew Shield · ${this.guanyinBarrier}`), '#6ee7b7'));
          }
        }
      }

      triggerAwakening() {
        if (this.awakenGauge < this.maxAwakenGauge || this.isAwakened) return;
        this.isAwakened = true;
        this.awakenDuration = gameState.playableHero === 'erlang' ? 8.0 : 10.0;
        if (gameState.playableHero === 'erlang') {
          this.houndCooldown = 0;
          enemies.filter(enemy => enemy.alive && !enemy.isAlly && enemy.judgmentMarkTimer > 0).slice(0, 8)
            .forEach(enemy => { enemy.takeDamage(90 * (this.metaDamageMultiplier || 1), true, true); enemy.judgmentMarkTimer = 0; fxList.push(new AnimatedLightningStrike(enemy.x, enemy.y)); });
        }
        sound.playAwaken();
        createScreenShake(15);
        fxList.push(new Shockwave(this.x, this.y, 260, '#facc15'));
      }

      takeDamage(amount) {
        if (isGameplayPaused() || this.isDashing || (this.isAwakened && gameState.playableHero !== 'erlang') || this.invulnTimer > 0) return;
        // NG+ enemy contact, projectile, boss and hazard damage all converge
        // here. Scale once at the player boundary so no attack family silently
        // keeps the old 1.2x modifier or accidentally receives the bonus twice.
        if (gameState.isNewGamePlus) amount *= NG_PLUS_ENEMY_DAMAGE_MULTIPLIER;
        if (gameState.playableHero === 'erlang' && (this.isAwakened || this.isManifested)) amount *= 0.75;
        amount *= 1 - Math.max(0, this.alignmentDamageReduction || 0);
        if (this.hp <= this.maxHp * .25) amount *= 1 - Math.max(0, this.alignmentLowHpReduction || 0);
        this.timeSinceDamage = 0;

        if (this.hasBoon('buddha_equanimity') && this.qi > this.maxQi * 0.5) {
          const level = this.getBoonLevel('buddha_equanimity');
          amount *= 1 - Math.min(0.24, 0.15 + 0.03 * (level - 1));
          fxList.push(new Shockwave(this.x, this.y, 52, '#fde68a'));
        }

        if (this.isTransformed && this.activeTransformationForm === 'ape') {
          amount *= 0.70; // heavy-form super armor
          amount *= 1 - Math.min(0.45, this.getActiveFormSkillRank('ape_titan') * 0.07 + this.getActiveFormSkillRank('ape_armor') * 0.04);
        } else if (this.isTransformed && this.activeTransformationForm === 'tortoise') {
          amount *= 0.48;
          const shieldRank = this.getActiveFormSkillRank('tort_shield');
          const perHitCap = this.maxHp * (shieldRank > 0 ? Math.max(0.04, 0.09 - shieldRank * 0.01) : 0.12);
          amount = Math.min(amount, perHitCap);
          fxList.push(new Shockwave(this.x, this.y, 58, '#10b981'));
          amount *= 1 - Math.min(0.65, this.getActiveFormSkillRank('tort_cover_sun') * 0.10);
        } else if (this.isTransformed && this.activeTransformationForm === 'tiger') {
          amount *= 1 - Math.min(0.80, this.getActiveFormSkillRank('tiger_bite') * 0.16);
        }

        if (this.isTransformed && this.activeTransformationForm === 'tortoise') {
          const flowRank = this.getActiveFormSkillRank('tort_flow');
          if (flowRank && Math.random() < Math.min(0.85, 0.17 * flowRank)) {
            this.qi = Math.min(this.maxQi, this.qi + amount * (0.35 + flowRank * 0.10));
            amount *= 0.35;
            this.cueFormSkill('tort_flow', this.x, this.y, 0.62);
          }
          const guardRank = this.getActiveFormSkillRank('tort_guard');
          if (guardRank && !this.formGuardTriggered && this.hp <= this.maxHp * 0.30) {
            this.formGuardTriggered = true;
            this.formBarrier += 90 + guardRank * 60;
            this.formBarrierMax = Math.max(this.formBarrierMax, this.formBarrier);
            this.cueFormSkill('tort_guard', this.x, this.y, 0.88);
          }
        }

        if ((this.alignmentBarrier || 0) > 0) {
          const warded = Math.min(this.alignmentBarrier, amount);
          this.alignmentBarrier -= warded;
          amount -= warded;
          fxList.push(new Shockwave(this.x, this.y, 50, getAlignmentPalette().secondary));
          if (amount <= 0) return;
        }

        if (this.formBarrier > 0) {
          const warded = Math.min(this.formBarrier, amount);
          this.formBarrier -= warded;
          amount -= warded;
          const profile = FORM_COMBAT_PROFILES[this.activeTransformationForm] || FORM_COMBAT_PROFILES.dragon;
          fxList.push(new Shockwave(this.x, this.y, 66, profile.color));
          if (amount <= 0) { updateHUD(); return; }
        }

        if (this.guanyinBarrier > 0 && this.guanyinBarrierTimer > 0) {
          const warded = Math.min(this.guanyinBarrier, amount);
          this.guanyinBarrier -= warded;
          amount -= warded;
          fxList.push(new Shockwave(this.x, this.y, 58, '#34d399'));
          if (amount <= 0) { updateHUD(); return; }
        }

        if (this.bullArmor > 0) {
          const absorbed = Math.min(this.bullArmor, amount);
          this.bullArmor -= absorbed;
          amount -= absorbed;
          fxList.push(new RadialSparksFX(this.x, this.y, 7, '#fb923c', 32));
          if (amount <= 0) { updateHUD(); return; }
        }

        if (this.masterworkArmor > 0) {
          const absorbed = Math.min(this.masterworkArmor, amount);
          this.masterworkArmor -= absorbed;
          amount -= absorbed;
          fxList.push(new RadialSparksFX(this.x, this.y, 5, '#fbbf24', 24));
          if (amount <= 0) { updateHUD(); return; }
        }

        if (this.armor > 0) {
          const absorbed = Math.min(this.armor, amount);
          this.armor -= absorbed;
          amount -= absorbed;
          if (amount <= 0) { updateHUD(); return; }
        }

        this.hp = Math.max(0, this.hp - amount);
        this.invulnTimer = 0.55;
        createScreenShake(5);

        floatingTexts.push(new FloatingText(this.x, this.y - 30, `-${Math.round(amount)}`, '#ef4444'));

        if (this.isTransformed && this.activeTransformationForm === 'tortoise') {
          const spikeRank = this.getActiveFormSkillRank('tort_spike');
          const supremeRank = this.getActiveFormSkillRank('tort_supreme');
          if (spikeRank || supremeRank) {
            const reflected = amount * Math.min(2.0, spikeRank * 0.28 + supremeRank * 0.40);
            enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - this.x, enemy.y - this.y) <= 150 + enemy.radius)
              .slice(0, 5).forEach(enemy => enemy.takeDamage(reflected, false, true));
            if (reflected > 0) this.cueFormSkill(supremeRank ? 'tort_supreme' : 'tort_spike', this.x, this.y, 0.68);
          }
        }

        if (this.hp <= 0) {
          if (this.isTransformed && this.activeTransformationForm === 'dragon' && this.hasActiveFormSkill('dragon_water_walk') && !this.formReviveUsed) {
            this.formReviveUsed = true;
            this.hp = Math.max(1, this.maxHp * 0.28);
            this.formBarrier = 80 + this.getActiveFormSkillRank('dragon_water_walk') * 45;
            this.invulnTimer = 1.5;
            fxList.push(new TransformationSpellFX('dragon', this.x, this.y, 155, 1.1));
            this.cueFormSkill('dragon_water_walk', this.x, this.y, 1.0);
            updateHUD();
            return;
          }
          if (this.isTransformed && this.activeTransformationForm === 'tortoise' && (this.formRevivesRemaining > 0 || (this.hasActiveFormSkill('tort_supreme') && !this.formReviveUsed))) {
            if (this.formRevivesRemaining > 0) this.formRevivesRemaining--;
            else this.formReviveUsed = true;
            this.hp = this.hasActiveFormSkill('tort_renew_head') ? this.maxHp : Math.max(1, this.maxHp * 0.45);
            this.qi = this.hasActiveFormSkill('tort_renew_head') ? this.maxQi : this.qi;
            this.invulnTimer = this.hasActiveFormSkill('tort_renew_head') ? 3.0 : 1.5;
            this.formBarrier = 90 + this.getActiveFormSkillRank('tort_shell') * 30;
            fxList.push(new TransformationSpellFX('tortoise', this.x, this.y, 175, 1.2));
            this.cueFormSkill(this.hasActiveFormSkill('tort_renew_head') ? 'tort_renew_head' : (this.hasActiveFormSkill('tort_supreme') ? 'tort_supreme' : 'tort_immortal'), this.x, this.y, 1.0);
            updateHUD();
            return;
          }
          if (this.lives > 0) {
            this.lives--;
            const nirvanaRank = this.hasBoon('guanyin_nirvana') ? this.getBoonLevel('guanyin_nirvana') : 0;
            const revivalRatio = nirvanaRank ? Math.min(0.90, 0.70 + 0.05 * (nirvanaRank - 1)) : 0.60;
            this.hp = Math.round(this.maxHp * revivalRatio);
            if (nirvanaRank) this.qi = this.maxQi;
            this.invulnTimer = 1.8;
            sound.playJadeChime();
            createScreenShake(10);
            fxList.push(new Shockwave(this.x, this.y, 200, '#4ade80'));
            floatingTexts.push(new FloatingText(this.x, this.y - 45, uiText('金身复活 · 重振神威!', 'Golden Body Revived!'), '#4ade80'));
          } else {
            this.hp = 0;
            handleGameOver(false);
          }
        }
        updateHUD();
      }

      drawAlignmentAura(ctx, foreground = false) {
        if (gameState.playableHero !== 'wukong') return;
        const palette = getAlignmentPalette();
        // Evil forms carry their identity in the authored armor and raster
        // strike frames. Do not redraw the old purple ellipses/tendrils over
        // the repaired avatar.
        if (palette.path === 'evil') return;
        const neutralProgress = Math.min(1, (this.neutralInvestedRanks || 0) / 120);
        const intensity = palette.path === 'neutral' ? Math.max(.12, neutralProgress) : Math.min(1, Math.abs(alignmentScore) / 60);
        ctx.save();
        const pulse = .5 + .5 * Math.sin(this.animClock * 4.5);
        if (!foreground) {
          ctx.globalAlpha = .18 + intensity * .20;
          ctx.strokeStyle = palette.secondary;
          ctx.shadowColor = palette.primary;
          ctx.shadowBlur = 10 + intensity * 12;
          ctx.lineWidth = 2 + intensity * 2;
          ctx.beginPath();
          ctx.ellipse(0, 38, 38 + pulse * 5, 14 + pulse * 2, 0, 0, Math.PI * 2);
          ctx.stroke();
          if (palette.path === 'good') {
            for (let i = 0; i < 3; i++) {
              const a = this.animClock * .8 + i * Math.PI * 2 / 3;
              ctx.fillStyle = i === 0 ? '#ffffff' : palette.secondary;
              ctx.beginPath(); ctx.arc(Math.cos(a) * 41, 12 + Math.sin(a) * 18, 2.5 + pulse, 0, Math.PI * 2); ctx.fill();
            }
          } else if (palette.path === 'evil') {
            ctx.globalAlpha = .14 + intensity * .18;
            for (let i = 0; i < 4; i++) {
              const a = this.animClock * 1.4 + i * Math.PI / 2;
              ctx.strokeStyle = i % 2 ? '#ef4444' : '#a855f7';
              ctx.beginPath();
              ctx.moveTo(Math.cos(a) * 28, 24 + Math.sin(a) * 8);
              ctx.quadraticCurveTo(Math.cos(a + .7) * 48, -2 - pulse * 9, Math.cos(a + 1.2) * 35, -28 - pulse * 10);
              ctx.stroke();
            }
          } else {
            ctx.globalAlpha = .20 + intensity * .24;
            ctx.lineWidth = 2.2 + intensity * 1.8;
            for (let i = 0; i < 2; i++) {
              const direction = i ? -1 : 1;
              const start = this.animClock * direction * .9 + i * Math.PI;
              ctx.strokeStyle = i ? '#8b5cf6' : '#facc15';
              ctx.shadowColor = ctx.strokeStyle;
              ctx.beginPath();
              ctx.arc(0, 1, 31 + i * 5 + pulse * 2, start, start + Math.PI * .78);
              ctx.stroke();
              ctx.fillStyle = i ? '#c4b5fd' : '#fff7ae';
              ctx.beginPath();
              ctx.arc(Math.cos(start) * (31 + i * 5), 1 + Math.sin(start) * (31 + i * 5), 2.4 + intensity, 0, Math.PI * 2);
              ctx.fill();
            }
          }
        } else if (palette.path === 'neutral') {
          ctx.globalAlpha = .32 + intensity * .26;
          ctx.shadowBlur = 10 + intensity * 10;
          for (let i = 0; i < 2; i++) {
            const a = this.animClock * (i ? -1.2 : 1.2) + i * Math.PI;
            ctx.fillStyle = i ? '#a78bfa' : '#fde047';
            ctx.shadowColor = ctx.fillStyle;
            ctx.beginPath();
            ctx.arc(Math.cos(a) * 24, -16 + Math.sin(a) * 9, 2.2 + pulse, 0, Math.PI * 2);
            ctx.fill();
          }
        }
        ctx.restore();
      }

      drawBoonAuras(ctx) {
        const pulse = 0.5 + 0.5 * Math.sin(this.animClock * 5);
        ctx.save();

        if (this.hasBoon('bull_ironhide') && this.bullArmorMax > 0) {
          const armorRatio = Math.max(0, Math.min(1, this.bullArmor / this.bullArmorMax));
          ctx.globalAlpha = 0.34 + armorRatio * 0.48;
          ctx.strokeStyle = armorRatio > 0 ? '#fb923c' : '#7c2d12';
          ctx.fillStyle = 'rgba(124,45,18,.24)';
          ctx.shadowColor = '#ea580c';
          ctx.shadowBlur = 10 + armorRatio * 12;
          ctx.lineWidth = 4;
          ctx.beginPath();
          ctx.arc(0, 4, 42 + pulse * 2, Math.PI * 0.10, Math.PI * 0.90);
          ctx.arc(0, 4, 42 + pulse * 2, Math.PI * 1.10, Math.PI * 1.90);
          ctx.stroke();
          // Horned shoulder plates make this read as armor rather than a generic shield.
          [-1, 1].forEach(side => {
            ctx.beginPath();
            ctx.moveTo(side * 24, -10);
            ctx.quadraticCurveTo(side * 46, -24, side * 50, -42);
            ctx.quadraticCurveTo(side * 36, -30, side * 30, -16);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
          });
          ctx.shadowBlur = 0;
          ctx.globalAlpha = 0.92;
          ctx.font = getCanvasFont(10, 900);
          ctx.textAlign = 'center';
          ctx.fillStyle = '#ffedd5';
          ctx.fillText(`🛡 ${Math.ceil(this.bullArmor)}/${this.bullArmorMax}`, 0, 64);
        }

        if (this.guanyinBarrier > 0 && this.guanyinBarrierTimer > 0) {
          ctx.globalAlpha = 0.50 + pulse * 0.18;
          ctx.strokeStyle = '#6ee7b7';
          ctx.shadowColor = '#34d399';
          ctx.shadowBlur = 16;
          ctx.lineWidth = 3;
          for (let i = 0; i < 8; i++) {
            const a = i * Math.PI / 4 + this.animClock * 0.35;
            ctx.beginPath();
            ctx.ellipse(Math.cos(a) * 38, 4 + Math.sin(a) * 22, 8, 3, a, 0, Math.PI * 2);
            ctx.stroke();
          }
        }

        if (this.hasBoon('luban_masterwork')) {
          const a = this.animClock * 1.8;
          ctx.globalAlpha = 0.70;
          ctx.strokeStyle = '#fbbf24';
          ctx.lineWidth = 2;
          ctx.shadowColor = '#f59e0b'; ctx.shadowBlur = 8;
          for (let i = 0; i < 8; i++) {
            const ga = a + i * Math.PI / 4;
            const x = Math.cos(ga) * 46, y = 7 + Math.sin(ga) * 18;
            ctx.strokeRect(x - 3, y - 3, 6, 6);
          }
        }

        if (this.hasBoon('erlang_truesight')) {
          ctx.globalAlpha = 0.72 + pulse * 0.22;
          ctx.strokeStyle = '#fde68a'; ctx.fillStyle = '#60a5fa';
          ctx.shadowColor = '#60a5fa'; ctx.shadowBlur = 9;
          ctx.beginPath(); ctx.ellipse(0, -54, 10, 4, 0, 0, Math.PI * 2); ctx.stroke();
          ctx.beginPath(); ctx.arc(0, -54, 2.2, 0, Math.PI * 2); ctx.fill();
        }

        if (this.hasBoon('guanyin_nirvana')) {
          ctx.globalAlpha = 0.25 + pulse * 0.12;
          ctx.strokeStyle = '#86efac'; ctx.lineWidth = 2;
          for (let i = 0; i < 6; i++) {
            const a = i * Math.PI / 3;
            ctx.beginPath(); ctx.ellipse(Math.cos(a) * 18, 39 + Math.sin(a) * 7, 14, 5, a, 0, Math.PI * 2); ctx.stroke();
          }
        }

        if (this.hasBoon('laojun_elixir')) {
          const a = -this.animClock * 1.2;
          ctx.globalAlpha = 0.86;
          ctx.fillStyle = '#fde047'; ctx.shadowColor = '#fb923c'; ctx.shadowBlur = 10;
          ctx.beginPath(); ctx.arc(Math.cos(a) * 36, -12 + Math.sin(a) * 15, 4, 0, Math.PI * 2); ctx.fill();
        }

        if (this.hasBoon('buddha_equanimity') && this.qi > this.maxQi * 0.5) {
          ctx.globalAlpha = 0.20 + pulse * 0.12;
          ctx.strokeStyle = '#fde68a'; ctx.lineWidth = 3;
          ctx.shadowColor = '#facc15'; ctx.shadowBlur = 12;
          ctx.beginPath(); ctx.arc(0, 2, 48, 0, Math.PI * 2); ctx.stroke();
          ctx.beginPath(); ctx.arc(0, 2, 34, 0, Math.PI * 2); ctx.stroke();
        }
        ctx.restore();
      }

      drawTransformationSkillAuras(ctx) {
        if (!this.isTransformed) return;
        const profile = FORM_COMBAT_PROFILES[this.activeTransformationForm] || FORM_COMBAT_PROFILES.dragon;
        const pulse = 0.5 + Math.sin(this.animClock * 5) * 0.5;
        ctx.save();
        if (this.formBarrier > 0) {
          const ratio = this.formBarrierMax > 0 ? Math.min(1, this.formBarrier / this.formBarrierMax) : 1;
          ctx.globalAlpha = 0.18 + ratio * 0.28;
          ctx.strokeStyle = profile.color; ctx.shadowColor = profile.color; ctx.shadowBlur = 14; ctx.lineWidth = 3;
          ctx.beginPath(); ctx.ellipse(0, 16, 58 + pulse * 4, 34 + pulse * 3, 0, 0, Math.PI * 2); ctx.stroke();
        }
        if (this.activeTransformationForm === 'dragon' && (this.hasActiveFormSkill('dragon_rain') || this.hasActiveFormSkill('dragon_storm'))) {
          ctx.globalAlpha = 0.45; ctx.strokeStyle = '#7dd3fc'; ctx.lineWidth = 2;
          for (let i=0;i<6;i++){const x=((i*29+this.animClock*65)%120)-60;const y=((i*37+this.animClock*90)%100)-65;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x-5,y+14);ctx.stroke();}
        } else if (this.activeTransformationForm === 'tiger' && this.formFrenzy > 0) {
          ctx.globalAlpha = Math.min(.62,.18+this.formFrenzy*2); ctx.strokeStyle='#fb7185';ctx.lineWidth=3;
          for(let i=0;i<4;i++){const y=-42+i*24;ctx.beginPath();ctx.moveTo(-58-pulse*8,y);ctx.lineTo(-24,y+7);ctx.stroke();}
        } else if (this.activeTransformationForm === 'roc' && (this.hasActiveFormSkill('roc_sky_scout') || this.hasActiveFormSkill('roc_supreme'))) {
          ctx.globalAlpha=.42+pulse*.18;ctx.strokeStyle='#fde047';ctx.lineWidth=2;
          for(let i=0;i<5;i++){const a=this.animClock*1.8+i*Math.PI*2/5;ctx.save();ctx.translate(Math.cos(a)*58,Math.sin(a)*26);ctx.rotate(a);ctx.beginPath();ctx.ellipse(0,0,10,3,0,0,Math.PI*2);ctx.stroke();ctx.restore();}
        } else if (this.activeTransformationForm === 'ape' && (this.hasActiveFormSkill('ape_titan') || this.hasActiveFormSkill('ape_overlord'))) {
          ctx.globalAlpha=.30+pulse*.14;ctx.strokeStyle='#fb923c';ctx.lineWidth=5;ctx.shadowColor='#ea580c';ctx.shadowBlur=10;
          ctx.beginPath();ctx.arc(0,12,62,Math.PI*.12,Math.PI*.88);ctx.stroke();ctx.beginPath();ctx.arc(0,12,62,Math.PI*1.12,Math.PI*1.88);ctx.stroke();
        } else if (this.activeTransformationForm === 'tortoise' && this.hasActiveFormSkill('tort_whirlpool')) {
          ctx.globalAlpha=.48;ctx.strokeStyle='#5eead4';ctx.lineWidth=3;
          for(let i=0;i<6;i++){const a=-this.animClock*2.4+i*Math.PI/3;ctx.save();ctx.translate(Math.cos(a)*68,18+Math.sin(a)*28);ctx.rotate(a+.6);ctx.beginPath();ctx.moveTo(-12,0);ctx.quadraticCurveTo(0,-7,12,0);ctx.quadraticCurveTo(0,7,-12,0);ctx.stroke();ctx.restore();}
        }
        ctx.restore();
      }

      drawRuyiContactBody(ctx, profile, progress) {
        const image = loadedImages['wukong_ruyi_contact_attacks'];
        if (!image || !image.complete || !image.naturalWidth || !profile) return false;
        // Side-authored anatomy is used only inside a narrow horizontal sector.
        // Up/down/diagonal attacks keep the canonical directional hero body and
        // receive the separately rotatable generated weapon path below.
        const horizontalError = Math.min(ruyiAngleDifference(this.attackAngle, 0), ruyiAngleDifference(this.attackAngle, Math.PI));
        if (horizontalError > Math.PI / 8) return false;
        const cell = 384;
        const frame = Math.min(RUYI_CONTACT_FRAME_COUNT - 1, Math.floor(Math.max(0, Math.min(.999, progress)) * RUYI_CONTACT_FRAME_COUNT));
        const scale = .45 * (this.isAwakened ? 1.12 : (this.weaponStyle === 'titan' ? 1.06 : 1));
        ctx.save();
        if (Math.cos(this.attackAngle) < 0) ctx.scale(-1, 1);
        // Keep the generated Wukong pose but clip away its baked outer staff.
        // The separate generated weapon-path layer owns the exact hand-to-tip
        // geometry and prevents a doubled weapon when aim/reach changes.
        ctx.beginPath();
        ctx.rect(-82, -132, 164, 188);
        ctx.clip();
        ctx.shadowColor = this.getActiveGodColor();
        ctx.shadowBlur = 7;
        ctx.drawImage(
          image,
          frame * cell, profile.row * cell, cell, cell,
          -profile.bodyPivotX * scale, 44 - profile.bodyFootY * scale,
          cell * scale, cell * scale,
        );
        ctx.restore();
        return true;
      }

      getRuyiDirectionalBodyFrame() {
        return getRuyiDirectionalBodyFrameForAngle(this.attackAngle);
      }

      getRuyiBodyHandAnchor(progress, profile = this.activeRuyiContactProfile) {
        const baseScaleFactor = this.isAwakened ? 1.12 : (this.weaponStyle === 'titan' ? 1.06 : 1);
        return getRuyiTemporalHandAnchor(this.attackAngle, profile || RUYI_CONTACT_PROFILES.arc, progress, baseScaleFactor);
      }

      drawRuyiDirectionalBodyOnly(ctx, progress, profile = this.activeRuyiContactProfile) {
        const alignmentPath = getAlignmentCombatStage()?.path || 'neutral';
        const atlasKey = getRuyiTemporalAtlasKey(alignmentPath);
        const image = loadedImages[atlasKey];
        if (!image || !image.complete || !image.naturalWidth) return { x:0, y:-18 };
        const activeProfile = profile || RUYI_CONTACT_PROFILES.arc;
        const frame = getRuyiTemporalFrame(progress);
        const row = getRuyiTemporalBodyRow(activeProfile, this.attackAngle);
        const cell = 192;
        const scale = .90 * (this.isAwakened ? 1.12 : (this.weaponStyle === 'titan' ? 1.06 : 1));
        const anchor = this.getRuyiBodyHandAnchor(progress, activeProfile);
        ctx.save();
        ctx.shadowColor = alignmentPath === 'evil' ? '#7e22ce' : (alignmentPath === 'good' ? '#93c5fd' : this.getActiveGodColor());
        ctx.shadowBlur = alignmentPath === 'neutral' ? 7 : 11;
        ctx.drawImage(
          image,
          frame * cell, row * cell, cell, cell,
          -96 * scale, 44 - 160 * scale,
          cell * scale, cell * scale,
        );
        ctx.restore();
        return anchor;
      }

      drawRuyiContactWeaponPath(ctx, profile, progress, handAnchor = null) {
        const image = loadedImages['ruyi_contact_weapon_paths'];
        if (!image || !image.complete || !image.naturalWidth || !profile) return;
        const cell = 384;
        const frame = getRuyiTemporalFrame(progress);
        const reach = Math.max(1, this.activeAttackReach || profile.baseReach);
        const sourceSegment = getRuyiWeaponSourceSegment(profile, frame);
        const worldShaft = getRuyiWorldShaft(0, 0, this.attackAngle, profile, progress, reach, handAnchor || {x:0,y:-18});
        // Every source frame is independently normalized from its measured
        // hand-to-tip segment. This is what keeps all eight spin poses, impact
        // art, gameplay reach and upgrade scaling on the same endpoint.
        const scale = reach / sourceSegment.length;
        ctx.save();
        ctx.translate(worldShaft.originX, worldShaft.originY);
        ctx.rotate(worldShaft.angle - sourceSegment.angle);
        ctx.globalAlpha = .94;
        ctx.shadowColor = this.getActiveGodColor();
        ctx.shadowBlur = 6;
        ctx.drawImage(
          image,
          frame * cell, profile.row * cell, cell, cell,
          -sourceSegment.pivotX * scale, -sourceSegment.pivotY * scale,
          cell * scale, cell * scale,
        );
        ctx.restore();
      }

      drawDirectionalRuyiAttackBody(ctx, progress) {
        const image = loadedImages['hero'];
        if (!image || !image.complete || !image.naturalWidth) return false;
        const cell = 128;
        // Use Wukong's authored attack rows for non-horizontal aim. Locomotion
        // rows made him appear to run while a detached staff struck diagonally.
        const row = this.currentCombo === 1 ? 4 : 3;
        const frame = Math.min(6, Math.floor(Math.max(0, Math.min(.999, progress)) * 7));
        const scale = 1.10 * PACKED_VISUAL_SCALE_128;
        ctx.save();
        if (Math.cos(this.attackAngle) < 0) ctx.scale(-1, 1);
        ctx.drawImage(image, frame * cell, row * cell, cell, cell, -cell * scale / 2, 44 - 100 * scale, cell * scale, cell * scale);
        ctx.restore();
        return true;
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        this.drawAlignmentAura(ctx, false);
        this.drawBoonAuras(ctx);
        this.drawTransformationSkillAuras(ctx);

        this.dashTrail.forEach(t => {
          ctx.save();
          ctx.beginPath();
          ctx.arc(t.x - this.x, t.y - this.y, t.radius, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(255, 245, 200, ${t.alpha * 0.45})`;
          ctx.fill();
          ctx.restore();
        });

        if (this.castActive) {
          ctx.save();
          ctx.translate(this.castActive.x - this.x, this.castActive.y - this.y);
          ctx.rotate(this.castActive.angle);

          ctx.beginPath();
          ctx.arc(0, 0, this.castActive.radius, 0, Math.PI * 2);
          ctx.strokeStyle = this.castActive.color || 'rgba(168, 85, 247, 0.85)';
          ctx.lineWidth = 3;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(0, 0, this.castActive.radius * 0.6, 0, Math.PI * 2);
          ctx.strokeStyle = '#facc15';
          ctx.lineWidth = 2;
          ctx.stroke();

          const castId = this.castActive.boonId;
          ctx.save();
          ctx.rotate(-this.castActive.angle);
          ctx.shadowColor = this.castActive.color;
          ctx.shadowBlur = 10;
          if (castId === 'luban_divine_gear') {
            ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 4;
            [0.38, 0.70].forEach((scale, ringIndex) => {
              ctx.save(); ctx.rotate(this.castActive.angle * (ringIndex ? -1.8 : 2.4));
              const teeth = ringIndex ? 12 : 8;
              for (let i = 0; i < teeth; i++) {
                const a = i * Math.PI * 2 / teeth;
                const radius = this.castActive.radius * scale;
                ctx.strokeRect(Math.cos(a) * radius - 5, Math.sin(a) * radius - 5, 10, 10);
              }
              ctx.beginPath(); ctx.arc(0, 0, this.castActive.radius * scale, 0, Math.PI * 2); ctx.stroke();
              ctx.restore();
            });
          } else if (castId === 'erlang_ring') {
            ctx.strokeStyle = '#93c5fd'; ctx.fillStyle = 'rgba(96,165,250,.24)'; ctx.lineWidth = 5;
            ctx.beginPath(); ctx.ellipse(0, 0, 92, 38, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
            ctx.fillStyle = '#fde68a'; ctx.beginPath(); ctx.arc(0, 0, 15, 0, Math.PI * 2); ctx.fill();
          } else if (castId === 'guanyin_ring') {
            ctx.strokeStyle = '#6ee7b7'; ctx.fillStyle = 'rgba(52,211,153,.16)'; ctx.lineWidth = 3;
            for (let i = 0; i < 9; i++) {
              const a = i * Math.PI * 2 / 9;
              ctx.beginPath(); ctx.ellipse(Math.cos(a) * 82, Math.sin(a) * 82, 38, 13, a, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
            }
          } else if (castId === 'nezha_ring') {
            ctx.strokeStyle = '#fb923c'; ctx.lineWidth = 7;
            for (let i = 0; i < 3; i++) {
              const a = this.castActive.angle * 2 + i * Math.PI * 2 / 3;
              ctx.beginPath(); ctx.arc(Math.cos(a) * 92, Math.sin(a) * 52, 26, 0, Math.PI * 2); ctx.stroke();
            }
          } else if (castId === 'laojun_ring') {
            ctx.strokeStyle = '#fb7185'; ctx.fillStyle = 'rgba(249,115,22,.15)'; ctx.lineWidth = 4;
            ctx.fillRect(-58, -72, 116, 144); ctx.strokeRect(-58, -72, 116, 144);
            ctx.beginPath(); ctx.arc(0, -70, 46, Math.PI, 0); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(-68, 0); ctx.lineTo(68, 0); ctx.moveTo(0, -80); ctx.lineTo(0, 80); ctx.stroke();
          } else if (castId === 'aoguang_ring') {
            ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 5;
            for (let i = 0; i < 4; i++) {
              ctx.beginPath(); ctx.arc(0, 0, 35 + i * 30, this.castActive.angle * (1 + i * .2) + i, this.castActive.angle * (1 + i * .2) + i + Math.PI * 1.45); ctx.stroke();
            }
          }
          ctx.restore();

          ctx.restore();
        }

        const erlangImg = loadedImages['erlang_player_actions'];
        if (gameState.playableHero === 'erlang' && erlangImg && erlangImg.complete && erlangImg.naturalWidth > 0) {
          const cell = 240;
          const erlangComboImg = loadedImages['erlang_combo_actions'];
          const useErlangCombo = Boolean(this.isAttacking && this.activeComboMove && erlangComboImg && erlangComboImg.complete && erlangComboImg.naturalWidth > 0);
          const erlangSourceImg = useErlangCombo ? erlangComboImg : erlangImg;
          let row = 0;
          let frame = 0;
          const isMoving = Math.hypot(this.vx, this.vy) > 10;
          if (this.isManifested && this.manifestAnimDuration < 0.82) {
            row = 4;
            frame = Math.min(6, Math.floor(this.manifestAnimDuration / 0.82 * 7));
          } else if (this.isAttacking) {
            row = useErlangCombo ? Math.max(0, Math.min(4, this.activeComboMove.animRow ?? 0)) : 1;
            const progress = Math.max(0, Math.min(0.999, 1 - this.attackDuration / this.attackMaxDuration));
            frame = Math.min(6, Math.floor(progress * 7));
          } else if (this.isCastingSpell || this.isSpecialActive) {
            row = 2;
            const duration = this.isCastingSpell ? this.castSpellDuration : this.specialDuration;
            const maximum = this.isCastingSpell ? this.castSpellMaxDuration : this.specialMaxDuration;
            const progress = Math.max(0, Math.min(0.999, 1 - duration / Math.max(0.001, maximum)));
            const safeCastFrames = [0, 1, 2, 3, 4, 4, 6];
            frame = safeCastFrames[Math.min(6, Math.floor(progress * 7))];
          } else if (this.isDashing) {
            row = 3;
            const progress = Math.max(0, Math.min(0.999, 1 - this.dashDuration / this.dashMaxDuration));
            frame = Math.min(6, Math.floor(progress * 7));
          } else if (isMoving) {
            row = 0;
            frame = 2 + Math.floor((this.animClock / 0.085) % 5);
          } else {
            row = 0;
            frame = Math.floor((this.animClock / 0.30) % 2);
          }
          const scale = 0.86 * PACKED_VISUAL_SCALE_240;
          const drawSize = cell * scale;
          const sourceFootY = useErlangCombo ? cell - 48 : cell - 56;
          if (this.isManifested) {
            ctx.save();
            ctx.globalAlpha = 0.34 + Math.sin(this.animClock * 7) * 0.08;
            ctx.strokeStyle = '#93c5fd';
            ctx.lineWidth = 4;
            ctx.shadowColor = '#60a5fa';
            ctx.shadowBlur = 18;
            ctx.beginPath();
            ctx.arc(0, 18, 48, 0, Math.PI * 2);
            ctx.stroke();
            ctx.restore();
          }
          ctx.save();
          if (this.facing === -1) ctx.scale(-1, 1);
          ctx.shadowColor = this.isManifested ? '#60a5fa' : '#facc15';
          ctx.shadowBlur = this.isManifested ? 14 : 6;
          ctx.drawImage(erlangSourceImg, frame * cell, row * cell, cell, cell, -drawSize / 2, 44 - sourceFootY * scale, drawSize, drawSize);
          ctx.restore();
          ctx.restore();
          return;
        }

        const formsImg = loadedImages['wukong_72_forms'];
        const formAttacksImg = loadedImages['wukong_72_form_attacks'];
        if (this.isTransformed && formsImg && formsImg.complete && formsImg.naturalWidth > 0) {
          const cellW = 200;
          const cellH = 200;
          const formRows = { dragon: 0, tiger: 1, roc: 2, ape: 3, tortoise: 4 };
          const r = formRows[this.activeTransformationForm] ?? 0;
          const profile = FORM_COMBAT_PROFILES[this.activeTransformationForm] || FORM_COMBAT_PROFILES.dragon;
          const scale = profile.scale * PACKED_VISUAL_SCALE_200;
          const auraColor = profile.color;

          let c = 0;
          const isMoving = Math.hypot(this.vx, this.vy) > 10;
          const hasAttackSheet = formAttacksImg && formAttacksImg.complete && formAttacksImg.naturalWidth > 0;
          const isCombatAction = this.isAttacking || this.isSpecialActive || this.isCastingSpell;
          let sourceImg = formsImg;
          if (isCombatAction && hasAttackSheet) {
            sourceImg = formAttacksImg;
            let prog = 0;
            if (this.isAttacking) prog = 1 - (this.attackDuration / this.attackMaxDuration);
            else if (this.isSpecialActive) prog = 1 - (this.specialDuration / this.specialMaxDuration);
            else prog = 1 - (this.castSpellDuration / this.castSpellMaxDuration);
            c = Math.min(6, Math.floor(Math.max(0, Math.min(0.999, prog)) * 7));
          } else if (isMoving) {
            c = Math.floor((this.animClock / 0.09) % 7);
          } else {
            c = 0; // the source sheet is locomotion-only; idle must not run in place
          }

          const drawW = cellW * scale;
          const drawH = cellH * scale;
          const sourceFootY = cellH - 48;
          const sharedGroundY = 44;
          const drawY = sharedGroundY - sourceFootY * scale;

          ctx.save();
          if (this.facing === -1) {
            ctx.scale(-1, 1);
          }
          ctx.shadowColor = auraColor;
          ctx.shadowBlur = 14;
          ctx.drawImage(sourceImg, c * cellW, r * cellH, cellW, cellH, -drawW / 2, drawY, drawW, drawH);
          ctx.restore();
          ctx.restore();
          return;
        }

        const alignmentCombatStage = gameState.playableHero === 'wukong' ? getAlignmentCombatStage() : null;
        const useDirectionalRuyiContactBody = gameState.playableHero === 'wukong'
          && this.isAttacking && this.activeRuyiContactProfile;
        if (useDirectionalRuyiContactBody) {
          const attackProgress = Math.max(0, Math.min(.999, 1 - this.attackDuration / Math.max(.001, this.attackMaxDuration)));
          const authoredProgress = getRuyiAuthoredProgress(attackProgress, this.activeRuyiContactProfile, this.activeAttackContactAt);
          const handAnchor = this.drawRuyiDirectionalBodyOnly(ctx, authoredProgress);
          this.drawRuyiContactWeaponPath(ctx, this.activeRuyiContactProfile, authoredProgress, handAnchor);
          this.drawAlignmentAura(ctx, true);
          ctx.restore();
          return;
        }
        const authoredComboAsset = this.activeComboMove
          ? (alignmentCombatStage?.path === 'evil'
              ? 'wukong_combo_moves_evil'
              : (alignmentCombatStage?.path === 'good' ? 'wukong_combo_moves_good' : 'wukong_combo_moves_neutral'))
          : null;
        const authoredComboImg = authoredComboAsset ? loadedImages[authoredComboAsset] : null;
        if (this.isAttacking && this.activeComboMove && authoredComboImg && authoredComboImg.complete && authoredComboImg.naturalWidth > 0) {
          const cell = 256;
          const row = Math.max(0, Math.min(6, this.activeComboMove.animRow ?? 0));
          const progress = Math.max(0, Math.min(.999, 1 - this.attackDuration / Math.max(.001, this.attackMaxDuration)));
          const frame = Math.min(6, Math.floor(progress * 7));
          const scale = (alignmentCombatStage ? .66 : .64) * PACKED_VISUAL_SCALE_256;
          const drawSize = cell * scale;
          const sourceFootY = cell - 48;
          const palette = getAlignmentPalette();
          ctx.save();
          if (this.facing === -1) ctx.scale(-1, 1);
          ctx.shadowColor = alignmentCombatStage?.path === 'evil' ? '#7e22ce' : (alignmentCombatStage?.path === 'good' ? '#60a5fa' : palette.primary);
          ctx.shadowBlur = alignmentCombatStage ? 10 + alignmentCombatStage.tier * 2 : 7;
          ctx.drawImage(authoredComboImg, frame * cell, row * cell, cell, cell, -drawSize / 2, 44 - sourceFootY * scale, drawSize, drawSize);
          ctx.restore();
          this.drawAlignmentAura(ctx, true);
          ctx.restore();
          return;
        }
        const alignmentCombatImg = alignmentCombatStage ? loadedImages[alignmentCombatStage.asset] : null;
        if (alignmentCombatImg && alignmentCombatImg.complete && alignmentCombatImg.naturalWidth > 0) {
          const cell = 240;
          let row = 0;
          let frame = 0;
          const isMoving = Math.hypot(this.vx, this.vy) > 10;
          if (this.isAttacking) {
            row = (this.activeComboMove || this.currentAttackToken === 'R' || this.currentCombo === 2) ? 2 : 1;
            const progress = Math.max(0, Math.min(.999, 1 - this.attackDuration / Math.max(.001, this.attackMaxDuration)));
            frame = Math.min(5, Math.floor(progress * 6));
          } else if (this.isCastingSpell) {
            row = 2;
            const progress = Math.max(0, Math.min(.999, 1 - this.castSpellDuration / Math.max(.001, this.castSpellMaxDuration)));
            frame = Math.min(5, Math.floor(progress * 6));
          } else if (this.isSpecialActive) {
            row = 2;
            const progress = Math.max(0, Math.min(.999, 1 - this.specialDuration / Math.max(.001, this.specialMaxDuration)));
            frame = Math.min(5, Math.floor(progress * 6));
          } else if (this.isDashing) {
            row = 0;
            const progress = Math.max(0, Math.min(.999, 1 - this.dashDuration / Math.max(.001, this.dashMaxDuration)));
            frame = 3 + Math.min(2, Math.floor(progress * 3));
          } else if (isMoving) {
            row = 0;
            frame = 1 + Math.floor((this.animClock / .105) % 5);
          } else {
            row = 0;
            frame = Math.floor((this.animClock / .42) % 2);
          }

          const scale = (.78 + alignmentCombatStage.tier * .014) * PACKED_VISUAL_SCALE_240;
          const drawSize = cell * scale;
          const sourceFootY = cell - 56;
          const palette = getAlignmentPalette();
          if (this.isAttacking && alignmentCombatStage.path === 'evil') {
            const evilStrikeFx = loadedImages['evil_ruyi_combo_fx'];
            if (evilStrikeFx && evilStrikeFx.complete && evilStrikeFx.naturalWidth > 0) {
              const fxCell = 256;
              const fxRow = Math.max(0, Math.min(2, this.currentCombo));
              const fxProgress = Math.max(0, Math.min(.999, 1 - this.attackDuration / Math.max(.001, this.attackMaxDuration)));
              const fxFrame = Math.min(6, Math.floor(fxProgress * 7));
              const fxSize = fxRow === 2 ? 286 : (fxRow === 1 ? 260 : 230);
              const forward = fxRow === 1 ? 0 : (fxRow === 2 ? 72 : 48);
              ctx.save();
              ctx.translate(Math.cos(this.attackAngle) * forward, Math.sin(this.attackAngle) * forward);
              if (fxRow !== 1) ctx.rotate(this.attackAngle + (fxRow === 2 ? -Math.PI / 2 : 0));
              ctx.globalAlpha = .88;
              ctx.shadowColor = '#ef4444';
              ctx.shadowBlur = 7;
              ctx.drawImage(evilStrikeFx, fxFrame * fxCell, fxRow * fxCell, fxCell, fxCell, -fxSize / 2, -fxSize / 2, fxSize, fxSize);
              ctx.restore();
            }
          }
          ctx.save();
          if (this.facing === -1) ctx.scale(-1, 1);
          ctx.shadowColor = alignmentCombatStage.path === 'evil' ? '#7e22ce' : '#60a5fa';
          ctx.shadowBlur = 7 + alignmentCombatStage.tier * 3;
          ctx.drawImage(alignmentCombatImg, frame * cell, row * cell, cell, cell, -drawSize / 2, 44 - sourceFootY * scale, drawSize, drawSize);
          ctx.restore();
          this.drawAlignmentAura(ctx, true);
          ctx.restore();
          return;
        }

        const hairClonesImg = loadedImages['wukong_hair_clones'];
        const combatCombosImg = loadedImages['wukong_combat_combos'];
        const realAnimsImg = loadedImages['wukong_real_anims'];
        const heroImg = loadedImages['hero'];

        if (this.isCastingSpell && hairClonesImg && hairClonesImg.complete && hairClonesImg.naturalWidth > 0) {
          // MK Blowing Hair Spell Casting (Row 0, 6 frames)
          const cellW = 200;
          const cellH = 200;
          const progress = 1 - (this.castSpellDuration / this.castSpellMaxDuration);
          const c = Math.min(5, Math.floor(progress * 6));
          const r = 0;

          const scale = 0.64 * PACKED_VISUAL_SCALE_200;
          const drawW = cellW * scale;
          const drawH = cellH * scale;

          ctx.save();
          if (this.facing === -1) {
            ctx.scale(-1, 1);
          }
          ctx.drawImage(hairClonesImg, c * cellW, r * cellH, cellW, cellH, -drawW / 2, 44 - (cellH - 48) * scale, drawW, drawH);
          ctx.restore();
        } else if (this.isAttacking && heroImg && heroImg.complete && heroImg.naturalWidth > 0) {
          // Keep the canonical ornate Wukong model for every normal attack. The old
          // 220px combo atlas depicted a different, larger character and made the
          // hero visibly transform on every left click.
          const progress = Math.max(0, Math.min(0.999, 1 - this.attackDuration / this.attackMaxDuration));
          const frame = Math.min(6, Math.floor(progress * 7));
          const heroCell = 128;
          const actionRow = this.currentCombo === 1 ? 4 : 3;
          const bodyScale = (this.isAwakened ? 1.22 : (this.weaponStyle === 'titan' ? 1.18 : 1.10)) * PACKED_VISUAL_SCALE_128;
          const impactPulse = Math.sin(progress * Math.PI);
          const bodyLift = this.currentCombo === 2 ? Math.sin(progress * Math.PI) * 18 : 0;
          ctx.save();
          if (this.facing === -1) ctx.scale(-1, 1);
          ctx.rotate((this.facing === -1 ? -1 : 1) * (progress - 0.5) * 0.05);
          ctx.scale(1 + impactPulse * 0.025, 1 - impactPulse * 0.018);
          ctx.drawImage(
            heroImg,
            frame * heroCell,
            actionRow * heroCell,
            heroCell,
            heroCell,
            -heroCell * bodyScale / 2,
            44 - 100 * bodyScale - bodyLift,
            heroCell * bodyScale,
            heroCell * bodyScale
          );
          ctx.restore();

          // A purpose-built Ruyi trail communicates the three contacts without
          // replacing or obscuring Wukong's body. It rotates to the actual aim.
          const meleeFx = loadedImages['ruyi_melee_combo_fx'];
          if (meleeFx && meleeFx.complete && meleeFx.naturalWidth > 0) {
            const fxCell = 256;
            const fxRow = Math.max(0, Math.min(2, this.currentCombo));
            const fxSize = this.currentCombo === 2 ? 250 : (this.currentCombo === 1 ? 230 : 205);
            const forward = this.currentCombo === 2 ? 48 : 34;
            ctx.save();
            ctx.translate(Math.cos(this.attackAngle) * forward, Math.sin(this.attackAngle) * forward);
            ctx.rotate(this.attackAngle + (this.currentCombo === 2 ? Math.PI / 2 : 0));
            ctx.globalAlpha = 0.82;
            ctx.shadowColor = this.getActiveGodColor();
            ctx.shadowBlur = 8;
            ctx.drawImage(meleeFx, frame * fxCell, fxRow * fxCell, fxCell, fxCell, -fxSize / 2, -fxSize / 2, fxSize, fxSize);
            ctx.restore();
          }
        } else if (this.isSpecialActive) {
          const throwImg = loadedImages['wukong_ruyi_throw'];
          const cellW = 220;
          const cellH = 220;
          const progress = Math.max(0, Math.min(0.999, 1 - this.specialDuration / this.specialMaxDuration));
          const c = Math.min(6, Math.floor(progress * 7));
          if (throwImg && throwImg.complete && throwImg.naturalWidth > 0) {
            const scale = (this.weaponStyle === 'titan' ? 0.93 : 0.84) * PACKED_VISUAL_SCALE_220;
            const drawW = cellW * scale;
            const drawH = cellH * scale;
            const sourceFootY = cellH - 52;
            const drawY = 44 - sourceFootY * scale;
            ctx.save();
            if (this.facing === -1) ctx.scale(-1, 1);
            ctx.shadowColor = this.getActiveGodColor();
            ctx.shadowBlur = 7;
            ctx.drawImage(throwImg, c * cellW, 0, cellW, cellH, -drawW / 2, drawY, drawW, drawH);
            ctx.restore();
          } else if (heroImg && heroImg.complete && heroImg.naturalWidth > 0) {
            const heroRow = this.direction === 'up' ? 1 : (this.direction === 'down' ? 0 : 2);
            const heroCol = heroRow === 2 ? 2 : 1;
            ctx.save();
            if (this.facing === -1) ctx.scale(-1, 1);
            const fallbackScale = PACKED_VISUAL_SCALE_128;
            ctx.drawImage(heroImg, heroCol * 128, heroRow * 128, 128, 128, -64 * fallbackScale, 44 - 100 * fallbackScale, 128 * fallbackScale, 128 * fallbackScale);
            ctx.restore();
          }
        } else if (this.isDashing && heroImg && heroImg.complete && heroImg.naturalWidth > 0) {
          // The old cartwheel atlas contained a missing/corrupt middle frame and
          // changed Wukong's costume. Keep the authored hero body and animate a
          // directional squash/tilt while movement interpolates along the path.
          const cellW = 128;
          const cellH = 128;
          const r = this.direction === 'up' ? 1 : (this.direction === 'down' ? 0 : 2);
          const c = r === 2 ? 3 : 3;
          const dashProgress = Math.max(0, Math.min(1, 1 - this.dashDuration / this.dashMaxDuration));
          const scaleX = 1.18 + Math.sin(dashProgress * Math.PI) * 0.22;
          const scaleY = 1.12 - Math.sin(dashProgress * Math.PI) * 0.16;
          ctx.save();
          if (this.facing === -1) ctx.scale(-1, 1);
          ctx.rotate((this.facing === -1 ? -1 : 1) * Math.sin(dashProgress * Math.PI) * 0.10);
          ctx.scale(scaleX, scaleY);
          ctx.globalAlpha = 0.92;
          const packedSize = cellW * PACKED_VISUAL_SCALE_128;
          ctx.drawImage(heroImg, c * cellW, r * cellH, cellW, cellH, -packedSize / 2, 44 / scaleY - 100 * PACKED_VISUAL_SCALE_128, packedSize, packedSize);
          ctx.restore();
        } else if (heroImg && heroImg.complete && heroImg.naturalWidth > 0) {
          const cellW = 128;
          const cellH = 128;

          let r = 0;
          let c = 0;
          const isMoving = Math.hypot(this.vx, this.vy) > 10;

          if (isMoving) {
            if (this.direction === 'up') {
              r = 1;
            } else if (this.direction === 'down') {
              r = 0;
            } else {
              r = 2;
            }
            const runFrames = r === 2 ? 5 : 6;
            c = 1 + Math.floor((this.animClock / 0.085) % runFrames);
          } else {
            if (this.direction === 'up') {
              r = 1;
            } else if (this.direction === 'down') {
              r = 0;
            } else {
              r = 2;
            }
            c = this.direction === 'down' ? 0 : 1;
          }

          r = Math.max(0, Math.min(6, r));
          c = Math.max(0, Math.min(6, c));

          const scale = (this.isAwakened ? 1.22 : (this.weaponStyle === 'titan' ? 1.18 : 1.10)) * PACKED_VISUAL_SCALE_128;
          const drawW = cellW * scale;
          const drawH = cellH * scale;

          ctx.save();
          if (this.facing === -1) {
            ctx.scale(-1, 1);
          }

          if (this.isAwakened) {
            ctx.shadowColor = '#facc15';
            ctx.shadowBlur = 18 + Math.sin(this.animClock * 8) * 4;
          }
          ctx.drawImage(heroImg, c * cellW, r * cellH, cellW, cellH, -drawW / 2, 44 - 100 * scale, drawW, drawH);
          ctx.restore();
        } else {
          // Fallback circular avatar if image is still loading
          ctx.beginPath();
          ctx.arc(0, 0, 26, 0, Math.PI * 2);
          ctx.fillStyle = '#facc15';
          ctx.fill();
        }

        this.drawAlignmentAura(ctx, true);
        ctx.restore();
      }
    }

    const player = new Player();

    // LU BAN IN-GAME AVATAR NPC
    class LubanAvatarNPC {
      constructor(x, y) {
        this.x = x;
        this.y = y;
        this.radius = 36;
        this.animClock = 0;
        this.pulseTimer = 0.2;
      }

      update(dt) {
        this.animClock += dt;
        this.pulseTimer -= dt;
        if (this.pulseTimer <= 0) {
          this.pulseTimer = 0.75;
          fxList.push(new Shockwave(this.x + (Math.random() * 16 - 8), this.y - 20, 25, '#fbbf24'));
        }
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);

        const img = loadedImages['luban_avatar'];
        if (img && img.complete && img.naturalWidth > 0) {
          const cellW = 128;
          const cellH = 128;
          const packedSize = cellW * PACKED_VISUAL_SCALE_128;
          const packedY = 44 - (cellH - 28) * PACKED_VISUAL_SCALE_128;

          ctx.drawImage(img, 0, 3 * cellH, cellW, cellH, -packedSize / 2, packedY, packedSize, packedSize);

          const c = Math.floor((this.animClock / 0.12) % 8);
          ctx.drawImage(img, c * cellW, 1 * cellH, cellW, cellH, -packedSize / 2, packedY, packedSize, packedSize);
        }

        const dist = Math.hypot(player.x - this.x, player.y - this.y);
        ctx.font = getCanvasFont(15, 700);
        ctx.textAlign = 'center';
        ctx.fillStyle = '#fbbf24';
        ctx.shadowColor = '#000';
        ctx.shadowBlur = 8;
        ctx.fillText(uiText('【巧圣仙师·鲁班】神兵天铸', '[Sage Artisan Lu Ban] Divine Weapon Forge'), 0, -82);

        if (dist < 100) {
          ctx.fillStyle = '#fff2a8';
          ctx.font = getCanvasFont(13, 700);
          ctx.fillText(uiText('按 [E] / 点击 对话重铸金箍棒', 'Press [E] / tap to reforge your weapon'), 0, -64);
        }

        ctx.restore();
      }
    }

    let activeLubanAvatar = null;

    class ClockworkKiteRocket {
      constructor(x, y, target, damage) {
        this.x = x;
        this.y = y;
        this.target = target;
        this.damage = damage;
        this.speed = 440;
        this.radius = 12;
        this.life = 2.4;
        this.alive = true;
        this.angle = target ? Math.atan2(target.y - y, target.x - x) : 0;
        this.trailTimer = 0;
      }

      explode() {
        if (!this.alive) return;
        this.alive = false;
        enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - this.x, enemy.y - this.y) <= 105 + enemy.radius)
          .slice(0, 8).forEach(enemy => {
            enemy.takeDamage(this.damage, false, true);
            enemy.applyBurn(this.damage * 0.28, 1.5);
          });
        fxList.push(new AnimatedFireExplosion(this.x, this.y, 105));
        fxList.push(new Shockwave(this.x, this.y, 105, '#fbbf24'));
        fxList.push(new RadialSparksFX(this.x, this.y, 12, '#fef08a', 68));
        createScreenShake(3);
      }

      update(dt) {
        this.life -= dt;
        if (!this.target || !this.target.alive || this.target.isAlly) {
          this.target = enemies.filter(enemy => enemy.alive && !enemy.isAlly)
            .sort((a, b) => Math.hypot(a.x - this.x, a.y - this.y) - Math.hypot(b.x - this.x, b.y - this.y))[0] || null;
        }
        if (this.target) {
          const desired = Math.atan2(this.target.y - this.y, this.target.x - this.x);
          let delta = desired - this.angle;
          while (delta > Math.PI) delta -= Math.PI * 2;
          while (delta < -Math.PI) delta += Math.PI * 2;
          this.angle += Math.max(-5.5 * dt, Math.min(5.5 * dt, delta));
        }
        this.x += Math.cos(this.angle) * this.speed * dt;
        this.y += Math.sin(this.angle) * this.speed * dt;
        this.trailTimer -= dt;
        if (this.trailTimer <= 0) {
          this.trailTimer = 0.05;
          fxList.push(new RadialSparksFX(this.x - Math.cos(this.angle) * 13, this.y - Math.sin(this.angle) * 13, 2, '#fb923c', 16));
        }
        if (this.target && Math.hypot(this.target.x - this.x, this.target.y - this.y) <= this.target.radius + this.radius) this.explode();
        else if (this.life <= 0) this.explode();
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);
        ctx.shadowColor = '#f59e0b'; ctx.shadowBlur = 12;
        ctx.fillStyle = '#78350f';
        ctx.fillRect(-16, -5, 29, 10);
        ctx.fillStyle = '#fbbf24';
        ctx.beginPath(); ctx.moveTo(18, 0); ctx.lineTo(8, -9); ctx.lineTo(8, 9); ctx.closePath(); ctx.fill();
        ctx.strokeStyle = '#fde68a'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(-12, 0, 7, 0, Math.PI * 2); ctx.stroke();
        for (let i = 0; i < 4; i++) {
          const a = this.life * 18 + i * Math.PI / 2;
          ctx.beginPath(); ctx.moveTo(-12, 0); ctx.lineTo(-12 + Math.cos(a) * 12, Math.sin(a) * 12); ctx.stroke();
        }
        ctx.restore();
      }
    }

    class ClockworkKiteCompanion {
      constructor() {
        this.x = player.x + 72;
        this.y = player.y - 72;
        this.radius = 28;
        this.animClock = 0;
        this.fireTimer = 0.55;
        this.alive = true;
      }

      update(dt) {
        this.alive = player.hasBoon('luban_clockwork_kite');
        if (!this.alive) return;
        this.animClock += dt;
        const desiredX = player.x + Math.cos(this.animClock * 0.92) * 88;
        const desiredY = player.y - 74 + Math.sin(this.animClock * 1.84) * 25;
        this.x += (desiredX - this.x) * Math.min(1, dt * 5.5);
        this.y += (desiredY - this.y) * Math.min(1, dt * 5.5);
        this.fireTimer -= dt;
        if (this.fireTimer <= 0) {
          const target = enemies.filter(enemy => enemy.alive && !enemy.isAlly && Math.hypot(enemy.x - this.x, enemy.y - this.y) <= 920)
            .sort((a, b) => Math.hypot(a.x - this.x, a.y - this.y) - Math.hypot(b.x - this.x, b.y - this.y))[0];
          if (target) {
            const rank = player.getBoonLevel('luban_clockwork_kite');
            this.fireTimer = Math.max(1.7, 3.0 - 0.18 * (rank - 1));
            const damage = 90 * (1 + 0.30 * (rank - 1)) * (player.metaDamageMultiplier || 1);
            projectiles.push(new ClockworkKiteRocket(this.x, this.y, target, damage));
            fxList.push(new RadialSparksFX(this.x, this.y, 8, '#fbbf24', 44));
            floatingTexts.push(new FloatingText(this.x, this.y - 34, uiText('木鸢霹雳！', 'Clockwork Missile!'), '#fde68a', 13));
          } else {
            this.fireTimer = 0.35;
          }
        }
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        const flap = Math.sin(this.animClock * 8) * 5;
        ctx.shadowColor = '#f59e0b'; ctx.shadowBlur = 13;
        ctx.fillStyle = '#b45309'; ctx.strokeStyle = '#fde68a'; ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(0, -24); ctx.lineTo(34, flap); ctx.lineTo(0, 21); ctx.lineTo(-34, -flap); ctx.closePath();
        ctx.fill(); ctx.stroke();
        ctx.strokeStyle = '#78350f'; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(-31, -flap); ctx.lineTo(31, flap); ctx.moveTo(0, -22); ctx.lineTo(0, 20); ctx.stroke();
        ctx.fillStyle = '#fbbf24'; ctx.beginPath(); ctx.arc(0, 0, 8, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#fef3c7'; ctx.lineWidth = 2;
        for (let i = 0; i < 6; i++) {
          const a = this.animClock * 7 + i * Math.PI / 3;
          ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(a) * 16, Math.sin(a) * 16); ctx.stroke();
        }
        ctx.strokeStyle = '#f59e0b';
        ctx.beginPath(); ctx.moveTo(0, 21); ctx.quadraticCurveTo(18, 33, -4, 47); ctx.quadraticCurveTo(-20, 58, 4, 67); ctx.stroke();
        ctx.font = getCanvasFont(10, 900); ctx.textAlign = 'center'; ctx.fillStyle = '#fff7ed';
        ctx.fillText(uiText('神机木鸢', 'Clockwork Kite'), 0, -32);
        ctx.restore();
      }
    }

    let activeClockworkKite = null;

    // The authored campaign follows Wukong's life chronologically. Every chapter
    // selects one of the nine ImageGen arenas and named encounters use matching
    // seven-state animation rows (idle/run/windup/attack/impact/hurt/defeat).
    const CAMPAIGN_STAGES = [
      { max: 5, biome: 0, title: '花果山·水帘洞', sub: '与群猴试艺，从无名石猴打上花果山之巅', accent: '#4ade80' },
      { max: 8, biome: 1, title: '昆仑天梯·元始仙山', sub: '登天问道，择十八、三十六或七十二般变化', accent: '#c4b5fd' },
      { max: 12, biome: 2, title: '玉虚宫·弟子演武场', sub: '破玉虚门人阵，亲试元始天尊法度', accent: '#93c5fd' },
      { max: 18, biome: 3, title: '东海龙宫·珊瑚水府', sub: '踏浪入海，向东海龙王借取定海神珍', accent: '#22d3ee' },
      { max: 19, biome: 4, title: '龙宫宝库·定海神珍', sub: '如意金箍棒认主，一万三千五百斤随心变化', accent: '#facc15' },
      { max: 32, biome: 5, title: '九重天宫·凌霄金阙', sub: '战哪吒、四大天王、二郎神，直面如来佛祖', accent: '#fde68a' },
      { max: 33, biome: 7, title: '五指山·石匣幽谷', sub: '五百年风雨之后，取经人唐三藏来到山前', accent: '#a3e635' },
      { max: 36, biome: 9, title: '高老庄·竹林田舍', sub: '降服天蓬旧将猪八戒，师徒队伍初成', accent: '#86efac' },
      { max: 40, biome: 10, title: '流沙河·弱水险滩', sub: '踏过鹅毛不浮的流沙弱水，收卷帘将沙悟净', accent: '#38bdf8' },
      { max: 45, biome: 11, title: '白虎岭·白骨荒原', sub: '火眼金睛识三重幻相，纵被误会仍护师父周全', accent: '#e2e8f0' },
      { max: 50, biome: 12, title: '盘丝洞·七情蛛窟', sub: '万缕蛛丝缚身，师徒同心破七情疑阵', accent: '#c084fc' },
      { max: 55, biome: 13, title: '积雷山·牛魔王寨', sub: '旧日结义今日交锋，平天大圣守住火焰山', accent: '#f87171' },
      { max: 60, biome: 14, title: '火云洞·三昧火阵', sub: '红孩儿驾五辆火车，以三昧真火封住西行路', accent: '#fb923c' },
      { max: 64, biome: 15, title: '火焰山·万里赤地', sub: '烈焰横断八百里，唯有芭蕉宝扇可息天火', accent: '#f97316' },
      { max: 65, biome: 16, title: '翠云山·芭蕉洞', sub: '与铁扇公主了结家怨，借扇平息火焰山', accent: '#4ade80' },
      { max: 68, biome: 18, title: '祭赛国·金光寺碧波潭', sub: '为蒙冤僧众扫塔，追讨九头虫盗走的佛宝舍利', accent: '#fbbf24' },
      { max: 72, biome: 19, title: '荆棘岭·小雷音寺', sub: '木仙诗会暗藏情关，黄眉假佛更设金铙人种袋', accent: '#c084fc' },
      { max: 77, biome: 20, title: '朱紫国·麒麟山黄花观', sub: '悬丝诊脉炼乌金丹，盗紫金铃并破百眼毒光', accent: '#fb7185' },
      { max: 82, biome: 21, title: '狮驼岭·万妖之国', sub: '青狮、白象、金翅大鹏各守一关，解救满城生灵', accent: '#f59e0b' },
      { max: 88, biome: 22, title: '比丘国·陷空山无底洞', sub: '救千童、识白鹿、循雪中鼠影深入无底迷宫', accent: '#a5f3fc' },
      { max: 94, biome: 23, title: '隐雾山·玉华州竹节山', sub: '破豹精假首疑云，授艺三王子并战九灵元圣', accent: '#84cc16' },
      { max: 96, biome: 24, title: '金平府·青龙山', sub: '灯节三犀假佛盗油，寒暑尘三阵连环压境', accent: '#38bdf8' },
      { max: 99, biome: 25, title: '天竺国·广寒月宫', sub: '绣球招亲真假公主，月镜照出玉兔真身', accent: '#e0e7ff' },
      { max: 100, biome: 26, title: '灵山·凌云渡大雷音寺', sub: '脱去凡胎取得真经，渡过第八十一难回长安成佛', accent: '#fde68a' },
      { max: Infinity, biome: 26, title: '斗战胜佛·新西游', sub: '九九归真，仍可重温百章西游与诸天试炼', accent: '#facc15' }
    ];

    const CAMPAIGN_STAGE_EN = {
      0: ['Flower-Fruit Mountain · Water-Curtain Cave', 'Train with the monkey clan and climb from nameless Stone Monkey to king of the mountain.'],
      1: ['Kunlun Stairway · Yuanshi’s Sacred Mountain', 'Climb toward Heaven and choose 18, 36, or 72 transformations.'],
      2: ['Jade-Void Palace · Disciple Arena', 'Break the disciples’ formation and face Yuanshi Tianzun’s final trial.'],
      3: ['Eastern Sea Dragon Palace · Coral Court', 'Enter the ocean realm and seek the sea-calming Ruyi Jingu Bang.'],
      4: ['Dragon Treasury · Sea-Calming Treasure', 'The 13,500-jin Ruyi Staff recognizes its master.'],
      5: ['Celestial Court · Lingxiao Palace', 'Face Nezha, each of the Four Heavenly Kings, Erlang Shen, and finally Buddha.'],
      7: ['Five-Finger Mountain · Stone Valley', 'After five hundred years, the pilgrim Tang Sanzang arrives.'],
      9: ['Gao Village · Bamboo Farmland', 'Subdue Zhu Bajie and add the former Marshal Tianpeng to the pilgrimage.'],
      10: ['Flowing-Sands River · Treacherous Shoals', 'Cross the feather-sinking waters and recruit Sha Wujing.'],
      11: ['White-Bone Ridge · Bleached Wastes', 'See through three disguises and protect the master despite mistrust.'],
      12: ['Webbed Hollow · Cavern of Desire', 'Break the prison of ten thousand webs through fellowship.'],
      13: ['Mount Thunder · Bull Demon Stronghold', 'Old sworn brothers collide over the fate of Flaming Mountain.'],
      14: ['Fire-Cloud Cave · Samadhi Fire Array', 'Red Boy seals the western road with five fire carts and Samadhi flame.'],
      15: ['Flaming Mountain · Eight Hundred Li of Fire', 'Only the Plantain Fan can extinguish the burning road.'],
      16: ['Emerald-Cloud Mountain · Plantain Cave', 'Settle the family feud, borrow the fan, and save Flaming Mountain.'],
      17: ['Endless Journey West', 'The fellowship continues toward Thunderclap Monastery.'],
      18: ['Jisai · Golden Pagoda', 'Clear the pagoda, vindicate its monks, and recover the stolen Buddhist relic from the Nine-Headed Beast.'],
      19: ['Thorn Ridge · Little Thunderclap', 'Pass the tree immortals’ trial, then escape Yellow Brows’ false Buddha hall, golden cymbals, and Human Seed Bag.'],
      20: ['Zhuzi · Qilin Mountain', 'Cure the king, steal the Purple-Gold Bells, and break the Hundred-Eyed Demon’s poison light.'],
      21: ['Lion-Camel Ridge', 'Break the three gates held by the Azure Lion, White Elephant, and Golden-Winged Great Peng.'],
      22: ['Bhikkhu · Bottomless Cave', 'Save the children, expose the White Deer, and follow the mouse spirit into the shifting abyss.'],
      23: ['Yuhua · Bamboo-Joint Mountain', 'Defeat the leopard, train three princes, recover the weapons, and face the Nine-Spirit Lion.'],
      24: ['Jinping · Azure-Dragon Mountain', 'Expose three false Buddhas and survive the interlocking frost, heat, and dust domains.'],
      25: ['Tianzhu · Moon-Palace Road', 'Unmask the false princess and return the Jade Rabbit to the moon.'],
      26: ['Vulture Peak · Thunderclap', 'Shed the mortal shell, receive the scriptures, endure the final river ordeal, and return to Chang’an.']
    };

    const ERLANG_FENGSHEN_STAGES = [
      { max:4, biome:1, title:'玉泉山·金霞洞', titleEn:'Yuquan Mountain · Golden-Rays Cave', sub:'玉鼎真人门下修天眼、八九玄功与三尖两刃枪', subEn:'Train the Third Eye, Eight-Nine Mysteries, and three-pointed spear under Master Yuding.', accent:'#93c5fd' },
      { max:8, biome:0, title:'桃山·劈山救母', titleEn:'Peach Mountain · Rescue of His Mother', sub:'杨戬违天条劈开桃山，从此看清天命与亲情的冲突', subEn:'Yang Jian defies Heaven and splits Peach Mountain, confronting the cost of divine law.', accent:'#fda4af' },
      { max:12, biome:5, title:'西岐·封神前线', titleEn:'Xiqi · Front of Investiture', sub:'奉姜子牙之请入西岐，以护民而非求封神之位', subEn:'Answer Jiang Ziya’s call and defend Xiqi for its people, not for a divine title.', accent:'#fde68a' },
      { max:16, biome:2, title:'十绝阵·昆仑战场', titleEn:'Ten Absolute Arrays · Kunlun Front', sub:'以天眼辨阵眼，在阐截两教的仇怨之间寻找生路', subEn:'Read the Ten Absolute Arrays with the Third Eye and find a path through sectarian vengeance.', accent:'#c4b5fd' },
      { max:20, biome:15, title:'绝龙岭·闻太师归路', titleEn:'Juelong Ridge · Wen Zhong’s Last Road', sub:'雷部正神闻仲忠于殷商，杨戬必须击败而不轻辱忠臣', subEn:'Wen Zhong remains loyal to Shang; Erlang must defeat a worthy servant without dishonoring him.', accent:'#fbbf24' },
      { max:24, biome:12, title:'九曲黄河阵·三霄云台', titleEn:'Yellow River Array · Three-Sky Terrace', sub:'混元金斗削仙根，云霄以大阵为兄长复仇', subEn:'The Primordial Gold Dipper strips immortal power as Yunxiao seeks vengeance for her brother.', accent:'#67e8f9' },
      { max:28, biome:20, title:'金鸡岭·五色神光', titleEn:'Jinjiling · Five-Colored Divine Light', sub:'孔宣神光尽收五行法宝，天眼也无法只靠蛮力破局', subEn:'Kong Xuan’s five-colored light captures every elemental treasure; force alone cannot solve the duel.', accent:'#e879f9' },
      { max:34, biome:23, title:'梅山·七怪妖云', titleEn:'Mount Mei · Seven Demon Generals', sub:'杨戬以八九玄功对上袁洪七十二变，真假变化斗遍山河', subEn:'Yang Jian’s Eight-Nine Mysteries confront Yuan Hong’s transformations across Mount Mei.', accent:'#fb7185' },
      { max:38, biome:26, title:'朝歌·封神台', titleEn:'Zhaoge · Altar of Investiture', sub:'商周战火终止，杨戬从亲历者视角见证众魂归位', subEn:'As the Shang-Zhou war ends, Erlang witnesses the fallen receive their divine offices.', accent:'#facc15' }
    ];

    function getCampaignStage(index) {
      const stages = gameState.campaignRoute === 'fengshen' ? ERLANG_FENGSHEN_STAGES : CAMPAIGN_STAGES;
      return stages.find(stage => index <= stage.max) || stages[stages.length - 1];
    }

    const ERLANG_FENGSHEN_CHAPTERS = [null,
      { titleZh:'金霞洞开目', titleEn:'The Third Eye Opens', zh:'少年杨戬拜入玉鼎真人门下。师父没有先教杀伐，而是让他学会看见法术背后的因果。', en:'Young Yang Jian enters Master Yuding’s school. Before teaching violence, Yuding teaches him to see the causes hidden behind magic.', erlangZh:'若天眼只能找出敌人的破绽，它还算不上大道。', erlangEn:'If the Third Eye sees only an enemy’s weakness, it is not yet the Way.', allyNameZh:'玉鼎真人', allyNameEn:'Master Yuding', allyZh:'先看清为何出枪，再问这一枪能否刺中。', allyEn:'First understand why you raise the spear; only then ask whether it can strike.' },
      { titleZh:'八九玄功', titleEn:'The Eight-Nine Mysteries', zh:'杨戬在山风中练习七十二般玄妙变化，却坚持保持自己的本相与第三只眼。', en:'Yang Jian practices the transformations of the Eight-Nine Mysteries, yet insists on preserving his own form and Third Eye.', erlangZh:'变化不是逃离自己，而是以万形守住一心。', erlangEn:'Transformation is not escape from oneself; it is one purpose carried through many forms.', allyNameZh:'玉鼎真人', allyNameEn:'Master Yuding', allyZh:'记住这句话。将来你会遇到另一个精通变化的猿将。', allyEn:'Remember it. One day you will meet an ape general equally skilled in transformation.' },
      { titleZh:'三尖两刃', titleEn:'The Three-Pointed Spear', zh:'三尖两刃枪认主。杨戬以轻、重、挑、轮、判五路枪势构成自己的连招。', en:'The three-pointed spear accepts its master. Erlang shapes five linked arts: drill, rise, pin, wheel, and judgment.', erlangZh:'枪有三尖，心不可有三意。', erlangEn:'The spear has three points; the heart must not have three intentions.', allyNameZh:'玉鼎真人', allyNameEn:'Master Yuding', allyZh:'哮天犬会补足你看不见的侧翼，但不可把同伴当作兵器。', allyEn:'Xiaotianquan will guard the flank you cannot see, but never treat a companion as a weapon.' },
      { titleZh:'金霞洞试炼', titleEn:'Trial of Golden Rays', zh:'金霞洞弟子布下雷镜阵，杨戬必须用天眼辨出真身，以完整连招破阵。', en:'Disciples form the Thunder-Mirror Array. Erlang must identify the true bodies and break it with complete spear chains.', erlangZh:'天眼锁真，三尖破妄。', erlangEn:'The Third Eye fixes truth; the three points pierce illusion.', allyNameZh:'玉鼎真人', allyNameEn:'Master Yuding', allyZh:'下山吧。桃山正在等你作出第一场真正的选择。', allyEn:'Descend the mountain. Peach Mountain awaits your first real choice.' },
      { titleZh:'天条与母亲', titleEn:'Divine Law and His Mother', zh:'云华仙子因触犯天条被镇桃山。杨戬第一次怀疑：天庭的秩序是否总等于正义。', en:'Princess Yunhua is imprisoned beneath Peach Mountain for breaking divine law. Yang Jian first questions whether Heaven’s order always equals justice.', erlangZh:'若守法必须忘记母亲，这条法便需要被天眼重新审视。', erlangEn:'If obeying law requires forgetting my mother, that law must face the Third Eye.', allyNameZh:'哮天犬', allyNameEn:'Xiaotianquan', allyZh:'汪！山中有天兵，也有无辜樵夫，主人要分清。', allyEn:'Woof! There are heavenly troops and innocent woodcutters on the mountain. Tell them apart.' },
      { titleZh:'劈桃山', titleEn:'Splitting Peach Mountain', zh:'杨戬避开山民与守山灵脉，以玄功聚力劈开桃山封印。', en:'Erlang avoids villagers and the mountain’s living veins, concentrating the Mysteries to split the celestial seal.', erlangZh:'这一枪只破牢笼，不伤山中一草一木。', erlangEn:'This strike breaks only the prison—not one living thing upon the mountain.', allyNameZh:'云华仙子', allyNameEn:'Princess Yunhua', allyZh:'戬儿，救人容易，背负违逆天命的后果更难。', allyEn:'My son, rescue is the easy part. Bearing the cost of defying Heaven is harder.' },
      { titleZh:'天兵追索', titleEn:'Heaven’s Pursuit', zh:'天兵追至山口。杨戬不愿杀戮旧日同僚，只以枪背击落兵刃。', en:'Heavenly soldiers pursue him to the pass. Erlang refuses to slaughter them and disarms them with the spear’s haft.', erlangZh:'回去告诉天庭：杨戬认罪，但不认错。', erlangEn:'Tell Heaven: Yang Jian accepts the charge, but not that the rescue was wrong.', allyNameZh:'天将', allyNameEn:'Heavenly Captain', allyZh:'你今日放我，来日凌霄殿仍会记下这笔账。', allyEn:'Spare me today, and Lingxiao Palace will still record the debt.' },
      { titleZh:'灌江立誓', titleEn:'The Guanjiang Oath', zh:'杨戬在灌江口立庙护民，决定让香火来自百姓自愿，而非天庭敕令。', en:'At Guanjiang, Erlang establishes a temple to protect the people, accepting worship freely given rather than commanded by Heaven.', erlangZh:'神位若不能护住门前百姓，不过是一张金纸。', erlangEn:'A divine title that cannot protect the people at its gate is only a piece of gilded paper.', allyNameZh:'梅山兄弟', allyNameEn:'Brothers of Mount Mei', allyZh:'真君，西岐姜子牙派人求援，殷商大军已经压境。', allyEn:'True Lord, Jiang Ziya of Xiqi asks for aid. Shang’s army is already at the border.' },
      { titleZh:'入西岐', titleEn:'Entering Xiqi', zh:'杨戬来到西岐，不为封神榜上的名位，而为阻止战火吞没百姓。', en:'Erlang arrives in Xiqi, not for a place on the Investiture Roll but to keep war from consuming civilians.', erlangZh:'我可助周军，却不会把所有殷将都当作妖邪。', erlangEn:'I will aid Zhou, but I will not call every Shang general a demon.', allyNameZh:'姜子牙', allyNameEn:'Jiang Ziya', allyZh:'正因如此，贫道才请你来。封神之战最缺的不是强者，是能分辨的人。', allyEn:'That is why I asked for you. This war lacks not power, but discernment.' },
      { titleZh:'张桂芳点名', titleEn:'Zhang Guifang Calls the Name', zh:'张桂芳以点名落魂术震慑周营。天眼看见每一道军魂都系着一个未归的家。', en:'Zhang Guifang terrifies Zhou’s camp with his name-calling soul art. The Third Eye sees every soldier’s spirit tied to a home awaiting return.', erlangZh:'落魂术能夺神，却夺不走我为何而战。', erlangEn:'Your soul art can shake the spirit, but not the reason I fight.', allyNameZh:'张桂芳', allyNameEn:'Zhang Guifang', allyZh:'杨戬！既入战阵，便休谈两全！', allyEn:'Yang Jian! Once you enter war, abandon dreams of saving both sides!' },
      { titleZh:'魂幡夜袭', titleEn:'Night of Soul Banners', zh:'商营魂幡夜袭西岐。杨戬与哮天犬逐营拔旗，为伤兵开出退路。', en:'Shang soul banners descend on Xiqi at night. Erlang and Xiaotianquan tear them down and open an escape for the wounded.', erlangZh:'犬儿守住伤兵，我去断法坛。', erlangEn:'Guard the wounded, Xiaotianquan. I will break the altar.', allyNameZh:'哮天犬', allyNameEn:'Xiaotianquan', allyZh:'汪！锁定持幡者！', allyEn:'Woof! Banner bearer marked!' },
      { titleZh:'点将伏旗', titleEn:'Subduing Zhang Guifang', zh:'张桂芳亲临阵前。杨戬以天眼封住落魂声，以三尖枪逼他撤去魂幡。', en:'Zhang Guifang takes the field. Erlang seals the soul-calling voice with his Third Eye and forces the banners down.', erlangZh:'忠勇不该成为伤害百姓的借口。撤旗，我留你性命。', erlangEn:'Loyalty is no excuse to harm civilians. Lower the banners, and you live.', allyNameZh:'张桂芳', allyNameEn:'Zhang Guifang', allyZh:'那便让本将看看，你的仁慈能否挡住千军！', allyEn:'Then let me see whether mercy can withstand an army!' },
      { titleZh:'十绝阵书', titleEn:'The Challenge of Ten Arrays', zh:'金鳌岛十天君送来阵书。每一阵都以天地异象为门，却要凡人性命作代价。', en:'The Ten Lords of Golden-Ao Island issue their challenge. Each array opens with a cosmic phenomenon and feeds upon mortal lives.', erlangZh:'先疏散阵外村落，再谈破阵功名。', erlangEn:'Evacuate the villages before anyone speaks of glory in breaking arrays.', allyNameZh:'姜子牙', allyNameEn:'Jiang Ziya', allyZh:'你从桃山学会的，正是这场大战最需要的次序。', allyEn:'The priority you learned at Peach Mountain is exactly what this war needs.' },
      { titleZh:'天绝雷门', titleEn:'Gate of the Heaven-Absolute Array', zh:'天绝阵雷门轮转。杨戬借犬吠回声测出虚实，带周军绕开死门。', en:'Thunder gates rotate inside the Heaven-Absolute Array. Erlang uses Xiaotianquan’s echoing bark to chart the false paths.', erlangZh:'听声辨位，天眼只看最后一层。', erlangEn:'We navigate by sound; the Third Eye is saved for the final veil.', allyNameZh:'秦天君', allyNameEn:'Lord Qin', allyZh:'你能看破一门，未必看得破十门！', allyEn:'You may see through one gate, but not all ten!' },
      { titleZh:'地烈火脉', titleEn:'Earth-Blaze Veins', zh:'地烈阵引燃地脉。杨戬没有直冲阵心，而是先封住蔓延向农田的火线。', en:'The Earth-Blaze Array ignites the land’s veins. Erlang first seals the fire spreading toward farmland instead of rushing the core.', erlangZh:'破阵慢一步，百姓便少烧一亩田。', erlangEn:'Let the victory wait if it saves another field from burning.', allyNameZh:'周军先锋', allyNameEn:'Zhou Vanguard', allyZh:'真君，阵主正在趁机蓄势！', allyEn:'True Lord, the array master is gathering power!' },
      { titleZh:'十阵同鸣', titleEn:'Ten Arrays Resound', zh:'十绝阵同时共鸣。杨戬以天眼标出阵眼，让众仙不再以门人性命盲试死门。', en:'All Ten Arrays resonate. Erlang marks their eyes so the immortals need not sacrifice disciples to test fatal gates.', erlangZh:'封神榜记的是名字，我看见的却是每一个会死的人。', erlangEn:'The Investiture Roll records names; I see every person who would die.', allyNameZh:'玉鼎真人', allyNameEn:'Master Yuding', allyZh:'今日你已不是跟在我身后的弟子。去做你判断正确的事。', allyEn:'Today you are no longer the disciple walking behind me. Do what you judge right.' },
      { titleZh:'闻太师回朝', titleEn:'Grand Preceptor Wen Returns', zh:'闻仲平叛归朝，见商纣失德仍选择守住社稷。他的忠与杨戬的义正面相撞。', en:'Wen Zhong returns from campaign and chooses to defend Shang despite King Zhou’s corruption. His loyalty collides with Erlang’s justice.', erlangZh:'太师忠于江山，可江山之下还有百姓。', erlangEn:'You are loyal to the realm, Grand Preceptor—but beneath the realm are its people.', allyNameZh:'闻仲', allyNameEn:'Wen Zhong', allyZh:'臣若只在君明时尽忠，那忠便只是求名。', allyEn:'If a minister is loyal only to a worthy king, that loyalty is merely vanity.' },
      { titleZh:'墨麒麟踏雷', titleEn:'The Ink Qilin Rides Thunder', zh:'墨麒麟踏云而来，雷部神将封锁山道。杨戬以枪轮挡雷，为两军伤员争取撤离时间。', en:'Wen Zhong’s Ink Qilin rides the storm as thunder generals seal the pass. Erlang wheels his spear to shield wounded soldiers on both sides.', erlangZh:'今日先停半刻，让伤者离阵。', erlangEn:'Grant half an hour. Let the wounded leave the field.', allyNameZh:'闻仲', allyNameEn:'Wen Zhong', allyZh:'准。半刻之后，你我各尽其道。', allyEn:'Granted. Afterward, each of us follows his path.' },
      { titleZh:'绝龙岭雷书', titleEn:'Thunder Edict at Juelong Ridge', zh:'闻仲在绝龙岭布下雷书。杨戬看见这位老臣早知归路已绝，却仍不肯弃军而逃。', en:'Wen Zhong lays a thunder edict at Juelong Ridge. The Third Eye sees that he knows there is no road home, yet refuses to abandon his army.', erlangZh:'我敬你的忠，所以必须亲手结束这场战。', erlangEn:'I honor your loyalty, and therefore I must end this battle myself.', allyNameZh:'闻仲', allyNameEn:'Wen Zhong', allyZh:'杨戬，莫留手。对忠臣最大的侮辱，便是假意相让。', allyEn:'Do not hold back, Yang Jian. False mercy is the deepest insult to a loyal servant.' },
      { titleZh:'雷祖伏阵', titleEn:'The Grand Preceptor Subdued', zh:'天眼与额上神目隔雷相望，三尖枪对雌雄双鞭。此战决定绝龙岭还能否让士卒活着离开。', en:'Third Eye meets heavenly brow-mark through the storm; three-pointed spear meets paired whips. The soldiers’ survival depends on this duel.', erlangZh:'太师，败后撤军。我不会取你性命。', erlangEn:'Withdraw when you yield, Grand Preceptor. I will not take your life.', allyNameZh:'闻仲', allyNameEn:'Wen Zhong', allyZh:'先胜过雷部正法，再说生死！', allyEn:'First overcome the true thunder law—then speak of life and death!' },
      { titleZh:'赵公明遗恨', titleEn:'After Zhao Gongming', zh:'赵公明败亡的消息传至三仙岛。三霄下山，不为商纣，只为兄长讨还因果。', en:'News of Zhao Gongming’s fall reaches Three-Immortal Isle. The Three Xiaos descend not for King Zhou, but to answer their brother’s death.', erlangZh:'复仇有缘由，却仍会把无辜卷入阵中。', erlangEn:'Vengeance has a cause, but it still draws innocents into the array.', allyNameZh:'云霄娘娘', allyNameEn:'Lady Yunxiao', allyZh:'你既看得见因果，就该看见阐教欠下的债。', allyEn:'If you truly see cause and consequence, then see the debt owed by your own sect.' },
      { titleZh:'混元金斗', titleEn:'The Primordial Gold Dipper', zh:'混元金斗收走仙家修为。杨戬放弃追击，先救出被削去顶上三花的同门。', en:'The Primordial Gold Dipper strips immortal cultivation. Erlang abandons pursuit to rescue disciples whose three flowers have been cut away.', erlangZh:'修为可再炼，人命不能重来。', erlangEn:'Cultivation can be rebuilt. A life cannot.', allyNameZh:'杨任', allyNameEn:'Yang Ren', allyZh:'若让她完成黄河阵，所有人都会变成凡骨。', allyEn:'If she completes the Yellow River Array, every immortal here becomes mortal bone.' },
      { titleZh:'九曲黄河', titleEn:'Nine-Bend Yellow River Array', zh:'九曲黄河阵折叠方向与岁月。天眼只能照亮一瞬，哮天犬必须记住归路。', en:'The Nine-Bend Yellow River Array folds direction and time. The Third Eye reveals only moments; Xiaotianquan must remember the way home.', erlangZh:'我看阵眼，你记气味。我们一起把众人带出去。', erlangEn:'I will watch the array eye. You remember the scent. Together we lead them out.', allyNameZh:'哮天犬', allyNameEn:'Xiaotianquan', allyZh:'汪！归路未断！', allyEn:'Woof! The road home remains!' },
      { titleZh:'云霄问因果', titleEn:'Yunxiao Questions Cause and Effect', zh:'云霄守在金斗之前。她不愿伤凡人，却也不肯让兄长之死被一句天命带过。', en:'Yunxiao stands before the Gold Dipper. She will not harm mortals, but refuses to let “destiny” erase her brother’s death.', erlangZh:'我不替任何一教说天命。今日只阻止大阵继续吞人。', erlangEn:'I speak for no sect’s destiny. Today I stop this array from consuming more lives.', allyNameZh:'云霄娘娘', allyNameEn:'Lady Yunxiao', allyZh:'那就以你的天眼，看清我这一斗为何而落！', allyEn:'Then use your Third Eye and see why this dipper must fall!' },
      { titleZh:'金斗归静', titleEn:'The Gold Dipper Falls Silent', zh:'大阵停转。杨戬必须在复仇、门规与无辜者之间作出不杀云霄的处置。', en:'The array stops. Erlang must resolve Yunxiao’s fate without killing her, balancing vengeance, sect law, and innocent lives.', erlangZh:'你可以恨阐教，但不能再以凡人作阵中筹码。', erlangEn:'You may hate my sect, but mortals cannot remain counters in an immortal feud.', allyNameZh:'云霄娘娘', allyNameEn:'Lady Yunxiao', allyZh:'今日我败于你守人的决心，不败于阐教名号。', allyEn:'I yield to your resolve to protect life—not to the name of your sect.' },
      { titleZh:'金鸡岭阻路', titleEn:'The Road at Jinjiling', zh:'孔宣一人镇住金鸡岭，五色神光尽收兵刃法宝。杨戬第一次遇到天眼也难以分类的力量。', en:'Kong Xuan alone holds Jinjiling, his five-colored radiance collecting every weapon and treasure. Even the Third Eye cannot easily classify it.', erlangZh:'五行之内皆可收，若我不用五行法宝呢？', erlangEn:'You capture all within the Five Phases. Then I will not rely on a Five-Phase treasure.', allyNameZh:'孔宣', allyNameEn:'Kong Xuan', allyZh:'聪明。但放下法宝之后，你还剩多少本事？', allyEn:'Clever. But when your treasures are gone, how much of you remains?' },
      { titleZh:'五光夺枪', titleEn:'Five Lights Seize the Spear', zh:'三尖两刃枪被神光牵引。杨戬以徒手玄功和哮天犬牵制，重新夺回兵刃。', en:'The divine radiance pulls at Erlang’s spear. He relies on bare-handed Mysteries and Xiaotianquan to reclaim it.', erlangZh:'兵刃离手，枪法仍在身上。', erlangEn:'The weapon can leave my hand; the spear art remains in my body.', allyNameZh:'哮天犬', allyNameEn:'Xiaotianquan', allyZh:'汪！我咬住他的影子，主人取枪！', allyEn:'Woof! I have his shadow—take the spear!' },
      { titleZh:'孔雀明王影', titleEn:'Shadow of the Peacock King', zh:'天眼照见孔宣神光背后的孔雀真形，也看见他并非商纣臣子，只为证明大道。', en:'The Third Eye reveals the peacock form behind Kong Xuan’s radiance—and that he serves no king, only his own proof of the Way.', erlangZh:'你不是为殷商，那便更不该拿士卒性命作论道代价。', erlangEn:'You do not fight for Shang. Then soldiers should not pay the price of your debate.', allyNameZh:'孔宣', allyNameEn:'Kong Xuan', allyZh:'若你的道能让我退岭，便由你证明。', allyEn:'If your Way can drive me from this ridge, prove it.' },
      { titleZh:'五色神光决', titleEn:'Duel of Five-Colored Radiance', zh:'杨戬不用法宝硬碰五光，而以天眼锁住光起之前的一念，近身展开枪术连段。', en:'Erlang does not contest the five lights with treasures. He locks onto the intention before they rise and closes in with chained spear arts.', erlangZh:'天眼不看光，看你决定放光的那一刻。', erlangEn:'The Third Eye watches not the light, but the moment you decide to release it.', allyNameZh:'孔宣', allyNameEn:'Kong Xuan', allyZh:'好！那就看看你能否快过一念五色！', allyEn:'Good! Let us see whether you can outrun a single five-colored thought!' },
      { titleZh:'梅山妖榜', titleEn:'The Demons of Mount Mei', zh:'梅山七怪各据山头，袁洪统率猿兵袭扰周军粮道。杨戬看见了一个与自己同样善变的对手。', en:'The Seven Demons occupy Mount Mei while Yuan Hong’s ape troops strike Zhou supply lines. Erlang sees an opponent as mutable as himself.', erlangZh:'同会变化，不代表同走一条路。', erlangEn:'Sharing transformations does not mean sharing a path.', allyNameZh:'姜子牙', allyNameEn:'Jiang Ziya', allyZh:'袁洪能识破寻常变化。此战只能由你亲自拆解。', allyEn:'Yuan Hong sees through ordinary transformations. Only you can unravel this contest.' },
      { titleZh:'白猿盗形', titleEn:'The White Ape Steals Form', zh:'袁洪化作杨戬模样混入军营。哮天犬没有看脸，而凭气息识出真假。', en:'Yuan Hong takes Erlang’s shape and infiltrates camp. Xiaotianquan ignores the face and recognizes the true scent.', erlangZh:'天眼能被骗一瞬，同行多年的伙伴不会。', erlangEn:'The Third Eye may be fooled for a moment. A lifelong companion will not.', allyNameZh:'哮天犬', allyNameEn:'Xiaotianquan', allyZh:'汪！假的身上只有妖山石气。', allyEn:'Woof! The false one carries only demon-mountain stone scent.' },
      { titleZh:'七十二变斗法', titleEn:'Duel of Transformations', zh:'鹰追雀、虎逐鹿、蛟缠蛇，两位玄功高手从云端斗到江底。', en:'Hawk pursues sparrow, tiger chases deer, dragon coils serpent—the two masters battle from cloud height to riverbed.', erlangZh:'变化再多，也会留下你想伤人的那一点杀意。', erlangEn:'However many forms you take, the intent to harm remains visible.', allyNameZh:'袁洪', allyNameEn:'Yuan Hong', allyZh:'你的天眼看得见杀意，可追得上我的七十二变吗？', allyEn:'Your eye may see intent, but can it catch my seventy-two changes?' },
      { titleZh:'山河社稷图', titleEn:'Map of Mountains and Rivers', zh:'女娲赐下山河社稷图。杨戬没有立刻困杀袁洪，而在图中逼他看见被猿兵破坏的村庄。', en:'Nüwa lends the Map of Mountains and Rivers. Erlang does not use it to kill Yuan Hong, but to show him villages ruined by his troops.', erlangZh:'你求自在，却让别人失去家园。这不是自由。', erlangEn:'You seek freedom by taking homes from others. That is not freedom.', allyNameZh:'袁洪', allyNameEn:'Yuan Hong', allyZh:'少用神图说教！胜了我的棍，再谈对错！', allyEn:'Do not preach through a divine map! Defeat my staff, then speak of right and wrong!' },
      { titleZh:'梅山白猿伏', titleEn:'The White Ape Subdued', zh:'袁洪显出白猿真身。八九玄功对七十二变的最后一战在梅山主峰展开。', en:'Yuan Hong reveals the white-ape form. Eight-Nine Mysteries and seventy-two changes meet in a final duel atop Mount Mei.', erlangZh:'我不杀你。败后约束猿兵，修复你们毁掉的山村。', erlangEn:'I will not kill you. Yield, restrain your troops, and rebuild what they destroyed.', allyNameZh:'袁洪', allyNameEn:'Yuan Hong', allyZh:'先让我看看，清源妙道真君凭什么约束白猿王！', allyEn:'First show me why the Lord of Clear-Origin Mysteries may command the White Ape King!' },
      { titleZh:'朝歌城下', titleEn:'Below Zhaoge', zh:'商军溃散，朝歌百姓却仍在城中。杨戬阻止胜军趁乱抢掠，让封神之战不以新的暴行结束。', en:'Shang’s army collapses while Zhaoge’s people remain inside. Erlang stops the victors from looting so the war does not end with fresh cruelty.', erlangZh:'城破不等于百姓有罪。收刀，开粮仓。', erlangEn:'A fallen city does not make its people guilty. Sheathe your blades and open the granaries.', allyNameZh:'武王姬发', allyNameEn:'King Wu of Zhou', allyZh:'依真君之言，先安民，再入宫。', allyEn:'As the True Lord commands: secure the people before entering the palace.' },
      { titleZh:'摘星楼火', titleEn:'Fire at the Star-Picking Tower', zh:'摘星楼燃起。杨戬以天眼搜寻被困宫人，而非追逐最后的军功。', en:'The Star-Picking Tower burns. Erlang uses the Third Eye to find trapped servants rather than chase final glory.', erlangZh:'哮天犬，逐层搜人。今日不让无名者死在结局里。', erlangEn:'Search every floor, Xiaotianquan. No nameless person dies merely because the story is ending.', allyNameZh:'哮天犬', allyNameEn:'Xiaotianquan', allyZh:'汪！东侧还有三人！', allyEn:'Woof! Three more on the eastern side!' },
      { titleZh:'封神台前', titleEn:'Before the Investiture Altar', zh:'姜子牙展开封神榜，战死众魂等待归位。杨戬看见敌我之名最终同列一榜。', en:'Jiang Ziya opens the Investiture Roll as the fallen await their offices. Erlang sees enemies and allies written upon the same scroll.', erlangZh:'生前各执一方，死后却同守天地。这场战争究竟是谁赢了？', erlangEn:'They fought on opposing sides, yet now guard one cosmos. Who truly won this war?', allyNameZh:'姜子牙', allyNameEn:'Jiang Ziya', allyZh:'封神能安置亡魂，却不能替活人回答战争是否值得。', allyEn:'Investiture can settle spirits. It cannot tell the living whether the war was worth its cost.' },
      { titleZh:'清源妙道归灌江', titleEn:'The Clear-Origin Lord Returns', zh:'杨戬不恋天庭高位，带哮天犬与梅山兄弟回到灌江口。从他的视角，封神榜不是胜利册，而是一份代价清单。', en:'Erlang refuses to cling to celestial rank and returns to Guanjiang with Xiaotianquan and the Mount Mei brothers. To him, the Investiture Roll is not a victory ledger but an account of cost.', erlangZh:'我仍会听调，却不听宣。若天命伤人，天眼便要再次睁开。', erlangEn:'I may answer a just summons, but I will not obey blind proclamation. When destiny harms people, the Third Eye will open again.', allyNameZh:'玉鼎真人', allyNameEn:'Master Yuding', allyZh:'你已走出自己的道。回灌江去，那里才是你的封神台。', allyEn:'You have found your own Way. Return to Guanjiang; that is your true altar of investiture.' }
    ];

    const ERLANG_CAMPAIGN_BOSSES = {
      12: { type:'fengshen_zhang_guifang' },
      20: { type:'fengshen_wen_zhong' },
      24: { type:'fengshen_yunxiao' },
      29: { type:'fengshen_kong_xuan' },
      34: { type:'fengshen_yuan_hong' }
    };

    // Erlang's cutscenes introduce each chapter, but none of them replace the
    // battle. Dialogue pauses the already-created wave; closing it always
    // releases enemies, including in Chapters 1 and 2.
    const ERLANG_STORY_ONLY_CHAPTERS = new Set();

    function getErlangCampaignDialogue(chapter) {
      const scene = ERLANG_FENGSHEN_CHAPTERS[chapter];
      if (!scene) return null;
      const bossConfig = ERLANG_CAMPAIGN_BOSSES[chapter];
      const bossType = bossConfig?.type;
      const bossDef = bossType ? ENEMY_TYPES[bossType] : null;
      return {
        bossName: bossDef ? uiText(bossDef.name, bossDef.nameEn || bossDef.name) : uiText(scene.allyNameZh, scene.allyNameEn),
        bossTitle: uiText(scene.titleZh, scene.titleEn),
        portraitKey: bossDef?.campaignSheet || 'erlang_player_actions',
        portraitRow: bossDef?.campaignRow || 0,
        portraitCols: bossDef ? 7 : 7,
        portraitRows: bossDef ? 5 : 5,
        isBattle: Boolean(bossConfig),
        onComplete: chapter === 38 ? 'journeyVictory' : null,
        dialogues: [
          { speaker:'erlang', name:uiText('二郎显圣真君 · 杨戬', 'Erlang Shen · Yang Jian'), text:uiText(scene.erlangZh, scene.erlangEn) },
          { speaker:bossConfig ? 'boss' : 'ally', name:uiText(scene.allyNameZh, scene.allyNameEn), text:uiText(scene.allyZh, scene.allyEn) }
        ]
      };
    }

    const STORY_ONLY_CHAPTERS = new Set([68, 86, 89, 100]);
    const LATE_CHAPTER_BEATS = {
      66: { zh: '悟空为金光寺蒙冤僧众扫塔，循血雨与失窃舍利追向碧波潭。', en: 'Wukong clears Golden-Ray Pagoda, vindicates its monks, and traces the stolen relic toward Emerald-Wave Pool.' },
      67: { zh: '悟空、八戒闹龙宫，与九头虫争夺佛宝舍利。', en: 'Wukong and Bajie storm the dragon court and confront the Nine-Headed Beast for the sacred relic.' },
      68: { zh: '荆棘岭木仙邀唐僧谈诗，杏仙以情挽留；悟空救师亦思妖怪是否皆应一棒打死。', en: 'Tree immortals invite Tang to debate poetry; Apricot Immortal asks him to remain, leaving Wukong to weigh mercy against danger.' },
      69: { zh: '黄眉假设小雷音寺，利用众人急于抵达终点之心，将师徒困入金铙。', en: 'Yellow Brows builds a false Thunderclap Temple and traps the pilgrims through their eagerness to believe the journey is over.' },
      70: { zh: '弥勒以瓜田设局，悟空入黄眉腹中破法，逼其交出人种袋。', en: 'Maitreya’s melon-field plan lets Wukong break Yellow Brows’ magic from within and recover the Human Seed Bag.' },
      71: { zh: '七绝山红鳞巨蟒断路，悟空锁其退路，八戒挥耙合击。', en: 'A giant red-scaled python blocks Qijue Mountain; Wukong pins its coils while Bajie joins the finishing assault.' },
      72: { zh: '悟空化身神医，以悬丝诊脉查出朱紫国王心病。', en: 'Wukong poses as a physician and diagnoses the Zhuzi king’s grief by a thread tied to his pulse.' },
      73: { zh: '乌金丹救醒国王，金圣宫娘娘被赛太岁掳走之事终于揭明。', en: 'The Wujin Elixir restores the king, revealing that Sai Tai Sui abducted the queen.' },
      74: { zh: '悟空潜入麒麟山，以变化计盗取能放火、烟、沙的紫金铃。', en: 'Wukong infiltrates Qilin Mountain and steals the Purple-Gold Bells of fire, smoke, and sand.' },
      75: { zh: '假铃对真铃，观音现身收回金毛犼，金圣宫娘娘得归故国。', en: 'False bells counter the true bells until Guanyin reclaims the Golden-Haired Hou and restores the queen.' },
      76: { zh: '太白金星警示万妖之国，悟空化作小钻风探查狮驼岭三魔。', en: 'Warned by the Evening Star, Wukong becomes Little Wind Cutter to scout Lion-Camel Ridge’s three demon kings.' },
      77: { zh: '黄花观百眼魔君放出千眼金光，悟空须在毒日轮转间寻找破绽。', en: 'The Hundred-Eyed Demon unleashes a poisonous golden sun, forcing Wukong to fight between its rotating rays.' },
      78: { zh: '狮驼洞战鼓齐鸣，四万七千妖兵封山，第一关青狮张开吞天巨口。', en: 'Forty-seven thousand demons seal the ridge as the Azure Lion opens a heaven-swallowing maw at the first gate.' },
      79: { zh: '悟空被青狮吞下，反从其腹中挥棒破开第一重妖阵。', en: 'Swallowed by the Azure Lion, Wukong turns the beast’s own body into the battleground.' },
      80: { zh: '黄牙老象以象鼻缚魂、巨足震岳守住第二关。', en: 'The White Elephant guards the second gate with a binding trunk and mountain-shaking stomps.' },
      81: { zh: '金翅大鹏振翼九万里，以阴阳羽刃封住天空与退路。', en: 'The Golden-Winged Great Peng seals the sky with impossible speed and Yin-Yang feather blades.' },
      82: { zh: '三魔败退，师徒释放狮驼国囚民，重整行装继续西行。', en: 'With the three kings broken, the fellowship frees Lion-Camel City’s captives and regroups.' },
      83: { zh: '比丘国千童被囚待取心肝，悟空誓揭穿国丈的长生骗局。', en: 'A thousand children await sacrifice in Bhikkhu Kingdom, and Wukong vows to expose the royal preceptor’s false immortality.' },
      84: { zh: '白鹿国丈借长生之名害童，南极寿星将在战后收回坐骑。', en: 'The White Deer hides child sacrifice behind promises of longevity; the Old Man of the South Pole comes to reclaim his mount.' },
      85: { zh: '黑松林雪地留下一串非人足迹，获救女子的身份越发可疑。', en: 'Tracks in Black-Pine Forest snow reveal that the rescued woman is no mortal.' },
      86: { zh: '灭法国王誓杀和尚，悟空一夜剃光满朝君臣，以笑破仇。', en: 'A king vows to kill monks; Wukong shaves the entire court overnight and overturns hatred through comic humiliation.' },
      87: { zh: '无底洞花烛迷局重重，金鼻白毛老鼠精以假身诱惑唐僧。', en: 'The White Mouse Spirit fills Bottomless Cave with bridal snares, false bodies, and golden needles.' },
      88: { zh: '悟空从牌位查出女妖与托塔天王、哪吒的因缘，逼天庭下界收伏。', en: 'Hidden ancestral tablets reveal the mouse spirit’s bond to Li Jing and Nezha, forcing Heaven to answer.' },
      89: { zh: '灭法国一夜剃城后君王悔过，师徒不战而过，留下笑谈。', en: 'The Monk-Destroying King repents after the city wakes shaved, and the pilgrims pass without bloodshed.' },
      90: { zh: '隐雾山南山大王用假人头瓦解师徒信念，火眼金睛须识破豹精真身。', en: 'The leopard king uses a false severed head to break the fellowship’s hope; Fiery Golden Eyes must find the real body.' },
      91: { zh: '凤仙郡大旱非棍棒可解，悟空促国王悔过、百姓行善，终于天降甘霖。', en: 'Fengxian’s drought cannot be beaten with a staff; repentance and good works finally bring rain.' },
      92: { zh: '玉华州三王子拜师，悟空、八戒、沙僧第一次成为传法者。', en: 'Three princes take the disciples as teachers, turning former pupils into masters.' },
      93: { zh: '黄狮精盗走三件神兵开钉耙盛会，师兄弟乔装入寨夺兵。', en: 'Yellow Lion steals the pilgrims’ weapons for a grand feast, prompting a disguised counter-raid.' },
      94: { zh: '九灵元圣为徒孙复仇，九口齐开，竹节山群狮尽出。', en: 'Nine-Spirit Primordial Sage avenges his descendant as nine mouths roar across Bamboo-Joint Mountain.' },
      95: { zh: '金平府灯节三犀假扮佛爷享用香油，并趁乱掳走唐僧。', en: 'Three rhino kings pose as Buddhas, consume the city’s lamp oil, and seize Tang during the festival.' },
      96: { zh: '辟寒、辟暑、辟尘三王结成寒暑尘连环阵，必须逐角破盾。', en: 'The Cold-, Heat-, and Dust-Averting Rhino Kings combine three domains behind a shared formation.' },
      97: { zh: '天竺假公主抛绣球选中唐僧，悟空察觉宫中月气异常。', en: 'A false princess chooses Tang with an embroidered ball, while Wukong senses lunar magic in the palace.' },
      98: { zh: '真公主梦兆与寺中哭诉相合，月镜逐一照破玉兔替身。', en: 'The true princess’s testimony aligns with a prophetic dream, and moon mirrors expose the Jade Rabbit impostor.' },
      99: { zh: '玉兔以捣药玉杵引满月之力，悟空迎战取经路最后一位妖王。', en: 'The Jade Rabbit raises a full-moon domain with her jade pestle—the pilgrimage’s final demon duel.' },
      100: { zh: '凌云渡脱去凡胎，取得真经；老鼋翻舟补足第八十一难，五圣归长安成真。', en: 'At Cloud-Crossing Ferry the pilgrims shed mortality, receive the scriptures, endure the White Turtle’s final ordeal, and return in triumph.' }
    };

    const CAMPAIGN_BOSSES = {
      5:  { type: 'campaign_monkey_chief' },
      12: { type: 'campaign_yuanshi' },
      18: { type: 'campaign_dragon_king' },
      22: { type: 'campaign_nezha' },
      24: { type: 'campaign_king_chiguo' },
      25: { type: 'campaign_king_zengzhang' },
      26: { type: 'campaign_king_guangmu' },
      27: { type: 'campaign_king_duowen' },
      29: { type: 'campaign_erlang' },
      32: { type: 'campaign_buddha' },
      36: { type: 'campaign_zhubajie' },
      40: { type: 'campaign_shawujing' },
      45: { type: 'campaign_baigujing' },
      50: { type: 'campaign_spider_queen' },
      55: { type: 'campaign_bull_king' },
      60: { type: 'campaign_red_boy' },
      65: { type: 'campaign_iron_fan' },
      67: { type: 'campaign_nine_headed_beast' },
      70: { type: 'campaign_yellow_brows' },
      71: { type: 'campaign_giant_python' },
      75: { type: 'campaign_sai_taisui' },
      77: { type: 'campaign_hundred_eyed' },
      79: { type: 'campaign_azure_lion' },
      80: { type: 'campaign_white_elephant' },
      81: { type: 'campaign_golden_peng' },
      84: { type: 'campaign_white_deer' },
      87: { type: 'campaign_white_mouse' },
      90: { type: 'campaign_leopard_king' },
      93: { type: 'campaign_yellow_lion' },
      94: { type: 'campaign_nine_spirit' },
      96: { types: ['campaign_rhino_cold', 'campaign_rhino_heat', 'campaign_rhino_dust'] },
      99: { type: 'campaign_jade_rabbit' }
    };

    function outcomeStory(storyZh, storyEn, goodZh, goodEn, neutralZh, neutralEn, evilZh, evilEn, costZh, costEn) {
      return {
        storyZh, storyEn,
        good: { titleZh:goodZh, titleEn:goodEn, descZh:'护生并遵循取经正果。首领存活，因果 +1。', descEn:'Preserve life and honor the pilgrimage’s rightful lesson. The boss lives; alignment +1.' },
        neutral: { titleZh:neutralZh, titleEn:neutralEn, descZh:'封印、立契或放逐，不取性命，因果不变。', descEn:'Seal, bind, or banish without taking a life. Alignment does not move.' },
        evil: { titleZh:evilZh, titleEn:evilEn, descZh:`吸收其真炁而不杀死对手。${costZh} 因果 −1。`, descEn:`Absorb the boss’s zhen qi without killing them. ${costEn} Alignment −1.` }
      };
    }

    const BOSS_OUTCOME_STORIES = {
      5: outcomeStory('花果山老猿以败阵承认石猴有资格统领群猴。', 'The Elder Ape Chief yields and accepts the Stone Monkey’s right to lead Flower-Fruit Mountain.', '礼敬老猿，立为护山长老', 'Honor him as guardian elder', '立下不伤群猴的山盟', 'Bind him by a mountain oath', '夺其山脉真炁', 'Drain his mountain-vein qi', '群猴今后少一位守山者。', 'The monkey clan loses one of its protectors.'),
      12: outcomeStory('元始天尊试尽悟空根骨，问他将以何心驾驭变化。', 'Yuanshi Tianzun has tested Wukong’s nature and asks what heart will govern his transformations.', '执弟子礼，受玉清戒言', 'Bow and accept Jade-Purity counsel', '携变化法门各走其道', 'Take the doctrine and part as equals', '强摄玉清道炁', 'Seize Jade-Purity qi', '昆仑门人的护山道炁因此衰弱。', 'The disciples’ mountain wards are weakened.'),
      18: outcomeStory('东海龙王守着定海神珍与龙宫百姓，终于承认神铁已经择主。', 'The Dragon King protects both the Sea-Calming Treasure and his people, but admits the iron has chosen its master.', '立约护海，正取金箍棒', 'Swear to protect the sea and claim Ruyi', '封住宫门，留下互不侵犯契', 'Seal the palace under a truce', '掠取龙宫宝炁', 'Plunder Dragon-Palace treasure qi', '海族要以自身灵力修补被夺的宝库。', 'The sea folk must spend their own spirit to repair the treasury.'),
      22: outcomeStory('哪吒收起火尖枪，仍以天庭军礼等待悟空的答复。', 'Nezha lowers the Fire-Tip Spear and awaits Wukong’s answer with celestial military honor.', '敬莲身不屈，止战为友', 'Honor his lotus body and end as friends', '约定日后再较高下', 'Call a truce and promise a rematch', '摄取风火轮真炁', 'Siphon Wind-Fire Wheel qi', '哪吒仍活着，却要耗费百日重炼双轮。', 'Nezha lives, but must spend a hundred days restoring the wheels.'),
      24: outcomeStory('持国天王的碧玉琵琶弦断一根，东方天门暂失天音。', 'One string of King Chiguo’s jade pipa has broken, and the eastern gate falls silent.', '助他续弦，归还天音', 'Restore the string and celestial music', '封琴放逐，留他性命', 'Seal the pipa and banish him', '吸尽琵琶音炁', 'Absorb the pipa’s sound qi', '东方天门失去安魂乐，守军心神不宁。', 'The eastern gate loses its calming music.'),
      25: outcomeStory('增长天王青锋倒插云台，烈火已经熄灭。', 'King Zengzhang plants his green sword in the cloud terrace and its flame gutters out.', '归还青锋，护持南门', 'Return the sword to guard the south', '封剑百年', 'Seal the sword for a century', '吞纳剑中风火', 'Consume the sword’s wind-fire qi', '南天门的烈风屏障随之变薄。', 'The southern gate’s wind barrier thins.'),
      26: outcomeStory('广目天王的天龙伏地，等待主人和悟空决定去留。', 'King Guangmu’s celestial dragon lies subdued, awaiting judgment beside its master.', '释放天龙，止息仇怨', 'Release the dragon and end the feud', '封住龙目，逐出战场', 'Seal the dragon eye and banish both', '夺取龙目精炁', 'Take the dragon-eye essence', '天龙仍生，却暂时失去护卫西门的目力。', 'The dragon lives but temporarily loses the sight that guards the west.'),
      27: outcomeStory('多闻天王收拢宝伞，北门塔影不再压向悟空。', 'King Duowen folds his sacred umbrella, and the northern pagoda-shadow recedes.', '还伞守门，止戈', 'Return the umbrella and end hostilities', '封塔放逐天王', 'Seal the pagoda and banish him', '夺伞中宝炁', 'Steal the umbrella’s treasure qi', '北门百姓失去遮蔽天火的宝伞。', 'Those below the north gate lose protection from celestial fire.'),
      29: outcomeStory('二郎神天眼微合，承认这场较量已经分出高下。', 'Erlang Shen closes his Third Eye and concedes that the contest is decided.', '敬重知己，互称兄弟', 'Honor a worthy rival as a brother', '立下灌江口停战契', 'Bind a Guanjiang truce', '吸取天眼神炁', 'Absorb Third-Eye qi', '灌江口的妖患将趁天眼衰弱而起。', 'Demons near Guanjiang will exploit the weakened Third Eye.'),
      32: outcomeStory('如来以五指成山，却也让悟空在镇压前选择如何看待这场败局。', 'Buddha’s five fingers become a mountain, yet Wukong may choose what lesson to carry into confinement.', '受五百年风雨而无怨', 'Accept five hundred years without resentment', '记住界限，不敬不恨', 'Accept the boundary without devotion or hatred', '私藏一缕佛光真炁', 'Hoard a thread of Buddha-light qi', '这缕佛光原本会照亮五行山下的生灵。', 'That light would otherwise have warmed the lives beneath the mountain.'),
      36: outcomeStory('猪八戒恢复天蓬记忆，也想起高老庄与自己的过错。', 'Zhu Bajie remembers Marshal Tianpeng, Gao Village, and the harm caused by his appetites.', '邀他护送唐僧赎过', 'Invite him to atone on the pilgrimage', '以紧箍誓约约束同行', 'Bind him to the road by oath', '吸取天蓬元炁', 'Drain Tianpeng’s primordial qi', '高老庄要独自承担余下妖患。', 'Gao Village must face the remaining demons alone.'),
      40: outcomeStory('沙悟净放下降妖宝杖，流沙河中九个取经人骷髅浮出水面。', 'Sha Wujing lowers his staff as the nine pilgrim skulls rise from the Flowing-Sands River.', '超度亡魂，收他为徒弟', 'Release the souls and accept him as a disciple', '封河立誓，令他守渡口', 'Bind him to guard the crossing', '摄取骷髅项链真炁', 'Absorb the skull-necklace qi', '流沙河失去镇水之力，沿岸将受枯潮。', 'The river loses its stabilizing power and its banks face drought.'),
      45: outcomeStory('白骨夫人的三具化身尽散，岭中被困魂魄仍在哭泣。', 'Lady White Bone’s disguises have fallen, while trapped souls still cry across the ridge.', '释放亡魂，令她入轮回', 'Release the souls and send her to rebirth', '封骨于岭，永不得近人', 'Seal her bones away from mortals', '吸收白骨阴炁', 'Absorb her bone-yin qi', '她不死，但村民的亡魂继续困在岭中。', 'She lives, but the villagers’ souls remain trapped.'),
      50: outcomeStory('盘丝洞蛛网松开，七情泉与被缚旅人都等待处置。', 'The Webbed Hollow loosens its threads; captives and the Seven-Emotion Springs await judgment.', '救出旅人，净化毒泉', 'Free the captives and cleanse the springs', '封洞放逐蛛后', 'Seal the cave and banish the queen', '收割万丝毒炁', 'Harvest ten-thousand-thread venom qi', '毒泉会继续侵入附近村井。', 'Venom continues seeping into nearby wells.'),
      55: outcomeStory('牛魔王想起七大圣结义，也看见妻儿因争执而受苦。', 'The Bull Demon King remembers the Seven Sages’ brotherhood and sees the cost borne by his family.', '重续兄弟情，归还芭蕉扇', 'Restore brotherhood and return the fan', '逐离积雷山，停战百年', 'Exile him from Mount Thunder for a century', '夺取积雷山地脉', 'Seize Mount Thunder’s earth veins', '山中生灵失去滋养，翠云山也会枯黄。', 'Mountain life loses its nourishment and Emerald-Cloud Mountain withers.'),
      60: outcomeStory('红孩儿的三昧真火熄成一点火种，仍倔强地护在胸前。', 'Red Boy’s Samadhi Fire shrinks to one ember, still guarded defiantly at his chest.', '交予观音，修成善财童子', 'Entrust him to Guanyin as Sudhana', '封住火种，遣返火云洞', 'Seal the ember and send him home', '吸尽三昧火真炁', 'Absorb the Samadhi-Fire qi', '火焰不伤红孩儿性命，却使周边土地连年干旱。', 'Red Boy survives, but the surrounding land suffers drought.'),
      65: outcomeStory('铁扇公主收起芭蕉扇，火焰山百姓仍被烈火阻断西行。', 'Princess Iron Fan lowers the Plantain Fan while the people remain trapped behind Flaming Mountain.', '化解家怨，借扇灭火', 'Reconcile the family and borrow the fan', '强立借扇契，事后归还', 'Compel a loan, then return the fan', '盗取芭蕉扇本源', 'Steal the fan’s primal qi', '翠云洞根基受损，百姓灭火也更加艰难。', 'Emerald-Cloud Cave is damaged and the people struggle to quench the mountain.'),
      67: outcomeStory('九头虫吐出祭赛国佛宝，碧波潭的血雨终于停止。', 'The Nine-Headed Beast releases Jisai Kingdom’s relic and the blood-rain over Emerald-Wave Pool stops.', '归还佛宝，放他远遁', 'Return the relic and let him flee', '封入碧波潭底', 'Seal him beneath Emerald-Wave Pool', '吸收佛宝残光与九首炁', 'Absorb relic-light and nine-head qi', '祭赛国宝塔将多年无光。', 'Jisai’s pagoda remains dark for years.'),
      70: outcomeStory('黄眉大王的人种袋打开，被困神将与百姓仍在其中挣扎。', 'Yellow Brows’ Human Seed Bag opens while captives struggle inside.', '放出众生，交还弥勒', 'Free all captives and return him to Maitreya', '封铙封袋，放逐黄眉', 'Seal cymbals and bag, then banish him', '吞纳人种袋真炁', 'Absorb the Human Seed Bag’s qi', '袋中众生要承受更久的黑暗才能脱困。', 'The captives remain in darkness longer before escaping.'),
      71: outcomeStory('七绝山大蟒盘成一圈，污秽山路仍需有人清理。', 'The great python coils in surrender while Qijue’s poisoned road still needs cleansing.', '净化山路，放蛇归林', 'Cleanse the road and release the serpent', '封牙放逐荒山', 'Seal its fangs and exile it', '吸尽赤鳞毒炁', 'Drain its red-scale venom qi', '毒秽留在七绝山，后来旅人仍会受害。', 'The poison remains to harm later travelers.'),
      75: outcomeStory('赛太岁三枚紫金铃落地，朱紫国王后仍在等待解救。', 'Sai Tai Sui’s three purple-gold bells fall as the queen of Zhuzi waits for rescue.', '救回王后，送坐骑归观音', 'Rescue the queen and return the mount to Guanyin', '没收三铃，逐出朱紫国', 'Confiscate the bells and banish him', '吸收三铃风火烟炁', 'Absorb the bells’ wind-fire-smoke qi', '朱紫国上空将残留多年毒烟。', 'Poison smoke lingers over Zhuzi for years.'),
      77: outcomeStory('百眼魔君收拢千眼金光，黄花观毒日仍灼烧山谷。', 'The Hundred-Eyed Demon closes his golden eyes while the poison sun still burns the valley.', '请毗蓝婆收服并解毒', 'Entrust him to Pilanpo and cure the poison', '封千眼，放逐西荒', 'Seal his eyes and banish him west', '吞噬千眼日炁', 'Consume the thousand-eye solar qi', '毒日余光会继续灼伤山民。', 'The poisoned afterglow continues harming villagers.'),
      79: outcomeStory('青狮张开的吞天巨口合拢，狮驼岭囚徒终于能呼吸。', 'The Azure Lion closes his heaven-swallowing maw and Lion-Camel’s captives can breathe.', '释放囚徒，交还文殊', 'Free captives and return him to Manjusri', '封口放逐狮驼岭', 'Seal his maw and banish him', '夺取吞天狮吼真炁', 'Take the heaven-swallowing roar qi', '囚徒的生气也被一并抽走。', 'The captives lose part of their own vitality.'),
      80: outcomeStory('白象放下长鼻与兵刃，震裂的村田仍在下沉。', 'The White Elephant lowers trunk and weapon while shattered fields continue sinking.', '修复村田，交还普贤', 'Repair the fields and return him to Samantabhadra', '缚鼻放逐', 'Bind his trunk and banish him', '吸取黄牙地炁', 'Absorb Yellow-Tusk earth qi', '土地失去地炁，庄稼数年难生。', 'The soil loses its qi and crops fail for years.'),
      81: outcomeStory('金翅大鹏折翼落地，狮驼国上空终于露出天光。', 'The Golden Peng folds his wings and daylight returns over Lion-Camel Kingdom.', '放出城民，交予如来约束', 'Free the city and submit him to Buddha', '封翼逐往极西', 'Seal his wings and exile him west', '夺取阴阳羽翼精炁', 'Steal the yin-yang wing essence', '城中风脉被一同抽空，归乡者步履艰难。', 'The city’s wind veins are drained and survivors struggle home.'),
      84: outcomeStory('白鹿国丈的寿杖断裂，比丘国被选中的孩童仍在宫中。', 'The White Deer Preceptor’s longevity staff breaks while chosen children remain in the palace.', '救出孩童，送白鹿归寿星', 'Save the children and return the deer to the Longevity Star', '封角放逐，比丘国自理', 'Seal his antlers and leave the kingdom to recover', '夺取长生鹿炁', 'Take the deer’s longevity qi', '孩童本可得到的寿元被悟空占去。', 'Wukong takes longevity that could have restored the children.'),
      87: outcomeStory('金鼻白毛老鼠精放下双刃，无底洞地脉仍绑着唐僧。', 'The Golden-Nosed White Mouse lowers her blades while Bottomless Cave still binds Tang.', '解开地脉，交还李靖哪吒', 'Release the earth veins and return her to Li Jing and Nezha', '封洞逐往幽州', 'Seal the cave and banish her north', '吸收地涌金针炁', 'Absorb burrow and golden-needle qi', '无底洞附近井泉将逐渐干枯。', 'Wells around Bottomless Cave slowly dry up.'),
      90: outcomeStory('南山大王散去假唐僧头颅的迷雾，隐雾山旅人仍迷失其中。', 'The Southern Mountain King disperses the false-head illusion while travelers remain lost in Hidden-Mist Mountain.', '救出旅人，令豹王守路赎罪', 'Rescue travelers and make him guard the road', '驱离隐雾山', 'Banish him from Hidden-Mist Mountain', '吞取隐雾幻炁', 'Consume the hidden-mist illusion qi', '旅人仍要在无雾却无路标的山中受困。', 'Travelers remain stranded without the mist’s old landmarks.'),
      93: outcomeStory('黄狮精交出三件神兵，玉华州王子终于能取回师门兵器。', 'The Yellow Lion returns the three weapons so Yuhua’s princes may reclaim their training arms.', '归还神兵，宽恕爱兵之过', 'Return the weapons and forgive his obsession', '封兵宴，令其远走', 'End the weapon feast and exile him', '吸取三神兵灵炁', 'Absorb the three weapons’ spirit qi', '王子们取回的只剩失去灵性的空兵。', 'The princes receive weapons stripped of their spirit.'),
      94: outcomeStory('九灵元圣收住九口，竹节山群狮也随之伏地。', 'Nine-Spirit Primordial Sage closes his nine mouths and the lions of Bamboo-Joint Mountain yield.', '止群狮，送还太乙救苦天尊', 'Spare the lions and return him to Taiyi', '封九口，放逐天外', 'Seal nine mouths and banish him', '吸纳九灵吼炁', 'Absorb the ninefold roar qi', '竹节山失去镇山灵音，群兽四散。', 'Bamboo-Joint Mountain loses its guardian voice and beasts scatter.'),
      96: outcomeStory('辟寒、辟暑、辟尘三犀同时伏地，金平府灯油与三界天气都受其妖炁牵连。', 'The Cold-, Heat-, and Dust-Averting Rhino Kings yield together; Jinping’s lamp oil and weather remain bound to their qi.', '归还香油，交由天庭收伏三犀', 'Return the oil and hand all three to Heaven', '封角逐出金平府', 'Seal their horns and banish them', '吸尽寒暑尘三炁', 'Absorb cold, heat, and dust qi', '金平府将遭遇失序的寒潮、热浪与沙尘。', 'Jinping suffers disordered cold, heat, and dust storms.'),
      99: outcomeStory('玉兔精放下捣药玉杵，真正的天竺公主仍等待恢复身份。', 'The Jade Rabbit lowers her pestle while Tianzhu’s true princess awaits restoration.', '救回公主，送玉兔归广寒宫', 'Restore the princess and return the rabbit to the Moon Palace', '封玉杵，逐回月宫', 'Seal the pestle and banish her to the moon', '吸取广寒月炁', 'Absorb Moon-Palace lunar qi', '公主的月镜与一方夜色都会黯淡。', 'The princess’s moon mirror and the kingdom’s nights grow dim.' )
    };

    const ERLANG_BOSS_OUTCOME_STORIES = {
      12: outcomeStory('张桂芳魂幡尽落，却仍坚持忠于殷商军民。', 'Zhang Guifang’s soul banners fall, yet his loyalty to Shang’s soldiers and people remains.', '释放军魂，准其护送伤兵撤退', 'Release the souls and let him escort the wounded', '封住落魂术，令其离开西岐', 'Seal the soul art and banish him from Xiqi', '吸收魂幡真炁', 'Absorb the soul-banner qi', '失去魂幡镇护的伤兵更难平安返乡。', 'Without the banners’ protection, wounded soldiers struggle to return home.'),
      20: outcomeStory('闻仲双鞭落地，仍请求先让两军伤员离开绝龙岭。', 'Wen Zhong’s twin whips fall, and he asks only that both armies’ wounded leave Juelong Ridge first.', '敬忠臣之志，护送伤员撤离', 'Honor his loyalty and escort the wounded', '封雷鞭，令其退回朝歌', 'Seal the whips and order a retreat to Zhaoge', '吸收雷部正炁', 'Absorb orthodox thunder qi', '雷部护持消散，山道中的伤兵将受雷雨侵袭。', 'Without thunder protection, wounded soldiers suffer the storm.'),
      24: outcomeStory('九曲黄河阵停转，云霄仍要求阐教正视赵公明之死。', 'The Yellow River Array stops, but Yunxiao still demands that the Chan sect answer for Zhao Gongming’s death.', '允她带走兄长遗物并救治阵中人', 'Let her take her brother’s relics and heal the array’s victims', '封存混元金斗，立下停战契', 'Seal the Gold Dipper under a truce', '吸收金斗混元炁', 'Absorb the dipper’s primordial qi', '被削去修为的仙人将失去恢复根基的机会。', 'Those stripped of cultivation lose their chance to recover.'),
      29: outcomeStory('孔宣收起五色神光，承认杨戬不用法宝也守住了自己的道。', 'Kong Xuan withdraws the five-colored light, acknowledging that Erlang held to his Way without treasures.', '止战论道，放其离开金鸡岭', 'End the duel and let him leave Jinjiling', '封住五光，逐往西方', 'Seal the five lights and banish him west', '吸收五行神光', 'Absorb the five-phase radiance', '金鸡岭五行地脉随之失衡。', 'Jinjiling’s five elemental veins fall out of balance.'),
      34: outcomeStory('袁洪显出白猿真身，梅山猿兵与被毁村落都在等待结果。', 'Yuan Hong reveals his white-ape form while his troops and the ruined villages await judgment.', '令其率猿兵重建村落', 'Make him lead the ape troops in rebuilding', '封住变化，逐离梅山十年', 'Seal his transformations and exile him for ten years', '吸收七十二变妖炁', 'Absorb the qi of seventy-two changes', '失去妖炁的梅山林木与村落都更难复苏。', 'Without that mountain qi, both forests and villages recover more slowly.')
    };

    const BOSS_OUTCOME_INPUT_DELAY_MS = 1500;
    let pendingBossOutcomeGroup = [];
    let bossOutcomeUnlockAt = 0;
    let bossOutcomeUnlockTimer = null;

    function setBossOutcomeChoicesLocked(locked) {
      ['good','neutral','evil'].forEach(choice => {
        const button = document.getElementById(`outcome-${choice}`);
        button.disabled = locked;
        button.setAttribute('aria-disabled', locked ? 'true' : 'false');
      });
    }

    function refreshBossOutcomeInputLock() {
      const status = document.getElementById('boss-outcome-lock');
      const remainingMs = Math.max(0, bossOutcomeUnlockAt - performance.now());
      if (remainingMs > 0) {
        setBossOutcomeChoicesLocked(true);
        status.classList.remove('ready');
        status.innerText = uiText(
          `请先阅读剧情 · ${Math.ceil(remainingMs / 100) / 10} 秒后可选择`,
          `Please read the story · choices unlock in ${(Math.ceil(remainingMs / 100) / 10).toFixed(1)}s`
        );
        return false;
      }
      if (bossOutcomeUnlockTimer) window.clearInterval(bossOutcomeUnlockTimer);
      bossOutcomeUnlockTimer = null;
      setBossOutcomeChoicesLocked(false);
      status.classList.add('ready');
      status.innerText = uiText('选项已开放 · 请慎重决定', 'Choices unlocked · make a deliberate decision');
      return true;
    }

    function queueBossOutcomeIfBattleEnded() {
      if (gameState.bossOutcomeActive || gameState.dialogueActive) return;
      const activeBoss = enemies.some(enemy => enemy.isBoss && enemy.alive && !enemy.isSubdued);
      if (activeBoss) return;
      const subdued = enemies.filter(enemy => enemy.isBoss && enemy.alive && enemy.isSubdued && !enemy.outcomeResolved);
      if (subdued.length) openBossOutcomeChoice(subdued);
    }

    function openBossOutcomeChoice(bosses) {
      if (!bosses?.length || gameState.bossOutcomeActive) return;
      pendingBossOutcomeGroup = [...bosses];
      gameState.bossOutcomeActive = true;
      gameState.isPaused = true;
      clearHeldCombatInputs();
      projectiles = [];
      const chapter = gameState.chamberIndex;
      const routeOutcomes = gameState.campaignRoute === 'fengshen' ? ERLANG_BOSS_OUTCOME_STORIES : BOSS_OUTCOME_STORIES;
      const data = routeOutcomes[chapter] || outcomeStory(
        gameState.campaignRoute === 'fengshen' ? '首领已经败服，但仍然活着。杨戬必须决定如何结束这场争斗。' : '首领已经败服，但仍然活着。悟空必须决定如何结束这场争斗。',
        gameState.campaignRoute === 'fengshen' ? 'The boss is subdued but alive. Erlang must decide how this conflict ends.' : 'The boss is subdued but alive. Wukong must decide how this conflict ends.',
        '宽恕并救治', 'Spare and tend their wounds', '封印后放逐', 'Seal and banish', '吸取真炁', 'Absorb zhen qi',
        '附近生灵要承受灵脉衰弱。', 'Nearby lives suffer from the weakened spirit vein.'
      );
      const names = bosses.map(boss => boss.name).join(gameState.language === 'en' ? ', ' : '、');
      document.getElementById('boss-outcome-title').innerText = uiText(`首领已经伏地 · 决定${names}的命运`, `Boss Subdued · Decide the fate of ${names}`);
      document.getElementById('boss-outcome-subtitle').innerText = uiText('三种结局都不杀死首领 · 此选择永久保存', 'No outcome kills the boss · This choice is saved permanently');
      document.getElementById('boss-outcome-story').innerText = gameState.language === 'en' ? data.storyEn : data.storyZh;
      ['good','neutral','evil'].forEach(choice => {
        const item = data[choice];
        const delta = choice === 'good' ? '+1 GOOD' : (choice === 'evil' ? '−1 EVIL' : '±0 NEUTRAL');
        document.getElementById(`outcome-${choice}`).innerHTML = `<strong>${choice === 'good' ? '🪽' : (choice === 'evil' ? '🔻' : '☯️')} ${gameState.language === 'en' ? item.titleEn : item.titleZh}</strong>${gameState.language === 'en' ? item.descEn : item.descZh}<small>${delta}</small>`;
      });
      if (bossOutcomeUnlockTimer) window.clearInterval(bossOutcomeUnlockTimer);
      bossOutcomeUnlockAt = performance.now() + BOSS_OUTCOME_INPUT_DELAY_MS;
      setBossOutcomeChoicesLocked(true);
      document.getElementById('boss-outcome-modal').style.display = 'flex';
      document.getElementById('boss-outcome-title').focus({ preventScroll: true });
      refreshBossOutcomeInputLock();
      bossOutcomeUnlockTimer = window.setInterval(refreshBossOutcomeInputLock, 100);
    }

    function resolveBossOutcome(choice) {
      if (!gameState.bossOutcomeActive || !['good','neutral','evil'].includes(choice)) return;
      if (performance.now() < bossOutcomeUnlockAt || !refreshBossOutcomeInputLock()) return;
      if (bossOutcomeUnlockTimer) window.clearInterval(bossOutcomeUnlockTimer);
      bossOutcomeUnlockTimer = null;
      bossOutcomeUnlockAt = 0;
      setBossOutcomeChoicesLocked(true);
      const oldScore = alignmentScore;
      const hpRatio = player.maxHp > 0 ? player.hp / player.maxHp : 1;
      const qiRatio = player.maxQi > 0 ? player.qi / player.maxQi : 1;
      if (choice === 'good') {
        alignmentScore = Math.min(100, alignmentScore + 1);
        player.hp = Math.min(player.maxHp, player.hp + player.maxHp * (.12 + (player.alignmentEffects?.mercyHeal || 0)));
        player.alignmentBarrier = Math.max(player.alignmentBarrier || 0, 45);
      } else if (choice === 'evil') {
        alignmentScore = Math.max(-100, alignmentScore - 1);
        player.absorbedBossQi = (player.absorbedBossQi || 0) + pendingBossOutcomeGroup.length;
        player.qi = player.maxQi;
        gameState.gold += 80 * pendingBossOutcomeGroup.length;
      } else {
        player.hp = Math.min(player.maxHp, player.hp + player.maxHp * .06);
        player.qi = Math.min(player.maxQi, player.qi + player.maxQi * .20);
      }

      pendingBossOutcomeGroup.forEach(boss => {
        boss.outcomeResolved = true;
        boss.isSubdued = false;
        boss.alive = false;
        boss.isDying = false;
        boss.hp = 1;
        gameState.enemiesKilled++;
        gameState.gold += 120;
        gameState.ashes += choice === 'evil' ? 72 : (choice === 'good' ? 64 : 60);
        fxList.push(new HadesMagicCircleAOEFX(boss.x, boss.y, 92, .65, choice === 'good' ? '#93c5fd' : (choice === 'evil' ? '#a855f7' : '#facc15')));
        fxList.push(new Shockwave(boss.x, boss.y, 120, choice === 'good' ? '#dbeafe' : (choice === 'evil' ? '#ef4444' : '#facc15')));
      });
      pendingBossOutcomeGroup = [];
      player.applyMetaUpgrades();
      player.hp = Math.max(1, Math.min(player.maxHp, player.hp || player.maxHp * hpRatio));
      player.qi = Math.min(player.maxQi, Math.max(player.qi || player.maxQi * qiRatio, 0));
      player.armor = Math.max(player.armor || 0, player.baseArmor || 0);
      saveMetaProgress();
      updateHUD();
      document.getElementById('boss-outcome-modal').style.display = 'none';
      gameState.bossOutcomeActive = false;
      const continuation = gameState.bossOutcomeContinuation;
      gameState.bossOutcomeContinuation = null;
      player.invulnTimer = Math.max(player.invulnTimer, 1.2);
      sound.playJadeChime();
      floatingTexts.push(new FloatingText(player.x, player.y - 62,
        uiText(`因果 ${oldScore} → ${alignmentScore} · 首领存活`, `Alignment ${oldScore} → ${alignmentScore} · Boss spared`),
        choice === 'good' ? '#93c5fd' : (choice === 'evil' ? '#c084fc' : '#facc15'), 19));
      if (typeof continuation === 'function') {
        continuation();
      } else {
        gameState.isPaused = false;
        checkChamberClear();
      }
    }

    const CAMPAIGN_BOSS_PROFILES = {
      fengshen_zhang_guifang: { color:'#22d3ee', mobility:'teleport', pattern:'fan', projectiles:6, projectileSpeed:365, aoeRadius:260, rangedDamage:30, aoeDamage:48, rangedZh:'点名落魂枪', rangedEn:'Name-Calling Soul Spears', aoeZh:'幽魂战幡阵', aoeEn:'Soul-Banner Formation' },
      fengshen_wen_zhong: { color:'#fbbf24', mobility:'leap', pattern:'spiral', projectiles:9, projectileSpeed:390, aoeRadius:295, rangedDamage:34, aoeDamage:56, rangedZh:'雌雄雷鞭', rangedEn:'Twin Thunder Whips', aoeZh:'雷部正法界', aoeEn:'Orthodox Thunder Domain' },
      fengshen_yunxiao: { color:'#fde68a', mobility:'fly', pattern:'ring', projectiles:10, projectileSpeed:350, aoeRadius:310, rangedDamage:35, aoeDamage:58, rangedZh:'混元金斗光', rangedEn:'Primordial Gold-Dipper Rays', aoeZh:'九曲黄河阵', aoeEn:'Nine-Bend Yellow River Array' },
      fengshen_kong_xuan: { color:'#e879f9', mobility:'fly', pattern:'fan', projectiles:10, projectileSpeed:430, aoeRadius:300, rangedDamage:38, aoeDamage:62, rangedZh:'五色神光', rangedEn:'Five-Colored Divine Light', aoeZh:'孔雀明王轮', aoeEn:'Peacock-King Radiance' },
      fengshen_yuan_hong: { color:'#fb7185', mobility:'leap', pattern:'spiral', projectiles:8, projectileSpeed:410, aoeRadius:315, rangedDamage:40, aoeDamage:66, rangedZh:'七十二变妖兵', rangedEn:'Seventy-Two-Change Assault', aoeZh:'梅山白猿震岳', aoeEn:'Mount-Mei Ape Quake' },
      campaign_monkey_chief: { color: '#84cc16', mobility: 'leap', projectiles: 3, aoeRadius: 210, rangedDamage: 20, aoeDamage: 34, rangedZh: '山石连掷', rangedEn: 'Mountain-Stone Volley', aoeZh: '群猴王啸', aoeEn: 'Ape-King Roar' },
      campaign_yuanshi: { color: '#c084fc', mobility: 'teleport', projectiles: 7, aoeRadius: 270, rangedDamage: 24, aoeDamage: 40, rangedZh: '玉清道炁', rangedEn: 'Jade-Purity Bolts', aoeZh: '太极开天阵', aoeEn: 'Primordial Taiji Array' },
      campaign_dragon_king: { color: '#22d3ee', mobility: 'fly', projectiles: 5, aoeRadius: 260, rangedDamage: 23, aoeDamage: 39, rangedZh: '东海水龙弹', rangedEn: 'Eastern-Sea Dragon Orbs', aoeZh: '四海洪潮', aoeEn: 'Four-Seas Deluge' },
      campaign_nezha: { color: '#fb7185', mobility: 'fly', projectiles: 5, aoeRadius: 235, rangedDamage: 25, aoeDamage: 38, rangedZh: '乾坤圈连射', rangedEn: 'Universe-Ring Volley', aoeZh: '风火轮天阵', aoeEn: 'Wind-Fire Wheel Array' },
      campaign_king_chiguo: { color: '#2dd4bf', mobility: 'fly', projectiles: 6, aoeRadius: 245, rangedDamage: 24, aoeDamage: 39, rangedZh: '碧玉琵琶音刃', rangedEn: 'Jade-Pipa Sound Blades', aoeZh: '持国天音界', aoeEn: 'Realm of Celestial Music' },
      campaign_king_zengzhang: { color: '#f97316', mobility: 'leap', projectiles: 4, aoeRadius: 250, rangedDamage: 27, aoeDamage: 42, rangedZh: '青锋烈焰剑气', rangedEn: 'Blazing Divine Sword Waves', aoeZh: '增长焚天剑阵', aoeEn: 'Heaven-Burning Sword Array' },
      campaign_king_guangmu: { color: '#34d399', mobility: 'teleport', projectiles: 5, aoeRadius: 260, rangedDamage: 26, aoeDamage: 42, rangedZh: '天龙追魂息', rangedEn: 'Celestial-Dragon Breath', aoeZh: '广目龙界', aoeEn: 'All-Seeing Dragon Realm' },
      campaign_king_duowen: { color: '#60a5fa', mobility: 'fly', projectiles: 7, aoeRadius: 275, rangedDamage: 25, aoeDamage: 44, rangedZh: '宝伞玄光', rangedEn: 'Sacred-Umbrella Rays', aoeZh: '多闻宝塔界', aoeEn: 'Pagoda Canopy Domain' },
      campaign_erlang: { color: '#a78bfa', mobility: 'teleport', projectiles: 5, aoeRadius: 250, rangedDamage: 28, aoeDamage: 43, rangedZh: '天眼神雷', rangedEn: 'Third-Eye Divine Lightning', aoeZh: '灌江天罚阵', aoeEn: 'Guanjiang Judgment Array' },
      campaign_zhubajie: { color: '#f59e0b', mobility: 'leap', projectiles: 3, aoeRadius: 235, rangedDamage: 28, aoeDamage: 44, rangedZh: '九齿飞耙', rangedEn: 'Flying Nine-Tooth Rake', aoeZh: '天蓬震地', aoeEn: 'Marshal Tianpeng Quake' },
      campaign_shawujing: { color: '#38bdf8', mobility: 'teleport', projectiles: 5, aoeRadius: 250, rangedDamage: 27, aoeDamage: 43, rangedZh: '降妖宝杖波', rangedEn: 'Demon-Subduing Staff Waves', aoeZh: '流沙弱水阵', aoeEn: 'Flowing-Sands Undertow' },
      campaign_baigujing: { color: '#e2e8f0', mobility: 'teleport', projectiles: 6, aoeRadius: 260, rangedDamage: 27, aoeDamage: 45, rangedZh: '白骨幽魂箭', rangedEn: 'White-Bone Spirit Arrows', aoeZh: '白骨幽冥阵', aoeEn: 'White-Bone Nether Array' },
      campaign_spider_queen: { color: '#d946ef', mobility: 'fly', projectiles: 7, aoeRadius: 270, rangedDamage: 26, aoeDamage: 44, rangedZh: '七情毒丝', rangedEn: 'Seven-Emotion Venom Threads', aoeZh: '万丝缚心阵', aoeEn: 'Ten-Thousand Web Prison' },
      campaign_bull_king: { color: '#ef4444', mobility: 'leap', projectiles: 4, aoeRadius: 285, rangedDamage: 31, aoeDamage: 49, rangedZh: '混铁棍罡', rangedEn: 'Iron-Staff Shockwaves', aoeZh: '平天裂岳', aoeEn: 'Mountain-Splitting Quake' },
      campaign_red_boy: { color: '#fb923c', mobility: 'fly', projectiles: 8, aoeRadius: 255, rangedDamage: 29, aoeDamage: 47, rangedZh: '三昧火枪', rangedEn: 'Samadhi-Fire Bolts', aoeZh: '五辆火车阵', aoeEn: 'Five Fire-Cart Array' },
      campaign_iron_fan: { color: '#4ade80', mobility: 'fly', projectiles: 6, aoeRadius: 290, rangedDamage: 30, aoeDamage: 50, rangedZh: '芭蕉罡风刃', rangedEn: 'Plantain-Fan Wind Blades', aoeZh: '八万四千里风暴', aoeEn: 'Eighty-Four-Thousand-Li Storm' },
      campaign_nine_headed_beast: { color: '#f43f5e', mobility: 'fly', pattern: 'ring', projectiles: 9, projectileSpeed: 330, aoeRadius: 250, rangedDamage: 25, aoeDamage: 42, rangedZh: '九首血雨', rangedEn: 'Nine-Headed Blood Rain', aoeZh: '碧波九首阵', aoeEn: 'Nine-Headed Emerald-Wave Array' },
      campaign_yellow_brows: { color: '#facc15', mobility: 'teleport', pattern: 'fan', projectiles: 7, projectileSpeed: 350, aoeRadius: 275, rangedDamage: 27, aoeDamage: 46, rangedZh: '金铙震音', rangedEn: 'Golden-Cymbal Shock', aoeZh: '人种袋吞天', aoeEn: 'Human Seed Bag Domain' },
      campaign_giant_python: { color: '#ef4444', mobility: 'leap', pattern: 'ring', projectiles: 6, projectileSpeed: 285, aoeRadius: 265, rangedDamage: 28, aoeDamage: 48, rangedZh: '赤鳞毒牙', rangedEn: 'Red-Scale Venom Fangs', aoeZh: '盘山绞杀', aoeEn: 'Mountain-Coil Constriction' },
      campaign_sai_taisui: { color: '#a855f7', mobility: 'leap', pattern: 'spiral', projectiles: 9, projectileSpeed: 345, aoeRadius: 280, rangedDamage: 29, aoeDamage: 49, rangedZh: '紫金铃火烟沙', rangedEn: 'Purple-Gold Bell Triad', aoeZh: '三铃灾界', aoeEn: 'Three-Bell Calamity' },
      campaign_hundred_eyed: { color: '#eab308', mobility: 'teleport', pattern: 'ring', projectiles: 12, projectileSpeed: 315, aoeRadius: 285, rangedDamage: 27, aoeDamage: 50, rangedZh: '千眼金光', rangedEn: 'Thousand-Eye Golden Rays', aoeZh: '百目毒日阵', aoeEn: 'Hundred-Eye Poison Sun' },
      campaign_azure_lion: { color: '#06b6d4', mobility: 'leap', pattern: 'fan', projectiles: 5, projectileSpeed: 365, aoeRadius: 290, rangedDamage: 31, aoeDamage: 52, rangedZh: '吞天狮吼', rangedEn: 'Heaven-Swallowing Roar', aoeZh: '青狮巨口界', aoeEn: 'Azure Lion Maw Domain' },
      campaign_white_elephant: { color: '#d6d3d1', mobility: 'leap', pattern: 'fan', projectiles: 4, projectileSpeed: 325, aoeRadius: 305, rangedDamage: 33, aoeDamage: 55, rangedZh: '象鼻缚魂波', rangedEn: 'Soul-Binding Trunk Wave', aoeZh: '黄牙震岳', aoeEn: 'Yellow-Tusk Earthquake' },
      campaign_golden_peng: { color: '#f59e0b', mobility: 'fly', pattern: 'spiral', projectiles: 10, projectileSpeed: 410, aoeRadius: 285, rangedDamage: 31, aoeDamage: 53, rangedZh: '阴阳羽刃', rangedEn: 'Yin-Yang Feather Blades', aoeZh: '九万里绝空', aoeEn: 'Ninety-Thousand-Li Sky Seal' },
      campaign_white_deer: { color: '#86efac', mobility: 'teleport', pattern: 'ring', projectiles: 7, projectileSpeed: 325, aoeRadius: 265, rangedDamage: 29, aoeDamage: 48, rangedZh: '寿鹿灵枝', rangedEn: 'Longevity-Antler Bolts', aoeZh: '千童惑心阵', aoeEn: 'Thousand-Child Illusion' },
      campaign_white_mouse: { color: '#f8fafc', mobility: 'teleport', pattern: 'spiral', projectiles: 8, projectileSpeed: 390, aoeRadius: 260, rangedDamage: 31, aoeDamage: 50, rangedZh: '金针飞星', rangedEn: 'Golden-Needle Stars', aoeZh: '无底洞花烛迷阵', aoeEn: 'Bottomless Bridal Snare' },
      campaign_leopard_king: { color: '#64748b', mobility: 'leap', pattern: 'fan', projectiles: 6, projectileSpeed: 370, aoeRadius: 270, rangedDamage: 32, aoeDamage: 51, rangedZh: '隐雾连环斩', rangedEn: 'Hidden-Mist Chain Slash', aoeZh: '假首迷魂雾', aoeEn: 'False-Head Phantom Fog' },
      campaign_yellow_lion: { color: '#fbbf24', mobility: 'leap', pattern: 'fan', projectiles: 5, projectileSpeed: 360, aoeRadius: 275, rangedDamage: 32, aoeDamage: 52, rangedZh: '钉耙盛会飞兵', rangedEn: 'Weapon-Feast Volley', aoeZh: '黄狮夺兵阵', aoeEn: 'Yellow Lion Armament Theft' },
      campaign_nine_spirit: { color: '#fcd34d', mobility: 'teleport', pattern: 'ring', projectiles: 9, projectileSpeed: 350, aoeRadius: 310, rangedDamage: 33, aoeDamage: 56, rangedZh: '九口噬魂', rangedEn: 'Nine-Mouth Soul Devour', aoeZh: '九灵归元界', aoeEn: 'Nine-Spirit Primordial Domain' },
      campaign_rhino_cold: { color: '#38bdf8', mobility: 'leap', pattern: 'fan', projectiles: 5, projectileSpeed: 350, aoeRadius: 250, rangedDamage: 29, aoeDamage: 46, rangedZh: '辟寒冰角', rangedEn: 'Cold-Averting Ice Horn', aoeZh: '玄冰封灯阵', aoeEn: 'Lantern-Freezing Domain' },
      campaign_rhino_heat: { color: '#fb7185', mobility: 'leap', pattern: 'ring', projectiles: 7, projectileSpeed: 340, aoeRadius: 255, rangedDamage: 29, aoeDamage: 46, rangedZh: '辟暑炎角', rangedEn: 'Heat-Averting Flame Horn', aoeZh: '赤炎蒸空阵', aoeEn: 'Sky-Seething Flame Domain' },
      campaign_rhino_dust: { color: '#a3a3a3', mobility: 'teleport', pattern: 'spiral', projectiles: 8, projectileSpeed: 330, aoeRadius: 260, rangedDamage: 28, aoeDamage: 45, rangedZh: '辟尘砂角', rangedEn: 'Dust-Averting Sand Horn', aoeZh: '黄尘蔽日阵', aoeEn: 'Sun-Blotting Dust Domain' },
      campaign_jade_rabbit: { color: '#c4b5fd', mobility: 'teleport', pattern: 'spiral', projectiles: 9, projectileSpeed: 385, aoeRadius: 290, rangedDamage: 32, aoeDamage: 54, rangedZh: '捣药玉杵月华', rangedEn: 'Jade-Pestle Moonbeams', aoeZh: '广寒满月镜', aoeEn: 'Moon-Palace Mirror Domain' }
    };

    // ENEMY & BOSS DEFINITIONS (Specialized Archetypes & Mini-Bosses)
    const ENEMY_TYPES = {
      fengshen_zhang_guifang: { name:'青龙关·张桂芳', nameEn:'Zhang Guifang · Soul-Calling General', isBoss:true, maxHp:9200, speed:170, radius:54, behavior:'campaign_boss', campaignSheet:'fengshen_bosses', campaignRow:0, campaignScale:1.22 },
      fengshen_wen_zhong: { name:'殷商太师·闻仲', nameEn:'Grand Preceptor Wen Zhong', isBoss:true, maxHp:14600, speed:182, radius:58, behavior:'campaign_boss', campaignSheet:'fengshen_bosses', campaignRow:1, campaignScale:1.26 },
      fengshen_yunxiao: { name:'三霄之首·云霄娘娘', nameEn:'Lady Yunxiao · First of the Three Xiaos', isBoss:true, maxHp:17800, speed:190, radius:58, behavior:'campaign_boss', campaignSheet:'fengshen_bosses', campaignRow:2, campaignScale:1.27 },
      fengshen_kong_xuan: { name:'五色神光·孔宣', nameEn:'Kong Xuan · Five-Colored Radiance', isBoss:true, maxHp:21800, speed:205, radius:60, behavior:'campaign_boss', campaignSheet:'fengshen_bosses', campaignRow:3, campaignScale:1.30 },
      fengshen_yuan_hong: { name:'梅山白猿王·袁洪', nameEn:'Yuan Hong · White Ape King of Mount Mei', isBoss:true, maxHp:26800, speed:220, radius:64, behavior:'campaign_boss', campaignSheet:'fengshen_bosses', campaignRow:4, campaignScale:1.34 },
      fengshen_mirror_disciple: { name:'玉泉山·雷镜门人', nameEn:'Yuquan Thunder-Mirror Disciple', maxHp:310, speed:132, radius:26, behavior:'ranged_archer', campaignSheet:'fengshen_enemies', campaignRow:0, campaignScale:0.92 },
      fengshen_soul_guard: { name:'殷商·魂幡枪卫', nameEn:'Shang Soul-Banner Guard', maxHp:460, speed:116, radius:29, behavior:'shield_soldier', campaignSheet:'fengshen_enemies', campaignRow:1, campaignScale:0.96 },
      fengshen_array_adept: { name:'十绝阵·截教阵师', nameEn:'Ten-Absolute-Array Adept', maxHp:390, speed:108, radius:28, behavior:'aoe_ghost', campaignSheet:'fengshen_enemies', campaignRow:2, campaignScale:0.94 },
      fengshen_meishan_raider: { name:'梅山·白猿妖将', nameEn:'Mount-Mei White-Ape Raider', maxHp:590, speed:166, radius:30, behavior:'swarmer', campaignSheet:'fengshen_enemies', campaignRow:3, campaignScale:0.98 },
      ngp_stoneback_macaque: { name:'天镜·石背猕猴悍将', nameEn:'Celestial-Mirror Stoneback Macaque', maxHp:780, speed:175, radius:30, behavior:'swarmer', campaignSheet:'ng_plus_enemies_1', campaignRow:0, campaignScale:0.96 },
      ngp_wind_scout: { name:'天镜·水帘风刃斥候', nameEn:'Water-Curtain Wind Scout', maxHp:620, speed:164, radius:27, behavior:'ranged_archer', campaignSheet:'ng_plus_enemies_1', campaignRow:1, campaignScale:0.90 },
      ngp_jade_sword_adept: { name:'天镜·玉清剑卫', nameEn:'Jade-Purity Sword Adept', maxHp:980, speed:130, radius:30, behavior:'shield_soldier', campaignSheet:'ng_plus_enemies_1', campaignRow:2, campaignScale:0.95 },
      ngp_thunder_talisman: { name:'天镜·雷符阵徒', nameEn:'Thunder-Talisman Acolyte', maxHp:760, speed:118, radius:28, behavior:'aoe_ghost', campaignSheet:'ng_plus_enemies_1', campaignRow:3, campaignScale:0.92 },
      ngp_bronze_guardian: { name:'天镜·昆仑青铜巨灵', nameEn:'Kunlun Bronze Guardian', maxHp:2200, speed:82, radius:42, behavior:'mini_boss_golem', campaignSheet:'ng_plus_enemies_1', campaignRow:4, campaignScale:1.06 },
      ngp_coral_sentinel: { name:'天镜·东海珊瑚戟卫', nameEn:'Eastern-Sea Coral Sentinel', maxHp:1100, speed:128, radius:31, behavior:'shield_soldier', campaignSheet:'ng_plus_enemies_2', campaignRow:0, campaignScale:0.98 },
      ngp_pearl_siren: { name:'天镜·珠针海妖', nameEn:'Pearl-Needle Siren', maxHp:850, speed:142, radius:28, behavior:'ranged_archer', campaignSheet:'ng_plus_enemies_2', campaignRow:1, campaignScale:0.92 },
      ngp_abyssal_shell: { name:'天镜·渊甲巨兽', nameEn:'Abyssal Shell Beast', maxHp:2600, speed:88, radius:44, behavior:'mini_boss_golem', campaignSheet:'ng_plus_enemies_2', campaignRow:2, campaignScale:1.08 },
      ngp_cloud_lancer: { name:'天镜·凌云神枪卫', nameEn:'Celestial Cloud Lancer', maxHp:1150, speed:188, radius:30, behavior:'swarmer', campaignSheet:'ng_plus_enemies_2', campaignRow:3, campaignScale:0.96 },
      ngp_star_fire_archer: { name:'天镜·星火神射', nameEn:'Star-Fire Archer', maxHp:900, speed:150, radius:28, behavior:'ranged_archer', campaignSheet:'ng_plus_enemies_2', campaignRow:4, campaignScale:0.93 },
      ngp_thunder_drum_colossus: { name:'天镜·雷鼓巨将', nameEn:'Thunder-Drum Colossus', maxHp:2900, speed:92, radius:45, behavior:'mini_boss_commander', campaignSheet:'ng_plus_enemies_3', campaignRow:0, campaignScale:1.10 },
      ngp_nether_chain_warden: { name:'天镜·幽冥锁魂狱将', nameEn:'Nether Chain Warden', maxHp:1400, speed:122, radius:32, behavior:'shield_soldier', campaignSheet:'ng_plus_enemies_3', campaignRow:1, campaignScale:1.00 },
      ngp_white_bone_stalker: { name:'天镜·白骨猎煞', nameEn:'White-Bone Stalker', maxHp:1250, speed:184, radius:29, behavior:'swarmer', campaignSheet:'ng_plus_enemies_3', campaignRow:2, campaignScale:0.96 },
      ngp_web_cocoon_hexer: { name:'天镜·盘丝茧咒师', nameEn:'Web-Cocoon Hexer', maxHp:1050, speed:126, radius:30, behavior:'ranged_spider', campaignSheet:'ng_plus_enemies_3', campaignRow:3, campaignScale:0.96 },
      ngp_flame_cloud_spearling: { name:'天镜·火云枪灵', nameEn:'Flame-Cloud Spearling', maxHp:1250, speed:170, radius:29, behavior:'ranged_archer', campaignSheet:'ng_plus_enemies_3', campaignRow:4, campaignScale:0.95 },
      ngp_iron_fan_witch: { name:'天镜·铁扇罡风巫', nameEn:'Iron-Fan Gale Witch', maxHp:1350, speed:138, radius:31, behavior:'aoe_ghost', campaignSheet:'ng_plus_enemies_4', campaignRow:0, campaignScale:0.98 },
      ngp_lion_fang_brute: { name:'天镜·狮驼獠牙悍将', nameEn:'Lion-Camel Fang Brute', maxHp:3100, speed:116, radius:45, behavior:'mini_boss_commander', campaignSheet:'ng_plus_enemies_4', campaignRow:1, campaignScale:1.10 },
      ngp_shadow_mouse: { name:'天镜·无底影鼠刺客', nameEn:'Bottomless-Cave Shadow Mouse', maxHp:1200, speed:210, radius:27, behavior:'swarmer', campaignSheet:'ng_plus_enemies_4', campaignRow:2, campaignScale:0.91 },
      ngp_frost_hare: { name:'天镜·月宫霜兔灵', nameEn:'Moon-Palace Frost Hare', maxHp:1450, speed:160, radius:30, behavior:'ranged_archer', campaignSheet:'ng_plus_enemies_4', campaignRow:3, campaignScale:0.96 },
      ngp_dustbreaker: { name:'天镜·青龙山破尘犀将', nameEn:'Rhino-Mountain Dustbreaker', maxHp:3400, speed:108, radius:47, behavior:'mini_boss_golem', campaignSheet:'ng_plus_enemies_4', campaignRow:4, campaignScale:1.12 },
      campaign_monkey: { name: '花果山试艺灵猴', maxHp: 145, speed: 142, radius: 24, behavior: 'swarmer', campaignSheet: 'campaign_characters_act1', campaignRow: 0, campaignScale: 0.78 },
      campaign_monkey_chief: { name: '花果山·老猿寨主', nameEn: 'Flower-Fruit Mountain · Elder Ape Chief', isBoss: true, maxHp: 2400, speed: 138, radius: 50, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act1', campaignRow: 1, campaignScale: 1.08 },
      campaign_disciple: { name: '玉虚宫·天尊门人', maxHp: 245, speed: 112, radius: 26, behavior: 'ranged_archer', campaignSheet: 'campaign_characters_act1', campaignRow: 2, campaignScale: 0.83 },
      campaign_yuanshi: { name: '玉清境·元始天尊', nameEn: 'Jade-Purity Realm · Yuanshi Tianzun', isBoss: true, maxHp: 4800, speed: 118, radius: 58, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act1', campaignRow: 3, campaignScale: 1.16 },
      campaign_dragon_guard: { name: '东海龙宫·蛟龙巡卫', maxHp: 330, speed: 112, radius: 29, behavior: 'ranged_spider', campaignSheet: 'campaign_characters_act1', campaignRow: 4, campaignScale: 0.75 },
      campaign_dragon_king: { name: '东海龙王·敖广', nameEn: 'Dragon King of the Eastern Sea · Ao Guang', isBoss: true, maxHp: 6200, speed: 128, radius: 62, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act1', campaignRow: 4, campaignScale: 1.22 },
      campaign_nezha: { name: '三坛海会大神·哪吒', nameEn: 'Third Lotus Prince · Nezha', isBoss: true, maxHp: 7200, speed: 178, radius: 54, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act2', campaignRow: 0, campaignScale: 1.08 },
      campaign_erlang: { name: '二郎显圣真君·杨戬', nameEn: 'Erlang, Illustrious Sage · Yang Jian', isBoss: true, maxHp: 9200, speed: 166, radius: 58, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act2', campaignRow: 1, campaignScale: 1.12 },
      campaign_king_chiguo: { name: '东方持国天王·魔礼海', nameEn: 'Eastern King Chiguo · Mo Lihai', isBoss: true, maxHp: 7600, speed: 132, radius: 58, behavior: 'campaign_boss', campaignSheet: 'four_heavenly_kings', campaignRow: 0, campaignScale: 1.1 },
      campaign_king_zengzhang: { name: '南方增长天王·魔礼青', nameEn: 'Southern King Zengzhang · Mo Liqing', isBoss: true, maxHp: 8100, speed: 146, radius: 60, behavior: 'campaign_boss', campaignSheet: 'four_heavenly_kings', campaignRow: 1, campaignScale: 1.13 },
      campaign_king_guangmu: { name: '西方广目天王·魔礼寿', nameEn: 'Western King Guangmu · Mo Lishou', isBoss: true, maxHp: 8600, speed: 136, radius: 62, behavior: 'campaign_boss', campaignSheet: 'four_heavenly_kings', campaignRow: 2, campaignScale: 1.16 },
      campaign_king_duowen: { name: '北方多闻天王·魔礼红', nameEn: 'Northern King Duowen · Mo Lihong', isBoss: true, maxHp: 9200, speed: 126, radius: 64, behavior: 'campaign_boss', campaignSheet: 'four_heavenly_kings', campaignRow: 3, campaignScale: 1.18 },
      campaign_buddha: { name: '灵山世尊·如来佛祖', nameEn: 'World-Honored Buddha · Tathagata', isBoss: true, isBuddhaBoss: true, maxHp: 13200, speed: 0, radius: 92, behavior: 'boss_buddha', campaignSheet: 'campaign_characters_act2', campaignRow: 3, campaignScale: 1.38 },
      campaign_zhubajie: { name: '高老庄·猪八戒', nameEn: 'Gao Village · Zhu Bajie', isBoss: true, maxHp: 8200, speed: 138, radius: 62, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act3', campaignRow: 0, campaignScale: 1.16 },
      campaign_shawujing: { name: '流沙河·沙悟净', nameEn: 'Flowing-Sands River · Sha Wujing', isBoss: true, maxHp: 9400, speed: 132, radius: 61, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act3', campaignRow: 1, campaignScale: 1.14 },
      campaign_baigujing: { name: '白虎岭·白骨夫人', nameEn: 'White-Bone Ridge · Lady White Bone', isBoss: true, maxHp: 11200, speed: 148, radius: 58, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act3', campaignRow: 2, campaignScale: 1.14 },
      campaign_spider_queen: { name: '盘丝洞·蜘蛛女王', nameEn: 'Webbed Hollow · Spider Queen', isBoss: true, maxHp: 12600, speed: 144, radius: 64, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act3', campaignRow: 3, campaignScale: 1.18 },
      campaign_bull_king: { name: '积雷山·牛魔王', nameEn: 'Mount Thunder · Bull Demon King', isBoss: true, maxHp: 14800, speed: 142, radius: 72, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act3', campaignRow: 4, campaignScale: 1.3 },
      campaign_red_boy: { name: '火云洞·红孩儿', nameEn: 'Fire-Cloud Cave · Red Boy', isBoss: true, maxHp: 15400, speed: 172, radius: 55, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act3', campaignRow: 5, campaignScale: 1.08 },
      campaign_iron_fan: { name: '翠云山·铁扇公主', nameEn: 'Emerald-Cloud Mountain · Princess Iron Fan', isBoss: true, maxHp: 17800, speed: 148, radius: 59, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act3', campaignRow: 6, campaignScale: 1.15 },
      campaign_nine_headed_beast: { name: '碧波潭·九头虫', nameEn: 'Emerald-Wave Pool · Nine-Headed Beast', isBoss: true, maxHp: 7200, speed: 158, radius: 66, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act4', campaignRow: 0, campaignScale: 1.22 },
      campaign_thorn_spirit: { name: '荆棘岭·木仙', nameEn: 'Thorn Ridge · Tree Immortal', maxHp: 780, speed: 96, radius: 34, behavior: 'ranged_archer', campaignSheet: 'campaign_characters_act4', campaignRow: 1, campaignScale: 0.83 },
      campaign_yellow_brows: { name: '小雷音寺·黄眉大王', nameEn: 'Little Thunderclap · Yellow Brows Great King', isBoss: true, maxHp: 7800, speed: 142, radius: 64, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act4', campaignRow: 2, campaignScale: 1.18 },
      campaign_giant_python: { name: '七绝山·红鳞大蟒精', nameEn: 'Qijue Mountain · Great Red-Scaled Python', isBoss: true, maxHp: 7600, speed: 152, radius: 72, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act4', campaignRow: 3, campaignScale: 1.26 },
      campaign_sai_taisui: { name: '麒麟山·赛太岁', nameEn: 'Qilin Mountain · Sai Tai Sui', isBoss: true, maxHp: 8200, speed: 158, radius: 62, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act4', campaignRow: 4, campaignScale: 1.17 },
      campaign_hundred_eyed: { name: '黄花观·百眼魔君', nameEn: 'Yellow-Flower Temple · Hundred-Eyed Demon', isBoss: true, maxHp: 8500, speed: 140, radius: 65, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act4', campaignRow: 5, campaignScale: 1.2 },
      campaign_azure_lion: { name: '狮驼洞·青狮大王', nameEn: 'Lion-Camel Cave · Azure Lion King', isBoss: true, maxHp: 8800, speed: 150, radius: 72, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act5', campaignRow: 0, campaignScale: 1.25 },
      campaign_white_elephant: { name: '狮驼洞·黄牙老象', nameEn: 'Lion-Camel Cave · Yellow-Tusk White Elephant', isBoss: true, maxHp: 9200, speed: 126, radius: 78, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act5', campaignRow: 1, campaignScale: 1.3 },
      campaign_golden_peng: { name: '狮驼国·金翅大鹏雕', nameEn: 'Lion-Camel Kingdom · Golden-Winged Great Peng', isBoss: true, maxHp: 9800, speed: 192, radius: 70, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act5', campaignRow: 2, campaignScale: 1.28 },
      campaign_white_deer: { name: '比丘国·白鹿国丈', nameEn: 'Bhikkhu Kingdom · White Deer Preceptor', isBoss: true, maxHp: 8200, speed: 145, radius: 62, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act5', campaignRow: 3, campaignScale: 1.16 },
      campaign_white_mouse: { name: '无底洞·金鼻白毛老鼠精', nameEn: 'Bottomless Cave · Golden-Nosed White Mouse', isBoss: true, maxHp: 8600, speed: 184, radius: 57, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act5', campaignRow: 4, campaignScale: 1.1 },
      campaign_leopard_king: { name: '隐雾山·南山大王', nameEn: 'Hidden-Mist Mountain · Southern Mountain King', isBoss: true, maxHp: 9000, speed: 176, radius: 63, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act5', campaignRow: 5, campaignScale: 1.17 },
      campaign_yellow_lion: { name: '豹头山·黄狮精', nameEn: 'Leopard-Head Mountain · Yellow Lion Spirit', isBoss: true, maxHp: 9000, speed: 160, radius: 66, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act6', campaignRow: 0, campaignScale: 1.18 },
      campaign_nine_spirit: { name: '竹节山·九灵元圣', nameEn: 'Bamboo-Joint Mountain · Nine-Spirit Primordial Sage', isBoss: true, maxHp: 10800, speed: 150, radius: 82, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act6', campaignRow: 1, campaignScale: 1.34 },
      campaign_rhino_cold: { name: '青龙山·辟寒大王', nameEn: 'Azure-Dragon Mountain · Cold-Averting Rhino King', isBoss: true, maxHp: 5200, speed: 142, radius: 66, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act6', campaignRow: 2, campaignScale: 1.17 },
      campaign_rhino_heat: { name: '青龙山·辟暑大王', nameEn: 'Azure-Dragon Mountain · Heat-Averting Rhino King', isBoss: true, maxHp: 5200, speed: 148, radius: 66, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act6', campaignRow: 3, campaignScale: 1.17 },
      campaign_rhino_dust: { name: '青龙山·辟尘大王', nameEn: 'Azure-Dragon Mountain · Dust-Averting Rhino King', isBoss: true, maxHp: 5200, speed: 154, radius: 66, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act6', campaignRow: 4, campaignScale: 1.17 },
      campaign_jade_rabbit: { name: '天竺国·玉兔精', nameEn: 'Tianzhu Kingdom · Jade Rabbit Spirit', isBoss: true, maxHp: 10400, speed: 182, radius: 58, behavior: 'campaign_boss', campaignSheet: 'campaign_characters_act6', campaignRow: 5, campaignScale: 1.12 },
      campaign_late_acolyte: { name: '西域百相妖兵', nameEn: 'Western-Realm Demon Acolyte', maxHp: 980, speed: 148, radius: 29, behavior: 'swarmer', campaignSheet: 'campaign_characters_act6', campaignRow: 6, campaignScale: 0.78 },
      demon_ape: { name: '花果山狂猿妖', maxHp: 420, speed: 130, radius: 26, isBoss: false, row: 0, cols: 8, behavior: 'swarmer' },
      tianbing: { name: '天庭金甲枪卫', maxHp: 650, speed: 105, radius: 28, isBoss: false, row: 1, cols: 8, behavior: 'shield_soldier' },
      tian_archer: { name: '灵霄神射弓手', maxHp: 380, speed: 130, radius: 26, isBoss: false, row: 2, cols: 8, behavior: 'ranged_archer' },
      nether_ghost: { name: '幽冥鬼使法师', maxHp: 460, speed: 95, radius: 28, isBoss: false, row: 3, cols: 8, behavior: 'aoe_ghost' },
      bagua_golem: { name: '太上八卦巨傀 (巨型精英)', maxHp: 1450, speed: 70, radius: 40, isBoss: false, row: 4, cols: 8, behavior: 'mini_boss_golem' },
      tianbing_commander: { name: '金甲神威统帅 (重装精英)', maxHp: 1650, speed: 85, radius: 42, isBoss: false, row: 1, cols: 8, behavior: 'mini_boss_commander' },
      cave_spider: { name: '盘丝洞毒蛛兵', maxHp: 320, speed: 140, radius: 26, isBoss: false, row: 5, cols: 4, behavior: 'ranged_spider' },

      boss_spider: { name: '盘丝洞·蜘蛛精七仙姑 (第30重天)', isBoss: true, maxHp: 14000, speed: 115, radius: 64, row: 0, cols: 5, behavior: 'boss_spider' },
      boss_baigu: { name: '白虎岭·白骨精三变夫人 (第60重天)', isBoss: true, maxHp: 28000, speed: 125, radius: 64, row: 1, cols: 6, behavior: 'boss_baigu' },
      boss_jin_yin: { name: '平顶山莲花洞·金角银角双王 (第90重天)', isBoss: true, maxHp: 45000, speed: 130, radius: 68, row: 2, cols: 6, behavior: 'boss_jin_yin' },
      boss_erlang: { name: '灌江口·二郎显圣真君与哮天犬 (第120重天)', isBoss: true, maxHp: 65000, speed: 155, radius: 72, row: 0, cols: 4, isErlangBoss: true, behavior: 'boss_erlang' },
      boss_buddha: { name: '大日雷音寺·大日如来佛祖 (第150重天)', isBoss: true, maxHp: 120000, speed: 0, radius: 120, row: 0, cols: 5, isBuddhaBoss: true, behavior: 'boss_buddha' },
      boss_tongbei: { name: '混世魔猴·通臂猿猴 (最终决战 第180重天)', isBoss: true, maxHp: 180000, speed: 165, radius: 75, row: 5, cols: 6, isFinalBoss: true, behavior: 'boss_tongbei' },

      xiaotianquan_hound: { name: '二郎真君·啸天神犬', isHound: true, maxHp: 8500, speed: 280, radius: 32, row: 3, cols: 4, behavior: 'hound_attack' }
    };

    const NORMAL_ENEMY_WAVE_MULTIPLIER = 3;
    const BOSS_STRENGTH_MULTIPLIER = 3;
    const NG_PLUS_ENEMY_HP_MULTIPLIER = 7;
    const NG_PLUS_ENEMY_DAMAGE_MULTIPLIER = 3;

    class Enemy {
      constructor(typeKey, x, y, isAlly = false) {
        this.typeKey = typeKey;
        const def = ENEMY_TYPES[typeKey] || ENEMY_TYPES['demon_ape'];
        this.name = gameState.language === 'en' && def.nameEn ? def.nameEn : def.name;
        this.isBoss = def.isBoss || false;
        this.isErlangBoss = def.isErlangBoss || false;
        this.isBuddhaBoss = def.isBuddhaBoss || false;
        this.isHound = def.isHound || false;
        this.isFinalBoss = def.isFinalBoss || false;
        this.isAlly = isAlly;
        // The entire 100-chapter story is one continuous build. Enemy durability
        // rises without resetting at chapter 66, then tapers so late bosses remain
        // demanding without becoming pure damage sponges.
        const earlyJourneyProgress = Math.min(65, gameState.chamberIndex);
        const lateJourneyProgress = Math.max(0, gameState.chamberIndex - 65);
        const hpScale = 1 + earlyJourneyProgress * 0.035 + Math.min(0.875, lateJourneyProgress * 0.025);
        this.strengthMultiplier = this.isBoss ? BOSS_STRENGTH_MULTIPLIER : 1;
        this.maxHp = def.maxHp * hpScale * this.strengthMultiplier * (gameState.isNewGamePlus ? NG_PLUS_ENEMY_HP_MULTIPLIER : 1);
        this.hp = this.maxHp;
        this.speed = def.speed * (gameState.isNewGamePlus ? 1.08 : 1);
        this.radius = def.radius;
        this.row = def.row || 0;
        this.cols = def.cols || 8;
        this.campaignSheet = def.campaignSheet || null;
        this.campaignRow = def.campaignRow || 0;
        this.campaignScale = def.campaignScale || 1;
        this.direction = 'down';
        this.behavior = def.behavior;
        this.x = x;
        this.y = y;
        this.vx = 0;
        this.vy = 0;
        this.knockbackX = 0;
        this.knockbackY = 0;
        this.facing = 1;
        this.alive = true;
        this.attackTimer = 0;
        this.attackCooldown = 0.5 + Math.random() * 0.5;
        this.isAttacking = false;
        this.attackDuration = 0;
        this.attackMaxDuration = 0.38;
        this.attackAngle = 0;
        this.shotFired = false;
        this.isKnockedDown = false;
        this.knockdownTimer = 0;
        this.knockdownMaxDuration = 0.9;
        this.knockdownAngle = 0;
        this.hurtTimer = 0;
        this.meleeContactHoldTimer = 0;
        this.isDying = false;
        this.isSubdued = false;
        this.outcomeResolved = false;
        this.formKillCredited = false;
        this.formWeakPointTimer = 0;
        this.deathTimer = 0;
        this.deathMaxDuration = 0.65;
        this.burnTimer = 0;
        this.burnDmg = 0;
        this.freezeTimer = 0;
        this.slowTimer = 0;
        this.slowAmount = 0;
        this.phase = 1;
        this.state = 'idle';
        this.animClock = Math.random() * 0.6;
        this.pendingBossAttack = null;
        this.telegraphZone = null;
        this.attackTarget = null;
        this.commandTarget = null;
        this.commandPoint = null;
        this.companionCommandActive = false;
        this.houndSlamStartX = x;
        this.houndSlamStartY = y;
        this.houndSlamTargetX = x;
        this.houndSlamTargetY = y;
        this.houndSlamRank = 1;
        this.houndVisualLift = 0;
        this.judgmentMarkTimer = 0;
        this.campaignBossProfile = CAMPAIGN_BOSS_PROFILES[typeKey] || null;
        this.campaignAction = 'idle';
        this.campaignActionIndex = Math.floor(Math.random() * 3);
        this.mobilityStartX = x;
        this.mobilityStartY = y;
        this.mobilityTargetX = x;
        this.mobilityTargetY = y;
        this.mobilityLift = 0;
      }

      applyBurn(dmg, duration) {
        this.burnDmg = dmg;
        this.burnTimer = duration;
      }

      applyFreeze(duration) {
        this.freezeTimer = duration;
      }

      applySlow(amount, duration) {
        this.slowAmount = amount;
        this.slowTimer = duration;
      }

      takeDamage(amount, isCrit = false, forceKnockdown = false) {
        if (this.isDying || this.isSubdued) return;
        if (this.isAlly) return;

        if (player?.castActive?.boonId === 'erlang_ring') {
          const insideEye = Math.hypot(this.x - player.castActive.x, this.y - player.castActive.y) <= player.castActive.radius + this.radius;
          if (insideEye) {
            const rank = player.boons.cast?.level || 1;
            amount *= 1.40 + 0.08 * Math.max(0, rank - 1);
            if (Math.random() < 0.22) fxList.push(new AnimatedLightningStrike(this.x, this.y));
          }
        }

        if (this.isBuddhaBoss) {
          const surrenderRatio = this.typeKey === 'campaign_buddha' ? 0.5 : 0.08;
          if (this.hp <= this.maxHp * surrenderRatio) {
            this.hp = Math.round(this.maxHp * surrenderRatio);
            triggerBuddhaApprovalCutscene();
            return;
          }
        }

        this.hp -= amount;
        if (this.hp <= 0 && !this.isBoss && !this.formKillCredited) {
          this.formKillCredited = true;
          player.onFormEnemyDefeated(this);
        }
        if (this.hp > 0) this.hurtTimer = Math.max(this.hurtTimer, 0.20);
        floatingTexts.push(new FloatingText(this.x, this.y - 20, Math.round(amount), isCrit ? '#facc15' : '#ffffff', isCrit ? 19 : 13));

        const buddhaSurrenderRatio = this.typeKey === 'campaign_buddha' ? 0.5 : 0.08;
        if (this.isBuddhaBoss && this.hp <= this.maxHp * buddhaSurrenderRatio) {
          this.hp = Math.round(this.maxHp * buddhaSurrenderRatio);
          triggerBuddhaApprovalCutscene();
          return;
        }

        if (this.isFinalBoss && this.phase === 1 && this.hp <= this.maxHp * 0.5) {
          this.phase = 2;
          this.radius = 90;
          sound.playAwaken();
          createScreenShake(18);
          fxList.push(new Shockwave(this.x, this.y, 300, '#ef4444'));
          floatingTexts.push(new FloatingText(this.x, this.y - 60, uiText('万妖魔躯 · 魔猿法天象地!', 'Demon Colossus · Titan Ape Manifestation!'), '#ef4444', 24));
        }

        if (this.hp <= 0 && this.isBoss && gameState.hasStarted) {
          // Campaign outcomes are deliberately nonlethal. Hold the boss in a
          // harmless surrender pose until the paused karma decision is resolved.
          this.hp = 1;
          this.isSubdued = true;
          this.isAttacking = false;
          this.pendingBossAttack = null;
          this.telegraphZone = null;
          this.vx = 0;
          this.vy = 0;
          this.knockbackX = 0;
          this.knockbackY = 0;
          this.hurtTimer = 999;
          floatingTexts.push(new FloatingText(this.x, this.y - 48, uiText('伏地未死 · 等候因果裁决', 'Subdued, not slain · Awaiting karmic judgment'), '#fde68a', 17));
          queueBossOutcomeIfBattleEnded();
          return;
        }

        if (this.hp <= 0 && !this.isDying) {
          // DEATH ANIMATION
          this.isDying = true;
          this.deathTimer = this.deathMaxDuration;
          this.alive = false;
          gameState.enemiesKilled++;
          gameState.gold += Math.floor(Math.random() * 10) + (this.isBoss ? 120 : 6);
          gameState.ashes += Math.floor(Math.random() * 5) + (this.isBoss ? 60 : 3);
          scheduleMetaProgressSave();

          if (this.isBoss) {
            sound.playGong();
            createScreenShake(14);
          } else {
            sound.playGong();
          }

          fxList.push(new DeathSoulFX(this.x, this.y, this.typeKey, this.radius));
          updateHUD();
        } else if (!this.isBoss && (forceKnockdown || isCrit || amount >= 45 || Math.random() < 0.35)) {
          // KNOCKDOWN ANIMATION
          this.isKnockedDown = true;
          this.knockdownTimer = 0.85 + Math.random() * 0.35;
          this.knockdownMaxDuration = this.knockdownTimer;
          this.knockdownAngle = this.facing === 1 ? Math.PI / 2 : -Math.PI / 2;
          fxList.push(new KnockdownDustFX(this.x, this.y + 10));
        }
      }

      resolveBossAttack() {
        const attack = this.pendingBossAttack;
        if (!attack) return;
        this.pendingBossAttack = null;
        const angle = attack.angle;
        if (attack.type === 'campaign_ranged') {
          const count = attack.profile.projectiles;
          const spread = count <= 3 ? 0.17 : 0.12;
          const pattern = attack.profile.pattern || 'fan';
          const baseSpeed = attack.profile.projectileSpeed || 360;
          for (let i = 0; i < count; i++) {
            let ang;
            let speed = baseSpeed;
            if (pattern === 'ring') {
              ang = attack.angle + i * Math.PI * 2 / count;
            } else if (pattern === 'spiral') {
              ang = attack.angle + i * Math.PI * 2 / count + this.animClock * 0.55;
              speed *= 0.78 + (i % 3) * 0.12;
            } else {
              const offset = (i - (count - 1) / 2) * spread;
              ang = attack.angle + offset;
            }
            projectiles.push(new BossSkillProjectile(
              this.x, this.y - 12,
              Math.cos(ang) * speed, Math.sin(ang) * speed,
              attack.profile.rangedDamage * this.strengthMultiplier, attack.profile.color
            ));
          }
          fxList.push(new BossSkillAnimatedFX(this.x, this.y - 12, 0, 0.30, 92, attack.profile.color, false, 3, 4));
          sound.playLightning();
        } else if (attack.type === 'campaign_aoe') {
          const visibleHitRadius = attack.profile.aoeRadius * 0.72;
          fxList.push(new RadialSparksFX(this.x, this.y, 10, attack.profile.color, 58));
          if (Math.hypot(player.x - this.x, player.y - this.y) <= visibleHitRadius + player.radius) {
            player.takeDamage(attack.profile.aoeDamage * this.strengthMultiplier);
          }
          createScreenShake(7);
          sound.playStaffSmash(true);
        } else if (attack.type === 'campaign_mobility') {
          this.x = attack.targetX;
          this.y = attack.targetY;
          this.mobilityLift = 0;
          fxList.push(new BossSkillAnimatedFX(this.x, this.y, 2, 0.45, 105, attack.profile.color, true));
          fxList.push(new Shockwave(this.x, this.y, 105, attack.profile.color));
          createScreenShake(5);
        } else if (attack.type === 'erlang_thrust') {
          createScreenShake(8);
          for (let i = -3; i <= 3; i++) {
            const ang = angle + i * 0.15;
            projectiles.push(new Projectile(this.x, this.y, Math.cos(ang) * 340, Math.sin(ang) * 340, 26 * this.strengthMultiplier, '#facc15', true));
          }
          fxList.push(new AnimatedAttackSweep(this.x, this.y, angle, 140, '#facc15'));
        } else if (attack.type === 'erlang_command') {
          fxList.push(new AnimatedLightningStrike(attack.targetX, attack.targetY));
          projectiles.push(new Projectile(this.x, this.y, Math.cos(angle) * 400, Math.sin(angle) * 400, 35 * this.strengthMultiplier, '#38bdf8', true));
        } else if (attack.type === 'spider_fan') {
          for (let i = -2; i <= 2; i++) {
            const ang = angle + i * 0.25;
            projectiles.push(new Projectile(this.x, this.y, Math.cos(ang) * 260, Math.sin(ang) * 260, 22 * this.strengthMultiplier, '#22c55e', true));
          }
        } else if (attack.type === 'baigu_ring') {
          for (let i = 0; i < 6; i++) {
            const ang = angle + i * Math.PI * 2 / 6;
            projectiles.push(new Projectile(this.x, this.y, Math.cos(ang) * 250, Math.sin(ang) * 250, 25 * this.strengthMultiplier, '#10b981', true));
          }
        } else if (attack.type === 'jin_yin_fan') {
          for (let i = -3; i <= 3; i++) {
            const ang = angle + i * 0.18;
            projectiles.push(new Projectile(this.x, this.y, Math.cos(ang) * 300, Math.sin(ang) * 300, 28 * this.strengthMultiplier, '#f59e0b', true));
          }
        } else if (attack.type === 'tongbei_ring') {
          for (let i = 0; i < attack.count; i++) {
            const ang = i * Math.PI * 2 / attack.count + attack.offset;
            projectiles.push(new Projectile(this.x, this.y, Math.cos(ang) * 340, Math.sin(ang) * 340, attack.damage * this.strengthMultiplier, '#ef4444', true));
          }
          fxList.push(new Shockwave(this.x, this.y, 280, '#ef4444'));
          createScreenShake(12);
        }
      }

      update(dt) {
        this.animClock += dt;
        if (this.meleeContactHoldTimer > 0) {
          this.meleeContactHoldTimer = Math.max(0, this.meleeContactHoldTimer - dt);
          return;
        }
        if (this.isDying) {
          this.deathTimer -= dt;
          this.burnTimer = Math.max(0, this.burnTimer - dt);
          return;
        }

        if (this.isSubdued) return;

        if (!this.alive) return;

        if (this.hurtTimer > 0) this.hurtTimer = Math.max(0, this.hurtTimer - dt);
        if (this.judgmentMarkTimer > 0) this.judgmentMarkTimer = Math.max(0, this.judgmentMarkTimer - dt);
        this.knockbackX *= Math.exp(-12 * dt);
        this.knockbackY *= Math.exp(-12 * dt);

        if (this.knockdownTimer > 0) {
          this.knockdownTimer -= dt;
          if (this.knockdownTimer <= 0) {
            this.isKnockedDown = false;
          }
          this.x += (this.knockbackX * 0.8) * dt;
          this.y += (this.knockbackY * 0.8) * dt;
          this.clampBoundary();
          return;
        }

        if (this.attackCooldown > 0) this.attackCooldown -= dt;

        if (this.isAttacking) {
          this.attackDuration -= dt;
          const attackProgress = 1 - this.attackDuration / this.attackMaxDuration;
          if (this.pendingBossAttack && attackProgress >= this.pendingBossAttack.contactAt) this.resolveBossAttack();
          if (this.attackDuration <= 0) {
            if (this.pendingBossAttack) this.resolveBossAttack();
            this.isAttacking = false;
            this.shotFired = false;
            if (this.isErlangBoss) this.state = 'idle';
            if (this.campaignBossProfile) {
              this.state = 'idle';
              this.campaignAction = 'idle';
              this.mobilityLift = 0;
            }
            if (this.isHound) {
              this.state = 'idle';
              this.attackTarget = null;
              this.houndVisualLift = 0;
              if (this.isAlly && this.companionCommandActive) {
                this.companionCommandActive = false;
                this.commandTarget = null;
              }
            }
          }
        }

        if (this.burnTimer > 0) {
          this.burnTimer -= dt;
          this.hp -= (this.burnDmg * dt);
          if (this.hp <= 0) this.takeDamage(1);
        }

        if (this.freezeTimer > 0) {
          this.freezeTimer -= dt;
          this.x += this.knockbackX * dt;
          this.y += this.knockbackY * dt;
          this.clampBoundary();
          return;
        }

        let speedMod = 1.0;
        if (this.slowTimer > 0) {
          this.slowTimer -= dt;
          speedMod *= (1 - this.slowAmount);
        }

        let target = player;
        if (this.isAlly) {
          if (this.isHound && gameState.playableHero === 'erlang') {
            if (this.state === 'hound_empowered_slam' && this.isAttacking) {
              // Finish the authored leap even if the originally selected victim
              // dies mid-flight; the landing point still deals radial damage.
              target = this.commandTarget || player;
            } else if (this.companionCommandActive && this.commandTarget?.alive) {
              target = this.commandTarget;
            } else {
              this.companionCommandActive = false;
              this.commandTarget = null;
              const followX = player.x - player.facing * 55;
              const followY = player.y + 32;
              const followDistance = Math.hypot(followX - this.x, followY - this.y);
              if (followDistance > 18) {
                const followAngle = Math.atan2(followY - this.y, followX - this.x);
                this.vx = Math.cos(followAngle) * Math.min(this.speed, followDistance * 5);
                this.vy = Math.sin(followAngle) * Math.min(this.speed, followDistance * 5);
                this.facing = this.vx < 0 ? -1 : 1;
              } else {
                this.vx *= Math.exp(-10 * dt);
                this.vy *= Math.exp(-10 * dt);
              }
              this.x += this.vx * dt;
              this.y += this.vy * dt;
              this.clampBoundary();
              return;
            }
          } else {
          let nearestEnemy = null;
          let nearestDistanceSq = Infinity;
          enemies.forEach(candidate => {
            if (candidate === this || candidate.isAlly || !candidate.alive || candidate.isDying) return;
            const dx = candidate.x - this.x;
            const dy = candidate.y - this.y;
            const distanceSq = dx * dx + dy * dy;
            if (distanceSq < nearestDistanceSq) {
              nearestDistanceSq = distanceSq;
              nearestEnemy = candidate;
            }
          });
          if (nearestEnemy) target = nearestEnemy;
          else {
            this.vx *= Math.exp(-10 * dt);
            this.vy *= Math.exp(-10 * dt);
            return;
          }
          }
        }

        const distToTarget = Math.hypot(target.x - this.x, target.y - this.y);
        const angleToTarget = Math.atan2(target.y - this.y, target.x - this.x);

        const dy = target.y - this.y;
        const dx = target.x - this.x;
        if (Math.abs(dy) > Math.abs(dx)) {
          this.direction = dy < 0 ? 'up' : 'down';
          this.facing = 1;
        } else {
          this.direction = dx < 0 ? 'left' : 'right';
          this.facing = dx < 0 ? -1 : 1;
        }

        this.attackTimer += dt;

        if (this.isBuddhaBoss) {
          if (this.telegraphZone) {
            this.telegraphZone.timer -= dt;
            if (this.telegraphZone.timer <= 0) {
              const tz = this.telegraphZone;
              this.telegraphZone = null;

              sound.playStaffSmash(true);
              sound.playGong();
              createScreenShake(20);

              fxList.push(new Shockwave(tz.x, tz.y, tz.radius, '#facc15'));
              fxList.push(new AnimatedBuddhaPalmSlam(tz.x, tz.y, tz.radius));

              const distP = Math.hypot(player.x - tz.x, player.y - tz.y);
              if (distP <= tz.radius) {
                player.takeDamage(48 * this.strengthMultiplier);
              }
            }
          }

          if (this.attackTimer >= 3.2) {
            this.attackTimer = 0;
            const roll = Math.random();
            this.isAttacking = true;
            this.attackDuration = 1.1;
            this.attackMaxDuration = 1.1;

            if (roll < 0.6) {
              this.campaignAction = 'aoe';
              sound.playGong();
              this.telegraphZone = {
                x: target.x,
                y: target.y,
                radius: 175,
                maxTimer: 1.1,
                timer: 1.1
              };
              floatingTexts.push(new FloatingText(this.x, this.y - 120, uiText('大日如来神掌 · 五指山天降!', 'Tathagata Palm · Five-Finger Mountain Descends!'), '#facc15', 20));
            } else {
              this.campaignAction = 'ranged';
              const count = 10;
              for (let i = 0; i < count; i++) {
                const ang = (i * Math.PI * 2 / count) + (Date.now() * 0.001);
                projectiles.push(new Projectile(this.x, this.y + 60, Math.cos(ang)*240, Math.sin(ang)*240, 32 * this.strengthMultiplier, '#fef08a', true));
              }
              fxList.push(new Shockwave(this.x, this.y + 60, 220, '#fef08a'));
            }
          }
          return;
        }

        if (this.behavior === 'hound_attack') {
          // Center-to-center distance must include the victim's radius. The old
          // fixed 60px threshold was smaller than boss crowd spacing, so the
          // allied hound could chase a large boss forever without biting it.
          const attackReach = this.radius + target.radius + 34;
          if (this.state === 'hound_empowered_slam' && this.isAttacking) {
            const slamProgress = Math.max(0, Math.min(1, 1 - this.attackDuration / Math.max(0.001, this.attackMaxDuration)));
            const flightProgress = Math.min(1, slamProgress / 0.72);
            const easedFlight = flightProgress * flightProgress * (3 - 2 * flightProgress);
            this.x = this.houndSlamStartX + (this.houndSlamTargetX - this.houndSlamStartX) * easedFlight;
            this.y = this.houndSlamStartY + (this.houndSlamTargetY - this.houndSlamStartY) * easedFlight;
            this.houndVisualLift = Math.sin(flightProgress * Math.PI) * (118 + Math.min(36, (this.houndSlamRank - 1) * 6));
            this.vx = 0;
            this.vy = 0;

            if (!this.shotFired && slamProgress >= 0.72) {
              this.shotFired = true;
              this.x = this.houndSlamTargetX;
              this.y = this.houndSlamTargetY;
              this.houndVisualLift = 0;
              const specialRank = Math.max(1, this.houndSlamRank || 1);
              const specialSteps = specialRank - 1;
              const houndTraining = player.erlangSkillEffects || {};
              const slamRadius = 118 + Math.min(62, specialSteps * 11);
              const stunDuration = Math.min(1.65, 0.72 + specialSteps * 0.11 + (houndTraining.houndStun || 0));
              const slamDamage = 165
                * (1 + specialSteps * 0.28)
                * (1 + (houndTraining.houndDamage || 0))
                * (1 + (player.alignmentSpecialDamage || 0))
                * (player.metaDamageMultiplier || 1)
                * (player.isManifested ? 1.20 : 1);
              let struck = 0;
              let consumedMark = false;
              enemies.forEach(enemy => {
                if (!enemy.alive || enemy.isAlly || enemy.isDying) return;
                const distance = Math.hypot(enemy.x - this.x, enemy.y - this.y);
                if (distance > slamRadius + enemy.radius) return;
                const isPrimary = enemy === this.attackTarget;
                const marked = enemy.judgmentMarkTimer > 0;
                const radialScale = isPrimary ? 1 : Math.max(0.58, 0.78 - distance / Math.max(1, slamRadius) * 0.20);
                enemy.takeDamage(slamDamage * radialScale * (marked ? 1.35 : 1), false, true);
                enemy.applyFreeze(enemy.isBoss ? stunDuration * 0.62 : stunDuration);
                const knockAngle = Math.atan2(enemy.y - this.y, enemy.x - this.x);
                enemy.knockbackX += Math.cos(knockAngle) * (isPrimary ? 210 : 145);
                enemy.knockbackY += Math.sin(knockAngle) * (isPrimary ? 210 : 145);
                if (isPrimary && marked) {
                  enemy.judgmentMarkTimer = 0;
                  consumedMark = true;
                }
                fxList.push(new RadialSparksFX(enemy.x, enemy.y, isPrimary ? 12 : 7, '#c4b5fd', isPrimary ? 52 : 30));
                struck++;
              });
              if (consumedMark) player.houndCooldown = Math.max(0, player.houndCooldown - 1);
              fxList.push(new Shockwave(this.x, this.y, slamRadius, '#8b5cf6'));
              fxList.push(new HadesMagicCircleAOEFX(this.x, this.y, slamRadius, 0.58, '#60a5fa'));
              fxList.push(new AnimatedLightningStrike(this.x, this.y));
              floatingTexts.push(new FloatingText(
                this.x, this.y - 82,
                uiText(
                  `神雷震击 ${Math.round(slamDamage)} · 定身 ${stunDuration.toFixed(1)}秒`,
                  `Thunder Slam ${Math.round(slamDamage)} · Stun ${stunDuration.toFixed(1)}s`
                ),
                struck ? '#fde68a' : '#c4b5fd', 15
              ));
              sound.playLightning();
              sound.playStaffSmash(false);
              createScreenShake(3);
            }
            this.clampBoundary();
            return;
          }

          if (this.isAttacking) {
            const attackProgress = 1 - this.attackDuration / this.attackMaxDuration;
            if (attackProgress >= 0.16 && attackProgress <= 0.62) {
              this.vx = Math.cos(this.attackAngle) * this.speed * 0.92;
              this.vy = Math.sin(this.attackAngle) * this.speed * 0.92;
            } else {
              this.vx *= 0.42;
              this.vy *= 0.42;
            }
          } else if (distToTarget > attackReach) {
            this.vx = Math.cos(angleToTarget) * this.speed * speedMod;
            this.vy = Math.sin(angleToTarget) * this.speed * speedMod;
          } else {
            this.vx *= 0.5;
            this.vy *= 0.5;
            if (this.attackCooldown <= 0 && !this.isAttacking) {
              this.isAttacking = true;
              this.state = 'hound_pounce';
              this.animClock = 0;
              this.attackDuration = 0.52;
              this.attackMaxDuration = 0.52;
              const houndRank = this.isAlly && player.hasBoon('erlang_hound') ? player.getBoonLevel('erlang_hound') : 1;
              this.attackCooldown = Math.max(0.48, (0.92 - 0.06 * (houndRank - 1)) * (1 - (player.erlangSkillEffects?.houndCooldown || 0) * .5));
              this.attackAngle = angleToTarget;
              this.attackTarget = target;
              this.shotFired = false;
              sound.playHoundBark();
            }
          }

          if (this.isAttacking && !this.shotFired && this.attackDuration <= this.attackMaxDuration * 0.42) {
            this.shotFired = true;
            const biteTarget = this.attackTarget && this.attackTarget.alive ? this.attackTarget : target;
            const biteDistance = Math.hypot(biteTarget.x - this.x, biteTarget.y - this.y);
            const biteReach = this.radius + biteTarget.radius + 48;
            if (biteDistance <= biteReach) {
              const isCommandedCompanion = this.isAlly && gameState.playableHero === 'erlang';
              const marked = biteTarget.judgmentMarkTimer > 0;
              const houndRank = this.isAlly && player.hasBoon('erlang_hound') ? player.getBoonLevel('erlang_hound') : 1;
              const biteDamage = isCommandedCompanion
                ? 110 * (1 + (player.erlangSkillEffects?.houndDamage || 0)) * (player.metaDamageMultiplier || 1) * (marked ? 1.60 : 1)
                : (this.isAlly ? 80 * (1 + 0.30 * (houndRank - 1)) * (player.metaDamageMultiplier || 1) : 18);
              biteTarget.takeDamage(biteDamage, false, this.isAlly);
              if (isCommandedCompanion && marked) {
                biteTarget.judgmentMarkTimer = 0;
                player.houndCooldown = Math.max(0, player.houndCooldown - 1);
                fxList.push(new AnimatedLightningStrike(biteTarget.x, biteTarget.y));
              }
              if (this.isAlly) biteTarget.applyFreeze(0.24 + (player.erlangSkillEffects?.houndStun || 0));
              biteTarget.knockbackX += Math.cos(this.attackAngle) * (this.isAlly ? 145 : 70);
              biteTarget.knockbackY += Math.sin(this.attackAngle) * (this.isAlly ? 145 : 70);
              fxList.push(new EnemyClawSwipeFX(this.x, this.y, this.attackAngle, 72, this.isAlly ? '#facc15' : '#ef4444'));
              fxList.push(new RadialSparksFX(biteTarget.x, biteTarget.y, 8, this.isAlly ? '#fde68a' : '#ef4444', 34));
              sound.playStaffHit(false);
            }
          }
        } else if (this.behavior === 'campaign_boss') {
          const profile = this.campaignBossProfile;
          if (this.isAttacking) {
            this.vx = 0;
            this.vy = 0;
            const actionProgress = Math.max(0, Math.min(1, 1 - this.attackDuration / Math.max(0.001, this.attackMaxDuration)));
            if (this.pendingBossAttack?.type === 'campaign_mobility') {
              const eased = actionProgress * actionProgress * (3 - 2 * actionProgress);
              if (profile.mobility === 'teleport') {
                if (actionProgress >= 0.48) {
                  this.x = this.mobilityTargetX;
                  this.y = this.mobilityTargetY;
                }
                this.mobilityLift = Math.sin(actionProgress * Math.PI) * 72;
              } else {
                this.x = this.mobilityStartX + (this.mobilityTargetX - this.mobilityStartX) * eased;
                this.y = this.mobilityStartY + (this.mobilityTargetY - this.mobilityStartY) * eased;
                this.mobilityLift = Math.sin(actionProgress * Math.PI) * (profile.mobility === 'fly' ? 92 : 118);
              }
            }
          } else {
            this.mobilityLift = 0;
            if (distToTarget > 315) {
              this.vx = Math.cos(angleToTarget) * this.speed * 1.38 * speedMod;
              this.vy = Math.sin(angleToTarget) * this.speed * 1.38 * speedMod;
            } else {
              const orbitDirection = this.campaignActionIndex % 2 === 0 ? 1 : -1;
              this.vx = Math.cos(angleToTarget + orbitDirection * Math.PI / 2) * this.speed * 0.72 * speedMod;
              this.vy = Math.sin(angleToTarget + orbitDirection * Math.PI / 2) * this.speed * 0.72 * speedMod;
            }

            if (this.attackCooldown <= 0) {
              const action = ['mobility', 'ranged', 'aoe'][this.campaignActionIndex % 3];
              this.campaignActionIndex++;
              this.campaignAction = action;
              this.state = action;
              this.isAttacking = true;
              this.attackAngle = angleToTarget;
              this.shotFired = false;
              const duration = action === 'mobility' ? 0.78 : (action === 'ranged' ? 0.88 : 1.18);
              this.attackDuration = duration;
              this.attackMaxDuration = duration;
              this.attackCooldown = (action === 'aoe' ? 1.55 : 1.12) * (gameState.isNewGamePlus ? 0.90 : 1);

              if (action === 'mobility') {
                const side = this.campaignActionIndex % 2 === 0 ? 1 : -1;
                const landingDistance = this.radius + player.radius + 105;
                this.mobilityStartX = this.x;
                this.mobilityStartY = this.y;
                this.mobilityTargetX = Math.max(-1050, Math.min(1050, player.x - Math.cos(angleToTarget) * landingDistance + Math.cos(angleToTarget + Math.PI / 2) * side * 78));
                this.mobilityTargetY = Math.max(-750, Math.min(750, player.y - Math.sin(angleToTarget) * landingDistance + Math.sin(angleToTarget + Math.PI / 2) * side * 78));
                this.pendingBossAttack = { type: 'campaign_mobility', angle: angleToTarget, targetX: this.mobilityTargetX, targetY: this.mobilityTargetY, profile, contactAt: 0.84 };
                fxList.push(new BossSkillAnimatedFX(this.x, this.y, 2, duration, 110, profile.color, true));
              } else if (action === 'ranged') {
                this.pendingBossAttack = { type: 'campaign_ranged', angle: angleToTarget, profile, contactAt: 0.55 };
                const label = gameState.language === 'en' ? profile.rangedEn : profile.rangedZh;
                floatingTexts.push(new FloatingText(this.x, this.y - this.radius - 32, label, profile.color, 18));
              } else {
                this.pendingBossAttack = { type: 'campaign_aoe', angle: angleToTarget, profile, contactAt: 0.72 };
                fxList.push(new BossSkillAnimatedFX(this.x, this.y, 1, duration, profile.aoeRadius, profile.color, true));
                const label = gameState.language === 'en' ? profile.aoeEn : profile.aoeZh;
                floatingTexts.push(new FloatingText(this.x, this.y - this.radius - 32, label, profile.color, 19));
              }
            }
          }
        } else if (this.behavior === 'boss_erlang') {
          this.vx = Math.cos(angleToTarget) * this.speed * 0.7 * speedMod;
          this.vy = Math.sin(angleToTarget) * this.speed * 0.7 * speedMod;

          if (this.attackTimer >= 2.2) {
            this.attackTimer = 0;
            this.isAttacking = true;
            this.attackDuration = 0.72;
            this.attackMaxDuration = 0.72;
            this.attackAngle = angleToTarget;
            const roll = Math.random();

            if (roll < 0.5) {
              sound.playLightning();
              this.state = 'thrust';
              this.pendingBossAttack = { type: 'erlang_thrust', angle: angleToTarget, contactAt: 0.52 };
            } else {
              sound.playHoundBark();
              this.state = 'command';
              this.pendingBossAttack = { type: 'erlang_command', angle: angleToTarget, targetX: target.x, targetY: target.y, contactAt: 0.58 };
            }
          }
        } else if (this.behavior === 'boss_spider') {
          this.vx = Math.cos(angleToTarget) * this.speed * 0.7 * speedMod;
          this.vy = Math.sin(angleToTarget) * this.speed * 0.7 * speedMod;

          if (this.attackTimer >= 2.2) {
            this.attackTimer = 0;
            this.isAttacking = true;
            this.attackDuration = 0.68;
            this.attackMaxDuration = 0.68;
            this.attackAngle = angleToTarget;
            this.pendingBossAttack = { type: 'spider_fan', angle: angleToTarget, contactAt: 0.56 };
          }
        } else if (this.behavior === 'boss_baigu') {
          this.vx = Math.cos(angleToTarget) * this.speed * 0.75 * speedMod;
          this.vy = Math.sin(angleToTarget) * this.speed * 0.75 * speedMod;

          if (this.attackTimer >= 2.0) {
            this.attackTimer = 0;
            this.isAttacking = true;
            this.attackDuration = 0.8;
            this.attackMaxDuration = 0.8;
            this.attackAngle = angleToTarget;
            this.pendingBossAttack = { type: 'baigu_ring', angle: angleToTarget, contactAt: 0.54 };
          }
        } else if (this.behavior === 'boss_jin_yin') {
          this.vx = Math.cos(angleToTarget) * this.speed * 0.8 * speedMod;
          this.vy = Math.sin(angleToTarget) * this.speed * 0.8 * speedMod;

          if (this.attackTimer >= 1.8) {
            this.attackTimer = 0;
            this.isAttacking = true;
            this.attackDuration = 0.7;
            this.attackMaxDuration = 0.7;
            this.attackAngle = angleToTarget;
            this.pendingBossAttack = { type: 'jin_yin_fan', angle: angleToTarget, contactAt: 0.55 };
          }
        } else if (this.behavior === 'boss_tongbei') {
          const phaseMult = this.phase === 2 ? 1.4 : 1.0;
          this.vx = Math.cos(angleToTarget) * this.speed * phaseMult * speedMod;
          this.vy = Math.sin(angleToTarget) * this.speed * phaseMult * speedMod;

          if (this.attackTimer >= (this.phase === 2 ? 1.4 : 2.0)) {
            this.attackTimer = 0;
            this.isAttacking = true;
            this.attackDuration = 0.72;
            this.attackMaxDuration = 0.72;
            this.attackAngle = angleToTarget;
            const count = this.phase === 2 ? 16 : 10;
            this.pendingBossAttack = {
              type: 'tongbei_ring', angle: angleToTarget, count,
              offset: Math.sin(this.animClock * 2) * 0.5,
              damage: this.phase === 2 ? 40 : 30,
              contactAt: 0.54
            };
          }
        } else if (this.behavior === 'ranged_archer') {
          // RANGED SNIPER: Tian Archer (灵霄神射弓手)
          if (distToTarget < 220) {
            this.vx = -Math.cos(angleToTarget) * this.speed * 0.75 * speedMod;
            this.vy = -Math.sin(angleToTarget) * this.speed * 0.75 * speedMod;
          } else if (distToTarget > 380) {
            this.vx = Math.cos(angleToTarget) * this.speed * speedMod;
            this.vy = Math.sin(angleToTarget) * this.speed * speedMod;
          } else {
            this.vx = Math.cos(angleToTarget + Math.PI / 2) * this.speed * 0.35 * speedMod;
            this.vy = Math.sin(angleToTarget + Math.PI / 2) * this.speed * 0.35 * speedMod;
          }

          if (this.attackCooldown <= 0 && !this.isAttacking) {
            this.isAttacking = true;
            this.attackDuration = 0.5;
            this.attackMaxDuration = 0.5;
            this.attackCooldown = 1.7 + Math.random() * 0.5;
            this.attackAngle = angleToTarget;
            this.shotFired = false;
          }

          if (this.isAttacking && !this.shotFired && this.attackDuration <= 0.22) {
            this.shotFired = true;
            sound.playBowShoot();
            projectiles.push(new Projectile(this.x, this.y, Math.cos(this.attackAngle) * 360, Math.sin(this.attackAngle) * 360, 24, '#facc15', true));
            fxList.push(new RadialSparksFX(this.x, this.y, 8, '#facc15', 35));
          }
        } else if (this.behavior === 'ranged_spider') {
          // RANGED VENOM SPITTER: Cave Spider (盘丝洞毒蛛兵)
          if (distToTarget < 160) {
            this.vx = -Math.cos(angleToTarget) * this.speed * 0.8 * speedMod;
            this.vy = -Math.sin(angleToTarget) * this.speed * 0.8 * speedMod;
          } else if (distToTarget > 280) {
            this.vx = Math.cos(angleToTarget) * this.speed * speedMod;
            this.vy = Math.sin(angleToTarget) * this.speed * speedMod;
          } else {
            this.vx = Math.cos(angleToTarget + Math.PI / 2) * this.speed * 0.4 * speedMod;
            this.vy = Math.sin(angleToTarget + Math.PI / 2) * this.speed * 0.4 * speedMod;
          }

          if (this.attackCooldown <= 0 && !this.isAttacking) {
            this.isAttacking = true;
            this.attackDuration = 0.45;
            this.attackMaxDuration = 0.45;
            this.attackCooldown = 1.5 + Math.random() * 0.4;
            this.attackAngle = angleToTarget;
            this.shotFired = false;
          }

          if (this.isAttacking && !this.shotFired && this.attackDuration <= 0.2) {
            this.shotFired = true;
            projectiles.push(new Projectile(this.x, this.y, Math.cos(this.attackAngle) * 300, Math.sin(this.attackAngle) * 300, 20, '#22c55e', true));
            fxList.push(new RadialSparksFX(this.x, this.y, 8, '#22c55e', 35));
          }
        } else if (this.behavior === 'aoe_ghost') {
          // AOE CASTER: Nether Ghost (幽冥鬼使法师)
          if (distToTarget > 200) {
            this.vx = Math.cos(angleToTarget) * this.speed * speedMod;
            this.vy = Math.sin(angleToTarget) * this.speed * speedMod;
          } else if (distToTarget < 120) {
            this.vx = -Math.cos(angleToTarget) * this.speed * 0.6 * speedMod;
            this.vy = -Math.sin(angleToTarget) * this.speed * 0.6 * speedMod;
          } else {
            this.vx *= 0.7;
            this.vy *= 0.7;
          }

          if (this.attackCooldown <= 0 && !this.isAttacking) {
            this.isAttacking = true;
            this.attackDuration = 0.55;
            this.attackMaxDuration = 0.55;
            this.attackCooldown = 2.0 + Math.random() * 0.5;
            this.attackAngle = angleToTarget;
            this.shotFired = false;
          }

          if (this.isAttacking && !this.shotFired && this.attackDuration <= 0.15) {
            this.shotFired = true;
            sound.playJadeChime();
            fxList.push(new NetherGhostSoulAOEFX(this.x, this.y, 160));
            if (distToTarget <= 160) {
              target.takeDamage(26);
              createScreenShake(6);
            }
          }
        } else if (this.behavior === 'mini_boss_golem') {
          // TANKY MINI-BOSS: Bagua Golem (太上八卦巨傀)
          const reach = 85;
          if (distToTarget > reach + target.radius) {
            this.vx = Math.cos(angleToTarget) * this.speed * speedMod;
            this.vy = Math.sin(angleToTarget) * this.speed * speedMod;
          } else {
            this.vx *= 0.4;
            this.vy *= 0.4;
          }

          if (distToTarget <= reach + target.radius + 20 && this.attackCooldown <= 0 && !this.isAttacking) {
            this.isAttacking = true;
            this.attackDuration = 0.5;
            this.attackMaxDuration = 0.5;
            this.attackCooldown = 1.6 + Math.random() * 0.4;
            this.attackAngle = angleToTarget;
            this.shotFired = false;
          }

          if (this.isAttacking && !this.shotFired && this.attackDuration <= 0.18) {
            this.shotFired = true;
            sound.playStaffSmash(true);
            createScreenShake(12);
            fxList.push(new GroundFissureFX(this.x + Math.cos(this.attackAngle) * 60, this.y + Math.sin(this.attackAngle) * 60, this.attackAngle, 140, '#f97316'));
            fxList.push(new Shockwave(this.x + Math.cos(this.attackAngle) * 60, this.y + Math.sin(this.attackAngle) * 60, 110, '#f97316'));
            if (distToTarget <= 120) {
              target.takeDamage(42);
            }
          }
        } else if (this.behavior === 'mini_boss_commander') {
          // TANKY MINI-BOSS: Heavenly Commander (金甲神威统帅)
          const reach = 90;
          if (distToTarget > reach + target.radius) {
            this.vx = Math.cos(angleToTarget) * this.speed * speedMod;
            this.vy = Math.sin(angleToTarget) * this.speed * speedMod;
          } else {
            this.vx *= 0.4;
            this.vy *= 0.4;
          }

          if (distToTarget <= reach + target.radius + 25 && this.attackCooldown <= 0 && !this.isAttacking) {
            this.isAttacking = true;
            this.attackDuration = 0.45;
            this.attackMaxDuration = 0.45;
            this.attackCooldown = 1.5 + Math.random() * 0.4;
            this.attackAngle = angleToTarget;
            this.shotFired = false;
          }

          if (this.isAttacking && !this.shotFired && this.attackDuration <= 0.2) {
            this.shotFired = true;
            sound.playStaffSwing(2, true);
            createScreenShake(10);
            fxList.push(new ElementalSlashFX(this.x, this.y, this.attackAngle, 'golden', 190));
            if (distToTarget <= 125) {
              target.takeDamage(45);
              target.knockbackX += Math.cos(this.attackAngle) * 260;
              target.knockbackY += Math.sin(this.attackAngle) * 260;
            }
          }
        } else {
          // Melee Swarmers: tianbing (shield_soldier) & demon_ape (swarmer)
          const reach = (this.behavior === 'shield_soldier' ? 64 : 50);

          if (this.isAttacking) {
            this.vx = Math.cos(this.attackAngle) * 140 * speedMod;
            this.vy = Math.sin(this.attackAngle) * 140 * speedMod;
          } else if (distToTarget > reach + target.radius) {
            this.vx = Math.cos(angleToTarget) * this.speed * speedMod;
            this.vy = Math.sin(angleToTarget) * this.speed * speedMod;
          } else {
            this.vx *= 0.5;
            this.vy *= 0.5;
          }

          if (distToTarget <= reach + target.radius + 15 && this.attackCooldown <= 0 && !this.isAttacking) {
            this.isAttacking = true;
            this.attackDuration = 0.38;
            this.attackMaxDuration = 0.38;
            this.attackCooldown = 1.1 + Math.random() * 0.4;
            this.attackAngle = angleToTarget;
            this.shotFired = false;
          }

          if (this.isAttacking && !this.shotFired && this.attackDuration <= 0.16) {
            this.shotFired = true;
            if (this.typeKey === 'tianbing') {
              sound.playStaffSwing(0, false);
              fxList.push(new EnemySpearThrustFX(this.x, this.y, this.attackAngle, 85, '#facc15'));
              if (distToTarget <= reach + target.radius + 22) {
                target.takeDamage(18);
                fxList.push(new RadialSparksFX(target.x, target.y, 10, '#facc15', 40));
              }
            } else {
              sound.playStaffSwing(0, false);
              fxList.push(new EnemyClawSwipeFX(this.x, this.y, this.attackAngle, 65, '#ef4444'));
              if (distToTarget <= reach + target.radius + 22) target.takeDamage(15);
            }
          }
        }

        this.x += (this.vx + this.knockbackX) * dt;
        this.y += (this.vy + this.knockbackY) * dt;

        // Non-damaging physical body collision separation (MK only takes damage from attacks, never from touching enemies):
        if (!this.isDying && this.alive) {
          const distP = Math.hypot(player.x - this.x, player.y - this.y);
          const minDist = player.radius + this.radius;
          if (distP < minDist && distP > 0) {
            const push = (minDist - distP) * 0.5;
            const nx = (this.x - player.x) / distP;
            const ny = (this.y - player.y) / distP;
            this.x += nx * push * 0.6;
            this.y += ny * push * 0.6;
            player.x -= nx * push * 0.4;
            player.y -= ny * push * 0.4;
          }
        }

        this.clampBoundary();
      }

      clampBoundary() {
        const arenaHalfW = 1160;
        const arenaHalfH = 860;
        if (this.x < -arenaHalfW) { this.x = -arenaHalfW; this.vx = 0; this.knockbackX = 0; }
        if (this.x > arenaHalfW) { this.x = arenaHalfW; this.vx = 0; this.knockbackX = 0; }
        if (this.y < -arenaHalfH) { this.y = -arenaHalfH; this.vy = 0; this.knockbackY = 0; }
        if (this.y > arenaHalfH) { this.y = arenaHalfH; this.vy = 0; this.knockbackY = 0; }
      }

      draw(ctx) {
        if (!this.alive && !this.isDying) return;
        ctx.save();
        ctx.translate(this.x, this.y);
        const showingMeleeContactHold = this.meleeContactHoldTimer > 0;
        const displayIsDying = this.isDying && !showingMeleeContactHold;
        if (showingMeleeContactHold) {
          ctx.translate(this.knockbackX * .018, this.knockbackY * .018);
          ctx.filter = 'brightness(1.55) saturate(1.18)';
        }

        // DEATH DISSOLUTION ANIMATION
        if (displayIsDying) {
          const deathProg = 1 - (this.deathTimer / this.deathMaxDuration);
          ctx.globalAlpha = Math.max(0, 1 - deathProg);
          ctx.translate(0, -deathProg * 35);
          ctx.scale(1 + deathProg * 0.2, 1 + deathProg * 0.2);
        }

        // KNOCKDOWN & RECOVERY ANIMATION
        if (this.isKnockedDown) {
          const kdProg = 1 - (this.knockdownTimer / this.knockdownMaxDuration);
          let tilt = this.knockdownAngle;
          if (kdProg > 0.6) {
            const getUpProg = (kdProg - 0.6) / 0.4;
            tilt = this.knockdownAngle * (1 - Math.sin(getUpProg * Math.PI / 2));
          }
          ctx.rotate(tilt);
          ctx.translate(0, 14);
        }

        const isMoving = Math.hypot(this.vx, this.vy) > 10;
        const realEnemyImg = loadedImages['enemies_real_anims'];
        const realBossImg = loadedImages['bosses_real_anims'];
        const specialEnemyImg = loadedImages['special_enemies_anims'];

        const isTianbing = (this.typeKey === 'tianbing');
        const isDemonApe = (this.typeKey === 'demon_ape');
        const isBaigu = (this.typeKey === 'boss_baigu');
        const isTongbei = (this.typeKey === 'boss_tongbei');

        const isArcher = (this.typeKey === 'tian_archer');
        const isGhost = (this.typeKey === 'nether_ghost');
        const isGolem = (this.typeKey === 'bagua_golem');
        const isSpider = (this.typeKey === 'cave_spider');
        const isCommander = (this.typeKey === 'tianbing_commander');
        // These enemy types used to swap to legacy 160px sheets while attacking
        // or dying.  Those sheets depict different costumes/creatures and some
        // cells contain only a projectile or a cropped limb.  Keep one canonical
        // body atlas for every state; gameplay projectiles and hit FX remain
        // separate layers and therefore cannot replace or clip the character.
        const useCanonicalEnemyAtlas = isTianbing || isDemonApe || isArcher ||
          isGhost || isGolem || isSpider || isCommander;

        if (this.telegraphZone) {
          const tz = this.telegraphZone;
          ctx.save();
          ctx.translate(tz.x - this.x, tz.y - this.y);

          const progress = 1 - (tz.timer / tz.maxTimer);

          ctx.beginPath();
          ctx.arc(0, 0, tz.radius, 0, Math.PI * 2);
          ctx.strokeStyle = 'rgba(239, 68, 68, 0.85)';
          ctx.lineWidth = 3;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(0, 0, tz.radius * progress, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(250, 204, 21, 0.35)';
          ctx.fill();

          ctx.font = getCanvasFont(15, 700);
          ctx.fillStyle = '#facc15';
          ctx.textAlign = 'center';
          ctx.fillText(uiText('⚠️ 如来神掌降临 (快按空格闪避!)', "⚠️ Buddha's Palm incoming (Press Space to dodge!)"), 0, -tz.radius - 10);

          ctx.restore();
        }

        if (this.typeKey === 'campaign_erlang') {
          // Campaign Yang Jian shares the definitive playable identity: visible
          // cyan third eye, blue-purple-white robes, and three-pointed spear.
          // Reuse the complete 35-frame board so boss and hero never swap art.
          const erlangImg = loadedImages['erlang_player_actions'];
          if (erlangImg && erlangImg.complete && erlangImg.naturalWidth > 0) {
            const cell = 240;
            let row = 0;
            let frame = 0;
            if (displayIsDying || this.isSubdued) {
              row = 4;
              frame = 6;
            } else if (this.isKnockedDown || this.hurtTimer > 0) {
              row = 1;
              frame = 6;
            } else if (this.isAttacking) {
              const progress = Math.max(0, Math.min(0.999, 1 - this.attackDuration / Math.max(0.001, this.attackMaxDuration)));
              row = this.campaignAction === 'mobility' ? 3 : (this.campaignAction === 'ranged' || this.campaignAction === 'aoe' ? 2 : 1);
              frame = Math.min(6, Math.floor(progress * 7));
            } else if (isMoving) {
              row = 0;
              frame = 2 + Math.floor((this.animClock / 0.10) % 5);
            } else {
              frame = Math.floor((this.animClock / 0.34) % 2);
            }
            const scale = 1.18 * PACKED_VISUAL_SCALE_240;
            const drawSize = cell * scale;
            const footPivot = (cell - 56) * scale;
            const hoverBob = this.campaignAction === 'mobility' && this.isAttacking ? Math.sin(this.animClock * 10) * 3 : 0;
            ctx.save();
            ctx.translate(0, -this.mobilityLift - hoverBob);
            if (this.facing === -1) ctx.scale(-1, 1);
            ctx.shadowColor = '#60a5fa';
            ctx.shadowBlur = 12;
            ctx.drawImage(erlangImg, frame * cell, row * cell, cell, cell, -drawSize / 2, 42 - footPivot, drawSize, drawSize);
            ctx.restore();
          }
        } else if (this.campaignSheet) {
          const campaignImg = loadedImages[this.campaignSheet];
          if (campaignImg && campaignImg.complete && campaignImg.naturalWidth > 0) {
            const cellW = 200;
            const cellH = 200;
            let c = 0;
            if (displayIsDying) c = 6;
            else if (showingMeleeContactHold) c = 5;
            else if (this.isSubdued) c = 5;
            else if (this.isKnockedDown || this.hurtTimer > 0) c = 5;
            else if (this.isAttacking) {
              const progress = Math.max(0, Math.min(0.999, 1 - this.attackDuration / Math.max(0.001, this.attackMaxDuration)));
              if (this.campaignAction === 'mobility') c = 1;
              else if (this.campaignAction === 'ranged') c = progress < 0.48 ? 2 : 3;
              else if (this.campaignAction === 'aoe') c = progress < 0.56 ? 2 : 4;
              else c = 2 + Math.min(2, Math.floor(progress * 3));
            } else if (isMoving) c = 1;
            const packedCampaignScale = this.campaignScale * PACKED_VISUAL_SCALE_200;
            const drawW = cellW * packedCampaignScale;
            const drawH = cellH * packedCampaignScale;
            const footPivot = (cellH - 48) * packedCampaignScale;
            ctx.save();
            const profile = this.campaignBossProfile;
            const hoverBob = this.isBoss && (profile?.mobility === 'fly' || this.isBuddhaBoss) ? Math.sin(this.animClock * 5.2) * 7 : 0;
            ctx.translate(0, -this.mobilityLift - hoverBob);
            if (this.facing === -1) ctx.scale(-1, 1);
            if (this.campaignAction === 'mobility' && this.isAttacking) {
              ctx.save();
              ctx.globalAlpha = 0.22;
              const trailX = (this.mobilityStartX - this.x) * 0.32 * (this.facing === -1 ? -1 : 1);
              const trailY = (this.mobilityStartY - this.y) * 0.32;
              ctx.drawImage(campaignImg, cellW, this.campaignRow * cellH, cellW, cellH, -drawW / 2 + trailX, 42 - footPivot + trailY, drawW, drawH);
              ctx.restore();
            }
            ctx.drawImage(campaignImg, c * cellW, this.campaignRow * cellH, cellW, cellH, -drawW / 2, 42 - footPivot, drawW, drawH);
            ctx.restore();
          }
        } else if (this.isBuddhaBoss) {
          const buddhaImg = loadedImages['buddha_colossal'];
          if (buddhaImg && buddhaImg.complete && buddhaImg.naturalWidth > 0) {
            const cellW = 256;
            const cellH = 256;
            const c = Math.floor((this.animClock / 0.15) % 5);

            const drawW = 340 * PACKED_VISUAL_SCALE_256;
            const drawH = 340 * PACKED_VISUAL_SCALE_256;

            ctx.save();
            ctx.rotate(this.animClock * 0.5);
            ctx.beginPath();
            ctx.arc(0, -30, 160, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(250, 204, 21, 0.3)';
            ctx.lineWidth = 14;
            ctx.stroke();
            ctx.restore();

            ctx.drawImage(buddhaImg, c * cellW, 0, cellW, cellH, -drawW / 2, -drawH / 2 - 20, drawW, drawH);
          }
        } else if (this.isErlangBoss || this.isHound) {
          const img = loadedImages['erlang_and_dog'];
          const houndAttackImg = loadedImages['xiaotianquan_attack'];
          const houndSlamImg = loadedImages['xiaotianquan_empowered_slam'];
          if (this.isHound && this.state === 'hound_empowered_slam' && this.isAttacking && houndSlamImg && houndSlamImg.complete && houndSlamImg.naturalWidth > 0) {
            const cell = 240;
            const scale = 0.92 * PACKED_VISUAL_SCALE_240;
            const attackProgress = Math.max(0, Math.min(0.999, 1 - this.attackDuration / Math.max(0.001, this.attackMaxDuration)));
            const c = Math.min(6, Math.floor(attackProgress * 7));
            ctx.save();
            ctx.translate(0, -(this.houndVisualLift || 0));
            if (this.facing === -1) ctx.scale(-1, 1);
            // The ImageGen-authored cells include their own gathering lightning,
            // meteor trail, impact ring, and recovery sparks. Draw the complete
            // frame instead of reconstructing the power-up from generic shapes.
            ctx.drawImage(houndSlamImg, c * cell, 0, cell, cell, -cell * scale / 2, 40 - (cell - 56) * scale, cell * scale, cell * scale);
            ctx.restore();
          } else if (this.isHound && this.isAttacking && houndAttackImg && houndAttackImg.complete && houndAttackImg.naturalWidth > 0) {
            const cell = 220;
            const scale = 0.63 * PACKED_VISUAL_SCALE_220;
            const attackProgress = Math.max(0, Math.min(0.999, 1 - this.attackDuration / Math.max(0.001, this.attackMaxDuration)));
            const c = Math.min(4, Math.floor(attackProgress * 5));
            ctx.save();
            if (this.facing === -1) ctx.scale(-1, 1);
            // The generated strip is bottom-aligned with 34px transparent
            // gutters. Keep its paws on the same ground pivot as the run loop.
            ctx.drawImage(houndAttackImg, c * cell, 0, cell, cell, -cell * scale / 2, 40 - (cell - 52) * scale, cell * scale, cell * scale);
            ctx.restore();
          } else if (img && img.complete && img.naturalWidth > 0) {
            const cellW = 160;
            const cellH = 160;

            let r = 0;
            let c = 0;
            if (this.isHound) {
              if (this.isAttacking) {
                // Row 4 is the authored five-frame crouch, leap, bite, impact,
                // and recovery sequence. Row 3 remains the four-frame run loop.
                r = 4;
                const attackProgress = Math.max(0, Math.min(0.999, 1 - this.attackDuration / Math.max(0.001, this.attackMaxDuration)));
                c = Math.min(4, Math.floor(attackProgress * 5));
              } else {
                r = 3;
                c = isMoving ? Math.floor((this.animClock / 0.12) % 4) : 0;
              }
            } else {
              // The optional legacy Erlang sheet's thrust/command rows contain
              // effect-only and waist-cropped cells.  Campaign Erlang has a full
              // authored atlas; for this legacy encounter retain the complete
              // identity reference and let its existing lightning/projectile FX
              // communicate the action without replacing Yang Jian's body.
              r = 0;
              c = 0;
            }

            const scale = (this.isErlangBoss ? 1.35 : 0.85) * PACKED_VISUAL_SCALE_160;
            const drawW = cellW * scale;
            const drawH = cellH * scale;

            ctx.save();
            if (this.facing === -1) {
              ctx.scale(-1, 1);
            }
            const hover = this.isErlangBoss ? Math.sin(this.animClock * 4.8) * 3 : 0;
            ctx.drawImage(img, c * cellW, r * cellH, cellW, cellH, -drawW / 2, 40 - (cellH - 38) * scale + hover, drawW, drawH);
            ctx.restore();
          }
        } else if (!useCanonicalEnemyAtlas && (isArcher || isGhost || isGolem || isSpider || isCommander) && specialEnemyImg && specialEnemyImg.complete && specialEnemyImg.naturalWidth > 0 && (displayIsDying || this.isAttacking)) {
          const cellW = 160;
          const cellH = 160;
          let r = 0;
          let c = 0;
          let scale = 1.0;

          if (displayIsDying) {
            r = 5; // Sparkling spirit dissolution
            const prog = 1 - (this.deathTimer / this.deathMaxDuration);
            c = Math.min(3, Math.floor(prog * 4));
          } else if (isArcher) {
            r = 0; // Drawing bow & shooting golden arrow
            const prog = 1 - (this.attackDuration / this.attackMaxDuration);
            c = Math.min(5, Math.floor(prog * 6));
            scale = 1.0;
          } else if (isGhost) {
            r = 1; // Channeling purple spirit flame & casting AOE soul wave
            const prog = 1 - (this.attackDuration / this.attackMaxDuration);
            c = Math.min(7, Math.floor(prog * 8));
            scale = 1.1;
          } else if (isGolem) {
            r = 2; // Raising twin heavy stone hammers & ground smash
            const prog = 1 - (this.attackDuration / this.attackMaxDuration);
            c = Math.min(5, Math.floor(prog * 6));
            scale = 1.35;
          } else if (isSpider) {
            r = 3; // Rearing back fangs & venom spit
            const prog = 1 - (this.attackDuration / this.attackMaxDuration);
            c = Math.min(6, Math.floor(prog * 7));
            scale = 0.95;
          } else if (isCommander) {
            r = 4; // Golden halberd 360 sweeping cleave
            const prog = 1 - (this.attackDuration / this.attackMaxDuration);
            c = Math.min(5, Math.floor(prog * 6));
            scale = 1.4;
          }

          scale *= PACKED_VISUAL_SCALE_160;
          const drawW = cellW * scale;
          const drawH = cellH * scale;

          // Some legacy attack cells contain only the projectile/impact layer.
          // Preserve a stable same-row body underneath so an enemy never changes
          // design or disappears for one frame in the middle of its attack.
          let identityBaseC = -1;
          if (isGhost && (c === 4 || c === 5 || c === 7)) identityBaseC = 3;
          else if (isGolem && c === 4) identityBaseC = 3;
          else if (isSpider && c === 5) identityBaseC = 4;

          ctx.save();
          if (this.facing === -1) {
            ctx.scale(-1, 1);
          }
          if (identityBaseC >= 0) {
            ctx.drawImage(specialEnemyImg, identityBaseC * cellW, r * cellH, cellW, cellH, -drawW / 2, -drawH / 2 - 12, drawW, drawH);
          }
          ctx.drawImage(specialEnemyImg, c * cellW, r * cellH, cellW, cellH, -drawW / 2, -drawH / 2 - 12, drawW, drawH);
          ctx.restore();
        } else if (!useCanonicalEnemyAtlas && (isTianbing || isDemonApe) && realEnemyImg && realEnemyImg.complete && realEnemyImg.naturalWidth > 0 && (displayIsDying || this.isKnockedDown || this.isAttacking)) {
          const cellW = 160;
          const cellH = 160;
          let r = 0;
          let c = 0;

          if (isTianbing) {
            if (displayIsDying) {
              r = 2; // Golden soul dissolve
              const prog = 1 - (this.deathTimer / this.deathMaxDuration);
              c = Math.min(5, Math.floor(prog * 6));
            } else if (this.isKnockedDown) {
              r = 1; // Knockdown on floor and getting up
              const kdProg = 1 - (this.knockdownTimer / this.knockdownMaxDuration);
              c = Math.min(5, Math.floor(kdProg * 6));
            } else {
              r = 0; // Spear thrust and slash
              const prog = 1 - (this.attackDuration / this.attackMaxDuration);
              c = Math.min(5, Math.floor(prog * 6));
            }
          } else if (isDemonApe) {
            if (displayIsDying) {
              r = 5; // Purple demon flame dissolve
              const prog = 1 - (this.deathTimer / this.deathMaxDuration);
              c = Math.min(4, Math.floor(prog * 5));
            } else if (this.isKnockedDown) {
              r = 4; // Knockdown on stomach & crawl up
              const kdProg = 1 - (this.knockdownTimer / this.knockdownMaxDuration);
              c = Math.min(5, Math.floor(kdProg * 6));
            } else {
              r = 3; // Leaping double claw strike
              const prog = 1 - (this.attackDuration / this.attackMaxDuration);
              c = Math.min(5, Math.floor(prog * 6));
            }
          }

          const scale = 0.95 * PACKED_VISUAL_SCALE_160;
          const drawW = cellW * scale;
          const drawH = cellH * scale;

          ctx.save();
          if (this.facing === -1) {
            ctx.scale(-1, 1);
          }
          if (isTianbing && !displayIsDying && !this.isKnockedDown && c === 2) {
            ctx.drawImage(realEnemyImg, cellW, 0, cellW, cellH, -drawW / 2, -drawH / 2 - 12, drawW, drawH);
          }
          ctx.drawImage(realEnemyImg, c * cellW, r * cellH, cellW, cellH, -drawW / 2, -drawH / 2 - 12, drawW, drawH);
          ctx.restore();
        } else if ((isBaigu || isTongbei) && realBossImg && realBossImg.complete && realBossImg.naturalWidth > 0 && (displayIsDying || this.isAttacking)) {
          const cellW = 160;
          const cellH = 160;
          let r = 0;
          let c = 0;

          if (isBaigu) {
            if (displayIsDying) {
              r = 1; // Skeleton spirit dissolve
              const prog = 1 - (this.deathTimer / this.deathMaxDuration);
              c = Math.min(4, Math.floor(prog * 5));
            } else {
              r = 0; // Bone scythe slash
              const prog = 1 - (this.attackDuration / this.attackMaxDuration);
              c = Math.min(7, Math.floor(prog * 8));
            }
          } else if (isTongbei) {
            if (displayIsDying) {
              r = 3; // Kneel & spirit ghost dissolve
              const prog = 1 - (this.deathTimer / this.deathMaxDuration);
              c = Math.min(5, Math.floor(prog * 6));
            } else {
              r = 2; // Dark void staff smash & roar
              const prog = 1 - (this.attackDuration / this.attackMaxDuration);
              c = Math.min(5, Math.floor(prog * 6));
            }
          }

          const scale = (this.isFinalBoss ? (this.phase === 2 ? 1.6 : 1.35) : 1.25) * PACKED_VISUAL_SCALE_160;
          const drawW = cellW * scale;
          const drawH = cellH * scale;

          ctx.save();
          if (this.facing === -1) {
            ctx.scale(-1, 1);
          }
          ctx.drawImage(realBossImg, c * cellW, r * cellH, cellW, cellH, -drawW / 2, -drawH / 2 - 12, drawW, drawH);
          ctx.restore();
        } else {
          const isBossSheet = this.isBoss;
          const img = isBossSheet ? loadedImages['infinite_bosses_a'] : loadedImages['monsters_beasts'];

          if (img && img.complete && img.naturalWidth > 0) {
            const cellW = isBossSheet ? 160 : 128;
            const cellH = isBossSheet ? 160 : 128;

            let c = 0;
            if (isBossSheet) {
              // The legacy infinite-boss contact sheet mixed full bodies with
              // effect-only/cropped cells.  Its first cell is the stable identity
              // reference; motion now comes from a subtle procedural hover instead
              // of cycling through damaged source cells.
              c = 0;
            } else if (this.isAttacking) {
              const prog = 1 - (this.attackDuration / this.attackMaxDuration);
              if (this.row === 4) {
                c = 4 + Math.min(1, Math.floor(prog * 2));
              } else if (this.row === 5) {
                c = 2 + Math.min(1, Math.floor(prog * 2));
              } else {
                c = 6 + Math.min(1, Math.floor(prog * 2));
              }
            } else {
              let baseCol = 0;
              if (this.direction === 'up') baseCol = 2;
              else if (this.direction === 'down') baseCol = 0;
              else if (this.direction === 'right' || this.direction === 'left') baseCol = 4;

              c = isMoving ? (baseCol + Math.floor((Date.now() / 160) % 2)) : baseCol;
            }

            const r = this.row;
            const baseScale = this.isFinalBoss ? (this.phase === 2 ? 1.6 : 1.3) : (this.isBoss ? 1.25 : 0.95);
            const scale = baseScale * (this.isBoss ? PACKED_VISUAL_SCALE_160 : PACKED_VISUAL_SCALE_128);
            const drawW = cellW * scale;
            const drawH = cellH * scale;

            ctx.save();
            if (this.facing === -1) {
              ctx.scale(-1, 1);
            }
            const sourceFootY = isBossSheet ? (cellH - 38) : (cellH - 28);
            const hover = isBossSheet ? Math.sin(this.animClock * 4.2) * 3 : 0;
            ctx.drawImage(img, c * cellW, r * cellH, cellW, cellH, -drawW / 2, 40 - sourceFootY * scale + hover, drawW, drawH);
            ctx.restore();
          }
        }

        if (this.burnTimer > 0) {
          ctx.beginPath();
          ctx.arc(0, 0, this.radius + 6, 0, Math.PI * 2);
          ctx.strokeStyle = '#f97316';
          ctx.lineWidth = 3;
          ctx.stroke();
        }
        if (this.freezeTimer > 0) {
          ctx.beginPath();
          ctx.arc(0, 0, this.radius + 8, 0, Math.PI * 2);
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 3;
          ctx.stroke();
        }

        if (!this.isBoss && !this.isDying) {
          const hpPct = Math.max(0, this.hp / this.maxHp);
          const barW = this.radius * 2;
          ctx.fillStyle = '#110e18';
          ctx.fillRect(-barW / 2, -this.radius - 14, barW, 6);
          ctx.fillStyle = this.isAlly ? '#4ade80' : '#ef4444';
          ctx.fillRect(-barW / 2, -this.radius - 14, barW * hpPct, 6);
        }

        ctx.restore();
      }
    }

    let enemies = [];

    // PROJECTILES & VISUAL FX
    class BossSkillAnimatedFX {
      constructor(x, y, row, duration = 0.7, size = 180, color = '#facc15', ground = false, startFrame = 0, endFrame = 6) {
        this.x = x;
        this.y = y;
        this.row = row;
        this.duration = duration;
        this.maxDuration = duration;
        this.size = size;
        this.color = color;
        this.ground = ground;
        this.startFrame = Math.max(0, Math.min(6, startFrame));
        this.endFrame = Math.max(this.startFrame, Math.min(6, endFrame));
        this.alpha = 1;
      }

      update(dt) {
        this.duration -= dt;
        this.alpha = Math.max(0, Math.min(1, this.duration / Math.min(0.2, this.maxDuration)));
      }

      draw(ctx) {
        if (this.duration <= 0) return;
        const image = loadedImages['boss_skill_fx'];
        const progress = Math.max(0, Math.min(0.999, 1 - this.duration / this.maxDuration));
        const frameCount = this.endFrame - this.startFrame + 1;
        const frame = this.startFrame + Math.min(frameCount - 1, Math.floor(progress * frameCount));
        ctx.save();
        ctx.globalAlpha = Math.min(0.9, this.alpha);
        ctx.shadowColor = this.color;
        ctx.shadowBlur = this.row === 1 ? 18 : 12;
        if (image && image.complete && image.naturalWidth > 0) {
          const cell = 256;
          const drawSize = this.row === 1 ? this.size * 2.12 : this.size;
          ctx.drawImage(image, frame * cell, this.row * cell, cell, cell, this.x - drawSize / 2, this.y - drawSize / 2, drawSize, drawSize);
        } else {
          ctx.strokeStyle = this.color;
          ctx.lineWidth = 5;
          ctx.beginPath();
          ctx.arc(this.x, this.y, this.size * (0.25 + progress * 0.75), 0, Math.PI * 2);
          ctx.stroke();
        }
        ctx.restore();
      }
    }

    class BossSkillProjectile {
      constructor(x, y, vx, vy, damage, color) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.dmg = damage;
        this.color = color;
        this.radius = 15;
        this.alive = true;
        this.life = 3.4;
        this.animClock = Math.random() * 0.12;
        this.isEnemy = true;
      }

      update(dt) {
        this.x += this.vx * dt;
        this.y += this.vy * dt;
        this.animClock += dt;
        this.life -= dt;
        if (Math.hypot(player.x - this.x, player.y - this.y) <= player.radius + this.radius) {
          this.alive = false;
          player.takeDamage(this.dmg);
          fxList.push(new BossSkillAnimatedFX(this.x, this.y, 0, 0.30, 112, this.color, false, 4, 6));
          fxList.push(new RadialSparksFX(this.x, this.y, 7, this.color, 34));
        }
        if (this.life <= 0) this.alive = false;
      }

      draw(ctx) {
        const image = loadedImages['boss_skill_fx'];
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(Math.atan2(this.vy, this.vx));
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 14;
        if (image && image.complete && image.naturalWidth > 0) {
          const cell = 256;
          const frame = 2 + Math.floor(this.animClock * 18) % 2;
          ctx.drawImage(image, frame * cell, 0, cell, cell, -48, -48, 96, 96);
        } else {
          ctx.fillStyle = this.color;
          ctx.beginPath();
          ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
          ctx.fill();
        }
        ctx.restore();
      }
    }

    class Projectile {
      constructor(x, y, vx, vy, dmg, color, isEnemy = true) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.dmg = dmg;
        this.color = color;
        this.isEnemy = isEnemy;
        this.radius = 9;
        this.alive = true;
        this.life = 4.0;
      }

      update(dt) {
        this.x += this.vx * dt;
        this.y += this.vy * dt;
        this.life -= dt;
        if (this.life <= 0) this.alive = false;

        if (this.isEnemy) {
          if (Math.hypot(player.x - this.x, player.y - this.y) <= player.radius + this.radius) {
            this.alive = false;
            player.takeDamage(this.dmg);
          }
        } else {
          enemies.forEach(e => {
            if (e.alive && !e.isAlly && Math.hypot(e.x - this.x, e.y - this.y) <= e.radius + this.radius) {
              this.alive = false;
              e.takeDamage(this.dmg);
            }
          });
        }
      }

      draw(ctx) {
        ctx.save();
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 12;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.restore();
      }
    }

    const RUYI_THROW_SPIN_REVS_PER_SECOND = 6;

    class RuyiBoomerangProjectile {
      constructor(owner, angle, maxRange, damage, color, weaponProfile = RUYI_WEAPON_PROFILES.normal, formProfile = null) {
        this.owner = owner;
        this.angle = angle;
        this.maxRange = maxRange;
        this.damage = damage;
        this.color = color || '#facc15';
        this.weaponProfile = weaponProfile || RUYI_WEAPON_PROFILES.normal;
        this.isTitan = this.weaponProfile.id === 'titan';
        this.formProfile = formProfile;
        this.startX = owner.x + Math.cos(angle) * 34;
        this.startY = owner.y + Math.sin(angle) * 34;
        this.turnX = this.startX + Math.cos(angle) * maxRange;
        this.turnY = this.startY + Math.sin(angle) * maxRange;
        this.x = this.startX;
        this.y = this.startY;
        this.prevX = this.x;
        this.prevY = this.y;
        this.vx = 0;
        this.vy = 0;
        this.radius = 35 * this.weaponProfile.radius;
        this.outboundDuration = 0.44 * this.weaponProfile.travelTime;
        this.turnHoldDuration = this.weaponProfile.turnHold || 0;
        this.returnDuration = 0.46 * this.weaponProfile.travelTime;
        this.elapsed = 0;
        this.alive = true;
        this.isEnemy = false;
        this.returning = false;
        this.turnProcUsed = false;
        this.catchProcUsed = false;
        this.outboundHits = new Set();
        this.returnHits = new Set();
        this.hitCount = 0;
        this.formProcUsed = false;
        this.alignmentProcUsed = false;
        this.guanyinRestoredQi = false;
        this.reflectedCount = 0;
        this.buddhaSeals = new Set();
        this.buddhaDetonated = new Set();
        this.frame = 0;
        this.spinRotation = 0;
        this.spinRevolutionsPerSecond = this.isTitan ? 5.25 : RUYI_THROW_SPIN_REVS_PER_SECOND;
      }

      distanceToTravelSegment(x, y) {
        const dx = this.x - this.prevX;
        const dy = this.y - this.prevY;
        const lengthSq = dx * dx + dy * dy;
        if (lengthSq <= 0.0001) return Math.hypot(x - this.x, y - this.y);
        const t = Math.max(0, Math.min(1, ((x - this.prevX) * dx + (y - this.prevY) * dy) / lengthSq));
        return Math.hypot(x - (this.prevX + dx * t), y - (this.prevY + dy * t));
      }

      update(dt) {
        if (!this.owner || !this.alive) return;
        this.prevX = this.x;
        this.prevY = this.y;
        this.elapsed += dt;
        this.spinRotation = (this.spinRotation + dt * Math.PI * 2 * this.spinRevolutionsPerSecond) % (Math.PI * 2);
        const totalDuration = this.outboundDuration + this.turnHoldDuration + this.returnDuration;
        const sideX = Math.cos(this.angle + Math.PI / 2);
        const sideY = Math.sin(this.angle + Math.PI / 2);

        if (this.elapsed < this.outboundDuration) {
          const t = Math.max(0, Math.min(1, this.elapsed / this.outboundDuration));
          const eased = 1 - Math.pow(1 - t, 2);
          const bow = Math.sin(t * Math.PI) * Math.min(72, this.maxRange * 0.10);
          this.x = this.startX + Math.cos(this.angle) * this.maxRange * eased + sideX * bow;
          this.y = this.startY + Math.sin(this.angle) * this.maxRange * eased + sideY * bow;
        } else if (this.elapsed < this.outboundDuration + this.turnHoldDuration) {
          this.returning = true;
          const t = Math.max(0, Math.min(1, (this.elapsed - this.outboundDuration) / Math.max(0.001, this.turnHoldDuration)));
          const orbitAngle = this.angle + t * Math.PI * 2;
          const orbitRadius = this.weaponProfile.orbitRadius || 0;
          this.x = this.turnX + Math.cos(orbitAngle) * orbitRadius;
          this.y = this.turnY + Math.sin(orbitAngle) * orbitRadius;
        } else {
          this.returning = true;
          const t = Math.max(0, Math.min(1, (this.elapsed - this.outboundDuration - this.turnHoldDuration) / this.returnDuration));
          const eased = t * t * (3 - 2 * t);
          const bow = -Math.sin(t * Math.PI) * Math.min(58, this.maxRange * 0.08);
          const catchX = this.owner.x + Math.cos(this.angle) * 24;
          const catchY = this.owner.y + Math.sin(this.angle) * 24;
          this.x = this.turnX + (catchX - this.turnX) * eased + sideX * bow;
          this.y = this.turnY + (catchY - this.turnY) * eased + sideY * bow;
        }
        if (!this.turnProcUsed && this.elapsed >= this.outboundDuration) {
          this.turnProcUsed = true;
          this.owner.onRuyiTurn(this);
        }
        this.vx = (this.x - this.prevX) / Math.max(0.001, dt);
        this.vy = (this.y - this.prevY) / Math.max(0.001, dt);
        this.frame = Math.floor(this.elapsed * 28) % 7;

        const hitSet = this.returning ? this.returnHits : this.outboundHits;
        const travelAngle = Math.atan2(this.y - this.prevY, this.x - this.prevX);
        let playedHitSound = false;
        enemies.forEach(enemy => {
          if (!enemy.alive || enemy.isAlly || hitSet.has(enemy)) return;
          if (this.distanceToTravelSegment(enemy.x, enemy.y) > enemy.radius + this.radius) return;
          hitSet.add(enemy);
          this.hitCount++;
          const pierceBonus = !this.returning && this.weaponProfile.pierceRamp
            ? Math.min(0.60, Math.max(0, this.outboundHits.size - 1) * this.weaponProfile.pierceRamp)
            : 0;
          let passDamage = this.damage * (this.returning ? 0.72 : 1.0) * (1 + pierceBonus);
          if (enemy.isBoss) passDamage *= 1 + (this.owner.alignmentBossDamage || 0);
          if (enemy.hp < enemy.maxHp * .5) passDamage *= 1 + (this.owner.alignmentExecuteDamage || 0);
          enemy.takeDamage(passDamage, false, this.isTitan || this.returning);
          if ((this.owner.alignmentLifeLeech || 0) > 0) this.owner.healFromDamage(passDamage, this.owner.alignmentLifeLeech);
          enemy.knockbackX += Math.cos(travelAngle) * (this.returning ? 125 : 165);
          enemy.knockbackY += Math.sin(travelAngle) * (this.returning ? 125 : 165);
          fxList.push(new RuyiImpactBurstFX(enemy.x, enemy.y, this.isTitan ? 0.48 : 0.34));
          fxList.push(new HadesHitSparkFX(enemy.x, enemy.y, travelAngle, this.color));
          this.owner.applySpecialBoonOnHit(enemy, this.returning, travelAngle, this);
          if (this.formProfile) this.owner.procFormSpecialOnHit(enemy, this.returning, travelAngle, this);
          if (!this.alignmentProcUsed) {
            this.owner.procAlignmentOnHit(enemy, 1, passDamage);
            this.alignmentProcUsed = true;
          }
          if (!playedHitSound) {
            sound.playStaffHit(this.isTitan);
            playedHitSound = true;
          }
        });

        // The staff protects its own flight lane rather than reflecting the whole
        // arena: enemy shots touched by the spinning weapon are sent back.
        projectiles.forEach(projectile => {
          if (projectile === this || !projectile.alive || !projectile.isEnemy) return;
          if (this.distanceToTravelSegment(projectile.x, projectile.y) <= this.radius + projectile.radius) {
            projectile.isEnemy = false;
            projectile.vx = -projectile.vx * 1.35;
            projectile.vy = -projectile.vy * 1.35;
            projectile.dmg *= 1.2;
            this.reflectedCount++;
            this.owner.onRuyiReflect(this, projectile);
            fxList.push(new RadialSparksFX(projectile.x, projectile.y, 5, this.color, 24));
          }
        });

        if (this.elapsed >= totalDuration) {
          if (!this.catchProcUsed) {
            this.catchProcUsed = true;
            this.owner.onRuyiCatch(this);
          }
          this.alive = false;
          sound.playJadeChime();
          fxList.push(new RadialSparksFX(this.owner.x, this.owner.y, 5, '#fde68a', 24));
        }
      }

      draw(ctx) {
        if (!this.alive) return;
        const img = loadedImages['ruyi_boomerang_spin'];
        ctx.save();
        ctx.globalAlpha = 0.42;
        ctx.strokeStyle = this.color;
        ctx.lineWidth = this.isTitan ? 7 : 5;
        ctx.lineCap = 'round';
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 12;
        ctx.beginPath();
        ctx.moveTo(this.prevX, this.prevY);
        ctx.lineTo(this.x, this.y);
        ctx.stroke();
        ctx.restore();

        if (img && img.complete && img.naturalWidth > 0) {
          const cell = 220;
          const scale = this.isTitan ? 1.02 : 0.88;
          ctx.save();
          ctx.translate(this.x, this.y);
          // Keep the staff rotating continuously through the turn instead of
          // snapping it by 180 degrees when the boomerang begins its return.
          ctx.rotate(this.angle + this.spinRotation);
          ctx.shadowColor = this.color;
          ctx.shadowBlur = 10;
          ctx.drawImage(img, this.frame * cell, 0, cell, cell, -cell * scale / 2, -cell * scale / 2, cell * scale, cell * scale);
          // Do not tint with source-atop on the world canvas. The arena has
          // already been painted, so source-atop also colors the floor inside
          // this rotated cell and creates a conspicuous square matte. The
          // alignment color remains readable through the sprite-only shadow.
          ctx.restore();
        } else {
          ctx.save();
          ctx.translate(this.x, this.y);
          ctx.rotate(this.angle + this.elapsed * 18);
          ctx.strokeStyle = this.color;
          ctx.lineWidth = 8;
          ctx.lineCap = 'round';
          ctx.beginPath();
          ctx.moveTo(-56, 0);
          ctx.lineTo(56, 0);
          ctx.stroke();
          ctx.restore();
        }
      }
    }

    let projectiles = [];
    let fxList = [];
    let floatingTexts = [];
    const renderActors = [];

    class FloatingText {
      constructor(x, y, text, color = '#ffffff', size = 15) {
        this.x = x;
        this.y = y;
        this.text = text;
        this.color = color;
        this.size = size;
        this.alpha = 1.0;
        this.vy = -35;
      }

      update(dt) {
        this.y += this.vy * dt;
        this.alpha -= dt * 1.5;
      }

      draw(ctx) {
        ctx.save();
        ctx.font = getCanvasFont(this.size, 700);
        ctx.fillStyle = this.color;
        ctx.globalAlpha = Math.max(0, this.alpha);
        ctx.textAlign = 'center';
        ctx.fillText(this.text, this.x, this.y);
        ctx.restore();
      }
    }

    class FormSkillRuneFX {
      constructor(x, y, glyph, color, scale = 1) {
        this.x = x;
        this.y = y;
        this.glyph = glyph;
        this.color = color;
        this.scale = scale;
        this.life = 0.72;
        this.maxLife = 0.72;
        this.alpha = 1;
        this.angle = 0;
      }
      update(dt) {
        this.life -= dt;
        this.alpha = Math.max(0, this.life / this.maxLife);
        this.angle += dt * 3.2;
        this.y -= dt * 18;
      }
      draw(ctx) {
        const progress = 1 - this.alpha;
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.globalAlpha = Math.sin(Math.min(1, progress) * Math.PI) * 0.82;
        ctx.rotate(this.angle);
        ctx.strokeStyle = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 10;
        ctx.lineWidth = 2.5;
        const radius = (24 + progress * 18) * this.scale;
        ctx.beginPath(); ctx.arc(0, 0, radius, 0, Math.PI * 2); ctx.stroke();
        for (let i = 0; i < 4; i++) {
          const a = i * Math.PI / 2;
          ctx.beginPath(); ctx.moveTo(Math.cos(a) * (radius - 7), Math.sin(a) * (radius - 7)); ctx.lineTo(Math.cos(a) * (radius + 7), Math.sin(a) * (radius + 7)); ctx.stroke();
        }
        ctx.rotate(-this.angle);
        ctx.font = `${Math.round(19 * this.scale)}px "Segoe UI Emoji", sans-serif`;
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#ffffff';
        ctx.fillText(this.glyph, 0, 0);
        ctx.restore();
      }
    }

    class TransformationSpellFX {
      constructor(form, x, y, radius, duration = 1.1) {
        this.form = form;
        this.x = x;
        this.y = y;
        this.radius = Math.min(220, radius);
        this.life = duration;
        this.maxLife = duration;
        this.alpha = 1;
        this.angle = 0;
      }
      update(dt) {
        this.life -= dt;
        this.alpha = Math.max(0, this.life / this.maxLife);
        this.angle += dt * (this.form === 'roc' ? 6 : 2.6);
      }
      draw(ctx) {
        const p = 1 - this.alpha;
        const colors = { dragon:'#38bdf8', tiger:'#f59e0b', roc:'#fde047', ape:'#ea580c', tortoise:'#34d399' };
        const color = colors[this.form] || '#facc15';
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.globalAlpha = Math.sin(Math.min(1, p) * Math.PI) * 0.72;
        ctx.strokeStyle = color; ctx.fillStyle = color; ctx.shadowColor = color; ctx.shadowBlur = 12; ctx.lineWidth = 3;
        const r = this.radius * (0.30 + p * 0.70);
        if (this.form === 'dragon') {
          for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.arc(0, 0, r * (0.45 + i * .25), this.angle + i, this.angle + i + Math.PI * 1.35); ctx.stroke(); }
          for (let i = 0; i < 7; i++) { const a=i*Math.PI*2/7+this.angle; ctx.beginPath(); ctx.moveTo(Math.cos(a)*r*.18,Math.sin(a)*r*.18); ctx.lineTo(Math.cos(a+.12)*r*.72,Math.sin(a+.12)*r*.72); ctx.lineTo(Math.cos(a-.08)*r,Math.sin(a-.08)*r); ctx.stroke(); }
        } else if (this.form === 'tiger') {
          for (let i = 0; i < 3; i++) { const a=-.7+i*.7; ctx.beginPath(); ctx.moveTo(-r*.65,Math.sin(a)*20); ctx.quadraticCurveTo(0,-r*(.55-i*.12),r*.72,Math.cos(a)*30); ctx.stroke(); }
          ctx.beginPath(); ctx.arc(0,0,r*.75,0,Math.PI*2); ctx.stroke();
        } else if (this.form === 'roc') {
          for (let i = 0; i < 12; i++) { const a=this.angle+i*Math.PI*2/12; const rr=r*(.35+(i%3)*.2); ctx.save(); ctx.translate(Math.cos(a)*rr,Math.sin(a)*rr); ctx.rotate(a); ctx.beginPath(); ctx.ellipse(0,0,18,5,0,0,Math.PI*2); ctx.stroke(); ctx.restore(); }
        } else if (this.form === 'ape') {
          for (let i = 0; i < 10; i++) { const a=i*Math.PI*2/10; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(Math.cos(a)*r*.45,Math.sin(a)*r*.45); ctx.lineTo(Math.cos(a+.16)*r,Math.sin(a+.16)*r); ctx.stroke(); }
          ctx.lineWidth=6; ctx.beginPath(); ctx.arc(0,0,r*.72,0,Math.PI*2); ctx.stroke();
        } else {
          for (let ring = 0; ring < 3; ring++) { ctx.beginPath(); ctx.arc(0,0,r*(.42+ring*.24),this.angle*(ring%2?-1:1),this.angle*(ring%2?-1:1)+Math.PI*1.55); ctx.stroke(); }
          for (let i=0;i<6;i++){const a=i*Math.PI/3;ctx.beginPath();ctx.moveTo(Math.cos(a)*r*.32,Math.sin(a)*r*.32);ctx.lineTo(Math.cos(a)*r*.82,Math.sin(a)*r*.82);ctx.stroke();}
        }
        ctx.restore();
      }
    }

    class FormPulseDamageFX {
      constructor(x, y, radius, pulses, damage, color, interval = 0.2) {
        this.x=x; this.y=y; this.radius=Math.min(220,radius); this.pulsesRemaining=pulses; this.damage=damage; this.color=color; this.interval=interval;
        this.timer=0; this.life=interval*(pulses+1); this.maxLife=this.life; this.alpha=1; this.pulseIndex=0;
      }
      update(dt) {
        this.life -= dt; this.alpha=Math.max(0,this.life/this.maxLife); this.timer-=dt;
        if (this.timer <= 0 && this.pulsesRemaining > 0) {
          this.timer=this.interval; this.pulsesRemaining--; this.pulseIndex++;
          enemies.filter(enemy=>enemy.alive&&!enemy.isAlly&&Math.hypot(enemy.x-this.x,enemy.y-this.y)<=this.radius+enemy.radius)
            .forEach(enemy=>enemy.takeDamage(this.damage,false,true));
          fxList.push(new Shockwave(this.x,this.y,this.radius,this.color));
        }
      }
      draw(ctx) {
        ctx.save(); ctx.globalAlpha=this.alpha*.35; ctx.strokeStyle=this.color; ctx.lineWidth=4; ctx.shadowColor=this.color; ctx.shadowBlur=10;
        ctx.beginPath(); ctx.arc(this.x,this.y,this.radius*(.35+(1-this.alpha)*.65),0,Math.PI*2); ctx.stroke(); ctx.restore();
      }
    }

    class FormFeatherProjectile {
      constructor(x, y, angle, damage, color) {
        this.x=x; this.y=y; this.prevX=x; this.prevY=y; this.angle=angle; this.damage=damage; this.color=color; this.speed=620;
        this.radius=10; this.life=1.05; this.alive=true; this.isEnemy=false; this.hitTargets=new Set();
      }
      update(dt) {
        this.prevX=this.x; this.prevY=this.y; this.x+=Math.cos(this.angle)*this.speed*dt; this.y+=Math.sin(this.angle)*this.speed*dt; this.life-=dt;
        enemies.forEach(enemy=>{if(!enemy.alive||enemy.isAlly||this.hitTargets.has(enemy))return;if(Math.hypot(enemy.x-this.x,enemy.y-this.y)<=enemy.radius+this.radius){this.hitTargets.add(enemy);enemy.takeDamage(this.damage,false,false);fxList.push(new RadialSparksFX(this.x,this.y,4,this.color,22));if(this.hitTargets.size>=3)this.alive=false;}});
        if(this.life<=0)this.alive=false;
      }
      draw(ctx) {
        ctx.save();ctx.translate(this.x,this.y);ctx.rotate(this.angle);ctx.shadowColor=this.color;ctx.shadowBlur=9;ctx.strokeStyle=this.color;ctx.fillStyle='rgba(254,240,138,.55)';ctx.lineWidth=2;
        ctx.beginPath();ctx.moveTo(17,0);ctx.quadraticCurveTo(-2,-8,-17,0);ctx.quadraticCurveTo(-2,8,17,0);ctx.fill();ctx.stroke();ctx.beginPath();ctx.moveTo(-14,0);ctx.lineTo(14,0);ctx.stroke();ctx.restore();
      }
    }

    class AnimatedBuddhaPalmSlam {
      constructor(x, y, radius) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.alpha = 1.0;
        this.life = 0.45;
      }

      update(dt) {
        this.life -= dt;
        this.alpha = this.life / 0.45;
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);

        const img = loadedImages['buddha_colossal'];
        if (img && img.complete && img.naturalWidth > 0) {
          const cellW = 256;
          const cellH = 256;
          const c = Math.min(5, Math.floor((1 - this.alpha) * 6));
          ctx.drawImage(img, c * cellW, 1 * cellH, cellW, cellH, -this.radius, -this.radius, this.radius * 2, this.radius * 2);
        }

        ctx.restore();
      }
    }

    class ElementalSlashFX {
      constructor(x, y, angle, type = 'golden', reach = 160) {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.type = type;
        this.reach = reach;
        this.life = 0.28;
        this.maxLife = 0.28;

        if (type === 'fire') {
          this.row = 0;
          this.totalCols = 8;
        } else if (type === 'thunder' || type === 'lightning' || type === 'golden') {
          this.row = 1;
          this.totalCols = 7;
        } else if (type === 'water') {
          this.row = 2;
          this.totalCols = 8;
        } else if (type === 'ice' || type === 'frost') {
          this.row = 3;
          this.totalCols = 8;
        } else if (type === 'anvil' || type === 'forge') {
          this.row = 4;
          this.totalCols = 8;
        } else {
          this.row = 0;
          this.totalCols = 8;
        }
      }

      update(dt) {
        this.life -= dt;
      }

      draw(ctx) {
        if (this.life <= 0) return;
        const img = loadedImages['elemental_slashes'];
        if (!img || !img.complete || img.naturalWidth <= 0) return;

        const cellW = 160;
        const cellH = 160;
        const prog = 1 - (this.life / this.maxLife);
        const col = Math.min(this.totalCols - 1, Math.floor(prog * this.totalCols));

        const scale = (this.reach / 160) * 0.72;
        const drawW = cellW * scale;
        const drawH = cellH * scale;

        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);
        ctx.globalAlpha = Math.max(0, Math.min(0.78, this.life / this.maxLife));

        ctx.drawImage(img, col * cellW, this.row * cellH, cellW, cellH, 0, -drawH / 2, drawW, drawH);
        ctx.restore();
      }
    }

    class EnemySpearThrustFX {
      constructor(x, y, angle, length = 85, color = '#facc15') {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.length = length;
        this.color = color;
        this.alpha = 1.0;
        this.life = 0.28;
      }

      update(dt) {
        this.life -= dt;
        this.alpha = Math.max(0, this.life / 0.28);
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);
        ctx.globalAlpha = this.alpha;

        const prog = 1 - this.alpha;
        const currentLen = this.length * (0.4 + prog * 0.6);

        // Golden spear shaft
        ctx.strokeStyle = '#b45309';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(10, 0);
        ctx.lineTo(currentLen, 0);
        ctx.stroke();

        // Glowing Spearhead Blade
        ctx.fillStyle = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 16;
        ctx.beginPath();
        ctx.moveTo(currentLen + 22, 0);
        ctx.lineTo(currentLen - 6, -10);
        ctx.lineTo(currentLen, 0);
        ctx.lineTo(currentLen - 6, 10);
        ctx.closePath();
        ctx.fill();

        // Slash Trail Arc
        ctx.strokeStyle = '#ef4444';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(currentLen, 0, 18, -Math.PI * 0.4, Math.PI * 0.4);
        ctx.stroke();

        ctx.restore();
      }
    }

    class EnemyClawSwipeFX {
      constructor(x, y, angle, radius = 65, color = '#ef4444') {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.radius = radius;
        this.color = color;
        this.alpha = 1.0;
        this.life = 0.24;
      }

      update(dt) {
        this.life -= dt;
        this.alpha = Math.max(0, this.life / 0.24);
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);
        ctx.globalAlpha = this.alpha;

        ctx.strokeStyle = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 18;

        for (let offset of [-14, 0, 14]) {
          ctx.beginPath();
          ctx.lineWidth = 4;
          ctx.arc(0, offset, this.radius, -Math.PI * 0.35, Math.PI * 0.35);
          ctx.stroke();
        }

        ctx.restore();
      }
    }

    class EnemySoulStrikeFX {
      constructor(x, y, angle, radius = 70, color = '#c084fc') {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.radius = radius;
        this.color = color;
        this.alpha = 1.0;
        this.life = 0.3;
      }

      update(dt) {
        this.life -= dt;
        this.alpha = Math.max(0, this.life / 0.3);
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);
        ctx.globalAlpha = this.alpha;

        ctx.strokeStyle = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 20;
        ctx.lineWidth = 8;

        ctx.beginPath();
        ctx.arc(0, 0, this.radius, -Math.PI * 0.4, Math.PI * 0.4);
        ctx.stroke();

        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 3;
        ctx.stroke();

        ctx.restore();
      }
    }

    class NetherGhostSoulAOEFX {
      constructor(x, y, maxRadius = 160) {
        this.x = x;
        this.y = y;
        this.maxRadius = maxRadius;
        this.radius = 20;
        this.alpha = 1.0;
        this.life = 0.45;
      }

      update(dt) {
        this.life -= dt;
        this.alpha = Math.max(0, this.life / 0.45);
        this.radius += (this.maxRadius - this.radius) * 10 * dt;
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.globalAlpha = this.alpha;

        ctx.beginPath();
        ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(192, 132, 252, 0.25)';
        ctx.fill();

        ctx.strokeStyle = '#c084fc';
        ctx.lineWidth = 4;
        ctx.shadowColor = '#c084fc';
        ctx.shadowBlur = 18;
        ctx.stroke();

        ctx.restore();
      }
    }

    class PortalSummonFX {
      constructor(x, y, color = '#facc15') {
        this.x = x;
        this.y = y;
        this.color = color;
        this.life = 0.45;
        this.alpha = 1.0;
      }

      update(dt) {
        this.life -= dt;
        this.alpha = Math.max(0, this.life / 0.45);
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.globalAlpha = this.alpha;

        const pulse = Math.sin(this.life * 20) * 6;
        ctx.beginPath();
        ctx.ellipse(0, 0, 34 + pulse, 20 + pulse * 0.5, 0, 0, Math.PI * 2);
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 3;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 16;
        ctx.stroke();

        ctx.restore();
      }
    }

    class KnockdownDustFX {
      constructor(x, y) {
        this.x = x;
        this.y = y;
        this.particles = [];
        for (let i = 0; i < 10; i++) {
          const ang = Math.random() * Math.PI * 2;
          const spd = 30 + Math.random() * 60;
          this.particles.push({
            x: 0,
            y: 0,
            vx: Math.cos(ang) * spd,
            vy: Math.sin(ang) * spd * 0.4,
            radius: 4 + Math.random() * 5,
            alpha: 0.85
          });
        }
        this.life = 0.45;
      }

      update(dt) {
        this.life -= dt;
        this.particles.forEach(p => {
          p.x += p.vx * dt;
          p.y += p.vy * dt;
          p.alpha = Math.max(0, this.life / 0.45);
        });
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        this.particles.forEach(p => {
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(217, 180, 130, ${p.alpha * 0.6})`;
          ctx.fill();
        });
        ctx.restore();
      }
    }

    class DeathSoulFX {
      constructor(x, y, typeKey, radius = 30) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.life = 0.65;
        this.sparks = [];
        const isHeaven = (typeKey === 'tianbing' || typeKey === 'tian_archer');
        this.color = isHeaven ? '#facc15' : '#c084fc';
        for (let i = 0; i < 18; i++) {
          const ang = Math.random() * Math.PI * 2;
          const spd = 40 + Math.random() * 90;
          this.sparks.push({
            x: 0,
            y: 0,
            vx: Math.cos(ang) * spd,
            vy: Math.sin(ang) * spd - 35,
            size: 3 + Math.random() * 4,
            alpha: 1.0
          });
        }
      }

      update(dt) {
        this.life -= dt;
        this.sparks.forEach(s => {
          s.x += s.vx * dt;
          s.y += s.vy * dt;
          s.alpha = Math.max(0, this.life / 0.65);
        });
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);

        const prog = 1 - (this.life / 0.65);
        ctx.beginPath();
        ctx.arc(0, -prog * 30, this.radius * (1 + prog * 0.8), 0, Math.PI * 2);
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 2;
        ctx.globalAlpha = Math.max(0, 1 - prog);
        ctx.stroke();

        this.sparks.forEach(s => {
          ctx.beginPath();
          ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
          ctx.fillStyle = this.color;
          ctx.globalAlpha = s.alpha;
          ctx.fill();
        });

        ctx.restore();
      }
    }

    class GroundFissureFX {
      constructor(x, y, angle, length, color = '#facc15') {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.length = length;
        this.color = color;
        this.alpha = 1.0;
        this.life = 1.5;
        this.debris = [];
        for (let i = 0; i < 12; i++) {
          this.debris.push({
            dx: (Math.random() * 2 - 1) * 35,
            dy: (Math.random() * 2 - 1) * 20,
            size: Math.random() * 6 + 3,
            rot: Math.random() * Math.PI
          });
        }
      }

      update(dt) {
        this.life -= dt;
        this.alpha = Math.max(0, this.life / 1.5);
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);
        ctx.globalAlpha = this.alpha;

        // Ground fracture lines
        ctx.beginPath();
        ctx.moveTo(-this.length * 0.4, 0);
        ctx.lineTo(-this.length * 0.2, -12);
        ctx.lineTo(0, 14);
        ctx.lineTo(this.length * 0.2, -16);
        ctx.lineTo(this.length * 0.45, 0);

        ctx.strokeStyle = this.color;
        ctx.lineWidth = 6;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 18;
        ctx.stroke();

        // Inner glowing core fissure
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Debris fragments
        ctx.fillStyle = '#2a1a38';
        this.debris.forEach(d => {
          ctx.save();
          ctx.translate(d.dx, d.dy);
          ctx.rotate(d.rot);
          ctx.fillRect(-d.size/2, -d.size/2, d.size, d.size);
          ctx.strokeStyle = this.color;
          ctx.lineWidth = 1;
          ctx.strokeRect(-d.size/2, -d.size/2, d.size, d.size);
          ctx.restore();
        });

        ctx.restore();
      }
    }

    class RadialSparksFX {
      constructor(x, y, count = 12, color = '#facc15', maxDist = 60) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.alpha = 1.0;
        this.life = 0.35;
        this.particles = [];
        for (let i = 0; i < count; i++) {
          const ang = Math.random() * Math.PI * 2;
          const spd = (Math.random() * 0.7 + 0.3) * maxDist;
          this.particles.push({
            vx: Math.cos(ang) * spd,
            vy: Math.sin(ang) * spd,
            x: 0,
            y: 0,
            len: Math.random() * 12 + 6,
            thickness: Math.random() * 2.5 + 1.5
          });
        }
      }

      update(dt) {
        this.life -= dt;
        this.alpha = Math.max(0, this.life / 0.35);
        this.particles.forEach(p => {
          p.x += p.vx * dt * 4;
          p.y += p.vy * dt * 4;
          p.vx *= 0.92;
          p.vy *= 0.92;
        });
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.globalAlpha = this.alpha;
        ctx.strokeStyle = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 12;

        this.particles.forEach(p => {
          ctx.lineWidth = p.thickness;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          const mag = Math.hypot(p.vx, p.vy) || 1;
          ctx.lineTo(p.x + (p.vx / mag) * p.len, p.y + (p.vy / mag) * p.len);
          ctx.stroke();
        });

        ctx.restore();
      }
    }

    class SlashSparksFX {
      constructor(x, y, angle, color = '#facc15') {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.color = color;
        this.alpha = 1.0;
        this.life = 0.22;
        this.lines = [];
        for (let i = 0; i < 6; i++) {
          this.lines.push({
            ang: angle + (Math.random() * 1.0 - 0.5),
            len: Math.random() * 28 + 14,
            spd: Math.random() * 220 + 100
          });
        }
      }

      update(dt) {
        this.life -= dt;
        this.alpha = Math.max(0, this.life / 0.22);
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.globalAlpha = this.alpha;
        ctx.strokeStyle = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 14;

        this.lines.forEach(l => {
          ctx.beginPath();
          ctx.lineWidth = 2.5;
          const prog = 1 - this.alpha;
          const sx = Math.cos(l.ang) * (l.spd * prog);
          const sy = Math.sin(l.ang) * (l.spd * prog);
          ctx.moveTo(sx, sy);
          ctx.lineTo(sx + Math.cos(l.ang) * l.len, sy + Math.sin(l.ang) * l.len);
          ctx.stroke();
        });

        ctx.restore();
      }
    }

    class RuyiStaffSpecialSlamFX {
      constructor(x, y, radius = 260, color = '#facc15', style = 'pillar_drop') {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.color = color;
        this.style = style;
        this.duration = 0.58;
        this.maxDuration = 0.58;
        this.alpha = 1.0;
      }

      update(dt) {
        this.duration -= dt;
        this.alpha = Math.max(0, this.duration / this.maxDuration);
      }

      draw(ctx) {
        if (this.duration <= 0) return;
        const img = loadedImages['ruyi_special_slam'];
        if (img && img.complete && img.naturalWidth > 0) {
          const cellW = 200;
          const cellH = 200;
          const progress = 1 - (this.duration / this.maxDuration);
          const c = Math.min(6, Math.floor(progress * 7));

          let r = 0; // Row 0: Real AI Generated Colossal Ruyi Jingu Bang Slam
          if (this.style === 'dragon_sweep') r = 1;
          else if (this.style === 'ding_hai') r = 2;
          else if (this.style === 'crater_nova') r = 3;

          const visualRadius = Math.min(150, this.radius * 0.62);
          const scale = (visualRadius / 100) * 1.05;
          const drawW = cellW * scale;
          const drawH = cellH * scale;

          ctx.save();
          ctx.translate(this.x, this.y);
          ctx.globalAlpha = Math.max(0, this.alpha);

          // Golden sacred aura
          ctx.shadowColor = this.color;
          ctx.shadowBlur = 32;

          // Draw real AI animated frame of Ruyi Jingu Bang
          ctx.drawImage(img, c * cellW, r * cellH, cellW, cellH, -drawW / 2, -drawH + 45, drawW, drawH);

          // Divine glowing ground impact rings
          if (progress > 0.35) {
            ctx.beginPath();
            ctx.arc(0, 0, visualRadius * (0.35 + (progress - 0.35) * 0.9), 0, Math.PI * 2);
            ctx.strokeStyle = '#facc15';
            ctx.lineWidth = 4 * this.alpha;
            ctx.shadowColor = '#fff';
            ctx.shadowBlur = 20;
            ctx.stroke();
          }

          ctx.restore();
        }
      }
    }

    class StaffPillarSlamFX extends RuyiStaffSpecialSlamFX {}

    class AnimatedAttackSweep {
      constructor(x, y, angle, radius, color = '#facc15', isFullCircle = false) {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.radius = radius;
        this.color = color;
        this.isFullCircle = isFullCircle;
        this.alpha = 1.0;
        this.life = 0.24;
      }

      update(dt) {
        this.life -= dt;
        this.alpha = Math.max(0, this.life / 0.24);
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);
        ctx.globalAlpha = Math.max(0, this.alpha);

        const arcSpan = this.isFullCircle ? Math.PI * 2 : Math.PI * 0.85;
        const startAng = this.isFullCircle ? 0 : -arcSpan / 2;
        const endAng = this.isFullCircle ? Math.PI * 2 : arcSpan / 2;

        // Outer Blade Edge
        ctx.beginPath();
        ctx.arc(0, 0, this.radius, startAng, endAng);
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 18;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 24;
        ctx.stroke();

        // Inner Sharp Razor Arc
        ctx.beginPath();
        ctx.arc(0, 0, this.radius - 4, startAng, endAng);
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 4;
        ctx.stroke();

        // Flowing energy crescent fill
        if (!this.isFullCircle) {
          ctx.beginPath();
          ctx.arc(0, 0, this.radius, startAng, endAng);
          ctx.arc(0, 0, this.radius * 0.45, endAng, startAng, true);
          ctx.closePath();
          ctx.fillStyle = this.color;
          ctx.globalAlpha = Math.max(0, this.alpha * 0.25);
          ctx.fill();
        }

        ctx.restore();
      }
    }

    class ExtendedStaffBeam {
      constructor(x, y, angle, length, color = '#facc15') {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.length = length;
        this.color = color;
        this.alpha = 1.0;
        this.life = 0.28;
      }

      update(dt) {
        this.life -= dt;
        this.alpha = Math.max(0, this.life / 0.28);
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);

        ctx.fillStyle = this.color;
        ctx.globalAlpha = Math.max(0, this.alpha);
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 24;

        ctx.fillRect(0, -14, this.length, 28);
        ctx.fillStyle = '#ef4444';
        ctx.fillRect(0, -7, this.length, 14);

        ctx.restore();
      }
    }

    class Shockwave {
      constructor(x, y, maxRadius, color = '#facc15') {
        this.x = x;
        this.y = y;
        this.maxRadius = maxRadius;
        this.currentRadius = 10;
        this.color = color;
        this.alpha = 1.0;
      }

      update(dt) {
        this.currentRadius += (this.maxRadius - this.currentRadius) * dt * 14;
        this.alpha -= dt * 2.2;
      }

      draw(ctx) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.currentRadius, 0, Math.PI * 2);
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 4;
        ctx.globalAlpha = Math.max(0, this.alpha);
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 14;
        ctx.stroke();
        ctx.restore();
      }
    }

    class AnimatedLightningStrike {
      constructor(x, y) {
        this.x = x;
        this.y = y;
        this.alpha = 1.0;
      }

      update(dt) {
        this.alpha -= dt * 4.0;
      }

      draw(ctx) {
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(this.x + (Math.random()*20 - 10), this.y - 400);
        ctx.lineTo(this.x + (Math.random()*15 - 7), this.y - 200);
        ctx.lineTo(this.x + (Math.random()*10 - 5), this.y - 100);
        ctx.lineTo(this.x, this.y);
        ctx.strokeStyle = '#facc15';
        ctx.lineWidth = 6;
        ctx.globalAlpha = Math.max(0, this.alpha);
        ctx.shadowColor = '#fff';
        ctx.shadowBlur = 16;
        ctx.stroke();
        ctx.restore();
      }
    }

    class AnimatedFireExplosion {
      constructor(x, y, radius) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.alpha = 1.0;
      }

      update(dt) {
        this.alpha -= dt * 3.0;
      }

      draw(ctx) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius * (1.2 - this.alpha*0.2), 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(239, 68, 68, ' + Math.max(0, this.alpha*0.6) + ')';
        ctx.fill();
        ctx.strokeStyle = '#f97316';
        ctx.lineWidth = 4;
        ctx.stroke();
        ctx.restore();
      }
    }

    class AnimatedWaterWave {
      constructor(x, y, angle) {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.dist = 0;
        this.alpha = 1.0;
      }

      update(dt) {
        this.dist += 380 * dt;
        this.alpha -= dt * 2.0;
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x + Math.cos(this.angle)*this.dist, this.y + Math.sin(this.angle)*this.dist);
        ctx.rotate(this.angle);
        ctx.beginPath();
        ctx.arc(0, 0, 45, -Math.PI*0.4, Math.PI*0.4);
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 6;
        ctx.globalAlpha = Math.max(0, this.alpha);
        ctx.stroke();
        ctx.restore();
      }
    }

    class HadesDivineStaffSlashFX {
      constructor(x, y, angle, reach, slashType = 'golden', isFullCircle = false, visualScale = 1, opacity = 1) {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.reach = reach;
        this.slashType = slashType;
        this.isFullCircle = isFullCircle;
        this.visualScale = visualScale;
        this.opacity = opacity;
        this.duration = 0.24;
        this.maxDuration = 0.24;
        this.alpha = 1.0;
      }

      update(dt) {
        this.duration -= dt;
        this.alpha = Math.max(0, this.duration / this.maxDuration);
      }

      draw(ctx) {
        if (this.duration <= 0) return;
        const img = loadedImages['gods_boon_slashes'] || loadedImages['ruyi_staff_slashes'];
        if (img && img.complete && img.naturalWidth > 0) {
          const cellW = 160;
          const cellH = 160;
          const progress = 1 - (this.duration / this.maxDuration);

          let r = 0;
          let frameOffset = 0;
          let frameCount = 8;

          if (this.slashType === 'fire') {
            r = 1; // Row 1: Fire Phoenix slashes (8 frames)
            frameCount = 8;
          } else if (this.slashType === 'thunder') {
            r = 2; // Row 2: Azure/Violet Lightning slashes (8 frames)
            frameCount = 8;
          } else if (this.slashType === 'water') {
            r = 3; // Row 3: Water Tidal spray slashes (frames 0..3)
            frameOffset = 0;
            frameCount = 4;
          } else if (this.slashType === 'ice') {
            r = 3; // Row 3: Lunar Frost Ice blades (frames 4..7)
            frameOffset = 4;
            frameCount = 4;
          } else if (this.slashType === 'wind') {
            r = 4; // Row 4: Jade Wind Gale Tornado (frames 0..3)
            frameOffset = 0;
            frameCount = 4;
          } else if (this.slashType === 'alchemy') {
            r = 4; // Row 4: Purple-Bronze Alchemy Fire (frames 4..7)
            frameOffset = 4;
            frameCount = 4;
          } else {
            r = 0; // Row 0: Golden Sun / Buddha Holy Light (8 frames)
            frameCount = 8;
          }

          const c = frameOffset + Math.min(frameCount - 1, Math.floor(progress * frameCount));

          ctx.save();
          ctx.translate(this.x, this.y);
          ctx.rotate(this.angle);

          // 4x Smaller, sleek, tight, and aligned with staff tip
          const scale = (this.reach / 210) * 0.28 * this.visualScale;
          const drawW = cellW * scale;
          const drawH = cellH * scale;

          ctx.globalAlpha = Math.max(0, this.alpha * this.opacity);
          ctx.drawImage(img, c * cellW, r * cellH, cellW, cellH, 16, -drawH / 2, drawW, drawH);
          ctx.restore();
        }
      }
    }

    class ColossalStaffNovaFX {
      constructor(x, y, radius = 320, color = '#facc15') {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.color = color;
        this.duration = 0.44;
        this.maxDuration = 0.44;
        this.alpha = 1.0;
        this.rotation = Math.random() * Math.PI * 2;
      }

      update(dt) {
        this.duration -= dt;
        this.alpha = Math.max(0, this.duration / this.maxDuration);
        this.rotation += dt * 2.8;
      }

      draw(ctx) {
        if (this.duration <= 0) return;
        const img = loadedImages['hades_magic_circles'];
        if (img && img.complete && img.naturalWidth > 0) {
          const cellW = 200;
          const cellH = 200;
          const progress = 1 - (this.duration / this.maxDuration);
          const c = Math.min(5, Math.floor(progress * 6));
          const r = 2; // Row 2: Colossal 360° Circular Staff Cleave Nova & Starburst

          ctx.save();
          ctx.translate(this.x, this.y);
          ctx.rotate(this.rotation);

          const visualRadius = Math.min(160, this.radius * 0.62);
          const scale = (visualRadius / 100) * 0.92;
          const drawW = cellW * scale;
          const drawH = cellH * scale;

          ctx.globalAlpha = Math.max(0, this.alpha);
          ctx.drawImage(img, c * cellW, r * cellH, cellW, cellH, -drawW / 2, -drawH / 2, drawW, drawH);

          // Additional stylized luminous shockwave ring
          ctx.beginPath();
          ctx.arc(0, 0, visualRadius * (0.6 + progress * 0.45), 0, Math.PI * 2);
          ctx.strokeStyle = '#ffffff';
          ctx.lineWidth = 4 * this.alpha;
          ctx.shadowColor = this.color;
          ctx.shadowBlur = 24;
          ctx.stroke();

          ctx.restore();
        }
      }
    }

    class GroundSmashPillarEruptionFX {
      constructor(x, y, radius = 280, color = '#facc15') {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.color = color;
        this.duration = 0.46;
        this.maxDuration = 0.46;
        this.alpha = 1.0;
      }

      update(dt) {
        this.duration -= dt;
        this.alpha = Math.max(0, this.duration / this.maxDuration);
      }

      draw(ctx) {
        if (this.duration <= 0) return;
        const img = loadedImages['ruyi_staff_slashes'];
        if (img && img.complete && img.naturalWidth > 0) {
          const cellW = 200;
          const cellH = 200;
          const progress = 1 - (this.duration / this.maxDuration);
          const c = Math.min(4, Math.floor(progress * 5));
          const r = 3; // Row 3: Ground Smash Eruption Light Beams & Rupture

          ctx.save();
          ctx.translate(this.x, this.y);

          const visualRadius = Math.min(145, this.radius * 0.58);
          const scale = (visualRadius / 100) * 0.9;
          const drawW = cellW * scale;
          const drawH = cellH * scale;

          ctx.globalAlpha = Math.max(0, this.alpha);
          ctx.drawImage(img, c * cellW, r * cellH, cellW, cellH, -drawW / 2, -drawH + 30, drawW, drawH);
          ctx.restore();
        }
      }
    }

    class HadesMagicCircleAOEFX {
      constructor(x, y, radius = 190, duration = 5.0, color = '#facc15') {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.duration = duration;
        this.maxDuration = duration;
        this.color = color;
        this.rotation = 0;
      }

      update(dt) {
        this.duration -= dt;
        this.rotation += dt * 0.4;
      }

      draw(ctx) {
        if (this.duration <= 0) return;
        const img = loadedImages['hades_magic_circles'];
        if (img && img.complete && img.naturalWidth > 0) {
          const cellW = 200;
          const cellH = 200;
          const animFrame = Math.floor((Date.now() / 120) % 6);

          ctx.save();
          ctx.translate(this.x, this.y);
          ctx.rotate(this.rotation);

          const alpha = this.duration < 0.5 ? (this.duration / 0.5) : (this.maxDuration - this.duration < 0.3 ? (this.maxDuration - this.duration)/0.3 : 0.95);
          ctx.globalAlpha = Math.max(0, alpha);

          const scale = (this.radius / 95);
          const drawW = cellW * scale;
          const drawH = cellH * scale;

          ctx.drawImage(img, animFrame * cellW, 0, cellW, cellH, -drawW / 2, -drawH / 2, drawW, drawH);
          ctx.restore();
        }
      }
    }

    class RuyiImpactBurstFX {
      constructor(x, y, scale = 0.8) {
        this.x = x;
        this.y = y;
        this.scale = scale;
        this.duration = 0.36;
        this.maxDuration = 0.36;
        this.alpha = 1;
      }

      update(dt) {
        this.duration -= dt;
        this.alpha = Math.max(0, Math.min(1, this.duration / 0.12));
      }

      draw(ctx) {
        const img = loadedImages['ruyi_impact_burst'];
        if (!img || !img.complete || !img.naturalWidth || this.duration <= 0) return;
        const progress = Math.max(0, Math.min(0.999, 1 - this.duration / this.maxDuration));
        const frame = Math.min(7, Math.floor(progress * 8));
        const cellW = img.naturalWidth / 4;
        const cellH = img.naturalHeight / 2;
        const col = frame % 4;
        const row = Math.floor(frame / 4);
        const size = Math.min(142, 132 * this.scale);
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.globalAlpha = this.alpha;
        ctx.globalCompositeOperation = 'lighter';
        ctx.drawImage(img, col * cellW, row * cellH, cellW, cellH, -size / 2, -size / 2, size, size);
        ctx.restore();
      }
    }

    class HadesHitSparkFX {
      constructor(x, y, angle = 0, color = '#ffffff') {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.color = color;
        this.duration = 0.18;
        this.maxDuration = 0.18;
        this.frame = Math.floor(Math.random() * 5);
      }

      update(dt) {
        this.duration -= dt;
      }

      draw(ctx) {
        if (this.duration <= 0) return;
        const img = loadedImages['hades_magic_circles'];
        if (img && img.complete && img.naturalWidth > 0) {
          const cellW = 200;
          const cellH = 200;
          const progress = 1 - (this.duration / this.maxDuration);
          const c = Math.min(4, Math.floor(progress * 5));
          const r = 3; // Row 3: White-hot Hit Impact Stars

          ctx.save();
          ctx.translate(this.x, this.y);
          ctx.rotate(this.angle);

          const scale = 0.55;
          const drawW = cellW * scale;
          const drawH = cellH * scale;

          ctx.globalAlpha = Math.max(0, this.duration / this.maxDuration);
          ctx.drawImage(img, c * cellW, r * cellH, cellW, cellH, -drawW / 2, -drawH / 2, drawW, drawH);
          ctx.restore();
        }
      }
    }

    class StaffMotionWaveFX {
      constructor(x, y, angle, reach, color = '#facc15') {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.reach = reach;
        this.color = color;
        this.alpha = 1.0;
      }

      update(dt) {
        this.alpha -= dt * 3.5;
      }

      draw(ctx) {
        if (this.alpha <= 0) return;
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);

        // 4x Smaller, sleek weapon tip wind arc
        const arcRadius = 40 + (1 - this.alpha) * 8;
        ctx.beginPath();
        ctx.arc(0, 0, arcRadius, -0.45, 0.45);
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 3.5 * this.alpha;
        ctx.lineCap = 'round';
        ctx.globalAlpha = Math.max(0, this.alpha * 0.7);
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 8;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(0, 0, arcRadius + 1, -0.35, 0.35);
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5 * this.alpha;
        ctx.stroke();

        ctx.restore();
      }
    }

    class GlowingHairTrailFX {
      constructor(startX, startY, targetX, targetY, color = '#facc15') {
        this.x = startX;
        this.y = startY;
        this.startX = startX;
        this.startY = startY;
        this.targetX = targetX;
        this.targetY = targetY;
        this.progress = 0;
        this.color = color;
        this.alpha = 1.0;
        this.curve = (Math.random() - 0.5) * 80;
      }

      update(dt) {
        this.progress += dt * 3.2;
        if (this.progress >= 1.0) {
          this.alpha = 0;
        } else {
          const t = this.progress;
          const midX = (this.startX + this.targetX) / 2 - this.curve;
          const midY = (this.startY + this.targetY) / 2 - 60;
          this.x = (1 - t) * (1 - t) * this.startX + 2 * (1 - t) * t * midX + t * t * this.targetX;
          this.y = (1 - t) * (1 - t) * this.startY + 2 * (1 - t) * t * midY + t * t * this.targetY;
        }
      }

      draw(ctx) {
        if (this.alpha <= 0) return;
        ctx.save();
        ctx.beginPath();
        ctx.arc(this.x, this.y, 4, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.shadowColor = '#fff';
        ctx.shadowBlur = 12;
        ctx.fill();
        ctx.restore();
      }
    }

    let monkeyClones = [];

    class HouZhiHouShunClone {
      constructor(x, y, targetX, targetY) {
        this.x = x;
        this.y = y;
        this.originX = targetX;
        this.originY = targetY;
        this.radius = 18;
        this.speed = 230 + Math.random() * 70;
        this.duration = 4.5;
        this.alive = true;
        this.state = 'run';
        this.facing = 1;
        this.attackCooldown = 0.2 + Math.random() * 0.2;
        this.attackDuration = 0;
        this.attackMaxDuration = 0.42;
        this.targetEnemy = null;
        this.animTimer = Math.random() * 10;
        this.dissolveTimer = 0.55;
      }

      update(dt) {
        if (!this.alive) return;
        this.duration -= dt;
        this.animTimer += dt;

        if (this.duration <= 0.55) {
          this.state = 'smash_dissolve';
          this.dissolveTimer -= dt;
          if (this.dissolveTimer <= 0) {
            this.alive = false;
            const cloneColor = getAlignmentPath() === 'neutral' ? '#facc15' : getAlignmentPalette().primary;
            fxList.push(new RadialSparksFX(this.x, this.y, 8, cloneColor, 30));
            if ((player.alignmentEffects?.voidDamage || 0) > 0 && getAlignmentPath() === 'evil') {
              fxList.push(new HadesMagicCircleAOEFX(this.x, this.y, 58, .42, '#a855f7'));
            }
          }
          return;
        }

        let nearestEnemy = null;
        let minDist = 340;
        enemies.forEach(e => {
          if (!e.alive || e.isAlly) return;
          const d = Math.hypot(e.x - this.x, e.y - this.y);
          if (d < minDist) {
            minDist = d;
            nearestEnemy = e;
          }
        });
        this.targetEnemy = nearestEnemy;

        if (this.state === 'attack') {
          this.attackDuration -= dt;
          if (this.attackDuration <= 0) {
            this.state = 'run';
            this.attackCooldown = 0.35 + Math.random() * 0.2;
          }
        } else {
          this.attackCooldown -= dt;

          let targetX = this.originX;
          let targetY = this.originY;

          if (this.targetEnemy) {
            targetX = this.targetEnemy.x;
            targetY = this.targetEnemy.y;
          }

          const dist = Math.hypot(targetX - this.x, targetY - this.y);
          const ang = Math.atan2(targetY - this.y, targetX - this.x);

          if (dist > 40) {
            this.x += Math.cos(ang) * this.speed * dt;
            this.y += Math.sin(ang) * this.speed * dt;
            this.facing = Math.cos(ang) < 0 ? -1 : 1;
            this.state = 'run';
          } else if (this.targetEnemy && this.attackCooldown <= 0) {
            this.state = 'attack';
            this.attackDuration = this.attackMaxDuration;
            this.facing = (this.targetEnemy.x - this.x) < 0 ? -1 : 1;

            let dmg = 26;
            if (player.boons.cast) {
              dmg *= (1 + 0.35 * (player.boons.cast.level || 1));
            }
            dmg *= 1 + (player.alignmentEffects?.cloneDamage || 0);
            this.targetEnemy.takeDamage(dmg, false, false);
            this.targetEnemy.knockbackX += Math.cos(ang) * 90;
            this.targetEnemy.knockbackY += Math.sin(ang) * 90;
            fxList.push(new SlashSparksFX(this.targetEnemy.x, this.targetEnemy.y, ang, getAlignmentPath() === 'neutral' ? '#facc15' : getAlignmentPalette().primary));
            sound.playStaffSwing(0, false);
          }
        }
      }

      draw(ctx) {
        if (!this.alive) return;
        ctx.save();
        ctx.translate(this.x, this.y);

        const img = loadedImages['wukong_hair_clones'];
        if (img && img.complete && img.naturalWidth > 0) {
          const cellW = 200;
          const cellH = 200;

          let r = 1;
          let c = 0;

          if (this.state === 'smash_dissolve') {
            r = 3; // Leap smash & dissolve (Row 3, 6 frames)
            const prog = 1 - Math.max(0, this.dissolveTimer / 0.55);
            c = Math.min(5, Math.floor(prog * 6));
          } else if (this.state === 'attack') {
            r = 2; // Staff flurry strike (Row 2, 6 frames)
            const prog = 1 - Math.max(0, this.attackDuration / this.attackMaxDuration);
            c = Math.min(5, Math.floor(prog * 6));
          } else {
            r = 1; // Running (Row 1, 6 frames)
            c = Math.floor((this.animTimer * 12) % 6);
          }

          const scale = 0.65 * PACKED_VISUAL_SCALE_200;
          const drawW = cellW * scale;
          const drawH = cellH * scale;

          if (this.facing === -1) {
            ctx.scale(-1, 1);
          }
          if (getAlignmentPath() !== 'neutral') {
            ctx.shadowColor = getAlignmentPalette().primary;
            ctx.shadowBlur = 9;
          }
          ctx.drawImage(img, c * cellW, r * cellH, cellW, cellH, -drawW / 2, 44 - (cellH - 48) * scale, drawW, drawH);
        } else {
          ctx.beginPath();
          ctx.arc(0, 0, 14, 0, Math.PI * 2);
          ctx.fillStyle = '#facc15';
          ctx.fill();
        }

        ctx.restore();
      }
    }

    // Keep combat readable: authored animation and hit FX carry the impact,
    // while the camera supplies only a short, restrained confirmation. Even
    // the former 20px ultimate shakes now peak at 3px, and overlapping skills
    // can never stack above that cap. Reduced-motion users receive no shake.
    const SCREEN_SHAKE_SCALE = 0.18;
    const SCREEN_SHAKE_MAX_PX = 3;
    const SCREEN_SHAKE_DECAY_PER_SECOND = 36;
    function createScreenShake(amount) {
      if (gameState.reducedMotion) {
        gameState.screenShake = 0;
        return;
      }
      const softenedAmount = Math.min(SCREEN_SHAKE_MAX_PX, Math.max(0, Number(amount) || 0) * SCREEN_SHAKE_SCALE);
      gameState.screenShake = Math.max(gameState.screenShake || 0, softenedAmount);
    }

    // BUDDHA APPROVAL CUTSCENE LOGIC
    let buddhaCutsceneSlides = [];
    let buddhaCutsceneStep = 0;
    let buddhaCutsceneChapter = 0;
    let buddhaCutsceneActive = false;

    function renderBuddhaCutsceneStep() {
      const slide = buddhaCutsceneSlides[buddhaCutsceneStep];
      if (!slide) return;
      const frame = document.getElementById('buddha-cutscene-frame');
      document.getElementById('buddha-cutscene-speaker').innerText = slide.speaker;
      document.getElementById('buddha-cutscene-quote').innerText = slide.text;
      document.getElementById('buddha-cutscene-counter').innerText = `${buddhaCutsceneStep + 1} / ${buddhaCutsceneSlides.length}`;
      frame.className = `cutscene-frame focus-${slide.focus || 'narrator'}`;
      void frame.offsetWidth;
      frame.classList.add('slide-enter');
      const isLast = buddhaCutsceneStep >= buddhaCutsceneSlides.length - 1;
      const reward = document.getElementById('buddha-cutscene-reward');
      reward.style.display = isLast ? 'block' : 'none';
      document.getElementById('buddha-cutscene-btn').innerText = isLast
        ? uiText('五指山下 · 等候取经人', 'Beneath Five-Finger Mountain · Continue')
        : uiText('下一幕 ➔', 'Next Slide ➔');
    }

    function nextBuddhaCutsceneStep() {
      if (buddhaCutsceneStep >= buddhaCutsceneSlides.length - 1) {
        closeBuddhaApprovalCutscene();
        return;
      }
      buddhaCutsceneStep++;
      renderBuddhaCutsceneStep();
      sound.playJadeChime();
    }

    function triggerBuddhaApprovalCutscene() {
      const isCampaignBuddha = gameState.chamberIndex === 32;
      if (isCampaignBuddha && gameState.buddhaImprisoned) return;
      if (buddhaCutsceneActive) return;
      buddhaCutsceneActive = true;
      // Capture the chapter that opened the cutscene. The player can advance to a
      // story chapter from a boss-outcome modal, so closing logic must never infer
      // its destination from a later, mutable chamberIndex value.
      buddhaCutsceneChapter = gameState.chamberIndex;
      beginDialoguePause();
      projectiles = [];
      sound.playGong();
      setTimeout(() => sound.playJadeChime(), 300);

      const modal = document.getElementById('buddha-modal');
      const title = document.getElementById('buddha-cutscene-title');
      const subtitle = document.getElementById('buddha-cutscene-subtitle');
      const reward = document.getElementById('buddha-cutscene-reward');
      const cinematicImage = document.getElementById('buddha-cutscene-image');
      const cinematicArt = loadedImages[isCampaignBuddha ? 'cutscene_five_finger' : 'cutscene_vulture_peak'];
      if (cinematicArt?.src) {
        cinematicImage.src = cinematicArt.src;
        cinematicImage.alt = uiText('如来神掌化作五指山的剧情插画', 'Buddha’s palm becoming Five-Finger Mountain');
      }
      buddhaCutsceneStep = 0;

      if (isCampaignBuddha) {
        gameState.buddhaImprisoned = true;
        const buddha = enemies.find(enemy => enemy.typeKey === 'campaign_buddha');
        if (buddha) {
          buddha.alive = true;
          buddha.isDying = false;
          buddha.isSubdued = true;
          buddha.outcomeResolved = false;
          buddha.hp = Math.round(buddha.maxHp * .5);
          buddha.isAttacking = false;
          buddha.pendingBossAttack = null;
          buddha.telegraphZone = null;
        }
        if (gameState.language === 'en') {
          title.innerText = 'Tathagata Buddha · Five Fingers Become a Mountain';
          subtitle.innerText = 'Half Health Reached · The Buddha-Realm Closes';
          reward.innerText = '🖐 Story turn: Buddha can no longer be damaged. His five fingers become a mountain, and Tang Sanzang begins the next chapter.';
          buddhaCutsceneSlides = [
            { speaker:'Tathagata Buddha', focus:'boss', text:'Wukong, forcing back half my radiance proves your courage—but you have not yet seen the restless heart within you.' },
            { speaker:'Storyteller', focus:'narrator', text:'The Buddha’s five fingers descend through the golden cloud and become five mountain peaks. The battle ends without a killing blow.' },
            { speaker:'Tathagata Buddha', focus:'wukong', text:'Listen to five hundred years of rain beneath this mountain. When the pilgrim removes the seal, use that staff to protect a road longer than victory.' },
          ];
        } else {
          title.innerText = '如来佛祖 · 五指化山';
          subtitle.innerText = '战至半血 · 掌中佛国落定';
          reward.innerText = '🖐 剧情转折：如来不再受伤，以五指化山镇住悟空。下一章由唐三藏开启西行。';
          buddhaCutsceneSlides = [
            { speaker:'如来佛祖', focus:'boss', text:'悟空，你能逼退我半身佛光，已见勇力；却仍未见自己的狂心。' },
            { speaker:'章回旁白', focus:'narrator', text:'佛祖五指穿过金云，化作五座山峰落下。此战不以杀戮结束，齐天大圣被镇于山下。' },
            { speaker:'如来佛祖', focus:'wukong', text:'且听五百年风雨。待取经人揭去金帖，你再用这根金箍棒护一条比胜负更长的路。' },
          ];
        }
      } else {
        player.increaseRunMaxHp(100, 100);
        player.hp = player.maxHp;
        player.lives += 1;
        player.qi = player.maxQi;
        title.innerText = uiText('如来佛祖 · 斗战得证', 'Tathagata Buddha · Trial Acknowledged');
        subtitle.innerText = uiText('勇力之外 · 亦见本心', 'Beyond Strength · The Heart Revealed');
        reward.innerText = uiText('☸ 佛光赐福：气血与真气圆满，并增添一尊金身。', '☸ Buddha’s blessing: Health and Qi restored, with one additional life.');
        buddhaCutsceneSlides = gameState.language === 'en' ? [
          { speaker:'Storyteller', focus:'narrator', text:'The clash falls silent. Golden light settles over the road Wukong has crossed.' },
          { speaker:'Tathagata Buddha', focus:'boss', text:'Power brought you here; restraint decides what that power becomes.' },
          { speaker:'Sun Wukong', focus:'wukong', text:'Then let the road judge me. My staff will strike when it must—and rest when it should.' },
        ] : [
          { speaker:'章回旁白', focus:'narrator', text:'棍影与佛光一同归静，金辉落满悟空走过的西行路。' },
          { speaker:'如来佛祖', focus:'boss', text:'勇力带你来到此处，克制才决定这份勇力最终成为何物。' },
          { speaker:'孙悟空', focus:'wukong', text:'那便让西行路来评俺。该打时打，该收时收！' },
        ];
      }
      updateHUD();

      document.getElementById('buddha-cutscene-mode').innerText = uiText('🎞 五指山影卷', '🎞 FIVE-FINGER CHRONICLE');
      document.getElementById('buddha-cutscene-art-label').innerText = isCampaignBuddha
        ? uiText('如来神掌 · 五指化山', 'Buddha’s Palm · Five Fingers Become a Mountain')
        : uiText('灵山佛光 · 斗战得证', 'Vulture Peak · The Trial Acknowledged');
      document.getElementById('buddha-cutscene-hint').innerText = uiText('战斗保持暂停 · 悟空不会受到攻击', 'Combat remains paused · Wukong cannot be attacked');
      renderBuddhaCutsceneStep();
      modal.style.display = 'flex';
    }

    function closeBuddhaApprovalCutscene() {
      // Double-clicks and repeated Enter/Space events may arrive after the first
      // close has already advanced to Tang Sanzang's chapter. Ignore them instead
      // of executing a second progression branch against the new chamber state.
      if (!buddhaCutsceneActive) return;
      buddhaCutsceneActive = false;
      document.getElementById('buddha-modal').style.display = 'none';
      const completedCutsceneChapter = buddhaCutsceneChapter || gameState.chamberIndex;
      buddhaCutsceneSlides = [];
      buddhaCutsceneStep = 0;
      buddhaCutsceneChapter = 0;
      endDialoguePause(false);
      if (completedCutsceneChapter === 32) {
        const buddha = enemies.find(enemy => enemy.typeKey === 'campaign_buddha' && enemy.isSubdued);
        gameState.bossOutcomeContinuation = () => {
          gameState.chamberCleared = true;
          startChamber(33);
        };
        if (buddha) openBossOutcomeChoice([buddha]);
        else gameState.bossOutcomeContinuation();
      } else {
        // The old endless-mode build jumped to chamber 151 here. In the unified
        // 100-chapter campaign that corrupts progression and makes the next gate
        // award an immediate victory. A non-campaign Buddha approval is terminal.
        gameState.isPaused = false;
        gameState.chamberCleared = true;
        handleGameOver(true);
      }
    }

    // AUTHENTIC JOURNEY TO THE WEST BOSS DIALOGUES & SPEECH BUBBLES
    let speechBubbles = [];

    class SpeechBubbleFX {
      constructor(entity, text, duration = 3.5, color = '#fef08a', bgColor = 'rgba(20, 15, 35, 0.92)') {
        this.entity = entity;
        this.text = text;
        this.duration = duration;
        this.maxDuration = duration;
        this.color = color;
        this.bgColor = bgColor;
        this.alpha = 1.0;
      }

      update(dt) {
        this.duration -= dt;
        if (this.duration <= 0.4) {
          this.alpha = Math.max(0, this.duration / 0.4);
        }
      }

      draw(ctx) {
        if (this.duration <= 0 || !this.entity || (!this.entity.alive && !this.entity.isDying)) return;
        ctx.save();
        ctx.translate(this.entity.x, this.entity.y - (this.entity.radius || 40) - 45);

        ctx.font = getCanvasFont(15, 700);
        const textMetrics = ctx.measureText(this.text);
        const padX = 14;
        const padY = 8;
        const bubbleW = textMetrics.width + padX * 2;
        const bubbleH = 30;

        ctx.globalAlpha = Math.max(0, this.alpha);

        ctx.fillStyle = this.bgColor;
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 2;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 12;

        ctx.beginPath();
        ctx.roundRect(-bubbleW / 2, -bubbleH, bubbleW, bubbleH, 8);
        ctx.fill();
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(-6, 0);
        ctx.lineTo(0, 8);
        ctx.lineTo(6, 0);
        ctx.closePath();
        ctx.fillStyle = this.bgColor;
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = this.color;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.shadowBlur = 4;
        ctx.fillText(this.text, 0, -bubbleH / 2);

        ctx.restore();
      }
    }

    const BOSS_DIALOGUES = {
      30: {
        bossName: '百眼魔君与盘丝蛛后',
        bossTitle: '盘丝岭黄花观',
        bossPortrait: 'monsters_beasts',
        bossCol: 1, bossRow: 0,
        dialogues: [
          { speaker: 'boss', name: '百眼魔君', text: '泼猴！五百年前你在天庭偷蟠桃盗仙丹，今日竟敢擅闯我盘丝岭黄花观！看我千目金光与盘丝剧毒大阵，将你这猢狲化作一滩脓血！' },
          { speaker: 'wukong', name: '孙悟空', text: '嘿嘿！你这披毛戴角、湿生卵化的孽障！俺老孙当年大闹天宫十万天兵都不怕，还怕你几根蛛丝不成？吃俺老孙一棒！' }
        ]
      },
      60: {
        bossName: '白骨夫人',
        bossTitle: '白虎岭白骨洞',
        bossPortrait: 'bosses_real_anims',
        bossCol: 0, bossRow: 0,
        dialogues: [
          { speaker: 'boss', name: '白骨夫人', text: '齐天大圣，别来无恙！昔日你在白虎岭三打于我，害得唐僧将你逐回花果山！今日在这幽冥魔境，你休想再逃出我的白骨幽冥阵！' },
          { speaker: 'wukong', name: '孙悟空', text: '妖精！俺老孙火眼金睛早已看穿你那幻化皮囊！管你变少女、老妪还是骷髅，如意金箍棒下从无活鬼！纳命来！' }
        ]
      },
      90: {
        bossName: '金角大王与银角大王',
        bossTitle: '平顶山莲花洞',
        bossPortrait: 'infinite_bosses_a',
        bossCol: 2, bossRow: 0,
        dialogues: [
          { speaker: 'boss', name: '金角大王', text: '孙行者！我叫你一声，你可敢应？我这紫金红葫芦连太乙真仙都能吸入化为浓水，幌金绳七星剑早已布下天罗地网！' },
          { speaker: 'wukong', name: '孙悟空', text: '俺老孙叫者行孙、行者孙！莫说你偷老君的破葫芦，便是整座平顶山压下来，也伤不得俺老孙分毫！看棒！' }
        ]
      },
      120: {
        bossName: '二郎显圣真君',
        bossTitle: '南天门与灌江口',
        bossPortrait: 'erlang_and_dog',
        bossCol: 0, bossRow: 0,
        dialogues: [
          { speaker: 'boss', name: '二郎显圣真君', text: '孙悟空！当年花果山大战，你七十二变输我七十三变，被我神鹰细犬所擒！今日灵霄宝殿前，且看我三尖两刃枪再决高下！' },
          { speaker: 'wukong', name: '孙悟空', text: '杨戬小儿！当年若非太上老君金刚琢暗算偷袭，俺老孙怎会落败？今日在这南天门，俺老孙便让你输得心服口服！' }
        ]
      },
      150: {
        bossName: '大日如来佛祖',
        bossTitle: '西天大雷音寺',
        bossPortrait: 'buddha_colossal',
        bossCol: 0, bossRow: 0,
        dialogues: [
          { speaker: 'boss', name: '大日如来佛祖', text: '悟空，你这顽猴！昔日你夸下海口跳出三界，却跳不出吾之手掌心，被压在五行山下受五百年风霜雨雪，每日饮铜汁食铁丸！今日重临，可悟得何为万法皆空？' },
          { speaker: 'wukong', name: '孙悟空', text: '如来！当年你欺俺老孙不识乾坤八卦，以五指化山压俺五百年！今日俺老孙身怀混元道果，誓要破这五行定数，直捣九重天阙！' }
        ]
      },
      180: {
        bossName: '通臂猿猴',
        bossTitle: '混沌渊海·混世心魔',
        bossPortrait: 'bosses_real_anims',
        bossCol: 0, bossRow: 2,
        dialogues: [
          { speaker: 'boss', name: '通臂猿猴', text: '孙悟空！同为混世四猴，你享尽齐天大圣万世威名，受诸天神佛供奉；而我通臂猿猴拿日月、缩千山，却只能永坠幽冥混沌！今日这天地神位，合该归我！' },
          { speaker: 'wukong', name: '孙悟空', text: '六耳同源，心魔丛生！俺老孙历经九九八十一难，方知神通皆由心生！你若执迷不悟欲灭三界，俺便一棒打碎你这万丈心魔！' }
        ]
      }
    };

    const CAMPAIGN_DIALOGUES = {
      5: {
        bossName: '花果山老猿寨主', bossTitle: '群猴试艺·山巅之争', bossPortrait: 'campaign_characters_act1', bossCol: 0, bossRow: 1, portraitCols: 7, portraitRows: 5,
        dialogues: [
          { speaker: 'boss', name: '老猿寨主', text: '石猴，你一路胜过群猴，却只凭蛮力还做不得我花果山之王。山巅这一关，须让我看见你的胆与心！' },
          { speaker: 'wukong', name: '孙悟空', text: '俺也去水帘洞、登绝壁，从未退过半步。来吧！俺若胜了，便带孩儿们寻真正的长生本领！' }
        ]
      },
      6: {
        bossName: '元始天尊', bossTitle: '昆仑天梯·三乘变化之问', bossPortrait: 'campaign_characters_act1', bossCol: 0, bossRow: 3, portraitCols: 7, portraitRows: 5, isBattle: false, onComplete: 'transformationChoice',
        dialogues: [
          { speaker: 'boss', name: '元始天尊', text: '灵明石猴，你越沧海、登昆仑，所求是长生，还是胜尽天下？我有十八斗战之变、三十六天罡之变、七十二地煞之变。' },
          { speaker: 'wukong', name: '孙悟空', text: '长生要得，自在也要得！天尊且说三法之别，俺老孙自己选一条走到底。' },
          { speaker: 'boss', name: '元始天尊', text: '十八重攻伐，三十六攻守圆融，七十二变化无穷。择定之后，先过我玉虚门人，再亲来受我一试。' }
        ]
      },
      12: {
        bossName: '元始天尊', bossTitle: '玉虚宫·传法终试', bossPortrait: 'campaign_characters_act1', bossCol: 0, bossRow: 3, portraitCols: 7, portraitRows: 5,
        dialogues: [
          { speaker: 'boss', name: '元始天尊', text: '诸弟子皆败于你手。悟空，神通若无心性驾驭，越强越易反伤自身。今日我亲自守最后一关。' },
          { speaker: 'wukong', name: '孙悟空', text: '道理俺也去听，真本事也要学！天尊莫留手，让俺也去看昆仑仙法能否挡住花果山的棍！' },
          { speaker: 'boss', name: '元始天尊', text: '好。胜过此阵，你所择变化便算真正入门；再往东海寻一件与你心意相通的兵器吧。' }
        ]
      },
      18: {
        bossName: '东海龙王·敖广', bossTitle: '水晶宫·定海神珍', bossPortrait: 'campaign_characters_act1', bossCol: 0, bossRow: 4, portraitCols: 7, portraitRows: 5,
        dialogues: [
          { speaker: 'boss', name: '东海龙王', text: '上仙连败水族，却说只为借兵器？定海神珍重一万三千五百斤，镇住海眼，岂能任你拿去！' },
          { speaker: 'wukong', name: '孙悟空', text: '小刀小枪俺也去嫌轻。那铁柱见俺便放金光，分明在等主人！龙王，打赢你俺再取，绝不白拿！' },
          { speaker: 'boss', name: '东海龙王', text: '狂猴！若你真能令神珍认主，本王便连披挂一并相赠。先接我东海万潮！' }
        ]
      },
      19: {
        bossName: '东海龙王·敖广', bossTitle: '龙宫宝库·神兵认主', bossPortrait: 'campaign_characters_act1', bossCol: 6, bossRow: 4, portraitCols: 7, portraitRows: 5, isBattle: false,
        dialogues: [
          { speaker: 'boss', name: '东海龙王', text: '神珍竟自行缩作一根乌铁棍，金箍上正写着“如意金箍棒”。此宝既认你，本王信守诺言。' },
          { speaker: 'wukong', name: '孙悟空', text: '大，大，大！小，小，小！果然如意！老龙王，多谢宝贝。俺也去天上瞧瞧，那些神仙凭什么管俺花果山！' }
        ]
      },
      22: {
        bossName: '三坛海会大神·哪吒', bossTitle: '南天门·风火轮前', bossPortrait: 'campaign_characters_act2', bossCol: 0, bossRow: 0, portraitCols: 7, portraitRows: 5,
        dialogues: [
          { speaker: 'boss', name: '哪吒', text: '妖猴止步！你闯南天门、惊扰凌霄，先问我火尖枪与乾坤圈答不答应！' },
          { speaker: 'wukong', name: '孙悟空', text: '小哪吒，你三头六臂，俺有千般变化。俺也去不欺你年少，放马过来！' }
        ]
      },
      24: {
        bossName: '东方持国天王·魔礼海', bossTitle: '东天门·碧玉琵琶', bossPortrait: 'four_heavenly_kings', bossCol: 0, bossRow: 0, portraitCols: 7, portraitRows: 4,
        dialogues: [
          { speaker: 'boss', name: '持国天王', text: '我以碧玉琵琶持国安民，四弦一动便有十万天音化刃。妖猴，东天门不是你撒野之地！' },
          { speaker: 'wukong', name: '孙悟空', text: '俺也去听过仙乐，却没听过拿琴弦吓猴的。持国天王，先看你的音刃快，还是俺的金箍棒快！' }
        ]
      },
      25: {
        bossName: '南方增长天王·魔礼青', bossTitle: '南天门·青锋宝剑', bossPortrait: 'four_heavenly_kings', bossCol: 0, bossRow: 1, portraitCols: 7, portraitRows: 4,
        dialogues: [
          { speaker: 'boss', name: '增长天王', text: '青锋剑出，风火相随！我镇南方增长善根，也斩尽犯天条的狂徒。孙悟空，止步！' },
          { speaker: 'wukong', name: '孙悟空', text: '好一把青锋剑！可俺也去手中这根棒子专破天门。你若不让，俺便连剑阵一起打穿！' }
        ]
      },
      26: {
        bossName: '西方广目天王·魔礼寿', bossTitle: '西天门·天龙索敌', bossPortrait: 'four_heavenly_kings', bossCol: 0, bossRow: 2, portraitCols: 7, portraitRows: 4,
        dialogues: [
          { speaker: 'boss', name: '广目天王', text: '吾观三界善恶，掌中天龙缠尽无礼之敌。你的变化瞒不过广目，退回花果山！' },
          { speaker: 'wukong', name: '孙悟空', text: '火眼金睛对广目，正好比比谁看得真。俺也去变作一粒微尘，你那天龙也未必抓得住！' }
        ]
      },
      27: {
        bossName: '北方多闻天王·魔礼红', bossTitle: '北天门·混元宝伞', bossPortrait: 'four_heavenly_kings', bossCol: 0, bossRow: 3, portraitCols: 7, portraitRows: 4,
        dialogues: [
          { speaker: 'boss', name: '多闻天王', text: '混元宝伞一开，遮天蔽日，尽收神兵法宝。你连破三门，也该在北天门伏法了！' },
          { speaker: 'wukong', name: '孙悟空', text: '你的伞能收法宝，俺也去这棒却能大过天门。看它撑不撑得住一万三千五百斤！' }
        ]
      },
      29: {
        bossName: '二郎显圣真君·杨戬', bossTitle: '凌霄云海·七十二变之争', bossPortrait: 'campaign_characters_act2', bossCol: 0, bossRow: 1, portraitCols: 7, portraitRows: 5,
        dialogues: [
          { speaker: 'boss', name: '二郎神', text: '孙悟空，我有天眼照破虚妄。你在昆仑所学几般变化，今日尽管使来。' },
          { speaker: 'wukong', name: '孙悟空', text: '杨戬，俺也去早想会你！变化不是躲藏，是临阵百用。看是你天眼快，还是俺老孙心念快！' }
        ]
      },
      32: {
        bossName: '如来佛祖', bossTitle: '凌霄之上·掌中佛国', bossPortrait: 'campaign_characters_act2', bossCol: 0, bossRow: 3, portraitCols: 7, portraitRows: 5,
        dialogues: [
          { speaker: 'boss', name: '如来佛祖', text: '悟空，天宫不是靠一根棍便能坐稳。你若能逼退我半身佛光，我便让你看见力量之外的天地。' },
          { speaker: 'wukong', name: '孙悟空', text: '俺也去自花果山一路打上来，从不信谁生来便该高坐云端。半身佛光也好，满天神佛也罢——看棒！' }
        ]
      },
      33: {
        bossName: '唐三藏', bossTitle: '五指山·取经人至', bossPortrait: 'campaign_characters_act2', bossCol: 0, bossRow: 4, portraitCols: 7, portraitRows: 5, isBattle: false,
        dialogues: [
          { speaker: 'boss', name: '唐三藏', text: '山下可是孙悟空？贫僧唐三藏，奉观音菩萨指点西行取经。你若愿护我一路，我便揭下金帖救你出来。' },
          { speaker: 'wukong', name: '孙悟空', text: '师父快揭！五百年俺也去想明白了：自由不只是不受管束，也能是自己答应守住的一条路。' },
          { speaker: 'boss', name: '唐三藏', text: '善哉。从今日起，你我师徒同行；前路尚有高老庄、流沙河与重重妖山。' }
        ]
      },
      36: {
        bossName: '猪八戒', bossTitle: '高老庄·天蓬旧将', bossPortrait: 'campaign_characters_act3', bossCol: 0, bossRow: 0, portraitCols: 7, portraitRows: 7,
        dialogues: [
          { speaker: 'boss', name: '猪八戒', text: '你这弼马温少管闲事！俺老猪虽错投猪胎，九齿钉耙照样能开山。' },
          { speaker: 'wukong', name: '孙悟空', text: '呆子，师父正缺个挑担的师弟。打赢俺也去让你走，打输了便收拾行李跟上！' }
        ]
      },
      40: {
        bossName: '沙悟净', bossTitle: '流沙河·卷帘旧将', bossPortrait: 'campaign_characters_act3', bossCol: 0, bossRow: 1, portraitCols: 7, portraitRows: 7,
        dialogues: [
          { speaker: 'boss', name: '沙悟净', text: '流沙河弱水三千，鹅毛也沉。你们若要西过，先胜我降妖宝杖。' },
          { speaker: 'wukong', name: '孙悟空', text: '老沙，俺也去看你不是滥杀之妖。过几招把旧怨打散，便与我们一同西行！' }
        ]
      },
      45: {
        bossName: '白骨夫人', bossTitle: '白虎岭·三重幻相', bossPortrait: 'campaign_characters_act3', bossCol: 0, bossRow: 2, portraitCols: 7, portraitRows: 7,
        dialogues: [
          { speaker: 'boss', name: '白骨精', text: '圣僧慈悲，怎会信一只杀气腾腾的猴子？我换三副皮囊，足以让你们师徒离心。' },
          { speaker: 'wukong', name: '孙悟空', text: '皮囊骗得过肉眼，骗不过火眼金睛。师父纵然怪俺也去，这一棒也必须替他打！' }
        ]
      },
      50: {
        bossName: '盘丝洞蜘蛛女王', bossTitle: '七情蛛网·万丝缚心', bossPortrait: 'campaign_characters_act3', bossCol: 0, bossRow: 3, portraitCols: 7, portraitRows: 7,
        dialogues: [
          { speaker: 'boss', name: '蜘蛛女王', text: '盘丝千万，缚的不是手脚，是你们师徒各自心中的贪嗔疑惧。' },
          { speaker: 'wukong', name: '孙悟空', text: '俺也去一棍扫得断蛛丝，师徒同心更不受你摆布。现出真身来！' }
        ]
      },
      55: {
        bossName: '牛魔王', bossTitle: '积雷山·平天大圣', bossPortrait: 'campaign_characters_act3', bossCol: 0, bossRow: 4, portraitCols: 7, portraitRows: 7,
        dialogues: [
          { speaker: 'boss', name: '牛魔王', text: '贤弟，你我昔日七大圣结义，今日却为取经来坏我家门！这声“大哥”，你还叫不叫？' },
          { speaker: 'wukong', name: '孙悟空', text: '情义俺也去记得，是非俺也去分得清。大哥若护着火焰山害人，俺只能先把你打醒！' }
        ]
      },
      60: {
        bossName: '圣婴大王·红孩儿', bossTitle: '火云洞·三昧真火', bossPortrait: 'campaign_characters_act3', bossCol: 0, bossRow: 5, portraitCols: 7, portraitRows: 7,
        dialogues: [
          { speaker: 'boss', name: '红孩儿', text: '孙悟空！我的三昧真火不是凡水能灭。你敢欺我父王，先尝尝五辆火车之阵！' },
          { speaker: 'wukong', name: '孙悟空', text: '小娃娃火气倒大。俺也去不怕烧，却要教你本领再强也不能拿无辜之人下锅！' }
        ]
      },
      65: {
        bossName: '铁扇公主', bossTitle: '翠云山·芭蕉洞', bossPortrait: 'campaign_characters_act3', bossCol: 0, bossRow: 6, portraitCols: 7, portraitRows: 7,
        dialogues: [
          { speaker: 'boss', name: '铁扇公主', text: '你伤我孩儿、战我夫君，还敢来借芭蕉扇？一扇八万四千里，叫你永回花果山！' },
          { speaker: 'wukong', name: '孙悟空', text: '俺也去借扇是为救火焰山百姓，不为你我私怨。若非要打，便打到这把火熄灭为止！' }
        ]
      }
    };

    const CAMPAIGN_DIALOGUES_EN = {
      5: { bossName: 'Elder Ape Chief', bossTitle: 'Trial of the Monkey Clan · Summit Duel', dialogues: [
        { speaker: 'boss', name: 'Elder Ape Chief', text: 'Stone Monkey, you have beaten every challenger, but strength alone does not make a king. At the summit, show me your courage and your heart.' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'I crossed the waterfall and climbed the cliffs without retreating. If I win, I will lead our people in search of true immortality!' }
      ] },
      6: { bossName: 'Yuanshi Tianzun', bossTitle: 'Kunlun Stairway · The Three Paths', dialogues: [
        { speaker: 'boss', name: 'Yuanshi Tianzun', text: 'Stone Monkey of awakened mind, did you cross the sea and climb Kunlun for immortality—or to defeat everyone beneath Heaven? I offer eighteen warrior forms, thirty-six celestial forms, and seventy-two earthly forms.' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'I want long life and freedom both. Explain the three paths, and I will choose the road I mean to finish.' },
        { speaker: 'boss', name: 'Yuanshi Tianzun', text: 'Eighteen favors offense, thirty-six balances attack and defense, and seventy-two offers endless variety. Choose, defeat my disciples, then face my final trial.' }
      ] },
      12: { bossName: 'Yuanshi Tianzun', bossTitle: 'Jade-Void Palace · Final Trial', dialogues: [
        { speaker: 'boss', name: 'Yuanshi Tianzun', text: 'All my disciples have fallen. Wukong, power without discipline wounds its owner first. Today I guard the final gate myself.' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'I will hear the lesson and learn the real art. Hold nothing back—let us see whether Kunlun magic can stop a staff from Flower-Fruit Mountain!' },
        { speaker: 'boss', name: 'Yuanshi Tianzun', text: 'Good. Win, and your chosen transformations truly begin. Then seek a weapon in the Eastern Sea that answers your will.' }
      ] },
      18: { bossName: 'Ao Guang, Dragon King of the Eastern Sea', bossTitle: 'Crystal Palace · Sea-Calming Treasure', dialogues: [
        { speaker: 'boss', name: 'Ao Guang', text: 'You defeated my guards and still call this borrowing? The sea-calming treasure weighs thirteen thousand five hundred jin and seals the ocean eye. I cannot simply give it away!' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'Your blades and spears are too light. That iron pillar shone when it saw me—it has been waiting for its master. I will defeat you before I take it.' },
        { speaker: 'boss', name: 'Ao Guang', text: 'Arrogant monkey! If the treasure truly accepts you, I will add a suit of armor. First survive the tides of the Eastern Sea!' }
      ] },
      19: { bossName: 'Ao Guang, Dragon King of the Eastern Sea', bossTitle: 'Dragon Treasury · The Staff Chooses', dialogues: [
        { speaker: 'boss', name: 'Ao Guang', text: 'The treasure has shrunk into a dark iron staff. Its golden bands name it the Ruyi Jingu Bang. It has chosen you, and I will honor my word.' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'Grow! Shrink! Truly obedient to my will. Thank you, old Dragon King. Now I will visit Heaven and ask why its gods believe they rule Flower-Fruit Mountain!' }
      ] },
      22: { bossName: 'Third Lotus Prince · Nezha', bossTitle: 'Southern Heavenly Gate · Wind-Fire Wheels', dialogues: [
        { speaker: 'boss', name: 'Nezha', text: 'Demon monkey, stop! You storm the Southern Gate and disturb the Celestial Court. First answer my Fire-Tip Spear and Universe Ring!' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'Little Nezha, you have three heads and six arms; I have a thousand transformations. I will not underestimate you—come!' }
      ] },
      24: { bossName: 'Eastern King Chiguo · Mo Lihai', bossTitle: 'Eastern Gate · Jade Pipa', dialogues: [
        { speaker: 'boss', name: 'King Chiguo', text: 'I preserve the realm with my jade pipa. One chord becomes a hundred thousand blades of celestial sound. The Eastern Gate is no playground, monkey!' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'I have heard celestial music, but never a lute used to frighten monkeys. Let us see whether your sound blades are faster than my staff!' }
      ] },
      25: { bossName: 'Southern King Zengzhang · Mo Liqing', bossTitle: 'Southern Gate · Divine Sword', dialogues: [
        { speaker: 'boss', name: 'King Zengzhang', text: 'When my divine sword leaves its sheath, wind and fire follow. I foster virtue in the south—and cut down those who defy celestial law. Stop!' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'A fine sword, but this staff was made to break heavenly gates. Stand aside, or I will smash the sword array too!' }
      ] },
      26: { bossName: 'Western King Guangmu · Mo Lishou', bossTitle: 'Western Gate · Celestial Dragon', dialogues: [
        { speaker: 'boss', name: 'King Guangmu', text: 'I watch good and evil throughout the Three Realms, and my dragon binds every lawless enemy. Your disguises cannot fool the All-Seeing King. Retreat!' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'Fiery Golden Eyes against the All-Seeing King—let us learn who sees more clearly. I can become a grain of dust your dragon may never catch!' }
      ] },
      27: { bossName: 'Northern King Duowen · Mo Lihong', bossTitle: 'Northern Gate · Sacred Umbrella', dialogues: [
        { speaker: 'boss', name: 'King Duowen', text: 'When the sacred umbrella opens, it covers Heaven and gathers every divine weapon. You broke three gates; at the Northern Gate you finally submit!' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'Your umbrella may collect treasures, but my staff can grow larger than the gate. Let us see whether it can hold thirteen thousand five hundred jin!' }
      ] },
      29: { bossName: 'Erlang, Illustrious Sage · Yang Jian', bossTitle: 'Celestial Cloud-Sea · Contest of Transformations', dialogues: [
        { speaker: 'boss', name: 'Erlang Shen', text: 'Sun Wukong, my third eye pierces every illusion. Show me every transformation you learned at Kunlun.' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'Yang Jian, I have wanted this duel! Transformation is not hiding—it is a hundred answers in battle. Is your eye faster than my thought?' }
      ] },
      32: { bossName: 'Tathagata Buddha', bossTitle: 'Above the Celestial Court · Buddha’s Palm', dialogues: [
        { speaker: 'boss', name: 'Tathagata Buddha', text: 'Wukong, a throne in Heaven cannot be secured by one staff. Drive back half my radiance, and I will show you a world beyond raw strength.' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'I fought here from Flower-Fruit Mountain because I reject the claim that some are born above the clouds. Half your radiance or all the gods of Heaven—take my staff!' }
      ] },
      33: { bossName: 'Tang Sanzang', bossTitle: 'Five-Finger Mountain · The Pilgrim Arrives', dialogues: [
        { speaker: 'boss', name: 'Tang Sanzang', text: 'Are you Sun Wukong beneath this mountain? I am Tang Sanzang, sent west for the scriptures under Guanyin’s guidance. If you will protect me, I will remove the golden seal.' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'Master, remove it quickly! In five hundred years I learned that freedom is not only refusing chains; it can also be a road one freely vows to protect.' },
        { speaker: 'boss', name: 'Tang Sanzang', text: 'Excellent. From today we travel as master and disciple. Gao Village, Flowing-Sands River, and many demon mountains lie ahead.' }
      ] },
      36: { bossName: 'Zhu Bajie', bossTitle: 'Gao Village · Former Marshal Tianpeng', dialogues: [
        { speaker: 'boss', name: 'Zhu Bajie', text: 'Mind your own business, stable boy! I may have fallen into a pig’s body, but my nine-tooth rake can still split mountains.' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'Idiot, Master needs a junior disciple to carry the luggage. Beat me and leave; lose, and pack your things!' }
      ] },
      40: { bossName: 'Sha Wujing', bossTitle: 'Flowing-Sands River · Former Curtain General', dialogues: [
        { speaker: 'boss', name: 'Sha Wujing', text: 'Three thousand spans of weak water sink even a feather. To cross west, first defeat my demon-subduing staff.' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'Old Sha, you are no mindless killer. Let a few exchanges wash away old grudges, then journey west with us!' }
      ] },
      45: { bossName: 'Lady White Bone', bossTitle: 'White-Bone Ridge · Three Disguises', dialogues: [
        { speaker: 'boss', name: 'White Bone Spirit', text: 'How could the merciful monk trust a murderous monkey? Three borrowed faces are enough to divide master and disciple.' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'Skin may deceive mortal eyes, but not my Fiery Golden Eyes. Even if Master blames me, I must strike to protect him!' }
      ] },
      50: { bossName: 'Spider Queen', bossTitle: 'Webbed Hollow · Prison of Desire', dialogues: [
        { speaker: 'boss', name: 'Spider Queen', text: 'A thousand webs bind more than hands and feet. They bind the greed, anger, doubt, and fear inside each pilgrim.' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'My staff cuts webs, and a united fellowship is beyond your control. Show your true form!' }
      ] },
      55: { bossName: 'Bull Demon King', bossTitle: 'Mount Thunder · Great Sage Who Pacifies Heaven', dialogues: [
        { speaker: 'boss', name: 'Bull Demon King', text: 'Brother, we once swore fellowship as the Seven Great Sages. Now your pilgrimage brings ruin to my family. Will you still call me elder brother?' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'I remember our brotherhood, and I still know right from wrong. If you protect those who harm the people of Flaming Mountain, I must knock sense into you!' }
      ] },
      60: { bossName: 'Red Boy · Great King Holy Infant', bossTitle: 'Fire-Cloud Cave · Samadhi Fire', dialogues: [
        { speaker: 'boss', name: 'Red Boy', text: 'Sun Wukong! Ordinary water cannot extinguish my Samadhi Fire. You insulted my father—now face the Five Fire-Cart Array!' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'Such a temper for a child. I can endure the flames, but I will teach you that power never excuses cooking innocent people!' }
      ] },
      65: { bossName: 'Princess Iron Fan', bossTitle: 'Emerald-Cloud Mountain · Plantain Cave', dialogues: [
        { speaker: 'boss', name: 'Princess Iron Fan', text: 'You injured my son, fought my husband, and still dare ask for my fan? One stroke will send you eighty-four thousand li back to Flower-Fruit Mountain!' },
        { speaker: 'wukong', name: 'Sun Wukong', text: 'I borrow the fan to save the people of Flaming Mountain, not for our private feud. If we must fight, we fight until these flames are extinguished!' }
      ] }
    };

    const LATE_DIALOGUE_SCENES = {
      67: { asset: 'campaign_characters_act4', row: 0, rows: 6, nameZh: '九头虫', nameEn: 'Nine-Headed Beast', titleZh: '碧波潭·佛宝之争', titleEn: 'Emerald-Wave Pool · Battle for the Relic', zh: [['boss','九头虫','舍利玲珑内丹光，龙宫驸马正该享用。你这泼猴敢闯碧波潭，九颗头便各咬你一口！'],['wukong','孙悟空','佛宝照的是清净心，不是你偷来的威风。二郎兄已断你后路，俺也去打落你九颗狂头！']], en: [['boss','Nine-Headed Beast','The relic’s radiance belongs in my dragon court. Break into Emerald-Wave Pool, monkey, and all nine heads will answer!'],['wukong','Sun Wukong','A sacred light reveals a clean heart, not a thief’s pride. Erlang has closed your escape; my staff will settle the rest!']] },
      68: { asset: 'campaign_characters_act4', row: 1, rows: 6, nameZh: '荆棘岭木仙', nameEn: 'Tree Immortals of Thorn Ridge', titleZh: '木仙庵·诗心与慈悲', titleEn: 'Tree-Immortal Abbey · Poetry and Mercy', isBattle: false, zh: [['boss','十八公','圣僧，草木亦知风月。何必只谈西行，不肯为杏仙留一首诗？'],['wukong','孙悟空','会吟诗不等于没有算计。俺老孙今日救师，也记住这一路并非每个妖都只配一棒。'],['boss','唐三藏','悟空，守戒也需明辨慈悲。我们谢过诗会，仍须继续西行。']], en: [['boss','Elder Eighteen','Holy monk, even trees know moonlight and verse. Must every thought face west, with none left for Apricot Immortal’s poem?'],['wukong','Sun Wukong','Poetry does not erase a hidden snare. I will rescue Master—but I will remember that not every spirit deserves the same answer.'],['boss','Tang Sanzang','Discernment and compassion must travel together. We thank you for the poems, but our road continues west.']] },
      70: { asset: 'campaign_characters_act4', row: 2, rows: 6, nameZh: '黄眉大王', nameEn: 'Yellow Brows Great King', titleZh: '小雷音·伪佛金殿', titleEn: 'Little Thunderclap · The False Buddha', zh: [['boss','黄眉大王','你们心里早把雷音寺想成了终点，所以一见金身便跪。俺也去佛祖，金铙与人种袋就是俺也去法！'],['wukong','孙悟空','真佛不靠门匾骗人。弥勒老爷的瓜你既然敢吞，俺老孙便从你肚里拆了这座假雷音！']], en: [['boss','Yellow Brows','You wanted Thunderclap to be the end so badly that you knelt before the first golden hall. I am your Buddha now—the cymbals and sack are my law!'],['wukong','Sun Wukong','A true Buddha needs no false signboard. Since you swallowed Maitreya’s melon, I will tear this counterfeit paradise apart from inside you!']] },
      71: { asset: 'campaign_characters_act4', row: 3, rows: 6, nameZh: '红鳞大蟒精', nameEn: 'Great Red-Scaled Python', titleZh: '七绝山·盘山绞杀', titleEn: 'Qijue Mountain · Coils Across the Pass', zh: [['boss','红鳞大蟒精','七绝山污秽千年，正好埋你师徒四人。俺也去身躯一盘，前后皆是死路！'],['wukong','孙悟空','长不等于强。八戒守尾，俺也去锁头，今日把你这条臭蛇清出山道！']], en: [['boss','Great Python','Qijue Mountain has buried travelers for a thousand years. One turn of my coils closes every road!'],['wukong','Sun Wukong','Long is not the same as strong. Bajie takes the tail; I take the head. We clear this pass today!']] },
      75: { asset: 'campaign_characters_act4', row: 4, rows: 6, nameZh: '赛太岁', nameEn: 'Sai Tai Sui', titleZh: '麒麟山·紫金三铃', titleEn: 'Qilin Mountain · Three Purple-Gold Bells', zh: [['boss','赛太岁','一铃放火，一铃喷烟，一铃飞沙。你盗走假铃又如何，三灾齐发便叫朱紫国永无王后！'],['wukong','孙悟空','铃铛本是观音坐骑颈上之物，俺也去用假铃骗的是你的贪心。真主人已经到山门了！']], en: [['boss','Sai Tai Sui','One bell brings fire, one smoke, one sand. Your false bells change nothing—the queen of Zhuzi will never return!'],['wukong','Sun Wukong','Those bells belong on Guanyin’s mount. My counterfeits fooled only your greed—and their true owner has reached the gate!']] },
      77: { asset: 'campaign_characters_act4', row: 5, rows: 6, nameZh: '百眼魔君', nameEn: 'Hundred-Eyed Demon', titleZh: '黄花观·千眼毒日', titleEn: 'Yellow-Flower Temple · Poison Sun of a Hundred Eyes', zh: [['boss','百眼魔君','你毁我师妹盘丝洞，今日百目齐开，金光如日，毒气如海！'],['wukong','孙悟空','蜘蛛债俺也去认，吃人的毒阵俺也去更要破。昴日星官之母的绣花针，正照你这百只邪眼！']], en: [['boss','Hundred-Eyed Demon','You destroyed my sisters of Webbed Hollow. Now a hundred eyes become a poisonous sun!'],['wukong','Sun Wukong','I answer for every blow I struck—but I will still break a man-eating array. Pilanpo’s Dawn Needle points at every one of your wicked eyes!']] },
      79: { asset: 'campaign_characters_act5', row: 0, rows: 6, nameZh: '青狮大王', nameEn: 'Azure Lion King', titleZh: '狮驼洞·吞天巨口', titleEn: 'Lion-Camel Cave · Heaven-Swallowing Maw', zh: [['boss','青狮大王','俺也去一口吞十万天兵，吞你一只猴子不过塞牙！'],['wukong','孙悟空','好大的口气。你敢吞，俺也去就在你肚里架锅、点火、舞一万三千五百斤！']], en: [['boss','Azure Lion','I once swallowed a hundred thousand celestial soldiers. One monkey will not fill a tooth!'],['wukong','Sun Wukong','Then swallow me. I will light a fire, set up a kitchen, and swing thirteen thousand five hundred jin inside your belly!']] },
      80: { asset: 'campaign_characters_act5', row: 1, rows: 6, nameZh: '黄牙老象', nameEn: 'Yellow-Tusk White Elephant', titleZh: '狮驼国·象鼻锁魂', titleEn: 'Lion-Camel Kingdom · Binding Trunk', zh: [['boss','黄牙老象','青狮逞口，你却过不了俺也去象鼻。缠住元神，再以黄牙挑碎金箍棒！'],['wukong','孙悟空','鼻子再长也怕打结。俺也去借你冲势撞山，看第二关是谁先倒！']], en: [['boss','White Elephant','The lion relied on his mouth. My trunk binds the spirit itself, and these tusks will splinter your staff!'],['wukong','Sun Wukong','Even the longest trunk can be tied in a knot. Charge, and I will turn your weight against the mountain!']] },
      81: { asset: 'campaign_characters_act5', row: 2, rows: 6, nameZh: '金翅大鹏雕', nameEn: 'Golden-Winged Great Peng', titleZh: '金翅绝空·九万里', titleEn: 'Golden Wings Seal the Sky', zh: [['boss','金翅大鹏雕','俺也去一振翅九万里，你筋斗云不过十万八千里。天空是俺也去牢笼，灵山也须认俺也去亲缘！'],['wukong','孙悟空','快不等于逃得掉。俺也去救出师父，再请如来当面说清你这门亲戚！']], en: [['boss','Golden-Winged Great Peng','One beat of my wings crosses ninety thousand li. The sky is my prison, and even Vulture Peak acknowledges my blood!'],['wukong','Sun Wukong','Speed is not escape. I free my master first—then Buddha can explain this troublesome relative himself!']] },
      84: { asset: 'campaign_characters_act5', row: 3, rows: 6, nameZh: '白鹿国丈', nameEn: 'White Deer Preceptor', titleZh: '比丘国·千童悬命', titleEn: 'Bhikkhu Kingdom · A Thousand Children', zh: [['boss','白鹿国丈','千名童子的心肝换国王长生，岂不胜过凡人百年？莫坏俺也去仙方！'],['wukong','孙悟空','拿孩子炼寿算什么仙方！寿星老儿已来认鹿，俺也去先替千家父母打醒你！']], en: [['boss','White Deer','A thousand children’s hearts can buy a king centuries of life. Do not interfere with an immortal prescription!'],['wukong','Sun Wukong','A recipe built from children is no immortality. Your old master has come for his deer; first I strike for every family you terrified!']] },
      86: { asset: 'campaign_characters_act2', row: 4, rows: 5, nameZh: '唐三藏', nameEn: 'Tang Sanzang', titleZh: '灭法国·一夜剃城', titleEn: 'Monk-Destroying Kingdom · A City Shaved by Dawn', isBattle: false, zh: [['boss','唐三藏','悟空，此国王立誓杀尽万僧，硬闯恐令百姓受难。'],['wukong','孙悟空','师父放心。不流一滴血，俺也去叫满朝文武明早都顶着和尚头上朝！']], en: [['boss','Tang Sanzang','Wukong, this king has vowed to kill ten thousand monks. A violent entry would endanger the people.'],['wukong','Sun Wukong','Leave it to me, Master. Without spilling blood, the whole court will wake with a monk’s haircut!']] },
      87: { asset: 'campaign_characters_act5', row: 4, rows: 6, nameZh: '金鼻白毛老鼠精', nameEn: 'Golden-Nosed White Mouse', titleZh: '无底洞·花烛迷局', titleEn: 'Bottomless Cave · Bridal Snare', zh: [['boss','老鼠精','圣僧已入洞房，你见到的每个俺也去都可能是真身。哪吒义兄也未必找得到俺也去！'],['wukong','孙悟空','供桌上的牌位已经报了你家门。真假身躯怕火眼，托塔天王父子也该下界管管义女！']], en: [['boss','White Mouse','The holy monk is already in my bridal chamber. Every body you see may be the true one—even my sworn brother Nezha may not find me!'],['wukong','Sun Wukong','Your ancestral tablets gave away the family name. False bodies fear Fiery Golden Eyes, and Li Jing’s household must answer for its adopted daughter!']] },
      90: { asset: 'campaign_characters_act5', row: 5, rows: 6, nameZh: '南山大王', nameEn: 'Southern Mountain King', titleZh: '隐雾山·假首疑云', titleEn: 'Hidden-Mist Mountain · The False Head', zh: [['boss','南山大王','你两个师弟已见唐僧人头，信念早碎。雾中百豹皆是俺也去，也皆不是俺也去！'],['wukong','孙悟空','假的头骗得了眼泪，骗不了俺也去火眼金睛。师父还活着，你这豹子才要没命！']], en: [['boss','Southern Mountain King','Your brothers saw Tang’s severed head and lost hope. Every leopard in this fog is me—and none of them are!'],['wukong','Sun Wukong','A false head can draw real tears, but it cannot fool Fiery Golden Eyes. Master lives; your deception ends here!']] },
      93: { asset: 'campaign_characters_act6', row: 0, rows: 7, nameZh: '黄狮精', nameEn: 'Yellow Lion Spirit', titleZh: '豹头山·钉耙盛会', titleEn: 'Leopard-Head Mountain · Feast of Stolen Weapons', zh: [['boss','黄狮精','金箍棒、九齿耙、降妖杖都在俺也去席上。没了兵器，你们拿什么做师父？'],['wukong','孙悟空','兵器能偷，本事偷不走。俺也去先空手夺回三件神兵，再与你堂堂正正一战！']], en: [['boss','Yellow Lion','Staff, rake, and demon-subduing rod decorate my feast. Without weapons, what kind of masters are you?'],['wukong','Sun Wukong','You can steal weapons, not skill. I recover all three bare-handed—then we settle this honorably!']] },
      94: { asset: 'campaign_characters_act6', row: 1, rows: 7, nameZh: '九灵元圣', nameEn: 'Nine-Spirit Primordial Sage', titleZh: '竹节山·九口归元', titleEn: 'Bamboo-Joint Mountain · Nine Mouths Return to One', zh: [['boss','九灵元圣','黄狮是俺也去徒孙。你辱俺也去一脉，九口同开便将你师徒一并擒来！'],['wukong','孙悟空','护短也要讲理。九颗狮头正好九处破绽，太乙救苦天尊也在找他走失的坐骑！']], en: [['boss','Nine-Spirit Sage','Yellow Lion is my descendant. Insult my line, and nine mouths will seize your entire fellowship!'],['wukong','Sun Wukong','Family loyalty does not excuse wrongdoing. Nine heads mean nine openings—and Taiyi Jiuku Tianzun is looking for a missing mount!']] },
      96: { asset: 'campaign_characters_act6', row: 2, rows: 7, nameZh: '辟寒·辟暑·辟尘三大王', nameEn: 'The Three Rhino Kings', titleZh: '青龙山·寒暑尘连环阵', titleEn: 'Azure-Dragon Mountain · Frost, Heat, and Dust', zh: [['boss','三犀大王','俺也去三兄弟受香油千年，寒封脚、暑焚身、尘蔽眼，三角相连便是无破佛阵！'],['wukong','孙悟空','假佛吃油也敢称阵。八戒、沙僧各牵一角，俺也去逐个敲断你们的犀牛角！']], en: [['boss','Three Rhino Kings','For a thousand years we consumed the city’s sacred oil. Frost binds feet, heat burns flesh, dust blinds eyes—three horns form an unbreakable Buddha array!'],['wukong','Sun Wukong','False Buddhas stealing lamp oil call that holiness? Bajie and Wujing split the formation; I break the horns one by one!']] },
      99: { asset: 'campaign_characters_act6', row: 5, rows: 7, nameZh: '玉兔精', nameEn: 'Jade Rabbit Spirit', titleZh: '天竺国·满月玉杵', titleEn: 'Tianzhu Kingdom · Full-Moon Jade Pestle', zh: [['boss','玉兔精','素娥昔日打俺也去一掌，今日俺也去借公主之身配唐僧，正是月宫因果！'],['wukong','孙悟空','因果不是拿凡人姻缘出气。太阴星君已到，俺也去先用金箍棒会会你这捣药玉杵！']], en: [['boss','Jade Rabbit','The immortal maiden struck me long ago. Taking the princess’s place and marrying Tang repays a Moon-Palace debt!'],['wukong','Sun Wukong','Karma is no excuse to steal a mortal life. The Lunar Goddess is here—first let my staff answer your jade pestle!']] },
      100: { asset: 'campaign_characters_act2', row: 3, rows: 5, nameZh: '如来佛祖', nameEn: 'Tathagata Buddha', titleZh: '大雷音寺·五圣成真', titleEn: 'Thunderclap Monastery · Five Saints Attain Truth', isBattle: false, onComplete: 'journeyVictory', zh: [['boss','如来佛祖','九九八十一难已满，真经当传东土。悟空，你今日所胜不只诸魔，更是昔日只知逞强之心。'],['wukong','孙悟空','俺也去一路打过来，也一路学会何时不打。师父真经已归，头上这金箍怎么也不见了？'],['boss','如来佛祖','心猿归正，金箍自落。今封你为斗战胜佛，与三藏、悟能、悟净、白龙同证真果。']], en: [['boss','Tathagata Buddha','The eighty-one ordeals are fulfilled and the scriptures shall reach the East. Wukong, you conquered more than demons—you conquered the heart that knew only force.'],['wukong','Sun Wukong','I fought across the whole road, and learned when not to fight. The scriptures have returned—yet where did my golden headband go?'],['boss','Tathagata Buddha','When the mind-monkey returns to truth, the band falls by itself. You are now the Victorious Fighting Buddha, attaining the fruit beside your fellowship.']] }
    };

    // The late pilgrimage advances through a real scene at every chapter rather than
    // jumping from boss card to boss card. These quieter exchanges pause combat,
    // establish the next mystery, and then return control for the normal wave.
    const LATE_INTERMEDIATE_DIALOGUE_SCENES = {
      66: { asset:'campaign_characters_act2', row:4, rows:5, nameZh:'唐三藏', nameEn:'Tang Sanzang', titleZh:'祭赛国·金光塔冤案', titleEn:'Jisai Kingdom · The Pagoda Accusation', isBattle:false, zh:[['boss','唐三藏','金光寺僧众因佛宝失窃受尽刑罚。悟空，先救人，再查那场从碧波潭方向落下的血雨。'],['wukong','孙悟空','师父放心。俺也去一层层扫塔，妖气、血迹、脚印总有一样会把贼带到俺面前。']], en:[['boss','Tang Sanzang','The Golden-Ray monks are tortured for a relic they did not steal. Save them first, then follow the blood rain from Emerald-Wave Pool.'],['wukong','Sun Wukong','I will clear the tower floor by floor. Demon scent, blood, or footprints—one trail will lead the thief to my staff.']] },
      69: { asset:'campaign_characters_act4', row:2, rows:6, nameZh:'弥勒童子', nameEn:'Maitreya Acolyte', titleZh:'小雷音寺·真假佛门', titleEn:'Little Thunderclap · A False Sanctuary', isBattle:false, zh:[['boss','弥勒童子','前方雷音寺钟声来得太早，金铙与人种袋皆是弥勒宝物。切莫因盼终点便失了戒心。'],['wukong','孙悟空','俺也去正嫌门匾金得刺眼。真佛不拿师父当诱饵，先拆穿假礼，再找宝物主人。']], en:[['boss','Maitreya Acolyte','Thunderclap bells ring far too early. The golden cymbals and Human Seed Bag belong to Maitreya—do not let hope of the finish dull your caution.'],['wukong','Sun Wukong','That gilded sign already hurts my eyes. A true Buddha would not bait a trap with Master. I expose the fraud first.']] },
      72: { asset:'campaign_characters_act2', row:4, rows:5, nameZh:'朱紫国王', nameEn:'King of Zhuzi', titleZh:'朱紫国·悬丝诊脉', titleEn:'Zhuzi Kingdom · Diagnosis by Thread', isBattle:false, zh:[['boss','朱紫国王','御医皆说寡人无药可救，胸中却总像压着一只金铃。'],['wukong','孙悟空','这不是绝症，是多年惊惧结成的心病。俺也去先配乌金丹，再问那位失踪娘娘。']], en:[['boss','King of Zhuzi','Every physician says I cannot be cured, yet my chest feels burdened by a golden bell.'],['wukong','Sun Wukong','This is grief hardened into illness. I will prepare the Wujin Elixir—then you will tell me of the missing queen.']] },
      73: { asset:'campaign_characters_act2', row:4, rows:5, nameZh:'金圣宫娘娘', nameEn:'Queen of the Golden Palace', titleZh:'朱紫国·旧事重开', titleEn:'Zhuzi Kingdom · The Queen Taken', isBattle:false, zh:[['boss','金圣宫娘娘','赛太岁披霞光而来，以紫金铃放火烟黄沙，将我掳到麒麟山。'],['wukong','孙悟空','铃有三枚，招数也有三层。俺也去变个心腹进去，把真铃换成假铃。']], en:[['boss','Queen of the Golden Palace','Sai Tai Sui came in radiant armor. Three Purple-Gold Bells cast fire, smoke, and sand before he carried me to Qilin Mountain.'],['wukong','Sun Wukong','Three bells mean three openings. I will enter as a trusted servant and trade the true bells for false ones.']] },
      74: { asset:'campaign_characters_act4', row:4, rows:6, nameZh:'小钻风', nameEn:'Little Wind Cutter', titleZh:'麒麟山·盗铃之计', titleEn:'Qilin Mountain · The Bell Ruse', isBattle:false, zh:[['boss','小钻风','大王饮酒时也把紫金铃贴身藏着，陌生小妖连洞门都进不得。'],['wukong','孙悟空','那俺也去就不做陌生小妖。借你令牌、口令与模样一用，天亮前原样奉还。']], en:[['boss','Little Wind Cutter','The king keeps the Purple-Gold Bells against his body even while drinking. No unknown demon passes the gate.'],['wukong','Sun Wukong','Then I will not be unknown. Lend me your token, password, and face; I return all three by dawn.']] },
      76: { asset:'campaign_characters_act5', row:0, rows:6, nameZh:'太白金星', nameEn:'Evening Star', titleZh:'狮驼岭·万妖之国', titleEn:'Lion-Camel Ridge · Kingdom of Demons', isBattle:false, zh:[['boss','太白金星','狮驼岭不是一洞散妖。青狮、白象、大鹏统领四万七千妖兵，城中凡人已绝。'],['wukong','孙悟空','硬闯只会让师父再被搬一次。俺也去先做巡山小钻风，把三位大王的规矩都摸清。']], en:[['boss','Evening Star','Lion-Camel Ridge is no scattered den. Lion, Elephant, and Peng command forty-seven thousand demons; no mortal remains in the city.'],['wukong','Sun Wukong','A frontal charge only gets Master moved again. I will scout as Little Wind Cutter and learn the three kings’ rules.']] },
      78: { asset:'campaign_characters_act2', row:4, rows:5, nameZh:'狮驼国逃民', nameEn:'Lion-Camel Refugee', titleZh:'狮驼国·城中无炊烟', titleEn:'Lion-Camel City · No Mortal Hearth', isBattle:false, zh:[['boss','狮驼国逃民','三魔把活人分囚各洞，大鹏每日巡天，连飞鸟也逃不过金光。'],['wukong','孙悟空','俺也去去引开天空那双眼。八戒、沙僧趁机开牢，师父一步也别离开白龙马。']], en:[['boss','Lion-Camel Refugee','The three kings divide captives among their caves. Great Peng patrols the sky; even birds cannot escape his golden sight.'],['wukong','Sun Wukong','I draw those eyes away. Bajie and Wujing open the cells, and Master stays beside the dragon-horse.']] },
      82: { asset:'campaign_characters_act2', row:4, rows:5, nameZh:'唐三藏', nameEn:'Tang Sanzang', titleZh:'狮驼国·释放囚民', titleEn:'Lion-Camel City · The Gates Reopen', isBattle:false, zh:[['boss','唐三藏','三位魔王虽败，满城囚民仍惧怕踏出牢门。胜负之后，救人才算完成。'],['wukong','孙悟空','俺也去与八戒清路，老沙分水粮。等最后一家点起炊烟，我们再往西走。']], en:[['boss','Tang Sanzang','The three kings are defeated, yet the captives still fear leaving their cells. Victory is unfinished until people are safe.'],['wukong','Sun Wukong','Bajie and I clear the roads; Wujing shares food and water. We leave only when the first hearth burns again.']] },
      83: { asset:'campaign_characters_act2', row:4, rows:5, nameZh:'比丘国母亲', nameEn:'A Bhikkhu Mother', titleZh:'比丘国·千童悬命', titleEn:'Bhikkhu Kingdom · Children in Cages', isBattle:false, zh:[['boss','比丘国母亲','国丈说一千零一个童心能换国王长生，孩子们今夜就要被送入宫。'],['wukong','孙悟空','俺也去变作最后一颗童心送进去。等妖道开药炉，正好让满朝看清长生方的真面目。']], en:[['boss','A Bhikkhu Mother','The royal preceptor claims one thousand and one children’s hearts will prolong the king’s life. They are taken tonight.'],['wukong','Sun Wukong','I become the final heart and enter the furnace myself. When he begins, the whole court will see the true price of his immortality.']] },
      85: { asset:'campaign_characters_act5', row:4, rows:6, nameZh:'黑松林女子', nameEn:'Woman of Black-Pine Forest', titleZh:'黑松林·雪上异踪', titleEn:'Black-Pine Forest · Tracks in Snow', isBattle:false, zh:[['boss','黑松林女子','多谢长老救命。雪深路险，让小女子随你们到前村吧。'],['wukong','孙悟空','人脚不会忽然变成鼠爪，也不会在背风处没有影子。师父可救她，但俺也去一路盯着。']], en:[['boss','Woman of Black-Pine Forest','Thank you for rescuing me, holy master. The snow is deep; please let me travel to the next village.'],['wukong','Sun Wukong','Human footprints do not become mouse claws, and people cast shadows out of the wind. Master may help her; I will watch every step.']] },
      88: { asset:'campaign_characters_act2', row:0, rows:5, nameZh:'哪吒', nameEn:'Nezha', titleZh:'无底洞·牌位为证', titleEn:'Bottomless Cave · The Ancestral Tablets', isBattle:false, zh:[['boss','哪吒','那妖在洞中供奉父王与俺也去为义父义兄。此事若真，天庭不能推诿。'],['wukong','孙悟空','牌位俺也去拓下来了。你们封住地洞出口，俺去也最深处把师父和真身一起逼出来。']], en:[['boss','Nezha','The spirit keeps tablets naming my father and me as sworn kin. If true, Heaven cannot ignore this.'],['wukong','Sun Wukong','I copied the tablets. Seal every burrow exit while I drive both the true body and my master up from the deepest chamber.']] },
      89: { asset:'campaign_characters_act2', row:4, rows:5, nameZh:'灭法国王', nameEn:'King of the Monk-Destroying Realm', titleZh:'灭法国·一夜剃城', titleEn:'Monk-Destroying Kingdom · Shaved by Dawn', isBattle:false, zh:[['boss','灭法国王','满朝一夜皆成光头，寡人才知誓杀万僧不过是迁怒与狂妄。请圣僧赐教。'],['wukong','孙悟空','肯改就不必挨棒。把刀换成度牒，把杀僧榜换成护行榜，俺也去当这场只是个笑话。']], en:[['boss','King of the Monk-Destroying Realm','My whole court woke shaved. I see that my vow against ten thousand monks was anger and vanity. Teach me another road.'],['wukong','Sun Wukong','If you change, no staff is needed. Replace execution warrants with travel papers, and we leave this as a joke rather than a tragedy.']] },
      91: { asset:'campaign_characters_act2', row:4, rows:5, nameZh:'凤仙郡侯', nameEn:'Lord of Fengxian', titleZh:'凤仙郡·求雨不靠棍', titleEn:'Fengxian · Rain Cannot Be Beaten Down', isBattle:false, zh:[['boss','凤仙郡侯','三年无雨，河井俱空。大圣能降妖，可否也一棒打碎天上旱锁？'],['wukong','孙悟空','这回棒子无用。你先为昔日冒犯悔过，开仓行善；俺也去上天把米山、面山与锁链的缘由问明。']], en:[['boss','Lord of Fengxian','Three years without rain have emptied every well. Great Sage, can your staff break the drought’s lock in Heaven?'],['wukong','Sun Wukong','A staff is useless here. Repent, open the granaries, and serve the people while I learn why Heaven set its impossible conditions.']] },
      92: { asset:'campaign_characters_act6', row:0, rows:7, nameZh:'玉华州三王子', nameEn:'Three Princes of Yuhua', titleZh:'玉华州·从弟子到师父', titleEn:'Yuhua Kingdom · Pupils Become Masters', isBattle:false, zh:[['boss','玉华州三王子','愿拜三位高徒为师，学习金箍棒、九齿耙与降妖杖，不为炫技，只为护国。'],['wukong','孙悟空','学兵器先学收兵器。俺去也传棍法，八戒、老沙各收一徒；今晚先练站桩。']], en:[['boss','Three Princes of Yuhua','We ask to learn staff, rake, and demon-subduing rod—not for display, but to protect our people.'],['wukong','Sun Wukong','Before learning to swing a weapon, learn when to lower it. Each of us takes one pupil; tonight begins with stance and patience.']] },
      95: { asset:'campaign_characters_act6', row:2, rows:7, nameZh:'金平府灯官', nameEn:'Jinping Lantern Keeper', titleZh:'金平府·假佛吃油', titleEn:'Jinping Prefecture · False Buddhas at the Lamps', isBattle:false, zh:[['boss','金平府灯官','每年三位佛爷降临，收尽酥合香油；今年却连圣僧也随灯火消失。'],['wukong','孙悟空','真佛不偷油，更不偷师父。三股足印各带寒霜、焦土与沙尘，是三头犀牛。']], en:[['boss','Jinping Lantern Keeper','Three Buddhas descend yearly to consume every lamp of fragrant oil. This year the holy monk vanished with them.'],['wukong','Sun Wukong','True Buddhas steal neither oil nor Master. Three tracks carry frost, scorched earth, and dust—the thieves are three rhinoceros spirits.']] },
      97: { asset:'campaign_characters_act6', row:5, rows:7, nameZh:'天竺假公主', nameEn:'False Princess of Tianzhu', titleZh:'天竺国·绣球选亲', titleEn:'Tianzhu · The Embroidered Ball', isBattle:false, zh:[['boss','天竺假公主','绣球既落在圣僧身上，便是月老定缘。谁也不得带他出宫。'],['wukong','孙悟空','俺也去闻到的是月宫药杵的寒气，不是红线。婚礼照办，俺去也查查真正公主去了哪里。']], en:[['boss','False Princess of Tianzhu','The embroidered ball chose the holy monk. The match is written by fate, and none may take him from the palace.'],['wukong','Sun Wukong','I smell Moon-Palace medicine, not a red thread of fate. Continue the wedding preparations while I find the true princess.']] },
      98: { asset:'campaign_characters_act6', row:5, rows:7, nameZh:'天竺真公主', nameEn:'True Princess of Tianzhu', titleZh:'布金寺·月镜照身', titleEn:'Bujin Temple · The Moon Mirror', isBattle:false, zh:[['boss','天竺真公主','我被妖风卷出宫门，流落寺中一年。每逢满月，便梦见白兔占了俺也去寝殿。'],['wukong','孙悟空','梦与月气都对上了。俺也去借四面月镜照遍宫门，假身再多也躲不过自己的影子。']], en:[['boss','True Princess of Tianzhu','A demon wind cast me from the palace a year ago. Every full moon I dream of a white rabbit in my chamber.'],['wukong','Sun Wukong','Dream and lunar scent agree. I will set moon mirrors at every gate; no borrowed body can hide from its own shadow.']] }
    };

    Object.entries({ ...LATE_DIALOGUE_SCENES, ...LATE_INTERMEDIATE_DIALOGUE_SCENES }).forEach(([chapterKey, scene]) => {
      const chapter = Number(chapterKey);
      CAMPAIGN_DIALOGUES[chapter] = {
        bossName: scene.nameZh,
        bossTitle: scene.titleZh,
        bossPortrait: scene.asset,
        bossCol: 0,
        bossRow: scene.row,
        portraitCols: 7,
        portraitRows: scene.rows,
        isBattle: scene.isBattle,
        onComplete: scene.onComplete,
        dialogues: scene.zh.map(([speaker, name, text]) => ({ speaker, name, text }))
      };
      CAMPAIGN_DIALOGUES_EN[chapter] = {
        bossName: scene.nameEn,
        bossTitle: scene.titleEn,
        dialogues: scene.en.map(([speaker, name, text]) => ({ speaker, name, text }))
      };
    });

    function getLocalizedBossDialogue(chamberIndex) {
      if (gameState.campaignRoute === 'fengshen') return getErlangCampaignDialogue(chamberIndex);
      const source = CAMPAIGN_DIALOGUES[chamberIndex] || BOSS_DIALOGUES[chamberIndex];
      if (!source || gameState.language !== 'en') return source;
      const english = CAMPAIGN_DIALOGUES_EN[chamberIndex];
      return english ? { ...source, ...english } : source;
    }

    const CUTSCENE_ARCS = [
      { through: 5, asset: 'cutscene_flower_fruit', zh: '花果山 · 石猴称王', en: 'Flower-Fruit Mountain · Rise of the Monkey King' },
      { through: 12, asset: 'cutscene_kunlun', zh: '昆仑玉虚 · 变化问道', en: 'Kunlun · The Transformation Trials' },
      { through: 19, asset: 'cutscene_dragon_palace', zh: '东海龙宫 · 神珍认主', en: 'Eastern Sea · The Ruyi Staff Awakens' },
      { through: 29, asset: 'cutscene_havoc_heaven', zh: '大闹天宫 · 诸神拦路', en: 'Havoc in Heaven · The Celestial Duels' },
      { through: 32, asset: 'cutscene_five_finger', zh: '如来神掌 · 五指山下', en: 'Buddha’s Palm · Beneath Five-Finger Mountain' },
      { through: 40, asset: 'cutscene_pilgrims', zh: '取经人成行 · 师徒聚首', en: 'The Pilgrims Assemble' },
      { through: 50, asset: 'cutscene_bone_spider', zh: '白骨盘丝 · 幻相迷心', en: 'Bone and Web · Trials of Deception' },
      { through: 65, asset: 'cutscene_flaming_mountain', zh: '火云翠云 · 牛门恩怨', en: 'Flaming Mountain · The Bull Family' },
      { through: 77, asset: 'cutscene_mid_trials', zh: '碧波小雷音 · 佛宝与伪佛', en: 'Emerald Waves and False Thunderclap' },
      { through: 82, asset: 'cutscene_lion_camel', zh: '狮驼国 · 三魔封天', en: 'Lion-Camel Kingdom · Three Demon Kings' },
      { through: 96, asset: 'cutscene_late_trials', zh: '无底洞至青龙山 · 西路将尽', en: 'Bottomless Cave to Azure-Dragon Mountain' },
      { through: 100, asset: 'cutscene_vulture_peak', zh: '天竺灵山 · 功果圆满', en: 'Tianzhu to Vulture Peak · Journey Fulfilled' },
    ];

    function getCutsceneArc(chapter) {
      if (gameState.campaignRoute === 'fengshen') {
        return chapter <= 18
          ? { through:18, asset:'cutscene_fengshen_act1', zh:'二郎影卷·玉泉桃山至西岐', en:'Erlang Chronicle · Yuquan, Peach Mountain, and Xiqi' }
          : { through:38, asset:'cutscene_fengshen_act2', zh:'二郎影卷·绝龙黄河至封神台', en:'Erlang Chronicle · Juelong Ridge to the Investiture Altar' };
      }
      return CUTSCENE_ARCS.find(arc => chapter <= arc.through) || CUTSCENE_ARCS[CUTSCENE_ARCS.length - 1];
    }

    function buildCinematicSlides(data, chapter) {
      const slides = [{
        speaker: 'narrator',
        name: uiText('章回旁白', 'Storyteller'),
        text: gameState.campaignRoute === 'fengshen'
          ? uiText(`第 ${chapter} 章 · ${data.bossTitle}。此卷从杨戬亲历之事展开，天眼所见不只胜负，也照见封神大战的代价。`, `Chapter ${chapter} · ${data.bossTitle}. Told from Yang Jian’s own experience, the Third Eye sees not only victory and defeat, but the cost of Investiture.`)
          : uiText(`第 ${chapter} 章 · ${data.bossTitle}。西行路在此转入新的劫难，众人尚不知前方等待着什么。`, `Chapter ${chapter} · ${data.bossTitle}. The westward road reaches another turning point, and the travelers step into an uncertain trial.`)
      }, ...data.dialogues];
      while (slides.length < 3) {
        slides.push({
          speaker: 'narrator',
          name: uiText('章回旁白', 'Storyteller'),
          text: uiText('风云已动，眼前的选择将决定下一段西行路。', 'The scene is set; what happens here will shape the next stretch of the journey.')
        });
      }
      return slides;
    }

    let currentBossDialogueData = null;
    let currentCinematicSlides = [];
    let currentBossDialogueChapter = 0;
    let currentDialogueStep = 0;

    function openBossDialogue(chamberIndex) {
      const data = getLocalizedBossDialogue(chamberIndex);
      if (!data) return;

      beginDialoguePause();
      currentBossDialogueData = data;
      currentBossDialogueChapter = chamberIndex;
      currentCinematicSlides = buildCinematicSlides(data, chamberIndex);
      currentDialogueStep = 0;

      const modal = document.getElementById('boss-dialogue-modal');
      const bossNameEl = document.getElementById('dialogue-boss-name');
      const bossTitleEl = document.getElementById('dialogue-boss-title');
      const modeTitleEl = document.getElementById('dialogue-mode-title');
      const controlHintEl = document.getElementById('dialogue-control-hint');
      const skipBtn = document.getElementById('dialogue-skip-btn');

      bossNameEl.innerText = data.bossName;
      bossTitleEl.innerText = data.bossTitle;
      modeTitleEl.innerText = gameState.campaignRoute === 'fengshen'
        ? (data.isBattle === false ? uiText('🎞 二郎封神影卷', '🎞 ERLANG FENGSHEN CHRONICLE') : uiText('👁 天眼宿命战卷', '👁 THIRD-EYE DESTINED ENCOUNTER'))
        : (data.isBattle === false ? uiText('🎞 西游影卷', '🎞 JOURNEY CHRONICLE') : uiText('⚔ 宿命影卷', '⚔ DESTINED ENCOUNTER'));
      controlHintEl.innerText = uiText('[空格 / Enter] 下一幕 · 战斗全程暂停', '[Space / Enter] Next slide · Combat remains paused');
      skipBtn.innerText = uiText('跳过影卷', 'Skip Cutscene');

      renderBossDialogueStep();
      modal.style.display = 'flex';
      sound.playGong();
    }

    function renderBossDialogueStep() {
      if (!currentBossDialogueData) return;
      const step = currentCinematicSlides[currentDialogueStep];
      if (!step) {
        skipBossDialogue();
        return;
      }

      const tagEl = document.getElementById('dialogue-speaker-tag');
      const textEl = document.getElementById('dialogue-text-body');
      const nextBtn = document.getElementById('dialogue-next-btn');
      const counterEl = document.getElementById('dialogue-slide-counter');
      const frameEl = document.getElementById('dialogue-cinematic-frame');
      const imageEl = document.getElementById('dialogue-cinematic-image');
      const artLabelEl = document.getElementById('dialogue-art-label');
      const arc = getCutsceneArc(currentBossDialogueChapter);

      const visualSlide = Math.min(currentDialogueStep + 1, 4);
      const slideAssetKey = `${arc.asset}_slide_${visualSlide}`;
      const art = loadedImages[slideAssetKey] || loadedImages[arc.asset];
      if (art?.src && imageEl.src !== art.src) imageEl.src = art.src;
      imageEl.alt = uiText(
        `${arc.zh}剧情插画，第 ${visualSlide} 幕`,
        `${arc.en} story illustration, scene ${visualSlide}`
      );
      artLabelEl.innerText = gameState.language === 'en'
        ? `${arc.en} · Scene ${visualSlide}`
        : `${arc.zh} · 第 ${visualSlide} 幕`;
      counterEl.innerText = `${currentDialogueStep + 1} / ${currentCinematicSlides.length}`;
      const focus = step.speaker === 'wukong' || step.speaker === 'erlang' ? 'wukong' : (step.speaker === 'narrator' ? 'narrator' : 'boss');
      frameEl.className = `cutscene-frame focus-${focus}`;
      void frameEl.offsetWidth;
      frameEl.classList.add('slide-enter');

      if (step.speaker === 'wukong' || step.speaker === 'erlang') {
        tagEl.innerText = step.speaker === 'erlang' ? uiText('二郎显圣真君 · 杨戬', 'Erlang Shen · Yang Jian') : uiText('齐天大圣 · 孙悟空', 'Great Sage · Sun Wukong');
        tagEl.style.borderColor = step.speaker === 'erlang' ? '#60a5fa' : '#facc15';
        tagEl.style.color = step.speaker === 'erlang' ? '#dbeafe' : '#fde047';
        tagEl.style.background = step.speaker === 'erlang' ? 'rgba(37, 99, 235, 0.25)' : 'rgba(234, 179, 8, 0.25)';
      } else if (step.speaker === 'narrator') {
        tagEl.innerText = step.name;
        tagEl.style.borderColor = '#60a5fa';
        tagEl.style.color = '#dbeafe';
        tagEl.style.background = 'rgba(37, 99, 235, 0.24)';
      } else if (step.speaker === 'ally') {
        tagEl.innerText = step.name;
        tagEl.style.borderColor = '#34d399';
        tagEl.style.color = '#d1fae5';
        tagEl.style.background = 'rgba(5, 150, 105, 0.22)';
      } else {
        tagEl.innerText = step.name;
        tagEl.style.borderColor = '#ef4444';
        tagEl.style.color = '#fca5a5';
        tagEl.style.background = 'rgba(239, 68, 68, 0.25)';
      }

      textEl.innerText = step.text;

      const isLast = currentDialogueStep >= currentCinematicSlides.length - 1;
      nextBtn.innerText = isLast
        ? (currentBossDialogueData.isBattle === false ? uiText('继续西行 ➔', 'Continue West ➔') : uiText('接棒！开启大战 ⚔', 'Begin Battle ⚔'))
        : uiText('下一幕 ➔', 'Next Slide ➔');
    }

    function nextBossDialogueStep() {
      if (!currentBossDialogueData) return;
      currentDialogueStep++;
      if (currentDialogueStep >= currentCinematicSlides.length) {
        skipBossDialogue();
      } else {
        renderBossDialogueStep();
        sound.playJadeChime();
      }
    }

    function skipBossDialogue() {
      const modal = document.getElementById('boss-dialogue-modal');
      modal.style.display = 'none';
      const completedDialogue = currentBossDialogueData;

      const boss = enemies.find(e => e.isBoss && e.alive);
      if (boss && completedDialogue && completedDialogue.isBattle !== false) {
        speechBubbles.push(new SpeechBubbleFX(boss, completedDialogue.dialogues[0].text.substring(0, 24) + '...', 4.0, '#f87171'));
        const playerChallenge = gameState.playableHero === 'erlang'
          ? uiText('天眼已开，妖邪受伏！', 'The Third Eye opens—submit, demon!')
          : uiText('吃俺老孙一棒！', 'Taste my Ruyi Staff!');
        speechBubbles.push(new SpeechBubbleFX(player, playerChallenge, 3.0, '#facc15'));
      }
      currentBossDialogueData = null;
      currentCinematicSlides = [];
      currentBossDialogueChapter = 0;
      if (completedDialogue && completedDialogue.onComplete === 'transformationChoice') {
        endDialoguePause(false);
        openTransformationChoice();
      } else if (completedDialogue && completedDialogue.onComplete === 'journeyVictory') {
        endDialoguePause(false);
        handleGameOver(true);
      } else {
        endDialoguePause(true);
      }
    }

    function openTransformationChoice() {
      if (gameState.playableHero === 'erlang') {
        gameState.transformationDoctrine = 'erlang';
        gameState.isPaused = false;
        fxList.push(new HadesMagicCircleAOEFX(player.x, player.y, 115, 0.8, '#60a5fa'));
        floatingTexts.push(new FloatingText(player.x, player.y - 55, uiText('清源妙道 · 天眼法相已悟', 'Clear-Origin Art · Manifestation Unlocked'), '#fde68a', 20));
        return;
      }
      gameState.isPaused = true;
      document.getElementById('transformation-choice-modal').style.display = 'flex';
    }

    function chooseTransformationDoctrine(doctrine) {
      if (!['18', '36', '72'].includes(doctrine)) return;
      gameState.transformationDoctrine = doctrine;
      if (doctrine === '36') {
        player.increaseRunMaxHp(30, 30);
      } else if (doctrine === '72') {
        gameState.ashes += 36;
        scheduleMetaProgressSave();
      }
      const names = {
        '18': uiText('十八般变化·斗战', '18 Transformations · Warrior'),
        '36': uiText('三十六变·天罡', '36 Transformations · Celestial'),
        '72': uiText('七十二变·地煞', '72 Transformations · Earthly')
      };
      document.getElementById('transformation-choice-modal').style.display = 'none';
      gameState.isPaused = false;
      sound.playAwaken();
      fxList.push(new HadesMagicCircleAOEFX(player.x, player.y, 115, 0.8, '#c084fc'));
      floatingTexts.push(new FloatingText(player.x, player.y - 55, uiText(`已择 ${names[doctrine]}`, `Chosen: ${names[doctrine]}`), '#facc15', 20));
      updateHUD();
    }

    // EXIT GATES & PROGRESSION
    let exitGates = [];

    function setupExitGates() {
      exitGates = [];
      const godKeys = Object.keys(GODS);
      const hasAnyGodBoon = !!(player.boons.weapon || player.boons.attack || player.boons.special || player.boons.cast || player.boons.dash || player.boons.hex || (player.boons.passives && player.boons.passives.length > 0));

      const usedRewardTypes = new Set();
      const usedGodKeys = new Set();
      const gateOptions = [];

      // Constraint 1: AT LEAST ONE MUST BE GOD'S BOON
      const firstGodKey = takeWeightedGodKey(godKeys);
      usedGodKeys.add(firstGodKey);
      usedRewardTypes.add('god_' + firstGodKey);
      gateOptions.push({
        rewardType: 'god',
        godKey: firstGodKey,
        label: getGodDisplayName(firstGodKey)
      });

      // Possible other reward categories (No peaches until player has chosen a god's boon!)
      const otherCategories = ['shop', 'heart', 'ashes'];
      if (hasAnyGodBoon) {
        otherCategories.push('peach');
      }

      // Generate remaining 2 unique options without duplicates
      for (let i = 1; i < 3; i++) {
        const wantGod = Math.random() < 0.45 && godKeys.length > 0;
        if (wantGod) {
          const nextGod = takeWeightedGodKey(godKeys);
          usedGodKeys.add(nextGod);
          usedRewardTypes.add('god_' + nextGod);
          gateOptions.push({
            rewardType: 'god',
            godKey: nextGod,
            label: getGodDisplayName(nextGod)
          });
        } else {
          const availCats = otherCategories.filter(c => !usedRewardTypes.has(c));
          if (availCats.length > 0) {
            const cat = availCats[Math.floor(Math.random() * availCats.length)];
            usedRewardTypes.add(cat);
            let label = '';
            if (cat === 'peach') label = '天庭蟠桃 (神效精进)';
            else if (cat === 'shop') label = '龙宫宝阁 (灵丹妙药)';
            else if (cat === 'heart') label = '万年人参果 (+气血)';
            else if (cat === 'ashes') label = '功德灵砂 (+修为)';

            gateOptions.push({
              rewardType: cat,
              godKey: null,
              label: label
            });
          } else if (godKeys.length > 0) {
            const nextGod = takeWeightedGodKey(godKeys);
            usedGodKeys.add(nextGod);
            gateOptions.push({
              rewardType: 'god',
              godKey: nextGod,
              label: getGodDisplayName(nextGod)
            });
          }
        }
      }

      // Position the 3 gates evenly in an expansive formation
      const count = gateOptions.length;
      for (let i = 0; i < count; i++) {
        const ang = (i / count) * Math.PI * 2 + 0.3;
        const radialX = Math.max(105, Math.min(420, viewWidth * 0.27));
        const radialY = Math.max(145, Math.min(340, viewHeight * 0.25));
        const gateX = Math.cos(ang) * radialX;
        const gateY = Math.sin(ang) * radialY;

        exitGates.push({
          x: gateX,
          y: gateY,
          radius: 56,
          rewardType: gateOptions[i].rewardType,
          godKey: gateOptions[i].godKey,
          label: gateOptions[i].label
        });
      }

      document.getElementById('chamber-clear-alert').style.display = 'block';
    }

    const NG_PLUS_ENEMY_TIERS = [
      [
        { type:'ngp_stoneback_macaque', weight:28 }, { type:'ngp_wind_scout', weight:22 },
        { type:'ngp_jade_sword_adept', weight:20 }, { type:'ngp_thunder_talisman', weight:18 },
        { type:'ngp_bronze_guardian', weight:12 }
      ],
      [
        { type:'ngp_coral_sentinel', weight:24 }, { type:'ngp_pearl_siren', weight:22 },
        { type:'ngp_abyssal_shell', weight:13 }, { type:'ngp_cloud_lancer', weight:23 },
        { type:'ngp_star_fire_archer', weight:18 }
      ],
      [
        { type:'ngp_thunder_drum_colossus', weight:13 }, { type:'ngp_nether_chain_warden', weight:22 },
        { type:'ngp_white_bone_stalker', weight:24 }, { type:'ngp_web_cocoon_hexer', weight:21 },
        { type:'ngp_flame_cloud_spearling', weight:20 }
      ],
      [
        { type:'ngp_iron_fan_witch', weight:21 }, { type:'ngp_lion_fang_brute', weight:14 },
        { type:'ngp_shadow_mouse', weight:25 }, { type:'ngp_frost_hare', weight:22 },
        { type:'ngp_dustbreaker', weight:18 }
      ]
    ];

    function getNewGamePlusEnemyPool(index) {
      const tier = Math.max(0, Math.min(3, Math.floor((index - 1) / 25)));
      const current = NG_PLUS_ENEMY_TIERS[tier].map(entry => ({ ...entry }));
      // Celestial-Mirror echoes retain a few earlier threats in later acts, so
      // the roster broadens over the run instead of replacing five skins every
      // twenty-five chapters. The late game can therefore roll all 20 types.
      for (let previousTier = 0; previousTier < tier; previousTier++) {
        NG_PLUS_ENEMY_TIERS[previousTier].forEach(entry => current.push({ type:entry.type, weight:Math.max(4, Math.round(entry.weight * 0.22)) }));
      }
      return current;
    }

    function getAvailableEnemyPool(index) {
      if (gameState.isNewGamePlus) return getNewGamePlusEnemyPool(index);
      if (gameState.campaignRoute === 'fengshen') {
        if (index <= 4) return [{ type:'fengshen_mirror_disciple', weight:74 }, { type:'fengshen_soul_guard', weight:26 }];
        if (index <= 8) return [{ type:'fengshen_soul_guard', weight:58 }, { type:'fengshen_mirror_disciple', weight:42 }];
        if (index <= 12) return [{ type:'fengshen_soul_guard', weight:52 }, { type:'fengshen_array_adept', weight:48 }];
        if (index <= 16) return [{ type:'fengshen_array_adept', weight:64 }, { type:'fengshen_soul_guard', weight:36 }];
        if (index <= 20) return [{ type:'fengshen_soul_guard', weight:56 }, { type:'fengshen_array_adept', weight:44 }];
        if (index <= 24) return [{ type:'fengshen_array_adept', weight:66 }, { type:'fengshen_soul_guard', weight:34 }];
        if (index <= 28) return [{ type:'fengshen_array_adept', weight:55 }, { type:'fengshen_soul_guard', weight:27 }, { type:'fengshen_meishan_raider', weight:18 }];
        if (index <= 34) return [{ type:'fengshen_meishan_raider', weight:58 }, { type:'fengshen_array_adept', weight:27 }, { type:'fengshen_soul_guard', weight:15 }];
        return [{ type:'fengshen_soul_guard', weight:38 }, { type:'fengshen_array_adept', weight:34 }, { type:'fengshen_meishan_raider', weight:28 }];
      }
      if (index <= 5) return [{ type: 'campaign_monkey', weight: 100 }];
      if (index <= 12) return [
        { type: 'campaign_disciple', weight: 74 }, { type: 'bagua_golem', weight: 26 }
      ];
      if (index <= 18) return [
        { type: 'campaign_dragon_guard', weight: 72 }, { type: 'cave_spider', weight: 28 }
      ];
      if (index <= 32) return [
        { type: 'tianbing', weight: 42 }, { type: 'tian_archer', weight: 32 }, { type: 'tianbing_commander', weight: 26 }
      ];
      if (index <= 40) return [
        { type: 'demon_ape', weight: 45 }, { type: 'nether_ghost', weight: 30 }, { type: 'tianbing', weight: 25 }
      ];
      if (index <= 50) return [
        { type: 'cave_spider', weight: 48 }, { type: 'nether_ghost', weight: 30 }, { type: 'demon_ape', weight: 22 }
      ];
      if (index <= 65) return [
        { type: 'bagua_golem', weight: 28 }, { type: 'tianbing_commander', weight: 27 },
        { type: 'cave_spider', weight: 23 }, { type: 'nether_ghost', weight: 22 }
      ];
      if (index <= 72) return [
        { type: 'campaign_thorn_spirit', weight: 42 }, { type: 'campaign_late_acolyte', weight: 38 }, { type: 'nether_ghost', weight: 20 }
      ];
      if (index <= 82) return [
        { type: 'campaign_late_acolyte', weight: 48 }, { type: 'demon_ape', weight: 30 }, { type: 'tianbing_commander', weight: 22 }
      ];
      if (index <= 88) return [
        { type: 'campaign_late_acolyte', weight: 44 }, { type: 'cave_spider', weight: 34 }, { type: 'nether_ghost', weight: 22 }
      ];
      if (index <= 94) return [
        { type: 'campaign_late_acolyte', weight: 50 }, { type: 'demon_ape', weight: 28 }, { type: 'bagua_golem', weight: 22 }
      ];
      return [
        { type: 'campaign_late_acolyte', weight: 46 }, { type: 'nether_ghost', weight: 30 }, { type: 'tian_archer', weight: 24 }
      ];
    }

    const SAFE_ENEMY_SPAWN_DISTANCE = 640;
    const SAFE_BOSS_SPAWN_DISTANCE = 780;

    function getSafeEnemySpawnPosition(requestedX, requestedY, minDistance = SAFE_ENEMY_SPAWN_DISTANCE) {
      const minX = -1070;
      const maxX = 1070;
      const minY = -770;
      const maxY = 770;
      const clampX = value => Math.max(minX, Math.min(maxX, value));
      const clampY = value => Math.max(minY, Math.min(maxY, value));
      const firstX = clampX(requestedX);
      const firstY = clampY(requestedY);
      const requestedDx = firstX - player.x;
      const requestedDy = firstY - player.y;
      const requestedDistance = Math.hypot(requestedDx, requestedDy);
      if (requestedDistance >= minDistance) return { x: firstX, y: firstY };

      // Try a full ring around Wukong. This matters near arena edges, where simply
      // pushing the requested point outward could be clamped back into danger.
      const baseAngle = requestedDistance > 1
        ? Math.atan2(requestedDy, requestedDx)
        : Math.atan2(-player.y, -player.x || 1);
      let best = { x: firstX, y: firstY, distance: requestedDistance };
      for (let step = 0; step < 16; step++) {
        const offsetStep = step === 0 ? 0 : Math.ceil(step / 2) * (step % 2 ? 1 : -1);
        const angle = baseAngle + offsetStep * (Math.PI / 8);
        const candidateX = clampX(player.x + Math.cos(angle) * (minDistance + 24));
        const candidateY = clampY(player.y + Math.sin(angle) * (minDistance + 24));
        const distance = Math.hypot(candidateX - player.x, candidateY - player.y);
        if (distance > best.distance) best = { x: candidateX, y: candidateY, distance };
        if (distance >= minDistance) return { x: candidateX, y: candidateY };
      }
      return { x: best.x, y: best.y };
    }

    function spawnRandomEnemy(pool, spawnX, spawnY, minDistance = SAFE_ENEMY_SPAWN_DISTANCE) {
      const totalWeight = pool.reduce((acc, p) => acc + p.weight, 0);
      let rand = Math.random() * totalWeight;
      let selectedType = pool[0].type;
      for (const p of pool) {
        if (rand < p.weight) {
          selectedType = p.type;
          break;
        }
        rand -= p.weight;
      }
      const safeSpawn = getSafeEnemySpawnPosition(spawnX, spawnY, minDistance);
      fxList.push(new PortalSummonFX(safeSpawn.x, safeSpawn.y, selectedType.includes('tian') ? '#facc15' : '#c084fc'));
      const enemy = new Enemy(selectedType, safeSpawn.x, safeSpawn.y);
      enemies.push(enemy);
      return enemy;
    }

    function startChamber(index) {
      const campaignLastChapter = Math.max(1, Math.floor(Number(gameState.totalChambers) || 100));
      const requestedChapter = Math.floor(Number(index));
      index = Math.max(1, Math.min(campaignLastChapter, Number.isFinite(requestedChapter) ? requestedChapter : 1));
      if (index > 1) saveMetaProgress();
      gameState.chamberIndex = index;
      gameState.chamberCleared = false;
      enemies = [];
      projectiles = [];
      fxList = [];
      monkeyClones = [];
      speechBubbles = [];
      exitGates = [];
      activeLubanAvatar = null;
      activeClockworkKite = null;
      player.x = 0;
      player.y = 180;
      player.hasRuyiStaff = gameState.playableHero === 'wukong' && gameState.ruyiAcquired;
      updateHeroInterface();
      player.invulnTimer = Math.max(player.invulnTimer, index === 1 ? 10.5 : 2.25);
      document.getElementById('chamber-clear-alert').style.display = 'none';

      if (gameState.playableHero === 'erlang' || player.hasBoon('erlang_hound')) {
        const hound = new Enemy('xiaotianquan_hound', player.x + 40, player.y + 40, true);
        player.hound = hound;
        enemies.push(hound);
      }
      if (player.hasBoon('luban_clockwork_kite')) activeClockworkKite = new ClockworkKiteCompanion();

      const routeBosses = gameState.campaignRoute === 'fengshen' ? ERLANG_CAMPAIGN_BOSSES : CAMPAIGN_BOSSES;
      if (index % 10 === 0 && !routeBosses[index]) {
        activeLubanAvatar = new LubanAvatarNPC(0, -120);
      }

      const titleEl = document.getElementById('chamber-name');
      const subEl = document.getElementById('chamber-sub');

      const campaignStage = getCampaignStage(index);
      gameState.biome = campaignStage.biome + 1;
      gameState.campaignBiome = campaignStage.biome;
      const stageEnglish = gameState.campaignRoute === 'fengshen'
        ? [campaignStage.titleEn, campaignStage.subEn]
        : CAMPAIGN_STAGE_EN[campaignStage.biome];
      titleEl.innerText = gameState.language === 'en' && stageEnglish
        ? `${stageEnglish[0]} · Chapter ${index} / ${gameState.totalChambers}`
        : `${campaignStage.title} · 第 ${index} 章 / ${gameState.totalChambers} 章`;
      const chapterBeat = gameState.campaignRoute === 'fengshen'
        ? ERLANG_FENGSHEN_CHAPTERS[index]
        : LATE_CHAPTER_BEATS[index];
      subEl.innerText = chapterBeat
        ? (gameState.language === 'en' ? chapterBeat.en : chapterBeat.zh)
        : (gameState.language === 'en' && stageEnglish ? stageEnglish[1] : campaignStage.sub);

      const bossHud = document.getElementById('boss-hud');
      const bossConfig = routeBosses[index];
      const isBossChamber = !!bossConfig;
      const isStoryOnly = gameState.campaignRoute === 'fengshen' ? ERLANG_STORY_ONLY_CHAPTERS.has(index) : STORY_ONLY_CHAPTERS.has(index);
      gameState.isBossChamber = isBossChamber;
      gameState.isStoryChamber = isStoryOnly;

      if (isStoryOnly) {
        gameState.chamberType = 'story';
        bossHud.style.display = 'none';
        gameState.chamberTotalQuota = 0;
        gameState.chamberSpawned = 0;
        gameState.waveSpawnTimer = 0;
        player.invulnTimer = Math.max(player.invulnTimer, 2.5);
        openOrDeferBossDialogue(index);
      } else if (isBossChamber) {
        gameState.chamberType = 'boss';
        bossHud.style.display = 'flex';

        player.invulnTimer = Math.max(player.invulnTimer, 3.5);
        const bossTypes = bossConfig.types || [bossConfig.type];
        const spawnedBosses = bossTypes.map((type, bossIndex) => {
          const spreadAngle = -0.7 + bossIndex * (1.4 / Math.max(1, bossTypes.length - 1));
          const centeredBuddha = gameState.campaignRoute !== 'fengshen' && index === 32;
          const requestedBossX = centeredBuddha ? 0 : Math.cos(spreadAngle) * 620;
          const requestedBossY = centeredBuddha ? 80 : Math.sin(spreadAngle) * 430;
          const bossSpawn = getSafeEnemySpawnPosition(requestedBossX, requestedBossY, SAFE_BOSS_SPAWN_DISTANCE);
          const boss = new Enemy(type, bossSpawn.x, bossSpawn.y);
          enemies.push(boss);
          return boss;
        });

        gameState.chamberTotalQuota = bossTypes.length > 1 ? 0 : 7;
        gameState.chamberSpawned = 0;
        gameState.waveSpawnTimer = 0;

        document.getElementById('boss-name-text').innerText = spawnedBosses.map(boss => boss.name).join(' · ');

        // Trigger authentic Journey to the West Boss Dialogue!
        openOrDeferBossDialogue(index);
      } else {
        gameState.chamberType = 'normal';
        bossHud.style.display = 'none';

        // Full battlefield encounters: three times the former normal-enemy quota.
        const baseQuota = 8 + Math.min(8, Math.floor(index / 10));
        const totalQuota = baseQuota * NORMAL_ENEMY_WAVE_MULTIPLIER;
        gameState.chamberTotalQuota = totalQuota;
        gameState.chamberSpawned = 0;
        gameState.waveSpawnTimer = 0;

        // A small, distant vanguard gives first-time players room to read telegraphs.
        const initialCount = Math.min((4 + Math.floor(index / 25)) * NORMAL_ENEMY_WAVE_MULTIPLIER, totalQuota);
        const pool = getAvailableEnemyPool(index);
        for (let i = 0; i < initialCount; i++) {
          const ang = (i / initialCount) * Math.PI * 2 + (Math.random() * 0.4);
          const dist = SAFE_ENEMY_SPAWN_DISTANCE + 20 + Math.random() * 140;
          spawnRandomEnemy(pool, player.x + Math.cos(ang) * dist, player.y + Math.sin(ang) * dist);
        }
        gameState.chamberSpawned = initialCount;

        // Story conversations can introduce a location or companion without
        // pretending they are a boss fight.
        openOrDeferBossDialogue(index);
      }

      updateHUD();
    }

    function updateChamberSpawner(dt) {
      if (gameState.chamberCleared || gameState.isPaused) return;

      gameState.waveSpawnTimer = (gameState.waveSpawnTimer || 0) + dt;
      const interval = gameState.isBossChamber ? 4.5 : Math.max(2.4, 3.4 - gameState.chamberIndex * 0.004);

      if (gameState.waveSpawnTimer >= interval) {
        gameState.waveSpawnTimer = 0;

        if (gameState.chamberSpawned < gameState.chamberTotalQuota) {
          const activeLivingCount = enemies.filter(e => !e.isAlly && (e.alive || e.isDying)).length;
          const maxConcurrent = gameState.isBossChamber
            ? 6
            : Math.min(36, (9 + Math.floor(gameState.chamberIndex / 45)) * NORMAL_ENEMY_WAVE_MULTIPLIER);

          if (activeLivingCount < maxConcurrent) {
            const batchSize = Math.min(
              gameState.isBossChamber ? 2 : 3 * NORMAL_ENEMY_WAVE_MULTIPLIER,
              gameState.chamberTotalQuota - gameState.chamberSpawned
            );
            const pool = getAvailableEnemyPool(gameState.chamberIndex);

            for (let i = 0; i < batchSize; i++) {
              const spawnAngle = Math.random() * Math.PI * 2;
              const spawnDist = SAFE_ENEMY_SPAWN_DISTANCE + 20 + Math.random() * 180;
              const spawnX = Math.max(-1050, Math.min(1050, player.x + Math.cos(spawnAngle) * spawnDist));
              const spawnY = Math.max(-750, Math.min(750, player.y + Math.sin(spawnAngle) * spawnDist));

              spawnRandomEnemy(pool, spawnX, spawnY);
              gameState.chamberSpawned++;
            }
          }
        }
      }
    }

    function checkChamberClear() {
      if (gameState.chamberCleared || gameState.bossOutcomeActive) return;
      if (gameState.isBossChamber) {
        const mainBossAlive = enemies.some(e => e.isBoss && e.alive && !e.isSubdued);
        if (!mainBossAlive) {
          if (gameState.chamberIndex === 18 && !gameState.ruyiAcquired && gameState.playableHero === 'wukong') {
            gameState.ruyiAcquired = true;
            player.hasRuyiStaff = true;
            document.getElementById('weapon-style-title').innerText = uiText('如意金箍棒 · 一万三千五百斤', 'Ruyi Jingu Bang · 13,500 jin');
            player.qi = player.maxQi;
            fxList.push(new ColossalStaffNovaFX(player.x, player.y, 190, '#facc15'));
            floatingTexts.push(new FloatingText(player.x, player.y - 70, uiText('定海神珍认主 · 如意金箍棒！', 'The Sea-Calming Treasure chooses its master · Ruyi Jingu Bang!'), '#facc15', 23));
          }
          gameState.chamberCleared = true;
          sound.playGong();
          setupExitGates();
        }
      } else {
        if (gameState.chamberSpawned >= gameState.chamberTotalQuota) {
          const anyAlive = enemies.some(e => !e.isAlly && (e.alive || e.isDying));
          if (!anyAlive) {
            gameState.chamberCleared = true;
            sound.playGong();
            setupExitGates();
          }
        }
      }
    }

    // MODALS & BOONS LOGIC
    function openGodBoonModal(godKey) {
      beginRewardSelectionPause();
      const god = GODS[godKey] || GODS['luban'];
      const godEnglish = GOD_EN[godKey];
      const modal = document.getElementById('boon-modal');
      const container = document.getElementById('boon-choices-container');

      document.getElementById('god-name').innerText = gameState.language === 'en' && godEnglish ? godEnglish.name : god.name;
      document.getElementById('god-title').innerText = gameState.language === 'en' && godEnglish ? godEnglish.title : god.title;
      document.getElementById('god-quote').innerText = gameState.language === 'en' && godEnglish ? godEnglish.quote : god.quotes[Math.floor(Math.random() * god.quotes.length)];

      const portrait = document.getElementById('god-portrait');
      if (god.isAvatar) {
        const lubanImg = loadedImages['luban_avatar'];
        if (lubanImg && lubanImg.complete && lubanImg.naturalWidth > 0) {
          portrait.style.backgroundImage = `url(${lubanImg.src})`;
          portrait.style.backgroundPosition = `0 0`;
          portrait.style.backgroundSize = `800% 400%`;
        }
      } else if (god.portraitAsset === 'buddha_colossal') {
        const buddhaImg = loadedImages['buddha_colossal'];
        if (buddhaImg && buddhaImg.complete && buddhaImg.naturalWidth > 0) {
          portrait.style.backgroundImage = `url(${buddhaImg.src})`;
          portrait.style.backgroundPosition = '0 0';
          portrait.style.backgroundSize = '700% 400%';
        }
      } else {
        const godSheet = loadedImages['all_10_gods'];
        if (godSheet && godSheet.complete && godSheet.naturalWidth > 0) {
          const col = god.portraitCol !== undefined ? god.portraitCol : 0;
          const row = god.portraitRow !== undefined ? god.portraitRow : 0;
          portrait.style.backgroundImage = `url(${godSheet.src})`;
          portrait.style.backgroundPosition = `-${col * 120}px -${row * 120}px`;
          portrait.style.backgroundSize = `720px 240px`;
        }
      }

      container.innerHTML = '';
      const unownedBoons = god.boons.filter(b => !player.hasBoon(b.id));
      const pool = unownedBoons.length >= 3 ? unownedBoons : god.boons;
      const availableBoons = [...pool].sort(() => 0.5 - Math.random()).slice(0, 3);

      availableBoons.forEach(boon => {
        const shownBoon = getLocalizedBoon(boon, godKey);
        const slotKey = getBoonSlotKey(boon.slot);
        const equipped = slotKey ? player.boons[slotKey] : null;
        const takeoverLevel = equipped ? (equipped.level || 1) + 1 : 1;
        const takeoverCopy = slotKey === 'attack' && equipped
          ? `<div style="margin-top:10px;color:#fde68a;font-size:13px;line-height:1.45;">${gameState.language === 'en'
            ? `↻ Normal-attack takeover: preserves every Peach rank and advances to Rank ${takeoverLevel}`
            : `↻ 接管普攻：保留已吃蟠桃的修为，并升至第 ${takeoverLevel} 重`}<br>${getAttackComboPreview(equipped.level || 1).join('/')} → ${getAttackComboPreview(takeoverLevel).join('/')}</div>`
          : '';
        const card = document.createElement('button');
        card.type = 'button';
        card.className = 'boon-card';
        card.innerHTML = `
          <div>
            <div class="boon-slot-tag">${gameState.language === 'en' ? translateGameText(boon.slot) : boon.slot}</div>
            <div class="boon-name" style="color: ${god.color};">${shownBoon.name}</div>
            <div class="boon-desc">${shownBoon.desc}</div>
            ${takeoverCopy}
          </div>
          <div class="boon-action-btn">${slotKey === 'attack' && equipped
            ? (gameState.language === 'en' ? `Take Over Attack · Rank ${takeoverLevel}` : `接管普攻 · 升至第 ${takeoverLevel} 重`)
            : (gameState.language === 'en' ? 'Accept Divine Boon' : '领受仙法神通')}</div>
        `;
        card.onclick = () => {
          applyBoon(boon, godKey);
          modal.style.display = 'none';
          endRewardSelectionPause();
          sound.playJadeChime();
        };
        container.appendChild(card);
      });

      modal.style.display = 'flex';
    }

    function applyBoon(boon, godKey) {
      const slot = boon.slot;
      const slotKey = getBoonSlotKey(slot);
      const previous = slotKey ? player.boons[slotKey] : null;
      let nextLevel = Math.max(1, player.boonLevels[boon.id] || 0);
      if (previous) {
        player.boonLevels[previous.id] = previous.level || 1;
        nextLevel = Math.max(nextLevel, (previous.level || 1) + 1);
      }
      const boonData = { ...getLocalizedBoon(boon, godKey), godKey: godKey, level: nextLevel };

      if (boon.weaponForm) {
        player.weaponStyle = boon.weaponForm;
        const weaponLabels = {
          titan: ['Ruyi Jingu Bang · Mountain-Crushing Style', '如意金箍棒 · 巨灵重岳流'],
          extend: ['Ruyi Jingu Bang · Heaven-Reaching Style', '如意金箍棒 · 擎天长锋流'],
          chain: ['Ruyi Jingu Bang · Nine-Section Chain Style', '如意金箍棒 · 锁龙九节流']
        };
        const label = weaponLabels[boon.weaponForm] || weaponLabels.extend;
        document.getElementById('weapon-style-title').innerText = gameState.language === 'en' ? label[0] : label[1];
      }

      let effectiveLevel = nextLevel;
      if (slotKey) {
        player.boons[slotKey] = boonData;
        player.boonLevels[boon.id] = nextLevel;
        const tag = document.getElementById(`boon-tag-${slotKey}`);
        if (tag) tag.innerText = `${boonData.name} · Lv.${nextLevel}`;
        if (previous) {
          const verb = gameState.language === 'en'
            ? (previous.id === boon.id ? 'Boon Improved' : `${getGodDisplayName(godKey)} Takeover`)
            : (previous.id === boon.id ? '神通精进' : `${GODS[godKey]?.name || '仙圣'}接管`);
          const slotLabel = gameState.language === 'en' ? (slotKey === 'attack' ? 'Attack' : 'Boon') : (slotKey === 'attack' ? '普攻' : '神通');
          floatingTexts.push(new FloatingText(player.x, player.y - 52, gameState.language === 'en'
            ? `${verb} · ${slotLabel} Rank ${nextLevel}!`
            : `${verb} · ${slotLabel}第 ${nextLevel} 重!`, '#fde68a'));
        }
      } else {
        const ownedPassive = player.boons.passives.find(item => item.id === boon.id);
        if (ownedPassive) {
          ownedPassive.level = (ownedPassive.level || 1) + 1;
          effectiveLevel = ownedPassive.level;
        } else {
          player.boons.passives.push(boonData);
          effectiveLevel = boonData.level || 1;
        }
        player.boonLevels[boon.id] = effectiveLevel;
      }

      // Passive rewards become live immediately instead of waiting for a reset
      // or existing only as card text.
      if (boon.id === 'luban_clockwork_kite') {
        if (!activeClockworkKite || !activeClockworkKite.alive) activeClockworkKite = new ClockworkKiteCompanion();
        activeClockworkKite.fireTimer = Math.min(activeClockworkKite.fireTimer, 0.45);
      } else if (boon.id === 'bull_ironhide') {
        player.bullArmorMax = 50 + Math.max(0, effectiveLevel - 1) * 25;
        player.bullArmor = player.bullArmorMax;
        player.timeSinceDamage = 999;
      } else if (boon.id === 'luban_masterwork') {
        player.masterworkArmorMax = 50 * effectiveLevel;
        player.masterworkArmor = player.masterworkArmorMax;
      } else if (boon.id === 'guanyin_nirvana') {
        player.maxLives += 1;
        player.lives += 1;
      } else if (boon.id === 'erlang_hound') {
        const existingHound = enemies.find(enemy => enemy.alive && enemy.isAlly && enemy.typeKey === 'xiaotianquan_hound');
        if (!existingHound) enemies.push(new Enemy('xiaotianquan_hound', player.x + 70, player.y + 45, true));
        floatingTexts.push(new FloatingText(player.x, player.y - 45, gameState.language === 'en' ? 'Xiaotianquan answers the call!' : '哮天神犬奉召降临!', '#facc15'));
      }
      const cueColor = GODS[godKey]?.color || '#facc15';
      fxList.push(new Shockwave(player.x, player.y, 76, cueColor));
      floatingTexts.push(new FloatingText(player.x, player.y - 62,
        uiText('神通已显化 · 效果生效', 'Boon Manifested · Effect Active'), cueColor, 14));
      gameState.boonsCount++;
      updateHUD();
    }

    function openPeachModal() {
      beginRewardSelectionPause();
      const modal = document.getElementById('pom-modal');
      const container = document.getElementById('pom-choices-container');
      container.innerHTML = '';

      const peachIcon = document.getElementById('peach-modal-icon');
      const rewImg = loadedImages['reward_icons'];
      if (rewImg && rewImg.complete && rewImg.naturalWidth > 0) {
        peachIcon.style.backgroundImage = `url(${rewImg.src})`;
        peachIcon.style.backgroundPosition = `0 0`;
        peachIcon.style.backgroundSize = `200% 200%`;
      }

      const equipped = [];
      if (player.boons.weapon) equipped.push(player.boons.weapon);
      if (player.boons.attack) equipped.push(player.boons.attack);
      if (player.boons.special) equipped.push(player.boons.special);
      if (player.boons.cast) equipped.push(player.boons.cast);
      if (player.boons.dash) equipped.push(player.boons.dash);
      if (player.boons.hex) equipped.push(player.boons.hex);
      player.boons.passives.forEach(b => equipped.push(b));

      if (equipped.length === 0) {
        player.increaseRunMaxHp(30, 30);
        gameState.peachesEaten++;
        sound.playPeachBite();
        modal.style.display = 'none';
        endRewardSelectionPause();
        floatingTexts.push(new FloatingText(player.x, player.y - 40, gameState.language === 'en' ? 'Maximum Health +30 (Celestial Peach)!' : '气血上限 +30 (仙桃延寿)!', '#fb7185'));
        return;
      }

      const choices = equipped.sort(() => 0.5 - Math.random()).slice(0, 3);
      choices.forEach(b => {
        const rankForecast = getPeachRankForecast(b);
        const forecastRankLabel = rankForecast.minLevel === rankForecast.maxLevel
          ? `${rankForecast.minLevel}`
          : `${rankForecast.minLevel}–${rankForecast.maxLevel}`;
        const card = document.createElement('button');
        card.type = 'button';
        card.className = 'boon-card';
        card.innerHTML = `
          <div>
            <div class="boon-slot-tag" style="background: rgba(251, 113, 133, 0.2); border-color: var(--peach-pink); color: var(--peach-glow);">${gameState.language === 'en'
              ? `${translateGameText(b.slot)} · Rank ${rankForecast.level} ➔ Rank ${forecastRankLabel}`
              : `${b.slot} · 第 ${rankForecast.level} 重 ➔ 第 ${forecastRankLabel} 重`}</div>
            <div class="boon-name" style="color: var(--peach-glow);">${b.name}</div>
            <div class="boon-desc">${b.desc}</div>
            <div class="boon-upgrade-preview">${getBoonUpgradePreview(b)}</div>
          </div>
          <div class="boon-action-btn" style="background: linear-gradient(180deg, #e11d48, #9f1239);">${gameState.language === 'en' ? 'Eat Peach · Raise Rank' : '服食蟠桃 · 提升重数'}</div>
        `;
        card.onclick = () => {
          let rankIncrease = 1;
          if (player.hasBoon('laojun_elixir')) rankIncrease += player.getBoonLevel('laojun_elixir');
          if (player.hasBoon('luban_masterwork') && Math.random() < 0.5) rankIncrease += 1;
          b.level = (b.level || 1) + rankIncrease;
          player.boonLevels[b.id] = b.level;
          gameState.peachesEaten++;
          if (player.hasBoon('laojun_elixir')) {
            player.hp = player.maxHp;
            fxList.push(new AnimatedFireExplosion(player.x, player.y, 72));
            floatingTexts.push(new FloatingText(player.x, player.y - 58,
              uiText('九转金丹 · 满血且额外精进！', 'Nine-Turn Elixir · Full Health and Bonus Rank!'), '#f472b6'));
          }
          if (b.id === 'bull_ironhide') {
            player.bullArmorMax = 50 + Math.max(0, b.level - 1) * 25;
            player.bullArmor = player.bullArmorMax;
          } else if (b.id === 'luban_masterwork') {
            player.masterworkArmorMax = 50 * b.level;
            player.masterworkArmor = player.masterworkArmorMax;
          } else if (b.id === 'guanyin_nirvana') {
            player.maxLives += rankIncrease;
            player.lives += rankIncrease;
          } else if (b.id === 'luban_clockwork_kite' && activeClockworkKite) {
            activeClockworkKite.fireTimer = Math.min(activeClockworkKite.fireTimer, 0.35);
          }
          sound.playPeachBite();
          modal.style.display = 'none';
          endRewardSelectionPause();
          floatingTexts.push(new FloatingText(player.x, player.y - 40, gameState.language === 'en' ? `Rank ${b.level} ${b.name}! (+${rankIncrease})` : `第 ${b.level} 重 ${b.name}! (+${rankIncrease})`, '#fb7185'));
          const slotKey = getBoonSlotKey(b.slot);
          if (slotKey) {
            const tag = document.getElementById(`boon-tag-${slotKey}`);
            if (tag) tag.innerText = `${b.name} · Lv.${b.level}`;
          }
          updateHUD();
        };
        container.appendChild(card);
      });

      modal.style.display = 'flex';
    }

    function renderShopResourceSummary() {
      const healthItem = document.getElementById('shop-health-item');
      const livesItem = document.getElementById('shop-lives-item');
      document.getElementById('shop-gold-label').innerText = uiText('🪙 当前灵石', '🪙 Spirit Stones');
      document.getElementById('shop-health-label').innerText = uiText('❤️ 当前气血', '❤️ Current Health');
      document.getElementById('shop-lives-label').innerText = uiText('💗 剩余金身', '💗 Lives Remaining');
      document.getElementById('shop-merit-label').innerText = uiText('✨ 功德灵砂', '✨ Merit Sand');
      document.getElementById('shop-gold-value').innerText = gameState.gold;
      document.getElementById('shop-health-value').innerText = `${Math.max(0, Math.ceil(player.hp))} / ${Math.ceil(player.maxHp)}`;
      document.getElementById('shop-lives-value').innerText = `${player.lives} / ${player.maxLives}`;
      document.getElementById('shop-merit-value').innerText = gameState.ashes;
      healthItem.classList.toggle('critical', player.hp <= player.maxHp * 0.35);
      livesItem.classList.toggle('critical', player.lives <= 0);
      document.getElementById('shop-resource-summary').setAttribute('aria-label', uiText(
        `当前资源：${gameState.gold} 灵石，${Math.ceil(player.hp)} / ${Math.ceil(player.maxHp)} 气血，${player.lives} / ${player.maxLives} 金身，${gameState.ashes} 功德灵砂`,
        `Current resources: ${gameState.gold} Spirit Stones, ${Math.ceil(player.hp)} of ${Math.ceil(player.maxHp)} Health, ${player.lives} of ${player.maxLives} lives, ${gameState.ashes} Merit Sand`
      ));
    }

    const shopVisitPurchases = new Set();

    function openShopModal(startNewVisit = false) {
      if (startNewVisit) shopVisitPurchases.clear();
      beginRewardSelectionPause();
      const modal = document.getElementById('shop-modal');
      const container = document.getElementById('shop-choices-container');
      container.innerHTML = '';
      renderShopResourceSummary();

      const items = [
        {
          id: 'life_elixir', oncePerVisit: true,
          name: gameState.language === 'en' ? 'Ten-Thousand-Year Lingzhi' : '万年九叶灵芝 (疗伤生肌)',
          desc: gameState.language === 'en' ? 'Restore 60 Health and permanently raise maximum Health by 25. Limit: once per pavilion visit.' : '恢复 60 点气血，并永久提升 25 点气血上限。每次宝阁事件限购一次。',
          cost: 60, action: () => { player.increaseRunMaxHp(25, 60); }
        },
        {
          id: 'celestial_peach',
          name: gameState.language === 'en' ? 'Queen Mother’s Celestial Peach' : '王母天庭蟠桃 (仙品神果)',
          desc: gameState.language === 'en' ? 'Raise one learned divine ability by one rank and preview the exact improvement.' : '选择一项已习得的神通重数 +1，并明确显示提升前后数值。',
          cost: 95, opensModal: true, action: () => { openPeachModal(); }
        },
        {
          id: 'merit_talisman',
          name: gameState.language === 'en' ? 'Merit Talisman of the Supreme Elder' : '太上开光功德符 (道门至宝)',
          desc: gameState.language === 'en' ? 'Gain 30 Merit Sand for permanent 72 Transformations training.' : '直接获得 30 点功德灵砂以供修炼七十二变。',
          cost: 50, action: () => { gameState.ashes += 30; }
        }
      ];

      items.forEach(it => {
        const purchasedThisVisit = Boolean(it.oncePerVisit && shopVisitPurchases.has(it.id));
        const affordable = gameState.gold >= it.cost;
        const balanceAfter = Math.max(0, gameState.gold - it.cost);
        const shortfall = Math.max(0, it.cost - gameState.gold);
        const card = document.createElement('button');
        card.type = 'button';
        card.className = `boon-card${affordable ? '' : ' unaffordable'}${purchasedThisVisit ? ' purchased-this-visit' : ''}`;
        card.disabled = purchasedThisVisit;
        card.setAttribute('aria-disabled', String(purchasedThisVisit || !affordable));
        card.innerHTML = `
          <div>
            <div class="boon-slot-tag">${gameState.language === 'en' ? 'Dragon-Palace Treasure' : '龙宫珍宝'}</div>
            <div class="boon-name">${it.name}</div>
            <div class="boon-desc">${it.desc}</div>
          </div>
          <div class="boon-action-btn">${purchasedThisVisit
            ? uiText('本次宝阁已购', 'Purchased This Visit')
            : (gameState.language === 'en'
              ? (affordable ? `Trade 🪙 ${it.cost} · ${balanceAfter} left` : `Need 🪙 ${shortfall} more`)
              : (affordable ? `兑换 🪙 ${it.cost} · 余 ${balanceAfter}` : `还需 🪙 ${shortfall} 灵石`))}</div>
        `;
        card.onclick = () => {
          if (it.oncePerVisit && shopVisitPurchases.has(it.id)) return;
          if (gameState.gold >= it.cost) {
            gameState.gold -= it.cost;
            if (it.oncePerVisit) shopVisitPurchases.add(it.id);
            if (it.opensModal) modal.style.display = 'none';
            it.action();
            sound.playJadeChime();
            updateHUD();
            if (!it.opensModal) openShopModal(false);
          } else {
            alert(gameState.language === 'en' ? 'Not enough Spirit Stones!' : '灵石不足！');
          }
        };
        container.appendChild(card);
      });

      modal.style.display = 'flex';
    }

    function closeShopModal() {
      document.getElementById('shop-modal').style.display = 'none';
      endRewardSelectionPause();
    }

        // PERMANENT BROWSER PROFILE + 72 TRANSFORMATIONS SKILL TREE
    const META_SAVE_KEY = 'havocInHeavenMetaV3';
    const RUN_CHECKPOINT_SAVE_KEY = 'havocInHeavenRunCheckpointV1';
    const LEGACY_META_SAVE_KEY = 'havocInHeavenMetaV2';
    const PERMANENT_PASSIVES = [
      { id: 'damage', icon: '⚔️', name: '斗战本能', nameEn: 'Battle Instinct', maxRank: 100, baseCost: 15, costStep: 5, effect: rank => `全部伤害 +${rank}%`, effectEn: rank => `All damage +${rank}%`, perLevel: '每级全部伤害 +1%', perLevelEn: 'All damage +1% per level' },
      { id: 'vitality', icon: '❤️', name: '金刚道体', nameEn: 'Diamond Body', maxRank: 100, baseCost: 12, costStep: 4, effect: rank => `最大气血 +${rank}%`, effectEn: rank => `Maximum Health +${rank}%`, perLevel: '每级最大气血 +1%', perLevelEn: 'Maximum Health +1% per level' },
      { id: 'qi_regen', icon: '☯️', name: '混元吐纳', nameEn: 'Primordial Breathing', maxRank: 100, baseCost: 10, costStep: 4, effect: rank => `真气回复 +${rank}%`, effectEn: rank => `Qi regeneration +${rank}%`, perLevel: '每级真气回复 +1%', perLevelEn: 'Qi regeneration +1% per level' },
      { id: 'precision', icon: '🎯', name: '火眼金睛', nameEn: 'Fiery Golden Eyes', maxRank: 50, baseCost: 20, costStep: 8, effect: rank => `暴击率 +${(rank * 0.2).toFixed(1)}%`, effectEn: rank => `Critical chance +${(rank * 0.2).toFixed(1)}%`, perLevel: '每级暴击率 +0.2%', perLevelEn: 'Critical chance +0.2% per level' }
    ];

    const ERLANG_SKILLS = [
      { id:'eye_sight', branch:'eye', icon:'👁', nameZh:'天眼照妖', nameEn:'Demon-Revealing Third Eye', baseCost:8, step:2, effects:{ crit:.0015, eyeDamage:.015 }, descZh:'每重：暴击率 +0.15%，天眼枪伤害 +1.5%。', descEn:'Per rank: +0.15% critical chance and +1.5% Third-Eye Lance damage.' },
      { id:'eye_lance', branch:'eye', icon:'⚡', nameZh:'破妄神光', nameEn:'Truth-Piercing Lance', baseCost:11, step:2, prereq:'eye_sight', effects:{ eyeDamage:.025, eyeRange:6 }, descZh:'每重：天眼枪伤害 +2.5%，射程 +6。', descEn:'Per rank: +2.5% lance damage and +6 range.' },
      { id:'eye_chain', branch:'eye', icon:'🔗', nameZh:'连霄雷索', nameEn:'Sky-Chaining Lightning', baseCost:14, step:2, prereq:'eye_lance', effects:{ eyeChainProgress:.25 }, descZh:'每 4 重增加 1 次雷链跳跃；每次跳跃造成天眼枪 38% 伤害。', descEn:'Every 4 ranks adds one lightning jump dealing 38% of lance damage.' },
      { id:'eye_mark', branch:'eye', icon:'🎯', nameZh:'审判烙印', nameEn:'Judgment Brand', baseCost:17, step:3, prereq:'eye_chain', effects:{ markDamage:.02 }, descZh:'每重：被天眼标记的敌人受到二郎神伤害 +2%。', descEn:'Per rank: enemies branded by the Third Eye take +2% damage from Erlang.' },
      { id:'eye_clarity', branch:'eye', icon:'💠', nameZh:'清明玄照', nameEn:'Clear Mystic Sight', baseCost:20, step:3, prereq:'eye_mark', effects:{ maxQi:1.5, qiRegen:.03 }, descZh:'每重：最大真气 +1.5，真气每秒回复 +0.03。', descEn:'Per rank: +1.5 maximum Qi and +0.03 Qi regeneration per second.' },
      { id:'eye_array', branch:'eye', icon:'🔷', nameZh:'灌江审判阵', nameEn:'Guanjiang Judgment Array', baseCost:23, step:3, prereq:'eye_clarity', effects:{ arrayDamage:.025, arrayRadius:1.5, arrayDuration:.025 }, descZh:'每重：审判阵伤害 +2.5%，半径 +1.5，持续时间 +0.025 秒。', descEn:'Per rank: +2.5% array damage, +1.5 radius, and +0.025s duration.' },
      { id:'eye_verdict', branch:'eye', icon:'🌟', nameZh:'三界明断', nameEn:'Verdict of Three Realms', baseCost:28, step:4, prereq:'eye_array', effects:{ bossDamage:.006, eyeWidth:.45 }, descZh:'每重：对首领伤害 +0.6%，天眼枪命中宽度 +0.45。', descEn:'Per rank: +0.6% boss damage and +0.45 lance hit width.' },

      { id:'spear_mastery', branch:'spear', icon:'🔱', nameZh:'三尖枪宗', nameEn:'Three-Pointed Spear Mastery', baseCost:8, step:2, effects:{ spearDamage:.018 }, descZh:'每重：全部枪术与连招伤害 +1.8%。', descEn:'Per rank: +1.8% spear and combo damage.' },
      { id:'spear_tempo', branch:'spear', icon:'💨', nameZh:'游龙枪势', nameEn:'Wandering-Dragon Tempo', baseCost:11, step:2, prereq:'spear_mastery', effects:{ attackSpeed:.006 }, descZh:'每重：攻击速度 +0.6%。', descEn:'Per rank: +0.6% attack speed.' },
      { id:'spear_reach', branch:'spear', icon:'📏', nameZh:'锋贯八荒', nameEn:'Edge Across Eight Wilds', baseCost:14, step:2, prereq:'spear_tempo', effects:{ spearReach:.004 }, descZh:'每重：普通枪术与连招范围 +0.4%。', descEn:'Per rank: +0.4% normal spear and combo reach.' },
      { id:'spear_launcher', branch:'spear', icon:'↗️', nameZh:'苍龙升月', nameEn:'Crescent Dragon Rise', baseCost:17, step:3, prereq:'spear_reach', effects:{ launchDamage:.025, launchForce:5 }, descZh:'每重：苍龙升月伤害 +2.5%，挑飞力度 +5。', descEn:'Per rank: +2.5% Crescent Dragon Rise damage and +5 launch force.' },
      { id:'spear_wheel', branch:'spear', icon:'🌀', nameZh:'灌江天轮', nameEn:'Guanjiang Heavenly Wheel', baseCost:20, step:3, prereq:'spear_launcher', effects:{ spinDamage:.025, spinRadius:1.5 }, descZh:'每重：天轮伤害 +2.5%，周身范围 +1.5。', descEn:'Per rank: +2.5% Heavenly Wheel damage and +1.5 radial reach.' },
      { id:'spear_break', branch:'spear', icon:'🛡️', nameZh:'裂甲神锋', nameEn:'Armor-Rending Divine Edge', baseCost:23, step:3, prereq:'spear_wheel', effects:{ armorBreak:.012 }, descZh:'每重：枪击无视 1.2% 敌方护甲，并加深审判印。', descEn:'Per rank: spear hits ignore 1.2% armor and deepen Judgment Brand.' },
      { id:'spear_sage', branch:'spear', icon:'☄️', nameZh:'清源枪圣', nameEn:'Clear-Origin Spear Sage', baseCost:28, step:4, prereq:'spear_break', effects:{ comboDamage:.012, comboWindow:.012 }, descZh:'每重：完成连招伤害 +1.2%，输入宽限 +0.012 秒。', descEn:'Per rank: +1.2% completed-combo damage and +0.012s input grace.' },

      { id:'hound_bond', branch:'mystic', icon:'🐕', nameZh:'神犬同心', nameEn:'Divine Hound Bond', baseCost:8, step:2, effects:{ houndDamage:.025 }, descZh:'每重：哮天犬撕咬伤害 +2.5%。', descEn:'Per rank: +2.5% Xiaotianquan bite damage.' },
      { id:'hound_bite', branch:'mystic', icon:'🦷', nameZh:'锁妖犬牙', nameEn:'Demon-Locking Fangs', baseCost:11, step:2, prereq:'hound_bond', effects:{ houndDamage:.018, houndStun:.01 }, descZh:'每重：犬袭伤害 +1.8%，定身 +0.01 秒。', descEn:'Per rank: +1.8% hound damage and +0.01s pin duration.' },
      { id:'hound_pounce', branch:'mystic', icon:'🐾', nameZh:'逐影扑杀', nameEn:'Shadow-Chasing Pounce', baseCost:14, step:2, prereq:'hound_bite', effects:{ houndCooldown:.008 }, descZh:'每重：号令哮天犬冷却缩短 0.8%。', descEn:'Per rank: Xiaotianquan command cooldown is 0.8% shorter.' },
      { id:'thunderstep', branch:'mystic', icon:'⚡', nameZh:'金光雷遁', nameEn:'Golden-Light Thunderstep', baseCost:17, step:3, prereq:'hound_pounce', effects:{ speed:.003, dashDamage:.02 }, descZh:'每重：移动速度 +0.3%，雷遁路径伤害 +2%。', descEn:'Per rank: +0.3% movement speed and +2% Thunderstep trail damage.' },
      { id:'divine_armor', branch:'mystic', icon:'🛡️', nameZh:'银甲神将', nameEn:'Silver-Armored Divine General', baseCost:20, step:3, prereq:'thunderstep', effects:{ armor:.8, maxHp:.75 }, descZh:'每重：常驻护甲 +0.8，最大气血 +0.75。', descEn:'Per rank: +0.8 armor and +0.75 maximum Health.' },
      { id:'manifestation', branch:'mystic', icon:'👤', nameZh:'八九玄功法相', nameEn:'Eight-Nine Mysteries Manifestation', baseCost:23, step:3, prereq:'divine_armor', effects:{ manifestDuration:.12, manifestCooldown:.006, manifestDamage:.012 }, descZh:'每重：法相持续 +0.12 秒、伤害 +1.2%、冷却缩短 0.6%。', descEn:'Per rank: +0.12s duration, +1.2% damage, and 0.6% shorter cooldown.' },
      { id:'clear_origin', branch:'mystic', icon:'☯️', nameZh:'清源妙道真君', nameEn:'Lord of Clear-Origin Mysteries', baseCost:28, step:4, prereq:'manifestation', effects:{ damage:.004, qiRegen:.01, houndDamage:.008 }, descZh:'每重：全部伤害 +0.4%，真气回复 +0.01/秒，神犬伤害 +0.8%。', descEn:'Per rank: +0.4% all damage, +0.01 Qi/s, and +0.8% hound damage.' }
    ].map(skill => ({ ...skill, maxRank:20 }));

    function getErlangSkillEffects() {
      const totals = {};
      ERLANG_SKILLS.forEach(skill => {
        const rank = Math.min(skill.maxRank, Math.max(0, erlangSkillRanks?.[skill.id] || 0));
        Object.entries(skill.effects || {}).forEach(([key, value]) => { totals[key] = (totals[key] || 0) + value * rank; });
      });
      totals.eyeChains = Math.floor((totals.eyeChainProgress || 0));
      return totals;
    }

    const SKILL_BRANCH_EN = {
      core: 'Primordial Root', dragon: 'Azure Dragon · Storm-Tide', tiger: 'White Tiger · Metal Fury',
      roc: 'Golden Roc · Skybreaker', ape: 'Titan Ape · Mountain Shatter', tortoise: 'Black Tortoise · Nether Shell'
    };
    const SKILL_EN_NAMES = {
      root: 'Primordial Stone · First Awakening',
      form_dragon: 'Azure Dragon Form · Storm-Tide Dominion', dragon_dive: 'Abyss Dive', dragon_wind: 'Summon Wind', dragon_rain: 'Call Rain', dragon_scale: 'Reverse Dragon Scales', dragon_claw: 'Thunder Dragon Claw', dragon_breath: 'Nine-Heaven Dragon Breath', dragon_sea: 'Great Sage Who Overturns the Sea', dragon_thunder: 'Thunder Palm Seal', dragon_storm: 'Thunderous Rampage', dragon_tsunami: 'Heaven-Rending Tsunami', dragon_subdue: 'Dragon-Subduing Breaker', dragon_soar: 'Celestial Dragon Soar', dragon_water_walk: 'Water-Walking Dragon', dragon_water_know: 'Mysteries of Water',
      form_tiger: 'White Tiger Form · Metal Battle Fury', tiger_pounce: 'Crouching-Tiger Pounce', tiger_claws: 'Rending Fury Claws', tiger_roar: 'Mountain-Shaking Roar', tiger_frenzy: 'Blood-Drinking Frenzy', tiger_bleed: 'Metal-Soul Rend', tiger_slay: 'Demon Slayer', tiger_speed: 'Gale Fury', tiger_crit: 'Fatal Strike', tiger_bloodlust: 'Mystic Bloodlust', tiger_execute: 'White Tiger Execution', tiger_spirit: 'Fury Star Descends', tiger_bite: 'Blade-Eating Fury', tiger_sword: 'Sword-Spirit Release',
      form_roc: 'Golden Roc Form · Skybreaker Speed', roc_fly: 'Ride the Wind', roc_feather: 'Sky-Soaring Feather Blades', roc_dash: 'Ninety-Thousand-Li Escape', roc_vortex: 'Celestial Gale Vortex', roc_sky: 'Soar Beyond the Clouds', roc_talon: 'Heaven-Rending Talons', roc_cyclone: 'Ten-Thousand-Blade Cyclone', roc_sight: 'Truth-Piercing Eagle Eye', roc_solar: 'Sun-Chasing Radiance', roc_sonic: 'Sonic Skybreak', roc_supreme: 'Supreme Golden Wings', roc_feather_burst: 'Ten-Thousand Feathers', roc_sky_scout: 'Survey Heaven and Earth',
      form_ape: 'Titan Ape Form · World-Shaking Colossus', ape_might: 'Mountain-Uprooting Might', ape_quake: 'Earth-and-Heaven Quake', ape_mountain: 'Shoulder the Mountain', ape_titan: 'Ten-Thousand-Zhang Body', ape_stone: 'Stone-Splitting Impact', ape_smash: 'Pillar-of-Heaven Smash', ape_fist: 'Mountain-Breaking Fist', ape_armor: 'Diamond Immortal Body', ape_roar: 'Great Sage’s Roar', ape_shockwave: 'Chaos Shockwave', ape_overlord: 'World-Shaking Overlord', ape_stone_boil: 'Stone-Alchemy Bounty', ape_spit_flame: 'Heaven-Burning Flame Breath',
      form_tortoise: 'Black Tortoise Form · Nether Shell', tort_shell: 'Diamond Shell', tort_spike: 'Earthly Thorns', tort_guard: 'Radiant Guard', tort_flow: 'Return to Origin', tort_regen: 'Fasting Longevity', tort_abyss: 'Nine-Springs Abyss', tort_reflect: 'Force-Reversing Mirror', tort_immortal: 'Ninefold Rebirth', tort_shield: 'Life-Locking Ward', tort_whirlpool: 'Moon-Water Blades', tort_supreme: 'Undying Black Tortoise', tort_cover_sun: 'Eclipse Calamity', tort_renew_head: 'Perfect Rebirth'
    };
    const SKILL_EN_DESCRIPTIONS = {
      root: 'Born from a celestial stone atop Flower-Fruit Mountain. Provides balanced starting attributes.',
      form_dragon: 'Control form: claw strikes chain storm lightning and hasten Qi recovery. Strong crowd control with moderate single-target burst. Press [R] to transform.',
      form_tiger: 'Hunting form: greatly improves attack speed, lunges, and critical strikes. Claws inflict bleeding. Strongest close-range burst. Press [R] to transform.',
      form_roc: 'Skirmisher form: gains extra dodges, faster recharge, and long piercing wind blades. Best mobility. Press [R] to transform.',
      form_ape: 'Armored form: slow, crushing blows deal huge damage, knockdown, and earthquakes while resisting control. Press [R] to transform.',
      form_tortoise: 'Guardian form: heavy damage reduction, healing, and a slowing water ring. Lowest burst, highest survival. Press [R] to transform.'
    };

    function getSkillDisplayName(node) {
      return gameState.language === 'en' ? (SKILL_EN_NAMES[node.id] || node.name) : node.name;
    }

    function getSkillDisplayDescription(node) {
      if (gameState.language !== 'en') {
        if (node.id === 'root') return node.desc;
        if (node.isForm) return node.desc;
        const branchName = {dragon:'苍龙',tiger:'白虎',roc:'大鹏',ape:'巨猿',tortoise:'玄武'}[node.branch] || '对应真身';
        const formOnlyDescription = node.desc.replaceAll('永久', '真身期间');
        return `【仅在${branchName}变身期间生效】${formOnlyDescription}`;
      }
      if (SKILL_EN_DESCRIPTIONS[node.id]) return SKILL_EN_DESCRIPTIONS[node.id];
      const contract = FORM_SKILL_RUNTIME_CONTRACTS[node.id];
      const formName = SKILL_BRANCH_EN[node.branch] || node.branch;
      const hookText = {
        activation:'when the transformation begins', normalAttack:'through transformed normal attacks', special:'through the transformed flying-staff special',
        spell:'through the transformed E spell', dash:'through transformed dodge/dash', defense:'when the transformed body is struck',
        kill:'when the transformed form defeats an enemy', aura:'continuously while the transformation is active'
      }[contract?.hook] || 'during transformed combat';
      return `${getSkillDisplayName(node)} is active only in ${formName}, ${hookText}. Each rank strengthens its real combat effect and animated cue; it grants no generic stats outside that transformation.`;
    }

    function sanitizeRankMap(value) {
      if (!value || typeof value !== 'object' || Array.isArray(value)) return {};
      const clean = {};
      Object.entries(value).forEach(([key, rank]) => {
        if (typeof key === 'string' && Number.isFinite(rank)) clean[key] = Math.max(0, Math.floor(rank));
      });
      return clean;
    }

    function loadMetaProgress() {
      try {
        const current = JSON.parse(safeStorageGetItem(META_SAVE_KEY) || 'null');
        if (current && typeof current === 'object') return current;
        const legacy = JSON.parse(safeStorageGetItem(LEGACY_META_SAVE_KEY) || '{}');
        if (legacy && typeof legacy === 'object') {
          return {
            version: 3,
            currencies: { ashes: legacy.ashes || 0 },
            skills: { treeRanks: legacy.skillTreeRanks || {}, passives: {} },
            equippedForm: legacy.activeTransformationForm || 'dragon'
          };
        }
        return {};
      } catch (_) {
        return {};
      }
    }

    const savedMetaProgress = loadMetaProgress();
    const savedAshes = savedMetaProgress.currencies?.ashes ?? savedMetaProgress.ashes;
    if (Number.isFinite(savedAshes)) gameState.ashes = Math.max(0, Math.floor(savedAshes));
    let campaignUnlocks = {
      journeyComplete: !!(savedMetaProgress.unlocks?.journeyComplete || savedMetaProgress.unlocks?.volume2Complete),
      fengshenComplete: !!savedMetaProgress.unlocks?.fengshenComplete,
      newGamePlus: !!savedMetaProgress.unlocks?.newGamePlus,
      erlangPlayable: !!savedMetaProgress.unlocks?.erlangPlayable,
      ngPlusClears: Math.max(0, Math.floor(savedMetaProgress.unlocks?.ngPlusClears || 0))
    };
    let skillTreeRanks = sanitizeRankMap(savedMetaProgress.skills?.treeRanks || savedMetaProgress.skillTreeRanks || { root: 1, form_dragon: 1 });
    let passiveSkillRanks = sanitizeRankMap(savedMetaProgress.skills?.passives || savedMetaProgress.passiveSkillRanks || {});
    let erlangSkillRanks = sanitizeRankMap(savedMetaProgress.skills?.erlang || {});
    alignmentScore = Math.max(-100, Math.min(100, Math.round(savedMetaProgress.alignment?.score || 0)));
    alignmentSkillRanks = sanitizeRankMap(savedMetaProgress.alignment?.skillRanks || {});
    let activeTransformationForm = savedMetaProgress.equippedForm || savedMetaProgress.activeTransformationForm || 'dragon';
    gameState.playableHero = savedMetaProgress.equippedHero === 'erlang' && campaignUnlocks.erlangPlayable ? 'erlang' : 'wukong';
    gameState.campaignRoute = gameState.playableHero === 'erlang' ? 'fengshen' : 'journey';

    function saveMetaProgress() {
      try {
        const snapshot = {
          version: 6,
          updatedAt: new Date().toISOString(),
          currencies: { ashes: Math.max(0, Math.floor(gameState.ashes)) },
          skills: { treeRanks: { ...skillTreeRanks }, passives: { ...passiveSkillRanks }, erlang: { ...erlangSkillRanks } },
          alignment: { score: alignmentScore, skillRanks: { ...alignmentSkillRanks } },
          equippedForm: activeTransformationForm,
          equippedHero: gameState.playableHero,
          unlocks: { ...campaignUnlocks }
        };
        safeStorageSetItem(META_SAVE_KEY, JSON.stringify(snapshot));
        const saveStatus = document.getElementById('meta-save-status');
        if (saveStatus) saveStatus.innerText = gameState.language === 'en'
          ? `Saved in browser ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`
          : `浏览器已保存 ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
        return snapshot;
      } catch (_) {
        const saveStatus = document.getElementById('meta-save-status');
        if (saveStatus) { saveStatus.innerText = gameState.language === 'en' ? 'Save failed' : '保存失败'; saveStatus.style.color = '#fca5a5'; }
        return null;
      }
    }

    function selectPlayableHero(heroId) {
      if (heroId === 'erlang' && !campaignUnlocks.erlangPlayable) return false;
      gameState.playableHero = heroId === 'erlang' ? 'erlang' : 'wukong';
      gameState.campaignRoute = gameState.playableHero === 'erlang' ? 'fengshen' : 'journey';
      player.applyMetaUpgrades();
      player.hp = Math.min(player.hp, player.maxHp);
      player.qi = Math.min(player.qi, player.maxQi);
      refreshTitleUnlocks();
      updateHeroInterface();
      saveMetaProgress();
      return true;
    }

    function refreshTitleUnlocks() {
      const erlangButton = document.getElementById('hero-erlang-btn');
      const ngPlusButton = document.getElementById('start-ngplus-btn');
      const startButton = document.getElementById('start-game-btn');
      const freshButton = document.getElementById('start-fresh-btn');
      const checkpointStatus = document.getElementById('run-checkpoint-status');
      const checkpoint = loadRunCheckpoint();
      if (erlangButton) {
        erlangButton.disabled = !campaignUnlocks.erlangPlayable;
        erlangButton.innerHTML = campaignUnlocks.erlangPlayable
          ? `${uiText('👁 二郎显圣真君 · 杨戬', '👁 Erlang Shen · Yang Jian')}<span>${uiText('三尖两刃枪 · 天眼 · 哮天犬', 'Three-Pointed Spear · Third Eye · Xiaotianquan')}</span>`
          : `${uiText('👁 二郎神 · 尚未解锁', '👁 Erlang Shen · Locked')}<span>${uiText('通关完整百章西游后解锁天眼、三尖枪与哮天犬', 'Clear the complete 100-chapter journey to unlock the Third Eye, three-pointed spear, and Xiaotianquan.')}</span>`;
      }
      if (ngPlusButton) {
        ngPlusButton.disabled = !campaignUnlocks.newGamePlus;
        ngPlusButton.innerText = uiText('✦ 新游戏+ · 敌血 ×7 · 敌伤 ×3', '✦ New Game+ · Enemy HP ×7 · Damage ×3');
        ngPlusButton.title = campaignUnlocks.newGamePlus
          ? uiText('天镜强化：二十种全新妖将与神兵加入百章轮换。', 'Celestial-Mirror difficulty: twenty newly animated enemy types join the 100-chapter rotation.')
          : uiText('通关完整百章西游后解锁', 'Clear the complete 100-chapter journey to unlock');
      }
      const selectedErlangRoute = gameState.playableHero === 'erlang';
      if (startButton) startButton.innerText = checkpoint
        ? uiText(`继续${checkpoint.route === 'fengshen' ? '二郎封神录' : '西游'} · 第 ${checkpoint.chapter} 章`, `Continue ${checkpoint.route === 'fengshen' ? 'Erlang Fengshen Chronicle' : 'Journey'} · Chapter ${checkpoint.chapter}`)
        : (selectedErlangRoute ? uiText('二郎封神录 · 第 1–38 章', 'Begin Erlang Fengshen Chronicle (1–38)') : uiText('西游全篇 · 第 1–100 章', 'Begin Complete Journey (1–100)'));
      if (freshButton) freshButton.hidden = !checkpoint;
      if (checkpointStatus) checkpointStatus.innerText = checkpoint
        ? uiText(`💾 浏览器存档：${checkpoint.route === 'fengshen' ? '二郎封神录' : '西游'}第 ${checkpoint.chapter} 章开头`, `💾 Browser save: ${checkpoint.route === 'fengshen' ? 'Erlang Fengshen Chronicle' : 'Journey'}, Chapter ${checkpoint.chapter}`)
        : uiText('按 [Esc] 可在战斗中打开菜单并保存退出', 'Press [Esc] during play to open the menu and Save & Exit');
      document.getElementById('hero-wukong-btn')?.classList.toggle('active', gameState.playableHero === 'wukong');
      erlangButton?.classList.toggle('active', gameState.playableHero === 'erlang');
      updateTitleKarmaPresentation();
    }

    function updateHeroInterface() {
      const isErlang = gameState.playableHero === 'erlang';
      const heroName = document.querySelector('.hero-name');
      if (heroName) heroName.innerText = isErlang
        ? uiText('灌江口 · 二郎显圣真君', 'Erlang Shen · Lord of Guanjiang')
        : uiText('齐天大圣 · 孙悟空', 'Great Sage Equal to Heaven · Sun Wukong');
      const weaponTitle = document.getElementById('weapon-style-title');
      if (weaponTitle) weaponTitle.innerText = isErlang
        ? uiText('三尖两刃枪 · 天眼神锋', 'Three-Pointed Spear · Heaven-Eye Edge')
        : (player.hasRuyiStaff ? uiText('如意金箍棒 · 一万三千五百斤', 'Ruyi Jingu Bang · 13,500 jin') : uiText('花果山石棍 · 尚未取得定海神珍', 'Flower-Fruit Stone Staff · Ruyi Staff not yet claimed'));
      const setSlot = (id, label, boon) => {
        const slot = document.getElementById(id);
        if (!slot) return;
        const labelEl = slot.querySelector('.slot-label');
        const boonEl = slot.querySelector('.slot-boon');
        if (labelEl) labelEl.innerText = label;
        if (boonEl) boonEl.innerText = boon;
      };
      if (isErlang) {
        setSlot('slot-attack', uiText('三尖枪三连势', 'Three-Pointed Spear Chain'), uiText('突刺 · 回斩 · 天雷贯穿', 'Thrust · Sweep · Thunder Pierce'));
        setSlot('slot-special', uiText('哮天犬 / 天眼枪', 'Xiaotianquan / Third Eye'), uiText('右键神雷跃击 · Q贯穿', 'RMB Thunder Slam · Q Pierce'));
        setSlot('slot-cast', uiText('灌江口审判阵', 'Guanjiang Judgment Array'), uiText('四重天雷 · 审判印', 'Four Thunder Pulses · Judgment Mark'));
        setSlot('slot-dash', uiText('金光雷遁', 'Golden-Light Thunderstep'), uiText('穿敌留雷', 'Lightning Trail'));
        setSlot('slot-hex', uiText('清源妙道法相', 'Clear-Origin Manifestation'), uiText('天眼 · 神将甲 · 犬袭强化', 'Third Eye · Divine Armor · Hound Boost'));
      } else {
        setSlot('slot-attack', uiText('金箍混合棍法', 'Mixed Ruyi Staff Arts'), uiText('按 [C] 查看连招', 'Press [C] for Combos'));
        setSlot('slot-special', uiText('如意飞棒', 'Flying Ruyi Staff'), uiText('去回双击', 'Out-and-Back Double Hit'));
        setSlot('slot-cast', uiText('吹毛成兵', 'Hair-Clone Spell'), uiText('猴王分身', 'Monkey-King Clones'));
        setSlot('slot-dash', uiText('筋斗云遁', 'Somersault-Cloud Dash'), uiText('浮光掠影', 'Lightstep Afterimage'));
      }
      const touchSpecial = document.querySelector('[data-touch-action="special"]');
      if (touchSpecial) touchSpecial.innerText = isErlang ? uiText('犬', 'Dog') : uiText('飞', 'Throw');
      const comboHudButton = document.getElementById('combo-hud-btn');
      if (comboHudButton) comboHudButton.innerText = isErlang ? uiText('👁 [C] 二郎枪连招谱', '👁 [C] Erlang Combo Manual') : uiText('⚔ [C] 金箍棒连招谱', '⚔ [C] Ruyi Combo Manual');
      const comboTitleButton = document.getElementById('combo-title-btn');
      if (comboTitleButton) comboTitleButton.innerText = isErlang ? uiText('👁 查看二郎枪连招谱', '👁 View Erlang Combo Manual') : uiText('⚔ 查看金箍棒连招谱', '⚔ View Ruyi Combo Manual');
      const trainingTitleButton = document.getElementById('training-title-btn');
      if (trainingTitleButton) trainingTitleButton.innerText = isErlang ? uiText('二郎封神技能', 'Erlang Skills') : uiText('七十二变', '72 Transformations');
      const trainingHudButton = document.getElementById('training-hud-btn');
      if (trainingHudButton) trainingHudButton.innerText = isErlang ? uiText('👁 二郎封神修行树', '👁 Erlang Fengshen Skill Tree') : uiText('📜 七十二变地煞树', '📜 72 Transformations Tree');
      const trainingGameoverButton = document.getElementById('training-gameover-btn');
      if (trainingGameoverButton) trainingGameoverButton.innerText = isErlang ? uiText('👁 修习二郎封神神通', '👁 Train Erlang Fengshen Skills') : uiText('📜 领悟地煞七十二变神木树', '📜 Train 72 Transformations');
      const alignmentHudButton = document.getElementById('alignment-hud-btn');
      if (alignmentHudButton) alignmentHudButton.style.display = isErlang ? 'none' : '';
    }

    let metaSaveTimer = null;
    function scheduleMetaProgressSave() {
      window.clearTimeout(metaSaveTimer);
      metaSaveTimer = window.setTimeout(saveMetaProgress, 350);
    }
    window.addEventListener('pagehide', saveMetaProgress);

    function getPermanentPassiveRank(id) {
      return Math.max(0, passiveSkillRanks[id] || 0);
    }

    function getPermanentPassiveCost(passive, rank = getPermanentPassiveRank(passive.id)) {
      return passive.baseCost + passive.costStep * rank;
    }

    let alignmentReturnWasPaused = true;
    function getAlignmentSkillRank(id) {
      return Math.max(0, alignmentSkillRanks[id] || 0);
    }

    function getAlignmentSkillCost(skill, rank = getAlignmentSkillRank(skill.id)) {
      // Every karma discipline now spans 20 ranks. Neutrality keeps a gentler
      // curve; the more potent pure-path ranks demand more Merit as they deepen.
      return skill.cost + rank * (skill.path === 'neutral' ? 1 : 3);
    }

    function alignmentPrerequisitesMet(skill) {
      return (skill.prereq || []).every(id => getAlignmentSkillRank(id) > 0 && isAlignmentSkillActive(id));
    }

    function getAlignmentRequirementText(skill) {
      if (skill.path === 'good') return uiText(`善念 ≥ +${skill.threshold}`, `Good ≥ +${skill.threshold}`);
      if (skill.path === 'evil') return uiText(`恶念 ≤ −${skill.threshold}`, `Evil ≤ −${skill.threshold}`);
      return uiText(`因果介于 −${skill.maxAbs} 与 +${skill.maxAbs}`, `Balance between −${skill.maxAbs} and +${skill.maxAbs}`);
    }

    function initAlignmentSystem() {
      ALIGNMENT_SKILLS.forEach(skill => {
        alignmentSkillRanks[skill.id] = Math.min(skill.maxRank, getAlignmentSkillRank(skill.id));
      });
      const sheet = loadedImages['wukong_alignment_portraits'];
      document.querySelectorAll('.alignment-portrait').forEach(portrait => {
        if (sheet?.src) portrait.style.backgroundImage = `url(${sheet.src})`;
      });
      updateAlignmentHUD();
    }

    function openAlignmentTree() {
      alignmentReturnWasPaused = gameState.isPaused;
      gameState.isPaused = true;
      gameState.mouse.isDown = false;
      renderAlignmentSkillTree();
      const modal = document.getElementById('alignment-tree-modal');
      modal.style.display = 'flex';
      modal.querySelector('button:not([disabled])')?.focus();
    }

    function closeAlignmentTree() {
      document.getElementById('alignment-tree-modal').style.display = 'none';
      saveMetaProgress();
      gameState.isPaused = alignmentReturnWasPaused || !gameState.hasStarted || gameState.dialogueActive || gameState.rewardSelectionActive || gameState.bossOutcomeActive;
      document.getElementById('gameCanvas')?.focus();
    }

    function investAlignmentSkill(id) {
      const skill = ALIGNMENT_SKILLS.find(item => item.id === id);
      if (!skill) return;
      const rank = getAlignmentSkillRank(id);
      const cost = getAlignmentSkillCost(skill, rank);
      if (rank >= skill.maxRank || !alignmentThresholdMet(skill) || !alignmentPrerequisitesMet(skill) || gameState.ashes < cost) return;
      gameState.ashes -= cost;
      alignmentSkillRanks[id] = rank + 1;
      player.applyMetaUpgrades();
      player.hp = Math.min(player.hp, player.maxHp);
      player.qi = Math.min(player.qi, player.maxQi);
      player.armor = Math.max(player.armor, player.baseArmor || 0);
      saveMetaProgress();
      sound.playJadeChime();
      renderAlignmentSkillTree();
      updateHUD();
      captureChapterStartCheckpoint();
    }

    function renderAlignmentSkillTree() {
      const path = getAlignmentPath();
      const portrait = document.getElementById('alignment-tree-portrait');
      portrait.className = `alignment-portrait ${path}`;
      const sheet = loadedImages['wukong_alignment_portraits'];
      if (sheet?.src) portrait.style.backgroundImage = `url(${sheet.src})`;
      const pathName = path === 'good' ? uiText('善道', 'Good') : (path === 'evil' ? uiText('恶道', 'Evil') : uiText('中道', 'Neutral'));
      document.getElementById('alignment-tree-title').innerText = uiText('☯ 悟空因果道 · 善、恶、中道神通树', '☯ Wukong’s Karmic Path · Good, Neutral, and Evil Trees');
      document.getElementById('alignment-tree-score').innerText = uiText(`因果平衡 ${alignmentScore > 0 ? '+' : ''}${alignmentScore} · ${pathName}`, `Alignment ${alignmentScore > 0 ? '+' : ''}${alignmentScore} · ${pathName}`);
      document.getElementById('alignment-tree-help').innerText = uiText(
        '每位首领败阵后只能选择非致死结局。善 +1、恶 −1；跨越门槛会令不再满足前提的神通休眠，但永久等级不会丢失。',
        'Every subdued boss ends in a nonlethal choice. Good gives +1 and Evil gives −1. Crossing a threshold makes ineligible skills dormant, but their permanent ranks are never deleted.'
      );
      document.getElementById('alignment-tree-merit').innerText = uiText(`✨ 功德灵砂：${gameState.ashes}`, `✨ Merit: ${gameState.ashes}`);
      const pathMeta = {
        good: [uiText('善道 · 护世圣法', 'GOOD · Sacred Protection'), uiText('护甲、减伤、圣光、复苏', 'Armor · Defense · Holy Light · Renewal')],
        neutral: [uiText('中道 · 阴阳二十重', 'NEUTRAL · Twentyfold Yin-Yang'), uiText('20级精修 · 攻守切换、双相冲击与里程碑神通', '20-rank mastery · adaptive defense, dual-aspect bursts, and milestone powers')],
        evil: [uiText('恶道 · 掠炁魔功', 'EVIL · Zhen-Qi Predation'), uiText('伤害、攻速、吸血、幽冥爆发', 'Damage · Speed · Life Leech · Void Bursts')]
      };
      document.getElementById('alignment-skill-grid').innerHTML = ['good','neutral','evil'].map(branch => {
        const skills = ALIGNMENT_SKILLS.filter(skill => skill.path === branch);
        return `<section class="alignment-path-column ${branch}"><div class="alignment-path-title">${pathMeta[branch][0]}<div style="font:600 11px var(--font-body);color:#94a3b8;margin-top:2px">${pathMeta[branch][1]}</div></div>${skills.map(skill => {
          const rank = getAlignmentSkillRank(skill.id);
          const active = rank > 0 && isAlignmentSkillActive(skill);
          const dormant = rank > 0 && !active;
          const prereqs = alignmentPrerequisitesMet(skill);
          const threshold = alignmentThresholdMet(skill);
          const cost = getAlignmentSkillCost(skill, rank);
          const maxed = rank >= skill.maxRank;
          const disabled = maxed || !threshold || !prereqs || gameState.ashes < cost;
          const status = dormant ? uiText('已拥有 · 当前休眠', 'Owned · Currently Dormant') : (active ? uiText('已激活', 'Active') : (!threshold ? uiText('因果门槛未满足', 'Alignment threshold not met') : (!prereqs ? uiText('前置神通未激活', 'Prerequisite inactive') : uiText('可参悟', 'Ready to learn'))));
          const buttonText = maxed ? uiText('已圆满', 'Complete') : uiText(`参悟 1 级 · ${cost} 功德`, `Invest 1 Rank · ${cost} Merit`);
          const rankTrack = `<div class="neutral-rank-track ${branch}" role="progressbar" aria-label="${gameState.language === 'en' ? `${pathMeta[branch][0]} skill rank` : `${pathMeta[branch][0]}神通等级`}" aria-valuemin="0" aria-valuemax="${skill.maxRank}" aria-valuenow="${rank}"><i style="width:${rank / skill.maxRank * 100}%"></i></div><div class="neutral-rank-milestones"><span>1</span><span>5</span><span>10</span><span>15</span><span>20</span></div>`;
          return `<article class="alignment-skill ${active ? 'active' : ''} ${dormant ? 'dormant' : ''} ${!rank && disabled ? 'locked' : ''}">
            <div class="alignment-skill-name">${skill.icon} ${gameState.language === 'en' ? skill.nameEn : skill.nameZh}</div>
            <div class="alignment-skill-meta">Lv.${rank}/${skill.maxRank} · ${getAlignmentRequirementText(skill)} · ${status}</div>
            ${rankTrack}
            <div class="alignment-skill-desc">${gameState.language === 'en' ? skill.descEn : skill.descZh}</div>
            <button class="btn-hud" type="button" ${disabled ? 'disabled' : ''} onclick="investAlignmentSkill('${skill.id}')">${buttonText}</button>
          </article>`;
        }).join('')}</section>`;
      }).join('');
    }

    function updateAlignmentHUD() {
      const marker = document.getElementById('alignment-marker');
      if (!marker) return;
      const goodWidth = Math.max(0, alignmentScore) / 2;
      const evilWidth = Math.max(0, -alignmentScore) / 2;
      document.getElementById('alignment-good-fill').style.width = `${goodWidth}%`;
      document.getElementById('alignment-evil-fill').style.width = `${evilWidth}%`;
      marker.style.left = `${50 + alignmentScore / 2}%`;
      const path = getAlignmentPath();
      const pathName = path === 'good' ? uiText('善道', 'Good') : (path === 'evil' ? uiText('恶道', 'Evil') : uiText('中道', 'Neutral'));
      document.getElementById('alignment-readout').innerText = uiText(`${pathName} · 因果 ${alignmentScore > 0 ? '+' : ''}${alignmentScore}`, `${pathName} · ${alignmentScore > 0 ? '+' : ''}${alignmentScore}`);
      const labels = document.querySelector('#alignment-meter .alignment-labels');
      if (labels) labels.innerHTML = gameState.language === 'en' ? '<span>EVIL −100</span><span>NEUTRAL 0</span><span>GOOD +100</span>' : '<span>恶 −100</span><span>中道 0</span><span>善 +100</span>';
      document.getElementById('alignment-meter').setAttribute('aria-label', uiText('善恶中道因果平衡与技能树', 'Good, neutral, and evil alignment balance and skill tree'));
    }

    function getErlangSkillRank(id) {
      return Math.max(0, Math.min(20, erlangSkillRanks[id] || 0));
    }

    function getErlangSkillCost(skill, rank = getErlangSkillRank(skill.id)) {
      return skill.baseCost + skill.step * rank;
    }

    function erlangSkillPrerequisiteMet(skill) {
      return !skill.prereq || getErlangSkillRank(skill.prereq) >= 5;
    }

    function getErlangCurrentEffectText(skill, rank) {
      if (!rank) return uiText('当前：尚未修习', 'Current: not learned');
      const parts = Object.entries(skill.effects || {}).map(([key, value]) => {
        const total = value * rank;
        const labels = {
          crit:['暴击率','Critical chance'], eyeDamage:['天眼枪伤害','Lance damage'], eyeRange:['天眼枪射程','Lance range'],
          eyeChainProgress:['雷链进度','Lightning-chain progress'], markDamage:['标记增伤','Brand damage'], maxQi:['最大真气','Maximum Qi'],
          qiRegen:['真气回复/秒','Qi regeneration/s'], arrayDamage:['审判阵伤害','Array damage'], arrayRadius:['审判阵半径','Array radius'],
          arrayDuration:['审判阵持续','Array duration'], bossDamage:['首领伤害','Boss damage'], eyeWidth:['天眼枪宽度','Lance width'],
          spearDamage:['枪术伤害','Spear damage'], attackSpeed:['攻击速度','Attack speed'], spearReach:['枪术范围','Spear reach'],
          launchDamage:['升月伤害','Rise damage'], launchForce:['挑飞力度','Launch force'], spinDamage:['天轮伤害','Wheel damage'],
          spinRadius:['天轮半径','Wheel radius'], armorBreak:['无视护甲','Armor ignored'], comboDamage:['连招伤害','Combo damage'],
          comboWindow:['输入宽限','Input grace'], houndDamage:['神犬伤害','Hound damage'], houndStun:['神犬定身','Hound pin'],
          houndCooldown:['神犬冷却缩减','Hound cooldown reduction'], speed:['移动速度','Move speed'], dashDamage:['雷遁伤害','Thunderstep damage'],
          armor:['护甲','Armor'], maxHp:['最大气血','Maximum Health'], manifestDuration:['法相持续','Manifest duration'],
          manifestCooldown:['法相冷却缩减','Manifest cooldown reduction'], manifestDamage:['法相伤害','Manifest damage'], damage:['全部伤害','All damage']
        };
        const percentKeys = new Set(['crit','eyeDamage','markDamage','arrayDamage','bossDamage','spearDamage','attackSpeed','spearReach','launchDamage','spinDamage','armorBreak','comboDamage','houndDamage','houndCooldown','speed','dashDamage','manifestCooldown','manifestDamage','damage']);
        const secondsKeys = new Set(['arrayDuration','comboWindow','houndStun','manifestDuration']);
        const label = labels[key]?.[gameState.language === 'en' ? 1 : 0] || key;
        const valueText = percentKeys.has(key) ? `+${(total * 100).toFixed(1)}%` : (secondsKeys.has(key) ? `+${total.toFixed(2)}s` : `+${Number(total.toFixed(2))}`);
        return `${label} ${valueText}`;
      });
      return `${uiText('当前', 'Current')}: ${parts.join(' · ')}`;
    }

    function renderErlangSkillTree() {
      const grid = document.getElementById('erlang-skill-grid');
      if (!grid) return;
      document.getElementById('erlang-tree-title').innerText = uiText('👁 清源妙道 · 二郎封神修行', '👁 Clear-Origin Mysteries · Erlang Fengshen Skills');
      document.getElementById('erlang-tree-subtitle').innerText = uiText('天眼、三尖两刃枪、哮天犬与八九玄功 · 每项永久修至 20 重', 'Third Eye, three-pointed spear, Xiaotianquan, and Eight-Nine Mysteries · 20 permanent ranks each');
      document.getElementById('erlang-tree-merit').innerText = uiText(`✨ 功德灵砂：${gameState.ashes}`, `✨ Merit: ${gameState.ashes}`);
      document.getElementById('erlang-tree-close').innerText = uiText('保存修行 · 返回', 'Save Training · Return');
      const branches = {
        eye:[uiText('👁 天眼明断', '👁 THIRD EYE VERDICT'), uiText('贯穿、雷链、标记与审判阵', 'Piercing · chains · brands · judgment array')],
        spear:[uiText('🔱 三尖枪道', '🔱 THREE-POINTED SPEAR'), uiText('枪伤、攻速、挑飞与周身天轮', 'Damage · tempo · launch · radial wheel')],
        mystic:[uiText('🐕 八九玄功', '🐕 EIGHT-NINE MYSTERIES'), uiText('哮天犬、雷遁、银甲与清源法相', 'Hound · Thunderstep · armor · manifestation')]
      };
      grid.innerHTML = Object.entries(branches).map(([branch, meta]) => `<section class="erlang-branch ${branch}">
        <div class="erlang-branch-title">${meta[0]}<small>${meta[1]}</small></div>
        ${ERLANG_SKILLS.filter(skill => skill.branch === branch).map(skill => {
          const rank = getErlangSkillRank(skill.id);
          const maxed = rank >= skill.maxRank;
          const prereqMet = erlangSkillPrerequisiteMet(skill);
          const cost = getErlangSkillCost(skill, rank);
          const disabled = maxed || !prereqMet || gameState.ashes < cost;
          const prereq = skill.prereq ? ERLANG_SKILLS.find(item => item.id === skill.prereq) : null;
          const status = maxed ? uiText('已圆满', 'Complete') : (!prereqMet ? uiText(`需 ${prereq?.nameZh || ''} Lv.5`, `Requires ${prereq?.nameEn || ''} Lv.5`) : uiText('可修习', 'Ready'));
          return `<article class="erlang-skill-card ${rank ? 'active' : ''} ${!prereqMet ? 'locked' : ''}">
            <div class="erlang-skill-name">${skill.icon} ${gameState.language === 'en' ? skill.nameEn : skill.nameZh}</div>
            <div class="erlang-skill-meta">Lv.${rank}/20 · ${status}</div>
            <div class="erlang-rank-track" role="progressbar" aria-valuemin="0" aria-valuemax="20" aria-valuenow="${rank}"><i style="width:${rank * 5}%"></i></div>
            <div class="erlang-skill-desc">${gameState.language === 'en' ? skill.descEn : skill.descZh}</div>
            <div class="erlang-skill-current">${getErlangCurrentEffectText(skill, rank)}</div>
            <button class="btn-hud" type="button" ${disabled ? 'disabled' : ''} onclick="investErlangSkill('${skill.id}')">${maxed ? uiText('已圆满', 'Complete') : uiText(`修习 1 重 · ${cost} 功德`, `Invest 1 Rank · ${cost} Merit`)}</button>
          </article>`;
        }).join('')}</section>`).join('');
    }

    function investErlangSkill(id) {
      const skill = ERLANG_SKILLS.find(item => item.id === id);
      if (!skill) return;
      const rank = getErlangSkillRank(id);
      const cost = getErlangSkillCost(skill, rank);
      if (rank >= 20 || !erlangSkillPrerequisiteMet(skill) || gameState.ashes < cost) return;
      gameState.ashes -= cost;
      erlangSkillRanks[id] = rank + 1;
      player.applyMetaUpgrades();
      player.hp = Math.min(player.maxHp, player.hp + Math.max(0, player.maxHp - player.hp) * .05);
      player.qi = Math.min(player.maxQi, player.qi + 2);
      saveMetaProgress();
      renderErlangSkillTree();
      updateHUD();
      sound.playJadeChime();
      captureChapterStartCheckpoint();
    }

    function openErlangSkillTree(preserveReturnMode = false) {
      if (!preserveReturnMode) altarReturnMode = 'game';
      gameState.isPaused = true;
      gameState.mouse.isDown = false;
      renderErlangSkillTree();
      const modal = document.getElementById('erlang-skill-modal');
      modal.style.display = 'flex';
      modal.querySelector('button:not([disabled])')?.focus();
    }

    function closeErlangSkillTree() {
      document.getElementById('erlang-skill-modal').style.display = 'none';
      saveMetaProgress();
      if (altarReturnMode === 'title') {
        document.getElementById('start-screen').style.display = 'flex';
        gameState.isPaused = true;
      } else if (altarReturnMode === 'gameover') {
        document.getElementById('gameover-modal').style.display = 'flex';
        gameState.isPaused = true;
      } else {
        gameState.isPaused = false;
      }
      altarReturnMode = 'game';
    }

    let selectedTreeNodeId = 'dragon_dive';
    let treeView = {
      panX: -400,
      panY: -200,
      isDragging: false,
      pointerId: null,
      moved: false,
      suppressNextClick: false,
      dragStartX: 0,
      dragStartY: 0,
      panStartX: 0,
      panStartY: 0
    };

    function initSkillTreeSystem() {
      SKILL_TREE_72.forEach(node => {
        if (skillTreeRanks[node.id] === undefined) {
          skillTreeRanks[node.id] = (node.id === 'root' || node.id === 'form_dragon') ? 1 : 0;
        }
      });
      if (!['dragon', 'tiger', 'roc', 'ape', 'tortoise'].includes(activeTransformationForm)) activeTransformationForm = 'dragon';
      PERMANENT_PASSIVES.forEach(passive => {
        passiveSkillRanks[passive.id] = Math.min(passive.maxRank, getPermanentPassiveRank(passive.id));
      });
      player.activeTransformationForm = activeTransformationForm;
      const accessibleSelect = document.getElementById('tree-node-select');
      accessibleSelect.innerHTML = SKILL_TREE_72.map(node => `<option value="${node.id}">${node.icon} ${getSkillDisplayName(node)}</option>`).join('');
      accessibleSelect.addEventListener('change', () => {
        inspectTreeNode(accessibleSelect.value);
        renderSkillTreeCanvas();
      });
      renderPermanentPassives();
      initAlignmentSystem();
      saveMetaProgress();
    }
    initSkillTreeSystem();

    function getSkillRank(id) {
      return skillTreeRanks[id] || 0;
    }

    function renderPermanentPassives() {
      const container = document.getElementById('passive-skill-list');
      if (!container) return;
      container.innerHTML = PERMANENT_PASSIVES.map(passive => {
        const rank = getPermanentPassiveRank(passive.id);
        const isMax = rank >= passive.maxRank;
        const cost = getPermanentPassiveCost(passive, rank);
        const disabled = isMax || gameState.ashes < cost;
        const buttonText = gameState.language === 'en'
          ? (isMax ? 'Complete' : (gameState.ashes < cost ? `Need ${cost} Merit` : `+1 Level · ${cost}`))
          : (isMax ? '已圆满' : (gameState.ashes < cost ? `需 ${cost} 灵砂` : `+1级 · ${cost}`));
        const name = gameState.language === 'en' ? passive.nameEn : passive.name;
        const perLevel = gameState.language === 'en' ? passive.perLevelEn : passive.perLevel;
        const currentEffect = gameState.language === 'en' ? passive.effectEn(rank) : passive.effect(rank);
        return `<div class="passive-skill-row">
          <div>
            <div class="passive-skill-name">${passive.icon} ${name} <span style="color:#facc15">Lv.${rank}/${passive.maxRank}</span></div>
            <div class="passive-skill-effect">${perLevel} · ${gameState.language === 'en' ? 'Current' : '当前'}: ${currentEffect}</div>
          </div>
          <button type="button" class="passive-invest-btn" ${disabled ? 'disabled' : ''} onclick="investPermanentPassive('${passive.id}')">${buttonText}</button>
        </div>`;
      }).join('');
    }

    function refreshLocalizedSkillTree() {
      const accessibleSelect = document.getElementById('tree-node-select');
      if (!accessibleSelect) return;
      const selected = selectedTreeNodeId || accessibleSelect.value;
      accessibleSelect.innerHTML = SKILL_TREE_72.map(node => `<option value="${node.id}">${node.icon} ${getSkillDisplayName(node)}</option>`).join('');
      accessibleSelect.value = selected;
      renderPermanentPassives();
      inspectTreeNode(selected);
      renderSkillTreeCanvas();
    }

    function investPermanentPassive(id) {
      const passive = PERMANENT_PASSIVES.find(item => item.id === id);
      if (!passive) return;
      const rank = getPermanentPassiveRank(id);
      const cost = getPermanentPassiveCost(passive, rank);
      if (rank >= passive.maxRank || gameState.ashes < cost) return;
      gameState.ashes -= cost;
      passiveSkillRanks[id] = rank + 1;
      player.applyMetaUpgrades();
      player.hp = Math.min(player.hp, player.maxHp);
      player.qi = Math.min(player.qi, player.maxQi);
      document.getElementById('tree-ashes-val').innerText = gameState.ashes;
      renderPermanentPassives();
      inspectTreeNode(selectedTreeNodeId);
      updateHUD();
      saveMetaProgress();
      sound.playJadeChime();
    }

    function isNodeUnlocked(id) {
      const node = SKILL_TREE_72.find(n => n.id === id);
      if (!node) return false;
      if (node.id === 'root') return true;
      if (!node.prereq || node.prereq.length === 0) return true;
      // Unlocked if at least one prerequisite is unlocked (> 0 rank)
      return node.prereq.some(pid => getSkillRank(pid) > 0);
    }

    let altarReturnMode = 'game';

    function openAltarFromTitle() {
      altarReturnMode = 'title';
      document.getElementById('start-screen').style.display = 'none';
      openAltarOfTransformations(true);
    }

    function openTrainingFromGameOver() {
      altarReturnMode = 'gameover';
      document.getElementById('gameover-modal').style.display = 'none';
      openAltarOfTransformations(true);
    }

    function openAltarOfTransformations(preserveReturnMode = false) {
      if (gameState.playableHero === 'erlang') {
        openErlangSkillTree(preserveReturnMode);
        return;
      }
      if (!preserveReturnMode) altarReturnMode = 'game';
      gameState.isPaused = true;
      const modal = document.getElementById('altar-modal');
      modal.style.display = 'flex';

      document.getElementById('tree-ashes-val').innerText = gameState.ashes;

      setupTreeCanvas();
      inspectTreeNode(selectedTreeNodeId || 'dragon_dive');
      renderPermanentPassives();
      renderSkillTreeCanvas();
    }

    function closeAltarModal() {
      document.getElementById('altar-modal').style.display = 'none';
      if (altarReturnMode === 'title') {
        document.getElementById('start-screen').style.display = 'flex';
        gameState.isPaused = true;
      } else if (altarReturnMode === 'gameover') {
        document.getElementById('gameover-modal').style.display = 'flex';
        gameState.isPaused = true;
      } else {
        gameState.isPaused = false;
      }
      altarReturnMode = 'game';
    }

    let treeCanvasInitDone = false;
    function getTreePointFromClient(canvasEl, clientX, clientY) {
      const rect = canvasEl.getBoundingClientRect();
      const scaleX = canvasEl.width / Math.max(1, rect.width);
      const scaleY = canvasEl.height / Math.max(1, rect.height);
      return {
        x: (clientX - rect.left) * scaleX - treeView.panX,
        y: (clientY - rect.top) * scaleY - treeView.panY,
        scaleX,
        scaleY
      };
    }

    function selectTreeNodeAtClient(canvasEl, clientX, clientY) {
      const point = getTreePointFromClient(canvasEl, clientX, clientY);
      const node = SKILL_TREE_72.find(candidate => Math.hypot(candidate.x - point.x, candidate.y - point.y) <= (candidate.isForm ? 38 : 32));
      if (!node) return null;
      inspectTreeNode(node.id);
      renderSkillTreeCanvas();
      sound.playJadeChime();
      return node;
    }

    function setupTreeCanvas() {
      const canvasEl = document.getElementById('skill-tree-canvas');
      const container = document.getElementById('tree-canvas-container');
      if (!canvasEl || !container) return;

      if (!treeCanvasInitDone) {
        treeCanvasInitDone = true;

        canvasEl.addEventListener('pointerdown', (e) => {
          if (e.button !== 0) return;
          e.preventDefault();
          treeView.pointerId = e.pointerId;
          treeView.isDragging = true;
          treeView.moved = false;
          treeView.dragStartX = e.clientX;
          treeView.dragStartY = e.clientY;
          treeView.panStartX = treeView.panX;
          treeView.panStartY = treeView.panY;
          canvasEl.setPointerCapture(e.pointerId);
        });

        canvasEl.addEventListener('pointermove', (e) => {
          if (!treeView.isDragging || e.pointerId !== treeView.pointerId) return;
          const rect = canvasEl.getBoundingClientRect();
          const deltaX = e.clientX - treeView.dragStartX;
          const deltaY = e.clientY - treeView.dragStartY;
          if (Math.hypot(deltaX, deltaY) > 4) treeView.moved = true;
          treeView.panX = treeView.panStartX + deltaX * (canvasEl.width / Math.max(1, rect.width));
          treeView.panY = treeView.panStartY + deltaY * (canvasEl.height / Math.max(1, rect.height));
          renderSkillTreeCanvas();
        });

        const finishTreePointer = e => {
          if (e.pointerId !== treeView.pointerId) return;
          const wasMoved = treeView.moved;
          treeView.isDragging = false;
          treeView.pointerId = null;
          treeView.suppressNextClick = wasMoved;
        };
        canvasEl.addEventListener('pointerup', finishTreePointer);
        canvasEl.addEventListener('pointercancel', e => {
          if (e.pointerId === treeView.pointerId) {
            treeView.isDragging = false;
            treeView.pointerId = null;
          }
        });
        canvasEl.addEventListener('click', e => {
          if (treeView.suppressNextClick) {
            treeView.suppressNextClick = false;
            return;
          }
          selectTreeNodeAtClient(canvasEl, e.clientX, e.clientY);
        });
        canvasEl.addEventListener('dblclick', e => {
          const node = selectTreeNodeAtClient(canvasEl, e.clientX, e.clientY);
          if (node && getSkillRank(node.id) < node.maxRank) upgradeNodeFromInspector();
        });
      }
    }

    function inspectTreeNode(nodeId) {
      selectedTreeNodeId = nodeId;
      const node = SKILL_TREE_72.find(n => n.id === nodeId);
      if (!node) return;

      const rank = getSkillRank(node.id);
      const unlocked = isNodeUnlocked(node.id);
      const isMax = rank >= node.maxRank;
      const nextCost = Math.round(node.cost * (rank + 1));

      const branchColors = {
        core: '#c084fc',
        dragon: '#38bdf8',
        tiger: '#f59e0b',
        roc: '#fbbf24',
        ape: '#ea580c',
        tortoise: '#10b981'
      };
      const branchNames = {
        core: '混元祖根',
        dragon: '🐲 苍龙神变 (水雷御海)',
        tiger: '🐯 白虎战煞 (庚金杀伐)',
        roc: '🦅 金翅大鹏 (极速破虚)',
        ape: '🦍 法天象地 (泰坦崩山)',
        tortoise: '🐢 玄武不灭 (幽冥玄甲)'
      };

      const bColor = branchColors[node.branch] || '#facc15';
      const badge = document.getElementById('inspect-branch-badge');
      badge.style.borderColor = bColor;
      badge.style.color = bColor;
      badge.style.background = bColor + '22';
      badge.innerText = gameState.language === 'en' ? (SKILL_BRANCH_EN[node.branch] || node.branch) : (branchNames[node.branch] || node.branch);

      document.getElementById('inspect-name').innerText = `${node.icon} ${getSkillDisplayName(node)}`;
      document.getElementById('tree-node-select').value = node.id;
      document.getElementById('inspect-rank').innerText = gameState.language === 'en'
        ? (isMax ? `Current Rank: Complete (${rank}/${node.maxRank})` : `Current Rank: ${rank} / ${node.maxRank}`)
        : (isMax ? `当前境界: 已圆满 (${rank}/${node.maxRank})` : `当前境界: 第 ${rank} 重 / 共 ${node.maxRank} 重`);
      document.getElementById('inspect-rank').style.color = isMax ? '#facc15' : (unlocked ? '#4ade80' : '#94a3b8');

      document.getElementById('inspect-desc').innerText = getSkillDisplayDescription(node);

      const statsEl = document.getElementById('inspect-stats-bonus');
      const passiveDamage = getPermanentPassiveRank('damage');
      const passiveVitality = getPermanentPassiveRank('vitality');
      statsEl.innerHTML = gameState.language === 'en' ? `
        <div>• Status: ${unlocked ? (rank > 0 ? `Rank ${rank} active` : 'Ready to learn') : 'Prerequisite not learned'}</div>
        <div>• Form-only hook: ${FORM_SKILL_RUNTIME_CONTRACTS[node.id]?.hook || 'origin'} · dormant outside its matching transformation</div>
        <div>• Visible feedback: ${node.icon} animated ${FORM_SKILL_RUNTIME_CONTRACTS[node.id]?.hook || 'origin'} rune + form-element effect</div>
        <div>• Permanent passives: All damage +${passiveDamage}% · Maximum Health +${passiveVitality}%</div>
        <div>• Merit cost: ${isMax ? 'Fully mastered' : `${nextCost} Merit Sand`}</div>
      ` : `
        <div>• 属性加成: ${unlocked ? (rank > 0 ? `已激活第 ${rank} 重神威` : '尚未激活') : '未解锁前置神通'}</div>
        <div>• 真身专属触发: ${FORM_SKILL_RUNTIME_CONTRACTS[node.id]?.hook || '灵根'} · 离开对应变身即休眠</div>
        <div>• 可见反馈: ${node.icon} 动态神通印记 + 真身元素动画</div>
        <div>• 永久被动: 全伤害 +${passiveDamage}% · 最大气血 +${passiveVitality}%</div>
        <div>• 消耗灵砂: ${isMax ? '已至登峰造极' : `${nextCost} 功德灵砂`}</div>
      `;

      const equipBtn = document.getElementById('inspect-equip-btn');
      if (node.isForm && rank > 0) {
        equipBtn.style.display = 'block';
        if (activeTransformationForm === node.formKey) {
          equipBtn.innerText = gameState.language === 'en' ? '⭐ Active Battle Form (Equipped)' : '⭐ 当前出战真容 (已佩戴)';
          equipBtn.style.opacity = '0.7';
        } else {
          equipBtn.innerText = gameState.language === 'en'
            ? `⭐ Equip as [R] Form (${getSkillDisplayName(node)})`
            : `⭐ 装备为 [R] 变身真身 (${node.name})`;
          equipBtn.style.opacity = '1.0';
        }
      } else {
        equipBtn.style.display = 'none';
      }

      const upBtn = document.getElementById('inspect-upgrade-btn');
      if (isMax) {
        upBtn.disabled = true;
        upBtn.innerText = gameState.language === 'en' ? '✨ Fully Mastered' : '✨ 已修炼至圆满境界';
        upBtn.style.opacity = '0.6';
      } else if (!unlocked) {
        upBtn.disabled = true;
        upBtn.innerText = gameState.language === 'en' ? '🔒 Learn a Prerequisite First' : '🔒 前置神通未参悟';
        upBtn.style.opacity = '0.5';
      } else if (gameState.ashes < nextCost) {
        upBtn.disabled = true;
        upBtn.innerText = gameState.language === 'en' ? `Not Enough Merit (Need ${nextCost})` : `灵砂不足 (需 ${nextCost} 灵砂)`;
        upBtn.style.opacity = '0.5';
      } else {
        upBtn.disabled = false;
        upBtn.innerText = gameState.language === 'en' ? `Invest Rank (Cost: ${nextCost} Merit)` : `参悟提升境界 (消耗 ${nextCost} 灵砂)`;
        upBtn.style.opacity = '1.0';
      }
    }

    function upgradeNodeFromInspector() {
      const node = SKILL_TREE_72.find(n => n.id === selectedTreeNodeId);
      if (!node) return;

      const rank = getSkillRank(node.id);
      const nextCost = Math.round(node.cost * (rank + 1));

      if (rank < node.maxRank && isNodeUnlocked(node.id) && gameState.ashes >= nextCost) {
        gameState.ashes -= nextCost;
        skillTreeRanks[node.id] = rank + 1;
        player.applyMetaUpgrades();
        sound.playJadeChime();
        document.getElementById('tree-ashes-val').innerText = gameState.ashes;
        inspectTreeNode(node.id);
        renderSkillTreeCanvas();
        renderPermanentPassives();
        updateHUD();
        saveMetaProgress();
      }
    }

    function equipActiveFormFromInspector() {
      const node = SKILL_TREE_72.find(n => n.id === selectedTreeNodeId);
      if (!node || !node.isForm) return;

      activeTransformationForm = node.formKey;
      player.activeTransformationForm = node.formKey;
      sound.playGong();
      inspectTreeNode(node.id);
      renderSkillTreeCanvas();
      updateHUD();
      saveMetaProgress();
    }

    function resetAllSkillTreePoints() {
      if (!confirm(uiText('确定要重置神木节点并全额退还灵砂吗？永久被动修行不会被重置。', 'Reset all tree nodes and refund their Merit Sand? Permanent passives will remain.'))) return;

      let refund = 0;
      SKILL_TREE_72.forEach(node => {
        const rank = getSkillRank(node.id);
        if (rank > 0 && node.id !== 'root' && node.cost > 0) {
          for (let r = 1; r <= rank; r++) {
            refund += Math.round(node.cost * r);
          }
        }
      });

      skillTreeRanks = { root: 1, form_dragon: 1 };
      gameState.ashes += refund;
      player.applyMetaUpgrades();
      sound.playJadeChime();
      document.getElementById('tree-ashes-val').innerText = gameState.ashes;
      inspectTreeNode('form_dragon');
      renderSkillTreeCanvas();
      renderPermanentPassives();
      updateHUD();
      saveMetaProgress();
      alert(uiText(`已重置神木节点并返还 ${refund} 点功德灵砂。永久被动修行保持不变。`, `Tree nodes reset. ${refund} Merit Sand refunded; permanent passives were preserved.`));
    }

    function focusTreeBranch(branch) {
      document.querySelectorAll('.branch-btn').forEach(b => b.classList.remove('active'));
      const targetBtn = Array.from(document.querySelectorAll('.branch-btn')).find(b => b.innerText.includes(branch) || (branch === 'all' && b.innerText.includes('全景')));
      if (targetBtn) targetBtn.classList.add('active');

      if (branch === 'dragon') {
        treeView.panX = -600;
        treeView.panY = 100;
        inspectTreeNode('form_dragon');
      } else if (branch === 'tiger') {
        treeView.panX = -1000;
        treeView.panY = -250;
        inspectTreeNode('form_tiger');
      } else if (branch === 'roc') {
        treeView.panX = -900;
        treeView.panY = -600;
        inspectTreeNode('form_roc');
      } else if (branch === 'ape') {
        treeView.panX = -450;
        treeView.panY = -600;
        inspectTreeNode('form_ape');
      } else if (branch === 'tortoise') {
        treeView.panX = -200;
        treeView.panY = -250;
        inspectTreeNode('form_tortoise');
      } else {
        treeView.panX = -550;
        treeView.panY = -280;
      }
      renderSkillTreeCanvas();
    }

    function renderTreeHitTargets() {
      const layer = document.getElementById('tree-hit-layer');
      if (!layer) return;
      if (layer.children.length !== SKILL_TREE_72.length) {
        layer.innerHTML = '';
        SKILL_TREE_72.forEach(node => {
          const button = document.createElement('button');
          button.type = 'button';
          button.tabIndex = -1;
          button.className = `tree-node-hit${node.isForm ? ' form-hit' : ''}`;
          button.dataset.nodeId = node.id;
          button.setAttribute('aria-label', gameState.language === 'en'
            ? `${getSkillDisplayName(node)}, current rank ${getSkillRank(node.id)} of ${node.maxRank}`
            : `${node.name}，当前 ${getSkillRank(node.id)}/${node.maxRank} 重`);
          button.title = gameState.language === 'en'
            ? `${getSkillDisplayName(node)} · Click to select, double-click to invest`
            : `${node.name} · 单击选择，双击投资`;
          button.addEventListener('click', event => {
            event.stopPropagation();
            inspectTreeNode(node.id);
            renderSkillTreeCanvas();
            sound.playJadeChime();
          });
          button.addEventListener('dblclick', event => {
            event.stopPropagation();
            inspectTreeNode(node.id);
            upgradeNodeFromInspector();
          });
          layer.appendChild(button);
        });
      }
      SKILL_TREE_72.forEach((node, index) => {
        const button = layer.children[index];
        button.style.left = `${((node.x + treeView.panX) / 1800) * 100}%`;
        button.style.top = `${((node.y + treeView.panY) / 1200) * 100}%`;
        button.setAttribute('aria-label', gameState.language === 'en'
          ? `${getSkillDisplayName(node)}, current rank ${getSkillRank(node.id)} of ${node.maxRank}`
          : `${node.name}，当前 ${getSkillRank(node.id)}/${node.maxRank} 重`);
        button.setAttribute('aria-pressed', selectedTreeNodeId === node.id ? 'true' : 'false');
      });
    }

    function renderSkillTreeCanvas() {
      const canvasEl = document.getElementById('skill-tree-canvas');
      if (!canvasEl) return;
      const ctxT = canvasEl.getContext('2d');

      ctxT.clearRect(0, 0, canvasEl.width, canvasEl.height);

      ctxT.save();
      ctxT.translate(treeView.panX, treeView.panY);

      // Background Starfield Grid
      ctxT.strokeStyle = 'rgba(230, 180, 80, 0.05)';
      ctxT.lineWidth = 1;
      for (let x = 0; x < 2000; x += 100) {
        ctxT.beginPath();
        ctxT.moveTo(x, 0);
        ctxT.lineTo(x, 1400);
        ctxT.stroke();
      }
      for (let y = 0; y < 1400; y += 100) {
        ctxT.beginPath();
        ctxT.moveTo(0, y);
        ctxT.lineTo(2000, y);
        ctxT.stroke();
      }

      const branchColors = {
        core: '#c084fc',
        dragon: '#38bdf8',
        tiger: '#f59e0b',
        roc: '#fbbf24',
        ape: '#ea580c',
        tortoise: '#10b981'
      };

      // 1. Draw Connection Lines
      SKILL_TREE_72.forEach(node => {
        if (node.prereq && node.prereq.length > 0) {
          node.prereq.forEach(pid => {
            const parent = SKILL_TREE_72.find(p => p.id === pid);
            if (parent) {
              const unlocked = isNodeUnlocked(node.id);
              const active = getSkillRank(node.id) > 0;
              const color = branchColors[node.branch] || '#facc15';

              ctxT.beginPath();
              ctxT.moveTo(parent.x, parent.y);
              const midX = (parent.x + node.x) / 2;
              const midY = (parent.y + node.y) / 2;
              ctxT.quadraticCurveTo(midX, midY, node.x, node.y);

              ctxT.strokeStyle = active ? color : (unlocked ? 'rgba(255,255,255,0.4)' : 'rgba(255,255,255,0.1)');
              ctxT.lineWidth = active ? 4 : (unlocked ? 2 : 1);
              if (active) {
                ctxT.shadowColor = color;
                ctxT.shadowBlur = 12;
              } else {
                ctxT.shadowBlur = 0;
              }
              ctxT.stroke();
              ctxT.shadowBlur = 0;
            }
          });
        }
      });

      // 2. Draw Nodes
      SKILL_TREE_72.forEach(node => {
        const rank = getSkillRank(node.id);
        const unlocked = isNodeUnlocked(node.id);
        const isSelected = selectedTreeNodeId === node.id;
        const color = branchColors[node.branch] || '#facc15';
        const isEquippedForm = node.isForm && activeTransformationForm === node.formKey;

        ctxT.save();
        ctxT.translate(node.x, node.y);

        const radius = node.isForm ? 28 : (node.id === 'root' ? 32 : 22);

        // Node Glow Ring
        if (isSelected || isEquippedForm || rank > 0) {
          ctxT.beginPath();
          ctxT.arc(0, 0, radius + 6, 0, Math.PI * 2);
          ctxT.strokeStyle = isEquippedForm ? '#facc15' : (isSelected ? '#fff' : color);
          ctxT.lineWidth = isSelected ? 3 : 2;
          ctxT.shadowColor = isEquippedForm ? '#facc15' : color;
          ctxT.shadowBlur = 16;
          ctxT.stroke();
          ctxT.shadowBlur = 0;
        }

        // Inner Circle
        ctxT.beginPath();
        ctxT.arc(0, 0, radius, 0, Math.PI * 2);
        ctxT.fillStyle = rank > 0 ? (node.isForm ? color : '#1e1630') : (unlocked ? '#120d20' : '#08050e');
        ctxT.fill();
        ctxT.strokeStyle = rank > 0 ? color : (unlocked ? 'rgba(255,255,255,0.4)' : 'rgba(255,255,255,0.15)');
        ctxT.lineWidth = 2;
        ctxT.stroke();

        // Icon
        ctxT.font = `${node.isForm ? 22 : 16}px sans-serif`;
        ctxT.textAlign = 'center';
        ctxT.textBaseline = 'middle';
        ctxT.fillText(node.icon, 0, -2);

        // Text label
        ctxT.font = getCanvasFont(11, 600);
        ctxT.fillStyle = rank > 0 ? '#fef08a' : (unlocked ? '#cbd5e1' : '#64748b');
        const nodeLabel = getSkillDisplayName(node);
        ctxT.font = getCanvasFont(gameState.language === 'en' && nodeLabel.length > 24 ? 9 : 11, 600);
        ctxT.fillText(nodeLabel, 0, radius + 14);

        // Rank Badge
        if (node.maxRank > 1) {
          ctxT.fillStyle = rank >= node.maxRank ? '#facc15' : (rank > 0 ? '#4ade80' : '#64748b');
          ctxT.font = '10px sans-serif';
          ctxT.fillText(`${rank}/${node.maxRank}`, 0, radius + 26);
        } else if (isEquippedForm) {
          ctxT.fillStyle = '#facc15';
          ctxT.font = '10px sans-serif';
          ctxT.fillText(gameState.language === 'en' ? '⭐ Active' : '⭐ 出战中', 0, radius + 26);
        }

        ctxT.restore();
      });

      ctxT.restore();
      renderTreeHitTargets();
    }


    function openSkillCodex() {
      gameState.isPaused = true;
      const modal = document.getElementById('codex-modal');
      const container = document.getElementById('codex-cards-container');
      container.innerHTML = '';

      for (let k in GODS) {
        const g = GODS[k];
        const ge = GOD_EN[k];
        const card = document.createElement('div');
        card.className = 'codex-card';
        card.innerHTML = `
          <div class="codex-god-title" style="color: ${g.color};">${gameState.language === 'en' && ge ? `${ge.name} (${ge.title})` : `${g.name} (${g.title})`}</div>
          <div class="codex-boon-list">
            ${g.boons.map(b => { const shown = getLocalizedBoon(b, k); return `<div>• <b>${shown.name}</b> [${gameState.language === 'en' ? translateGameText(b.slot) : b.slot}]: ${shown.desc}</div>`; }).join('')}
          </div>
        `;
        container.appendChild(card);
      }

      modal.style.display = 'flex';
    }

    function closeSkillCodex() {
      document.getElementById('codex-modal').style.display = 'none';
      gameState.isPaused = false;
    }

    function handleGameOver(isVictory) {
      if (gameState.isPaused && document.getElementById('gameover-modal').style.display === 'flex') return;
      gameState.isPaused = true;
      gameState.mouse.isDown = false;
      gameState.mobileMove.x = 0;
      gameState.mobileMove.y = 0;
      const modal = document.getElementById('gameover-modal');
      const title = document.getElementById('gameover-title');
      const sub = document.getElementById('gameover-sub');

      if (isVictory) {
        title.className = 'gameover-title victory';
        campaignUnlocks.newGamePlus = true;
        campaignUnlocks.erlangPlayable = true;
        if (gameState.campaignRoute === 'fengshen') {
          campaignUnlocks.fengshenComplete = true;
          title.innerText = uiText('清源妙道 · 封神亲历圆满！', 'Clear-Origin Sage · Fengshen Chronicle Complete!');
          sub.innerText = uiText('杨戬见证三十八章封神大战，以天眼照见天命背后的众生代价，最终带哮天犬回归灌江口。二郎神永久技能与连招修为已保存在浏览器。', 'Across thirty-eight chapters, Yang Jian witnesses the Investiture War and the human cost behind destiny, then returns to Guanjiang with Xiaotianquan. Erlang’s permanent skills and combo mastery remain saved in this browser.');
        } else if (gameState.isNewGamePlus) {
          campaignUnlocks.journeyComplete = true;
          campaignUnlocks.ngPlusClears++;
          title.innerText = uiText('天镜百章再破 · 显圣凯旋！', 'Celestial Mirror Conquered · New Game+ Complete!');
          sub.innerText = uiText('百章劫难在天镜中再度破尽。二郎神与悟空的修行均永久保留，可继续挑战更高修为。', 'All one hundred trials fall again in the Celestial Mirror. Permanent cultivation for Wukong and Erlang remains saved for another ascent.');
        } else {
          campaignUnlocks.journeyComplete = true;
          title.innerText = gameState.language === 'en' ? 'Five Saints Attain Truth · Victorious Fighting Buddha!' : '五圣成真 · 斗战胜佛！';
          sub.innerText = gameState.language === 'en'
            ? 'The true scriptures reach Chang’an. Wukong returns to Vulture Peak, receives the title Victorious Fighting Buddha, and the golden headband falls away at last.'
            : '真经传回长安，师徒复返灵山受封。悟空成就斗战胜佛，头上金箍自然脱落，百章西游圆满。';
        }
        sound.playGong();
      } else {
        title.className = 'gameover-title defeat';
        title.innerText = gameState.language === 'en' ? 'Defeated' : '道消身殒';
        sub.innerText = gameState.campaignRoute === 'fengshen'
          ? uiText('法身虽败，清源妙道仍存。二郎神永久技能已保存，可从封神录第一章重新出发。', 'The manifestation falls, but Clear-Origin mastery remains. Erlang’s permanent skills are saved; restart the Fengshen Chronicle from Chapter 1.')
          : (gameState.language === 'en' ? 'The spirit endures. Permanent cultivation remains saved; restart the complete journey from chapter 1.' : '形骸虽散，神魂不灭。永久修行仍已保存，可从第一章重新踏上完整西游。');
      }

      const displayedChapter = Math.max(1, Math.min(gameState.totalChambers, Math.floor(Number(gameState.chamberIndex) || 1)));
      document.getElementById('stat-chambers').innerText = gameState.language === 'en'
        ? `${displayedChapter} / ${gameState.totalChambers} Chapters`
        : `${displayedChapter} / ${gameState.totalChambers} 章`;
      document.getElementById('stat-kills').innerText = gameState.enemiesKilled;
      document.getElementById('stat-boons').innerText = gameState.boonsCount;
      document.getElementById('stat-peaches').innerText = gameState.peachesEaten;
      document.getElementById('stat-ashes').innerText = gameState.ashes;
      saveMetaProgress();
      refreshTitleUnlocks();

      modal.style.display = 'flex';
    }

    let currentChapterStartCheckpoint = null;

    function loadRunCheckpoint() {
      try {
        const checkpoint = JSON.parse(safeStorageGetItem(RUN_CHECKPOINT_SAVE_KEY) || 'null');
        const chapter = Math.floor(Number(checkpoint?.chapter));
        if (!checkpoint || checkpoint.version !== 1 || chapter < 1 || chapter > 100 || !checkpoint.player || !checkpoint.run) return null;
        checkpoint.chapter = chapter;
        return checkpoint;
      } catch (_) {
        return null;
      }
    }

    function clearRunCheckpoint() {
      safeStorageRemoveItem(RUN_CHECKPOINT_SAVE_KEY);
    }

    function checkpointBoon(boon) {
      return boon?.id ? { id: boon.id, godKey: boon.godKey || null, level: Math.max(1, Math.floor(boon.level || 1)) } : null;
    }

    function createRunCheckpoint(chapter = gameState.chamberIndex) {
      return {
        version: 1,
        chapter: Math.max(1, Math.min(gameState.totalChambers || 100, Math.floor(chapter || 1))),
        savedAt: new Date().toISOString(),
        hero: gameState.playableHero,
        route: gameState.campaignRoute,
        isNewGamePlus: !!gameState.isNewGamePlus,
        run: {
          gold: Math.max(0, Math.floor(gameState.gold || 0)),
          peachesEaten: Math.max(0, Math.floor(gameState.peachesEaten || 0)),
          enemiesKilled: Math.max(0, Math.floor(gameState.enemiesKilled || 0)),
          boonsCount: Math.max(0, Math.floor(gameState.boonsCount || 0)),
          transformationDoctrine: gameState.transformationDoctrine || null,
          ruyiAcquired: !!gameState.ruyiAcquired,
          buddhaImprisoned: !!gameState.buddhaImprisoned
        },
        player: {
          hp: Math.max(1, Number(player.hp) || 1), maxHp: Math.max(1, Number(player.maxHp) || 100),
          runMaxHpBonus: Math.max(0, Number(player.runMaxHpBonus) || 0),
          qi: Math.max(0, Number(player.qi) || 0), maxQi: Math.max(1, Number(player.maxQi) || 100),
          lives: Math.max(0, Math.floor(player.lives || 0)), maxLives: Math.max(1, Math.floor(player.maxLives || 1)),
          armor: Math.max(0, Number(player.armor) || 0),
          bullArmor: Math.max(0, Number(player.bullArmor) || 0), bullArmorMax: Math.max(0, Number(player.bullArmorMax) || 0),
          masterworkArmor: Math.max(0, Number(player.masterworkArmor) || 0), masterworkArmorMax: Math.max(0, Number(player.masterworkArmorMax) || 0),
          weaponStyle: player.weaponStyle || 'normal',
          activeTransformationForm: player.activeTransformationForm || activeTransformationForm || 'dragon',
          absorbedBossQi: Math.max(0, Math.floor(player.absorbedBossQi || 0)),
          boonLevels: { ...player.boonLevels },
          boons: {
            weapon: checkpointBoon(player.boons.weapon), attack: checkpointBoon(player.boons.attack),
            special: checkpointBoon(player.boons.special), cast: checkpointBoon(player.boons.cast),
            dash: checkpointBoon(player.boons.dash), hex: checkpointBoon(player.boons.hex),
            passives: player.boons.passives.map(checkpointBoon).filter(Boolean)
          }
        }
      };
    }

    function captureChapterStartCheckpoint() {
      if (!gameState.hasStarted || gameState.chamberCleared) return currentChapterStartCheckpoint;
      currentChapterStartCheckpoint = createRunCheckpoint(gameState.chamberIndex);
      return currentChapterStartCheckpoint;
    }

    function persistRunCheckpoint(checkpoint) {
      if (!checkpoint) return false;
      const savedCopy = JSON.parse(JSON.stringify(checkpoint));
      savedCopy.savedAt = new Date().toISOString();
      return safeStorageSetItem(RUN_CHECKPOINT_SAVE_KEY, JSON.stringify(savedCopy));
    }

    function restoreCheckpointBoon(savedBoon) {
      if (!savedBoon?.id) return null;
      let godKey = savedBoon.godKey;
      let definition = GODS[godKey]?.boons?.find(boon => boon.id === savedBoon.id);
      if (!definition) {
        const owner = Object.entries(GODS).find(([, god]) => god.boons.some(boon => boon.id === savedBoon.id));
        if (!owner) return null;
        godKey = owner[0];
        definition = owner[1].boons.find(boon => boon.id === savedBoon.id);
      }
      return { ...getLocalizedBoon(definition, godKey), godKey, level: Math.max(1, Math.floor(savedBoon.level || 1)) };
    }

    function refreshRestoredBoonInterface() {
      ['attack','special','cast','dash','hex'].forEach(slot => {
        const tag = document.getElementById(`boon-tag-${slot}`);
        const boon = player.boons[slot];
        if (tag && boon) tag.innerText = `${boon.name} · Lv.${boon.level || 1}`;
      });
      if (player.boons.weapon) document.getElementById('weapon-style-title').innerText = `${player.boons.weapon.name} · Lv.${player.boons.weapon.level || 1}`;
    }

    function restoreRunCheckpoint(checkpoint, showNotice = true) {
      if (!checkpoint || checkpoint.version !== 1) return false;
      sound.init();
      closeAllOverlays();
      document.getElementById('start-screen').style.display = 'none';
      const checkpointHero = checkpoint.hero === 'erlang' && campaignUnlocks.erlangPlayable ? 'erlang' : 'wukong';
      gameState.playableHero = checkpointHero;
      gameState.campaignRoute = checkpoint.route === 'fengshen' && checkpointHero === 'erlang' ? 'fengshen' : 'journey';
      gameState.isNewGamePlus = !!checkpoint.isNewGamePlus;
      gameState.runStartChapter = checkpoint.chapter;
      gameState.runEndChapter = gameState.campaignRoute === 'fengshen' ? 38 : 100;
      gameState.totalChambers = gameState.runEndChapter;
      resetRunStats();
      gameState.gold = Math.max(0, Math.floor(checkpoint.run.gold || 0));
      gameState.peachesEaten = Math.max(0, Math.floor(checkpoint.run.peachesEaten || 0));
      gameState.enemiesKilled = Math.max(0, Math.floor(checkpoint.run.enemiesKilled || 0));
      gameState.boonsCount = Math.max(0, Math.floor(checkpoint.run.boonsCount || 0));
      gameState.transformationDoctrine = checkpoint.run.transformationDoctrine || (checkpointHero === 'erlang' ? 'erlang' : null);
      gameState.ruyiAcquired = !!checkpoint.run.ruyiAcquired;
      gameState.buddhaImprisoned = !!checkpoint.run.buddhaImprisoned;
      gameState.hasStarted = true;
      gameState.isPaused = false;

      player.resetForRun();
      const savedPlayer = checkpoint.player || {};
      player.boonLevels = sanitizeRankMap(savedPlayer.boonLevels || {});
      player.boons = {
        weapon: restoreCheckpointBoon(savedPlayer.boons?.weapon),
        attack: restoreCheckpointBoon(savedPlayer.boons?.attack),
        special: restoreCheckpointBoon(savedPlayer.boons?.special),
        cast: restoreCheckpointBoon(savedPlayer.boons?.cast),
        dash: restoreCheckpointBoon(savedPlayer.boons?.dash),
        hex: restoreCheckpointBoon(savedPlayer.boons?.hex),
        passives: (savedPlayer.boons?.passives || []).map(restoreCheckpointBoon).filter(Boolean)
      };
      [...Object.values(player.boons).filter(boon => boon && !Array.isArray(boon)), ...player.boons.passives]
        .forEach(boon => { player.boonLevels[boon.id] = Math.max(player.boonLevels[boon.id] || 0, boon.level || 1); });
      player.weaponStyle = ['normal','titan','extend','chain'].includes(savedPlayer.weaponStyle) ? savedPlayer.weaponStyle : 'normal';
      player.activeTransformationForm = ['dragon','tiger','roc','ape','tortoise'].includes(savedPlayer.activeTransformationForm) ? savedPlayer.activeTransformationForm : activeTransformationForm;
      player.absorbedBossQi = Math.max(0, Math.floor(savedPlayer.absorbedBossQi || 0));
      const savedMaxHp = Math.max(1, Number(savedPlayer.maxHp) || player.maxHp);
      const savedRunMaxHpBonus = Number(savedPlayer.runMaxHpBonus);
      player.runMaxHpBonus = Number.isFinite(savedRunMaxHpBonus)
        ? Math.max(0, savedRunMaxHpBonus)
        : Math.max(0, savedMaxHp - (player.metaMaxHp || player.maxHp));
      player.maxHp = (player.metaMaxHp || player.maxHp) + player.runMaxHpBonus;
      player.maxQi = Math.max(player.maxQi, Number(savedPlayer.maxQi) || player.maxQi);
      player.hp = Math.max(1, Math.min(player.maxHp, Number(savedPlayer.hp) || player.maxHp));
      player.qi = Math.max(0, Math.min(player.maxQi, Number(savedPlayer.qi) || 0));
      player.maxLives = Math.max(player.maxLives, Math.floor(savedPlayer.maxLives || 1));
      player.lives = Math.max(0, Math.min(player.maxLives, Math.floor(savedPlayer.lives ?? player.maxLives)));
      player.armor = Math.max(player.baseArmor || 0, Number(savedPlayer.armor) || 0);
      player.bullArmorMax = Math.max(0, Number(savedPlayer.bullArmorMax) || 0);
      player.bullArmor = Math.min(player.bullArmorMax, Math.max(0, Number(savedPlayer.bullArmor) || 0));
      player.masterworkArmorMax = Math.max(0, Number(savedPlayer.masterworkArmorMax) || 0);
      player.masterworkArmor = Math.min(player.masterworkArmorMax, Math.max(0, Number(savedPlayer.masterworkArmor) || 0));

      currentChapterStartCheckpoint = JSON.parse(JSON.stringify(checkpoint));
      updateHeroInterface();
      startChamber(checkpoint.chapter);
      refreshRestoredBoonInterface();
      if (showNotice) {
        const tutorial = document.getElementById('tutorial-card');
        tutorial.innerText = uiText(`已载入存档 · 从第 ${checkpoint.chapter} 章开头重新开始 · [Esc] 菜单`, `Save loaded · restarting at the beginning of Chapter ${checkpoint.chapter} · [Esc] Menu`);
        tutorial.style.display = 'block';
        window.clearTimeout(startJourney.tutorialTimer);
        startJourney.tutorialTimer = window.setTimeout(() => { tutorial.style.display = 'none'; }, 7000);
      }
      canvas.focus?.();
      return true;
    }

    function startOrContinueJourney() {
      const checkpoint = loadRunCheckpoint();
      if (checkpoint) restoreRunCheckpoint(checkpoint, true);
      else startJourney(false);
    }

    function startFreshJourney() {
      const checkpoint = loadRunCheckpoint();
      if (checkpoint && !window.confirm(uiText('删除本次旅程存档并从第 1 章重新开始？永久技能与功德不会删除。', 'Delete this journey save and restart from Chapter 1? Permanent skills and Merit will remain.'))) return;
      startJourney(false);
    }

    function restartCurrentChapter() {
      if (!currentChapterStartCheckpoint) return;
      restoreRunCheckpoint(currentChapterStartCheckpoint, true);
    }

    function saveAndExitToTitle() {
      const checkpoint = currentChapterStartCheckpoint || captureChapterStartCheckpoint();
      saveMetaProgress();
      if (!persistRunCheckpoint(checkpoint)) {
        const info = document.getElementById('pause-checkpoint-info');
        if (info) info.innerText = uiText('浏览器阻止了存档。请不要关闭页面，并检查浏览器储存权限。', 'The browser blocked saving. Keep this page open and check browser storage permissions.');
        return false;
      }
      returnToTitle();
      return true;
    }

    function closeAllOverlays() {
      document.querySelectorAll('.modal-overlay').forEach(modal => { modal.style.display = 'none'; });
      document.getElementById('altar-modal').style.display = 'none';
    }

    function resetRunStats() {
      gameState.gold = 0;
      gameState.peachesEaten = 0;
      gameState.enemiesKilled = 0;
      gameState.boonsCount = 0;
      gameState.screenShake = 0;
      gameState.transformationDoctrine = null;
      gameState.ruyiAcquired = false;
      gameState.buddhaImprisoned = false;
      gameState.campaignBiome = 0;
      gameState.dialogueActive = false;
      gameState.rewardSelectionActive = false;
      gameState.bossOutcomeActive = false;
      gameState.bossOutcomeContinuation = null;
      pendingBossOutcomeGroup = [];
      gameState.deferredDialogueChapter = null;
      gameState.keys = {};
      gameState.mouse.isDown = false;
      gameState.mouse.rightDown = false;
      gameState.mobileMove.x = 0;
      gameState.mobileMove.y = 0;
      buddhaCutsceneActive = false;
      buddhaCutsceneChapter = 0;
      buddhaCutsceneSlides = [];
      buddhaCutsceneStep = 0;
    }

    function startJourney(newGamePlus = false) {
      sound.init();
      clearRunCheckpoint();
      currentChapterStartCheckpoint = null;
      closeAllOverlays();
      document.getElementById('start-screen').style.display = 'none';
      gameState.isNewGamePlus = !!newGamePlus;
      gameState.campaignRoute = gameState.playableHero === 'erlang' ? 'fengshen' : 'journey';
      gameState.runStartChapter = 1;
      gameState.runEndChapter = gameState.campaignRoute === 'fengshen' ? 38 : 100;
      gameState.totalChambers = gameState.runEndChapter;
      resetRunStats();
      gameState.hasStarted = true;
      gameState.isPaused = false;
      player.resetForRun();
      updateHeroInterface();
      if (gameState.playableHero === 'erlang') {
        gameState.transformationDoctrine = 'erlang';
        player.hasRuyiStaff = false;
        player.invulnTimer = Math.max(player.invulnTimer, 10.5);
      }
      startChamber(gameState.runStartChapter);
      const tutorial = document.getElementById('tutorial-card');
      tutorial.innerText = uiText('天光护体 10 秒 · 左右键混合连招 · 按 [C] 查看连招谱 · 按 [Esc] 打开菜单与保存退出', 'Celestial protection: 10 seconds · Mix left/right attacks · Press [C] for combos · Press [Esc] for Menu and Save & Exit');
      tutorial.style.display = 'block';
      window.clearTimeout(startJourney.tutorialTimer);
      startJourney.tutorialTimer = window.setTimeout(() => { tutorial.style.display = 'none'; }, 8500);
      canvas.focus?.();
    }

    function startNewRun() {
      startJourney(false);
    }

    function startNewGamePlus() {
      if (!campaignUnlocks.newGamePlus) return;
      startJourney(true);
    }

    function restartRun() {
      startJourney(gameState.isNewGamePlus);
    }

    let comboReadoutVersion = 0;
    let comboListOpenedFromPause = false;
    let comboListResumeOnClose = false;

    function updateComboReadout(sequence = '', completed = null) {
      const readout = document.getElementById('combo-chain-readout');
      if (!readout) return;
      comboReadoutVersion++;
      const version = comboReadoutVersion;
      if (completed) {
        const presentation = getActiveComboPresentation(completed);
        readout.innerText = uiText(`连招完成：${presentation.name}`, `Combo Complete: ${presentation.name}`);
        readout.classList.add('complete');
        window.setTimeout(() => {
          if (version !== comboReadoutVersion) return;
          readout.innerText = uiText('连招输入：—', 'Combo Input: —');
          readout.classList.remove('complete');
        }, 1150);
        return;
      }
      readout.classList.remove('complete');
      readout.innerText = sequence
        ? uiText(`连招输入：${sequence.split('').join(' · ')}`, `Combo Input: ${sequence.split('').join(' · ')}`)
        : uiText('连招输入：—', 'Combo Input: —');
    }

    function renderComboList() {
      const grid = document.getElementById('combo-list-grid');
      if (!grid) return;
      const isErlang = gameState.playableHero === 'erlang';
      const comboDefinitions = getActiveComboDefinitions();
      const stage = isErlang ? null : getAlignmentCombatStage();
      const pathClass = isErlang ? 'good' : (stage?.path || 'neutral');
      const title = document.getElementById('combo-list-title');
      const subtitle = document.getElementById('combo-list-subtitle');
      const help = document.getElementById('combo-list-help');
      if (title) title.innerText = isErlang ? uiText('👁 二郎真君 · 三尖两刃连招谱', '👁 Erlang Shen · Three-Pointed Spear Combos') : uiText('⚔ 如意金箍棒 · 混合连招谱', '⚔ Ruyi Jingu Bang · Mixed Combo Manual');
      if (subtitle) subtitle.innerText = isErlang
        ? uiText('三次左键为贯天入门枪；右键接在左键连段中为枪术重式，单独右键号令哮天犬。', 'Three left clicks perform the beginner drill. Right click inside a chain becomes a heavy spear input; right click alone commands Xiaotianquan.')
        : uiText('连续三次左键为新手三连：弧斩、周身横扫、裂地收棍。右键接在左键连段后为重棍；单独右键仍投掷金箍棒。', 'Three left clicks perform the beginner arc, sweep, and ground slam. Right click inside a chain becomes a heavy strike; right click alone throws the staff.');
      if (help) help.innerText = isErlang
        ? uiText('每次输入需在 1.20 秒内衔接。枪钻、升龙挑、神犬夹击、天轮横扫和天眼审判均使用独立七帧动作。', 'Link each input within 1.20 seconds. Drill, launcher, hound pin, heavenly wheel, and Third-Eye judgment each use a dedicated seven-frame animation.')
        : uiText('每次输入需在 1.35 秒内衔接。攻击期间输入会自动缓冲，不再吞键。善恶境界会改变悟空的整套动作、兵甲与收招特效。', 'Link each input within 1.35 seconds. Inputs buffer during attacks. Good and evil karma change Wukong’s moves, armor, and finish effects.');
      grid.innerHTML = comboDefinitions.map(combo => {
        const presentation = getActiveComboPresentation(combo);
        const tokens = combo.pattern.split('').map(token => `<span class="combo-token ${token === 'R' ? 'right' : ''}">${token}</span>`).join('');
        const damagePct = Math.round((combo.damage - 1) * 100);
        const reachPct = Math.round((combo.reach - 1) * 100);
        return `<article class="combo-card ${pathClass}">
          <div class="combo-card-name">${presentation.name}${combo.beginner ? `<span class="combo-badge">${uiText('新手推荐', 'Beginner')}</span>` : ''}</div>
          <div class="combo-pattern">${tokens}</div>
          <div class="combo-card-desc">${presentation.desc}</div>
          <div class="combo-card-desc">${uiText(`终结式：伤害 +${damagePct}% · 范围 +${reachPct}%`, `Finisher: +${damagePct}% damage · +${reachPct}% reach`)}</div>
        </article>`;
      }).join('');
    }

    function openComboList(fromPause = false) {
      const modal = document.getElementById('combo-list-modal');
      if (!modal || modal.style.display === 'flex') return;
      const pauseModal = document.getElementById('pause-modal');
      comboListOpenedFromPause = Boolean(fromPause && pauseModal?.style.display === 'flex');
      comboListResumeOnClose = Boolean(gameState.hasStarted && !gameState.isPaused);
      gameState.isPaused = true;
      clearHeldCombatInputs();
      if (comboListOpenedFromPause) pauseModal.style.display = 'none';
      renderComboList();
      modal.style.display = 'flex';
      document.getElementById('combo-list-close')?.focus();
    }

    function closeComboList() {
      const modal = document.getElementById('combo-list-modal');
      if (modal) modal.style.display = 'none';
      clearHeldCombatInputs();
      if (comboListOpenedFromPause) {
        document.getElementById('pause-modal').style.display = 'flex';
        document.querySelector('#pause-modal button')?.focus();
        gameState.isPaused = true;
      } else if (comboListResumeOnClose && gameState.hasStarted && !gameState.dialogueActive && !gameState.rewardSelectionActive && !gameState.bossOutcomeActive) {
        gameState.isPaused = false;
      }
      comboListOpenedFromPause = false;
      comboListResumeOnClose = false;
    }

    function showPauseMenu() {
      if (!gameState.hasStarted || isGameplayPaused()) return;
      gameState.isPaused = true;
      clearHeldCombatInputs();
      const info = document.getElementById('pause-checkpoint-info');
      if (info) info.innerText = uiText(
        `保存后将从第 ${gameState.chamberIndex} 章开头继续。本章内已经击败的敌人与首领会重新出现。`,
        `Your save will resume from the beginning of Chapter ${gameState.chamberIndex}. Enemies and bosses defeated during this chapter will return.`
      );
      document.getElementById('pause-modal').style.display = 'flex';
      document.querySelector('#pause-modal button')?.focus();
    }

    function resumeGame() {
      document.getElementById('pause-modal').style.display = 'none';
      if (gameState.hasStarted && !gameState.dialogueActive) gameState.isPaused = false;
    }

    function returnToTitle() {
      closeAllOverlays();
      gameState.hasStarted = false;
      gameState.isPaused = true;
      gameState.dialogueActive = false;
      gameState.rewardSelectionActive = false;
      gameState.bossOutcomeActive = false;
      gameState.bossOutcomeContinuation = null;
      gameState.deferredDialogueChapter = null;
      enemies = [];
      projectiles = [];
      fxList = [];
      monkeyClones = [];
      document.getElementById('tutorial-card').style.display = 'none';
      document.getElementById('start-screen').style.display = 'flex';
      refreshTitleUnlocks();
      updateHeroInterface();
      document.getElementById('start-game-btn').focus();
    }

    function updateHUD() {
      const hpPct = Math.max(0, player.hp / player.maxHp) * 100;
      const qiPct = Math.max(0, player.qi / player.maxQi) * 100;
      const awakenPct = Math.max(0, player.awakenGauge / player.maxAwakenGauge) * 100;
      updateAlignmentHUD();

      document.getElementById('hp-bar').style.width = `${hpPct}%`;
      document.getElementById('hp-text').innerText = `${Math.max(0, Math.round(player.hp))} / ${player.maxHp}`;
      const armorTotal = Math.max(0, Math.ceil((player.armor || 0) + (player.bullArmor || 0) + (player.masterworkArmor || 0) + (player.guanyinBarrier || 0) + (player.formBarrier || 0)));
      const hpLabel = document.getElementById('hp-label');
      if (hpLabel) hpLabel.innerText = uiText(`气血值 · 🛡 ${armorTotal}`, `Health · 🛡 ${armorTotal}`);

      document.getElementById('qi-bar').style.width = `${qiPct}%`;
      document.getElementById('qi-text').innerText = `${Math.round(player.qi)} / ${player.maxQi}`;

      document.getElementById('awaken-bar').style.width = `${awakenPct}%`;
      const awakenName = gameState.playableHero === 'erlang'
        ? uiText('天律觉醒', "Heaven's Law")
        : uiText('大闹天宫', 'Havoc Awakening');
      document.getElementById('awaken-text').innerText = player.isAwakened
        ? uiText(`觉醒中 (${Math.ceil(player.awakenDuration)}秒)`, `Awakened (${Math.ceil(player.awakenDuration)}s)`)
        : (awakenPct >= 100 ? uiText('觉醒就绪: 按 [G] 施展', 'Awakening Ready: Press [G]') : `${awakenName}: ${Math.round(awakenPct)}%`);

      document.getElementById('gold-val').innerText = gameState.gold;
      document.getElementById('ashes-val').innerText = gameState.ashes;
      document.getElementById('peaches-val').innerText = gameState.peachesEaten;

      const formLabelEl = document.getElementById('slot-hex-label');
      const formTagEl = document.getElementById('boon-tag-hex');
      if (formLabelEl && formTagEl) {
        if (gameState.playableHero === 'erlang') {
          formLabelEl.innerText = uiText('清源妙道法相', 'Clear-Origin Manifestation');
          formTagEl.innerText = player.isManifested
            ? uiText(`法相中 (${Math.ceil(player.manifestDuration)}秒)`, `Manifested (${Math.ceil(player.manifestDuration)}s)`)
            : (player.manifestCooldown > 0 ? uiText(`冷却: ${Math.ceil(player.manifestCooldown)}秒`, `Cooldown: ${Math.ceil(player.manifestCooldown)}s`) : uiText('天眼 · 神甲 · 犬袭', 'Third Eye · Divine Armor · Hound'));
        } else {
          const formNames = {
            dragon: { zh: '苍龙真身', en: 'Azure Dragon Form', subZh: '引雷控场', subEn: 'Storm Control' },
            tiger: { zh: '白虎战煞', en: 'White Tiger', subZh: '爆发流血', subEn: 'Burst Bleed' },
            roc: { zh: '金翅大鹏', en: 'Golden Roc', subZh: '风刃游击', subEn: 'Wind Skirmisher' },
            ape: { zh: '法天象地', en: 'Titan Ape', subZh: '霸体崩山', subEn: 'Mountain Breaker' },
            tortoise: { zh: '玄武真形', en: 'Black Tortoise', subZh: '减伤反击', subEn: 'Guard Counter' }
          };
          const cur = formNames[player.activeTransformationForm] || formNames.dragon;
          formLabelEl.innerText = uiText(cur.zh, cur.en);
          formTagEl.innerText = player.isTransformed
            ? uiText(`化身中 (${Math.ceil(player.transformDuration)}秒)`, `Transformed (${Math.ceil(player.transformDuration)}s)`)
            : (player.transformCooldown > 0 ? uiText(`冷却: ${Math.ceil(player.transformCooldown)}秒`, `Cooldown: ${Math.ceil(player.transformCooldown)}s`) : uiText(cur.subZh, cur.subEn));
        }
      }

      const updateSlot = (id, unavailable, badgeText) => {
        const slot = document.getElementById(id);
        if (!slot) return;
        slot.classList.toggle('unavailable', unavailable);
        const badge = slot.querySelector('.key-badge');
        if (badge) badge.innerText = badgeText;
      };
      updateSlot('slot-attack', player.attackCooldown > 0, player.attackCooldown > 0 ? `${uiText('左/右键', 'L/R')} · ${player.attackCooldown.toFixed(1)}s` : uiText('左键 + 右键', 'LMB + RMB'));
      if (gameState.playableHero === 'erlang') {
        const specialBusy = player.specialCooldown > 0 || player.houndCooldown > 0;
        const dogStatus = player.houndCooldown > 0 ? player.houndCooldown.toFixed(1) : uiText('就绪', 'Ready');
        const eyeStatus = player.specialCooldown > 0 ? player.specialCooldown.toFixed(1) : uiText('就绪', 'Ready');
        updateSlot('slot-special', specialBusy, `RMB ${dogStatus} · Q ${eyeStatus}`);
        updateSlot('slot-cast', player.castCooldown > 0 || player.qi < 65, player.qi < 65 ? uiText('E · 真气不足', 'E · Not Enough Qi') : (player.castCooldown > 0 ? `E · ${player.castCooldown.toFixed(1)}s` : uiText('E/审判阵 (65真气)', 'E · Judgment (65 Qi)')));
      } else {
        updateSlot('slot-special', player.specialCooldown > 0, player.specialCooldown > 0 ? `Q · ${player.specialCooldown.toFixed(1)}s` : uiText('Q / 单独右键', 'Q / Single RMB'));
        if (player.isTransformed) {
          const formSpells = {
            dragon: ['潜渊雷雨', 'Abyss Dive Storm'], tiger: ['虎啸撼岳', 'Mountain-Shaking Roar'], roc: ['天罡神风', 'Celestial Gale Cyclone'],
            ape: ['擎天怒砸', 'Pillar-Heaven Smash'], tortoise: ['幽通九泉', 'Nine-Springs Abyss']
          };
          const spell = formSpells[player.activeTransformationForm] || formSpells.dragon;
          const castLabel = document.querySelector('#slot-cast .slot-label');
          const castTag = document.getElementById('boon-tag-cast');
          if (castLabel) castLabel.innerText = gameState.language === 'en' ? spell[1] : spell[0];
          if (castTag) castTag.innerText = uiText('真身专属法术与技能树强化', 'Form-only spell · Skill-tree enhanced');
          updateSlot('slot-cast', player.castCooldown > 0 || player.qi < 45, player.qi < 45 ? uiText('E · 真气不足', 'E · Not Enough Qi') : (player.castCooldown > 0 ? `E · ${player.castCooldown.toFixed(1)}s` : uiText('E/真身法术 (45真气)', 'E · Form Spell (45 Qi)')));
        } else {
          const castLabel = document.querySelector('#slot-cast .slot-label');
          const castTag = document.getElementById('boon-tag-cast');
          if (castLabel) castLabel.innerText = uiText('吹毛成兵', 'Hair-Clone Spell');
          if (castTag) castTag.innerText = player.boons.cast ? `${player.boons.cast.name} · Lv.${player.boons.cast.level || 1}` : uiText('猴王分身', 'Monkey-King Clones');
          updateSlot('slot-cast', player.castCooldown > 0 || player.qi < 75, player.qi < 75 ? uiText('E · 真气不足', 'E · Not Enough Qi') : (player.castCooldown > 0 ? `E · ${player.castCooldown.toFixed(1)}s` : uiText('E/法术 (75真气)', 'E · Spell (75 Qi)')));
        }
      }
      const effectiveDashMax = player.maxDashCharges + player.getActiveFormSkillRank('roc_fly');
      updateSlot('slot-dash', player.dashCharges <= 0, `${uiText('空格/闪避', 'Space · Dodge')} · ${player.dashCharges}/${effectiveDashMax}`);
      if (gameState.playableHero === 'erlang') {
        updateSlot('slot-hex', player.manifestCooldown > 0, player.isManifested ? `R/F · ${Math.ceil(player.manifestDuration)}s` : (player.manifestCooldown > 0 ? `R/F · ${Math.ceil(player.manifestCooldown)}s` : uiText('R/F/清源法相', 'R/F · Manifest')));
      } else {
        updateSlot('slot-hex', player.transformCooldown > 0, player.isTransformed ? `R/F · ${Math.ceil(player.transformDuration)}s` : (player.transformCooldown > 0 ? `R/F · ${Math.ceil(player.transformCooldown)}s` : uiText('R/F/神兽化身', 'R/F · Beast Form')));
      }
      document.getElementById('lives-val').innerText = player.lives;

      if (gameState.chamberType === 'boss') {
        const livingBosses = enemies.filter(e => e.isBoss && e.alive && !e.isSubdued);
        if (livingBosses.length) {
          const combinedHp = livingBosses.reduce((sum, boss) => sum + Math.max(0, boss.hp), 0);
          const combinedMaxHp = livingBosses.reduce((sum, boss) => sum + boss.maxHp, 0);
          const bossPct = Math.max(0, combinedHp / Math.max(1, combinedMaxHp)) * 100;
          document.getElementById('boss-bar-fill').style.width = `${bossPct}%`;
        }
      }
    }

    // MAIN GAME LOOP & RENDERING
    let lastTime = 0;
    let worldHitStopRemaining = 0;

    function beginConfirmedMeleeHitStop(seconds) {
      worldHitStopRemaining = Math.max(worldHitStopRemaining, Math.max(0, Math.min(.11, seconds || 0)));
    }

    function isEffectAlive(effect) {
      if (typeof effect.alpha === 'number') return effect.alpha > 0;
      if (typeof effect.duration === 'number') return effect.duration > 0;
      if (typeof effect.life === 'number') return effect.life > 0;
      return true;
    }

    function isGroundEffect(effect) {
      return effect instanceof GroundFissureFX
        || effect instanceof HadesMagicCircleAOEFX
        || effect instanceof TransformationSpellFX
        || effect instanceof FormPulseDamageFX
        || effect instanceof KnockdownDustFX
        || effect instanceof PortalSummonFX
        || effect instanceof RuyiStaffSpecialSlamFX
        || (effect instanceof BossSkillAnimatedFX && effect.ground);
    }

    function getEnemyCrowdRadius(enemy) {
      // Campaign sprites occupy more screen space than their combat hit circles.
      // Use a visual-footprint radius here so a boss cannot hide an entire minion.
      if (enemy.campaignSheet) {
        return Math.max(enemy.radius, 58 * enemy.campaignScale);
      }
      return Math.max(18, enemy.radius * 0.95);
    }

    const ENEMY_CROWD_GRID_SIZE = 192;
    const enemyCrowdGrid = new Map();
    const crowdLiving = [];
    const crowdRadii = [];

    function resolveEnemyCrowding() {
      crowdLiving.length = 0;
      crowdRadii.length = 0;
      for (let i = 0; i < enemies.length; i++) {
        const enemy = enemies[i];
        if (!enemy.alive || enemy.isDying) continue;
        crowdLiving.push(enemy);
        crowdRadii.push(getEnemyCrowdRadius(enemy));
      }
      if (crowdLiving.length < 2) return;

      // Tripled waves made the former all-pairs solver grow quadratically. A
      // reusable spatial grid restricts checks to neighboring cells while keeping
      // the same two-pass separation and heavyweight-boss behavior.
      for (let pass = 0; pass < 2; pass++) {
        enemyCrowdGrid.forEach(bucket => { bucket.length = 0; });
        for (let i = 0; i < crowdLiving.length; i++) {
          const enemy = crowdLiving[i];
          const cellX = Math.floor(enemy.x / ENEMY_CROWD_GRID_SIZE);
          const cellY = Math.floor(enemy.y / ENEMY_CROWD_GRID_SIZE);
          const key = (cellX + 32) * 128 + (cellY + 32);
          let bucket = enemyCrowdGrid.get(key);
          if (!bucket) {
            bucket = [];
            enemyCrowdGrid.set(key, bucket);
          }
          bucket.push(i);
        }

        for (let i = 0; i < crowdLiving.length; i++) {
          const a = crowdLiving[i];
          const cellX = Math.floor(a.x / ENEMY_CROWD_GRID_SIZE);
          const cellY = Math.floor(a.y / ENEMY_CROWD_GRID_SIZE);
          for (let offsetX = -1; offsetX <= 1; offsetX++) {
            for (let offsetY = -1; offsetY <= 1; offsetY++) {
              const key = (cellX + offsetX + 32) * 128 + (cellY + offsetY + 32);
              const bucket = enemyCrowdGrid.get(key);
              if (!bucket?.length) continue;
              for (let candidate = 0; candidate < bucket.length; candidate++) {
                const j = bucket[candidate];
                if (j <= i) continue;
                const b = crowdLiving[j];
                let dx = b.x - a.x;
                let dy = b.y - a.y;
                let distSq = dx * dx + dy * dy;
                const minDist = crowdRadii[i] + crowdRadii[j];
                if (distSq >= minDist * minDist) continue;

                if (distSq < 0.0001) {
                  const angle = ((i * 37 + j * 101) % 360) * Math.PI / 180;
                  dx = Math.cos(angle);
                  dy = Math.sin(angle);
                  distSq = 1;
                }

                const dist = Math.sqrt(distSq);
                const nx = dx / dist;
                const ny = dy / dist;
                const correction = (minDist - dist) * 0.62;
                const massA = Math.max(1, a.radius / 24) * (a.isBoss ? 4 : 1);
                const massB = Math.max(1, b.radius / 24) * (b.isBoss ? 4 : 1);
                const moveA = massB / (massA + massB);
                const moveB = massA / (massA + massB);

                a.x -= nx * correction * moveA;
                a.y -= ny * correction * moveA;
                b.x += nx * correction * moveB;
                b.y += ny * correction * moveB;
                a.clampBoundary();
                b.clampBoundary();
              }
            }
          }
        }
      }
    }

    function gameLoop(currentTime) {
      requestAnimationFrame(gameLoop);

      try {
        if (!lastTime) lastTime = currentTime;
        const dt = Math.min(0.05, (currentTime - lastTime) / 1000);
        lastTime = currentTime;

        if (!isGameplayPaused() && worldHitStopRemaining > 0) {
          // Rendering continues below while every gameplay clock is held on
          // the generated contact pose. Whiffs never enter this branch because
          // only resolvePendingAttack's confirmed-hit feedback starts it.
          worldHitStopRemaining = Math.max(0, worldHitStopRemaining - dt);
        } else if (!isGameplayPaused()) {
          player.update(dt);

          monkeyClones.forEach(c => c.update(dt));
          monkeyClones = monkeyClones.filter(c => c.alive);

          speechBubbles.forEach(sb => sb.update(dt));
          speechBubbles = speechBubbles.filter(sb => sb.duration > 0);

          enemies.forEach(e => e.update(dt));
          resolveEnemyCrowding();
          enemies = enemies.filter(e => e.alive || (e.isDying && e.deathTimer > 0));

          if (activeLubanAvatar) activeLubanAvatar.update(dt);
          if (activeClockworkKite) {
            activeClockworkKite.update(dt);
            if (!activeClockworkKite.alive) activeClockworkKite = null;
          }

          projectiles.forEach(p => p.update(dt));
          projectiles = projectiles.filter(p => p.alive);

          fxList.forEach(fx => fx.update(dt));
          fxList = fxList.filter(isEffectAlive);

          floatingTexts.forEach(ft => ft.update(dt));
          floatingTexts = floatingTexts.filter(ft => ft.alpha > 0);

          updateChamberSpawner(dt);
          checkChamberClear();
          gameState.hudTimer = (gameState.hudTimer || 0) + dt;
          if (gameState.hudTimer >= 0.1) {
            gameState.hudTimer = 0;
            updateHUD();
          }

          if (gameState.chamberCleared) {
            exitGates.forEach(gate => {
              const dist = Math.hypot(player.x - gate.x, player.y - gate.y);
              if (dist <= gate.radius + player.radius) {
                if (gate.rewardType === 'god') {
                  openGodBoonModal(gate.godKey);
                } else if (gate.rewardType === 'peach') {
                  openPeachModal();
                } else if (gate.rewardType === 'shop') {
                  openShopModal(true);
                } else if (gate.rewardType === 'heart') {
                  player.increaseRunMaxHp(30, 30);
                  sound.playJadeChime();
                  floatingTexts.push(new FloatingText(player.x, player.y - 40, uiText('气血上限 +30!', 'Maximum Health +30!'), '#10b981'));
                } else if (gate.rewardType === 'ashes') {
                  gameState.ashes += 25;
                  sound.playJadeChime();
                  floatingTexts.push(new FloatingText(player.x, player.y - 40, uiText('功德灵砂 +25!', 'Merit Sand +25!'), '#c084fc'));
                }

                if (gameState.chamberIndex === gameState.totalChambers && !enemies.some(e => e.isFinalBoss && e.alive)) {
                  handleGameOver(true);
                } else {
                  startChamber(gameState.chamberIndex + 1);
                }
              }
            });
          }
        }

        // Render Canvas
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.setTransform(deviceScale, 0, 0, deviceScale, 0, 0);
        ctx.imageSmoothingEnabled = false;

        ctx.save();
        let shakeX = 0;
        let shakeY = 0;
        if (gameState.screenShake > 0) {
          shakeX = (Math.random() * 2 - 1) * gameState.screenShake;
          shakeY = (Math.random() * 2 - 1) * gameState.screenShake;
          gameState.screenShake = Math.max(0, gameState.screenShake - dt * SCREEN_SHAKE_DECAY_PER_SECOND);
        }

        // Align the camera to real backing pixels. Fractional nearest-neighbor
        // translations made the detailed floor shimmer and feel like movement lag.
        const cameraOffsetX = Math.round((viewWidth / 2 - player.x + shakeX) * deviceScale) / deviceScale;
        const cameraOffsetY = Math.round((viewHeight / 2 - player.y + shakeY) * deviceScale) / deviceScale;
        ctx.translate(cameraOffsetX, cameraOffsetY);

        // 1. Draw Expansive Celestial Palace Battlefield (2400 x 1800)
        const arenaW = 2400;
        const arenaH = 1800;
        const halfW = arenaW / 2;
        const halfH = arenaH / 2;

        ctx.imageSmoothingEnabled = true;
        const campaignFloor = loadedImages['campaign_biomes'];
        const pilgrimageFloor = loadedImages['campaign_pilgrimage_biomes'];
        const finalJourneyFloor = loadedImages['campaign_final_biomes'];
        const floorImg = loadedImages['seamless_floor'];
        const requestedAtlasIndex = Math.max(0, Math.min(2, Math.floor((gameState.campaignBiome || 0) / 9)));
        const campaignAtlases = [campaignFloor, pilgrimageFloor, finalJourneyFloor];
        const requestedCampaignFloor = campaignAtlases[requestedAtlasIndex];
        const activeCampaignFloor = requestedCampaignFloor && requestedCampaignFloor.complete && requestedCampaignFloor.naturalWidth > 0
          ? requestedCampaignFloor : campaignFloor;
        if (activeCampaignFloor && activeCampaignFloor.complete && activeCampaignFloor.naturalWidth > 0) {
          const cellSize = activeCampaignFloor.naturalWidth / 3;
          const atlasOffset = activeCampaignFloor === finalJourneyFloor ? 18 : (activeCampaignFloor === pilgrimageFloor ? 9 : 0);
          const biomeIndex = Math.max(0, Math.min(8, (gameState.campaignBiome || 0) - atlasOffset));
          const biomeCol = biomeIndex % 3;
          const biomeRow = Math.floor(biomeIndex / 3);
          ctx.drawImage(activeCampaignFloor, biomeCol * cellSize, biomeRow * cellSize, cellSize, cellSize, -halfW, -halfH, arenaW, arenaH);
          const edgeShade = ctx.createRadialGradient(0, 0, 260, 0, 0, 1350);
          edgeShade.addColorStop(0, 'rgba(0,0,0,0.02)');
          edgeShade.addColorStop(1, 'rgba(4,3,12,0.48)');
          ctx.fillStyle = edgeShade;
          ctx.fillRect(-halfW, -halfH, arenaW, arenaH);
        } else if (floorImg && floorImg.complete && floorImg.naturalWidth > 0) {
          const tileS = 600;
          for (let tx = -halfW; tx < halfW; tx += tileS) {
            for (let ty = -halfH; ty < halfH; ty += tileS) {
              ctx.drawImage(floorImg, tx, ty, Math.min(tileS, halfW - tx), Math.min(tileS, halfH - ty));
            }
          }
        } else {
          ctx.fillStyle = '#161026';
          ctx.fillRect(-halfW, -halfH, arenaW, arenaH);
        }
        ctx.imageSmoothingEnabled = false;

        // Arena edge follows the chapter palette instead of forcing palace gold
        // onto forests, sea floors, mountains, and pilgrimage wilderness.
        const stageAccent = getCampaignStage(gameState.chamberIndex).accent;
        ctx.strokeStyle = stageAccent;
        ctx.lineWidth = 10;
        ctx.strokeRect(-halfW, -halfH, arenaW, arenaH);

        ctx.strokeStyle = stageAccent;
        ctx.globalAlpha = 0.46;
        ctx.lineWidth = 4;
        ctx.strokeRect(-halfW + 16, -halfH + 16, arenaW - 32, arenaH - 32);
        ctx.globalAlpha = 1;

        // Corner Imperial Pillars
        const cornerSize = 48;
        const corners = [
          [-halfW, -halfH], [halfW - cornerSize, -halfH],
          [-halfW, halfH - cornerSize], [halfW - cornerSize, halfH - cornerSize]
        ];
        corners.forEach(([cx, cy]) => {
          ctx.fillStyle = stageAccent;
          ctx.fillRect(cx, cy, cornerSize, cornerSize);
          ctx.strokeStyle = '#fef08a';
          ctx.lineWidth = 3;
          ctx.strokeRect(cx, cy, cornerSize, cornerSize);
        });

        // 2. Draw Exit Gates. Keep the reward field visually neutral: the
        // former player-side arrow looked like it recommended one boon.
        if (gameState.chamberCleared) {
          exitGates.forEach(gate => {
            ctx.save();
            ctx.translate(gate.x, gate.y);

            const pulse = 1 + Math.sin(Date.now() * 0.006) * 0.08;
            ctx.beginPath();
            ctx.arc(0, 0, gate.radius * pulse, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(230, 180, 80, 0.35)';
            ctx.fill();
            ctx.strokeStyle = '#facc15';
            ctx.lineWidth = 5;
            ctx.shadowColor = '#facc15';
            ctx.shadowBlur = 20;
            ctx.stroke();

            const rewImg = loadedImages['reward_icons'];
            if (rewImg && rewImg.complete && rewImg.naturalWidth > 0) {
              let col = 0, row = 0;
              if (gate.rewardType === 'peach') { col = 0; row = 0; }
              else if (gate.rewardType === 'shop') { col = 1; row = 0; }
              else if (gate.rewardType === 'heart') { col = 0; row = 1; }
              else if (gate.rewardType === 'ashes') { col = 1; row = 1; }
              else if (gate.rewardType === 'god') {
                const isLuban = gate.godKey === 'luban';
                const isBuddha = gate.godKey === 'buddha';
                const godsImg = isLuban ? loadedImages['luban_avatar'] : (isBuddha ? loadedImages['buddha_colossal'] : loadedImages['all_10_gods']);
                if (godsImg && godsImg.complete && godsImg.naturalWidth > 0) {
                  if (isLuban) {
                    ctx.drawImage(godsImg, 0, 128, 128, 128, -38, -38, 76, 76);
                  } else if (isBuddha) {
                    ctx.drawImage(godsImg, 0, 0, 256, 256, -38, -38, 76, 76);
                  } else {
                    const gGod = GODS[gate.godKey] || GODS['erlangshen'];
                    const gCol = gGod.portraitCol !== undefined ? gGod.portraitCol : 0;
                    const gRow = gGod.portraitRow !== undefined ? gGod.portraitRow : 0;
                    const gW = godsImg.naturalWidth / 6;
                    const gH = godsImg.naturalHeight / 2;
                    ctx.drawImage(godsImg, gCol * gW, gRow * gH, gW, gH, -38, -38, 76, 76);
                  }
                }
              }

              if (gate.rewardType !== 'god' && gameState.language === 'en') {
                const rewardGlyphs = { peach: '🍑', shop: '🏺', heart: '❤️', ashes: '✨' };
                ctx.font = '42px "Segoe UI Emoji", sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.shadowColor = 'rgba(250,204,21,.75)';
                ctx.shadowBlur = 9;
                ctx.fillText(rewardGlyphs[gate.rewardType] || '✦', 0, 0);
                ctx.textBaseline = 'alphabetic';
              } else if (gate.rewardType !== 'god') {
                const rW = rewImg.naturalWidth / 2;
                const rH = rewImg.naturalHeight / 2;
                ctx.drawImage(rewImg, col * rW, row * rH, rW, rH, -38, -38, 76, 76);
              }
            }

            ctx.font = getCanvasFont(16, 700);
            ctx.fillStyle = '#fff2a8';
            ctx.textAlign = 'center';
            ctx.shadowColor = '#000';
            ctx.shadowBlur = 8;
            const gateLabel = gameState.language === 'en' ? translateGameText(gate.label) : gate.label;
            const labelParts = gateLabel.includes(' (') ? gateLabel.replace(' (', '\\n(').split('\\n') : [gateLabel];
            labelParts.slice(0, 2).forEach((part, line) => {
              ctx.fillText(part, 0, -gate.radius - 14 + line * 19, Math.max(120, Math.min(280, viewWidth * 0.42)));
            });

            ctx.restore();
          });
        }

        // 3. Ground effects sit below characters; actors are depth-sorted by feet.
        for (let i = 0; i < fxList.length; i++) if (isGroundEffect(fxList[i])) fxList[i].draw(ctx);
        renderActors.length = 0;
        for (let i = 0; i < monkeyClones.length; i++) renderActors.push({ entity: monkeyClones[i], y: monkeyClones[i].y });
        renderActors.push({ entity: player, y: player.y });
        for (let i = 0; i < enemies.length; i++) renderActors.push({ entity: enemies[i], y: enemies[i].y });
        if (activeLubanAvatar) renderActors.push({ entity: activeLubanAvatar, y: activeLubanAvatar.y });
        if (activeClockworkKite) renderActors.push({ entity: activeClockworkKite, y: activeClockworkKite.y });
        renderActors.sort((a, b) => a.y - b.y);
        for (let i = 0; i < renderActors.length; i++) renderActors[i].entity.draw(ctx);
        projectiles.forEach(p => p.draw(ctx));
        speechBubbles.forEach(sb => sb.draw(ctx));
        for (let i = 0; i < fxList.length; i++) if (!isGroundEffect(fxList[i])) fxList[i].draw(ctx);
        floatingTexts.forEach(ft => ft.draw(ctx));

        ctx.restore();
      } catch (err) {
        console.error("Game loop render error:", err);
      }
    }

    // Launch Game
    player.resetForRun();
    gameState.isPaused = true;
    gameState.hasStarted = false;
    applyGameLanguage();
    refreshTitleUnlocks();
    updateHeroInterface();
    document.getElementById('start-game-btn').focus();
    requestAnimationFrame(gameLoop);
  </script>
</body>
</html>
"""

final_html = (
    html_template
    .replace('%ASSETS_JSON%', json.dumps(b64_data))
    .replace('%RUYI_GRIP_ANCHORS%', json.dumps(ruyi_grip_anchors, separators=(',', ':')))
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"Successfully compiled index.html with clean DOM and JavaScript ({len(final_html)} bytes)!")
