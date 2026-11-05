"""Check every internal href/src in docs/ resolves to a file (and #anchors exist)."""
import re, pathlib, html, sys
D = pathlib.Path(__file__).resolve().parent.parent / 'docs'
bad = []; n = 0
ids = {}
def target(u):
    p = D / u.lstrip('/')
    if u.endswith('/') or p.is_dir(): p = p / 'index.html'
    return p
for f in D.rglob('*.html'):
    s = f.read_text()
    for u in re.findall(r'(?:href|src|data)="([^"]+)"', s):
        u = html.unescape(u)
        if u.startswith(('http', 'mailto:', 'data:')): continue
        n += 1
        path, _, frag = u.partition('#')
        path = path.split('?')[0]
        if not path: t = f
        elif path.startswith('/'): t = target(path)
        else: t = target(str(f.parent.relative_to(D) / path))
        if not t.exists(): bad.append((str(f.relative_to(D)), u)); continue
        if frag and t.suffix == '.html':
            if t not in ids: ids[t] = set(re.findall(r'id="([^"]+)"', t.read_text()))
            if frag not in ids[t]: bad.append((str(f.relative_to(D)), u))
print(f'{n} internal links checked, {len(bad)} broken'); [print('BROKEN', a, b) for a, b in bad[:50]]
sys.exit(1 if bad else 0)
