#!/usr/bin/env python3
"""Static checks on docs/. Run: python3 tests/test_site.py"""
import re, json, pathlib, sys, html
D = pathlib.Path(__file__).resolve().parent.parent / 'docs'
sys.path.insert(0, str(D.parent)); from build import BASE_URL
fails, passes = [], {}
def check(name, ok, msg=''):
    passes.setdefault(name, 0)
    if ok: passes[name] += 1
    else: fails.append(f'{name}: {msg}')
pages = sorted(D.rglob('*.html'))
sitemap = open(D / 'sitemap.xml').read()
locs = set(re.findall(r'<loc>(.*?)</loc>', sitemap))
for p in pages:
    s = p.read_text(); rel = '/' + str(p.relative_to(D)).replace('index.html', '')
    body = re.sub(r'<script.*?</script>', '', s, flags=re.S)
    check('one h1', len(re.findall(r'<h1[\s>]', s)) == 1, rel)
    t = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1)); check('title < 65', len(t) < 65, f'{rel} {len(t)} {t}')
    m = re.search(r'<meta name="description" content="(.*?)"', s); dl = len(html.unescape(m.group(1))) if m else 0
    check('desc 70-160', 70 <= dl <= 160, f'{rel} {dl}')
    check('lang en', '<html lang="en">' in s, rel)
    if '404' not in rel:
        c = re.search(r'<link rel="canonical" href="(.*?)"', s); check('canonical', bool(c) and c.group(1) == BASE_URL + rel, rel)
        check('in sitemap', BASE_URL + rel in locs, rel)
        for k in ['og:title', 'og:description', 'og:image', 'twitter:card']: check('og/twitter', k in s, f'{rel} {k}')
        og = re.search(r'og:image" content="(.*?)"', s).group(1).replace(BASE_URL + '/', ''); check('og image exists', (D / og).exists(), og)
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(j); check('json-ld valid', True)
        except Exception as e: check('json-ld valid', False, f'{rel} {e}')
    nb = re.sub(r'<pre id="p-package" class="pkgtext">.*?</pre>', '', body, flags=re.S)  # verbatim original PDF text is exempt
    check('no em dash', '\u2014' not in nb and '&mdash;' not in nb, rel)
    for u in re.findall(r'(?:src|href)="([^"#]+)"', s):
        if u.startswith(('http:', 'https:', '//')):
            check('no external requests', 'rel="canonical"' in s and False if re.search(r'<(script|img|link)[^>]*(src|href)="' + re.escape(u), s) and 'canonical' not in re.search(r'<[^>]*' + re.escape(u), s).group(0) else True, f'{rel} {u}')
            continue
        if u.startswith(('mailto:',)): continue
        tgt = D / u.lstrip('/'); tgt = tgt / 'index.html' if u.endswith('/') else tgt
        check('internal links', tgt.exists(), f'{rel} -> {u}')
    for img in re.findall(r'<img[^>]*>', s):
        check('img alt/size/lazy', all(a in img for a in ['alt="', 'width=', 'height=']) and ('loading="lazy"' in img or 'fetchpriority="high"' in img), f'{rel} {img[:80]}')
    for a, b in re.findall(r'<h([1-6])', s) and zip(re.findall(r'<h([1-6])', s), re.findall(r'<h([1-6])', s)[1:]):
        check('heading order', int(b) <= int(a) + 1, f'{rel} h{a}->h{b}')
    if '/kits/' in rel and rel.count('/') == 3:
        check('kit notice', 'AI-assisted content. Check facts before you publish.' in s, rel)
        check('kit features', all(x in s for x in ['class="toc"', 'class="copy"', 'data-print', 'class="pager"', 'Related kits', 'crumbs', 'min read', '"HowTo"']), rel)
from build import KITS
for k in KITS:
    for part in ('cover', 'inside'):
        f = D / f"assets/kits/{k['slug']}-{part}.jpg"; check('kit preview images', f.exists() and f.stat().st_size > 5000, str(f))
        pg = (D / f"kits/{k['slug']}/index.html").read_text(); check('kit page shows preview', f"{k['slug']}-{part}.jpg" in pg, k['slug'])
    for idx in ['kits/index.html']: check('kit card uses cover', f"{k['slug']}-cover.jpg" in (D / idx).read_text(), k['slug'])
check('sitemap count', len(locs) == len(pages) - 1, f'{len(locs)} vs {len(pages)-1}')
check('robots', 'Sitemap:' in (D / 'robots.txt').read_text())
for js in D.rglob('*.js'): check('no network in js', not re.search(r'fetch\(|XMLHttpRequest|sendBeacon|https?://', js.read_text()), str(js))
for k, v in passes.items(): print(f'PASS-COUNT {k}: {v}')
print(f'{len(pages)} html files, {len(fails)} failures'); [print('FAIL', f) for f in fails]
sys.exit(1 if fails else 0)
