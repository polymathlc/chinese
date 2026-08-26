"""
Journey to the West: From Cave to Heaven & Showdown with Tongbei Yuanhou
(西游记：大闹天宫与通臂之决 - 100% 简体中文 180重天史诗动作肉鸽 - 浏览器与 GitHub Pages 极速稳定版)
"""

import os
import json
import base64

# Load all webp assets
assets_keys = [
    'hero',
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

print(f"Loaded {len(b64_data)} embedded assets.")

# HTML / CSS / JS Template for Journey to the West
html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>西游记：大闹天宫与通臂之决 (180重天动作肉鸽)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
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

    /* UI Layer Overlay */
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

    /* Top HUD */
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
      width: 360px;
      filter: drop-shadow(0 4px 14px rgba(0,0,0,0.95));
    }

    .hero-tag {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 2px;
    }

    .hero-name {
      font-family: var(--font-chinese);
      font-size: 22px;
      font-weight: 900;
      color: var(--gold-light);
      letter-spacing: 2px;
      text-shadow: 0 0 10px rgba(230, 180, 80, 0.8);
    }

    .hero-title {
      font-family: var(--font-chinese);
      font-size: 15px;
      color: #f87171;
      margin-left: 4px;
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

    /* Top Center: Chamber / Biome Banner */
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
      text-shadow: 0 0 14px rgba(230, 180, 80, 0.8);
    }

    .chamber-subtitle {
      font-family: var(--font-chinese);
      font-size: 16px;
      color: #e2e8f0;
      letter-spacing: 1.5px;
      margin-top: 3px;
    }

    /* Currency & Meta Panel */
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

    /* Boss HUD */
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

    /* Bottom Controls HUD */
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
      width: 68px;
      height: 68px;
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
      max-width: 62px;
    }

    /* Right Quick Buttons */
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

    /* Modals Overlay */
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

    /* Cards Grid */
    .boon-cards-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      width: 100%;
      margin-top: 10px;
    }

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
    }

    .boon-card:hover {
      border-color: var(--gold-primary);
      transform: translateY(-4px);
      box-shadow: 0 0 20px rgba(230, 180, 80, 0.6);
      background: linear-gradient(180deg, rgba(55, 36, 85, 0.95), rgba(22, 16, 35, 0.95));
    }

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

    /* Altar Grid */
    .altar-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      width: 100%;
      margin-top: 14px;
    }

    .altar-item {
      background: rgba(22, 16, 35, 0.9);
      border: 2px solid var(--gold-dark);
      border-radius: 8px;
      padding: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .altar-info {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .altar-name {
      font-family: var(--font-chinese);
      font-size: 16px;
      font-weight: 700;
      color: var(--gold-light);
    }

    .altar-desc {
      font-family: var(--font-body);
      font-size: 12px;
      color: #94a3b8;
    }

    .altar-level {
      font-family: var(--font-chinese);
      font-size: 13px;
      color: #4ade80;
    }

    .altar-btn {
      background: linear-gradient(180deg, #7c3aed, #4c1d95);
      border: 1px solid #c084fc;
      color: #fff;
      font-family: var(--font-chinese);
      font-size: 13px;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 6px;
      cursor: pointer;
      white-space: nowrap;
    }

    .altar-btn:hover {
      box-shadow: 0 0 10px #c084fc;
    }

    .altar-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    /* Codex Grid */
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

    /* Close Button */
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

    /* Game Over / Victory Modal */
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
  </style>
</head>
<body>
  <div id="game-container">
    <canvas id="gameCanvas"></canvas>

    <div id="ui-layer">
      <!-- Top HUD -->
      <div class="top-hud">
        <div class="player-bars">
          <div class="hero-tag">
            <span class="hero-name">齐天大圣 · 孙悟空</span>
            <span class="hero-title">如意金箍棒 · 一万三千五百斤</span>
          </div>
          <div class="bar-wrapper">
            <div id="hp-bar" class="bar-fill health" style="width: 100%;"></div>
            <div class="bar-text"><span>气血值 (生命)</span><span id="hp-text">100 / 100</span></div>
          </div>
          <div class="bar-wrapper">
            <div id="qi-bar" class="bar-fill qi" style="width: 100%;"></div>
            <div class="bar-text"><span>混元真气 (法力)</span><span id="qi-text">50 / 50</span></div>
          </div>
          <div class="bar-wrapper" style="height: 16px;">
            <div id="awaken-bar" class="bar-fill awakening" style="width: 0%;"></div>
            <div class="bar-text" style="font-size: 10px;"><span>大闹天宫觉醒</span><span id="awaken-text">蓄力中: 按 [R/F] 施展</span></div>
          </div>
        </div>

        <div class="top-center-hud">
          <div id="chamber-name" class="chamber-title">花果山水帘洞与盘丝岭 · 第 1 重天 / 180 重天</div>
          <div id="chamber-sub" class="chamber-subtitle">仙石初辟悟大道 · 降妖除魔登九霄</div>
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

      <!-- Boss HUD -->
      <div id="boss-hud" class="boss-bar-container">
        <div id="boss-name-text" class="boss-name">盘丝洞·蜘蛛精七仙姑</div>
        <div class="boss-bar-wrapper">
          <div id="boss-bar-fill" class="boss-bar-fill" style="width: 100%;"></div>
        </div>
      </div>

      <!-- Bottom HUD -->
      <div class="bottom-hud">
        <div class="action-slots">
          <div class="action-slot active" id="slot-attack">
            <div class="key-badge">左键/普攻</div>
            <div class="slot-label">金箍棒击</div>
            <div class="slot-boon" id="boon-tag-attack">神针横扫</div>
          </div>
          <div class="action-slot" id="slot-special">
            <div class="key-badge">右键/Q/特殊</div>
            <div class="slot-label">定海神柱</div>
            <div class="slot-boon" id="boon-tag-special">重岳劈地</div>
          </div>
          <div class="action-slot" id="slot-cast">
            <div class="key-badge">E/法术</div>
            <div class="slot-label">定身神咒</div>
            <div class="slot-boon" id="boon-tag-cast">八卦法阵</div>
          </div>
          <div class="action-slot" id="slot-dash">
            <div class="key-badge">空格/闪避</div>
            <div class="slot-label">筋斗云遁</div>
            <div class="slot-boon" id="boon-tag-dash">浮光掠影</div>
          </div>
          <div class="action-slot" id="slot-hex">
            <div class="key-badge">R/F/觉醒</div>
            <div class="slot-label">法天象地</div>
            <div class="slot-boon" id="boon-tag-hex">齐天狂暴</div>
          </div>
        </div>

        <div class="quick-buttons">
          <button class="btn-hud" onclick="openAltarOfTransformations()">📜 七十二变神通谱</button>
          <button class="btn-hud" onclick="openSkillCodex()">📖 西游万神伏魔录</button>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <!-- 1. Chinese Gods Boon Modal -->
    <div id="boon-modal" class="modal-overlay">
      <div class="modal-box">
        <div class="modal-header">
          <div id="god-portrait" class="modal-god-portrait"></div>
          <div id="god-name" class="modal-title">二郎显圣真君·杨戬</div>
          <div id="god-title" class="modal-subtitle">天眼洞察 · 执掌九天刑罚神律</div>
          <div id="god-quote" class="modal-quote">“泼猴，接本君三尖两刃枪之威！荡尽三界妖邪，休得阻碍西行正道！”</div>
        </div>
        <div id="boon-choices-container" class="boon-cards-grid">
        </div>
      </div>
    </div>

    <!-- 2. Heavenly Peaches of Immortality Modal -->
    <div id="pom-modal" class="modal-overlay">
      <div class="modal-box">
        <div class="modal-header">
          <div id="peach-modal-icon" style="width: 110px; height: 110px; border-radius: 50%; border: 3px solid var(--peach-pink); box-shadow: 0 0 24px rgba(251, 113, 133, 0.8); margin: 0 auto 12px; background-size: 200%; background-position: 0 0;"></div>
          <div class="modal-title" style="color: var(--peach-pink);">王母天庭蟠桃盛宴 (仙桃延寿)</div>
          <div class="modal-subtitle">三千年一熟，人吃了体健身轻，道法大进</div>
          <div class="modal-quote">“服食一枚仙桃，顿增三千年道行功力！请选择一项已修习的神通提升品阶境界。”</div>
        </div>
        <div id="pom-choices-container" class="boon-cards-grid">
        </div>
      </div>
    </div>

    <!-- 3. Dragon King's Treasury & Earth God Pavilion (Shop) -->
    <div id="shop-modal" class="modal-overlay">
      <div class="modal-box">
        <div class="modal-header">
          <div style="font-size: 52px; margin-bottom: 8px;">🏮</div>
          <div class="modal-title" style="color: #facc15;">东海龙宫珍宝阁与土地神坛</div>
          <div class="modal-subtitle">以灵石换取仙家丹药与通天至宝</div>
        </div>
        <div id="shop-choices-container" class="boon-cards-grid">
        </div>
        <button class="modal-close-btn" onclick="closeShopModal()">离开宝阁</button>
      </div>
    </div>

    <!-- 4. Altar of 72 Transformations (Meta Progression) -->
    <div id="altar-modal" class="modal-overlay">
      <div class="modal-box">
        <div class="modal-header">
          <div class="modal-title" style="color: #c084fc;">七十二变·地煞神通谱</div>
          <div class="modal-subtitle">消耗历练所得功德灵砂，淬炼肉身，铸就不朽仙体</div>
        </div>
        <div id="altar-items-container" class="altar-grid">
        </div>
        <button class="modal-close-btn" onclick="closeAltarModal()">继续西行</button>
      </div>
    </div>

    <!-- 5. Codex of Immortals & Demons -->
    <div id="codex-modal" class="modal-overlay">
      <div class="modal-box">
        <div class="modal-header">
          <div class="modal-title">西游万神伏魔录 (仙圣仙缘宝典)</div>
          <div class="modal-subtitle">收录三界十大神仙与一百零八式通天神通</div>
        </div>
        <div id="codex-cards-container" class="codex-grid">
        </div>
        <button class="modal-close-btn" onclick="closeSkillCodex()">合上宝典</button>
      </div>
    </div>

    <!-- 6. Game Over / Victory Modal -->
    <div id="gameover-modal" class="modal-overlay">
      <div class="modal-box gameover-box">
        <div id="gameover-title" class="gameover-title defeat">道消身殒</div>
        <div id="gameover-sub" class="modal-subtitle">形骸虽散，神魂不灭。且回花果山水帘洞潜心参悟七十二变！</div>
        <div class="stats-summary">
          <div class="stat-row"><span>已破重天关卡:</span><span id="stat-chambers" class="stat-val">1</span></div>
          <div class="stat-row"><span>斩灭妖魔法相:</span><span id="stat-kills" class="stat-val">0</span></div>
          <div class="stat-row"><span>领悟仙圣神通:</span><span id="stat-boons" class="stat-val">0</span></div>
          <div class="stat-row"><span>服食天庭蟠桃:</span><span id="stat-peaches" class="stat-val">0</span></div>
          <div class="stat-row"><span>积攒功德灵砂:</span><span id="stat-ashes" class="stat-val">0</span></div>
        </div>
        <button class="btn-hud" style="font-size: 16px; padding: 10px 36px;" onclick="restartRun()">再战三界 · 重新启程</button>
      </div>
    </div>

  </div>

  <script>
    // Embedded Base64 Assets
    const ASSETS = %ASSETS_JSON%;
    const loadedImages = {};
    let loadedCount = 0;
    const totalAssets = Object.keys(ASSETS).length;

    for (let key in ASSETS) {
      const img = new Image();
      img.src = ASSETS[key];
      img.onload = () => {
        loadedCount++;
      };
      loadedImages[key] = img;
    }

    // ==========================================
    // SOUND SYNTHESIZER (Web Audio API)
    // Chinese Mythological Martial Soundscape
    // ==========================================
    class SoundEngine {
      constructor() {
        this.ctx = null;
        this.isMuted = false;
      }

      init() {
        if (!this.ctx) {
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          this.ctx = new AudioContext();
        }
        if (this.ctx.state === 'suspended') {
          this.ctx.resume();
        }
      }

      playStaffSwing() {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          const filter = this.ctx.createBiquadFilter();

          osc.type = 'sine';
          osc.frequency.setValueAtTime(340, t);
          osc.frequency.exponentialRampToValueAtTime(140, t + 0.14);

          filter.type = 'lowpass';
          filter.frequency.setValueAtTime(900, t);

          gain.gain.setValueAtTime(0.3, t);
          gain.gain.linearRampToValueAtTime(0.01, t + 0.14);

          osc.connect(filter);
          filter.connect(gain);
          gain.connect(this.ctx.destination);

          osc.start(t);
          osc.stop(t + 0.14);
        } catch(e) {}
      }

      playStaffHit() {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const osc1 = this.ctx.createOscillator();
          const gain1 = this.ctx.createGain();
          osc1.type = 'triangle';
          osc1.frequency.setValueAtTime(620, t);
          osc1.frequency.exponentialRampToValueAtTime(220, t + 0.18);
          gain1.gain.setValueAtTime(0.45, t);
          gain1.gain.exponentialRampToValueAtTime(0.001, t + 0.18);
          osc1.connect(gain1);
          gain1.connect(this.ctx.destination);
          osc1.start(t);
          osc1.stop(t + 0.18);

          const osc2 = this.ctx.createOscillator();
          const gain2 = this.ctx.createGain();
          osc2.type = 'sine';
          osc2.frequency.setValueAtTime(140, t);
          osc2.frequency.exponentialRampToValueAtTime(45, t + 0.22);
          gain2.gain.setValueAtTime(0.55, t);
          gain2.gain.exponentialRampToValueAtTime(0.001, t + 0.22);
          osc2.connect(gain2);
          gain2.connect(this.ctx.destination);
          osc2.start(t);
          osc2.stop(t + 0.22);
        } catch(e) {}
      }

      playStaffSmash() {
        if (!this.ctx) return;
        try {
          const t = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(240, t);
          osc.frequency.exponentialRampToValueAtTime(30, t + 0.45);

          gain.gain.setValueAtTime(0.65, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.45);

          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(t);
          osc.stop(t + 0.45);
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
            osc.frequency.exponentialRampToValueAtTime(freq * 0.96, t + 1.8);

            gain.gain.setValueAtTime(0.28 / (idx + 1), t);
            gain.gain.exponentialRampToValueAtTime(0.0001, t + 1.8);

            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(t);
            osc.stop(t + 1.8);
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

    // ==========================================
    // 10 CHINESE IMMORTALS & 100 BOONS (SIMPLIFIED CHINESE)
    // ==========================================
    const GODS = {
      erlangshen: {
        name: '二郎显圣真君·杨戬',
        title: '灌江口昭惠显圣二郎真君',
        portraitIndex: 0,
        color: '#facc15',
        quotes: [
          '“泼猴，接本君三尖两刃枪之威！荡尽三界妖邪，休得阻碍西行正道！”',
          '“天眼洞察三界虚妄，九天神雷听吾敕令！受死！”'
        ],
        boons: [
          { id: 'erlang_strike', name: '天眼破军击', slot: '普通攻击', desc: '【普攻】金箍棒挥击召唤九天真雷神矛，造成 45 点额外神圣真实伤害并附加破军易伤。' },
          { id: 'erlang_ring', name: '洞察真光阵', slot: '法术法阵', desc: '【法阵】法阵内显化天眼神威，使敌方受到的所有伤害提升 40%，并不停发射天眼极光脉冲。' },
          { id: 'erlang_dash', name: '疾雷瞬身步', slot: '闪避身法', desc: '【闪避】施展筋斗云时在原地降下惩戒神雷，对周围造成 40 点雷电范围伤害。' },
          { id: 'erlang_special', name: '裂天三尖斩', slot: '特殊攻击', desc: '【特殊】定海神针重劈释放开天辟地的金色枪芒冲击波，贯穿沿途所有敌人并造成 75 伤害。' },
          { id: 'erlang_hound', name: '哮天犬噬魂', slot: '被动·仙宠', desc: '【被动】暴击时召唤哮天犬扑咬目标，造成 120 伤害并强制眩晕目标 1 秒。' },
          { id: 'erlang_truesight', name: '火眼天眼合一', slot: '被动·暴击', desc: '【被动】全攻击暴击几率提升 25%，暴击伤害提升 50%。' },
          { id: 'erlang_execute', name: '真君诛邪诀', slot: '被动·斩杀', desc: '【被动】对生命值低于 20% 的敌人造成 3 倍真实伤害。' },
          { id: 'erlang_lance', name: '神锋追魂', slot: '被动·飞枪', desc: '【被动】特殊攻击额外发射 3 柄自动索敌的金色神枪，每柄造成 35 伤害。' },
          { id: 'erlang_wrath', name: '三界神威', slot: '被动·受击', desc: '【被动】受到伤害时瞬间释放全屏强光，使全场敌人致盲眩晕 1.5 秒。' },
          { id: 'erlang_apotheosis', name: '天界战神降世', slot: '被动·觉醒', desc: '【被动】法天象地大闹天宫觉醒持续时间延长 50%，且常驻提升 30% 攻击速度。' }
        ]
      },
      guanyin: {
        name: '南海大悲观世音菩萨',
        title: '大慈大悲救苦救难观世音',
        portraitIndex: 1,
        color: '#34d399',
        quotes: [
          '“悟空，心如明镜，方显神通。慈悲大海，能渡一切苦厄。”',
          '“受此玉净瓶杨柳甘露，愿你金身不坏，西行圆满。”'
        ],
        boons: [
          { id: 'guanyin_strike', name: '净瓶甘露击', slot: '普通攻击', desc: '【普攻】金箍棒命中敌人时恢复自身 4 点气血，并瞬间驱散身上所有负面状态。' },
          { id: 'guanyin_ring', name: '九品莲台阵', slot: '法术法阵', desc: '【法阵】召唤圣洁莲花阵，每秒为悟空恢复 8 点气血，并将阵内敌人移速降低 50%。' },
          { id: 'guanyin_dash', name: '杨柳清风步', slot: '闪避身法', desc: '【闪避】施展筋斗云时获得翡翠玉露护盾，吸收最多 30 点伤害，持续 2.5 秒。' },
          { id: 'guanyin_special', name: '慈悲普度澜', slot: '特殊攻击', desc: '【特殊】特殊攻击释放浩瀚慈悲佛光，反弹一切敌方弹幕并恢复 15 点真气。' },
          { id: 'guanyin_nirvana', name: '涅槃不灭金身', slot: '被动·保命', desc: '【被动】金身复活次数 +1，复活时恢复 70% 最大生命值与全部真气。' },
          { id: 'guanyin_aegis', name: '菩提清净甲', slot: '被动·减伤', desc: '【被动】受到的所有伤害降低 25%，并免疫一切场地陷阱伤害。' },
          { id: 'guanyin_dew', name: '杨柳甘露润泽', slot: '被动·续航', desc: '【被动】每进入一个新的关卡，立即恢复 35 点气血与 25 点真气。' },
          { id: 'guanyin_serenity', name: '明心见性', slot: '被动·真气', desc: '【被动】混元真气每秒自动回复 3 点。' },
          { id: 'guanyin_bloom', name: '步步生莲', slot: '被动·莲花', desc: '【被动】被击败的敌人原地绽放金莲，爆炸造成 80 点范围伤害并治疗自身。' },
          { id: 'guanyin_grace', name: '大悲无疆', slot: '被动·体质', desc: '【被动】气血上限提升 60 点，真气上限提升 30 点。' }
        ]
      },
      nezha: {
        name: '三坛海会大神·哪吒',
        title: '中坛元帅三太子哪吒',
        portraitIndex: 2,
        color: '#f97316',
        quotes: [
          '“大圣！且看小爷的风火轮与你的筋斗云孰快孰慢！”',
          '“九龙神火罩下，万千妖魔皆化为灰烬！”'
        ],
        boons: [
          { id: 'nezha_strike', name: '烈焰火尖枪', slot: '普通攻击', desc: '【普攻】金箍棒附带三昧真火枪意，使敌人陷入烈火灼烧，3 秒内造成 60 点烈焰伤害。' },
          { id: 'nezha_ring', name: '乾坤金圈阵', slot: '法术法阵', desc: '【法阵】法阵内飞出乾坤圈在最多 6 名敌人之间快速弹射，每次造成 35 点重击伤害。' },
          { id: 'nezha_dash', name: '风火飞轮遁', slot: '闪避身法', desc: '【闪避】筋斗云带起熊熊烈火轨迹，踏入火海的敌人每秒受到 50 点火焰伤害。' },
          { id: 'nezha_special', name: '崩山风火刺', slot: '特殊攻击', desc: '【特殊】定海神针重劈引发地脉烈焰爆发，造成 90 点范围火伤害并将敌人击飞。' },
          { id: 'nezha_ribbon', name: '混天红绫缚', slot: '被动·控制', desc: '【被动】攻击有 30% 几率以混天绫缠绕定身敌人 2 秒。' },
          { id: 'nezha_speed', name: '风驰电掣', slot: '被动·移速', desc: '【被动】永久提升 35% 移动速度，并增加 1 次筋斗云闪避充能。' },
          { id: 'nezha_combust', name: '烈焰爆破', slot: '被动·增伤', desc: '【被动】击中灼烧中的敌人触发烈焰连环爆破，造成 45 点额外范围伤害。' },
          { id: 'nezha_spearvortex', name: '乾坤旋刃', slot: '被动·特殊', desc: '【被动】特殊攻击同时掷出 2 枚回旋火轮。' },
          { id: 'nezha_lotusbody', name: '莲花化身', slot: '被动·求生', desc: '【被动】生命值低于 30% 时爆发烈焰冲击波逼退敌群，并进入 4 秒无敌状态。' },
          { id: 'nezha_inferno', name: '三头六臂真火', slot: '被动·灼烧', desc: '【被动】灼烧伤害触发速度加快 50%，并在敌群之间自动蔓延。' }
        ]
      },
      laojun: {
        name: '太上道祖·太上老君',
        title: '三清道祖道德天尊',
        portraitIndex: 3,
        color: '#ec4899',
        quotes: [
          '“老道八卦炉炼就你的火眼金睛，如今且看你道法修至何等境界！”',
          '“九转还魂，阴阳合一。天地玄黄，道法自然。”'
        ],
        boons: [
          { id: 'laojun_strike', name: '三昧真火印', slot: '普通攻击', desc: '【普攻】棍法挥洒三昧纯阳真火，造成 50 点道家仙法伤害并永久熔穿敌方护甲。' },
          { id: 'laojun_ring', name: '八卦神炉阵', slot: '法术法阵', desc: '【法阵】在地面显化八卦阴阳炉阵，每 0.3 秒对阵内敌人造成 40 点炼化伤害。' },
          { id: 'laojun_dash', name: '灵霄丹烟步', slot: '闪避身法', desc: '【闪避】闪避留下金色仙丹云雾，使敌人致盲且自身伤害提升 30%。' },
          { id: 'laojun_special', name: '九转金丹破', slot: '特殊攻击', desc: '【特殊】定海神针重劈引发仙丹爆炸，造成 110 点混元道法伤害。' },
          { id: 'laojun_elixir', name: '九转还魂丹', slot: '被动·仙果', desc: '【被动】天庭蟠桃额外赋予 1 次升级效果，且每次吃蟠桃瞬间补满全生命值。' },
          { id: 'laojun_yin_yang', name: '阴阳生化诀', slot: '被动·连招', desc: '【被动】交替使用普攻与特殊攻击时，伤害提升 60%，持续 3 秒。' },
          { id: 'laojun_qi_surge', name: '混元气涌', slot: '被动·真气', desc: '【被动】施放法术真气消耗降低 50%，施法时恢复 10 点气血。' },
          { id: 'laojun_furnace', name: '八卦共鸣', slot: '被动·法阵', desc: '【被动】站在法阵内时攻击速度提升 40%，暴击率提升 30%。' },
          { id: 'laojun_transmute', name: '点石成金', slot: '被动·收益', desc: '【被动】击败敌人掉落的灵石提升 70%，功德灵砂提升 50%。' },
          { id: 'laojun_primordial', name: '先天一气', slot: '被动·觉醒', desc: '【被动】大闹天宫法天象地觉醒能量积攒速度加快 50%。' }
        ]
      },
      aoguang: {
        name: '东海龙王·敖广',
        title: '东海四海龙王之首',
        portraitIndex: 4,
        color: '#38bdf8',
        quotes: [
          '“你抢了老龙的定海神针铁！今日且叫你见识四海翻腾之狂澜！”',
          '“汪洋怒涛，听吾号令！覆灭三界妖逆！”'
        ],
        boons: [
          { id: 'aoguang_strike', name: '怒涛狂澜击', slot: '普通攻击', desc: '【普攻】金箍棒附带重水龙威，发射水刃强力击退敌人并造成 40 点额外伤害。' },
          { id: 'aoguang_ring', name: '归墟大漩涡', slot: '法术法阵', desc: '【法阵】召唤汪洋漩涡将全场敌人强力吸附至中心并造成碾压伤害。' },
          { id: 'aoguang_dash', name: '狂澜惊涛步', slot: '闪避身法', desc: '【闪避】身法掀起滔天海浪击退敌群，并附加潮湿易伤状态。' },
          { id: 'aoguang_special', name: '蛟龙出海刺', slot: '特殊攻击', desc: '【特殊】神针重劈召唤碧水青龙咆哮奔腾，造成 85 点寒冰水浪伤害。' },
          { id: 'aoguang_pressure', name: '惊涛裂壁', slot: '被动·撞击', desc: '【被动】将敌人击退撞击在关卡石壁上时，造成 80 点真实粉碎伤害。' },
          { id: 'aoguang_drench', name: '寒霜透骨', slot: '被动·减速', desc: '【被动】潮湿状态下的敌人移速降低 35%，受到雷电与冰霜伤害提升 30%。' },
          { id: 'aoguang_pearl', name: '沧海明珠', slot: '被动·水弹', desc: '【被动】每 2 秒自动向最近敌人发射 2 颗寻敌龙珠，造成 35 伤害。' },
          { id: 'aoguang_riptide', name: '定海回澜', slot: '被动·普攻', desc: '【普攻】三连击终结技原地生成持续 2 秒的水龙卷。' },
          { id: 'aoguang_leviathan', name: '龙皇冰魄', slot: '被动·冻结', desc: '【被动】特殊攻击有 40% 几率将敌人彻底冰冻冻结 2 秒。' },
          { id: 'aoguang_sovereign', name: '四海尊者', slot: '被动·防御', desc: '【被动】移速提升 20%，并将造成伤害的 15% 转化为自身护盾。' }
        ]
      },
      bullking: {
        name: '平天大圣·牛魔王',
        title: '七大圣之首·大力牛魔王',
        portraitIndex: 5,
        color: '#ea580c',
        quotes: [
          '“贤弟悟空！七大圣威震天下，今日随俺老牛踏破这灵霄宝殿！”',
          '“混铁棍撼天动地！俺老牛的一身蛮力，谁人可挡？！”'
        ],
        boons: [
          { id: 'bull_strike', name: '撼地开山击', slot: '普通攻击', desc: '【普攻】金箍棒造成 40% 额外沉重物理打击，并伴随地震波击退敌人。' },
          { id: 'bull_ring', name: '地动山摇阵', slot: '法术法阵', desc: '【法阵】法阵引发剧烈地裂，每秒爆震造成 50 点破甲伤害。' },
          { id: 'bull_dash', name: '蛮荒冲撞步', slot: '闪避身法', desc: '【闪避】横冲直撞冲撞敌人，造成 45 点霸体冲撞伤害。' },
          { id: 'bull_special', name: '破岳混铁棍', slot: '特殊攻击', desc: '【特殊】神针重劈直线撕裂大地，造成 120 点开山裂石之巨额物理伤害。' },
          { id: 'bull_ironhide', name: '魔王不坏铁躯', slot: '被动·护甲', desc: '【被动】获得 50 点常驻护甲值，未受击 8 秒后自动回复全满。' },
          { id: 'bull_stagger', name: '崩山重震', slot: '被动·眩晕', desc: '【被动】所有重击攻击有 25% 几率眩晕敌人 1.5 秒。' },
          { id: 'bull_trample', name: '践踏狂威', slot: '被动·增伤', desc: '【被动】闪避穿过敌人时提升 30% 攻击伤害，持续 4 秒（可叠 3 层）。' },
          { id: 'bull_brute', name: '大力神通', slot: '被动·增伤', desc: '【被动】普攻与特殊攻击基础伤害常驻提升 35%。' },
          { id: 'bull_rage', name: '绝境狂暴', slot: '被动·残血', desc: '【被动】生命值低于 40% 时，攻击速度与伤害飙升 60%。' },
          { id: 'bull_boulder', name: '地脉碎石', slot: '被动·碎裂', desc: '【被动】被消灭的敌人化作飞石爆裂，对周围造成 60 点范围伤害。' }
        ]
      },
      ironfan: {
        name: '翠云山·铁扇公主',
        title: '得道仙真·铁扇仙',
        portraitIndex: 6,
        color: '#4ade80',
        quotes: [
          '“我这芭蕉宝扇，一扇息火，二扇生风，三扇下雨！教天兵天将尽化飞灰！”',
          '“清风化煞，扫尽妖邪！”'
        ],
        boons: [
          { id: 'ironfan_strike', name: '芭蕉罡风刃', slot: '普通攻击', desc: '【普攻】棍法劈出锐利青色风刃，穿透敌人造成 35 点风属性穿甲伤害。' },
          { id: 'ironfan_ring', name: '狂风卷地阵', slot: '法术法阵', desc: '【法阵】召唤呼啸龙卷风阵，将敌人持续吸扯至风眼并反弹弹幕。' },
          { id: 'ironfan_dash', name: '顺风御气行', slot: '闪避身法', desc: '【闪避】借风力冲刺，获得 2 秒 50% 移速加成并吹飞身边敌人。' },
          { id: 'ironfan_special', name: '席卷乾坤破', slot: '特殊攻击', desc: '【特殊】特殊攻击召唤巨型龙卷风横扫全图，造成 90 点多段风暴伤害。' },
          { id: 'ironfan_deflect', name: '罡风反弹', slot: '被动·反弹', desc: '【被动】所有棍法挥击与特殊技能均能精准反弹敌人发射的远程弹幕。' },
          { id: 'ironfan_razor', name: '撕裂风煞', slot: '被动·易伤', desc: '【被动】风属性伤害附加撕裂易伤，使敌人受到的全伤害提升 25%。' },
          { id: 'ironfan_agility', name: '风行灵动', slot: '被动·闪避', desc: '【被动】获得常驻 20% 概率完全闪避任何伤害。' },
          { id: 'ironfan_tailwind', name: '疾风骤雨', slot: '被动·攻速', desc: '【被动】攻击速度提升 30%。' },
          { id: 'ironfan_twister', name: '双生风暴', slot: '被动·龙卷', desc: '【被动】特殊攻击额外释放两道分叉龙卷风。' },
          { id: 'ironfan_tempest', name: '风王结界', slot: '被动·护体', desc: '【被动】身边常驻呼啸灵风风环，每秒对近身敌人造成 20 点切裂伤害。' }
        ]
      },
      puti: {
        name: '灵台方寸山·菩提祖师',
        title: '大觉金仙没垢姿·菩提老祖',
        portraitIndex: 7,
        color: '#c084fc',
        quotes: [
          '“鸿蒙初判得真仙，显密圆通真妙诀。悟彻菩提真妙理，西行路上任纵横。”',
          '“七十二般变化，夺天地之造化，悟空，莫忘师门！”'
        ],
        boons: [
          { id: 'puti_strike', name: '灵台归一击', slot: '普通攻击', desc: '【普攻】棍法蕴含菩提禅机，吸取敌人精气恢复 15% 伤害的气血并附加道家真言。' },
          { id: 'puti_ring', name: '斜月三星阵', slot: '法术法阵', desc: '【法阵】布下方寸山悟道法阵，地脉升腾七彩仙芒，穿刺重创敌人 60 伤害。' },
          { id: 'puti_dash', name: '筋斗化光行', slot: '闪避身法', desc: '【闪避】化作金光瞬移，在原地留下替身幻影吸引敌人仇恨与火力。' },
          { id: 'puti_special', name: '显密圆通破', slot: '特殊攻击', desc: '【特殊】神针重劈显化祖师拂尘巨相，造成 85 点乾坤混元伤害。' },
          { id: 'puti_decay', name: '大道无为', slot: '被动·减速', desc: '【被动】被击中的敌人陷入悟道迟滞，攻速移速降低 30% 且受伤害加深。' },
          { id: 'puti_drain', name: '方寸纳海', slot: '被动·成长', desc: '【被动】每斩灭一名妖魔，气血上限永久 +2（单局最高 +60）。' },
          { id: 'puti_phantom', name: '身外法身', slot: '被动·分身', desc: '【被动】击败敌人有 30% 几率显化灵气分身协助作战。' },
          { id: 'puti_shadow_rend', name: '明心破妄', slot: '被动·背刺', desc: '【被动】从敌人背后攻击或攻击被分身吸引的敌人时，必定造成 100% 暴击加成。' },
          { id: 'puti_armor', name: '金丹舍利身', slot: '被动·免死', desc: '【被动】受到致命伤害时免疫死亡并保留 1 血，获得 3 秒无敌（每关限 1 次）。' },
          { id: 'puti_torment', name: '圆通妙法', slot: '被动·增伤', desc: '【被动】对身上带有任何负面异常状态的敌人伤害提升 40%。' }
        ]
      },
      yanluo: {
        name: '幽冥教主·阎罗王',
        title: '十殿阎君之第五殿阎罗天子',
        portraitIndex: 8,
        color: '#ef4444',
        quotes: [
          '“生死簿上早已勾去你的名姓！今日且助大圣勾尽天下妖魔寿元！”',
          '“幽冥地府十八层，锁链过处，万鬼断魂！”'
        ],
        boons: [
          { id: 'yanluo_strike', name: '生死判官笔', slot: '普通攻击', desc: '【普攻】棍法刻下判官朱砂死印，3 秒后在目标身上引爆 70 点幽冥死气伤害。' },
          { id: 'yanluo_ring', name: '勾魂铁索阵', slot: '法术法阵', desc: '【法阵】召唤地府勾魂锁链链接全场敌人，使所有被链接敌人承受 50% 伤害均摊共享。' },
          { id: 'yanluo_dash', name: '地府冥火遁', slot: '闪避身法', desc: '【闪避】身法踏过留下幽绿冥火，对踏入的敌人施加阎罗索命效果。' },
          { id: 'yanluo_special', name: '阎罗索命破', slot: '特殊攻击', desc: '【特殊】特殊攻击挥下判官朱笔，直接斩杀生命值低于 15% 的非首领敌人。' },
          { id: 'yanluo_doom', name: '幽冥死印', slot: '被动·爆发', desc: '【被动】死印引爆伤害提升至 120 点巨额幽冥伤害。' },
          { id: 'yanluo_execution', name: '判官勾决', slot: '被动·首领', desc: '【被动】对首领 Boss 与精英妖魔的伤害常驻提升 35%。' },
          { id: 'yanluo_soul_gem', name: '聚魂宝瓮', slot: '被动·收益', desc: '【被动】击败敌人获得的功德灵砂数量翻倍（+100%）。' },
          { id: 'yanluo_ghost_gate', name: '鬼门大开', slot: '被动·特殊', desc: '【被动】特殊攻击同时撕开幽冥之门，飞出 4 颗索敌怨灵骷髅造成 30 伤害。' },
          { id: 'yanluo_retribution', name: '因果业报', slot: '被动·反击', desc: '【被动】受击时将受到伤害的 200% 反弹给攻击者。' },
          { id: 'yanluo_sovereign', name: '无常索魂', slot: '被动·无伤', desc: '【被动】每无伤通关 1 重天，全伤害提升 10%（最高提升 50%）。' }
        ]
      },
      change: {
        name: '广寒仙子·嫦娥与玉兔',
        title: '太阴星君广寒月宫之主',
        portraitIndex: 9,
        color: '#93c5fd',
        quotes: [
          '“广寒宫月华如水，照彻幽夜。愿此太阴清辉伴大圣扫荡三界。”',
          '“玉兔已捣成不死神药，饮此月髓仙浆，涤荡尘心！”'
        ],
        boons: [
          { id: 'change_strike', name: '冰魄寒月击', slot: '普通攻击', desc: '【普攻】棍影挥洒广寒月魄玄冰，造成 35 点冰霜伤害并冻结敌人 1.2 秒。' },
          { id: 'change_ring', name: '太阴清辉镜', slot: '法术法阵', desc: '【法阵】生成太阴灵镜法阵，反射一切外部投射物并持续冻结阵内敌群。' },
          { id: 'change_dash', name: '月影幽仙步', slot: '闪避身法', desc: '【闪避】月影幻化穿行敌群，将沿途穿过的所有敌人冻结 1.5 秒。' },
          { id: 'change_special', name: '皓月当空破', slot: '特殊攻击', desc: '【特殊】特殊攻击召唤 3 颗旋转月魄宝珠环绕自身，重创近身敌人并吸收伤害。' },
          { id: 'change_rabbit', name: '玉兔捣药', slot: '被动·灵药', desc: '【被动】每 10 秒玉兔投掷一枚长生仙药瓶，拾取恢复 15 点气血与 15 点真气。' },
          { id: 'change_frostbite', name: '太阴彻骨', slot: '被动·增伤', desc: '【被动】被冻结的目标受到的所有物理打击伤害提升 50%。' },
          { id: 'change_moonbeam', name: '九天月芒', slot: '被动·暴击', desc: '【被动】暴击时自苍穹引下一道直击月华神柱，造成 90 点范围太阴伤害。' },
          { id: 'change_glaze', name: '广寒仙衣', slot: '被动·护盾', desc: '【被动】每 15 秒获得一层广寒护体仙衣，完全免疫下一次伤害。' },
          { id: 'change_radiance', name: '清辉玉露', slot: '被动·真气', desc: '【被动】消耗真气施法时触发太阴冰爆，冻结周围全敌人 1.5 秒。' },
          { id: 'change_eclipse', name: '月蚀乾坤', slot: '被动·觉醒', desc: '【被动】法天象地大闹天宫期间全图沐浴月华，所有敌人移速与攻速降低 60%。' }
        ]
      }
    };

    // ==========================================
    // GAME ENGINE & CANVAS RENDERING
    // ==========================================
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
      canvas.width = window.innerWidth || document.documentElement.clientWidth || 1280;
      canvas.height = window.innerHeight || document.documentElement.clientHeight || 720;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Game State (180 Chambers Journey)
    const gameState = {
      chamberIndex: 1,
      totalChambers: 180,
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
      mouse: { x: 0, y: 0, isDown: false, rightDown: false },
      camera: { x: 0, y: 0 },
      isPaused: false,
      activeModal: null
    };

    // Meta Upgrade Save State (72 Transformations)
    const metaUpgrades = {
      stone_monkey: 0,
      golden_eyes: 0,
      somersault: 0,
      hair_clones: 0,
      qi_circulation: 0,
      nirvana_body: 0
    };

    // Keyboard & Mouse Listeners
    window.addEventListener('keydown', (e) => {
      gameState.keys[e.key.toLowerCase()] = true;
      if (e.key === ' ' || e.key === 'Shift') {
        player.performDash();
      }
      if (e.key.toLowerCase() === 'e') {
        player.performCast();
      }
      if (e.key.toLowerCase() === 'q') {
        player.performSpecial();
      }
      if (e.key.toLowerCase() === 'r' || e.key.toLowerCase() === 'f') {
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
      if (gameState.isPaused) return;
      if (e.button === 0) {
        gameState.mouse.isDown = true;
        player.performAttack();
      } else if (e.button === 2) {
        gameState.mouse.rightDown = true;
        player.performSpecial();
      }
    });

    window.addEventListener('mouseup', (e) => {
      if (e.button === 0) gameState.mouse.isDown = false;
      if (e.button === 2) gameState.mouse.rightDown = false;
    });

    window.addEventListener('contextmenu', (e) => e.preventDefault());

    // ==========================================
    // PLAYER CLASS: SUN WUKONG (MONKEY KING)
    // ==========================================
    class Player {
      constructor() {
        this.x = 0;
        this.y = 0;
        this.vx = 0;
        this.vy = 0;
        this.facing = 1;
        this.radius = 26;
        this.baseSpeed = 250;
        this.speed = 250;
        this.hp = 100;
        this.maxHp = 100;
        this.qi = 50;
        this.maxQi = 50;
        this.qiRegen = 1.5;
        this.armor = 0;

        // Combat Mechanics
        this.comboIndex = 0;
        this.comboTimer = 0;
        this.isAttacking = false;
        this.attackDuration = 0;
        this.attackMaxDuration = 0.18;
        this.attackAngle = 0;
        this.attackCooldown = 0;

        // Special Attack
        this.isSpecialActive = false;
        this.specialCooldown = 0;
        this.specialDuration = 0;

        // Somersault Cloud Dash
        this.isDashing = false;
        this.dashDuration = 0;
        this.dashCooldown = 0;
        this.dashCharges = 2;
        this.maxDashCharges = 2;
        this.dashRechargeTimer = 0;
        this.dashTrail = [];

        // Cast Circle
        this.castActive = null;
        this.castCooldown = 0;

        // Awakened Form (Havoc in Heaven / 法天象地)
        this.awakenGauge = 0;
        this.maxAwakenGauge = 100;
        this.isAwakened = false;
        this.awakenDuration = 0;

        // Death Defiance Lives
        this.lives = 1;
        this.maxLives = 1;

        // Equipped Boons
        this.boons = {
          attack: null,
          special: null,
          cast: null,
          dash: null,
          hex: null,
          passives: []
        };
      }

      resetForRun() {
        this.applyMetaUpgrades();
        this.hp = this.maxHp;
        this.qi = this.maxQi;
        this.lives = this.maxLives;
        this.awakenGauge = 0;
        this.isAwakened = false;
        this.boons = {
          attack: null,
          special: null,
          cast: null,
          dash: null,
          hex: null,
          passives: []
        };
        this.x = 0;
        this.y = 0;
        this.vx = 0;
        this.vy = 0;
        this.castActive = null;
        this.dashTrail = [];
        updateHUD();
      }

      applyMetaUpgrades() {
        this.maxHp = 100 + metaUpgrades.stone_monkey * 25;
        this.maxQi = 50 + metaUpgrades.qi_circulation * 15;
        this.qiRegen = 1.5 + metaUpgrades.qi_circulation * 0.8;
        this.maxDashCharges = 2 + metaUpgrades.somersault;
        this.dashCharges = this.maxDashCharges;
        this.maxLives = 1 + metaUpgrades.nirvana_body;
        this.lives = this.maxLives;
      }

      hasBoon(id) {
        if (this.boons.attack && this.boons.attack.id === id) return true;
        if (this.boons.special && this.boons.special.id === id) return true;
        if (this.boons.cast && this.boons.cast.id === id) return true;
        if (this.boons.dash && this.boons.dash.id === id) return true;
        if (this.boons.hex && this.boons.hex.id === id) return true;
        return this.boons.passives.some(b => b.id === id);
      }

      getBoonLevel(id) {
        if (this.boons.attack && this.boons.attack.id === id) return this.boons.attack.level || 1;
        if (this.boons.special && this.boons.special.id === id) return this.boons.special.level || 1;
        if (this.boons.cast && this.boons.cast.id === id) return this.boons.cast.level || 1;
        if (this.boons.dash && this.boons.dash.id === id) return this.boons.dash.level || 1;
        if (this.boons.hex && this.boons.hex.id === id) return this.boons.hex.level || 1;
        const p = this.boons.passives.find(b => b.id === id);
        return p ? (p.level || 1) : 1;
      }

      update(dt) {
        if (this.qi < this.maxQi) {
          this.qi = Math.min(this.maxQi, this.qi + this.qiRegen * dt);
        }

        if (this.dashCharges < this.maxDashCharges) {
          this.dashRechargeTimer += dt;
          if (this.dashRechargeTimer >= 0.75) {
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

        if (this.attackCooldown > 0) this.attackCooldown -= dt;
        if (this.specialCooldown > 0) this.specialCooldown -= dt;
        if (this.castCooldown > 0) this.castCooldown -= dt;
        if (this.dashCooldown > 0) this.dashCooldown -= dt;

        if (this.comboTimer > 0) {
          this.comboTimer -= dt;
          if (this.comboTimer <= 0) {
            this.comboIndex = 0;
          }
        }

        const worldMouseX = gameState.mouse.x - canvas.width / 2 + this.x;
        this.facing = worldMouseX < this.x ? -1 : 1;

        let moveX = 0;
        let moveY = 0;
        if (gameState.keys['w'] || gameState.keys['arrowup']) moveY -= 1;
        if (gameState.keys['s'] || gameState.keys['arrowdown']) moveY += 1;
        if (gameState.keys['a'] || gameState.keys['arrowleft']) moveX -= 1;
        if (gameState.keys['d'] || gameState.keys['arrowright']) moveX += 1;

        const len = Math.hypot(moveX, moveY);
        if (len > 0) {
          moveX /= len;
          moveY /= len;
        }

        if (this.isDashing) {
          this.dashDuration -= dt;
          if (this.dashDuration <= 0) {
            this.isDashing = false;
          }
          this.dashTrail.push({
            x: this.x,
            y: this.y,
            alpha: 1.0,
            radius: 24
          });
        } else {
          let curSpeed = this.baseSpeed;
          if (this.isAwakened) curSpeed *= 1.4;
          if (this.hasBoon('nezha_speed')) curSpeed *= (1 + 0.35 * this.getBoonLevel('nezha_speed'));
          if (this.hasBoon('ironfan_tailwind')) curSpeed *= 1.25;

          this.vx = moveX * curSpeed;
          this.vy = moveY * curSpeed;
          this.x += this.vx * dt;
          this.y += this.vy * dt;
        }

        const bound = 650;
        this.x = Math.max(-bound, Math.min(bound, this.x));
        this.y = Math.max(-bound, Math.min(bound, this.y));

        for (let i = this.dashTrail.length - 1; i >= 0; i--) {
          this.dashTrail[i].alpha -= dt * 3.5;
          if (this.dashTrail[i].alpha <= 0) {
            this.dashTrail.splice(i, 1);
          }
        }

        if (this.castActive) {
          this.castActive.duration -= dt;
          this.castActive.tickTimer += dt;
          if (this.castActive.tickTimer >= 0.25) {
            this.castActive.tickTimer = 0;
            this.triggerCastTick();
          }
          if (this.castActive.duration <= 0) {
            this.castActive = null;
          }
        }

        if (gameState.mouse.isDown && !this.isAttacking && this.attackCooldown <= 0) {
          this.performAttack();
        }

        if (this.isAttacking) {
          this.attackDuration -= dt;
          if (this.attackDuration <= 0) {
            this.isAttacking = false;
          }
        }

        if (this.isSpecialActive) {
          this.specialDuration -= dt;
          if (this.specialDuration <= 0) {
            this.isSpecialActive = false;
          }
        }
      }

      performAttack() {
        if (this.isDashing || this.isAttacking || this.attackCooldown > 0) return;

        sound.playStaffSwing();
        this.isAttacking = true;
        this.attackDuration = this.attackMaxDuration;
        this.attackCooldown = 0.16;

        const worldMouseX = gameState.mouse.x - canvas.width / 2 + this.x;
        const worldMouseY = gameState.mouse.y - canvas.height / 2 + this.y;
        this.attackAngle = Math.atan2(worldMouseY - this.y, worldMouseX - this.x);

        this.comboIndex = (this.comboIndex + 1) % 3;
        this.comboTimer = 0.6;

        let baseDmg = 42;
        let reach = 115;
        let arc = Math.PI * 0.8;

        if (this.comboIndex === 2) {
          baseDmg = 92;
          reach = 155;
          arc = Math.PI * 0.95;
          sound.playStaffSmash();
          createScreenShake(7);
        } else {
          sound.playStaffHit();
        }

        if (this.isAwakened) {
          baseDmg *= 2.2;
          reach *= 1.6;
        }

        if (this.boons.attack) {
          const lvl = this.boons.attack.level || 1;
          baseDmg *= (1 + 0.3 * (lvl - 1));
          this.procAttackBoon(this.boons.attack.id, lvl);
        }

        fxList.push(new AnimatedAttackSweep(this.x, this.y, this.attackAngle, reach, this.comboIndex === 2 ? '#facc15' : '#ef4444'));

        let hitAny = false;
        enemies.forEach(enemy => {
          if (!enemy.alive) return;
          const dist = Math.hypot(enemy.x - this.x, enemy.y - this.y);
          if (dist <= reach + enemy.radius) {
            const angleToEnemy = Math.atan2(enemy.y - this.y, enemy.x - this.x);
            let angleDiff = Math.abs(this.attackAngle - angleToEnemy);
            while (angleDiff > Math.PI) angleDiff = Math.abs(angleDiff - Math.PI * 2);

            if (angleDiff <= arc / 2) {
              hitAny = true;
              let crit = Math.random() < (0.15 + (metaUpgrades.golden_eyes * 0.08) + (this.hasBoon('erlang_truesight') ? 0.25 : 0));
              let finalDmg = baseDmg * (crit ? 2.5 : 1.0);

              enemy.takeDamage(finalDmg, crit);

              const knock = (this.comboIndex === 2 ? 240 : 130);
              enemy.vx += Math.cos(angleToEnemy) * knock;
              enemy.vy += Math.sin(angleToEnemy) * knock;

              this.awakenGauge = Math.min(this.maxAwakenGauge, this.awakenGauge + (crit ? 5 : 2.5));
            }
          }
        });

        if (hitAny) {
          sound.playStaffHit();
        }
      }

      procAttackBoon(id, level) {
        if (id === 'erlang_strike') {
          sound.playLightning();
          enemies.slice(0, 3).forEach(e => {
            if (e.alive) {
              fxList.push(new AnimatedLightningStrike(e.x, e.y));
              e.takeDamage(45 * level, false);
            }
          });
        } else if (id === 'nezha_strike') {
          sound.playFire();
          enemies.forEach(e => {
            if (e.alive && Math.hypot(e.x - this.x, e.y - this.y) < 160) {
              e.applyBurn(60 * level, 3);
            }
          });
        } else if (id === 'laojun_strike') {
          sound.playFire();
          fxList.push(new AnimatedFireExplosion(this.x + Math.cos(this.attackAngle)*80, this.y + Math.sin(this.attackAngle)*80, 75));
        } else if (id === 'aoguang_strike') {
          fxList.push(new AnimatedWaterWave(this.x, this.y, this.attackAngle));
        } else if (id === 'change_strike') {
          enemies.forEach(e => {
            if (e.alive && Math.hypot(e.x - this.x, e.y - this.y) < 140) {
              e.applyFreeze(1.5);
            }
          });
        }
      }

      performSpecial() {
        if (this.specialCooldown > 0 || this.isDashing) return;
        this.specialCooldown = 1.0;
        this.isSpecialActive = true;
        this.specialDuration = 0.35;

        sound.playStaffSmash();
        createScreenShake(8);

        const worldMouseX = gameState.mouse.x - canvas.width / 2 + this.x;
        const worldMouseY = gameState.mouse.y - canvas.height / 2 + this.y;
        const angle = Math.atan2(worldMouseY - this.y, worldMouseX - this.x);

        let baseDmg = 100;
        let reach = 200;
        if (this.boons.special) {
          const lvl = this.boons.special.level || 1;
          baseDmg *= (1 + 0.35 * (lvl - 1));
        }

        fxList.push(new Shockwave(this.x, this.y, reach, '#facc15'));

        enemies.forEach(enemy => {
          if (!enemy.alive) return;
          const dist = Math.hypot(enemy.x - this.x, enemy.y - this.y);
          if (dist <= reach + enemy.radius) {
            enemy.takeDamage(baseDmg, true);
            const knockAngle = Math.atan2(enemy.y - this.y, enemy.x - this.x);
            enemy.vx += Math.cos(knockAngle) * 340;
            enemy.vy += Math.sin(knockAngle) * 340;
          }
        });

        projectiles.forEach(p => {
          if (p.isEnemy && Math.hypot(p.x - this.x, p.y - this.y) < reach) {
            p.isEnemy = false;
            p.vx = -p.vx * 1.5;
            p.vy = -p.vy * 1.5;
          }
        });
      }

      performCast() {
        if (this.castCooldown > 0 || this.qi < 15) return;
        this.qi -= 15;
        this.castCooldown = 0.5;

        sound.playJadeChime();

        const worldMouseX = gameState.mouse.x - canvas.width / 2 + this.x;
        const worldMouseY = gameState.mouse.y - canvas.height / 2 + this.y;

        this.castActive = {
          x: worldMouseX,
          y: worldMouseY,
          radius: 130,
          duration: 6.0,
          tickTimer: 0,
          angle: 0
        };

        fxList.push(new Shockwave(worldMouseX, worldMouseY, 130, '#a855f7'));
      }

      triggerCastTick() {
        if (!this.castActive) return;
        enemies.forEach(enemy => {
          if (!enemy.alive) return;
          const dist = Math.hypot(enemy.x - this.castActive.x, enemy.y - this.castActive.y);
          if (dist <= this.castActive.radius + enemy.radius) {
            let dmg = 28;
            if (this.boons.cast) {
              dmg *= (1 + 0.3 * (this.boons.cast.level || 1));
            }
            enemy.takeDamage(dmg, false);
            enemy.applySlow(0.5, 0.4);
          }
        });
      }

      performDash() {
        if (this.isDashing || this.dashCharges <= 0) return;
        this.dashCharges--;
        this.isDashing = true;
        this.dashDuration = 0.22;
        sound.playDash();

        let moveX = 0;
        let moveY = 0;
        if (gameState.keys['w'] || gameState.keys['arrowup']) moveY -= 1;
        if (gameState.keys['s'] || gameState.keys['arrowdown']) moveY += 1;
        if (gameState.keys['a'] || gameState.keys['arrowleft']) moveX -= 1;
        if (gameState.keys['d'] || gameState.keys['arrowright']) moveX += 1;

        if (moveX === 0 && moveY === 0) {
          const worldMouseX = gameState.mouse.x - canvas.width / 2 + this.x;
          const worldMouseY = gameState.mouse.y - canvas.height / 2 + this.y;
          const ang = Math.atan2(worldMouseY - this.y, worldMouseX - this.x);
          moveX = Math.cos(ang);
          moveY = Math.sin(ang);
        } else {
          const l = Math.hypot(moveX, moveY);
          moveX /= l;
          moveY /= l;
        }

        const dashSpeed = 700;
        this.vx = moveX * dashSpeed;
        this.vy = moveY * dashSpeed;
        this.x += this.vx * 0.22;
        this.y += this.vy * 0.22;

        if (this.boons.dash) {
          const lvl = this.boons.dash.level || 1;
          if (this.boons.dash.id === 'nezha_dash') {
            fxList.push(new AnimatedFireExplosion(this.x, this.y, 80));
          } else if (this.boons.dash.id === 'aoguang_dash') {
            fxList.push(new AnimatedWaterWave(this.x, this.y, Math.atan2(moveY, moveX)));
          } else if (this.boons.dash.id === 'erlang_dash') {
            fxList.push(new AnimatedLightningStrike(this.x, this.y));
          }
        }
      }

      triggerAwakening() {
        if (this.awakenGauge < this.maxAwakenGauge || this.isAwakened) return;
        this.isAwakened = true;
        this.awakenDuration = 10.0;
        sound.playAwaken();
        createScreenShake(15);
        fxList.push(new Shockwave(this.x, this.y, 260, '#facc15'));
      }

      takeDamage(amount) {
        if (this.isDashing || this.isAwakened) return;

        if (this.armor > 0) {
          const absorbed = Math.min(this.armor, amount);
          this.armor -= absorbed;
          amount -= absorbed;
          if (amount <= 0) return;
        }

        this.hp -= amount;
        createScreenShake(5);

        floatingTexts.push(new FloatingText(this.x, this.y - 30, `-${Math.round(amount)}`, '#ef4444'));

        if (this.hp <= 0) {
          if (this.lives > 0) {
            this.lives--;
            this.hp = Math.round(this.maxHp * 0.6);
            sound.playJadeChime();
            createScreenShake(10);
            fxList.push(new Shockwave(this.x, this.y, 200, '#4ade80'));
            floatingTexts.push(new FloatingText(this.x, this.y - 45, '金身复活 · 重振神威!', '#4ade80'));
          } else {
            handleGameOver(false);
          }
        }
        updateHUD();
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);

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
          this.castActive.angle += 0.02;
          ctx.rotate(this.castActive.angle);

          ctx.beginPath();
          ctx.arc(0, 0, this.castActive.radius, 0, Math.PI * 2);
          ctx.strokeStyle = 'rgba(168, 85, 247, 0.85)';
          ctx.lineWidth = 3;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(0, 0, this.castActive.radius * 0.6, 0, Math.PI * 2);
          ctx.strokeStyle = 'rgba(250, 204, 21, 0.7)';
          ctx.lineWidth = 2;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(0, 0, 20, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
          ctx.fill();

          ctx.restore();
        }

        const heroImg = loadedImages['hero'];
        if (heroImg && heroImg.complete && heroImg.naturalWidth > 0) {
          const cols = 8;
          const rows = 7;
          const cellW = heroImg.naturalWidth / cols;
          const cellH = heroImg.naturalHeight / rows;

          let r = 0;
          let c = 0;

          if (this.isAwakened) {
            r = 5;
            c = Math.floor((Date.now() / 90) % 8);
          } else if (this.isDashing) {
            r = 4;
            c = Math.floor((Date.now() / 70) % 8);
          } else if (this.isAttacking) {
            if (this.comboIndex === 2) {
              r = 3;
            } else {
              r = 2;
            }
            c = Math.min(7, Math.floor((1 - this.attackDuration / this.attackMaxDuration) * 8));
          } else if (Math.hypot(this.vx, this.vy) > 10) {
            r = 1;
            c = Math.floor((Date.now() / 100) % 8);
          } else {
            r = 0;
            c = Math.floor((Date.now() / 120) % 8);
          }

          const scale = this.isAwakened ? 1.5 : 1.1;
          const drawW = 96 * scale;
          const drawH = 96 * scale;

          ctx.save();
          if (this.facing === -1) {
            ctx.scale(-1, 1);
          }

          ctx.drawImage(heroImg, c * cellW, r * cellH, cellW, cellH, -drawW/2, -drawH/2 - 8, drawW, drawH);
          ctx.restore();
        } else {
          // Fallback procedural Sun Wukong
          ctx.beginPath();
          ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
          ctx.fillStyle = '#f59e0b';
          ctx.fill();
          ctx.strokeStyle = '#fff';
          ctx.lineWidth = 3;
          ctx.stroke();

          // Golden Crown & Staff
          ctx.fillStyle = '#ef4444';
          ctx.fillRect(-12, -26, 24, 6);
          ctx.strokeStyle = '#facc15';
          ctx.lineWidth = 4;
          ctx.beginPath();
          ctx.moveTo(-18, 0);
          ctx.lineTo(24, 0);
          ctx.stroke();
        }

        ctx.restore();
      }
    }

    const player = new Player();

    // ==========================================
    // 30-LEVEL BOSS PROGRESSION & MONSTERS
    // ==========================================
    const ENEMY_TYPES = {
      // Normal / Elite Enemies
      demon_ape: { name: '花果山狂猿妖', maxHp: 75, speed: 120, radius: 26, sheet: 'monsters_beasts', row: 4, cols: 6, rows: 6, behavior: 'swarmer' },
      cave_spider: { name: '盘丝洞毒蛛兵', maxHp: 60, speed: 135, radius: 24, sheet: 'infinite_bosses_a', row: 0, cols: 4, rows: 4, behavior: 'shooter' },
      nether_ghost: { name: '幽冥鬼使幽灵', maxHp: 85, speed: 100, radius: 26, sheet: 'monsters_beasts', row: 5, cols: 6, rows: 6, behavior: 'ghost' },
      tianbing: { name: '天庭神威神将', maxHp: 160, speed: 105, radius: 28, sheet: 'monsters_beasts', row: 0, cols: 6, rows: 6, behavior: 'shield_soldier' },
      tian_archer: { name: '灵霄神射弓手', maxHp: 70, speed: 135, radius: 24, sheet: 'monsters_beasts', row: 1, cols: 6, rows: 6, behavior: 'shooter' },
      bagua_golem: { name: '太上八卦傀儡', maxHp: 260, speed: 70, radius: 36, sheet: 'monsters_beasts', row: 3, cols: 6, rows: 6, behavior: 'smasher' },

      // 6 Major Story Bosses (Every 30 Chambers)
      boss_spider: { name: '盘丝洞·蜘蛛精七仙姑 (第30重天)', isBoss: true, maxHp: 4800, speed: 115, radius: 64, sheet: 'infinite_bosses_a', row: 0, cols: 4, rows: 4, behavior: 'boss_spider' },
      boss_baigu: { name: '白虎岭·白骨精三变夫人 (第60重天)', isBoss: true, maxHp: 9500, speed: 125, radius: 64, sheet: 'infinite_bosses_a', row: 1, cols: 4, rows: 4, behavior: 'boss_baigu' },
      boss_jin_yin: { name: '平顶山莲花洞·金角银角双王 (第90重天)', isBoss: true, maxHp: 15000, speed: 130, radius: 68, sheet: 'infinite_bosses_a', row: 2, cols: 4, rows: 4, behavior: 'boss_jin_yin' },
      boss_erlang: { name: '灌江口·二郎神杨戬与哮天犬 (第120重天)', isBoss: true, maxHp: 23500, speed: 155, radius: 66, sheet: 'infinite_bosses_a', row: 0, cols: 2, rows: 2, isRightHalf: true, behavior: 'boss_erlang' },
      boss_buddha: { name: '大日雷音寺·大日如来佛祖 (第150重天)', isBoss: true, maxHp: 42000, speed: 90, radius: 80, sheet: 'infinite_bosses_b', row: 0, cols: 4, rows: 4, behavior: 'boss_buddha' },
      boss_tongbei: { name: '混世魔猴·通臂猿猴 (最终决战 第180重天)', isBoss: true, maxHp: 68000, speed: 165, radius: 75, sheet: 'infinite_bosses_b', row: 2, cols: 4, rows: 4, isFinalBoss: true, behavior: 'boss_tongbei' }
    };

    class Enemy {
      constructor(typeKey, x, y) {
        this.typeKey = typeKey;
        const def = ENEMY_TYPES[typeKey] || ENEMY_TYPES['demon_ape'];
        this.name = def.name;
        this.isBoss = def.isBoss || false;
        this.isFinalBoss = def.isFinalBoss || false;
        this.maxHp = def.maxHp * (1 + (gameState.chamberIndex * 0.035));
        this.hp = this.maxHp;
        this.speed = def.speed;
        this.radius = def.radius;
        this.sheet = def.sheet;
        this.row = def.row || 0;
        this.cols = def.cols || 4;
        this.rows = def.rows || 4;
        this.isRightHalf = def.isRightHalf || false;
        this.behavior = def.behavior;
        this.x = x;
        this.y = y;
        this.vx = 0;
        this.vy = 0;
        this.facing = 1;
        this.alive = true;
        this.attackTimer = 0;
        this.burnTimer = 0;
        this.burnDmg = 0;
        this.freezeTimer = 0;
        this.slowTimer = 0;
        this.slowAmount = 0;
        this.phase = 1;
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

      takeDamage(amount, isCrit = false) {
        this.hp -= amount;
        floatingTexts.push(new FloatingText(this.x, this.y - 20, Math.round(amount), isCrit ? '#facc15' : '#ffffff', isCrit ? 19 : 13));

        if (this.isFinalBoss && this.phase === 1 && this.hp <= this.maxHp * 0.5) {
          this.phase = 2;
          this.radius = 90;
          sound.playAwaken();
          createScreenShake(18);
          fxList.push(new Shockwave(this.x, this.y, 300, '#ef4444'));
          floatingTexts.push(new FloatingText(this.x, this.y - 60, '万妖魔躯 · 魔猿法天象地!', '#ef4444', 24));
        }

        if (this.hp <= 0 && this.alive) {
          this.alive = false;
          gameState.enemiesKilled++;
          gameState.gold += Math.floor(Math.random() * 10) + (this.isBoss ? 120 : 6);
          gameState.ashes += Math.floor(Math.random() * 5) + (this.isBoss ? 60 : 3);

          if (this.isBoss) {
            sound.playGong();
            createScreenShake(14);
          }

          updateHUD();
        }
      }

      update(dt) {
        if (!this.alive) return;

        if (this.burnTimer > 0) {
          this.burnTimer -= dt;
          this.hp -= (this.burnDmg * dt);
          if (this.hp <= 0) this.takeDamage(1);
        }

        if (this.freezeTimer > 0) {
          this.freezeTimer -= dt;
          return;
        }

        let speedMod = 1.0;
        if (this.slowTimer > 0) {
          this.slowTimer -= dt;
          speedMod *= (1 - this.slowAmount);
        }

        const distToPlayer = Math.hypot(player.x - this.x, player.y - this.y);
        const angleToPlayer = Math.atan2(player.y - this.y, player.x - this.x);

        this.facing = player.x < this.x ? -1 : 1;
        this.attackTimer += dt;

        // Behaviors
        if (this.behavior === 'swarmer' || this.behavior === 'charger') {
          if (distToPlayer > this.radius + player.radius) {
            this.vx = Math.cos(angleToPlayer) * this.speed * speedMod;
            this.vy = Math.sin(angleToPlayer) * this.speed * speedMod;
          } else {
            if (this.attackTimer >= 1.1) {
              this.attackTimer = 0;
              player.takeDamage(16);
            }
          }
        } else if (this.behavior === 'shooter') {
          if (distToPlayer < 240) {
            this.vx = -Math.cos(angleToPlayer) * this.speed * 0.8 * speedMod;
            this.vy = -Math.sin(angleToPlayer) * this.speed * 0.8 * speedMod;
          } else if (distToPlayer > 360) {
            this.vx = Math.cos(angleToPlayer) * this.speed * speedMod;
            this.vy = Math.sin(angleToPlayer) * this.speed * speedMod;
          } else {
            this.vx *= 0.8;
            this.vy *= 0.8;
          }

          if (this.attackTimer >= 2.0) {
            this.attackTimer = 0;
            projectiles.push(new Projectile(this.x, this.y, Math.cos(angleToPlayer)*280, Math.sin(angleToPlayer)*280, 16, '#38bdf8', true));
          }
        } else if (this.behavior === 'boss_spider') {
          this.vx = Math.cos(angleToPlayer) * this.speed * 0.7 * speedMod;
          this.vy = Math.sin(angleToPlayer) * this.speed * 0.7 * speedMod;

          if (this.attackTimer >= 2.2) {
            this.attackTimer = 0;
            for (let i = -2; i <= 2; i++) {
              const ang = angleToPlayer + (i * 0.25);
              projectiles.push(new Projectile(this.x, this.y, Math.cos(ang)*260, Math.sin(ang)*260, 22, '#22c55e', true));
            }
          }
        } else if (this.behavior === 'boss_baigu') {
          this.vx = Math.cos(angleToPlayer) * this.speed * 0.75 * speedMod;
          this.vy = Math.sin(angleToPlayer) * this.speed * 0.75 * speedMod;

          if (this.attackTimer >= 2.0) {
            this.attackTimer = 0;
            const count = 6;
            for (let i = 0; i < count; i++) {
              const ang = angleToPlayer + (i * Math.PI * 2 / count);
              projectiles.push(new Projectile(this.x, this.y, Math.cos(ang)*250, Math.sin(ang)*250, 25, '#10b981', true));
            }
          }
        } else if (this.behavior === 'boss_jin_yin') {
          this.vx = Math.cos(angleToPlayer) * this.speed * 0.8 * speedMod;
          this.vy = Math.sin(angleToPlayer) * this.speed * 0.8 * speedMod;

          if (this.attackTimer >= 1.8) {
            this.attackTimer = 0;
            for (let i = -3; i <= 3; i++) {
              const ang = angleToPlayer + (i * 0.18);
              projectiles.push(new Projectile(this.x, this.y, Math.cos(ang)*300, Math.sin(ang)*300, 28, '#f59e0b', true));
            }
          }
        } else if (this.behavior === 'boss_erlang') {
          this.vx = Math.cos(angleToPlayer) * this.speed * 0.85 * speedMod;
          this.vy = Math.sin(angleToPlayer) * this.speed * 0.85 * speedMod;

          if (this.attackTimer >= 2.2) {
            this.attackTimer = 0;
            for (let i = 0; i < 8; i++) {
              const ang = angleToPlayer + (i * Math.PI * 2 / 8);
              projectiles.push(new Projectile(this.x, this.y, Math.cos(ang)*320, Math.sin(ang)*320, 32, '#facc15', true));
            }
            fxList.push(new Shockwave(this.x, this.y, 220, '#facc15'));
          }
        } else if (this.behavior === 'boss_buddha') {
          this.vx = Math.cos(angleToPlayer) * this.speed * 0.4 * speedMod;
          this.vy = Math.sin(angleToPlayer) * this.speed * 0.4 * speedMod;

          if (this.attackTimer >= 2.0) {
            this.attackTimer = 0;
            const count = 12;
            for (let i = 0; i < count; i++) {
              const ang = (i * Math.PI * 2 / count) + (Date.now() * 0.001);
              projectiles.push(new Projectile(this.x, this.y, Math.cos(ang)*270, Math.sin(ang)*270, 35, '#fef08a', true));
            }
            createScreenShake(8);
          }
        } else if (this.behavior === 'boss_tongbei') {
          const phaseMult = this.phase === 2 ? 1.4 : 1.0;
          this.vx = Math.cos(angleToPlayer) * this.speed * phaseMult * speedMod;
          this.vy = Math.sin(angleToPlayer) * this.speed * phaseMult * speedMod;

          if (this.attackTimer >= (this.phase === 2 ? 1.4 : 2.0)) {
            this.attackTimer = 0;
            const count = this.phase === 2 ? 16 : 10;
            for (let i = 0; i < count; i++) {
              const ang = (i * Math.PI * 2 / count) + (Math.sin(Date.now() * 0.002) * 0.5);
              projectiles.push(new Projectile(this.x, this.y, Math.cos(ang)*340, Math.sin(ang)*340, this.phase === 2 ? 40 : 30, '#ef4444', true));
            }
            fxList.push(new Shockwave(this.x, this.y, 280, '#ef4444'));
            createScreenShake(12);
          }
        }

        this.x += this.vx * dt;
        this.y += this.vy * dt;
      }

      draw(ctx) {
        if (!this.alive) return;
        ctx.save();
        ctx.translate(this.x, this.y);

        const img = loadedImages[this.sheet] || loadedImages['monsters_beasts'];
        if (img && img.complete && img.naturalWidth > 0) {
          let cellW = img.naturalWidth / this.cols;
          let cellH = img.naturalHeight / this.rows;
          let offsetX = 0;

          if (this.isRightHalf) {
            cellW = img.naturalWidth / 2;
            cellH = img.naturalHeight / 2;
            offsetX = img.naturalWidth / 2;
          }

          const c = Math.floor((Date.now() / 140) % (this.cols > 4 ? 4 : this.cols));
          const r = this.row;

          const scale = this.isFinalBoss ? (this.phase === 2 ? 2.8 : 2.0) : (this.isBoss ? 2.2 : 1.3);
          const drawW = 80 * scale;
          const drawH = 80 * scale;

          ctx.save();
          if (this.facing === -1) {
            ctx.scale(-1, 1);
          }

          ctx.drawImage(img, offsetX + c * cellW, r * cellH, cellW, cellH, -drawW/2, -drawH/2 - 6, drawW, drawH);
          ctx.restore();
        } else {
          ctx.beginPath();
          ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
          ctx.fillStyle = this.isBoss ? '#ef4444' : '#d97706';
          ctx.fill();
          ctx.strokeStyle = '#ffffff';
          ctx.lineWidth = 2;
          ctx.stroke();
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

        if (!this.isBoss) {
          const hpPct = Math.max(0, this.hp / this.maxHp);
          const barW = this.radius * 2;
          ctx.fillStyle = '#110e18';
          ctx.fillRect(-barW/2, -this.radius - 14, barW, 6);
          ctx.fillStyle = '#ef4444';
          ctx.fillRect(-barW/2, -this.radius - 14, barW * hpPct, 6);
        }

        ctx.restore();
      }
    }

    let enemies = [];

    // ==========================================
    // PROJECTILES & VISUAL FX CLASSES
    // ==========================================
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
            if (e.alive && Math.hypot(e.x - this.x, e.y - this.y) <= e.radius + this.radius) {
              this.alive = false;
              e.takeDamage(this.dmg);
            }
          });
        }
      }

      draw(ctx) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 10;
        ctx.restore();
      }
    }

    let projectiles = [];
    let fxList = [];
    let floatingTexts = [];

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
        ctx.font = `bold ${this.size}px 'Ma Shan Zheng', serif`;
        ctx.fillStyle = this.color;
        ctx.globalAlpha = Math.max(0, this.alpha);
        ctx.textAlign = 'center';
        ctx.fillText(this.text, this.x, this.y);
        ctx.restore();
      }
    }

    class AnimatedAttackSweep {
      constructor(x, y, angle, radius, color = '#facc15') {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.radius = radius;
        this.color = color;
        this.alpha = 1.0;
        this.life = 0.18;
      }

      update(dt) {
        this.life -= dt;
        this.alpha = this.life / 0.18;
      }

      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);
        ctx.beginPath();
        ctx.arc(0, 0, this.radius, -Math.PI * 0.45, Math.PI * 0.45);
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 15;
        ctx.globalAlpha = Math.max(0, this.alpha);
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 16;
        ctx.stroke();
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

    function createScreenShake(amount) {
      gameState.screenShake = amount;
    }

    // ==========================================
    // EXIT GATES & STORY PROGRESSION
    // ==========================================
    let exitGates = [];

    function setupExitGates() {
      exitGates = [];
      const godKeys = Object.keys(GODS);

      const count = 2 + (Math.random() > 0.5 ? 1 : 0);
      for (let i = 0; i < count; i++) {
        const ang = (i / count) * Math.PI * 2;
        const gateX = Math.cos(ang) * 450;
        const gateY = Math.sin(ang) * 450;

        let rewardType = 'god';
        let godKey = godKeys[Math.floor(Math.random() * godKeys.length)];
        let label = GODS[godKey].name;

        const roll = Math.random();
        if (roll < 0.25) {
          rewardType = 'peach';
          label = '天庭蟠桃 (神效精进)';
        } else if (roll < 0.40) {
          rewardType = 'shop';
          label = '龙宫宝阁 (灵丹妙药)';
        } else if (roll < 0.55) {
          rewardType = 'heart';
          label = '万年人参果 (+气血)';
        } else if (roll < 0.70) {
          rewardType = 'ashes';
          label = '功德灵砂 (+修为)';
        }

        exitGates.push({
          x: gateX,
          y: gateY,
          radius: 52,
          rewardType: rewardType,
          godKey: godKey,
          label: label
        });
      }
    }

    function startChamber(index) {
      gameState.chamberIndex = index;
      gameState.chamberCleared = false;
      enemies = [];
      projectiles = [];
      fxList = [];
      exitGates = [];

      const titleEl = document.getElementById('chamber-name');
      const subEl = document.getElementById('chamber-sub');

      if (index <= 30) {
        gameState.biome = 1;
        titleEl.innerText = `花果山水帘洞与盘丝岭 · 第 ${index} 重天 / 180 重天`;
        subEl.innerText = '洞天福地初悟道 · 盘丝幽径斩蛛妖';
      } else if (index <= 60) {
        gameState.biome = 2;
        titleEl.innerText = `白虎岭白骨洞与幽冥界 · 第 ${index} 重天 / 180 重天`;
        subEl.innerText = '白骨夫人三变化 · 阴阳两界显威风';
      } else if (index <= 90) {
        gameState.biome = 3;
        titleEl.innerText = `平顶山莲花洞 · 第 ${index} 重天 / 180 重天`;
        subEl.innerText = '紫金红葫芦锁乾坤 · 幌金绳七星宝剑';
      } else if (index <= 120) {
        gameState.biome = 4;
        titleEl.innerText = `南天门与天庭灵霄界 · 第 ${index} 重天 / 180 重天`;
        subEl.innerText = '金阙云宫灵霄殿 · 二郎真君战大圣';
      } else if (index <= 150) {
        gameState.biome = 5;
        titleEl.innerText = `西天大雷音寺与五行天 · 第 ${index} 重天 / 180 重天`;
        subEl.innerText = '大日如来佛光照 · 五指神山定乾坤';
      } else if (index <= 180) {
        gameState.biome = 6;
        titleEl.innerText = `混沌渊海·决战通臂猿猴 · 第 ${index} 重天 / 180 重天`;
        subEl.innerText = '混世四猴善恶决 · 破灭心魔证大道';
      } else {
        gameState.biome = 7;
        titleEl.innerText = `无尽混元轮回试炼 · 第 ${index} 重天`;
        subEl.innerText = '超脱三界外，不在五行中';
      }

      const bossHud = document.getElementById('boss-hud');
      const isBossChamber = (index === 30 || index === 60 || index === 90 || index === 120 || index === 150 || index === 180);

      if (isBossChamber) {
        gameState.chamberType = 'boss';
        bossHud.style.display = 'flex';

        let bossKey = 'boss_spider';
        if (index === 60) bossKey = 'boss_baigu';
        if (index === 90) bossKey = 'boss_jin_yin';
        if (index === 120) bossKey = 'boss_erlang';
        if (index === 150) bossKey = 'boss_buddha';
        if (index === 180) bossKey = 'boss_tongbei';

        const boss = new Enemy(bossKey, 0, -220);
        enemies.push(boss);
        document.getElementById('boss-name-text').innerText = boss.name;
      } else {
        gameState.chamberType = 'normal';
        bossHud.style.display = 'none';

        const enemyCount = 3 + Math.floor((index % 30) * 0.2);
        let availableTypes = ['demon_ape', 'cave_spider'];
        if (index > 30) availableTypes = ['cave_spider', 'nether_ghost'];
        if (index > 60) availableTypes = ['demon_ape', 'nether_ghost', 'tianbing'];
        if (index > 90) availableTypes = ['tianbing', 'tian_archer', 'bagua_golem'];
        if (index > 120) availableTypes = ['tianbing', 'tian_archer', 'bagua_golem', 'demon_ape'];

        for (let i = 0; i < enemyCount; i++) {
          const t = availableTypes[Math.floor(Math.random() * availableTypes.length)];
          const ang = Math.random() * Math.PI * 2;
          const dist = 220 + Math.random() * 320;
          enemies.push(new Enemy(t, Math.cos(ang)*dist, Math.sin(ang)*dist));
        }
      }

      player.x = 0;
      player.y = 200;
      updateHUD();
    }

    function checkChamberClear() {
      if (gameState.chamberCleared) return;
      if (enemies.length > 0 && enemies.every(e => !e.alive)) {
        gameState.chamberCleared = true;
        sound.playGong();
        setupExitGates();
      }
    }

    // ==========================================
    // MODALS & BOONS LOGIC
    // ==========================================
    function openGodBoonModal(godKey) {
      gameState.isPaused = true;
      const god = GODS[godKey] || GODS['erlangshen'];
      const modal = document.getElementById('boon-modal');
      const container = document.getElementById('boon-choices-container');

      document.getElementById('god-name').innerText = god.name;
      document.getElementById('god-title').innerText = god.title;
      document.getElementById('god-quote').innerText = god.quotes[Math.floor(Math.random() * god.quotes.length)];

      const portrait = document.getElementById('god-portrait');
      const godSheet = loadedImages['all_10_gods'];
      if (godSheet && godSheet.complete && godSheet.naturalWidth > 0) {
        const col = god.portraitIndex % 5;
        const row = Math.floor(god.portraitIndex / 5);
        portrait.style.backgroundImage = `url(${godSheet.src})`;
        portrait.style.backgroundPosition = `-${col * 120}px -${row * 120}px`;
        portrait.style.backgroundSize = `600px 240px`;
      }

      container.innerHTML = '';
      const availableBoons = [...god.boons].sort(() => 0.5 - Math.random()).slice(0, 3);

      availableBoons.forEach(boon => {
        const card = document.createElement('div');
        card.className = 'boon-card';
        card.innerHTML = `
          <div>
            <div class="boon-slot-tag">${boon.slot}</div>
            <div class="boon-name">${boon.name}</div>
            <div class="boon-desc">${boon.desc}</div>
          </div>
          <div class="boon-action-btn">领受仙法神通</div>
        `;
        card.onclick = () => {
          applyBoon(boon, godKey);
          modal.style.display = 'none';
          gameState.isPaused = false;
          sound.playJadeChime();
        };
        container.appendChild(card);
      });

      modal.style.display = 'flex';
    }

    function applyBoon(boon, godKey) {
      const slot = boon.slot;
      const boonData = { ...boon, godKey: godKey, level: 1 };

      if (slot.includes('普攻') || slot.includes('普通攻击')) {
        player.boons.attack = boonData;
        document.getElementById('boon-tag-attack').innerText = boon.name;
      } else if (slot.includes('特殊')) {
        player.boons.special = boonData;
        document.getElementById('boon-tag-special').innerText = boon.name;
      } else if (slot.includes('法术') || slot.includes('法阵')) {
        player.boons.cast = boonData;
        document.getElementById('boon-tag-cast').innerText = boon.name;
      } else if (slot.includes('闪避') || slot.includes('身法')) {
        player.boons.dash = boonData;
        document.getElementById('boon-tag-dash').innerText = boon.name;
      } else if (slot.includes('绝技') || slot.includes('觉醒')) {
        player.boons.hex = boonData;
        document.getElementById('boon-tag-hex').innerText = boon.name;
      } else {
        player.boons.passives.push(boonData);
      }
      gameState.boonsCount++;
      updateHUD();
    }

    // Heavenly Peaches Modal
    function openPeachModal() {
      gameState.isPaused = true;
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
      if (player.boons.attack) equipped.push(player.boons.attack);
      if (player.boons.special) equipped.push(player.boons.special);
      if (player.boons.cast) equipped.push(player.boons.cast);
      if (player.boons.dash) equipped.push(player.boons.dash);
      player.boons.passives.forEach(b => equipped.push(b));

      if (equipped.length === 0) {
        player.maxHp += 30;
        player.hp = Math.min(player.maxHp, player.hp + 30);
        gameState.peachesEaten++;
        sound.playPeachBite();
        modal.style.display = 'none';
        gameState.isPaused = false;
        floatingTexts.push(new FloatingText(player.x, player.y - 40, '气血上限 +30 (仙桃延寿)!', '#fb7185'));
        return;
      }

      const choices = equipped.sort(() => 0.5 - Math.random()).slice(0, 3);
      choices.forEach(b => {
        const card = document.createElement('div');
        card.className = 'boon-card';
        card.innerHTML = `
          <div>
            <div class="boon-slot-tag" style="background: rgba(251, 113, 133, 0.2); border-color: var(--peach-pink); color: var(--peach-glow);">${b.slot} · 第 ${b.level || 1} 重 ➔ 第 ${(b.level || 1) + 1} 重</div>
            <div class="boon-name" style="color: var(--peach-glow);">${b.name}</div>
            <div class="boon-desc">${b.desc}</div>
          </div>
          <div class="boon-action-btn" style="background: linear-gradient(180deg, #e11d48, #9f1239);">服食蟠桃 · 提升重数</div>
        `;
        card.onclick = () => {
          b.level = (b.level || 1) + 1;
          gameState.peachesEaten++;
          sound.playPeachBite();
          modal.style.display = 'none';
          gameState.isPaused = false;
          floatingTexts.push(new FloatingText(player.x, player.y - 40, `第 ${b.level} 重 ${b.name}!`, '#fb7185'));
          updateHUD();
        };
        container.appendChild(card);
      });

      modal.style.display = 'flex';
    }

    // Shop Modal
    function openShopModal() {
      gameState.isPaused = true;
      const modal = document.getElementById('shop-modal');
      const container = document.getElementById('shop-choices-container');
      container.innerHTML = '';

      const items = [
        { name: '万年九叶灵芝 (疗伤生肌)', desc: '恢复 60 点气血，并永久提升 25 点气血上限。', cost: 60, action: () => { player.maxHp += 25; player.hp = Math.min(player.maxHp, player.hp + 60); } },
        { name: '王母天庭蟠桃 (仙品神果)', desc: '随机令一项已习得的神通品阶重数 +1。', cost: 95, action: () => { openPeachModal(); } },
        { name: '太上开光功德符 (道门至宝)', desc: '直接获得 30 点功德灵砂以供修炼七十二变。', cost: 50, action: () => { gameState.ashes += 30; } }
      ];

      items.forEach(it => {
        const card = document.createElement('div');
        card.className = 'boon-card';
        card.innerHTML = `
          <div>
            <div class="boon-slot-tag">龙宫珍宝</div>
            <div class="boon-name">${it.name}</div>
            <div class="boon-desc">${it.desc}</div>
          </div>
          <div class="boon-action-btn">兑换: 🪙 ${it.cost} 灵石</div>
        `;
        card.onclick = () => {
          if (gameState.gold >= it.cost) {
            gameState.gold -= it.cost;
            it.action();
            sound.playJadeChime();
            updateHUD();
            openShopModal();
          } else {
            alert('灵石不足！');
          }
        };
        container.appendChild(card);
      });

      modal.style.display = 'flex';
    }

    function closeShopModal() {
      document.getElementById('shop-modal').style.display = 'none';
      gameState.isPaused = false;
    }

    // Altar of 72 Transformations
    function openAltarOfTransformations() {
      gameState.isPaused = true;
      const modal = document.getElementById('altar-modal');
      const container = document.getElementById('altar-items-container');
      container.innerHTML = '';

      const traits = [
        { key: 'stone_monkey', name: '石猴金身 (混元仙躯)', desc: '每阶永久提升 25 点气血上限与护甲。', cost: 10 },
        { key: 'golden_eyes', name: '火眼金睛 (洞察破妄)', desc: '每阶提升 8% 暴击率与 15% 暴击伤害。', cost: 15 },
        { key: 'somersault', name: '筋斗云精通 (浮光掠影)', desc: '每阶增加 1 次筋斗云瞬移闪避充能。', cost: 25 },
        { key: 'hair_clones', name: '身外化身 (毫毛变幻)', desc: '攻击命中概率召唤毫毛分身协助战阵。', cost: 20 },
        { key: 'qi_circulation', name: '胎息纳气 (归元吐纳)', desc: '提升 15 点真气上限与 0.8 每秒回气。', cost: 12 },
        { key: 'nirvana_body', name: '不灭金身 (九转还魂)', desc: '增加 1 次阵亡金身复活次数。', cost: 35 }
      ];

      traits.forEach(tr => {
        const lvl = metaUpgrades[tr.key];
        const cost = tr.cost * (lvl + 1);
        const div = document.createElement('div');
        div.className = 'altar-item';
        div.innerHTML = `
          <div class="altar-info">
            <div class="altar-name">${tr.name}</div>
            <div class="altar-desc">${tr.desc}</div>
            <div class="altar-level">当前重数: 第 ${lvl} 重</div>
          </div>
          <button class="altar-btn" ${gameState.ashes < cost ? 'disabled' : ''} onclick="upgradeTrait('${tr.key}', ${cost})">参悟修行 (${cost} ✨)</button>
        `;
        container.appendChild(div);
      });

      modal.style.display = 'flex';
    }

    function upgradeTrait(key, cost) {
      if (gameState.ashes >= cost) {
        gameState.ashes -= cost;
        metaUpgrades[key]++;
        player.applyMetaUpgrades();
        sound.playJadeChime();
        updateHUD();
        openAltarOfTransformations();
      }
    }

    function closeAltarModal() {
      document.getElementById('altar-modal').style.display = 'none';
      gameState.isPaused = false;
    }

    // Codex Modal
    function openSkillCodex() {
      gameState.isPaused = true;
      const modal = document.getElementById('codex-modal');
      const container = document.getElementById('codex-cards-container');
      container.innerHTML = '';

      for (let k in GODS) {
        const g = GODS[k];
        const card = document.createElement('div');
        card.className = 'codex-card';
        card.innerHTML = `
          <div class="codex-god-title" style="color: ${g.color};">${g.name} (${g.title})</div>
          <div class="codex-boon-list">
            ${g.boons.map(b => `<div>• <b>${b.name}</b> [${b.slot}]: ${b.desc}</div>`).join('')}
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
      gameState.isPaused = true;
      const modal = document.getElementById('gameover-modal');
      const title = document.getElementById('gameover-title');
      const sub = document.getElementById('gameover-sub');

      if (isVictory) {
        title.className = 'gameover-title victory';
        title.innerText = '功德圆满 · 威震三界！';
        sub.innerText = '孙悟空破灭通臂猿猴魔心，扫清三界妖氛，证道斗战胜佛！';
        sound.playGong();
      } else {
        title.className = 'gameover-title defeat';
        title.innerText = '道消身殒';
        sub.innerText = '形骸虽散，神魂不灭。且回花果山水帘洞潜心参悟七十二变！';
      }

      document.getElementById('stat-chambers').innerText = `${gameState.chamberIndex} / 180 重天`;
      document.getElementById('stat-kills').innerText = gameState.enemiesKilled;
      document.getElementById('stat-boons').innerText = gameState.boonsCount;
      document.getElementById('stat-peaches').innerText = gameState.peachesEaten;
      document.getElementById('stat-ashes').innerText = gameState.ashes;

      modal.style.display = 'flex';
    }

    function restartRun() {
      document.getElementById('gameover-modal').style.display = 'none';
      gameState.isPaused = false;
      player.resetForRun();
      startChamber(1);
    }

    function updateHUD() {
      const hpPct = Math.max(0, player.hp / player.maxHp) * 100;
      const qiPct = Math.max(0, player.qi / player.maxQi) * 100;
      const awakenPct = Math.max(0, player.awakenGauge / player.maxAwakenGauge) * 100;

      document.getElementById('hp-bar').style.width = `${hpPct}%`;
      document.getElementById('hp-text').innerText = `${Math.round(player.hp)} / ${player.maxHp}`;

      document.getElementById('qi-bar').style.width = `${qiPct}%`;
      document.getElementById('qi-text').innerText = `${Math.round(player.qi)} / ${player.maxQi}`;

      document.getElementById('awaken-bar').style.width = `${awakenPct}%`;
      document.getElementById('awaken-text').innerText = player.isAwakened ? `狂暴觉醒中 (${Math.ceil(player.awakenDuration)}秒)` : (awakenPct >= 100 ? '觉醒就绪: 按 [R/F] 施展' : `大闹天宫: ${Math.round(awakenPct)}%`);

      document.getElementById('gold-val').innerText = gameState.gold;
      document.getElementById('ashes-val').innerText = gameState.ashes;
      document.getElementById('peaches-val').innerText = gameState.peachesEaten;
      document.getElementById('lives-val').innerText = player.lives;

      if (gameState.chamberType === 'boss') {
        const boss = enemies.find(e => e.isBoss && e.alive);
        if (boss) {
          const bossPct = Math.max(0, boss.hp / boss.maxHp) * 100;
          document.getElementById('boss-bar-fill').style.width = `${bossPct}%`;
        }
      }
    }

    // ==========================================
    // MAIN GAME LOOP & RENDERING (FAIL-SAFE)
    // ==========================================
    let lastTime = 0;

    function gameLoop(currentTime) {
      requestAnimationFrame(gameLoop);

      try {
        if (!lastTime) lastTime = currentTime;
        const dt = Math.min(0.05, (currentTime - lastTime) / 1000);
        lastTime = currentTime;

        if (!gameState.isPaused) {
          player.update(dt);

          enemies.forEach(e => e.update(dt));
          enemies = enemies.filter(e => e.alive || e.burnTimer > 0);

          projectiles.forEach(p => p.update(dt));
          projectiles = projectiles.filter(p => p.alive);

          fxList.forEach(fx => fx.update(dt));
          fxList = fxList.filter(fx => fx.alpha > 0);

          floatingTexts.forEach(ft => ft.update(dt));
          floatingTexts = floatingTexts.filter(ft => ft.alpha > 0);

          checkChamberClear();

          if (gameState.chamberCleared) {
            exitGates.forEach(gate => {
              const dist = Math.hypot(player.x - gate.x, player.y - gate.y);
              if (dist <= gate.radius + player.radius) {
                if (gate.rewardType === 'god') {
                  openGodBoonModal(gate.godKey);
                } else if (gate.rewardType === 'peach') {
                  openPeachModal();
                } else if (gate.rewardType === 'shop') {
                  openShopModal();
                } else if (gate.rewardType === 'heart') {
                  player.maxHp += 30;
                  player.hp = Math.min(player.maxHp, player.hp + 30);
                  sound.playJadeChime();
                  floatingTexts.push(new FloatingText(player.x, player.y - 40, '气血上限 +30!', '#10b981'));
                } else if (gate.rewardType === 'ashes') {
                  gameState.ashes += 25;
                  sound.playJadeChime();
                  floatingTexts.push(new FloatingText(player.x, player.y - 40, '功德灵砂 +25!', '#c084fc'));
                }

                if (gameState.chamberIndex >= 180 && !enemies.some(e => e.isFinalBoss && e.alive)) {
                  handleGameOver(true);
                } else {
                  startChamber(gameState.chamberIndex + 1);
                }
              }
            });
          }
        }

        // Render Canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        let shakeX = 0;
        let shakeY = 0;
        if (gameState.screenShake > 0) {
          shakeX = (Math.random() * 2 - 1) * gameState.screenShake;
          shakeY = (Math.random() * 2 - 1) * gameState.screenShake;
          gameState.screenShake = Math.max(0, gameState.screenShake - dt * 25);
        }

        ctx.translate(canvas.width / 2 - player.x + shakeX, canvas.height / 2 - player.y + shakeY);

        // 1. Draw Celestial Floor
        const floorImg = loadedImages['seamless_floor'];
        if (floorImg && floorImg.complete && floorImg.naturalWidth > 0) {
          ctx.drawImage(floorImg, -700, -700, 1400, 1400);
        } else {
          ctx.fillStyle = '#161026';
          ctx.fillRect(-700, -700, 1400, 1400);

          // Procedural Bagua Arena
          ctx.beginPath();
          ctx.arc(0, 0, 600, 0, Math.PI * 2);
          ctx.fillStyle = '#1a1330';
          ctx.fill();
          ctx.strokeStyle = '#e6b450';
          ctx.lineWidth = 6;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(0, 0, 300, 0, Math.PI * 2);
          ctx.strokeStyle = 'rgba(230, 180, 80, 0.4)';
          ctx.lineWidth = 3;
          ctx.stroke();
        }

        // Golden Boundary Frame
        ctx.strokeStyle = 'rgba(230, 180, 80, 0.75)';
        ctx.lineWidth = 10;
        ctx.strokeRect(-680, -680, 1360, 1360);

        // 2. Draw Exit Gates
        if (gameState.chamberCleared) {
          exitGates.forEach(gate => {
            ctx.save();
            ctx.translate(gate.x, gate.y);

            ctx.beginPath();
            ctx.arc(0, 0, gate.radius, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(230, 180, 80, 0.25)';
            ctx.fill();
            ctx.strokeStyle = '#facc15';
            ctx.lineWidth = 4;
            ctx.shadowColor = '#facc15';
            ctx.shadowBlur = 16;
            ctx.stroke();

            const rewImg = loadedImages['reward_icons'];
            if (rewImg && rewImg.complete && rewImg.naturalWidth > 0) {
              let col = 0, row = 0;
              if (gate.rewardType === 'peach') { col = 0; row = 0; }
              else if (gate.rewardType === 'shop') { col = 1; row = 0; }
              else if (gate.rewardType === 'heart') { col = 0; row = 1; }
              else if (gate.rewardType === 'ashes') { col = 1; row = 1; }
              else if (gate.rewardType === 'god') {
                const godsImg = loadedImages['all_10_gods'];
                if (godsImg && godsImg.complete && godsImg.naturalWidth > 0) {
                  const gIndex = GODS[gate.godKey].portraitIndex;
                  const gCol = gIndex % 5;
                  const gRow = Math.floor(gIndex / 5);
                  const gW = godsImg.naturalWidth / 5;
                  const gH = godsImg.naturalHeight / 2;
                  ctx.drawImage(godsImg, gCol * gW, gRow * gH, gW, gH, -36, -36, 72, 72);
                }
              }

              if (gate.rewardType !== 'god') {
                const rW = rewImg.naturalWidth / 2;
                const rH = rewImg.naturalHeight / 2;
                ctx.drawImage(rewImg, col * rW, row * rH, rW, rH, -36, -36, 72, 72);
              }
            } else {
              // Fallback text icon
              ctx.font = '28px sans-serif';
              ctx.textAlign = 'center';
              ctx.textBaseline = 'middle';
              let emoji = '🍑';
              if (gate.rewardType === 'shop') emoji = '🏮';
              if (gate.rewardType === 'heart') emoji = '💖';
              if (gate.rewardType === 'ashes') emoji = '✨';
              if (gate.rewardType === 'god') emoji = '⚡';
              ctx.fillText(emoji, 0, 0);
            }

            ctx.font = "bold 15px 'Ma Shan Zheng', serif";
            ctx.fillStyle = '#fff2a8';
            ctx.textAlign = 'center';
            ctx.shadowColor = '#000';
            ctx.shadowBlur = 6;
            ctx.fillText(gate.label, 0, -gate.radius - 12);

            ctx.restore();
          });
        }

        // 3. Draw Entities
        player.draw(ctx);
        enemies.forEach(e => e.draw(ctx));
        projectiles.forEach(p => p.draw(ctx));
        fxList.forEach(fx => fx.draw(ctx));
        floatingTexts.forEach(ft => ft.draw(ctx));

        ctx.restore();
      } catch (err) {
        console.error("Game loop render error:", err);
      }
    }

    // Initialize & Launch
    player.resetForRun();
    startChamber(1);
    requestAnimationFrame(gameLoop);
  </script>
</body>
</html>
"""

final_html = html_template.replace('%ASSETS_JSON%', json.dumps(b64_data))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

with open('generate_game.py', 'w', encoding='utf-8') as f:
    f.write(f'''# Journey to the West: Havoc in Heaven build generator
import json
import base64
import os

b64_data = {json.dumps(b64_data)}

html_template = """{html_template}"""
final_html = html_template.replace('%ASSETS_JSON%', json.dumps(b64_data))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Successfully compiled Journey to the West index.html!")
''')

print(f"Successfully compiled Complete Journey to the West index.html ({len(final_html)} bytes)!")
