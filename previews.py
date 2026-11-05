"""Render PDF-style preview images (cover + inside page) per kit, 1200x800 JPG, Corzo palette."""
import pathlib, textwrap
from PIL import Image, ImageDraw, ImageFont
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FM = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
F = lambda p, s: ImageFont.truetype(p, s)
def bg():
    im = Image.new('RGB', (1200, 800), '#0a1628'); d = ImageDraw.Draw(im, 'RGBA')
    for x in range(0, 1200, 56): d.line([(x, 0), (x, 800)], fill=(255, 255, 255, 12))
    for y in range(0, 800, 56): d.line([(0, y), (1200, y)], fill=(255, 255, 255, 12))
    for r in range(380, 0, -10): d.ellipse([200 - r, 120 - r, 200 + r, 120 + r], fill=(196, 30, 58, 4))
    return im, d
def page(d, x, y, w, h):
    d.rounded_rectangle([x + 14, y + 18, x + w + 14, y + h + 18], 14, fill=(0, 0, 0, 90))
    d.rounded_rectangle([x, y, x + w, y + h], 14, fill='#12233f', outline=(255, 255, 255, 40))
def wrap(d, txt, font, maxw):
    out, cur = [], ''
    for w in txt.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) > maxw and cur: out.append(cur); cur = w
        else: cur = t
    return out + [cur]
def badge(d):
    d.rounded_rectangle([1040, 30, 1170, 72], 21, fill='#c41e3a'); d.text((1062, 39), 'PREVIEW', font=F(FB, 20), fill='#fff')
def render(k, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    im, d = bg(); x, y, w, h = 300, 40, 600, 720; page(d, x, y, w, h)
    ah = 330; art = Image.open(outdir / f"{k['slug']}-art.jpg").convert('RGB')
    sw, sh = art.size; ch = int(sw * ah / w); top = max(0, (sh - ch) // 2)
    art = art.crop((0, top, sw, top + ch)).resize((w, ah), Image.LANCZOS)
    mask = Image.new('L', (w, ah), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, w, ah + 20], 14, fill=255)
    im.paste(art, (x, y), mask); d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle([x, y + ah, x + w, y + ah + 8], fill='#c41e3a')
    cy = y + ah + 30; lab = k['cat'].upper() + ' KIT'
    d.rounded_rectangle([x + 36, cy, x + 36 + d.textlength(lab, font=F(FB, 15)) + 28, cy + 32], 16, fill=(196, 30, 58, 60), outline='#ff4d66')
    d.text((x + 50, cy + 7), lab, font=F(FB, 15), fill='#ff8a9a')
    ty = cy + 48
    for l in wrap(d, k['title'], F(FB, 38), w - 72)[:2]: d.text((x + 36, ty), l, font=F(FB, 38), fill='#f4f6fa'); ty += 48
    ty += 6
    for l in wrap(d, k['summary'], F(FR, 17), w - 72)[:2]: d.text((x + 36, ty), l, font=F(FR, 17), fill='#9aa8bf'); ty += 25
    for i, s in enumerate(['Prompt framework', 'Example prompts', 'How to adapt it', 'Fact check checklist']):
        xx = x + 36 + (i % 2) * 270; yy = y + h - 104 + (i // 2) * 32
        d.ellipse([xx, yy + 6, xx + 11, yy + 17], fill='#ff4d66'); d.text((xx + 22, yy), s, font=F(FR, 17), fill='#f4f6fa')
    d.text((x + 36, y + h - 34), 'Open Source Prompt PH  |  AI-assisted. Check facts.', font=F(FR, 14), fill='#9aa8bf')
    badge(d); d.text((40, 750), 'Sample cover', font=F(FR, 18), fill='#9aa8bf')
    im.save(outdir / f"{k['slug']}-cover.jpg", quality=82, optimize=True, progressive=True)
    im, d = bg(); x, y, w, h = 150, 50, 900, 700; page(d, x, y, w, h)
    d.text((x + 40, y + 34), k['title'].upper(), font=F(FB, 15), fill='#ff8a9a'); d.text((x + w - 120, y + 34), 'Page 2', font=F(FR, 15), fill='#9aa8bf')
    d.text((x + 40, y + 66), 'Prompt framework', font=F(FB, 36), fill='#f4f6fa')
    yy = y + 130
    for lab, txt in [('01 ROLE', k['role']), ('02 CONTEXT', k['context']), ('03 OUTPUT', k['output'])]:
        lines = wrap(d, txt, F(FM, 16), w - 130)[:5]; bh = 44 + 24 * len(lines)
        d.rounded_rectangle([x + 40, yy, x + w - 40, yy + bh], 10, fill='#081222'); d.rectangle([x + 40, yy, x + 44, yy + bh], fill='#ff4d66')
        d.text((x + 62, yy + 12), lab, font=F(FB, 14), fill='#ff4d66')
        for i, l in enumerate(lines): d.text((x + 62, yy + 36 + i * 24), l, font=F(FM, 16), fill='#f4f6fa')
        yy += bh + 16
    d.text((x + 40, yy + 4), 'Fact check checklist', font=F(FB, 22), fill='#f4f6fa'); yy += 38
    for c in k['checks'][:3]:
        if yy > y + h - 40: break
        d.rounded_rectangle([x + 40, yy + 3, x + 56, yy + 19], 4, outline='#ff4d66', width=2)
        d.text((x + 68, yy), wrap(d, c, F(FR, 16), w - 140)[0] + ' ...', font=F(FR, 16), fill='#9aa8bf'); yy += 30
    badge(d); d.text((40, 762), 'Sample inside page of the printable kit', font=F(FR, 18), fill='#9aa8bf')
    im.save(outdir / f"{k['slug']}-inside.jpg", quality=82, optimize=True, progressive=True)

def cover_card(k, outdir):
    """Cover card for an original OSP kit (no illustration): title, category, PDF label."""
    outdir.mkdir(parents=True, exist_ok=True)
    im, d = bg(); x, y, w, h = 120, 80, 960, 640; page(d, x, y, w, h)
    d.rectangle([x, y, x + w, y + 8], fill='#c41e3a')
    lab = k['cat'].upper() + ' KIT'
    d.rounded_rectangle([x + 50, y + 60, x + 50 + d.textlength(lab, font=F(FB, 20)) + 36, y + 102], 21, fill=(196, 30, 58, 60), outline='#ff4d66')
    d.text((x + 68, y + 69), lab, font=F(FB, 20), fill='#ff8a9a')
    ty = y + 150
    for l in wrap(d, k['short'], F(FB, 56), w - 100)[:4]: d.text((x + 50, ty), l, font=F(FB, 56), fill='#f4f6fa'); ty += 70
    d.text((x + 50, y + h - 120), 'Creator Kit  |  AI Prompt Framework', font=F(FR, 24), fill='#9aa8bf')
    d.rounded_rectangle([x + 50, y + h - 76, x + 230, y + h - 36], 20, fill='#c41e3a'); d.text((x + 72, y + h - 68), 'ORIGINAL PDF', font=F(FB, 18), fill='#fff')
    d.text((x + w - 330, y + h - 66), 'Open Source Prompt PH', font=F(FR, 22), fill='#9aa8bf')
    im.save(outdir / f"{k['slug']}-cover.jpg", quality=80, optimize=True, progressive=True)
