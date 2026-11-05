"""Compare visible main text of each original OSP page (cached HTML in /tmp/orig/cmp) with the mjd build. Usage: python3 tests/textdiff.py"""
import json, re, html, os, subprocess, pathlib, sys
R = pathlib.Path(__file__).resolve().parent.parent; C = pathlib.Path('/tmp/orig/cmp')
S = json.loads((R/'site/osp_site.json').read_text())
paths = ['', *[f'page/{i}/' for i in range(2, 9)], '50-chatgpt-video-editing-prompts-for-creators/', 'how-to-use-this-2-step-ai-automation-prompt/']
for c in S['cats']:
    n = sum(p['cat'] == c['slug'] for p in S['posts'])
    paths += [f"category/{c['slug']}/" + ('' if i == 1 else f'page/{i}/') for i in range(1, (n + 9)//10 + 1)]
paths += [p['slug'] + '/' for p in S['posts']]
IGN = re.compile(r'^(Discussion|.* says:|.* at \d+:\d+ [ap]m|Reply)$')
def txt(h):
    i = h.find('<main'); h = h[i:h.find('</main>', i)]
    h = re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', '', h, flags=re.S)
    h = re.sub(r'<(div|section|ol)[^>]*(id="(respond|comments)"|class="comment-list)[^>]*>.*', '', h, flags=re.S)
    h = re.sub(r'<nav[^>]*(pagination|pnav)[^>]*>.*?</nav>', '', h, flags=re.S)
    h = re.sub(r'<(br|/p|/h\d|/li|/div|/section|/a|/time|/span|/button|/label|/option|/figcaption|/small)[^>]*>', '\n', h)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', h))
    return [l for l in (re.sub(r'\s+', ' ', x).strip() for x in t.split('\n')) if l]
tot = miss = 0; rows = []
for p in paths:
    f = C / ('o_' + p.replace('/', '_') + '.html')
    if not f.exists(): subprocess.run(['curl', '-sL', '-o', str(f), 'https://opensourcepromptph.com/' + p])
    o = txt(f.read_text(errors='replace')); m = set(txt((R/'docs'/p/'index.html').read_text()))
    ms = [l for l in o if l not in m and not IGN.match(l)]; tot += len(o); miss += len(ms)
    if ms: rows.append((p, ms))
print(f'{len(paths)} pages, {tot} original text lines, {miss} missing on mjd')
for p, ms in rows: print('MISSING', p or '/', ms[:8])
