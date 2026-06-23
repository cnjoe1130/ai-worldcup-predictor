#!/usr/bin/env python3
"""
Chrome截图脚本
将HTML卡片转换为PNG图片
"""

import subprocess
from pathlib import Path

def get_chrome_path() -> str:
    """获取Chrome浏览器路径"""
    # macOS
    mac_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if Path(mac_path).exists():
        return mac_path
    
    # Linux
    linux_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium-browser"
    ]
    for path in linux_paths:
        if Path(path).exists():
            return path
    
    # Windows
    win_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    for path in win_paths:
        if Path(path).exists():
            return path
    
    return None

def screenshot_html(html_path: Path, output_path: Path, chrome_path: str):
    """使用Chrome Headless截图"""
    cmd = [
        chrome_path,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--window-size=1080,1440",
        f"--screenshot={output_path}",
        "--hide-scrollbars",
        f"file://{html_path.absolute()}"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            print(f"  ✅ {output_path.name} ({size_kb:.0f} KB)")
            return True
        else:
            print(f"  ❌ {output_path.name} 截图失败")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ❌ {output_path.name} 截图超时")
        return False
    except Exception as e:
        print(f"  ❌ {output_path.name} 错误: {e}")
        return False

def main():
    chrome_path = get_chrome_path()
    if not chrome_path:
        print("❌ 未找到Chrome浏览器，请安装后重试")
        print("   下载地址：https://www.google.com/chrome/")
        exit(1)
    
    print(f"🌐 使用Chrome: {chrome_path}")
    
    # 输出目录
    output_dir = Path(__file__).parent.parent / "output"
    html_files = list(output_dir.glob("prediction-*.html"))
    
    if not html_files:
        print("❌ 未找到HTML卡片，请先运行 generate_cards.py")
        exit(1)
    
    print(f"\n📸 正在截图 {len(html_files)} 张卡片...")
    
    success_count = 0
    for html_path in html_files:
        png_path = html_path.with_suffix('.png')
        if screenshot_html(html_path, png_path, chrome_path):
            success_count += 1
    
    print(f"\n🎉 截图完成！成功 {success_count}/{len(html_files)} 张")
    print(f"📁 输出目录：{output_dir}")

if __name__ == "__main__":
    main()
