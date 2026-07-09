#!/usr/bin/env python3
"""
快速注册 Public APIs 的工具
运行 python register_apis.py 自动打开注册页面
"""
import webbrowser
import sys

apis = {
    "groq": {
        "name": "Groq",
        "url": "https://console.groq.com/keys",
        "desc": "免费LLM推理 (Llama/Mixtral/Gemma)",
        "steps": [
            "1. 用邮箱注册 (zhukai@weikaitechnology.com)",
            "2. 收验证码 → 登录控制台",
            "3. 点「Create API Key」→ 复制 key",
            "4. 设环境变量: set GROQ_API_KEY=你的key",
        ],
    },
    "hirak": {
        "name": "Hirak OCR + Translate",
        "url_ocr": "https://ocr.hirak.site/register",
        "url_translate": "https://translate.hirak.site/register",
        "desc": "免费无限次OCR(100+语言) + 21语翻译",
        "steps": [
            "1. 注册任意一个，同一个账号通用",
            "2. 注册后去 Dashboard 复制 API Key",
            "3. 设: set HIRAK_API_KEY=你的key",
        ],
    },
    "freesound": {
        "name": "Freesound",
        "url": "https://freesound.org/apiv2/apply/",
        "desc": "免费音效/音乐采样库",
        "steps": [
            "1. 注册 Freesound 账号",
            "2. 申请 API Key (填应用名: Hermes-APIToolkit)",
            "3. 设: set FREESOUND_API_KEY=你的key",
        ],
    },
    "aftership": {
        "name": "AfterShip",
        "url": "https://www.aftership.com/",
        "desc": "统一物流追踪 (60+快递)",
        "steps": [
            "1. 注册 AfterShip 账号",
            "2. 设置 → API → 生成 API Key",
            "3. 设: set AFTERSHIP_API_KEY=你的key",
        ],
    },
}

if len(sys.argv) > 1:
    name = sys.argv[1].lower()
    if name in apis:
        api = apis[name]
        print(f"\n{'='*50}")
        print(f"📋 {api['name']}")
        print(f"{'='*50}")
        print(f"  用途: {api['desc']}")
        print(f"\n  注册步骤:")
        for s in api['steps']:
            print(f"    {s}")
        
        # 打开注册页面
        url = api.get('url') or api.get('url_ocr', '')
        print(f"\n  正在打开注册页面: {url}")
        webbrowser.open(url)
    else:
        print(f"未知: {name}，可用: {', '.join(apis.keys())}")
else:
    print("📋 快速注册 Public APIs")
    print("=" * 50)
    for key, api in apis.items():
        print(f"\n  {key:<15} {api['name']}")
        print(f"  {'':15} {api['desc']}")
    print(f"\n用法: python register_apis.py <name>")
    print(f"示例: python register_apis.py groq")
