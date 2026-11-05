#!/usr/bin/env python3
"""Build Open Source Prompt PH: site/ (content.py, css, js) -> docs/. Change BASE_URL before deploying."""
import json, shutil, pathlib, html, sys, re
from previews import render, cover_card
from PIL import Image, ImageDraw, ImageFont
BASE_URL = 'https://mjd.johnnybodegas.com'   # <- single config value for canonical, OG, sitemap
SITE_NAME = 'Open Source Prompt PH'
SRC = pathlib.Path('site'); OUT = pathlib.Path('docs')
sys.path.insert(0, str(SRC)); from content import KITS as ALL_KITS, GUIDES, DATE
KITS = [k for k in ALL_KITS if (SRC/'pdfs'/f"{k['slug']}.pdf").exists()]
NICHE = [k for k in ALL_KITS if k not in KITS]
_EX = json.loads((SRC/'osp_existing.json').read_text())
for k in KITS: k.update(_EX[k['slug']])
def short(t): return re.sub(r'\s*Creator Kit\s*-?\s*AI Prompt Framework\s*(\.pdf)?\s*$', '', t, flags=re.I).strip(' -')
OSP = json.loads((SRC/'osp_kits.json').read_text())
for o in OSP:
    o['osp'] = True; o['short'] = short(o['title'])
    o['summary'] = f"The original {o['short']} creator kit from Open Source Prompt PH. Read the full PDF text, copy it all or download the original PDF."
PDFK = sorted(KITS + OSP, key=lambda k: (k['date'], k['post_id']), reverse=True)
E = html.escape
NOTICE = 'AI-assisted content. Check facts before you publish.'
PAGES = []  # (path, title) for sitemap

def url(p): return BASE_URL.rstrip('/') + '/' + p
def words(*ts): return sum(len(str(t).split()) for t in ts)
def rtime(n): return max(1, round(n / 200))

FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def og(slug, title, kicker):
    W, H = 1200, 630; im = Image.new('RGB', (W, H), '#0a1628'); d = ImageDraw.Draw(im, 'RGBA')
    for x in range(0, W, 56): d.line([(x, 0), (x, H)], fill=(255, 255, 255, 14))
    for y in range(0, H, 56): d.line([(0, y), (W, y)], fill=(255, 255, 255, 14))
    glow = Image.new('RGBA', (W, H)); g = ImageDraw.Draw(glow)
    for r in range(320, 0, -8): g.ellipse([980 - r, -80 - r, 980 + r, -80 + r], fill=(196, 30, 58, int(5)))
    im.paste(glow, (0, 0), glow); d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle([60, 60, 1140, 570], 20, fill=(18, 35, 63, 200), outline=(255, 255, 255, 30))
    f1 = ImageFont.truetype(FB, 64); f2 = ImageFont.truetype(FB, 24); f3 = ImageFont.truetype(FR, 26)
    d.rounded_rectangle([100, 100, 100 + d.textlength(kicker.upper(), font=f2) + 36, 146], 23, fill=(196, 30, 58))
    d.text((118, 108), kicker.upper(), font=f2, fill='#fff')
    lines, cur = [], ''
    for w in title.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f1) > 980: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur); y = 190
    for l in lines[:3]: d.text((100, y), l, font=f1, fill='#f4f6fa'); y += 80
    d.text((100, 500), SITE_NAME + '  |  free prompt guides for creators', font=f3, fill='#9aa8bf')
    d.rectangle([100, 480, 220, 484], fill='#ff4d66')
    p = OUT / 'og' / f'{slug}.png'; p.parent.mkdir(exist_ok=True); im.save(p, optimize=True)
    return f'og/{slug}.png'

# Original OSP menu (same labels/order as opensourcepromptph.com), internal links rewritten to mjd; plus our Niche ideas tab
NAV = [('https://ko-fi.com/opensourcepromptphpremium/shop', 'Premium niche'), ('50-chatgpt-video-editing-prompts-for-creators/', 'Video editing guide'),
       ('how-to-use-this-2-step-ai-automation-prompt/', 'Instructions'), ('#guides', 'Explore prompts'), ('#workshop', 'Prompt workshop'),
       ('https://www.google.com/search?q=site:+https://mjd.johnnybodegas.com', 'Search via google'), ('https://www.facebook.com/groups/890192480414598', 'Facebook community')]
EXTRA_NAV = [('niche-ideas/', 'Niche ideas')]
FOOT_EXTRA = [('kits/', 'Kits library'), ('niche-ideas/', 'Niche ideas'), ('guides/', 'Guides'), ('builder/', 'Builder'), ('about/', 'About'), ('privacy/', 'Privacy')]
def href(p): return p if p.startswith('http') else '/' + p
def layout(path, title, desc, body, crumbs=None, ld=None, og_slug='home', og_kicker='Open Source Prompt PH', mbar=True, robots=None, og_override=None, extra_js='', full_title=None):
    full = title if len(title) <= 40 else title
    t = f'{full} | {SITE_NAME}' if path else f'{SITE_NAME}: Free AI Prompt Kits for Creators'
    if len(t) > 64: t = full
    if full_title: t = full_title
    ogimg = og_override or og(og_slug, title if path else 'Free AI prompt kits for Filipino creators', og_kicker)
    ld = list(ld or [])
    ld.insert(0, {"@context": "https://schema.org", "@type": "Organization", "name": SITE_NAME, "url": url(''), "logo": url('og/home.png')})
    if not path: ld.insert(0, {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": url(''), "inLanguage": "en"})
    crumbs_html = ''
    if crumbs:
        items = [('', 'Home')] + crumbs
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (p, n) in enumerate(items)]})
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + ''.join(
            (f'<li><a href="/{p}">{E(n)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{E(n)}</li>') for i, (p, n) in enumerate(items)) + '</ol></nav>'
    body = body.replace('{{crumbs}}', crumbs_html)
    cur = 'niche-ideas/' if any(path == f"kits/{k['slug']}/" for k in NICHE) else path
    navh = ''.join(f'<li><a href="{href(p)}"{" aria-current=page" if (p == cur and not p.startswith(("http", "#"))) else ""}>{n}</a></li>' for p, n in NAV + EXTRA_NAV)
    footh = ''.join(f'<li><a href="{href(p)}">{n}</a></li>' for p, n in NAV)
    foot2 = ''.join(f'<li><a href="/{p}">{n}</a></li>' for p, n in FOOT_EXTRA)
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    mb = '<div class="mbar" aria-hidden="false"><a class="btn pri" href="/kits/">Browse kits</a><a class="btn" href="/builder/">Build a prompt</a></div>' if mbar else ''
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(t)}</title><meta name="description" content="{E(desc)}">
{f'<meta name="robots" content="{robots}">' if robots else f'<link rel="canonical" href="{url(path)}">'}
<meta name="theme-color" content="#0a1628">
<meta property="og:type" content="{'article' if path.count('/') > 1 else 'website'}"><meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{E(t)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url(path)}">
<meta property="og:image" content="{url(ogimg)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="{800 if og_override else 630}"><meta property="og:image:alt" content="{E(title)} cover card">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(t)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{url(ogimg)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/css/style.css">{lds}
</head><body><a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="in"><a class="brand" href="/" aria-label="{SITE_NAME} home"><i aria-hidden="true"></i><span><b class="bn">Open Source Prompt <em>PH</em></b><small>THE CREATOR’S FIELD GUIDE</small></span></a>
<button class="menubtn" type="button" aria-expanded="false" aria-controls="mainnav">Menu</button>
<nav class="main" id="mainnav" aria-label="Main navigation"><ul>{navh}</ul></nav></div></header>
<main id="main">{body}</main>
<footer class="site"><div class="wrap"><a class="fbrand" href="/">Free AI Prompts &amp; Creator Kits | {SITE_NAME}</a>
<nav aria-label="Footer navigation"><ul>{footh}</ul><ul class="foot2">{foot2}</ul></nav>
<p>© 2026 Free AI Prompts &amp; Creator Kits | {SITE_NAME} · Practical ideas, thoughtfully explained.</p><p class="muted">Static copy hosted at mjd.johnnybodegas.com. No tracking, no accounts.</p></div></footer>
{mb}<script src="/js/app.js" defer></script>{extra_js}</body></html>'''
    out = OUT / path / 'index.html' if path != '404.html' else OUT / '404.html'
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(doc)
    if not robots: PAGES.append(path)

def hero(h1, lead, kicker='', extra='', small=True):
    return f'''<section class="hero{' sm' if small else ''}"><div class="gridbg" aria-hidden="true"></div><div class="orb o1" aria-hidden="true"></div><div class="orb o2" aria-hidden="true"></div>
<div class="wrap">{{{{crumbs}}}}{f'<span class="pill"><b></b>{kicker}</span>' if kicker else ''}<h1>{h1}</h1><p class="lead">{lead}</p>{extra}</div></section>'''

def kitcard(k, lvl='h3'):
    text = E((k['title'] + ' ' + k['summary'] + ' ' + k['cat']).lower())
    return f'''<div class="rv" data-kit data-cat="{E(k['cat'])}" data-text="{text}"><a class="card kitcard" href="/kits/{k['slug']}/">
<img src="/assets/kits/{k['slug']}-cover.jpg" alt="Preview of the {E(k['title'])} printable cover page, with its illustration" width="1200" height="800" loading="lazy" decoding="async">
<span class="tag">{E(k['cat'])}</span><{lvl}>{E(k['title'])}</{lvl}><p>{E(k['summary'])}</p></a></div>'''

def pblock(id_, label, text):
    return f'<div class="pblock"><div class="ph"><span>{E(label)}</span><button class="copy" type="button" data-target="{id_}" aria-label="Copy {E(label)} prompt">Copy</button></div><pre id="{id_}">{E(text)}</pre></div>'

STEPS = '''<ol class="steps"><li><span>STEP 1</span><strong>Get the idea</strong><p>Pick a kit or a topic you care about.</p></li><li><span>STEP 2</span><strong>Make it yours</strong><p>Swap the placeholders for your topic and audience.</p></li><li><span>STEP 3</span><strong>Review the output</strong><p>Read it, then check every fact.</p></li><li><span>STEP 4</span><strong>Refine and repeat</strong><p>Ask for changes to only the parts you want.</p></li></ol>'''


def package_text(k):
    L=[k['title'].upper(), SITE_NAME+' | '+k['cat']+' kit', '', 'OVERVIEW', k['summary'], k['why'], '',
       'PROMPT FRAMEWORK (replace anything in square brackets)', '', '01 ROLE', k['role'], '', '02 CONTEXT', k['context'], '', '03 OUTPUT', k['output'], '',
       'FULL PROMPT (copy and paste this)', k['role'], k['context'], k['output'], '', 'EXAMPLE PROMPTS']
    for t,x in k['examples']: L+=['', t, x]
    L+=['', 'HOW TO ADAPT IT']+[f'{i+1}. {a}' for i,a in enumerate(k['adapt'])]
    L+=['', 'FACT CHECK CHECKLIST']+['- '+c for c in k['checks']]
    L+=['', NOTICE, 'Free at mjd.johnnybodegas.com']
    return '\n'.join(L)

def make_pdf(k, path):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
    from reportlab.lib import colors
    H=ParagraphStyle('h',fontName='Helvetica-Bold',fontSize=20,leading=24,textColor=colors.HexColor('#0a1628'),spaceAfter=4)
    S=ParagraphStyle('s',fontName='Helvetica',fontSize=10,textColor=colors.grey,spaceAfter=10)
    H2=ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=12,leading=15,textColor=colors.HexColor('#b3202a'),spaceBefore=12,spaceAfter=4)
    P=ParagraphStyle('p',fontName='Helvetica',fontSize=10.5,leading=14.5,spaceAfter=4)
    import html as _h, textwrap
    def para(t): return Paragraph(_h.escape(t).replace('\n','<br/>'),P)
    def box(t):
        from reportlab.platypus import Table, TableStyle
        pre=Paragraph(_h.escape(t).replace('\n','<br/>'),ParagraphStyle('b',fontName='Courier',fontSize=9.5,leading=13))
        tb=Table([[pre]],colWidths=[170*mm]); tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#f1f3f7')),('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#c9ced8')),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)])); return tb
    full=f"{k['role']}\n{k['context']}\n{k['output']}"
    st=[Paragraph(_h.escape(k['title']),H),Paragraph(SITE_NAME+' | '+_h.escape(k['cat'])+' kit',S),
        Paragraph('Overview',H2),para(k['summary']),para(k['why']),
        Paragraph('Prompt framework (replace anything in square brackets)',H2),
        Paragraph('01 Role',P),box(k['role']),Spacer(1,4),Paragraph('02 Context',P),box(k['context']),Spacer(1,4),Paragraph('03 Output',P),box(k['output']),
        Paragraph('Full prompt (copy and paste this)',H2),box(full),Paragraph('Example prompts',H2)]
    for t,x in k['examples']: st+=[Paragraph(_h.escape(t),P),box(x),Spacer(1,4)]
    st+=[Paragraph('How to adapt it',H2)]+[para(f'{i+1}. {a}') for i,a in enumerate(k['adapt'])]
    st+=[Paragraph('Fact check checklist',H2)]+[para('- '+c) for c in k['checks']]
    st+=[Spacer(1,10),Paragraph(_h.escape(NOTICE),S),Paragraph('Free at mjd.johnnybodegas.com',S)]
    def foot(c,d):
        c.setFont('Helvetica',8); c.setFillColor(colors.grey); c.drawString(20*mm,10*mm,SITE_NAME+' | '+k['title']); c.drawRightString(190*mm,10*mm,'Page %d'%d.page)
    SimpleDocTemplate(str(path),pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=18*mm,bottomMargin=18*mm,title=k['title'],author=SITE_NAME).build(st,onFirstPage=foot,onLaterPages=foot)

def attach_html(slug):
    fs = [f for p in OSPS['posts'] if p['kit'] == slug for f in p['files'] if f['kind'] == 'file']
    seen = {}; [seen.setdefault(f['path'], f) for f in fs]
    if not seen: return ''
    return '<p class="orig"><strong>Also attached to the original post:</strong> ' + ', '.join(f'<a href="{f["path"]}" download="{E(f["name"])}">{E(f["name"])}</a>' for f in seen.values()) + '</p>'
def osp_page(k, prev, nxt, rel):
    (OUT/'downloads').mkdir(exist_ok=True)
    shutil.copyfile(SRC/'pdfs'/f"{k['slug']}.pdf", OUT/'downloads'/f"{k['slug']}.pdf")
    dlname = (SRC/'pdfs'/f"{k['slug']}.name").read_text().strip()
    ptext = (SRC/'pdf_text'/f"{k['slug']}.txt").read_text(encoding='utf-8')
    otitle = (SRC/'pdfs'/f"{k['slug']}.title").read_text(encoding='utf-8').strip()
    if len(ptext.strip()) > 50:
        box = f'<pre id="p-package" class="pkgtext">{E(ptext)}</pre>'; pintro = 'This is the complete text of the PDF; downloading gives you the original file.'
    else:
        box = '<pre id="p-package" class="pkgtext">This PDF has no extractable text (it may be scanned images). Use Download PDF for the original file.</pre>'; pintro = 'No text could be extracted from this PDF. The download is the original file.'
    n = words(ptext)
    pkg = f'''<section class="pkg" id="package" aria-labelledby="pkg-h"><h2 id="pkg-h">Full package: complete text of the PDF</h2><p>{pintro}</p><p class="orig"><strong>Original title:</strong> {E(otitle)}<br><strong>Original:</strong> {E(otitle)} ({E(dlname)})</p>{attach_html(k["slug"])}
<div class="pblock"><div class="ph"><span>{E(k['short'])} (full text)</span><span class="pb"><button class="copy" type="button" data-target="p-package" aria-label="Copy the whole package">Copy all</button><a class="dl" href="/downloads/{k['slug']}.pdf" download="{E(dlname)}">Download PDF</a></span></div>{box}</div></section>'''
    art = f'''<article class="prose">{pkg}<p class="notice" role="note">{NOTICE}</p>
<p>New to these kits? Read <a href="/guides/adapt-a-kit-to-your-project/">how to adapt a kit to your project</a> and <a href="/guides/fact-check-ai-output/">how to fact-check AI output</a>.</p>
<nav class="pager" aria-label="More kits"><a class="card prev" href="/kits/{prev['slug']}/"><small>Previous kit</small>{E(prev.get('short', prev['title']))}</a><a class="card next" href="/kits/{nxt['slug']}/"><small>Next kit</small>{E(nxt.get('short', nxt['title']))}</a></nav>
<section class="related" aria-labelledby="rel"><h2 id="rel">Related kits</h2><div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">{''.join(kitcard(x) for x in rel)}</div></section></article>'''
    tools = f'<div class="tools"><a class="btn pri" href="/downloads/{k['slug']}.pdf" download="{E(dlname)}">Download PDF</a><button class="btn" type="button" data-print>Print</button><a class="btn" href="/kits/">All kits</a></div>'
    body = hero(E(k['title']), E(k['summary']), E(k['cat']) + ' kit', f'<div class="meta"><span>{rtime(n)} min read</span><span>Posted {k["date"][:10]}</span><span>{k["pages"]} page PDF</span></div><p class="notice" role="note">{NOTICE}</p>{tools}') + \
        f'<div class="wrap layout"><nav class="toc" aria-label="On this page"><strong>On this page</strong><ol><li><a href="#package">Full package</a></li><li><a href="#rel">Related kits</a></li></ol></nav>{art}</div>'
    cw = {"@context": "https://schema.org", "@type": "CreativeWork", "name": k['title'], "description": k['summary'], "inLanguage": "en", "datePublished": k['date'][:10], "image": url(f"assets/kits/{k['slug']}-cover.jpg"), "encoding": {"@type": "MediaObject", "encodingFormat": "application/pdf", "contentUrl": url(f"downloads/{k['slug']}.pdf")}, "isBasedOn": "https://opensourcepromptph.com/?p=" + str(k['post_id'])}
    layout(f"kits/{k['slug']}/", k['short'], k['summary'][:158], body, crumbs=[('kits/', 'Kits'), (f"kits/{k['slug']}/", k['short'])], ld=[cw], og_slug='kit-' + k['slug'], og_kicker=k['cat'] + ' kit', og_override=f"assets/kits/{k['slug']}-cover.jpg")


# ---------- Original-site replica (opensourcepromptph.com structure) ----------
OSPS = json.loads((SRC/'osp_site.json').read_text())
OSP_POSTS = sorted(OSPS['posts'], key=lambda p: (p['date'], p['id']), reverse=True)
OSP_CATS = sorted(OSPS['cats'], key=lambda c: c['name'])
OSP_PAGES = json.loads((SRC/'osp_pages.json').read_text())
_KN = {}
def kit_pdf_name(slug): return (SRC/'pdfs'/f'{slug}.name').read_text().strip()
import datetime as _dt
def hdate(d): x = _dt.date.fromisoformat(d[:10]); return f'{x.strftime("%B")} {x.day}, {x.year}'
def pshort(t): return short(t.replace('.pdf', '').strip())
PER = 10

def search_form(q='', cur_cat=''):
    chips = ''.join(
        f'<a class="chip" href="/category/{c["slug"]}/"{" aria-current=page" if c["slug"] == cur_cat else ""}>{E(c["name"])}</a>'
        for c in OSP_CATS)
    return f'''<form role="search" method="get" class="search-form" action="/search/"><label class="vh" for="site-search">Search articles</label><input class="search" type="search" id="site-search" name="s" placeholder="Search articles…" value="{E(q)}"><button class="btn pri" type="submit">Search</button></form>
<div class="filters" role="navigation" aria-label="Categories">{chips}</div>'''

def pcard(p, lvl='h3'):
    return f'''<article class="card pcard" data-post><div class="kicker">{E(p['catname'])}</div><{lvl}><a href="/{p['slug']}/">{E(p['title'].strip())}</a></{lvl}><p></p><a class="more" href="/{p['slug']}/">Read article ↗</a><div class="pmeta"><span>Partee88</span><time datetime="{p['date']}">{hdate(p['date'])}</time></div></article>'''

def pager(base, cur, total):
    if total <= 1: return ''
    u = lambda n: base if n == 1 else f'{base}page/{n}/'
    show = sorted({1, total, cur - 1, cur, cur + 1} & set(range(1, total + 1))); out = []; last = 0
    if cur > 1: out.append(f'<a href="{u(cur - 1)}">Previous</a>')
    for n in show:
        if n - last > 1: out.append('<span>…</span>')
        out.append(f'<span aria-current="page">{n}</span>' if n == cur else f'<a href="{u(n)}">{n}</a>'); last = n
    if cur < total: out.append(f'<a href="{u(cur + 1)}">Next</a>')
    return f'<nav class="pnav" aria-label="Posts pagination"><h2 class="vh">Posts pagination</h2>{"".join(out)}</nav>'

def reading_room(posts, base, cur, total, h='h2', head='Explore the latest articles.', q='', cur_cat=''):
    return f'''<section class="wrap sec" id="guides"><div class="kicker">The creator’s reading room</div><{h}>{E(head)}</{h}>{search_form(q, cur_cat)}
<div class="grid pgrid">{''.join(pcard(p, 'h2' if h == 'h1' else 'h3') for p in posts)}</div>{pager(base, cur, total)}</section>'''

def home_top():
    sl = OSPS['slides']
    slides = ''.join(f'''<a class="slide{' on' if i == 0 else ''}" href="/{x['post_slug']}/" aria-label="{E(x['title'])} — open AI prompt creator kit"{'' if i == 0 else ' aria-hidden="true" tabindex="-1" inert'}><img src="/assets/osp/{x['img']}" alt="{E(x['alt'])}" width="1280" height="720" {'fetchpriority="high"' if i == 0 else 'loading="lazy"'} decoding="async"><span class="scopy"><span class="slabel">{E(x['label'])}</span><h2>{E(x['title'])}</h2><span class="sdesc">{E(x['desc'])}</span><span class="scta">Explore this prompt <span aria-hidden="true">↗</span></span></span></a>''' for i, x in enumerate(sl))
    car = f'''<section class="wrap featured" aria-label="Featured prompt creator kits"><div class="fhead"><span>Five featured creator kits</span><span>Find your next idea ↗</span></div>
<div class="carousel" id="carousel" role="region" aria-roledescription="carousel" aria-label="Featured AI prompt creator kits"><div class="stage">{slides}</div>
<div class="cctl"><span class="ccount" aria-live="polite">01 / {len(sl):02d}</span><button type="button" class="cbtn" data-c="pause">Pause</button><button type="button" class="cbtn" data-c="prev" aria-label="Previous slide">←</button><button type="button" class="cbtn" data-c="next" aria-label="Next slide">→</button></div></div>
<p class="fnote">AI-generated artwork · Click any slide to open its prompt kit</p></section>'''
    hero_ = f'''<section class="hero"><div class="gridbg" aria-hidden="true"></div><div class="orb o1" aria-hidden="true"></div><div class="orb o2" aria-hidden="true"></div><div class="wrap hgrid"><div class="rv"><span class="pill"><b></b>A little direction. A better creation.</span>
<h1>Better prompts.<br><span class="grad">More possibilities.</span></h1><p class="lead">Practical AI guides for curious creators. Learn the process, understand the prompt, and make something of your own.</p>
<div class="ctas"><a class="btn pri" href="#guides">Explore the guides ↗</a><a class="btn" href="/how-to-use-this-2-step-ai-automation-prompt/">Watch the 3-step guide ↗</a></div><p class="muted hnote">For beginners and makers · Clear examples · No sign-up</p></div>
<div class="card glow rv" id="notebook"><div class="nb-head"><span>THE PROMPT NOTEBOOK</span><span>FIELD NOTE / 01</span></div><p class="kicker">From vague idea to clear brief</p><h2 style="margin:4px 0 12px;font-size:22px">Give your idea a little structure.</h2>
<div class="part on"><span class="pl">01 / ROLE</span><br>Act as an educational content editor.</div><div class="part on"><span class="pl">02 / CONTEXT</span><br>Explain a topic to a curious beginner.</div><div class="part on"><span class="pl">03 / OUTPUT</span><br>One clear explanation. One useful example.</div><p class="nbfoot"><span>Make it specific. Make it yours.</span><span aria-hidden="true">↗</span></p></div></div></section>
<div class="wrap principles"><span><b>01</b> Understand the process</span><span><b>02</b> Adapt the example</span><span><b>03</b> Check the result</span><span><b>04</b> Keep improving</span></div>'''
    return car + hero_

WORKSHOP = '''<section class="wrap sec" id="workshop"><div class="learn card"><div><div class="kicker">The prompt workshop</div><h2>Your idea.<br>A clearer starting point.</h2><p>A useful prompt explains the task, the audience, and what a good result should contain. Try the builder, then adapt the brief to your project.</p>
<ol class="wsteps"><li><b>1</b><span>Choose one specific topic and an output format.</span></li><li><b>2</b><span>Copy the brief into your preferred AI tool.</span></li><li><b>3</b><span>Check accuracy and revise before you publish.</span></li></ol></div>
<div class="wbuilder"><label for="topic">What are you creating about?</label><input class="search" id="topic" value="The history of the Philippine jeepney" maxlength="200"><label for="format">Choose your format</label><select class="search" id="format"><option>60-second video outline</option><option>beginner-friendly article outline</option><option>five-slide educational carousel</option></select><label for="prompt-output">Your editable prompt</label><textarea class="search" id="prompt-output" rows="8"></textarea><button class="btn pri" id="copy-prompt" type="button">Copy prompt ↗</button><span id="copy-status" class="status" role="status" aria-live="polite"></span><p class="muted" style="font-size:14px">Runs in your browser. Your topic is not sent to an AI service.</p></div></div></section>'''
WJS = '<script src="/js/osp.js" defer></script>'
HOME_DESC = 'Explore free AI prompts, video editing workflows, and downloadable PDF creator kits for image generation, storytelling, and educational content.'

REPL = '<!-- osp-replica: text copied verbatim from opensourcepromptph.com -->'
def osp_site():
    total = (len(OSP_POSTS) + PER - 1) // PER
    for n in range(1, total + 1):
        posts = OSP_POSTS[(n - 1) * PER:n * PER]
        body = REPL + home_top() + reading_room(posts, '/', n, total) + WORKSHOP
        path = '' if n == 1 else f'page/{n}/'
        ft = 'Free AI Prompts & Creator Kits | Open Source Prompt PH' + ('' if n == 1 else f' – Page {n}')
        layout(path, 'Free AI Prompts & Creator Kits' + ('' if n == 1 else f' – Page {n}'), HOME_DESC, body, og_slug='home', extra_js=WJS, full_title=ft[:64] if n == 1 else f'Free AI Prompts & Creator Kits – Page {n} | OSP PH')
    # categories
    for c in OSP_CATS:
        cp = [p for p in OSP_POSTS if p['cat'] == c['slug']]; tot = (len(cp) + PER - 1) // PER
        for n in range(1, tot + 1):
            base = f"category/{c['slug']}/"; path = base if n == 1 else f'{base}page/{n}/'
            body = '<div class="sp"></div>' + reading_room(cp[(n - 1) * PER:n * PER], '/' + base, n, tot, 'h1', f"Category: {c['name']}", cur_cat=c['slug'])
            layout(path, f"Category: {c['name']}" + ('' if n == 1 else f' – Page {n}'), f"Open Source Prompt PH articles in the {c['name']} category: {len(cp)} AI prompt creator kits with original PDF downloads.", body, crumbs=None, og_slug='cat-' + c['slug'], og_kicker='Category')
    # search (client side; the original uses WordPress ?s=)
    idx = [{"t": p['title'].strip(), "u": f"/{p['slug']}/", "c": p['catname'], "d": p['date'], "h": hdate(p['date'])} for p in OSP_POSTS]
    body = '<div class="sp"></div>' + f'''<section class="wrap sec" id="guides"><div class="kicker">The creator’s reading room</div><h1 id="sh">Search</h1>{search_form()}<div class="grid pgrid" id="sresults">{''.join(pcard(p, 'h2') for p in OSP_POSTS)}</div><p id="noresults" hidden>No matching articles. Try another search or return to the <a href="/">homepage</a>.</p></section><script type="application/json" id="sindex">{json.dumps(idx, ensure_ascii=False)}</script>'''
    layout('search/', 'Search Results', 'Search the Open Source Prompt PH articles: AI prompt creator kits, video editing guides and step by step instructions.', body, og_slug='search', extra_js=WJS)
    # WP pages
    for pg in OSP_PAGES:
        html_ = (SRC/'osp_pages'/f"{pg['slug']}.html").read_text()
        html_ = re.sub(r'<h1 class="wp-block-heading">(.*?)</h1>', r'<p class="lead"><strong>\1</strong></p>', html_, flags=re.S)
        body = REPL + f'<div class="wrap narrow"><article class="article prose wpc"><a href="/">← Home</a><h1>{E(pg["title"])}</h1>{html_}</article></div>'
        d = pg['excerpt'][:155].rsplit(' ', 1)[0] + '...'
        layout(pg['slug'] + '/', pg['title'], d, body, og_slug='page-' + pg['slug'], og_kicker='Guide')
    # posts (one page per original post; links into the kit page with full text)
    chron = sorted(OSP_POSTS, key=lambda p: (p['date'], p['id']))
    for i, p in enumerate(chron):
        k = p['kit']; t = p['title'].strip(); nm = p['pdf_name']
        fblocks = ''.join(f'''<div class="fileblock"><object class="pdfembed" data="/downloads/{k}.pdf" type="application/pdf" aria-label="Embed of {E(f['label'])}."></object><a href="/downloads/{k}.pdf">{E(f['label'])}</a> <a class="btn pri" href="/downloads/{k}.pdf" download="{E(nm)}">Download</a></div>''' if f['kind'] == 'pdf' else f'''<div class="fileblock"><a href="{f['path']}">{E(f['label'])}</a> <a class="btn" href="{f['path']}" download="{E(f['name'])}">Download</a></div>''' for f in p['files'])
        prv = chron[i - 1] if i > 0 else None; nxt = chron[i + 1] if i + 1 < len(chron) else None
        nav = '<nav class="postnav" aria-label="Posts"><h2 class="vh">Post navigation</h2>' + (f'<a class="card" rel="prev" href="/{prv["slug"]}/"><small>Previous</small>{E(prv["title"].strip())}</a>' if prv else '<span></span>') + (f'<a class="card" rel="next" href="/{nxt["slug"]}/"><small>Next</small>{E(nxt["title"].strip())}</a>' if nxt else '') + '</nav>'
        body = f'''<div class="wrap narrow"><article class="article prose"><a href="/">← Home</a><h1>{E(t)}</h1><div class="pmeta">By <span>Partee88</span>{E(p['meta'].split('Partee88', 1)[1])}</div>
{fblocks}
<p class="note"><strong>Full package text and Copy all:</strong> <a href="/kits/{k}/">open the kit page</a> to read the complete PDF text in the browser.</p>
{nav}<p class="muted">Comments are not available on this copy of the site.</p></article></div>'''
        st = pshort(t); ft = (st if len(st) <= 40 else st[:40].rsplit(' ', 1)[0]) + ' | Open Source Prompt PH'
        d = f'{st}: original AI prompt creator kit PDF from Open Source Prompt PH. Download the PDF or read its full text.'
        if len(d) > 158: d = d[:155].rsplit(' ', 1)[0] + '...'
        layout(p['slug'] + '/', st, d, body, og_slug='kit-' + k, og_kicker='Creator kit', og_override=f'assets/kits/{k}-cover.jpg', full_title=ft)

def osp_404():
    body = REPL + '''<section class="hero sm"><div class="gridbg" aria-hidden="true"></div><div class="wrap"><span class="pill"><b></b>PAGE NOT FOUND</span><p class="big404" aria-hidden="true">404</p><h1>This prompt led nowhere.</h1><p class="lead">The page may have moved, but your next idea is still here. Let’s get you back to creating.</p><div class="ctas"><a class="btn pri" href="/#guides">Explore AI Prompts →</a><a class="btn" href="/">Back to Home</a></div></div></section>'''
    layout('404.html', 'Page not found', 'This page could not be found. Explore the free AI prompts on Open Source Prompt PH or go back to the homepage.', body, robots='noindex', mbar=False, full_title='404 — Page not found | Open Source Prompt PH')

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(); (OUT / 'CNAME').write_text('mjd.johnnybodegas.com\n'); (OUT / '.nojekyll').write_text(''); shutil.copytree(SRC / 'css', OUT / 'css'); shutil.copytree(SRC / 'js', OUT / 'js')
    (OUT / 'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="9" fill="#c41e3a"/><text x="16" y="22" font-family="monospace" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">&gt;_</text></svg>')
    for k in ALL_KITS: render(k, SRC / 'assets/kits')
    for k in OSP: cover_card(k, SRC / 'assets/kits')
    shutil.copytree(SRC / 'assets', OUT / 'assets'); shutil.copytree(SRC / 'files', OUT / 'files')
    cats = sorted({k['cat'] for k in PDFK})
    osp_site()
    # KITS INDEX
    chips = '<button class="chip" type="button" data-cat="All" aria-pressed="true">All</button>' + ''.join(f'<button class="chip" type="button" data-cat="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in cats)
    body = hero('Creator kits', 'Original prompt frameworks for explainers, scripts and image series. Search by topic or filter by category.', 'Kits library') + f'''
<section class="sec" style="padding-top:44px"><div class="wrap"><label class="lbl" for="q">Search kits</label><input class="search" id="q" type="search" placeholder="Try: space, dog, logo" autocomplete="off">
<div class="filters" role="group" aria-label="Filter by category">{chips}</div><p class="count" id="count" aria-live="polite">{len(PDFK)} kits</p>
<div class="grid" id="kitgrid">{''.join(kitcard(k, 'h2') for k in PDFK)}</div><div class="ctas"><button class="btn" type="button" id="more" hidden>Show more kits</button></div></div></section>'''
    il = {"@context": "https://schema.org", "@type": "ItemList", "name": "Creator kits", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": url(f"kits/{k['slug']}/"), "name": k['title']} for i, k in enumerate(PDFK)]}
    layout('kits/', 'Creator Kits: Free AI Prompt Frameworks', f'Browse {len(PDFK)} free Open Source Prompt PH creator kits with full PDF text and downloads: animals, space, history, health, maps, military and more.', body, crumbs=[('kits/', 'Kits')], ld=[il], og_slug='kits', og_kicker='Kits library')
    # KIT PAGES
    nbody = hero('Niche ideas', 'Starter niche ideas written for this site. These are not from the original PDF kits.', 'Other niche options') + f'''
<section class="sec" style="padding-top:44px"><div class="wrap"><p class="muted">Each idea has a site-written prompt framework, examples and a fact check list you can adapt. For the original kits with PDFs, see <a href="/kits/">Kits</a>.</p>
<div class="grid">{''.join(kitcard(k, 'h2') for k in NICHE)}</div></div></section>'''
    nil = {"@context": "https://schema.org", "@type": "ItemList", "name": "Niche ideas", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": url(f"kits/{k['slug']}/"), "name": k['title']} for i, k in enumerate(NICHE)]}
    layout('niche-ideas/', 'Niche Ideas: Starter Prompt Ideas', 'Starter niche ideas written for this site: jeepney history, Filipino street food and Philippine festivals. Not from the original PDF kits.', nbody, crumbs=[('niche-ideas/', 'Niche ideas')], ld=[nil], og_slug='niche-ideas', og_kicker='Niche ideas')
    for GROUP in (PDFK, NICHE):
      isn = GROUP is NICHE
      for i, k in enumerate(GROUP):
        prev, nxt = GROUP[i - 1], GROUP[(i + 1) % len(GROUP)]
        rel = [x for x in GROUP if x['cat'] == k['cat'] and x is not k][:3]
        rel += [x for x in GROUP if x not in rel and x is not k and x not in (prev, nxt)][:3 - len(rel)]
        if k.get('osp'):
            osp_page(k, prev, nxt, rel); continue
        n = words(k['summary'], k['why'], k['role'], k['context'], k['output'], *[e[1] for e in k['examples']], *k['adapt'], *k['checks']) + 150
        toc = [('package', 'Full package'), ('overview', 'Overview'), ('framework', 'Prompt framework'), ('examples', 'Example prompts'), ('adapt', 'How to adapt it'), ('fact-check', 'Fact check checklist')]
        full = f"{k['role']}\n{k['context']}\n{k['output']}"
        (OUT/'downloads').mkdir(exist_ok=True)
        orig = SRC/'pdfs'/f"{k['slug']}.pdf"
        if orig.exists():
            shutil.copyfile(orig, OUT/'downloads'/f"{k['slug']}.pdf")
            dlname = (SRC/'pdfs'/f"{k['slug']}.name").read_text().strip()
            ptext = (SRC/'pdf_text'/f"{k['slug']}.txt").read_text(encoding='utf-8')
            phead = 'Full package: complete text of the PDF'
            pintro = 'This is the complete text of the PDF; downloading gives you the original file.'
            tfile = SRC/'pdfs'/f"{k['slug']}.title"
            osp_title = tfile.read_text(encoding='utf-8').strip() if tfile.exists() else dlname
            orig_line = f'<p class="orig"><strong>Original title:</strong> {E(osp_title)}<br><strong>Original:</strong> {E(osp_title)} ({E(dlname)})</p>' + attach_html(k['slug'])
            guide = '<p class="note"><strong>Simplified starter guide.</strong> The sections below are a simplified starter guide written for this site, not the PDF. The full PDF text is above.</p>'
        else:
            make_pdf(k, OUT/'downloads'/f"{k['slug']}.pdf")
            dlname = f"{k['slug']}.pdf"; ptext = package_text(k)
            phead = 'Full package (site-written)'
            pintro = 'This kit has no original PDF yet. This text and PDF were written for this site from the guide below; they are not an original kit PDF.'
            orig_line = '<p class="orig"><strong>Site-written kit.</strong> No original Open Source Prompt PH PDF is attached to this page.</p>'
            guide = ''
        pkg = f'''<section class="pkg" id="package" aria-labelledby="pkg-h"><h2 id="pkg-h">{phead}</h2><p>{pintro}</p>{orig_line}
<div class="pblock"><div class="ph"><span>{E(k['title'])} (full text)</span><span class="pb"><button class="copy" type="button" data-target="p-package" aria-label="Copy the whole package">Copy all</button><a class="dl" href="/downloads/{k['slug']}.pdf" download="{E(dlname)}">Download PDF</a></span></div><pre id="p-package" class="pkgtext">{E(ptext)}</pre></div></section>{guide}'''
        art = f'''<article class="prose">
{pkg}<h2 id="overview">Overview</h2><p>{E(k['summary'])}</p><p>{E(k['why'])}</p>
<h2 id="framework">Prompt framework</h2><p>Copy each part, or copy the full prompt. Replace anything in square brackets.</p>
<h3>01 Role</h3>{pblock('p-role', 'Role', k['role'])}<h3>02 Context</h3>{pblock('p-context', 'Context', k['context'])}<h3>03 Output</h3>{pblock('p-output', 'Output', k['output'])}
<h3>Full prompt</h3>{pblock('p-full', 'Full prompt', full)}
<h2 id="examples">Example prompts</h2><p>These are original examples written for this kit. Results vary by tool, so review every output.</p>
{''.join(f'<h3>{E(t)}</h3>' + pblock(f'p-ex{j}', t, x) for j, (t, x) in enumerate(k['examples']))}
<h2 id="adapt">How to adapt it</h2><ol>{''.join(f'<li>{E(a)}</li>' for a in k['adapt'])}</ol><p>More tips in <a href="/guides/adapt-a-kit-to-your-project/">how to adapt a kit to your project</a>.</p>
<h2 id="fact-check">Fact check checklist</h2><ul class="checklist">{''.join(f'<li>{E(c)}</li>' for c in k['checks'])}</ul>
<p>See the full method in <a href="/guides/fact-check-ai-output/">how to fact-check AI output</a>.</p>
<p class="notice" role="note">{NOTICE}</p>
<nav class="pager" aria-label="More kits"><a class="card prev" href="/kits/{prev['slug']}/"><small>{"Previous idea" if isn else "Previous kit"}</small>{E(prev['title'])}</a><a class="card next" href="/kits/{nxt['slug']}/"><small>{"Next idea" if isn else "Next kit"}</small>{E(nxt['title'])}</a></nav>
<section class="related" aria-labelledby="rel"><h2 id="rel">{"More niche ideas" if isn else "Related kits"}</h2><div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">{''.join(kitcard(x) for x in rel)}</div></section>
</article>'''
        banner = f'''<div class="artbanner"><img src="/assets/kits/{k['slug']}-art.jpg" alt="Illustration for the {E(k['title'])}" width="1152" height="864" fetchpriority="high" decoding="async"></div>'''
        prev_html = f'''<figure class="preview"><div class="pv"><img src="/assets/kits/{k['slug']}-cover.jpg" alt="Preview of the printable cover page for the {E(k['title'])}, showing the illustration, title and section list" width="1200" height="800" loading="lazy" decoding="async"><img src="/assets/kits/{k['slug']}-inside.jpg" alt="Preview of an inside page of the {E(k['title'])}, showing the Role, Context and Output prompt framework and the fact check checklist" width="1200" height="800" loading="lazy" decoding="async"></div><figcaption>Preview of the printable kit. Use Download PDF for the full kit.</figcaption></figure>'''
        tools = f'<div class="tools"><a class="btn pri" href="/downloads/{k['slug']}.pdf" download="{E(dlname)}">Download PDF</a><button class="btn" type="button" data-print>Print</button><a class="btn" href="/builder/">Open the builder</a></div>'
        body = hero(E(k['title']), E(k['summary']), E(k['cat']) + ' kit', f'<div class="meta"><span>{rtime(n)} min read</span><span>Updated {DATE}</span><span>Original content</span></div><p class="notice" role="note">{NOTICE}</p>{banner}{tools}{prev_html}') + \
            f'<div class="wrap layout"><nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>{"".join(f"<li><a href=\"#{a}\">{b}</a></li>" for a, b in toc)}</ol></nav>{art}</div>'
        howto = {"@context": "https://schema.org", "@type": "HowTo", "name": k['title'], "description": k['summary'], "inLanguage": "en", "image": [url(f"assets/kits/{k['slug']}-cover.jpg"), url(f"assets/kits/{k['slug']}-inside.jpg")], "totalTime": f"PT{rtime(n) + 10}M",
                 "step": [{"@type": "HowToStep", "position": 1, "name": "Set the role", "text": k['role']}, {"@type": "HowToStep", "position": 2, "name": "Add the context", "text": k['context']},
                          {"@type": "HowToStep", "position": 3, "name": "Ask for the output", "text": k['output']}, {"@type": "HowToStep", "position": 4, "name": "Fact check", "text": ' '.join(k['checks'])}]}
        desc = k['summary'] if len(k['summary']) <= 158 else k['summary'][:155].rsplit(' ', 1)[0] + '...'
        if len(desc) < 75: desc += ' Free prompt framework and fact check list.'
        layout(f"kits/{k['slug']}/", k['title'], desc, body, crumbs=[('niche-ideas/', 'Niche ideas') if isn else ('kits/', 'Kits'), (f"kits/{k['slug']}/", k['title'])], ld=[howto], og_slug='kit-' + k['slug'], og_kicker=k['cat'] + ' kit', og_override=f"assets/kits/{k['slug']}-cover.jpg")
    # GUIDES
    gcards = ''.join(f'<div class="rv"><a class="card kitcard" href="/guides/{g["slug"]}/"><img src="/og/guide-{g["slug"]}.png" alt="Cover card for the guide {E(g["title"])}" width="1200" height="630" loading="lazy" decoding="async"><span class="tag">Guide</span><h2 style="font-size:20px;margin:0">{E(g["title"])}</h2><p>{E(g["summary"])}</p></a></div>' for g in GUIDES)
    for g in GUIDES: og('guide-' + g['slug'], g['title'], 'Guide')
    il = {"@context": "https://schema.org", "@type": "ItemList", "name": "Guides", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": url(f"guides/{g['slug']}/"), "name": g['title']} for i, g in enumerate(GUIDES)]}
    layout('guides/', 'Guides: Better AI Prompts, Step by Step', 'Short, original guides on writing clear AI prompts, fact-checking AI output and adapting creator kits to your own project.', hero('Guides', 'Short reads that teach the method behind every kit.', 'Learn the basics') + f'<section class="sec" style="padding-top:44px"><div class="wrap"><div class="grid">{gcards}</div></div></section>', crumbs=[('guides/', 'Guides')], ld=[il], og_slug='guides', og_kicker='Guides')
    for i, g in enumerate(GUIDES):
        n = words(g['summary'], *[b for _, b in g['body']], g['prompt'])
        secs = ''.join(f'<h2 id="s{j}">{E(h)}</h2><p>{E(b)}</p>' for j, (h, b) in enumerate(g['body']))
        others = ''.join(f'<li><a href="/guides/{o["slug"]}/">{E(o["title"])}</a></li>' for o in GUIDES if o is not g)
        art = f'<div class="wrap layout"><nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>{"".join(f"<li><a href=\"#s{j}\">{E(h)}</a></li>" for j, (h, _) in enumerate(g["body"]))}<li><a href="#try">Try it</a></li></ol></nav><article class="prose">{secs}<h2 id="try">Try it</h2>{pblock("p-guide", "Example prompt", g["prompt"])}<p class="notice" role="note">{NOTICE}</p><h2>More guides</h2><ul>{others}</ul><p>Ready to practice? <a href="/kits/">Pick a kit</a> or <a href="/builder/">open the builder</a>.</p></article></div>'
        body = hero(E(g['title']), E(g['summary']), 'Guide', f'<div class="meta"><span>{rtime(n)} min read</span><span>Updated {DATE}</span></div>') + art
        artld = {"@context": "https://schema.org", "@type": "Article", "headline": g['title'], "description": g['summary'], "datePublished": DATE, "dateModified": DATE, "inLanguage": "en", "image": url(f"og/guide-{g['slug']}.png"), "author": {"@type": "Organization", "name": SITE_NAME}, "publisher": {"@type": "Organization", "name": SITE_NAME}, "mainEntityOfPage": url(f"guides/{g['slug']}/")}
        layout(f"guides/{g['slug']}/", g['title'], g['summary'], body, crumbs=[('guides/', 'Guides'), (f"guides/{g['slug']}/", g['title'])], ld=[artld], og_slug='guide-' + g['slug'], og_kicker='Guide')
    # BUILDER
    fm = ''.join(f'<button class="chip fmt" type="button" data-f="{f}" aria-pressed="{"true" if i == 0 else "false"}">{f}</button>' for i, f in enumerate(['Short video script', 'Carousel', 'Image prompts', 'Blog outline']))
    body = hero('Prompt builder', 'Type a topic, choose a format and get a 3 part prompt you can copy. Everything runs in your browser. Nothing is saved or sent.', 'Runs offline') + f'''
<section class="sec" style="padding-top:44px"><div class="wrap hgrid" style="align-items:start"><form class="card builder" id="builder"><label for="topic">Your topic</label><input class="search" id="topic" type="text" placeholder="e.g. history of the jeepney" autocomplete="off">
<label for="aud">Audience</label><input class="search" id="aud" type="text" placeholder="e.g. Grade 6 students" autocomplete="off">
<fieldset><legend>Format</legend><div class="filters" style="margin:0">{fm}</div></fieldset>
<noscript><p>The builder needs JavaScript. You can still copy the framework from any kit page.</p></noscript></form>
<div class="card glow out" aria-live="polite"><div class="nb-head"><span>Your prompt</span><span>3 parts</span></div>
<div class="part on"><b>01 · ROLE</b><p id="o1"></p></div><div class="part on"><b>02 · CONTEXT</b><p id="o2"></p></div><div class="part on"><b>03 · OUTPUT</b><p id="o3"></p></div>
{pblock('built', 'Full prompt', '')}<p class="muted" style="font-size:14px">{NOTICE}</p></div></div></section>'''
    layout('builder/', 'Prompt Builder: Make a 3 Part AI Prompt', 'Free prompt builder that turns your topic, audience and format into a clear Role, Context and Output prompt. Runs in your browser, saves nothing.', body, crumbs=[('builder/', 'Builder')], og_slug='builder', og_kicker='Tool')
    # ABOUT / PRIVACY / 404
    layout('about/', 'About Open Source Prompt PH', 'Open Source Prompt PH is a free library of original AI prompt kits and guides for Filipino creators, built to teach clear prompts and careful fact-checking.',
           hero('About Open Source Prompt PH', 'Better prompts. More possibilities. A free library of prompt kits and guides for first time and busy creators.', 'About') + f'<div class="wrap narrow"><article class="prose" style="padding:40px 0"><h2>What this site is</h2><p>Each kit is a web page with a prompt framework, examples, tips to adapt it and a fact check checklist. You can print any kit or save it as a PDF from your browser.</p><h2>How the content is made</h2><p>Kits and guides are written for this site and drafted with AI assistance, then reviewed. They do not contain verified facts about their topics. The prompts ask you to check facts yourself before publishing.</p><p>Cover illustrations are AI generated.</p><p class="notice" role="note">{NOTICE}</p><h2>What we do not do</h2><ul><li>No accounts, no sign ups.</li><li>No analytics, ads or trackers.</li><li>No collection of what you type in the builder.</li></ul><p>Read the <a href="/privacy/">privacy page</a> for details.</p></article></div>',
           crumbs=[('about/', 'About')], og_slug='about')
    layout('privacy/', 'Privacy', 'Open Source Prompt PH uses no cookies, analytics or trackers. The prompt builder runs in your browser and nothing you type is saved or sent.',
           hero('Privacy', 'Short version: we do not collect anything.', '') + '<div class="wrap narrow"><article class="prose" style="padding:40px 0"><h2>No tracking</h2><p>This site has no analytics, ads, cookies or third party scripts. Fonts and scripts load from this site only.</p><h2>The prompt builder</h2><p>The builder runs in your browser. What you type is not stored or sent to any server. Copying uses your browser clipboard.</p><h2>Hosting</h2><p>Like any website, the host server may keep standard access logs. Check the hosting provider for its policy once the site is live.</p></article></div>',
           crumbs=[('privacy/', 'Privacy')], og_slug='privacy')
    osp_404()
    # SITEMAP / ROBOTS
    (OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{url(p)}</loc><lastmod>{DATE}</lastmod></url>\n' for p in PAGES) + '</urlset>\n')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {url("sitemap.xml")}\n')
    print(f'built {len(PAGES)} indexable pages + 404 -> {OUT}/')

if __name__ == '__main__': build()
