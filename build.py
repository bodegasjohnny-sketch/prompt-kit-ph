#!/usr/bin/env python3
"""Build Prompt Kit PH: site/ (content.py, css, js) -> docs/. Change BASE_URL before deploying."""
import json, shutil, pathlib, html, sys
from previews import render
from PIL import Image, ImageDraw, ImageFont
BASE_URL = 'https://mjd.johnnybodegas.com'   # <- single config value for canonical, OG, sitemap
SITE_NAME = 'Prompt Kit PH'
SRC = pathlib.Path('site'); OUT = pathlib.Path('docs')
sys.path.insert(0, str(SRC)); from content import KITS, GUIDES, DATE
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

NAV = [('', 'Home'), ('kits/', 'Kits'), ('guides/', 'Guides'), ('builder/', 'Builder'), ('about/', 'About')]
def layout(path, title, desc, body, crumbs=None, ld=None, og_slug='home', og_kicker='Prompt Kit PH', mbar=True, robots=None, og_override=None):
    full = title if len(title) <= 40 else title
    t = f'{full} | {SITE_NAME}' if path else f'{SITE_NAME}: Free AI Prompt Kits for Creators'
    if len(t) > 64: t = full
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
    navh = ''.join(f'<li><a href="/{p}"{" aria-current=page" if (p == path or (p and path.startswith(p))) else ""}>{n}</a></li>' for p, n in NAV)
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
<header class="top"><div class="in"><a class="brand" href="/" aria-label="{SITE_NAME} home"><i aria-hidden="true"></i><span>Prompt Kit <em>PH</em></span><small>(working name)</small></a>
<nav class="main" aria-label="Main"><ul>{navh}</ul></nav></div></header>
<main id="main">{body}</main>
<footer class="site"><div class="wrap"><p>{SITE_NAME} (working name). Free, original prompt guides. No tracking, no accounts.</p>
<ul><li><a href="/kits/">Kits</a></li><li><a href="/guides/">Guides</a></li><li><a href="/builder/">Builder</a></li><li><a href="/about/">About</a></li><li><a href="/privacy/">Privacy</a></li></ul></div></footer>
{mb}<script src="/js/app.js" defer></script></body></html>'''
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
    L=[k['title'].upper(), 'Prompt Kit PH | '+k['cat']+' kit', '', 'OVERVIEW', k['summary'], k['why'], '',
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
    st=[Paragraph(_h.escape(k['title']),H),Paragraph('Prompt Kit PH | '+_h.escape(k['cat'])+' kit',S),
        Paragraph('Overview',H2),para(k['summary']),para(k['why']),
        Paragraph('Prompt framework (replace anything in square brackets)',H2),
        Paragraph('01 Role',P),box(k['role']),Spacer(1,4),Paragraph('02 Context',P),box(k['context']),Spacer(1,4),Paragraph('03 Output',P),box(k['output']),
        Paragraph('Full prompt (copy and paste this)',H2),box(full),Paragraph('Example prompts',H2)]
    for t,x in k['examples']: st+=[Paragraph(_h.escape(t),P),box(x),Spacer(1,4)]
    st+=[Paragraph('How to adapt it',H2)]+[para(f'{i+1}. {a}') for i,a in enumerate(k['adapt'])]
    st+=[Paragraph('Fact check checklist',H2)]+[para('- '+c) for c in k['checks']]
    st+=[Spacer(1,10),Paragraph(_h.escape(NOTICE),S),Paragraph('Free at mjd.johnnybodegas.com',S)]
    def foot(c,d):
        c.setFont('Helvetica',8); c.setFillColor(colors.grey); c.drawString(20*mm,10*mm,'Prompt Kit PH | '+k['title']); c.drawRightString(190*mm,10*mm,'Page %d'%d.page)
    SimpleDocTemplate(str(path),pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=18*mm,bottomMargin=18*mm,title=k['title'],author='Prompt Kit PH').build(st,onFirstPage=foot,onLaterPages=foot)

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(); (OUT / 'CNAME').write_text('mjd.johnnybodegas.com\n'); (OUT / '.nojekyll').write_text(''); shutil.copytree(SRC / 'css', OUT / 'css'); shutil.copytree(SRC / 'js', OUT / 'js')
    (OUT / 'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="9" fill="#c41e3a"/><text x="16" y="22" font-family="monospace" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">&gt;_</text></svg>')
    for k in KITS: render(k, SRC / 'assets/kits')
    shutil.copytree(SRC / 'assets', OUT / 'assets')
    cats = sorted({k['cat'] for k in KITS})
    # HOME
    nb = '''<div class="card glow rv" id="notebook"><div class="nb-head"><span>Prompt notebook</span><span>Sample page</span></div>
<div class="nb-tabs" role="group" aria-label="Show prompt parts"><button class="chip" type="button" aria-pressed="true">01 Role</button><button class="chip" type="button" aria-pressed="false">02 Context</button><button class="chip" type="button" aria-pressed="false">03 Output</button></div>
<div class="part on"><b>01 · ROLE</b><p>You are a friendly science teacher for Grade 6 students.</p></div>
<div class="part"><b>02 · CONTEXT</b><p>Topic: why the Philippines has a rainy season. Keep it under 90 seconds. Mark claims I should verify.</p></div>
<div class="part"><b>03 · OUTPUT</b><p>Give me a 6 scene script with one image prompt per scene.</p></div>
<p class="muted" style="font-size:13px;margin:14px 0 0">Example prompt for illustration. Results vary by tool.</p></div>'''
    body = f'''<section class="hero"><div class="gridbg" aria-hidden="true"></div><div class="orb o1" aria-hidden="true"></div><div class="orb o2" aria-hidden="true"></div>
<div class="wrap hgrid"><div class="rv"><span class="pill"><b></b>Free AI prompt kits for Filipino creators</span>
<h1>Write it clearly. <span class="grad">Create it better.</span></h1>
<p class="lead">Original, step by step prompt kits for videos, carousels and explainers. Read the framework, swap in your topic and check the facts before you publish.</p>
<div class="ctas"><a class="btn pri" href="/kits/">Browse the kits</a><a class="btn" href="/builder/">Try the prompt builder</a></div></div>{nb}</div></section>
<section class="sec"><div class="wrap"><p class="eyebrow">How it works</p><h2 class="rv">Four steps from idea to a checked draft</h2>{STEPS}</div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><p class="eyebrow">Latest creator kits</p><h2 class="rv">Ready to adapt, free to read and print</h2>
<p class="muted">Every kit is a full web page with a prompt framework, worked examples and a fact check list. Every kit has a Copy all button and a Download PDF button.</p>
<div class="grid">{''.join(kitcard(k) for k in KITS[-6:][::-1])}</div><div class="ctas"><a class="btn" href="/kits/">See all {len(KITS)} kits</a></div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="cta-box rv"><p class="eyebrow">Prompt builder</p><h2>Build a 3 part prompt in seconds</h2><p class="muted">Type a topic, pick a format and copy the result. Nothing is saved or sent anywhere.</p><div class="ctas"><a class="btn pri" href="/builder/">Open the builder</a><a class="btn" href="/guides/write-a-prompt-in-3-parts/">Read the 3 part guide</a></div></div></div></section>'''
    layout('', SITE_NAME, 'Free, original AI prompt kits and guides for Filipino creators. Copy a framework, adapt it to your topic and fact-check before you publish.', body, og_slug='home')
    # KITS INDEX
    chips = '<button class="chip" type="button" data-cat="All" aria-pressed="true">All</button>' + ''.join(f'<button class="chip" type="button" data-cat="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in cats)
    body = hero('Creator kits', 'Original prompt frameworks for explainers, scripts and image series. Search by topic or filter by category.', 'Kits library') + f'''
<section class="sec" style="padding-top:44px"><div class="wrap"><label class="lbl" for="q">Search kits</label><input class="search" id="q" type="search" placeholder="Try: space, food, jeepney" autocomplete="off">
<div class="filters" role="group" aria-label="Filter by category">{chips}</div><p class="count" id="count" aria-live="polite">{len(KITS)} kits shown</p>
<div class="grid">{''.join(kitcard(k, 'h2') for k in KITS)}</div></div></section>'''
    il = {"@context": "https://schema.org", "@type": "ItemList", "name": "Creator kits", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": url(f"kits/{k['slug']}/"), "name": k['title']} for i, k in enumerate(KITS)]}
    layout('kits/', 'Creator Kits: Free AI Prompt Frameworks', f'Browse {len(KITS)} free, original AI prompt kits for explainers on animals, space, history, tech and Filipino culture. Search and filter by topic.', body, crumbs=[('kits/', 'Kits')], ld=[il], og_slug='kits', og_kicker='Kits library')
    # KIT PAGES
    for i, k in enumerate(KITS):
        prev, nxt = KITS[i - 1], KITS[(i + 1) % len(KITS)]
        rel = [x for x in KITS if x['cat'] == k['cat'] and x is not k][:3]
        rel += [x for x in KITS if x not in rel and x is not k and x not in (prev, nxt)][:3 - len(rel)]
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
            guide = '<p class="note"><strong>Simplified starter guide.</strong> The sections below are a simplified starter guide written for this site, not the PDF. The full PDF text is above.</p>'
        else:
            make_pdf(k, OUT/'downloads'/f"{k['slug']}.pdf")
            dlname = f"{k['slug']}.pdf"; ptext = package_text(k)
            phead = 'Full package (site-written)'
            pintro = 'This kit has no original PDF yet. This text and PDF were written for this site from the guide below; they are not an original kit PDF.'
            guide = ''
        pkg = f'''<section class="pkg" id="package" aria-labelledby="pkg-h"><h2 id="pkg-h">{phead}</h2><p>{pintro}</p>
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
<nav class="pager" aria-label="More kits"><a class="card prev" href="/kits/{prev['slug']}/"><small>Previous kit</small>{E(prev['title'])}</a><a class="card next" href="/kits/{nxt['slug']}/"><small>Next kit</small>{E(nxt['title'])}</a></nav>
<section class="related" aria-labelledby="rel"><h2 id="rel">Related kits</h2><div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">{''.join(kitcard(x) for x in rel)}</div></section>
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
        layout(f"kits/{k['slug']}/", k['title'], desc, body, crumbs=[('kits/', 'Kits'), (f"kits/{k['slug']}/", k['title'])], ld=[howto], og_slug='kit-' + k['slug'], og_kicker=k['cat'] + ' kit', og_override=f"assets/kits/{k['slug']}-cover.jpg")
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
{pblock('built', 'Full prompt', '')}<p class="muted" style="font-size:13px">{NOTICE}</p></div></div></section>'''
    layout('builder/', 'Prompt Builder: Make a 3 Part AI Prompt', 'Free prompt builder that turns your topic, audience and format into a clear Role, Context and Output prompt. Runs in your browser, saves nothing.', body, crumbs=[('builder/', 'Builder')], og_slug='builder', og_kicker='Tool')
    # ABOUT / PRIVACY / 404
    layout('about/', 'About Prompt Kit PH', 'Prompt Kit PH is a free library of original AI prompt kits and guides for Filipino creators, built to teach clear prompts and careful fact-checking.',
           hero('About Prompt Kit PH', 'A free library of original prompt kits and guides, made for first time and busy creators.', 'Working name') + f'<div class="wrap narrow"><article class="prose" style="padding:40px 0"><h2>What this site is</h2><p>Each kit is a web page with a prompt framework, examples, tips to adapt it and a fact check checklist. You can print any kit or save it as a PDF from your browser.</p><h2>How the content is made</h2><p>Kits and guides are written for this site and drafted with AI assistance, then reviewed. They do not contain verified facts about their topics. The prompts ask you to check facts yourself before publishing.</p><p>Cover illustrations are AI generated.</p><p class="notice" role="note">{NOTICE}</p><h2>What we do not do</h2><ul><li>No accounts, no sign ups.</li><li>No analytics, ads or trackers.</li><li>No collection of what you type in the builder.</li></ul><p>Read the <a href="/privacy/">privacy page</a> for details.</p></article></div>',
           crumbs=[('about/', 'About')], og_slug='about')
    layout('privacy/', 'Privacy', 'Prompt Kit PH uses no cookies, analytics or trackers. The prompt builder runs in your browser and nothing you type is saved or sent.',
           hero('Privacy', 'Short version: we do not collect anything.', '') + '<div class="wrap narrow"><article class="prose" style="padding:40px 0"><h2>No tracking</h2><p>This site has no analytics, ads, cookies or third party scripts. Fonts and scripts load from this site only.</p><h2>The prompt builder</h2><p>The builder runs in your browser. What you type is not stored or sent to any server. Copying uses your browser clipboard.</p><h2>Hosting</h2><p>Like any website, the host server may keep standard access logs. Check the hosting provider for its policy once the site is live.</p></article></div>',
           crumbs=[('privacy/', 'Privacy')], og_slug='privacy')
    layout('404.html', 'Page not found', 'This page could not be found. Browse the free prompt kits or guides on Prompt Kit PH instead.', hero('Page not found', 'That link does not lead anywhere. Try one of these instead.', '', '<div class="ctas"><a class="btn pri" href="/kits/">Browse kits</a><a class="btn" href="/">Go home</a></div>'), robots='noindex', mbar=False)
    # SITEMAP / ROBOTS
    (OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{url(p)}</loc><lastmod>{DATE}</lastmod></url>\n' for p in PAGES) + '</urlset>\n')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {url("sitemap.xml")}\n')
    print(f'built {len(PAGES)} indexable pages + 404 -> {OUT}/')

if __name__ == '__main__': build()
