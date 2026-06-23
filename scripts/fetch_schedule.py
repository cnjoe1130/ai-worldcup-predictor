#!/usr/bin/env python3
"""
赛程抓取脚本
从Wikipedia API获取世界杯赛程数据
"""

import json
import requests
import yaml
from pathlib import Path

def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    if not config_path.exists():
        print("❌ 请先复制 config.example.yaml 为 config.yaml 并配置")
        exit(1)
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def fetch_wikipedia_schedule(group: str) -> list:
    """从Wikipedia获取小组赛赛程"""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": f"2026_FIFA_World_Cup_Group_{group}",
        "prop": "wikitext",
        "format": "json"
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        wikitext = data.get('parse', {}).get('wikitext', {}).get('*', '')
        return parse_wikitext_schedule(wikitext, group)
    except Exception as e:
        print(f"⚠️ Wikipedia API失败: {e}")
        return []

def parse_wikitext_schedule(wikitext: str, group: str) -> list:
    """解析Wikitext格式的赛程"""
    import re
    
    matches = []
    # 匹配比赛模式：队A vs 队B
    pattern = r'===\s*(.+?)\s+vs\s+(.+?)\s*==='
    
    for match in re.finditer(pattern, wikitext):
        team_a = match.group(1)
        team_b = match.group(2)
        
        # 尝试提取时间（本地时间）
        time_pattern = r'(\d{1,2}:\d{2})'
        time_match = re.search(time_pattern, wikitext[match.start():match.start()+200])
        time = time_match.group(1) if time_match else "TBD"
        
        matches.append({
            "team_a": team_a,
            "team_b": team_b,
            "time": time,
            "group": f"{group}组",
            "venue": "待确认"
        })
    
    return matches

def fetch_manual_schedule() -> list:
    """手动输入赛程"""
    print("\n📝 请输入比赛信息（输入空行结束）：")
    matches = []
    
    while True:
        print("\n--- 新比赛 ---")
        team_a = input("队A名称: ").strip()
        if not team_a:
            break
        team_b = input("队B名称: ").strip()
        time = input("北京时间 (如 01:00): ").strip()
        group = input("组别 (如 J组): ").strip()
        venue = input("球场: ").strip()
        
        matches.append({
            "team_a": team_a,
            "team_b": team_b,
            "time": time,
            "group": group,
            "venue": venue
        })
    
    return matches

def save_schedule(matches: list, output_path: Path):
    """保存赛程到JSON文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    print(f"✅ 赛程已保存到 {output_path}")

def main():
    config = load_config()
    source = config.get('schedule', {}).get('source', 'manual')
    group = config.get('schedule', {}).get('group', 'J')
    
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "schedule.json"
    
    if source == 'wikipedia':
        print(f"🌐 正在从Wikipedia获取{group}组赛程...")
        matches = fetch_wikipedia_schedule(group)
    else:
        matches = fetch_manual_schedule()
    
    if matches:
        save_schedule(matches, output_path)
        print(f"\n📊 共 {len(matches)} 场比赛：")
        for m in matches:
            print(f"  {m['team_a']} vs {m['team_b']} | {m['time']} | {m['group']}")
    else:
        print("❌ 未获取到比赛信息")

if __name__ == "__main__":
    main()
