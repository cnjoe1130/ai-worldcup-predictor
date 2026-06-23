#!/usr/bin/env python3
"""
AI吵个球 — 世界杯预测系统
一键生成预测卡片
"""

import sys
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

def main():
    print("⚽ AI吵个球 — 世界杯预测系统")
    print("=" * 40)
    
    # 步骤1: 获取赛程
    print("\n📅 步骤1/4: 获取赛程...")
    from fetch_schedule import main as fetch_main
    fetch_main()
    
    # 步骤2: 生成预测
    print("\n🤖 步骤2/4: 生成AI预测...")
    from generate_predictions import main as predict_main
    predict_main()
    
    # 步骤3: 生成卡片
    print("\n🎨 步骤3/4: 生成HTML卡片...")
    from generate_cards import main as cards_main
    cards_main()
    
    # 步骤4: 截图
    print("\n📸 步骤4/4: Chrome截图...")
    from screenshot import main as screenshot_main
    screenshot_main()
    
    print("\n" + "=" * 40)
    print("🎉 全部完成！")
    print(f"📁 输出目录: {Path(__file__).parent / 'output'}")
    print("\n使用方法:")
    print("  1. 打开output目录")
    print("  2. 找到.png图片")
    print("  3. 发布到小红书/朋友圈")

if __name__ == "__main__":
    main()
