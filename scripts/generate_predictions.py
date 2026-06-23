#!/usr/bin/env python3
"""
AI预测生成脚本
调用LLM生成两个AI的预测结果
"""

import json
import yaml
from pathlib import Path
from openai import OpenAI

def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_prompt(name: str) -> str:
    """加载人设Prompt"""
    prompt_path = Path(__file__).parent.parent / "prompts" / f"{name}.txt"
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def call_llm(system_prompt: str, user_prompt: str, config: dict) -> str:
    """调用LLM API"""
    llm_config = config.get('llm', {})
    provider = llm_config.get('provider', 'openai')
    
    if provider == 'openai':
        client = OpenAI(api_key=llm_config.get('api_key'))
        response = client.chat.completions.create(
            model=llm_config.get('model', 'gpt-4o-mini'),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    
    elif provider == 'anthropic':
        import anthropic
        client = anthropic.Anthropic(api_key=llm_config.get('api_key'))
        response = client.messages.create(
            model=llm_config.get('model', 'claude-3-haiku-20240307'),
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return response.content[0].text
    
    elif provider == 'groq':
        from groq import Groq
        client = Groq(api_key=llm_config.get('api_key'))
        response = client.chat.completions.create(
            model=llm_config.get('model', 'llama-3.3-70b-versatile'),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    
    else:
        raise ValueError(f"不支持的LLM提供商: {provider}")

def generate_prediction(match: dict, config: dict) -> dict:
    """为一场比赛生成两个AI的预测"""
    hongli_prompt = load_prompt('hongli')
    hermes_prompt = load_prompt('hermes')
    
    user_prompt = f"预测这场比赛：{match['team_a']} vs {match['team_b']}"
    
    print(f"\n🤖 正在预测：{match['team_a']} vs {match['team_b']}")
    
    # 弘历预测
    print("  👑 弘历思考中...")
    hongli_response = call_llm(hongli_prompt, user_prompt, config)
    hongli_data = parse_prediction(hongli_response, match)
    
    # 赫妹预测
    print("  🔮 赫妹思考中...")
    hermes_response = call_llm(hermes_prompt, user_prompt, config)
    hermes_data = parse_prediction(hermes_response, match)
    
    return {
        "match": match,
        "hongli": hongli_data,
        "hermes": hermes_data
    }

def parse_prediction(response: str, match: dict) -> dict:
    """解析LLM返回的预测结果"""
    try:
        # 尝试解析JSON
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return {
                "score": f"{data.get('team_a_score', '?')}-{data.get('team_b_score', '?')}",
                "winner": data.get('winner', '未知'),
                "reasons": data.get('reasons', ['暂无理由'])
            }
    except:
        pass
    
    # 解析失败，使用默认值
    return {
        "score": "1-1",
        "winner": "平局",
        "reasons": ["预测分析中..."]
    }

def save_predictions(predictions: list, output_path: Path):
    """保存预测结果"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(predictions, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 预测结果已保存到 {output_path}")

def main():
    config = load_config()
    
    # 读取赛程
    schedule_path = Path(__file__).parent.parent / "output" / "schedule.json"
    if not schedule_path.exists():
        print("❌ 请先运行 fetch_schedule.py 获取赛程")
        exit(1)
    
    with open(schedule_path, 'r', encoding='utf-8') as f:
        matches = json.load(f)
    
    print(f"⚽ 开始预测 {len(matches)} 场比赛...")
    
    predictions = []
    for match in matches:
        pred = generate_prediction(match, config)
        predictions.append(pred)
    
    # 保存结果
    output_path = Path(__file__).parent.parent / "output" / "predictions.json"
    save_predictions(predictions, output_path)
    
    # 打印摘要
    print("\n📊 预测摘要：")
    for pred in predictions:
        m = pred['match']
        h = pred['hongli']
        he = pred['hermes']
        print(f"  {m['team_a']} vs {m['team_b']}")
        print(f"    弘历：{h['score']} {h['winner']}")
        print(f"    赫妹：{he['score']} {he['winner']}")

if __name__ == "__main__":
    main()
