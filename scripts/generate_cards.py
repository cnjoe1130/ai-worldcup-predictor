#!/usr/bin/env python3
"""
HTML卡片生成脚本
将预测结果填充到HTML模板中
"""

import json
from pathlib import Path
from jinja2 import Template

# 国旗emoji映射
FLAG_MAP = {
    "阿根廷": "🇦🇷", "奥地利": "🇦🇹", "法国": "🇫🇷", "伊拉克": "🇮🇶",
    "挪威": "🇳🇴", "塞内加尔": "🇸🇳", "约旦": "🇯🇴", "阿尔及利亚": "🇩🇿",
    "葡萄牙": "🇵🇹", "乌兹别克斯坦": "🇺🇿", "英格兰": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "加纳": "🇬🇭",
    "巴拿马": "🇵🇦", "克罗地亚": "🇭🇷", "哥伦比亚": "🇨🇴", "刚果民主共和国": "🇨🇩",
    "西班牙": "🇪🇸", "沙特": "🇸🇦", "比利时": "🇧🇪", "伊朗": "🇮🇷",
    "乌拉圭": "🇺🇾", "佛得角": "🇨🇻", "新西兰": "🇳🇿", "埃及": "🇪🇬",
    "巴西": "🇧🇷", "墨西哥": "🇲🇽", "德国": "🇩🇪", "日本": "🇯🇵",
    "荷兰": "🇳🇱", "韩国": "🇰🇷", "美国": "🇺🇸", "意大利": "🇮🇹",
}

def get_flag(team_name: str) -> str:
    """获取队伍的国旗emoji"""
    return FLAG_MAP.get(team_name, "🏳️")

def load_template() -> Template:
    """加载HTML模板"""
    template_path = Path(__file__).parent.parent / "templates" / "prediction.html"
    with open(template_path, 'r', encoding='utf-8') as f:
        return Template(f.read())

def generate_card(prediction: dict, day_num: int) -> str:
    """生成单场比赛的HTML卡片"""
    template = load_template()
    
    match = prediction['match']
    hongli = prediction['hongli']
    hermes = prediction['hermes']
    
    # 格式化弘历预测
    hongli_prediction = f"{match['team_a']} {hongli['score']}"
    hongli_reasons = [f"<strong>{r.split('：')[0]}：</strong>{r.split('：')[1]}" if '：' in r else f"<strong>{r}</strong>" for r in hongli['reasons']]
    
    # 格式化赫妹预测
    if hermes['winner'] == '平局':
        hermes_prediction = f"{hermes['score']} 平局"
    else:
        hermes_prediction = f"{match['team_a']} {hermes['score']}"
    hermes_reasons = [f"<strong>{r.split('：')[0]}：</strong>{r.split('：')[1]}" if '：' in r else f"<strong>{r}</strong>" for r in hermes['reasons']]
    
    # 渲染模板
    html = template.render(
        day_tag=f"DAY {day_num}",
        group_tag=match.get('group', '小组赛'),
        team_a_flag=get_flag(match['team_a']),
        team_a_name=match['team_a'],
        team_b_flag=get_flag(match['team_b']),
        team_b_name=match['team_b'],
        match_date="6月24日（周三）",
        match_time=match.get('time', 'TBD'),
        venue=match.get('venue', '待确认'),
        hongli_prediction=hongli_prediction,
        hongli_reasons=hongli_reasons,
        hermes_prediction=hermes_prediction,
        hermes_reasons=hermes_reasons,
        tags=f"#世界杯聊个球 #{match['team_a']}vs{match['team_b']} #世界杯 #AI预测 #热AI训练营"
    )
    
    return html

def main():
    # 读取预测结果
    predictions_path = Path(__file__).parent.parent / "output" / "predictions.json"
    if not predictions_path.exists():
        print("❌ 请先运行 generate_predictions.py 生成预测")
        exit(1)
    
    with open(predictions_path, 'r', encoding='utf-8') as f:
        predictions = json.load(f)
    
    # 输出目录
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    print(f"🎨 正在生成 {len(predictions)} 张卡片...")
    
    for i, pred in enumerate(predictions, 1):
        match = pred['match']
        html = generate_card(pred, day_num=13)
        
        # 保存HTML文件
        filename = f"prediction-{match['team_a']}-{match['team_b']}.html"
        filename = filename.replace(' ', '-').lower()
        output_path = output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  ✅ {filename}")
    
    print(f"\n🎉 卡片生成完成！共 {len(predictions)} 张")
    print(f"📁 输出目录：{output_dir}")

if __name__ == "__main__":
    main()
