"""
Test suite for Journey to the West: Havoc in Heaven
"""

import os
import re
import hashlib
import json
from pathlib import Path

from PIL import Image


def connected_alpha_areas(image, threshold=20):
    """Return 8-connected visible component sizes for a single atlas cell."""
    alpha = image.convert("RGBA").getchannel("A")
    width, height = alpha.size
    visible = [value > threshold for value in alpha.getdata()]
    visited = bytearray(width * height)
    areas = []
    for start, is_visible in enumerate(visible):
        if not is_visible or visited[start]:
            continue
        visited[start] = 1
        stack = [start]
        area = 0
        while stack:
            index = stack.pop()
            area += 1
            x, y = index % width, index // width
            for ny in range(max(0, y - 1), min(height, y + 2)):
                for nx in range(max(0, x - 1), min(width, x + 2)):
                    neighbor = ny * width + nx
                    if visible[neighbor] and not visited[neighbor]:
                        visited[neighbor] = 1
                        stack.append(neighbor)
        areas.append(area)
    return sorted(areas, reverse=True)


def max_wide_alpha_row_streak(image, alpha_threshold=31, width_fraction=0.72):
    """Measure 2D rectangular matte bands, not legitimate thin staff runs."""
    alpha = image.convert("RGBA").getchannel("A")
    width, height = alpha.size
    values = list(alpha.getdata())
    required_run = int(width * width_fraction)
    widest_streak = current_streak = 0
    for y in range(height):
        longest = run = 0
        for value in values[y * width:(y + 1) * width]:
            if value > alpha_threshold:
                run += 1
                longest = max(longest, run)
            else:
                run = 0
        current_streak = current_streak + 1 if longest >= required_run else 0
        widest_streak = max(widest_streak, current_streak)
    return widest_streak

def test_game_features():
    assert os.path.exists("index.html"), "index.html must exist!"
    size = os.path.getsize("index.html")
    assert size > 2500000, f"index.html should contain embedded assets (size: {size})"
    print(f"File size: {size} bytes")

    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    source = Path("generate_complete_game.py").read_text(encoding="utf-8")

    # 1. Check HTML Structure & Tags
    assert "<style>" in html, "<style> must exist!"
    assert "</style>" in html, "</style> must exist!"
    assert "</head>" in html, "</head> must exist!"
    assert "<body>" in html, "<body> must exist!"
    assert '<canvas id="gameCanvas"' in html, "gameCanvas must exist!"
    assert '<canvas id="gameCanvas" role="img" tabindex="0"' in html, "The game canvas must accept keyboard focus after Start!"
    assert "</body>" in html, "</body> must exist!"
    assert "</html>" in html, "</html> must exist!"

    # Ensure style tag closes BEFORE body begins
    style_close = html.find("</style>")
    body_open = html.find("<body>")
    canvas_pos = html.find('<canvas id="gameCanvas"')
    script_open = html.find("<script>")
    script_close = html.find("</script>")
    body_close = html.find("</body>")

    assert style_close < body_open < canvas_pos < script_open < script_close < body_close, "HTML structure order must be correct!"

    # Launch, pause, accessibility and input-state regressions.
    assert 'id="start-screen"' in html, "An explicit start/onboarding screen must exist!"
    assert 'id="pause-modal"' in html, "A pause menu must exist!"
    assert "[Esc] Menu" in html and "Save & Exit" in html and "startOrContinueJourney()" in html, "Students must see that Esc opens a menu with Save & Exit!"
    assert "RUN_CHECKPOINT_SAVE_KEY = 'havocInHeavenRunCheckpointV1'" in html, "Run checkpoints need a dedicated browser-storage record!"
    assert "captureChapterStartCheckpoint();" in html and "currentChapterStartCheckpoint || captureChapterStartCheckpoint()" in html, "Save & Exit must use the start of the current chapter, never the live mid-fight enemy state!"
    assert "function restoreRunCheckpoint" in html and "startChamber(checkpoint.chapter)" in html, "Continue must rebuild the saved run at the beginning of its chapter!"
    assert "startChamber(151)" not in source, "The obsolete 151/100 Buddha transition must never return!"
    assert "const completedCutsceneChapter = buddhaCutsceneChapter || gameState.chamberIndex" in source and "completedCutsceneChapter === 32" in source, "Five-Finger Mountain must finish according to the chapter that opened its cutscene, not mutable later state!"
    assert "if (!buddhaCutsceneActive) return" in source and "buddhaCutsceneActive = false" in source, "Repeated cutscene clicks must not execute the Five-Finger Mountain transition twice!"
    assert "Math.min(campaignLastChapter" in source and "Number.isFinite(requestedChapter)" in source, "Every direct chapter transition must be clamped to the unified 1-100 campaign!"
    assert "gameState.chamberIndex === gameState.totalChambers" in source and "gameState.chamberIndex >= gameState.totalChambers" not in source, "Only Chapter 100 may award portal victory; Chapter 33 must continue to Chapter 34!"
    assert "const displayedChapter = Math.max(1, Math.min(gameState.totalChambers" in source, "Victory statistics must never display an impossible chapter such as 151/100!"
    assert "checkpointBoon(player.boons.attack)" in html and "boonLevels: { ...player.boonLevels }" in html, "Checkpoint saves must preserve equipped boons and Peach ranks!"
    assert "increaseRunMaxHp(amount, healing = amount)" in html, "All run-earned maximum Health must use one durable ledger!"
    assert "this.maxHp = this.metaMaxHp + Math.max(0, Number(this.runMaxHpBonus) || 0)" in html, "Meta/alignment recalculation must preserve maximum Health earned during the run!"
    assert "runMaxHpBonus: Math.max(0, Number(player.runMaxHpBonus) || 0)" in html, "Chapter checkpoints must save run-earned maximum Health!"
    assert "savedMaxHp - (player.metaMaxHp || player.maxHp)" in html, "Older checkpoints must recover their run-earned maximum Health safely!"
    assert source.count("player.increaseRunMaxHp(") == 5, "Every story, doctrine, Peach, shop, and gate maximum-Health reward must use the durable run ledger!"
    assert "Your save will resume from the beginning of Chapter" in html, "The pause menu must explain the chapter-start rollback clearly!"
    assert 'id="touch-controls"' in html, "Touch controls must exist!"
    assert 'role="dialog"' in html and 'aria-modal="true"' in html, "Modal semantics must exist!"
    assert 'id="tree-node-select"' in html and "getModalFocusables" in html, "Dialogs and the skill tree must be keyboard navigable!"
    assert 'gameState.hasStarted' in html, "Gameplay must be gated behind the Start action!"
    assert "function safeStorageGetItem" in html and "function safeStorageSetItem" in html, "Direct-file browser storage restrictions must not abort game initialization!"
    assert "const INITIAL_LANGUAGE = safeStorageGetItem" in html, "Language initialization must use the safe storage fallback!"
    assert "e.key.toLowerCase() === 'g'" in html, "Awakening must have its own G binding!"
    assert '999999' not in html, "Production one-key kill cheats must not ship!"
    launch_block = html[html.rfind('// Launch Game'):script_close]
    assert 'startChamber(1)' not in launch_block, "The first chamber must not begin before the player presses Start!"

    # Persistent Good / Neutral / Evil alignment progression.
    assert 'id="alignment-meter"' in html and 'id="alignment-tree-modal"' in html, "The alignment balance bar and extensive tree must be reachable!"
    assert 'id="boss-outcome-modal"' in html, "Every subdued campaign boss must end in a paused outcome decision!"
    assert "let alignmentScore = 0" in html and "alignment: { score: alignmentScore" in html, "Alignment and owned ranks must persist in the browser meta save!"
    assert "alignmentScore = Math.min(100, alignmentScore + 1)" in html, "Good decisions must move the balance exactly one point right!"
    assert "alignmentScore = Math.max(-100, alignmentScore - 1)" in html, "Evil decisions must move the balance exactly one point left!"
    assert "ALIGNMENT_SKILLS" in html and source.count("path:'good'") >= 12 and source.count("path:'neutral'") >= 12 and source.count("path:'evil'") >= 12, "All three alignment branches must be extensive!"
    assert "const KARMA_SKILL_MAX_RANK = 20" in html and "].map(skill => ({ ...skill, maxRank: KARMA_SKILL_MAX_RANK }))" in html, "Every Good, Neutral, and Evil karma skill must support 20 persistent ranks!"
    assert "aria-valuemax=\"${skill.maxRank}\"" in html and "branch === 'neutral' ?" not in source[source.index("const rankTrack ="):source.index("const rankTrack =") + 600], "All three karma paths must display their 20-rank progress track!"
    assert "isAlignmentSkillActive" in html and "Owned · Currently Dormant" in html, "Owned alignment ranks must become dormant, never be deleted, when prerequisites fail!"
    assert "LIFE_LEECH_WINDOW_MAX_HP = 0.04" in html and "LIFE_LEECH_PER_HIT_MAX_HP = 0.02" in html, "Life leech needs both burst-window and per-contact healing caps!"
    assert "GUANYIN_STRIKE_HEAL_BASE = 1" in html and "GUANYIN_STRIKE_HEAL_PER_RANK = 0.5" in html, "Guanyin on-hit healing must be one quarter of its former 4 + 2/rank value!"
    assert "effects:{lifeLeech:.0015}" in html and "effects:{damage:.01,attackSpeed:.01,lifeLeech:.0005,evilCapstone:1}" in html and "Math.min(0.025, alignmentEffects.lifeLeech || 0)" in html, "Evil alignment leech must scale across 20 ranks without bypassing its sustain cap!"
    assert "getActiveFormSkillRank('tiger_frenzy') * 0.015" in html, "White Tiger critical leech must be reduced from 6% to 1.5% per rank!"
    assert "this.isSubdued = true" in html and "Subdued, not slain" in html, "Boss defeat must stop in a nonlethal surrender state!"
    assert html.count("this.drawAlignmentAura(ctx, true)") >= 3, "Normal, karma, and authored combo bodies must finish with Wukong's foreground aura pass!"
    assert "ctx.ellipse(-7, -38" not in html, "Red eyes must be authored on each face, never painted at fixed world coordinates!"
    assert "gameState.bossOutcomeActive" in html and "isGameplayPaused" in html, "The outcome choice must own the gameplay pause!"
    assert "const SCREEN_SHAKE_SCALE = 0.18" in html and "const SCREEN_SHAKE_MAX_PX = 3" in html, "All skill and boss camera shake must be globally softened and capped at three pixels!"
    assert "Math.max(gameState.screenShake || 0, softenedAmount)" in html and "SCREEN_SHAKE_DECAY_PER_SECOND = 36" in html, "Overlapping impacts must not stack shake, and residual motion must decay quickly!"
    for chapter in (5, 12, 18, 22, 24, 25, 26, 27, 29, 32, 36, 40, 45, 50, 55, 60, 65, 67, 70, 71, 75, 77, 79, 80, 81, 84, 87, 90, 93, 94, 96, 99):
        assert f"{chapter}: outcomeStory(" in source, f"Chapter {chapter} needs an authentic nonlethal boss outcome!"
    alignment_art = Image.open("assets_webp/wukong_alignment_portraits.webp")
    assert alignment_art.mode == "RGBA" and alignment_art.getchannel("A").getextrema()[0] == 0, "Good/Neutral/Evil Wukong art must preserve transparency!"
    assert alignment_art.width >= alignment_art.height * 2, "Alignment portrait sheet must keep the three designs widely separated!"
    assert 'id="title-karma-state"' in html and "function updateTitleKarmaPresentation" in html, "The title must explain and display persistent karma progression!"
    assert "score >= 60" in html and "score >= 25" in html and "score >= 8" in html, "Good title art needs three slow progression milestones!"
    assert "score <= -60" in html and "score <= -25" in html and "score <= -8" in html, "Evil title art needs three slow progression milestones!"
    assert "background-size: auto 100%" in html and "background-position: right center" in html, "Ultrawide title art must preserve Wukong's full height and head!"
    for karma_title in (
        "title_karma_neutral", "title_karma_good_1", "title_karma_good_2", "title_karma_good_3",
        "title_karma_evil_1", "title_karma_evil_2", "title_karma_evil_3",
    ):
        assert karma_title in html, f"Missing embedded progressive title asset: {karma_title}"
    for karma_animation in (
        "wukong_good_1", "wukong_good_2", "wukong_good_3",
        "wukong_evil_1", "wukong_evil_2", "wukong_evil_3",
    ):
        assert karma_animation in html, f"Missing embedded progressive karma animation asset: {karma_animation}"
        assert (Path("assets_sources/alignment_sprites") / f"{karma_animation}_source.png").exists(), f"Missing project-bound ImageGen source: {karma_animation}"
    assert "const RUYI_COMBO_WINDOW = 1.35" in html and "this.combatInputQueue" in html, "Mixed attacks need a documented input window and attack-time buffer!"
    assert "pattern:'LLL'" in html and "Great Sage Beginner Chain" in html, "New players must retain the simple L-L-L route!"
    assert "pattern:'LLRR'" in html and "pattern:'LLLRR'" in html and "pattern:'LLRLR'" in html, "The requested mixed left/right combo routes must ship!"
    assert all(f"animRow:{row}" in html for row in range(7)), "Every Ruyi combo needs its own authored Wukong body-motion row!"
    assert "wukong_combo_moves_neutral" in html and "wukong_combo_moves_good" in html and "wukong_combo_moves_evil" in html, "Neutral, Good, and Evil finishers need matching generated animation atlases!"
    assert "const canExtend = comboDefinitions.some" in html and "combo.pattern.startsWith(candidate)" in html, "Hero-specific short finishers must extend while invalid extra clicks restart cleanly!"
    assert 'id="combo-list-modal"' in html and "function renderComboList()" in html and "e.key.toLowerCase() === 'c'" in html, "Players need a bilingual, keyboard-accessible combo list!"

    # 2. Check Enemy Active Attacks & Animated Strike FX
    assert "EnemySpearThrustFX" in html, "Enemy spear thrust FX must exist!"
    assert "EnemyClawSwipeFX" in html, "Enemy claw swipe FX must exist!"
    assert "EnemySoulStrikeFX" in html, "Enemy soul strike FX must exist!"
    assert "this.attackDuration" in html, "Enemy attack duration timer must exist!"
    assert "pendingAttack" in html and "contactAt" in html, "Player damage must be synchronized to an authored contact frame!"
    assert "pendingSpecial" in html and "resolvePendingSpecial" in html, "Special damage must land on its visible contact frame!"
    assert "pendingBossAttack" in html and "resolveBossAttack" in html, "Boss projectiles must launch on their animation contact frame!"

    # 3. Check Progressive Spawner, Specialized Archetypes & Mini-Bosses
    assert "KnockdownDustFX" in html, "Knockdown dust FX must exist!"
    assert "DeathSoulFX" in html, "Death soul dissolution FX must exist!"
    assert "isKnockedDown" in html, "Enemy knockdown state must exist!"
    assert "isDying" in html, "Enemy dying state must exist!"
    assert "tianbing_commander" in html, "Tianbing commander mini-boss must exist!"
    assert "updateChamberSpawner" in html, "Progressive wave spawner function must exist!"
    assert "special_enemies_anims" in html, "Specialized enemy animation asset must exist!"

    # 3. Check Elemental Slash Animations & Expansive Arena
    assert "ElementalSlashFX" in html, "ElementalSlashFX must exist!"
    assert "isEffectAlive" in html, "Effects without an alpha field must survive until their own lifetime expires!"
    assert "elemental_slashes" in html, "Elemental slashes sprite sheet must exist!"
    assert "GroundFissureFX" in html, "Ground fissure earth-shattering FX must exist!"
    assert "StaffPillarSlamFX" in html, "Pillar slam special attack FX must exist!"
    assert "arenaHalfW = 1160" in html, "Expansive rectangular arena boundary should exist!"

    # 5. Check Colossal Buddha & Approval Cutscene
    assert "buddha_colossal" in html, "Colossal Buddha asset should exist!"
    assert "triggerBuddhaApprovalCutscene" in html, "Buddha approval cutscene function should exist!"
    assert "大日如来神掌" in html, "Tathagata palm attack should exist!"
    assert "telegraphZone" in html, "Telegraphed dodge window for Buddha attacks should exist!"
    assert "buddha-modal" in html, "Buddha cutscene modal should exist!"

    # 6. Check Buff Erlang & Independent Xiao Tian Quan
    assert "erlang_and_dog" in html, "Erlang & Dog asset should exist!"
    assert "xiaotianquan_hound" in html, "Independent Xiao Tian Quan combat entity should exist!"
    assert "const attackReach = this.radius + target.radius + 34" in html, "Xiaotianquan must be able to attack bosses outside their collision footprint!"
    assert "this.attackTarget = target" in html and "biteTarget.takeDamage" in html, "Xiaotianquan must retain and damage its selected hostile target at bite contact!"
    assert "r = 4" in html and "Math.floor(attackProgress * 5)" in html, "Xiaotianquan must play its authored five-frame pounce/bite animation!"
    assert "hound_empowered_slam" in html and "xiaotianquan_empowered_slam" in html, "Erlang's direct command must play the authored seven-frame Xiaotianquan thunder slam!"
    assert "specialSteps * 0.28" in html and "stunDuration" in html and "slamRadius" in html, "Xiaotianquan's commanded slam must scale damage, stun, and area with special rank!"
    assert "const ERLANG_STORY_ONLY_CHAPTERS = new Set();" in html, "Erlang cutscenes must introduce combat chapters instead of creating empty rounds!"
    for enemy_type in ("fengshen_mirror_disciple", "fengshen_soul_guard", "fengshen_array_adept", "fengshen_meishan_raider"):
        assert enemy_type in html, f"Erlang's dedicated Fengshen enemy is missing: {enemy_type}"
    assert "三尖两刃枪" in html, "Erlang trident spear should exist!"

    # 7. Check God Portraits Grid Mapping
    assert "portraitCol: 0" in html, "Erlangshen/Bullking portrait column must exist!"
    assert "portraitCol: 1" in html, "Guanyin/Ironfan portrait column must exist!"
    assert "portraitCol: 4" in html, "Aoguang/Change portrait column must exist!"
    assert "portraitCol: 5" in html, "Luban portrait column must exist!"
    assert "portraitRow: 1" in html, "Second row gods must have portraitRow: 1!"

    # 8. Check Lu Ban in-game avatar
    assert "luban_avatar" in html, "Lu Ban avatar asset should exist!"
    assert "LubanAvatarNPC" in html, "Lu Ban avatar NPC class should exist!"
    assert "巧圣仙师·鲁班" in html, "Lu Ban name should exist!"

    # 8. Check 4-Directional movement & attack perspectives
    assert "direction = 'up'" in html, "Up direction should exist!"
    assert "direction = 'down'" in html, "Down direction should exist!"

    # 9. Check the single continuous authored Journey (chapters 1-100).
    assert "totalChambers: 100" in html, "The campaign must expose all 100 authored chapters as one journey!"
    assert "runStartChapter: 1" in html and "runEndChapter: 100" in html, "The unified journey boundaries must remain explicit!"
    assert "function startJourney(newGamePlus = false)" in html and "function startVolumeTwoRun()" not in html, "The title screen must launch one continuous journey without a second-volume shortcut!"
    assert "gameState.runStartChapter = 1" in html and "gameState.campaignRoute === 'fengshen' ? 38 : 100" in html and "gameState.totalChambers = gameState.runEndChapter" in html, "Wukong must traverse 1-100 while Erlang uses the authored 1-38 Fengshen route!"
    assert "LATE_CHAPTER_BEATS" in html and "STORY_ONLY_CHAPTERS" in html, "Every late chapter needs a story beat and non-combat chapters must be supported!"
    assert "LATE_DIALOGUE_SCENES" in html and "journeyVictory" in html, "The unified pilgrimage must end with a bilingual Buddhahood story scene!"
    late_beats = html[html.find("const LATE_CHAPTER_BEATS"):html.find("const CAMPAIGN_BOSSES")]
    for chapter in range(66, 101):
        assert f"{chapter}: {{ zh:" in late_beats, f"Chapter {chapter} needs a Chinese and English narrative beat!"
    assert "CAMPAIGN_BOSSES" in html and "campaign_iron_fan" in html, "The campaign boss schedule must reach Princess Iron Fan!"
    for chapter, king in [(24, "campaign_king_chiguo"), (25, "campaign_king_zengzhang"), (26, "campaign_king_guangmu"), (27, "campaign_king_duowen")]:
        assert f"{chapter}: {{ type: '{king}' }}" in html, f"Chapter {chapter} must contain its own Heavenly King boss fight!"
    assert "campaign_heavenly_kings" not in html, "The Four Heavenly Kings must not remain a combined single boss!"
    assert "CAMPAIGN_BOSS_PROFILES" in html and "behavior: 'campaign_boss'" in html, "Campaign bosses need the universal dynamic combat controller!"
    assert "campaign_ranged" in html and "campaign_aoe" in html and "campaign_mobility" in html, "Every campaign boss must cycle ranged, large-AOE, and mobility skills!"
    assert "BossSkillProjectile" in html and "BossSkillAnimatedFX" in html, "Boss ranged and large-AOE skills need authored animation playback!"
    for late_boss in ["campaign_nine_headed_beast", "campaign_yellow_brows", "campaign_sai_taisui", "campaign_golden_peng", "campaign_white_mouse", "campaign_nine_spirit", "campaign_jade_rabbit"]:
        assert late_boss in html, f"Missing late-journey boss: {late_boss}"
    assert "types: ['campaign_rhino_cold', 'campaign_rhino_heat', 'campaign_rhino_dust']" in html, "The three rhino kings must fight together as separate bosses!"
    assert "pattern: 'fan'" in html and "pattern: 'ring'" in html and "pattern: 'spiral'" in html, "Late bosses need distinct projectile patterns!"
    assert "earlyJourneyProgress" in html and "lateJourneyProgress" in html and "lateJourneyProgress * 0.025" in html, "The unified journey needs a continuous, tapered chapter-1-to-100 HP curve!"

    # 9b. Erlang's independent Fengshen campaign, combat language, and training.
    assert "const ERLANG_COMBOS" in html and all(f"pattern:'{pattern}'" in html for pattern in ("LLL", "LLR", "LRL", "LRR", "LLRR")), "Erlang needs five authored mixed-input spear/hound/Third-Eye combos!"
    assert "erlang_combo_actions" in html and "loadedImages['erlang_combo_actions']" in html, "Erlang combo animation atlas must be embedded and rendered!"
    assert "player.handleCombatInput('R');" in html and "else player.performRightClickSkill();" not in html, "Erlang right click must enter the contextual combo parser instead of always bypassing it for the hound!"
    fengshen_chapters = html[html.find("const ERLANG_FENGSHEN_CHAPTERS"):html.find("const ERLANG_CAMPAIGN_BOSSES")]
    assert fengshen_chapters.count("titleZh:") == 38, "Erlang's continuous Fengshen chronicle must contain exactly 38 bilingual chapters!"
    for boss in ("fengshen_zhang_guifang", "fengshen_wen_zhong", "fengshen_yunxiao", "fengshen_kong_xuan", "fengshen_yuan_hong"):
        assert boss in html, f"Missing Erlang Fengshen boss: {boss}"
    assert "cutscene_fengshen_act1" in html and "cutscene_fengshen_act2" in html and "speaker:'erlang'" in html, "Fengshen cutscenes must use Erlang's perspective and generated slide art!"
    erlang_skills = html[html.find("const ERLANG_SKILLS"):html.find("function getErlangSkillEffects")]
    assert erlang_skills.count("id:'") == 21 and "maxRank:20" in erlang_skills, "Erlang needs 21 persistent skills with 20 ranks each!"
    assert "erlang: { ...erlangSkillRanks }" in html and "id=\"erlang-skill-modal\"" in html, "Erlang ranks must persist in browser storage and have their own accessible tree!"
    for hook in ("eyeChains", "arrayDamage", "spearDamage", "houndDamage", "dashDamage", "manifestDuration"):
        assert hook in html, f"Erlang skill effect {hook} must be wired into gameplay!"
    for filename, expected_size in {
        "erlang_combo_actions.webp": (1680, 1200),
        "fengshen_bosses.webp": (1400, 1000),
        "cutscene_fengshen_act1_slide_1.webp": (1280, 720),
        "cutscene_fengshen_act2_slide_4.webp": (1280, 720),
    }.items():
        sheet = Image.open(Path("assets_webp") / filename)
        assert sheet.size == expected_size, f"{filename} must keep its authored grid/slide dimensions!"

    # 10. Check Real Frame-by-Frame Generated Animation Sheets
    assert "wukong_real_anims" in html, "Wukong real combat animation asset must exist!"
    assert "enemies_real_anims" in html, "Enemies real combat animation asset must exist!"
    assert "bosses_real_anims" in html, "Bosses real combat animation asset must exist!"
    assert "wukong_combat_combos" in html, "Wukong combat combos sprite sheet must exist!"
    assert "wukong_hair_clones" in html, "Wukong hair clones sprite sheet must exist!"

    # 11. Check Spell Cast Hou Zhi Hou Shun & Motion Blur Waves
    assert "HouZhiHouShunClone" in html, "Monkey clone army class must exist!"
    assert "StaffMotionWaveFX" in html, "Staff kinetic motion wave FX must exist!"
    assert "GlowingHairTrailFX" in html, "Glowing hair trail FX must exist!"

    # 13. Check Authentic Journey to the West Boss Dialogues & Speech Bubbles
    assert "BOSS_DIALOGUES" in html, "BOSS_DIALOGUES data must exist!"
    assert "openBossDialogue" in html, "openBossDialogue function must exist!"
    assert "SpeechBubbleFX" in html, "SpeechBubbleFX class must exist!"
    assert "boss-dialogue-modal" in html, "boss-dialogue-modal UI container must exist!"
    assert "五行山下受五百" in html, "Buddha authentic Five Finger Mountain dialogue must exist!"
    assert "CAMPAIGN_DIALOGUES" in html and "唐三藏" in html, "Campaign story dialogue and Tang Sanzang must exist!"
    assert "dialogueActive" in html and "beginDialoguePause" in html and "endDialoguePause" in html, "Story dialogue must own a fail-safe simulation pause lock!"
    assert "return gameState.isPaused || gameState.dialogueActive || gameState.rewardSelectionActive" in html, "Dialogue and reward selection must independently freeze the simulation even if another overlay changes the generic pause flag!"
    assert "beginRewardSelectionPause()" in html and "endRewardSelectionPause()" in html, "Boon, Peach, and shop choices need an explicit pause lock lifecycle!"
    assert "const shopVisitPurchases = new Set()" in html and "openShopModal(true)" in html, "Each Treasure Pavilion event must start with a fresh per-visit purchase ledger!"
    assert "id: 'life_elixir', oncePerVisit: true" in html and "shopVisitPurchases.add(it.id)" in html, "The life elixir must be limited to one purchase per pavilion visit!"
    assert "Purchased This Visit" in html and "card.disabled = purchasedThisVisit" in html, "The purchased life elixir must visibly disable for the rest of that visit!"
    assert "deferredDialogueChapter" in html and "openOrDeferBossDialogue(index)" in html, "The next story dialogue must wait for the active reward modal to close!"
    assert "player.invulnTimer = Math.max(player.invulnTimer, 0.9)" in html, "Dialogue exit must include protection from frozen melee/projectiles!"
    assert 'id="dialogue-cinematic-image"' in html and 'class="modal-box boss-dialogue-box"' in html, "Story dialogue must use the large rectangular cinematic image player!"
    assert "const CUTSCENE_ARCS" in html and "function buildCinematicSlides" in html, "Every dialogue chapter must map to authored story art and cinematic slides!"
    assert "while (slides.length < 3)" in html and "currentCinematicSlides.length" in html, "Every story cutscene must contain at least three slides!"
    assert "nextBuddhaCutsceneStep()" in html and "buddhaCutsceneSlides = [" in html, "The special Five-Finger Mountain sequence must also be a multi-slide cinematic!"
    cutscene_names = [
        "cutscene_flower_fruit", "cutscene_kunlun", "cutscene_dragon_palace",
        "cutscene_havoc_heaven", "cutscene_five_finger", "cutscene_pilgrims",
        "cutscene_bone_spider", "cutscene_flaming_mountain", "cutscene_mid_trials",
        "cutscene_lion_camel", "cutscene_late_trials", "cutscene_vulture_peak",
    ]
    for cutscene_name in cutscene_names:
        assert cutscene_name in html, f"Missing embedded cinematic story art: {cutscene_name}"
        cutscene_path = Path("assets_webp") / f"{cutscene_name}.webp"
        assert cutscene_path.exists(), f"Missing packaged cutscene file: {cutscene_path}"
        with Image.open(cutscene_path) as cutscene_image:
            assert cutscene_image.size == (1280, 720), f"{cutscene_name} must retain the 16:9 cinematic contract!"
        slide_hashes = set()
        for slide in range(1, 5):
            slide_name = f"{cutscene_name}_slide_{slide}"
            assert slide_name in html, f"Missing embedded generated story slide: {slide_name}"
            slide_path = Path("assets_webp") / f"{slide_name}.webp"
            assert slide_path.exists(), f"Missing packaged generated story slide: {slide_path}"
            with Image.open(slide_path) as slide_image:
                assert slide_image.size == (1280, 720), f"{slide_name} must be a 16:9 cinematic image!"
                slide_hashes.add(hashlib.sha256(slide_image.convert("RGB").tobytes()).hexdigest())
        assert len(slide_hashes) == 4, f"{cutscene_name} must use four different generated pictures!"
    assert "const slideAssetKey = `${arc.asset}_slide_${visualSlide}`" in html, "Next must advance to a separately generated story image!"
    assert "Math.min(currentDialogueStep + 1, 4)" in html, "Dialogue slide number must select its corresponding story image!"
    dialogue_open_block = html[html.find("function openBossDialogue"):html.find("function renderBossDialogueStep")]
    assert "beginDialoguePause();" in dialogue_open_block, "Opening any campaign/boss conversation must acquire the dialogue lock!"
    game_loop_block = html[html.find("function gameLoop"):html.find("// Launch Game")]
    assert "if (!isGameplayPaused())" in game_loop_block, "Dialogue must freeze the entire gameplay simulation loop!"

    # Complete bilingual UI and story localization persists independently of a run.
    assert 'id="lang-zh-btn"' in html and 'id="lang-en-btn"' in html, "The title screen must offer Chinese and English before play!"
    assert "havocInHeavenLanguageV1" in html and "safeStorageSetItem(LANGUAGE_SAVE_KEY" in html, "Language choice must persist whenever browser storage is available!"
    assert 'html[lang="en"]' in html and "--font-en-ui: 'Segoe UI'" in html, "English UI must use a readable non-cursive system font!"
    assert "function getCanvasFont" in html and "gameState.language === 'en'" in html, "Canvas labels must switch away from the Chinese brush font in English mode!"
    assert "CAMPAIGN_DIALOGUES_EN" in html and "Tang Sanzang" in html and "Princess Iron Fan" in html, "All campaign dialogue must have an English path!"
    assert "GOD_EN" in html and "SKILL_EN_NAMES" in html and "refreshLocalizedSkillTree" in html, "God boons and the full interactive skill tree must localize to English!"
    assert "Queen Mother’s Celestial Peach" in html and "Dragon-Palace Treasure" in html, "Dynamic Peach and shop interfaces must be localized!"
    assert "Taste my Ruyi Staff!" in html and "Xiaotianquan answers the call!" in html, "Battle barks and dynamic boon feedback must localize to English!"
    assert "Journey to the West action arena" in html and "Selectable 72 Transformations skill nodes" in html, "English accessibility labels must not retain mixed Chinese fragments!"
    assert "'$1 / $2 Chapters'" in html, "Dynamic defeat progress must translate the trailing Chinese chapter suffix!"

    # Boss sprite semantics and damage timing must match their authored cells.
    assert "this.hurtTimer = 0" in html and "this.isKnockedDown || this.hurtTimer > 0" in html, "Campaign bosses must display their authored hurt frame!"
    assert "this.campaignAction === 'ranged') c = progress < 0.48 ? 2 : 3" in html, "Ranged attacks must not incorrectly finish on the AOE frame!"
    assert "else if (isMoving) c = 1" in html, "Boss locomotion must hold the mobility pose instead of snapping to front idle!"
    assert "visibleHitRadius = attack.profile.aoeRadius * 0.72" in html, "Boss AOE damage must stay inside the visible generated ring!"
    assert "false, 4, 6" in html, "Projectile impacts must begin on impact frames rather than replaying charge frames!"

    # 14. Check 5x Fa Shu Mana (Qi) Cost
    assert "this.qi -= 75" in html, "Fa Shu mana cost must be 75 (5x increased)!"

    # 15. Check Hades-Style Divine Staff Slashes & Colossal Circular Nova AOE
    assert "ruyi_staff_slashes" in html, "Ruyi staff divine slashes asset must exist!"
    assert "hades_magic_circles" in html, "Hades magic circles and circular nova asset must exist!"
    assert "HadesDivineStaffSlashFX" in html, "Hades divine staff slash FX class must exist!"
    assert "ColossalStaffNovaFX" in html, "Colossal 360 staff nova FX class must exist!"
    assert "GroundSmashPillarEruptionFX" in html, "Ground smash pillar eruption FX class must exist!"
    assert "HadesMagicCircleAOEFX" in html, "Hades magic circle AOE FX class must exist!"
    assert "HadesHitSparkFX" in html, "Hades hit spark FX class must exist!"

    # 16. Check 72 Transformations Complete Skill Tree & [R] Transformation System
    assert "SKILL_TREE_72" in html, "SKILL_TREE_72 array must exist!"
    assert "wukong_72_forms" in html, "wukong_72_forms asset must exist!"
    assert "wukong_72_form_attacks" in html, "Every transformation must have a dedicated attack sheet!"
    assert "FORM_COMBAT_PROFILES" in html and "procFormAttackOnHit" in html, "Forms must own distinct combat playstyles!"
    assert "triggerTransformation" in html, "triggerTransformation method must exist!"
    assert "this.transformDuration -= dt" in html, "Transformation duration must tick down!"
    assert "this.transformCooldown = Math.max(0" in html, "Transformation cooldown must tick down!"
    assert "form_dragon" in html, "Dragon transformation branch must exist!"
    assert "form_tiger" in html, "White tiger transformation branch must exist!"
    assert "form_roc" in html, "Golden roc transformation branch must exist!"
    assert "form_ape" in html, "Colossal ape transformation branch must exist!"
    assert "form_tortoise" in html, "Black tortoise transformation branch must exist!"
    assert "renderSkillTreeCanvas" in html, "Interactive canvas skill tree renderer must exist!"
    assert "getTreePointFromClient" in html and "canvasEl.width / Math.max(1, rect.width)" in html, "Skill-tree hit testing must account for CSS canvas scaling!"
    assert 'id="tree-hit-layer"' in html and "renderTreeHitTargets" in html, "Visible canvas nodes must have reliable DOM hit targets!"
    assert "investPermanentPassive" in html and "每级全部伤害 +1%" in html, "Permanent passive skill investment must exist!"
    assert "equipActiveFormFromInspector" in html, "Form equip logic must exist!"
    assert "resetAllSkillTreePoints" in html, "Points reset logic must exist!"

    # 17. Check the generated ranged Ruyi throw, return, and catch special.
    assert "wukong_ruyi_throw" in html, "Wukong throw/catch animation asset must exist!"
    assert "ruyi_boomerang_spin" in html, "Spinning Ruyi staff animation asset must exist!"
    assert "RuyiBoomerangProjectile" in html, "The special must be a returning ranged projectile!"
    assert "outboundHits" in html and "returnHits" in html, "The staff must damage independently on the outward and return paths!"
    assert "RUYI_THROW_SPIN_REVS_PER_SECOND = 6" in html, "The thrown staff must complete several readable revolutions per flight!"
    assert "this.angle + this.spinRotation" in html, "The flying staff must use continuous time-based rotation without snapping on return!"
    assert "ctx.fillRect(-cell * scale / 2, -cell * scale / 2, cell * scale, cell * scale);" not in source, "Thrown Ruyi alignment tint must not paint a rotated square over the arena!"
    assert "fxList.push(new RuyiStaffSpecialSlamFX" not in html, "The legacy ground-slam special must no longer be invoked!"

    # 18. Check 11 Gods & Elemental Boon Attack Slashes & Scaled Slashes
    assert "gods_boon_slashes" in html, "gods_boon_slashes asset must exist!"
    assert "ironfan_strike" in html, "Princess iron fan wind slash boon must exist!"

    # Enemies with different sprite scales must not visually merge into one
    # contaminated-looking animation frame while converging on the player.
    assert "function getEnemyCrowdRadius" in html, "Visual enemy footprint calculation must exist!"
    assert "function resolveEnemyCrowding" in html, "Enemy crowd separation solver must exist!"
    assert "ENEMY_CROWD_GRID_SIZE = 192" in html and "enemyCrowdGrid = new Map()" in html, "Tripled waves need spatially partitioned crowd checks instead of an all-pairs solver!"
    assert "58 * enemy.campaignScale" in html, "Campaign boss spacing must account for rendered sprite scale!"
    assert "enemies.forEach(e => e.update(dt));\n          resolveEnemyCrowding();" in html, "Enemy separation must run after chase movement every frame!"
    assert "MAX_CANVAS_BACKING_PIXELS = 4000000" in html and "Math.min(1.5, nativeScale, budgetScale)" in html, "High-DPI and ultrawide canvases must stay within the movement-performance budget!"
    assert "cameraOffsetX = Math.round" in html and "ctx.imageSmoothingEnabled = true" in html, "The scrolling floor needs backing-pixel camera alignment and smooth sampling!"

    # No encounter may materialize on top of Wukong at room start or mid-wave.
    assert "SAFE_ENEMY_SPAWN_DISTANCE = 640" in html and "SAFE_BOSS_SPAWN_DISTANCE = 780" in html, "Enemy and boss spawn safety radii must exist!"
    assert "function getSafeEnemySpawnPosition" in html, "Every hostile spawn must be projected outside Wukong's safety ring!"
    assert "const safeSpawn = getSafeEnemySpawnPosition" in html, "Random initial and wave enemies must use the shared safe-spawn resolver!"
    assert "const bossSpawn = getSafeEnemySpawnPosition" in html, "Fixed campaign boss coordinates must also respect spawn safety!"
    assert "index === 1 ? 10.5 : 2.25" in html and "player.invulnTimer = Math.max(player.invulnTimer, 3.5)" in html, "Room and boss introductions need entry protection!"

    # Generated sheet geometry and chroma-key cleanliness.
    expected_sheets = {
        "hero.webp": (896, 896),
        "wukong_72_forms.webp": (1400, 1000),
        "wukong_72_form_attacks.webp": (1400, 1000),
        "wukong_ruyi_throw.webp": (1540, 220),
        "ruyi_boomerang_spin.webp": (1540, 220),
        "xiaotianquan_attack.webp": (1100, 220),
        "xiaotianquan_empowered_slam.webp": (1680, 240),
        "ruyi_impact_burst.webp": (1024, 512),
        "title_key_art.webp": (1672, 941),
        "title_karma_neutral.webp": (1672, 941),
        "title_karma_good_1.webp": (1672, 941),
        "title_karma_good_2.webp": (1672, 941),
        "title_karma_good_3.webp": (1672, 941),
        "title_karma_evil_1.webp": (1672, 941),
        "title_karma_evil_2.webp": (1672, 941),
        "title_karma_evil_3.webp": (1672, 941),
        "wukong_good_1.webp": (1440, 720),
        "wukong_good_2.webp": (1440, 720),
        "wukong_good_3.webp": (1440, 720),
        "wukong_evil_1.webp": (1440, 720),
        "wukong_evil_2.webp": (1440, 720),
        "wukong_evil_3.webp": (1440, 720),
        "campaign_biomes.webp": (1536, 1536),
        "campaign_pilgrimage_biomes.webp": (1536, 1536),
        "campaign_final_biomes.webp": (1536, 1536),
        "campaign_characters_act1.webp": (1400, 1000),
        "campaign_characters_act2.webp": (1400, 1000),
        "campaign_characters_act3.webp": (1400, 1400),
        "campaign_characters_act4.webp": (1400, 1200),
        "campaign_characters_act5.webp": (1400, 1200),
        "campaign_characters_act6.webp": (1400, 1400),
        "four_heavenly_kings.webp": (1400, 800),
        "boss_skill_fx.webp": (1792, 768),
        "ruyi_melee_combo_fx.webp": (1792, 768),
        "wukong_ruyi_contact_attacks.webp": (3072, 1536),
        "ruyi_contact_weapon_paths.webp": (3072, 1536),
        "evil_ruyi_combo_fx.webp": (1792, 768),
        "wukong_combo_moves_neutral.webp": (1792, 1792),
        "wukong_combo_moves_good.webp": (1792, 1792),
        "wukong_combo_moves_evil.webp": (1792, 1792),
        "fengshen_enemies.webp": (1400, 800),
    }
    for filename, expected_size in expected_sheets.items():
        path = Path("assets_webp") / filename
        assert path.exists(), f"Missing generated/cleaned art asset: {filename}"
        image = Image.open(path).convert("RGBA")
        assert image.size == expected_size, f"{filename} grid changed: {image.size} != {expected_size}"
        pixels = list(image.getdata())
        visible = [(r, g, b) for r, g, b, a in pixels if a > 20]
        magenta = sum(1 for r, g, b in visible if r > 220 and b > 180 and g < 90)
        magenta_limit = 0.08 if filename.startswith("campaign_characters") else 0.001
        assert magenta / max(1, len(visible)) < magenta_limit, f"{filename} contains residual magenta key pixels"

    # Every runtime animation atlas must keep a transparent safety gutter in
    # every visible cell. This prevents adjacent pictures from entering a frame.
    safe_animation_sheets = {
        "hero.webp": (7, 7, 128, 128, 28),
        "monsters_beasts.webp": (6, 10, 128, 128, 28),
        "erlang_and_dog.webp": (5, 6, 160, 160, 38),
        "erlang_player_actions.webp": (5, 7, 240, 240, 56),
        "xiaotianquan_attack.webp": (1, 5, 220, 220, 52),
        "xiaotianquan_empowered_slam.webp": (1, 7, 240, 240, 56),
        "buddha_colossal.webp": (4, 7, 256, 256, 60),
        "infinite_bosses_a.webp": (6, 9, 160, 160, 38),
        "luban_avatar.webp": (4, 8, 128, 128, 28),
        "wukong_real_anims.webp": (5, 7, 160, 160, 38),
        "enemies_real_anims.webp": (6, 7, 160, 160, 38),
        "bosses_real_anims.webp": (4, 8, 160, 160, 38),
        "elemental_slashes.webp": (5, 9, 160, 160, 38),
        "special_enemies_anims.webp": (6, 8, 160, 160, 38),
        "wukong_combat_combos.webp": (4, 7, 220, 220, 52),
        "wukong_ruyi_throw.webp": (1, 7, 220, 220, 52),
        "ruyi_boomerang_spin.webp": (1, 7, 220, 220, 52),
        "wukong_hair_clones.webp": (4, 6, 200, 200, 48),
        "ruyi_staff_slashes.webp": (4, 6, 200, 200, 48),
        "hades_magic_circles.webp": (4, 6, 200, 200, 48),
        "wukong_72_forms.webp": (5, 7, 200, 200, 48),
        "wukong_72_form_attacks.webp": (5, 7, 200, 200, 48),
        "ruyi_special_slam.webp": (4, 7, 200, 200, 48),
        "gods_boon_slashes.webp": (5, 8, 160, 160, 38),
        "ruyi_impact_burst.webp": (2, 4, 256, 256, 60),
        "campaign_characters_act1.webp": (5, 7, 200, 200, 48),
        "campaign_characters_act2.webp": (5, 7, 200, 200, 48),
        "campaign_characters_act3.webp": (7, 7, 200, 200, 48),
        "campaign_characters_act4.webp": (6, 7, 200, 200, 48),
        "campaign_characters_act5.webp": (6, 7, 200, 200, 48),
        "campaign_characters_act6.webp": (7, 7, 200, 200, 48),
        "four_heavenly_kings.webp": (4, 7, 200, 200, 48),
        "fengshen_enemies.webp": (4, 7, 200, 200, 48),
        "boss_skill_fx.webp": (3, 7, 256, 256, 60),
        "ruyi_melee_combo_fx.webp": (3, 7, 256, 256, 60),
        "wukong_ruyi_contact_attacks.webp": (4, 8, 384, 384, 40),
        "ruyi_contact_weapon_paths.webp": (4, 8, 384, 384, 40),
        "wukong_ruyi_temporal_neutral.webp": (32, 8, 192, 192, 32),
        "evil_ruyi_combo_fx.webp": (3, 7, 256, 256, 60),
        "wukong_combo_moves_neutral.webp": (7, 7, 256, 256, 48),
        "wukong_combo_moves_good.webp": (7, 7, 256, 256, 48),
        "wukong_combo_moves_evil.webp": (7, 7, 256, 256, 48),
        "wukong_good_1.webp": (3, 6, 240, 240, 56),
        "wukong_good_2.webp": (3, 6, 240, 240, 56),
        "wukong_good_3.webp": (3, 6, 240, 240, 56),
        "wukong_evil_1.webp": (3, 6, 240, 240, 56),
        "wukong_evil_2.webp": (3, 6, 240, 240, 56),
        "wukong_evil_3.webp": (3, 6, 240, 240, 56),
    }
    for filename, (rows, cols, cell_w, cell_h, gutter) in safe_animation_sheets.items():
        sheet = Image.open(Path("assets_webp") / filename).convert("RGBA")
        assert sheet.size == (cols * cell_w, rows * cell_h), f"{filename} no longer matches its renderer grid"
        for row in range(rows):
            for col in range(cols):
                alpha = sheet.crop((col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)).getchannel("A")
                solid = alpha.point(lambda value: 255 if value > 20 else 0)
                bbox = solid.getbbox()
                if bbox is None:
                    continue
                actual_gutter = min(bbox[0], bbox[1], cell_w - bbox[2], cell_h - bbox[3])
                assert actual_gutter >= gutter - 1, f"{filename} r{row}c{col} has only {actual_gutter}px gutter; expected {gutter}px"

    assert (Path("assets_webp") / "ape_form_attack_strip_v2.png").exists(), "Regenerated seven-pose ape attack source must remain project-bound"
    assert (Path("assets_webp") / "ruyi_boomerang_special_v1.png").exists(), "Generated Ruyi throw/return source must remain project-bound"
    assert (Path("assets_webp") / "xiaotianquan_attack_strip_v1.png").exists(), "Generated Xiaotianquan pounce/bite source must remain project-bound"
    assert (Path("assets_sources/erlang_fengshen") / "xiaotianquan_empowered_slam_v1_source.png").exists(), "Generated Xiaotianquan empowered-slam source must remain project-bound"
    for fengshen_enemy_source in (
        "fengshen_mirror_disciple_v1_source.png", "fengshen_soul_guard_v1_source.png",
        "fengshen_array_adept_v1_source.png", "fengshen_meishan_raider_v1_source.png",
    ):
        assert (Path("assets_sources/erlang_fengshen") / fengshen_enemy_source).exists(), f"Missing project-bound Fengshen enemy source: {fengshen_enemy_source}"
    assert (Path("assets_webp") / "four_heavenly_kings_v2.png").exists(), "Four distinct Heavenly Kings source atlas must remain project-bound"
    assert (Path("assets_webp") / "boss_skill_fx_v1.png").exists(), "Boss projectile/AOE/mobility source atlas must remain project-bound"
    assert (Path("assets_webp") / "ruyi_melee_combo_fx_source.png").exists(), "Generated left-click Ruyi combo source must remain project-bound"
    contact_source_dir = Path("assets_sources") / "ruyi_contact_attacks"
    assert len(list(contact_source_dir.glob("ruyi_contact_*_v1_source.png"))) == 4, "Four generated Wukong anticipation/contact/recovery strips must remain project-bound"
    assert len(list(contact_source_dir.glob("ruyi_weapon_*_v1_source.png"))) == 4, "Four generated rotatable Ruyi path strips must remain project-bound"
    temporal_source_dir = Path("assets_sources") / "ruyi_contact_temporal"
    expected_temporal_sources = {
        f"{move}_{direction}_v1_source.png"
        for move in ("arc", "thrust", "slam", "spin")
        for direction in ("e", "ne", "n", "nw", "w", "sw", "s", "se")
    }
    assert {path.name for path in temporal_source_dir.glob("*_v1_source.png")} == expected_temporal_sources, "All 32 original ImageGen temporal/directional strips must remain project-bound with stable names"
    grip_manifest_path = temporal_source_dir / "wukong_ruyi_grip_anchors_v1.json"
    grip_manifest = json.loads(grip_manifest_path.read_text(encoding="utf-8"))
    assert grip_manifest["move_order"] == ["arc", "thrust", "slam", "spin"], "Grip manifest move order must match atlas row order"
    assert grip_manifest["direction_order"] == ["e", "ne", "n", "nw", "w", "sw", "s", "se"], "Grip manifest direction order must match atlas row order"
    measured_anchors = grip_manifest["anchors"]
    assert sum(len(frames) for move in measured_anchors.values() for frames in move) == 256, "Every generated body frame needs its own measured two-hand grip"
    assert all(0 <= coordinate < 192 for move in measured_anchors.values() for direction in move for anchor in direction for coordinate in anchor), "Measured grip anchors must remain inside their 192px source cells"
    for karma_path in ("neutral", "good", "evil"):
        temporal_atlas = Image.open(Path("assets_webp") / f"wukong_ruyi_temporal_{karma_path}.webp").convert("RGBA")
        assert temporal_atlas.size == (1536, 6144), f"{karma_path} temporal Wukong atlas must remain 4 moves x 8 directions x 8 frames"
    assert (Path("assets_webp") / "wukong_ruyi_temporal_neutral.webp").read_bytes() != (Path("assets_webp") / "wukong_ruyi_temporal_good.webp").read_bytes(), "Good Wukong temporal attacks need a distinct bitmap palette"
    assert (Path("assets_webp") / "wukong_ruyi_temporal_neutral.webp").read_bytes() != (Path("assets_webp") / "wukong_ruyi_temporal_evil.webp").read_bytes(), "Evil Wukong temporal attacks need a distinct bitmap palette"
    qa_sheet = Image.open(Path("assets_webp") / "ruyi_contact_all_frames_qa.jpg")
    assert qa_sheet.size == (1536, 1536), "All 64 Ruyi body/path frames need an explicit checker/dark composite QA sheet"
    temporal_qa = Image.open(Path("assets_webp") / "wukong_ruyi_temporal_contact_qa.jpg")
    assert temporal_qa.size == (1536, 768), "Temporal Wukong needs a four-move/eight-direction contact-pose QA sheet"
    for move in ("arc", "thrust", "slam", "spin"):
        combined_qa = Image.open(Path("assets_webp") / f"wukong_ruyi_combined_anchor_qa_{move}.jpg")
        assert combined_qa.size == (3072, 3072), f"{move} needs an all-64-frame body+weapon+grip-marker QA sheet"
    for contact_atlas in ("wukong_ruyi_contact_attacks.webp", "ruyi_contact_weapon_paths.webp"):
        contact_sheet = Image.open(Path("assets_webp") / contact_atlas).convert("RGBA")
        for row in range(4):
            for col in range(8):
                contact_cell = contact_sheet.crop((col * 384, row * 384, (col + 1) * 384, (row + 1) * 384))
                assert max_wide_alpha_row_streak(contact_cell) <= 18, f"{contact_atlas} r{row}c{col} contains a large rectangular alpha band"
    for evil_fx_source in ("evil_ruyi_arc_strip_v1.png", "evil_ruyi_ring_strip_v1.png", "evil_ruyi_slam_strip_v1.png"):
        assert (Path("assets_sources/combat_fx") / evil_fx_source).exists(), f"Missing project-bound generated Evil Ruyi source: {evil_fx_source}"
    for combo_source in ("wukong_combo_neutral_source.png", "wukong_combo_good_source.png", "wukong_combo_evil_source.png"):
        assert (Path("assets_sources/combo_moves") / combo_source).exists(), f"Missing project-bound generated combo body source: {combo_source}"
    assert (Path("assets_webp") / "campaign_final_biomes_v1.png").exists(), "Generated late-pilgrimage biome source must remain project-bound"
    assert (Path("assets_webp") / "campaign_characters_act4_v1.png").exists(), "Generated late-journey act-4 source must remain project-bound"
    assert (Path("assets_webp") / "campaign_characters_act5_v1.png").exists(), "Generated late-journey act-5 source must remain project-bound"
    assert (Path("assets_webp") / "campaign_characters_act6_v1.png").exists(), "Generated late-journey act-6 source must remain project-bound"
    hound_attack_sheet = Image.open(Path("assets_webp") / "xiaotianquan_attack.webp").convert("RGBA")
    for col in range(5):
        frame = hound_attack_sheet.crop((col * 220, 0, (col + 1) * 220, 220))
        visible_pixels = sum(1 for value in frame.getchannel("A").getdata() if value > 20)
        assert visible_pixels > 2500, f"Xiaotianquan attack frame c{col} is incomplete or blank"
    hound_slam_sheet = Image.open(Path("assets_webp") / "xiaotianquan_empowered_slam.webp").convert("RGBA")
    for col in range(7):
        frame = hound_slam_sheet.crop((col * 240, 0, (col + 1) * 240, 240))
        visible_pixels = sum(1 for value in frame.getchannel("A").getdata() if value > 20)
        assert visible_pixels > 450, f"Xiaotianquan empowered-slam frame c{col} is incomplete or blank"
    fengshen_enemy_sheet = Image.open(Path("assets_webp") / "fengshen_enemies.webp").convert("RGBA")
    for row in range(4):
        for col in range(7):
            frame = fengshen_enemy_sheet.crop((col * 200, row * 200, (col + 1) * 200, (row + 1) * 200))
            visible_pixels = sum(1 for value in frame.getchannel("A").getdata() if value > 20)
            assert visible_pixels > 600, f"Fengshen enemy frame r{row}c{col} is incomplete or blank"
    hero_sheet = Image.open(Path("assets_webp") / "hero.webp").convert("RGBA")
    for row in range(7):
        for col in range(7):
            frame = hero_sheet.crop((col * 128, row * 128, (col + 1) * 128, (row + 1) * 128))
            visible_pixels = sum(1 for value in frame.getchannel("A").getdata() if value > 20)
            assert visible_pixels > 450, f"Hero frame r{row}c{col} is blank or only a leftover source fragment"

    # The former r4c1 cell contained two complete Bagua golems.  A second
    # near-equal component is character bleed, not a weapon or spell accent.
    monster_sheet = Image.open(Path("assets_webp") / "monsters_beasts.webp").convert("RGBA")
    golem_walk = monster_sheet.crop((128, 4 * 128, 2 * 128, 5 * 128))
    golem_components = connected_alpha_areas(golem_walk)
    assert golem_components and (len(golem_components) == 1 or golem_components[1] < golem_components[0] * 0.35), "Bagua golem walk cell contains a second full character"

    form_attacks = Image.open(Path("assets_webp") / "wukong_72_form_attacks.webp").convert("RGBA")
    for row in range(5):
        for col in range(7):
            cell = form_attacks.crop((col * 200, row * 200, (col + 1) * 200, (row + 1) * 200))
            visible_pixels = sum(1 for alpha in cell.getchannel("A").getdata() if alpha > 20)
            assert visible_pixels > 1200, f"Transformation attack cell r{row}c{col} is blank or unusably sparse"

    # Dragon frames are generated with overlapping source bounding boxes. The
    # packer must isolate silhouettes before placing them in safe padded cells.
    for filename in ["wukong_72_forms.webp", "wukong_72_form_attacks.webp"]:
        dragon_sheet = Image.open(Path("assets_webp") / filename).convert("RGBA")
        for col in range(7):
            cell = dragon_sheet.crop((col * 200, 0, (col + 1) * 200, 200))
            alpha = cell.getchannel("A")
            solid = alpha.point(lambda value: 255 if value > 20 else 0)
            bbox = solid.getbbox()
            assert bbox is not None, f"Dragon frame {filename} c{col} is blank"
            assert bbox[0] >= 4 and bbox[1] >= 4 and bbox[2] <= 196 and bbox[3] <= 196, f"Dragon frame {filename} c{col} touches/crosses its cell edge: {bbox}"
            edge_alpha = sum(alpha.crop((0, 0, 200, 1)).getdata()) + sum(alpha.crop((0, 199, 200, 200)).getdata()) + sum(alpha.crop((0, 0, 1, 200)).getdata()) + sum(alpha.crop((199, 0, 200, 200)).getdata())
            assert edge_alpha == 0, f"Dragon frame {filename} c{col} bleeds into a neighboring frame"
    package_source = Path("package_all_clean_sheets.py").read_text(encoding="utf-8")
    assert "extract_ordered_alpha_components" in package_source and "complete silhouettes" in package_source, "Transformation build must isolate overlapping source silhouettes before cropping"
    assert "normalize_all_animation_atlases" in package_source and "replace_atlas_row_from_generated_strip" in package_source, "All animated atlases must be safely repacked and the ape attack row regenerated on every build"
    assert "repack_known_source_grid" in package_source and "is_not_second_actor" in package_source, "Known grids must preserve logical frames while rejecting a second actor"
    assert "repair_campaign_sparse_body_frames" in package_source and "repair_campaign_defeat_identity_frames" in package_source, "Campaign fragment and wrong-identity repairs must be reproducible"

    campaign_rows = {
        "campaign_characters_act1.webp": 5,
        "campaign_characters_act2.webp": 5,
        "campaign_characters_act3.webp": 7,
        "campaign_characters_act4.webp": 6,
        "campaign_characters_act5.webp": 6,
        "campaign_characters_act6.webp": 7,
    }
    for filename, rows in campaign_rows.items():
        sheet = Image.open(Path("assets_webp") / filename).convert("RGBA")
        visible_total = 0
        visible_magenta = 0
        for row in range(rows):
            for col in range(7):
                cell = sheet.crop((col * 200, row * 200, (col + 1) * 200, (row + 1) * 200))
                pixels = list(cell.getdata())
                visible = [(r, g, b) for r, g, b, a in pixels if a > 24]
                assert len(visible) > 1200, f"Campaign state cell {filename} r{row}c{col} is blank"
                visible_total += len(visible)
                visible_magenta += sum(1 for r, g, b in visible if r > 225 and b > 215 and g < 35)
        assert visible_magenta / max(1, visible_total) < 0.01, f"{filename} retains a visible magenta matte"

    # Persistence and honest full-tree progression.
    assert "havocInHeavenMetaV3" in html and "pagehide" in html, "Versioned meta-progression must persist locally!"
    assert "passiveSkillRanks" in html and "skills: { treeRanks:" in html, "Permanent passive ranks must be included in the browser save!"
    assert "const masteryRanks = 0" in source and "Transformation-tree ranks are techniques, not generic account stats" in source, "Transformation ranks must not leak generic permanent stats into normal Wukong!"
    skill_block = source[source.index("const SKILL_TREE_72"):source.index("const FORM_SKILL_RUNTIME_GROUPS")]
    transformation_skill_ids = [skill_id for skill_id in re.findall(r"id: '([^']+)'", skill_block) if skill_id != "root"]
    runtime_group_block = source[source.index("const FORM_SKILL_RUNTIME_GROUPS"):source.index("const FORM_SKILL_RUNTIME_CONTRACTS")]
    contracted_form_ids = re.findall(r"'((?:form|dragon|tiger|roc|ape|tort)_[a-z0-9_]+)'", runtime_group_block)
    assert len(transformation_skill_ids) == 71 and set(transformation_skill_ids) == set(contracted_form_ids), "All 71 form/branch nodes need an exclusive runtime trigger contract!"
    assert "getActiveFormSkillRank(id)" in source and "if (!this.isTransformed" in source, "Every transformation technique must go dormant outside its matching form!"
    assert "performTransformationSpell" in source and "TransformationSpellFX" in source, "Each form needs a real E spell and animated elemental effect!"
    assert "class FormSkillRuneFX" in source and "class FormPulseDamageFX" in source and "class FormFeatherProjectile" in source, "Form skill procs need visible runes, multi-hit pulses, and authored projectile motion!"
    assert "Abyss Dive Storm" in source and "Mountain-Shaking Roar" in source and "Celestial Gale Cyclone" in source and "Nine-Springs Abyss" in source, "The HUD must name each transformed E spell instead of showing the generic clone spell!"
    assert "Every rank grants permanent mastery" not in source and "General mastery: each rank" not in source, "The skill inspector must not advertise the removed generic mastery fallback!"
    assert "Ruyi Jingu Bang's golden signature remains" in html, "Golden base attack animation must remain under god boon effects!"
    assert "Math.min(160, this.radius * 0.62)" in html, "Oversized nova visuals must be capped independently of gameplay radius!"

    # Normal-combat redesign, denser encounters, and explicit boss tuning.
    assert "loadedImages['wukong_ruyi_contact_attacks']" in html and "loadedImages['ruyi_contact_weapon_paths']" in html, "Left-click attacks must use generated body-contact and exact staff-path atlases!"
    assert "loadedImages['evil_ruyi_combo_fx']" in html and "usesAuthoredEvilStrike" in html, "Evil Wukong strikes must use generated frame art instead of procedural slash shapes!"
    assert "if (palette.path === 'evil') return" in html, "The repaired Evil avatar must not be covered by the old procedural purple rings!"
    assert "actionRow = this.currentCombo === 1 ? 4 : 3" in html, "Normal attacks must retain the canonical ornate Wukong body sheet!"
    assert "useCanonicalEnemyAtlas" in html and "!useCanonicalEnemyAtlas" in html, "Normal enemies must never swap to a mismatched legacy body sheet!"
    assert "sourceFootY = isBossSheet ? (cellH - 38) : (cellH - 28)" in html, "Repacked enemies and bosses must use their new bottom pivots!"
    assert "optional legacy Erlang sheet" in html and "40 - (cellH - 38) * scale + hover" in html, "Legacy Erlang and Xiaotianquan must keep complete bodies on the shared ground pivot!"
    assert "NORMAL_ENEMY_WAVE_MULTIPLIER = 3" in html, "Normal chamber enemy count multiplier must be exactly three!"
    assert "baseQuota * NORMAL_ENEMY_WAVE_MULTIPLIER" in html and "3 * NORMAL_ENEMY_WAVE_MULTIPLIER" in html, "Wave quota and simultaneous spawn batch must both be tripled!"
    assert "BOSS_STRENGTH_MULTIPLIER = 3" in html, "Boss strength multiplier must be exactly three!"
    assert "def.maxHp * hpScale * this.strengthMultiplier" in html, "Boss maximum health must receive the three-times multiplier!"
    assert "attack.profile.aoeDamage * this.strengthMultiplier" in html, "Boss attack damage must receive the three-times multiplier!"
    assert "LATE_INTERMEDIATE_DIALOGUE_SCENES" in html, "The late journey must include narrative scenes between boss chapters!"
    for chapter in [66, 69, 72, 73, 74, 76, 78, 82, 83, 85, 88, 89, 91, 92, 95, 97, 98]:
        assert f"{chapter}: {{ asset:" in html or f"{chapter}: {{ asset" in html, f"Missing intermediate story dialogue for chapter {chapter}"

    # Campaign systems are gameplay-bearing, not decorative room labels.
    assert "transformation-choice-modal" in html and "chooseTransformationDoctrine" in html, "Yuanshi must offer 18/36/72 transformation doctrines!"
    assert "gameState.ruyiAcquired = true" in html and "if (!this.hasRuyiStaff)" in html, "Ruyi acquisition must upgrade the actual attack model!"
    assert "this.typeKey === 'campaign_buddha' ? 0.5 : 0.08" in html, "Campaign Buddha must end the fight at half health!"
    assert "gameState.campaignBiome" in html and "campaign_biomes" in html and "campaign_pilgrimage_biomes" in html and "campaign_final_biomes" in html, "Every campaign and pilgrimage chapter must render generated biome art!"
    for required_place in ["高老庄·竹林田舍", "流沙河·弱水险滩", "白虎岭·白骨荒原", "盘丝洞·七情蛛窟", "积雷山·牛魔王寨", "火云洞·三昧火阵", "火焰山·万里赤地", "翠云山·芭蕉洞"]:
        assert required_place in html, f"Missing distinct generated stage mapping: {required_place}"
    for required_late_place in ["祭赛国·金光寺碧波潭", "荆棘岭·小雷音寺", "狮驼岭·万妖之国", "比丘国·陷空山无底洞", "隐雾山·玉华州竹节山", "天竺国·广寒月宫", "灵山·凌云渡大雷音寺"]:
        assert required_late_place in html, f"Missing late-journey stage mapping: {required_late_place}"

    # Boon takeover/Peach progression and animation-contact correctness.
    god_block = source[source.index("const GODS ="):source.index("const LANGUAGE_SAVE_KEY")]
    boon_ids = re.findall(r"id: '([^']+)'", god_block)
    contract_block = source[source.index("const BOON_RUNTIME_CONTRACTS"):source.index("function validateBoonRuntimeContracts")]
    contracted_ids = re.findall(r"^\s+([a-z0-9_]+):\{mechanic:", contract_block, re.MULTILINE)
    assert len(boon_ids) == 41 and set(boon_ids) == set(contracted_ids), "Every selectable deity boon needs a mechanic-and-visual runtime contract!"
    assert "class ClockworkKiteCompanion" in source and "class ClockworkKiteRocket" in source, "Lu Ban's Clockwork Kite must exist as a visible combat companion with its own missile!"
    assert "activeClockworkKite.update(dt)" in source and "Clockwork Missile!" in source, "The Clockwork Kite must update, render, and visibly announce its attacks!"
    assert "this.bullArmorMax = 50" in source and "this.timeSinceDamage >= 8" in source, "Bull Demon Iron Body must provide and regenerate its promised armor!"
    assert "Horned shoulder plates" in source and "player.bullArmor" in source[source.index("function updateHUD"):], "Bull armor must be visible on Wukong and in the HUD!"
    for cast_id in ["luban_divine_gear", "erlang_ring", "guanyin_ring", "nezha_ring", "laojun_ring", "aoguang_ring"]:
        assert source.count(cast_id) >= 5, f"{cast_id} must have definition, translation, mechanic, and visual hooks!"
    assert "projectile.isEnemy" in source and "-projectile.vx * 1.15" in source, "Lu Ban's gear array must reflect hostile projectiles!"
    assert "this.guanyinBarrier = 30" in source and "this.hasBoon('nezha_dash')" in source, "Guanyin and Nezha dash cards need their promised shield and fire-trail mechanics!"
    assert "player.hasBoon('laojun_elixir')" in source and "player.hasBoon('luban_masterwork')" in source, "Peach passives must alter Peach upgrades instead of remaining text-only!"
    assert "nextLevel = Math.max(nextLevel, (previous.level || 1) + 1)" in html, "A new god attack boon must inherit and advance the equipped slot rank!"
    preview_block = source[source.index("const BOON_UPGRADE_PREVIEWERS"):source.index("function validateBoonUpgradePreviewers")]
    previewed_ids = re.findall(r"^\s+([a-z0-9_]+): f =>", preview_block, re.MULTILINE)
    assert len(previewed_ids) == 41 and set(boon_ids) == set(previewed_ids), "Every selectable deity boon needs an exact numeric Peach-rank preview!"
    assert "stronger primary and divine effects" not in html and "\u4e3b\u6548\u679c\u4e0e\u795e\u6548\u5f3a\u5ea6\u63d0\u5347" not in html, "Generic upgrade wording must never replace measurable stats!"
    assert "getPeachRankForecast" in html and "Rank ${rankForecast.level} \u2794 Rank ${forecastRankLabel}" in html, "Peach cards must show guaranteed and Lu Ban bonus-rank outcomes before selection!"
    assert "Current-weapon triple-strike base damage" in html and "Current-loadout outward hit" in html, "Attack and flying-staff upgrades need loadout-aware damage previews!"
    assert "player.getBoonLevel('laojun_elixir')" in html and "masterworkChance" in html, "Laojun and Lu Ban Peach modifiers must be included in the displayed rank forecast!"
    assert "truesightCritDamage" in html and "80 * (1 + 0.30 * (houndRank - 1))" in html, "Third-Eye crit damage and Xiaotianquan ranks must scale in real combat!"
    assert "const revivalRatio = nirvanaRank" in html and "this.qi = this.maxQi" in html, "Nirvana ranks must improve the actual revival, not only its card text!"
    assert "opensModal: true" in html and "if (!it.opensModal) openShopModal(false)" in html, "Buying a Peach must leave its upgrade modal visible while ordinary purchases rerender the same shop visit!"
    assert 'id="shop-resource-summary"' in html and "function renderShopResourceSummary()" in html, "The pavilion must show current resources inside its opaque decision modal!"
    assert "shop-gold-value" in html and "shop-health-value" in html and "shop-lives-value" in html and "shop-merit-value" in html, "Shop decisions need Spirit Stones, Health, lives, and Merit at a glance!"
    assert "balanceAfter" in html and "shortfall" in html and "aria-disabled" in html, "Each shop purchase must preview the remaining balance or clearly show the missing currency!"
    assert "BOSS_OUTCOME_INPUT_DELAY_MS = 1500" in html and "bossOutcomeUnlockAt - performance.now()" in html, "Boss outcomes need a visible input grace period to prevent combat click-through!"
    assert "setBossOutcomeChoicesLocked(true)" in html and "performance.now() < bossOutcomeUnlockAt" in html, "Alignment choices must remain disabled and independently reject early input!"
    assert 'id="boss-outcome-title" class="modal-title" tabindex="-1"' in html and "boss-outcome-title').focus" in html, "Outcome focus must land on the heading, never a choice that Enter could activate accidentally!"
    assert "const nearestGate = exitGates[0]" not in html, "Boon gates must not show an arrow that appears to recommend one reward!"
    assert "contactFrame / RUYI_CONTACT_FRAME_COUNT" in html and "isRuyiContactHit(ruyiContactShape" in html, "Wukong damage must land on the generated contact frame and visible staff path!"
    assert "baseReach:132" in html and "baseReach:154" in html and "baseReach:142" in html and "baseReach:138" in html, "Ordinary Ruyi reach must stay within the authored 132-154px contact paths!"
    assert "getRuyiSweepFrameAngle(progress, angle)" in html and "frame * (Math.PI / 4)" in html, "The 360 sweep collider must advance with each visible 45-degree staff frame!"
    assert "isRuyiContactHit(thrust, 140, 9, 0)" in html and "!isRuyiContactHit(thrust, 140, 13, 0)" in html, "Narrow thrust boundaries need explicit just-inside/just-outside regression coverage!"
    assert "isRuyiContactHit(slam, 173, 0, 0)" in html and "!isRuyiContactHit(slam, 176, 0, 0)" in html, "Localized overhead impact boundaries need explicit just-inside/just-outside coverage!"
    assert "!isRuyiContactHit(arc, 0, 100, 24)" in html, "A right-facing generated staff frame must not hit a target ninety degrees north!"
    for temporal_asset in ("wukong_ruyi_temporal_neutral", "wukong_ruyi_temporal_good", "wukong_ruyi_temporal_evil"):
        assert temporal_asset in html, f"Missing embedded temporal/directional Wukong atlas: {temporal_asset}"
    assert "moveRow * 8 + getRuyiDirectionalBodyFrameForAngle(angle)" in html and "getRuyiTemporalFrame(progress)" in html, "Every move needs eight temporal frames in every compass direction!"
    assert "getRuyiTemporalBodyRow(RUYI_CONTACT_PROFILES.slam, Math.PI / 2) === 22" in html, "South-facing slam must address row 22 in the move-major 32-row temporal atlas!"
    assert source.count("this.drawRuyiContactWeaponPath(ctx") == 1, "Base, alignment, and advanced combos must share one staff compositor without duplicate baked overlays!"
    assert "RUYI_TEMPORAL_GRIP_ANCHORS" in html and "drawRuyiContactWeaponPath(ctx, this.activeRuyiContactProfile, authoredProgress, handAnchor)" in html, "The generated weapon must originate from each temporal/directional pose's measured hand pivot!"
    assert "sourceAnchor[0] - 96" in html and "sourceAnchor[1] - 160" in html, "Measured source anchors must use the exact 192px body draw transform!"
    assert html.count("getRuyiWorldShaft(") >= 4 and "...ruyiWorldShaft" in html and "worldShaft.originX" in html, "Rendering, collision, and burst placement must share the same authored world shaft!"
    assert "RUYI_WEAPON_SOURCE_SEGMENTS" in html and "RUYI_WEAPON_SOURCE_SEGMENTS.spin.length === 8" in html and "sourceSegment.length" in html, "All eight inconsistent spin frames need independent measured pivot/tip normalization!"
    assert "getRuyiTemporalAtlasKey(alignmentPath)" in html, "Temporal attacks must preserve neutral, Good, and Evil bitmap identities!"
    assert "comboMove?.contactAt ?? (ruyiContactProfile.contactFrame / RUYI_CONTACT_FRAME_COUNT)" in html, "Advanced combos must preserve their authored .58-.72 contact timing!"
    assert "getRuyiAuthoredProgress(attackProgress, this.activeRuyiContactProfile, this.activeAttackContactAt)" in html, "Weapon frames must be time-warped so each combo's chosen contact frame matches its authored timing!"
    resolve_attack = source[source.index("resolvePendingAttack(sweepProgress"):source.index("      procAlignmentOnHit(enemy, combo")]
    feedback_block = resolve_attack[resolve_attack.index("if (hitAny)"):]
    assert "playStaffHit" in feedback_block and "createScreenShake" in feedback_block and "beginConfirmedMeleeHitStop" in feedback_block, "Sound, shake, and hit-stop must share the confirmed-contact branch!"
    assert "playStaffHit" not in resolve_attack[:resolve_attack.index("if (hitAny)")] and "createScreenShake" not in resolve_attack[:resolve_attack.index("if (hitAny)")], "Whiffs must not make hit sounds or shake the screen!"
    assert "worldHitStopRemaining > 0" in html and "? .095 : .055" in html, "Confirmed normal/heavy contacts need readable 55/95ms world hit-stop!"
    assert "meleeContactHoldTimer" in html and "enemy.hp > 0 ? .20 : .12" in html, "Enemies must show a nonlethal hurt pose and a brief lethal contact hold before disappearing!"
    assert "const runFrames = r === 2 ? 5 : 6" in html, "Horizontal locomotion must not sample the known-empty frame!"

    # Rare Buddha boon, real Luban weapon forms, and composed Ruyi synergies.
    assert "puti_strike" not in source and "puti_special" not in source, "The accidental Lady White Bone/Puti boon provider must be removed!"
    assert "buddha: {" in source and "buddha_dharma_return" in source and "buddha_equanimity" in source, "Buddha must replace the removed boon provider with gameplay-bearing choices!"
    assert "offerWeight: 1" in source and "DEFAULT_GOD_OFFER_WEIGHT = 3" in source, "Buddha must be exactly three times rarer than an ordinary deity!"
    assert "takeWeightedGodKey(godKeys)" in source and "const firstGodKey = takeWeightedGodKey(godKeys)" in source, "Every deity gate draw must use weighted sampling without replacement!"
    assert "if (slot.includes('\u795e\u5175') || slot.includes('\u91cd\u94f8')) return 'weapon'" in source, "Luban reforges need an exclusive weapon slot!"
    assert "luban_chain_staff" in source and "const RUYI_WEAPON_PROFILES" in source, "Luban must offer three mechanically distinct Ruyi forms!"
    assert "range: 1.65" in source and "turnHold: 0.42" in source and "turnSlam: true" in source, "Extend, chain, and titan throws need measurable distinct mechanics!"
    assert "0.18 * (weaponLevel - 1)" in source and "0.05 * (weaponLevel - 1)" in source, "Peach ranks on a weapon form must improve its throw numerically!"
    assert "onRuyiCreated" in source and "onRuyiTurn" in source and "onRuyiCatch" in source and "onRuyiReflect" in source, "The thrown staff needs explicit, bounded lifecycle hooks!"
    assert "compassionate_lotus_return" in source and "furnace_forged_needle" in source and "wind_calls_rain" in source, "Buddha/Guanyin and weapon-element deity synergies must exist!"
    assert "source.buddhaSeals.add(enemy)" in source and "source.buddhaDetonated.has(enemy)" in source, "Buddha's return detonation must be capped once per target per throw!"
    assert "if (player.boons.weapon) equipped.push(player.boons.weapon)" in source, "Peaches must be able to rank up the equipped Luban weapon form!"

    # Persistent NG+ and playable Erlang Shen use a separate, complete action kit.
    assert "erlang_player_actions" in source and "5 rows x 7 isolated frames" in Path("package_all_clean_sheets.py").read_text(encoding="utf-8"), "Playable Erlang needs a dedicated, safely packed action atlas!"
    assert "function startNewGamePlus()" in source and "campaignUnlocks.newGamePlus = true" in source, "Completing the full journey must unlock persistent New Game+!"
    assert "campaignUnlocks.erlangPlayable = true" in source and "equippedHero: gameState.playableHero" in source, "Erlang unlock and hero selection must persist in browser storage!"
    assert "performErlangEyeLance" in source and "performErlangJudgmentArray" in source and "triggerErlangManifestation" in source, "Erlang requires distinct Q, E, and R/F skills!"
    assert "performRightClickSkill" in source and "commandXiaotianquan" in source and "companionCommandActive" in source, "Right-click must command Xiaotianquan instead of throwing Wukong's staff!"
    assert "gameState.playableHero === 'erlang'" in source and "row = 4" in source, "Erlang must render his generated combat and Manifestation frames!"
    assert "this.typeKey === 'campaign_erlang'" in source and "Campaign Yang Jian shares the definitive playable identity" in source, "Campaign Erlang must use the same new third-eye and three-pointed-spear animation set!"
    assert "NG_PLUS_ENEMY_HP_MULTIPLIER = 7" in source, "NG+ enemies must have exactly seven times their normal maximum Health!"
    assert "NG_PLUS_ENEMY_DAMAGE_MULTIPLIER = 3" in source and "gameState.isNewGamePlus) amount *= NG_PLUS_ENEMY_DAMAGE_MULTIPLIER" in source, "NG+ enemy damage must be tripled once at the player damage boundary!"
    assert "const NG_PLUS_ENEMY_TIERS" in source and source.count("ngp_") >= 40, "NG+ needs twenty named enemy definitions plus a chapter-scaled encounter roster!"
    assert "getNewGamePlusEnemyPool(index)" in source and "if (gameState.isNewGamePlus) return getNewGamePlusEnemyPool(index)" in source, "NG+ chapters must actually spawn the new roster!"
    for atlas_index in range(1, 5):
        atlas_name = f"ng_plus_enemies_{atlas_index}"
        assert atlas_name in source, f"Missing embedded NG+ atlas hook: {atlas_name}"
        ngp_sheet = Image.open(Path("assets_webp") / f"{atlas_name}.webp").convert("RGBA")
        assert ngp_sheet.size == (1400, 1000), f"{atlas_name} must be a strict 7x5 atlas of 200px cells"
        for row in range(5):
            for col in range(7):
                frame = ngp_sheet.crop((col * 200, row * 200, (col + 1) * 200, (row + 1) * 200))
                alpha_frame = frame.getchannel("A")
                visible_pixels = sum(pixel > 20 for pixel in alpha_frame.getdata())
                bbox = alpha_frame.getbbox()
                assert visible_pixels > 800, f"NG+ animation frame {atlas_name} r{row}c{col} is blank or unusably sparse"
                assert bbox and bbox[0] >= 48 and bbox[1] >= 48 and bbox[2] <= 152 and bbox[3] <= 152, f"NG+ animation frame {atlas_name} r{row}c{col} violates its 48px safe gutter: {bbox}"
    ngp_source_dir = Path("assets_sources") / "ng_plus_enemies"
    assert len(list(ngp_source_dir.glob("ngp_*_v1_source.png"))) == 20, "All twenty project-bound ImageGen NG+ source strips must remain available for repacking!"
    assert "const passiveRecoveryAllowed = !gameState.chamberCleared" in source, "Passive Health and Qi recovery must know when combat has ended!"
    assert "passiveRecoveryAllowed && this.qi < this.maxQi" in source and "regenRank && passiveRecoveryAllowed" in source, "Players must not wait in a cleared room to refill Qi or transformation Health!"
    assert "Post-battle Health and Qi regeneration is paused" in source, "The chamber-clear banner must explain why passive recovery stopped!"
    assert Path("assets_sources/erlang_shen/erlang_identity_anchor_v2.png").exists() and Path("assets_sources/erlang_shen/erlang_player_actions_v2_source.png").exists(), "The generated blue-white Erlang identity and 35-frame source must remain project-bound!"
    packer_source = Path("package_all_clean_sheets.py").read_text(encoding="utf-8")
    assert "key_erlang_checkerboard_cell" in packer_source and "(col + 0.5) * source.width / (cols + 1)" in packer_source, "Erlang's white robes and half-cell safety margins must survive deterministic repacking!"

    erlang_sheet = Image.open("assets_webp/erlang_player_actions.webp").convert("RGBA")
    assert erlang_sheet.size == (1680, 1200), "Playable Erlang atlas must remain a strict 7x5 grid of 240px cells!"
    alpha = erlang_sheet.getchannel("A")

    erlang_combo_sheet = Image.open("assets_webp/erlang_combo_actions.webp").convert("RGBA")
    assert erlang_combo_sheet.size == (1680, 1200), "Erlang combo atlas must remain a strict 7x5 grid of 240px cells!"
    combo_counts = []
    for row in range(5):
        for col in range(7):
            alpha_cell = erlang_combo_sheet.crop(
                (col * 240, row * 240, (col + 1) * 240, (row + 1) * 240)
            ).getchannel("A")
            combo_counts.append(sum(pixel > 8 for pixel in alpha_cell.getdata()))
    assert min(combo_counts) > 1200, f"Every Erlang combo frame needs authored body/effect art; visible counts: {combo_counts}"
    for row in range(5):
        for col in range(7):
            cell = alpha.crop((col * 240, row * 240, (col + 1) * 240, (row + 1) * 240))
            bbox = cell.getbbox()
            assert bbox is not None, f"Erlang frame r{row}c{col} must not be blank!"
            assert bbox[0] >= 56 and bbox[2] <= 184 and bbox[1] >= 56 and bbox[3] <= 184, f"Erlang frame r{row}c{col} must keep its 56px gutter and shared foot pivot!"

    print("ALL STRUCTURE, ASSET, AND GAMEPLAY REGRESSION TESTS PASSED!")

if __name__ == "__main__":
    test_game_features()
