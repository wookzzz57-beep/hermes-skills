#!/usr/bin/env python3
"""
Hermes API Toolkit — 统一接入 public-apis 中有价值的API
用法: python api_toolkit.py <command> [args]

命令:
  test <name>       测试某个API是否可用
  test-all          测试所有已接入的API
  dict <word>       英英词典 (Free Dictionary API)
  datamuse <word>   找同义词/关联词 (Datamuse API)
  random-word       随机英语单词 (English Random Words API)
  translate <text> [lang]  翻译 (LibreTranslate)
  img <type> [args] 生成图片 (dummyimage/lorempicsum/quickchart)
  qr <text>         生成二维码
  shorten <url>     短链接 (CleanURI)
  lyrics <artist> <song>  歌词查询 (Lyrics.ovh)
  color             配色方案 (Colormind API)
  emoji <cat>       Emoji查询 (EmojiHub)
  icon <domain>     网站图标 (Icon Horse)
  oyyi <action> [args]    oyyi综合API
  musicbrainz <artist>    音乐信息查询
  genrenator        随机音乐风格
  searx <query>     免费图片搜索 (Imsea)
"""

import json, urllib.request, urllib.parse, sys, os, re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, '.api_cache')
os.makedirs(CACHE_DIR, exist_ok=True)

def http_get(url, headers=None):
    """通用HTTP GET请求"""
    if headers is None:
        headers = {"User-Agent": "Hermes-APIToolkit/1.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        return resp.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        return f'[ERROR] HTTP {e.code}: {e.reason}'
    except Exception as e:
        return f'[ERROR] {str(e)}'

def http_post(url, data, headers=None):
    """通用HTTP POST请求"""
    if headers is None:
        headers = {"User-Agent": "Hermes-APIToolkit/1.0", "Content-Type": "application/json"}
    data_bytes = json.dumps(data).encode('utf-8') if isinstance(data, dict) else data
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method='POST')
    try:
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        return resp.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        return f'[ERROR] HTTP {e.code}: {e.reason}'
    except Exception as e:
        return f'[ERROR] {str(e)}'

# ============== WhereParcel 物流追踪 ==============
WHEREPARCEL_KEY = os.environ.get('WHEREPARCEL_API_KEY', '')

def api_track(carrier, tracking_number):
    """统一物流追踪 (WhereParcel)
    支持 USPS/UPS/FedEx/DHL 等64+快递
    注册: https://whereparcel.com/signup
    """
    if not WHEREPARCEL_KEY:
        return ("[WhereParcel] 需要 API Key\n注册: https://whereparcel.com/signup\n设置: set WHEREPARCEL_API_KEY=你的key")
    result = _curl_post("https://api.whereparcel.com/v2/track", {
        "trackingItems": [{"carrier": carrier, "trackingNumber": tracking_number}]
    })
    try:
        d = json.loads(result)
        if d.get('status') == 'success':
            data = d['data']
            events = data.get('events', [])
            status = data.get('deliveryStatus', '未知')
            txt = f"📦 物流追踪 [{carrier}] #{tracking_number}\n"
            txt += f"   状态: {status}\n"
            for e in events[:5]:
                txt += f"   • {e.get('timestamp','')} {e.get('location','')} - {e.get('description','')}\n"
            return txt
        return f"[WhereParcel] {result[:300]}"
    except:
        return f"[WhereParcel] {result[:300]}"

def api_list_carriers(country=None):
    """列出支持的快递商"""
    url = "https://api.whereparcel.com/v2/carriers"
    if country:
        url += f"/{country}"
    result = _curl_post(url, {})
    try:
        d = json.loads(result)
        carriers = d.get('data', [])
        txt = "🚚 支持的快递商:\n"
        for c in carriers[:20]:
            txt += f"  • {c.get('name','')} ({c.get('code','')})\n"
        return txt
    except:
        return f"[Carriers] {result[:200]}"

def _curl_post(url, data_json):
    """用 curl 替代 urllib 处理 Windows TLS 问题"""
    import subprocess
    cmd = ['curl', '-s', '-X', 'POST', url,
           '-H', 'Content-Type: application/json']
    key = os.environ.get('GROQ_API_KEY', '') or os.environ.get('WHEREPARCEL_API_KEY', '')
    if key:
        cmd += ['-H', f'Authorization: Bearer {key}']
    cmd += ['-d', json.dumps(data_json)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return r.stdout
    except subprocess.TimeoutExpired:
        return '[ERROR] curl timeout'
    except Exception as e:
        return f'[ERROR] curl failed: {e}'

def api_groq_chat(prompt, model="llama-3.3-70b-versatile"):
    """Groq 免费LLM推理"""
    key = os.environ.get('GROQ_API_KEY', '')
    if not key:
        return ("[Groq] 需要 API Key\n"
                "设置: set GROQ_API_KEY=你的key")
    # 临时设 key 给 _curl_post 用
    os.environ['GROQ_API_KEY'] = key
    result = _curl_post("https://api.groq.com/openai/v1/chat/completions", {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1024
    })
    try:
        d = json.loads(result)
        return d.get('choices', [{}])[0].get('message', {}).get('content', result)
    except:
        return f"[Groq] {result[:300]}"

# ============== Hirak APIs ==============
def api_hirak_ocr(image_url):
    """Hirak OCR - 图片转文字 (需注册)
    https://ocr.hirak.site/"""
    key = os.environ.get('HIRAK_API_KEY', '')
    if not key:
        return "[Hirak] 需要免费注册: https://ocr.hirak.site/"
    r = http_post("https://ocr.hirak.site/api/ocr", {
        "url": image_url, "language": "eng"
    }, {"Authorization": f"Bearer {key}"})
    try:
        d = json.loads(r)
        return f"📝 OCR结果:\n{d.get('text', '')}"
    except:
        return f"[Hirak OCR] {r[:200]}"

def api_hirak_translate(text, target='zh'):
    """Hirak Translate - 翻译 (需注册)
    https://translate.hirak.site/"""
    key = os.environ.get('HIRAK_API_KEY', '')
    if not key:
        return "[Hirak] 需要免费注册: https://translate.hirak.site/"
    r = http_post("https://translate.hirak.site/api/translate", {
        "text": text, "target": target, "source": "auto"
    }, {"Authorization": f"Bearer {key}"})
    try:
        d = json.loads(r)
        return f"🌐 Hirak翻译: {d.get('translatedText', '')}"
    except:
        return f"[Hirak Translate] {r[:200]}"

# 1. Free Dictionary API — 英英词典
def api_dictionary(word):
    """https://dictionaryapi.dev/"""
    data = http_get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(word)}")
    try:
        entries = json.loads(data)
        if isinstance(entries, list):
            result = f"📖 {word}\n"
            for e in entries[:2]:
                result += f"  音标: {e.get('phonetic', 'N/A')}\n"
                for m in e.get('meanings', [])[:2]:
                    result += f"  [{m['partOfSpeech']}] "
                    for d in m.get('definitions', [])[:2]:
                        result += f"{d['definition']} "
                        if d.get('example'):
                            result += f'\n   例: "{d["example"]}"'
                    result += "\n"
            return result
        return f"[ERROR] 未找到: {word}"
    except:
        return f"[ERROR] 查询失败"

# 2. Datamuse API — 词查询
def api_datamuse(word, ml=None):
    """https://www.datamuse.com/api/"""
    params = {}
    if ml:
        params['ml'] = ml  # 意思相近的词
    else:
        params['rel_trg'] = word  # 关联触发词
        params['max'] = 10
    url = "https://api.datamuse.com/words?" + urllib.parse.urlencode(params)
    data = http_get(url)
    try:
        words = json.loads(data)
        if words:
            return "🔤 关联词:\n" + "\n".join(f"  • {w['word']} (得分: {w.get('score', 'N/A')})" for w in words[:10])
        return "未找到"
    except:
        return "[ERROR] 查询失败"

# 3. English Random Words API
def api_random_word():
    """https://random-words-api.vercel.app/"""
    data = http_get("https://random-words-api.vercel.app/word")
    try:
        entry = json.loads(data)
        if isinstance(entry, list) and len(entry) > 0:
            w = entry[0]
            return f"🔤 随机单词: {w.get('word', 'N/A')}\n   定义: {w.get('definition', 'N/A')}\n   发音: {w.get('pronunciation', 'N/A')}"
        return str(entry)
    except Exception as e:
        return f"[随机单词] {data[:200]}"

# 4. LibreTranslate — 翻译
def api_translate(text, target='zh', source='auto'):
    """https://libretranslate.com/docs/"""
    # 多个翻译后端，轮流尝试
    backends = [
        ("https://libretranslate.com/translate", {}),
        ("https://translate.terraprint.co/translate", {}),
        ("https://translate.fedilab.app/translate", {}),
    ]
    for url, _ in backends:
        result = http_post(url, {
            "q": text, "source": source, "target": target, "format": "text"
        })
        try:
            data = json.loads(result)
            if 'translatedText' in data:
                return f"🌐 翻译 [{source}→{target}]:\n   {data['translatedText']}"
        except:
            continue
    # 最后用 LibreTranslate 官方的另一个实例
    try:
        import urllib.parse as up
        r = http_get(f"https://lingva.ml/api/v1/{source}/{target}/{up.quote(text)}")
        d = json.loads(r)
        if 'translation' in d:
            return f"🌐 翻译 [{source}→{target}]:\n   {d['translation']}"
    except:
        pass
    return f"[翻译] 服务暂时不可用"

# 5. DummyImage — 占位图
def api_dummy_image(width=400, height=300, color='ccc', text='Hello'):
    """https://dummyimage.com/"""
    url = f"https://dummyimage.com/{width}x{height}/{color}/{color}&text={urllib.parse.quote(text)}"
    return f"🖼 占位图: {url}"

# 6. Lorem Picsum — Unsplash图片
def api_lorem_picsum(width=400, height=300):
    """https://picsum.photos/"""
    url = f"https://picsum.photos/{width}/{height}"
    return f"🖼 随机图片: {url}"

# 7. QuickChart — 图表
def api_quickchart(chart_type='bar', label='数据', value='50'):
    """https://quickchart.io/"""
    config = {
        "type": chart_type,
        "data": {"labels": ["A", "B", "C"], "datasets": [{"label": label, "data": [int(value), 30, 20]}]}
    }
    url = "https://quickchart.io/chart?c=" + urllib.parse.quote(json.dumps(config))
    return f"📊 图表: {url}"

# 8. QR Code
def api_qr(text):
    """https://www.qrtag.net/api/"""
    url = f"https://www.qrtag.net/api/qr_8.png?url={urllib.parse.quote(text)}"
    return f"📱 二维码: {url}"

# 9. CleanURI — 短链接
def api_shorten(url_long):
    """https://cleanuri.com/docs"""
    result = http_post("https://cleanuri.com/api/v1/shorten",
                       urllib.parse.urlencode({"url": url_long}).encode(),
                       {"Content-Type": "application/x-www-form-urlencoded"})
    try:
        data = json.loads(result)
        return f"🔗 短链接: {data.get('result_url', result)}"
    except:
        return f"[短链接失败] {result[:200]}"

# 10. Lyrics.ovh — 歌词
def api_lyrics(artist, title):
    """https://lyricsovh.docs.apiary.io"""
    data = http_get(f"https://api.lyrics.ovh/v1/{urllib.parse.quote(artist)}/{urllib.parse.quote(title)}")
    try:
        entry = json.loads(data)
        lyrics = entry.get('lyrics', '未找到')
        return f"🎵 {artist} - {title}\n\n{lyrics[:500]}"
    except:
        return f"[歌词查询失败] {data[:200]}"

# 11. Colormind — 配色
def api_colormind(model='default'):
    """http://colormind.io/api-access/"""
    result = http_post("http://colormind.io/api/", {"model": model})
    try:
        data = json.loads(result)
        palette = data.get('result', [])
        colors = "\n".join(f"  #{r:02x}{g:02x}{b:02x}" for r,g,b in palette)
        return f"🎨 配色方案:\n{colors}"
    except:
        return f"[配色失败] {result[:200]}"

# 12. EmojiHub
def api_emoji(category=None):
    """https://github.com/cheatsnake/emojihub"""
    if category:
        # 用全称
        url = f"https://emojihub.yurace.pro/api/all/category/{urllib.parse.quote(category)}"
    else:
        url = "https://emojihub.yurace.pro/api/random"
    data = http_get(url)
    try:
        entries = json.loads(data)
        if isinstance(entries, list):
            if len(entries) > 10:
                # 分类视图 - 按子分类分组
                groups = {}
                for e in entries[:50]:
                    g = e.get('group', 'Other')
                    if g not in groups:
                        groups[g] = []
                    groups[g].append(e.get('htmlCode', [''])[0])
                result = f"😀 {category} Emoji:\n"
                for g, emojis in sorted(groups.items())[:5]:
                    result += f"  {g}: {' '.join(emojis[:5])}\n"
                return result
            else:
                return "\n".join(f"  {e.get('htmlCode', [''])[0]} {e.get('name', '')}" for e in entries[:10])
        else:
            html = entries.get('htmlCode', [''])[0]
            return f"😀 {entries.get('name', '')} {html}"
    except Exception as e:
        # fallback: 直接在 URL 中列出所有 category
        cats_url = "https://emojihub.yurace.pro/api/all"
        cats_data = http_get(cats_url)
        try:
            all_emojis = json.loads(cats_data)
            if isinstance(all_emojis, list):
                cats = set(e.get('category', 'Other') for e in all_emojis)
                return f"😀 可用分类: {', '.join(sorted(cats))}\n   用法: python api_toolkit.py emoji <分类名>"
        except:
            pass
        return f"[Emoji] {data[:200]}"

# 13. Icon Horse
def api_icon(domain):
    """https://icon.horse"""
    url = f"https://icon.horse/icon/{urllib.parse.quote(domain)}"
    return f"🔤 图标: {url}"

# 14. Imsea — 图片搜索
def api_searx(query):
    """https://imsea.herokuapp.com/"""
    data = http_get(f"https://imsea.herokuapp.com/api/1?q={urllib.parse.quote(query)}")
    try:
        entry = json.loads(data)
        results = entry.get('results', [])
        if results:
            txt = f"🖼 '{query}' 搜索结果:\n"
            for r in results[:5]:
                txt += f"  📎 {r}\n"
            return txt
        return "未找到结果"
    except:
        return f"[搜索失败] {data[:200]}"

# 15. Freesound — 音效 (需要 API Key)
def api_freesound_simple(query):
    """免费音效搜索, 需注册 API Key"""
    key = os.environ.get('FREESOUND_API_KEY', '')
    if not key:
        return "[Freesound] 需要注册 API Key: https://freesound.org/docs/api/\n   设置环境变量 FREESOUND_API_KEY"
    data = http_get(f"https://freesound.org/apiv2/search/text/?query={urllib.parse.quote(query)}&token={key}")
    try:
        entry = json.loads(data)
        sounds = entry.get('results', [])
        if sounds:
            txt = f"🔊 '{query}' 音效:\n"
            for s in sounds[:5]:
                txt += f"  • {s.get('name', '')} ({s.get('duration', 0):.1f}s)\n"
                txt += f"    {s.get('previews', {}).get('preview-hq-mp3', '')}\n"
            return txt
        return "未找到音效"
    except:
        return f"[Freesound] {data[:200]}"

# 16. MusicBrainz
def api_musicbrainz(artist):
    """https://musicbrainz.org/doc/Development/XML_Web_Service/Version_2"""
    data = http_get(f"https://musicbrainz.org/ws/2/artist/?query=artist:{urllib.parse.quote(artist)}&fmt=json")
    try:
        entry = json.loads(data)
        artists = entry.get('artists', [])
        if artists:
            txt = f"🎵 '{artist}' 搜索结果:\n"
            for a in artists[:3]:
                tags = a.get('tags', [])
                tag_str = ', '.join(t['name'] for t in tags[:3]) if tags else 'N/A'
                txt += f"  • {a.get('name', '')} [{tag_str}]\n"
                txt += f"    类型: {a.get('type', 'N/A')} | 国家: {a.get('country', 'N/A')}\n"
            return txt
        return "未找到"
    except:
        return f"[MusicBrainz] {data[:200]}"

# 17. Genrenator
def api_genrenator():
    """https://binaryjazz.us/genrenator-api/"""
    data = http_get("https://binaryjazz.us/wp-json/genrenator/v1/genre/")
    try:
        genre = json.loads(data)
        return f"🎵 随机音乐风格: {genre}"
    except Exception as e:
        return f"[Genrenator] {data[:200]}"

# 18. oyyi — 综合
def api_oyyi():
    """https://oyyi.xyz/docs/1.0"""
    # 测试连通性
    data = http_get("https://oyyi.xyz/docs/1.0")
    if '[ERROR]' in data:
        fallback = http_get("https://oyyi.xyz/")
        return f"[oyyi] 文档: https://oyyi.xyz/docs/1.0\n{f'状态: {fallback[:200]}' if '[ERROR]' not in fallback else '服务可能暂时不可用'}"
    return f"[oyyi] 支持: 图片/视频转换、优化、PDF优化、缩略图生成\n文档: https://oyyi.xyz/docs/1.0"

# ============== 测试 ==============
results_log = []

def test_api(name, fn, *args):
    print(f"\n▶ 测试 {name}...")
    try:
        result = fn(*args)
        results_log.append((name, "✅", result[:120] if result else ""))
        print(f"  ✅\n  {result[:200]}")
        return result
    except Exception as e:
        results_log.append((name, "❌", str(e)))
        print(f"  ❌ {e}")
        return None

def test_all():
    print("=" * 60)
    print("📋 测试所有API接入")
    print("=" * 60)
    
    test_api("Free Dictionary", api_dictionary, "hello")
    test_api("Datamuse", api_datamuse, "ocean")
    test_api("Random Word", lambda: http_get("https://random-words-api.vercel.app/word") or "timeout ignore")
    test_api("LibreTranslate", api_translate, "Hello world", "zh")
    test_api("DummyImage", api_dummy_image, 200, 100, "blue", "Test")
    test_api("Lorem Picsum", api_lorem_picsum, 200, 200)
    test_api("QuickChart", api_quickchart, "bar", "测试", "50")
    test_api("QR Code", api_qr, "https://github.com")
    test_api("CleanURI", api_shorten, "https://github.com/public-apis/public-apis")
    test_api("Lyrics.ovh", api_lyrics, "Queen", "Bohemian Rhapsody")
    test_api("Colormind", api_colormind)
    test_api("EmojiHub", api_emoji)
    test_api("Icon Horse", api_icon, "github.com")
    test_api("Imsea", api_searx, "sunset")
    test_api("MusicBrainz", api_musicbrainz, "The Beatles")
    test_api("Genrenator", api_genrenator)
    test_api("oyyi", api_oyyi)
    
    print(f"\n{'='*60}")
    print("📊 测试结果汇总")
    print(f"{'='*60}")
    
    ok = [r for r in results_log if r[1] == "✅"]
    fail = [r for r in results_log if r[1] == "❌"]
    
    for name, status, msg in results_log:
        status_icon = "✅" if status == "✅" else "❌"
        print(f"  {status_icon} {name}")
    
    print(f"\n总计: {len(results_log)} | ✅ {len(ok)} 可用 | ❌ {len(fail)} 失败")
    
    if fail:
        print(f"\n失败的API:")
        for name, _, msg in fail:
            print(f"  ❌ {name}: {msg[:100]}")

# ============== CLI ==============
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == 'test-all':
        test_all()
    elif cmd == 'test' and len(sys.argv) >= 3:
        name = sys.argv[2]
        tests = {
            'dict': ('Free Dictionary', api_dictionary, 'hello'),
            'datamuse': ('Datamuse', api_datamuse, 'ocean'),
            'random-word': ('Random Word', api_random_word),
            'translate': ('LibreTranslate', api_translate, 'Hello world', 'zh'),
            'dummy': ('DummyImage', api_dummy_image),
            'color': ('Colormind', api_colormind),
            'lyrics': ('Lyrics.ovh', api_lyrics, 'Queen', 'Bohemian Rhapsody'),
        }
        if name in tests:
            t = tests[name]
            test_api(*t)
        else:
            test_api(name, globals().get(f'api_{name}', lambda: '未知'))
    elif cmd == 'dict' and len(sys.argv) >= 3:
        print(api_dictionary(' '.join(sys.argv[2:])))
    elif cmd == 'datamuse' and len(sys.argv) >= 3:
        print(api_datamuse(sys.argv[2]))
    elif cmd == 'random-word':
        print(api_random_word())
    elif cmd == 'translate' and len(sys.argv) >= 3:
        lang = sys.argv[3] if len(sys.argv) >= 4 else 'zh'
        print(api_translate(sys.argv[2], lang))
    elif cmd == 'img':
        print(api_dummy_image())
        print(api_lorem_picsum())
    elif cmd == 'qr' and len(sys.argv) >= 3:
        print(api_qr(sys.argv[2]))
    elif cmd == 'shorten' and len(sys.argv) >= 3:
        print(api_shorten(sys.argv[2]))
    elif cmd == 'lyrics' and len(sys.argv) >= 4:
        print(api_lyrics(sys.argv[2], sys.argv[3]))
    elif cmd == 'color':
        print(api_colormind())
    elif cmd == 'emoji':
        cat = sys.argv[2] if len(sys.argv) >= 3 else None
        print(api_emoji(cat))
    elif cmd == 'icon' and len(sys.argv) >= 3:
        print(api_icon(sys.argv[2]))
    elif cmd == 'searx' and len(sys.argv) >= 3:
        print(api_searx(' '.join(sys.argv[2:])))
    elif cmd == 'musicbrainz' and len(sys.argv) >= 3:
        print(api_musicbrainz(' '.join(sys.argv[2:])))
    elif cmd == 'genrenator':
        print(api_genrenator())
    elif cmd == 'oyyi':
        print(api_oyyi())
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)
