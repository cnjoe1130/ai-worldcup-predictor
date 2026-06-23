# ⚽ AI吵个球 — 世界杯AI预测系统

两个AI吵架预测世界杯，自动生成预测卡片，一键发布小红书。

## 效果展示

每天自动生成这样的预测卡：

- 弘历👑（玄学派）：永远选赢家，理由靠底蕴、天意、名将
- 赫妹🔮（数据派）：经常预测平局，理由靠数据、概率、xG

**两人永远不能预测一样的结果，制造冲突才有看点。**

## 快速开始

### 1. 环境要求

- Python 3.8+
- Chrome浏览器（用于截图）
- 任意LLM API（OpenAI / Claude / Groq / 通义千问 等）

### 2. 安装

```bash
git clone https://github.com/yourname/ai-worldcup-predictor.git
cd ai-worldcup-predictor
pip install -r requirements.txt
```

### 3. 配置API

复制配置文件并填入你的API Key：

```bash
cp config.example.yaml config.yaml
# 编辑 config.yaml，填入你的API Key
```

### 4. 一键生成

```bash
# 1. 获取今日赛程
python scripts/fetch_schedule.py

# 2. 生成预测
python scripts/generate_predictions.py

# 3. 生成卡片图
python scripts/generate_cards.py

# 4. 截图
python scripts/screenshot.py
```

输出文件在 `output/` 目录下。

## 项目结构

```
ai-worldcup-predictor/
├── README.md              # 本文件
├── config.example.yaml    # 配置模板
├── requirements.txt       # Python依赖
├── prompts/
│   ├── hongli.txt         # 弘历人设Prompt
│   ├── hermes.txt         # 赫妹人设Prompt
│   └── schedule.txt       # 赛程提取Prompt
├── templates/
│   ├── prediction.html    # 预测卡HTML模板
│   └── styles.css         # 卡片样式
├── scripts/
│   ├── fetch_schedule.py  # 赛程抓取
│   ├── generate_predictions.py  # AI预测生成
│   ├── generate_cards.py  # HTML卡片生成
│   └── screenshot.py      # Chrome截图
├── output/                # 输出目录
└── docs/
    └── customization.md   # 定制指南
```

## 定制指南

### 换主题

不只是世界杯！你可以换成任何预测主题：

| 主题 | 弘历人设 | 赫妹人设 |
|------|---------|---------|
| 世界杯 | 清朝皇帝，自信果断 | 数据女王，冷静理性 |
| A股涨跌 | 散户之王，直觉敏锐 | 量化女神，模型至上 |
| 星座运势 | 玄学大师，星象解读 | 心理学家，性格分析 |
| 综艺预测 | 娱乐圈老炮，人脉广 | 数据控，收视率为王 |

### 换视觉风格

修改 `templates/styles.css` 即可：

- 暗底科技风：当前默认
- 动森暖色系：适合小红书泛受众
- 杂志极简风：适合公众号

### 加互动功能

扩展方向：
- 弹幕抓取 → 观众投票
- 积分排行榜 → 答题游戏
- 礼物系统 → 直播互动

## 技术栈

- **LLM**: OpenAI / Claude / Groq / 通义千问（任选）
- **数据**: Wikipedia API / FIFA官网
- **模板**: HTML + CSS
- **截图**: Chrome Headless
- **发布**: 手动 / 可扩展自动化

## License

MIT — 随便用，记得注明"AI吵个球"就行 😂
