# 定制指南

## 换主题

不只是世界杯！你可以换成任何预测主题。

### A股涨跌预测

修改 `prompts/hongli.txt`：
```
你是一个散户之王，直觉敏锐，擅长技术分析。
口头禅：「我看涨」「此乃牛股」「技术面显示」
风格：K线形态、MACD、量价关系
```

修改 `prompts/hermes.txt`：
```
你是一个量化女神，模型至上，数据为王。
口头禅：「姐算过了」「数据显示」「风险控制」
风格：基本面、估值、资金流向
```

### 星座运势预测

修改 `prompts/hongli.txt`：
```
你是一个玄学大师，星象解读专家。
口头禅：「星象显示」「此乃天意」「运势分析」
风格：行星位置、相位、宫位
```

修改 `prompts/hermes.txt`：
```
你是一个心理学家，性格分析专家。
口头禅：「姐分析过」「性格决定」「数据表明」
风格：MBTI、性格特质、行为模式
```

### 综艺预测

修改 `prompts/hongli.txt`：
```
你是一个娱乐圈老炮，人脉广，消息灵通。
口头禅：「我听说」「业内消息」「这节目稳了」
风格：嘉宾阵容、话题热度、收视预期
```

修改 `prompts/hermes.txt`：
```
你是一个数据控，收视率为王。
口头禅：「姐查过」「收视率显示」「话题度分析」
风格：收视数据、社交媒体热度、广告商反馈
```

## 换视觉风格

### 动森暖色系（适合小红书）

修改 `templates/prediction.html` 中的CSS：

```css
body {
  background: #2d5016;  /* 深绿草地 */
}

.card {
  background: 
    radial-gradient(circle at 20% 80%, rgba(25,200,185,0.15) 0%, transparent 50%),
    linear-gradient(180deg, #2d5016 0%, #1e3a0f 100%);
}

.team-name {
  color: #f8f8f0;  /* 奶油色 */
}

.pred-pick.hongli {
  color: #d4a853;  /* 金色 */
}

.pred-pick.hermes {
  color: #19c8b9;  /* 薄荷绿 */
}
```

### 杂志极简风（适合公众号）

```css
body {
  background: #f5f5f5;
  color: #333;
}

.card {
  background: #fff;
  border: 1px solid #eee;
}

.team-name {
  font-weight: 300;
  letter-spacing: 0.1em;
}
```

## 加互动功能

### 弹幕抓取

扩展 `scripts/fetch_schedule.py`，加入弹幕监听：

```python
# 伪代码
def fetch_danmu(platform):
    """抓取直播弹幕"""
    if platform == 'douyin':
        # 使用抖音弹幕API
        pass
    elif platform == 'bilibili':
        # 使用B站弹幕API
        pass
```

### 积分排行榜

创建 `data/leaderboard.json`：

```json
{
  "users": [
    {"name": "用户A", "score": 120, "correct": 8},
    {"name": "用户B", "score": 95, "correct": 6}
  ]
}
```

### 礼物系统

监听直播礼物事件，触发特殊预测：

```python
# 伪代码
def on_gift_received(gift_type):
    if gift_type == "火箭":
        # 触发超级预测
        return generate_super_prediction()
    elif gift_type == "棒棒糖":
        # 触发提示
        return generate_hint()
```

## 常见问题

### Q: API调用失败怎么办？

A: 检查 `config.yaml` 中的API Key是否正确。推荐使用Groq（免费）。

### Q: 截图是黑色的？

A: 确保安装了Chrome浏览器，并且字体加载完成（等待3秒）。

### Q: 如何支持更多语言？

A: 修改 `templates/prediction.html` 中的文字即可。

### Q: 如何部署到服务器？

A: 使用Docker：

```dockerfile
FROM python:3.9
RUN apt-get update && apt-get install -y chromium-browser
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "scripts/main.py"]
```
