# 《西游记：孙悟空正传》 (Journey to the West: Wukong's Chronicle)

一款基于 HTML5 Canvas + Web Audio API 打造的《西游记》神魔动作肉鸽（Roguelite）单文件网页游戏。完整 100 章连续推进，从花果山、大闹天宫一路写到灵山成佛；包含中英双语、显式开局教学、五种真身、觉醒、持久化神通树、桌面与触屏操作、暂停和低动态效果适配。

---

## 🎮 快速开始 (How to Play)

### 方法一：本地游玩 (Local Browser)
Windows 用户请直接双击 `PLAY_GAME.bat`，等待浏览器打开后点击“完整西游”，再用 WASD 移动。启动器窗口需在游玩期间保持开启。

也可在项目目录手动运行 `python -m http.server 8765`，然后打开 `http://127.0.0.1:8765/`。不建议直接双击 `index.html`：部分浏览器会限制 `file://` 页面的本地存档或输入初始化。游戏现在会安全降级为临时内存存档，但通过本地服务器启动才能稳定保留永久神通进度。

### 方法二：GitHub Pages 网页托管 (GitHub Pages Deployment)
1. 将本项目推送到你的 GitHub 仓库。
2. 进入仓库的 **Settings** -> **Pages**。
3. 在 **Build and deployment** 下将 **Branch** 设置为 `main`（或 `master`），目录选择 `/ (root)`，点击 **Save**。
4. 稍等片刻，即可通过 GitHub 提供的公开网址直接在线畅玩！

---

## ⚔️ 操控指南 (Controls)

| 按键 | 动作 | 说明 |
| :--- | :--- | :--- |
| **W / A / S / D** 或 **方向键** | 身法移动 | 齐天大圣移动，身形随光标精准转向 |
| **鼠标左键** | 棍法三连击 | 前期使用花果山石棍；击败东海龙王后取得一万三千五百斤如意金箍棒，并真实提升伤害与范围 |
| **鼠标右键** 或 **Q** | 如意飞棒 | 将高速旋转的如意棒掷出；去程与回程各自命中，最终飞回悟空手中 |
| **E 键** | 吹毛成兵 | 消耗真气唤出猴王分身协同作战 |
| **空格键** 或 **Shift** | 筋斗云瞬移闪避 | 一个筋斗十万八千里，穿梭敌阵并触发身法神通 |
| **R 键** 或 **F 键** | 七十二变·真身 | 启用当前装备的苍龙、白虎、大鹏、巨猿或玄武真身；持续时间结束后自动还原 |
| **G 键** | 大闹天宫·觉醒 | 觉醒槽蓄满后释放十秒齐天神威，强化伤害、范围与身法 |
| **Esc** | 暂停 / 继续 | 打开暂停菜单，可静音、重新开始或返回天宫门前 |
| **📜 七十二变** | 地煞神通谱 | 消耗功德灵砂参悟石猴金身、火眼金睛与不灭法躯 |
| **☯ 因果善恶** | 永久阵营神通树 | 查看 −100 至 +100 因果平衡，并投资善、恶或中道的 36 项神通 |
| **📖 伏魔录** | 西游万神图鉴 | 查看三界十大仙圣与一百零八式神通妙法 |

窄屏与触屏设备会自动显示虚拟摇杆及攻击、闪避、神通、法阵、真身和觉醒按钮。

神通树支持拖拽平移、单击选择和双击直接投资。神木节点、装备真身、功德灵砂以及“斗战本能”等永久被动都会立即保存到浏览器；死亡、重新开局和关闭页面不会清除。当前存档内容版本为 6，并继续使用稳定的 `havocInHeavenMetaV3` 浏览器键，方便兼容旧存档及后续接入云端账户同步。

每场剧情首领战都以“伏地未死”结束并暂停战斗，随后提供符合原著情节的善、恶、中道三种非致死处置。善行使因果 +1，恶行通过吸收真炁或贪取宝物使因果 −1，中道不移动；这个分数跨周目永久累积。善树偏向护甲、减伤、圣光与复苏，恶树偏向伤害、攻速、吸血与幽冥爆发，中道在接近零点时提供较弱但全面的混合效果。已购买等级永不删除；当因果越过门槛时，只会休眠，回到所需阵营后会自动恢复。

普通攻击神通采用“接管不清零”规则：新仙圣的普攻会替换神效与颜色，但继承已有蟠桃修为并自动再升一重。蟠桃界面会明确显示三连击的伤害变化，商店购买蟠桃后不再被商店重新覆盖。

全部 41 项仙圣赐福都有独立的玩法挂钩与可见反馈。鲁班“神机木鸢”会实际绕行、锁敌、发射追踪霹雳弹并范围爆炸；牛魔王“铁躯”显示带角铁甲、独立护甲数值和八秒未受击后的完整回复。六种法阵分别实现齿轮反弹、天眼增伤、莲台治疗、乾坤圈连锁、八卦炉灼烧与归墟吸附；三种身法分别实现雷击、玉露盾与风火轨迹。测试会逐项比对赐福定义、玩法实现和视觉反馈，新增纯文字占位赐福会直接令构建测试失败。

五种真身现在各自使用专属 7 帧攻击序列与完整战斗循环：苍龙连锁引雷、白虎高速流血、大鹏风刃游击、魔猿霸体重拳、玄武减伤回复。仙圣普攻赐福只作为第二层神效，不会再覆盖真身的攻击身份。

七十二变神木的 71 项真身与分支节点不再提供笼统的常驻“通用精通”。每项技巧只在装备并开启对应真身后生效，并明确挂接在变身启动、普通攻击、飞棒特殊、E 键真身法术、闪避、受击、击败敌人或持续光环之一。五种 E 法术分别是苍龙“潜渊雷雨”、白虎“虎啸撼岳”、大鹏“天罡神风”、巨猿“擎天怒砸”和玄武“幽通九泉”；技能触发会显示小型动态神通印、元素法阵、多段冲击或专属羽刃，离开变身后全部休眠。真正需要跨形态永久生效的成长仍由下方四行“永久被动修行”承担。

---

## 👹 100 章孙悟空正传 (Story Campaign)

标题界面只提供一条第 1–100 章的完整西游。第 65 章结束后会直接进入第 66 章，保留本局取得的金箍棒、神通、仙圣赐福、武器重铸与蟠桃修为，不再重置或返回标题。

- **第 1–5 章**：花果山群猴试艺，老猿寨主守山巅。
- **第 6–12 章**：登昆仑玉虚宫；元始天尊让玩家亲选十八斗战、三十六天罡或七十二地煞变化，并以门人和天尊亲试传法。
- **第 13–19 章**：闯东海龙宫、战东海龙王，取得会随心伸缩的如意金箍棒。
- **第 20–32 章**：大闹天宫，依次战哪吒、四大天王、二郎神与如来。佛祖降至半血即以五指化山镇住悟空。
- **第 33 章**：唐三藏揭下金帖，师徒开始西行。
- **第 36 / 40 章**：高老庄战猪八戒、流沙河战沙悟净，败而成友。
- **第 45 / 50 章**：白虎岭三打白骨精，盘丝洞破蜘蛛女王七情蛛阵。
- **第 55 / 60 / 65 章**：积雷山战牛魔王、火云洞战红孩儿、翠云山战铁扇公主，借扇平息火焰山。

- **第 66–72 章**：祭赛国追佛宝、碧波潭战九头虫；荆棘岭论诗心，再破黄眉小雷音与七绝山红鳞巨蟒。
- **第 73–77 章**：朱紫国悬丝诊脉，智盗紫金铃战赛太岁，并在黄花观破百眼魔君毒日阵。
- **第 78–82 章**：闯狮驼岭三关，分别战青狮、黄牙白象与金翅大鹏，解救万妖之国囚民。
- **第 83–90 章**：比丘国救千童、灭法国一夜剃城、无底洞寻唐僧，再破隐雾山南山大王假首迷局。
- **第 91–96 章**：玉华州传授三王子武艺，夺回三件神兵；竹节山战黄狮与九灵元圣，金平府同时迎战辟寒、辟暑、辟尘三犀王。
- **第 97–100 章**：天竺国识破玉兔假公主，经凌云渡取得真经、补足八十一难，回到灵山受封斗战胜佛。

全线使用 27 张独立生成式场景和 36 名剧情角色的 252 个状态帧。关键首领与转折提供可逐句推进的中英双向对白；对白和奖励选择期间都会锁住完整战斗模拟。

---

## 🛠️ 项目文件结构 (Files)

- `index.html`：**完全自包含的单文件游戏**（内嵌所有 108 式神通、音频合成器与 Base64 精美美术）
- `generate_complete_game.py`：构建与编译游戏主文件的 Python 脚本
- `package_all_clean_sheets.py`：清理、校验并重新打包精灵图与生成式美术
- `assets_webp/`：包含所有高清 WebP 游戏原画与精灵图切片
- `test_game.py`：结构、资源网格与关键玩法回归测试
- `browser_campaign_smoke.js`：通过浏览器调试协议实测关键剧情跳转、奖励、半血佛祖转场与控制台错误


---

## 🐒 闯关问答 · The between-rounds question gate (Polymath Chinese Portal)

This copy of the game lives inside the Polymath **Chinese Learning Portal**
(`polymathlc/chinese`), and it has one thing the original does not.

Clear a chamber, three gates open — and stepping into one now asks **three
short Chinese questions** before it hands the reward over.

| | |
| :--- | :--- |
| **Every right answer** | +10 health, at once |
| **3 right** | the reward arrives 3 ranks better |
| **2 right** | 2 ranks better |
| **1 right** | 1 rank better |
| **0 right** | the ordinary reward — the gate never punishes, it only pays |

"Better" means what it says at each gate: a divine boon comes in already
advanced, a celestial peach raises the rank by that many more, and the
pavilion / ginseng fruit / merit sand gates each pay more.

**The questions are your teacher's own.** They are read live out of the
portal's question bank next door, and only the SHORT ones are ever asked —
never a comprehension passage, a cloze or an editing passage: you answer these
standing in a doorway with a horde on the other side. Signed out, offline, or
with nothing short enough in the bank, the gate falls back to a built-in
practice set, and the card always says which of the two a question came from.

Answering a bank question is recorded in the portal's usage tracker under
**Journey to the West**, exactly like any other practice mode.
