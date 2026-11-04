#!/usr/bin/env python3
"""Browser QA: screenshots, axe (wcag2a/aa), runtime external-request check, horizontal overflow. Usage: python3 tests/qa_browser.py http://127.0.0.1:8765/"""
import asyncio, sys, json, pathlib, re
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent; SHOTS = ROOT / 'shots'; SHOTS.mkdir(exist_ok=True)
D = ROOT / 'docs'
ALL = sorted('/' + str(p.relative_to(D)).replace('index.html', '') for p in D.rglob('*.html'))
SHOT = {'home': '/', 'kits': '/kits/', 'kit': '/kits/jeepney-history-explainer/', 'kit2': '/kits/dog-breed-explainer/', 'builder': '/builder/', 'guide': '/guides/write-a-prompt-in-3-parts/'}
AXE = next(p for p in ['/tmp/axe/axe.min.js', '/workspace/qa-3x3/site-pass2/axe.min.js'] if pathlib.Path(p).exists())
async def main(base):
    base = base.rstrip('/'); host = re.sub(r'https?://', '', base); axe = open(AXE).read(); res = {'external': [], 'overflow': [], 'axe': {}, 'console': []}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h in [(390, 844), (1366, 900)]:
            pg = await b.new_page(viewport={'width': w, 'height': h})
            pg.on('request', lambda r: res['external'].append(r.url) if host not in r.url and not r.url.startswith('data:') else None)
            pg.on('console', lambda m: res['console'].append(m.text) if m.type == 'error' else None)
            for path in ALL:
                await pg.goto(base + path); await pg.wait_for_timeout(300)
                await pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))"); await pg.wait_for_timeout(900)
                if await pg.evaluate('document.documentElement.scrollWidth>innerWidth'): res['overflow'].append(f'{w} {path}')
                await pg.add_script_tag(content=axe)
                v = await pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa']}).then(r=>r.violations.map(v=>v.id+'('+v.impact+') x'+v.nodes.length+' '+v.nodes[0].target.join(' ')))")
                if v: res['axe'][f'{w} {path}'] = v
            for name, path in SHOT.items():
                await pg.goto(base + path); await pg.wait_for_timeout(400)
                if name == 'builder': await pg.fill('#topic', 'history of the jeepney'); await pg.fill('#aud', 'Grade 6 students')
                await pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))"); await pg.wait_for_timeout(900)
                tag = 'mobile' if w == 390 else 'desktop'
                await pg.screenshot(path=str(SHOTS / f'{name}-{tag}.png'), full_page=True)
                await pg.screenshot(path=str(SHOTS / f'{name}-{tag}-fold.png'))
        await b.close()
    print(json.dumps(res, indent=1)); print('pages checked:', len(ALL))
asyncio.run(main(sys.argv[1]))
