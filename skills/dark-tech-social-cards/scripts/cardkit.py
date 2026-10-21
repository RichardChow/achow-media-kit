"""cardkit — social cards for X, two themes.

theme='dark'  (default) deep teal gradient + mint accent + glowing terminal  
theme='light' cream #F6F4EF + orange #FF5A1F + ink #111 + flat server-node illustration 

Two building blocks:
  cover(...)        2000x800 (5:2) cover: kicker + big title + subtitle + handle, terminal window on the right
  compare_card(...) 1200x1500 (4:5) A-vs-B data card: conditions row + sections of labelled usage bars

All text, colors and sizes are configurable. Fonts: Noto Sans CJK SC (Bold/Regular) for text,
JetBrains Mono for code/kicker, with automatic CJK fallback inside mono strings.
Run `python3 cardkit.py` for a demo. See cardkit-STYLE.md for the visual rules.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# ---------- palette ----------
BG_DARK = (6, 9, 12)          # left / top background
BG_TEAL = (11, 29, 31)        # right / bottom background tint
ACCENT = (61, 255, 180)       # mint accent (default highlight)
WHITE = (255, 255, 255)
TEXT2 = (200, 208, 212)       # secondary text
MUTED = (124, 134, 138)       # subtitles / handle / footnotes
FAINT = (70, 80, 86)
PANEL = (8, 17, 21)           # terminal body / card panel
PANEL_BAR = (20, 28, 31)      # terminal title bar
CLAUDE = (217, 119, 87)       # #D97757
CODEX = (74, 144, 255)        # Codex / OpenAI-ish blue
WARN = (255, 95, 87)

# ---------- light palette  ----------
L_BG = (246, 244, 239)        # #F6F4EF cream background
L_INK = (17, 17, 17)          # #111111 title / outlines / filled node
L_ACCENT = (255, 90, 31)      # #FF5A1F orange accent (pill, highlight word, node dots)
L_TEXT2 = (68, 68, 68)        # #444444 subtitle / labels
L_MUTED = (136, 136, 136)     # #888888 footer / handle / footnotes
L_PANEL = (255, 255, 255)     # #FFFFFF server boxes / cards
L_TRACK = (232, 228, 218)     # #E8E4DA empty bar track
L_RULE = (221, 217, 207)      # #DDD9CF divider
# dark-palette constants used in shared build scripts are auto-mapped in light theme
_LIGHT_MAP = {WHITE: L_INK, TEXT2: L_TEXT2, MUTED: L_MUTED, FAINT: L_MUTED, ACCENT: L_ACCENT}


def _lc(c):
    return _LIGHT_MAP.get(tuple(c), tuple(c))

# ---------- fonts ----------
def _find(env, *cands):
    for c in [os.environ.get(env)] + list(cands):
        if c and os.path.exists(c):
            return c
    return cands[0]


_CJK_B = _find('CARDKIT_CJK_BOLD', '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
               '/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc', '/System/Library/Fonts/PingFang.ttc')
_CJK_R = _find('CARDKIT_CJK_REGULAR', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
               '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc', '/System/Library/Fonts/PingFang.ttc')
def _glob_font(pattern):
    import glob
    for root in ('/usr/share/fonts', '/usr/local/share/fonts', os.path.expanduser('~/.fonts'),
                 os.path.expanduser('~/.local/share/fonts'), os.path.expanduser('~/Library/Fonts'), '/Library/Fonts'):
        hits = sorted(glob.glob(os.path.join(root, '**', pattern), recursive=True))
        if hits:
            return hits[0]
    return None


_MONO = os.environ.get('CARDKIT_MONO') or _glob_font('JetBrainsMono-VariableFont_wght.ttf') \
    or _glob_font('JetBrainsMono-Regular.ttf') or 'JetBrainsMono-Regular.ttf'
_MONO_FALLBACK = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
_cache = {}


def font(kind, size):
    """kind: 'b' CJK bold, 'r' CJK regular, 'm' mono regular, 'mb' mono bold."""
    k = (kind, size)
    if k in _cache:
        return _cache[k]
    if kind in ('b', 'r'):
        f = ImageFont.truetype(_CJK_B if kind == 'b' else _CJK_R, size, index=2)  # index 2 = SC
    else:
        if os.path.exists(_MONO):
            f = ImageFont.truetype(_MONO, size)
            try:
                f.set_variation_by_name('Bold' if kind == 'mb' else 'Regular')
            except Exception:
                pass
        else:
            f = ImageFont.truetype(_MONO_FALLBACK, size)
    _cache[k] = f
    return f


def _is_cjk(ch):
    o = ord(ch)
    return o >= 0x2E80 or 0xFF00 <= o <= 0xFFEF


def text_mixed(d, xy, s, mono, cjk, fill):
    """Draw s with `mono` for Latin and `cjk` for CJK chars; baseline-aligned. Returns end x."""
    x, y = xy
    asc_m = mono.getmetrics()[0]
    asc_c = cjk.getmetrics()[0]
    base = y + max(asc_m, asc_c)
    run, cur = '', None
    def flush(run, cur, x):
        if not run:
            return x
        f = cjk if cur else mono
        d.text((x, base), run, font=f, fill=fill, anchor='ls')
        return x + d.textlength(run, font=f)
    for ch in s:
        c = _is_cjk(ch)
        if cur is None or c == cur:
            run += ch; cur = c
        else:
            x = flush(run, cur, x); run, cur = ch, c
    return flush(run, cur, x)


def width_mixed(d, s, mono, cjk):
    return sum(d.textlength(ch, font=cjk if _is_cjk(ch) else mono) for ch in s)


def segments(d, xy, segs, f):
    """segs = [(text, color), ...] drawn on one line with font f. Returns end x."""
    x, y = xy
    for t, c in segs:
        d.text((x, y), t, font=f, fill=c)
        x += d.textlength(t, font=f)
    return x


# ---------- background ----------
def background(W, H, dark=BG_DARK, tint=BG_TEAL, dots=True, glow=None):
    """Diagonal dark gradient + faint dot grid. glow=(x, y, r, color) adds a soft light blob."""
    import numpy as np
    yy, xx = np.mgrid[0:H, 0:W]
    t = np.clip((xx / W) * .75 + (yy / H) * .25, 0, 1)[..., None] ** 1.3   # dark top-left -> teal bottom-right
    arr = np.array(dark)[None, None, :] * (1 - t) + np.array(tint)[None, None, :] * t
    img = Image.fromarray(arr.astype('uint8'), 'RGB')
    d = ImageDraw.Draw(img)
    if dots:
        for yy in range(20, H, 40):
            for xx in range(20, W, 40):
                d.point((xx, yy), fill=(28, 40, 44))
                d.point((xx + 1, yy), fill=(28, 40, 44))
    if glow:
        gx, gy, gr, gc = glow
        lay = Image.new('RGB', (W, H), (0, 0, 0))
        ImageDraw.Draw(lay).ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=tuple(int(v * .35) for v in gc))
        lay = lay.filter(ImageFilter.GaussianBlur(gr / 2))
        img = Image.fromarray(__import__('numpy').minimum(
            __import__('numpy').asarray(img).astype('int16') + __import__('numpy').asarray(lay), 255).astype('uint8'))
    return img


def glow_rect(img, box, color, radius=18, blur=28, strength=.55):
    lay = Image.new('RGB', img.size, (0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle(box, radius, fill=tuple(int(v * strength) for v in color))
    lay = lay.filter(ImageFilter.GaussianBlur(blur))
    import numpy as np
    out = np.minimum(np.asarray(img).astype('int16') + np.asarray(lay), 255).astype('uint8')
    img.paste(Image.fromarray(out))


def terminal(img, box, lines, glow=ACCENT, size=30, line_h=None):
    """Mac-style terminal window. lines = [(text, color), ...]; a text of '$_' draws a prompt + cursor."""
    x0, y0, x1, y1 = box
    glow_rect(img, box, glow)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, 18, fill=PANEL, outline=tuple(int(v * .45) for v in glow), width=2)
    d.rounded_rectangle([x0 + 1, y0 + 1, x1 - 1, y0 + 56], 17, fill=PANEL_BAR)
    d.rectangle([x0 + 1, y0 + 40, x1 - 1, y0 + 56], fill=PANEL_BAR)
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (39, 201, 63)]):
        cx = x0 + 32 + i * 30
        d.ellipse([cx - 8, y0 + 20, cx + 8, y0 + 36], fill=c)
    m, cj = font('m', size), font('r', size)
    lh = line_h or int(size * 1.7)
    y = y0 + 90
    for t, c in lines:
        if t == '$_':
            ex = text_mixed(d, (x0 + 36, y), '$ ', m, cj, c)
            d.rectangle([ex, y + 4, ex + size * .55, y + size * 1.1], fill=ACCENT)
        else:
            text_mixed(d, (x0 + 36, y), t, m, cj, c)
        y += lh
    return y


# ---------- cover ----------
def cover(out, title_lines, subtitle, handle='@your_handle', kicker=None, term_lines=None,
          W=2000, H=800, accent=ACCENT, title_size=None, glow=None, theme='dark',
          footer=None, illustration='servers'):
    """title_lines: list of lines, each a list of (text, color) segments.
    term_lines: [(text, color)] for the right-side terminal; None = full-width text layout.
    theme='light': kicker becomes an orange pill, footer=[...] stack line bottom-left (handle bottom-right),
    right side = illustration ('servers' | 'terminal' | None); term_lines is used when illustration='terminal'."""
    if theme == 'light':
        return _cover_light(out, title_lines, subtitle, handle, kicker, term_lines, W, H,
                            accent, title_size, footer, illustration)
    if title_size is None:
        title_size = 120
    img = background(W, H)
    d = ImageDraw.Draw(img)
    x, y = 140, 150 if len(title_lines) > 1 else 170
    if kicker:
        text_mixed(d, (x, y), kicker, font('m', 32), font('r', 32), accent)
        y += 75
    tf = font('b', title_size)
    for segs in title_lines:
        segments(d, (x, y - title_size * .18), segs, tf)
        y += int(title_size * 1.22)
    y += 18
    d.text((x, y), subtitle, font=font('r', 44), fill=TEXT2)
    d.text((x, H - 90), handle, font=font('r', 28), fill=MUTED)
    if term_lines:
        terminal(img, (1200, 175, W - 110, H - 175), term_lines, glow=glow or accent)
    img.save(out, optimize=True)
    return img.size


# ---------- compare card ----------
def compare_card(out, title, kicker, sides, sections, footnote, handle='@your_handle', W=1200, H=None,
                 theme='dark'):
    """theme: 'dark' (default) | 'light'.
    sides: [{'name','color','spec'}] x2 (left/right conditions).
    sections: [{'title','subtitle','rows':[{'side':0|1,'label','value','pct' (0-100 or None),'note'}]}]
    Bars show pct of a quota; value is the exact text printed at the bar end. Use only real numbers.
    H=None -> height fits content (two-pass)."""
    if theme == 'light':
        return _compare_light(out, title, kicker, sides, sections, footnote, handle, W, H)
    if H is None:
        _, end = compare_card('/tmp/_cardkit_probe.png', title, kicker, sides, sections, footnote, handle, W, 4000)
        H = end + 150
    img = background(W, H)
    d = ImageDraw.Draw(img)
    X = 80
    y = 70
    text_mixed(d, (X, y), kicker, font('m', 28), font('r', 28), ACCENT); y += 60
    segments(d, (X, y), title, font('b', 64)); y += 128
    # conditions
    cw = (W - 2 * X - 30) // 2
    for i, s in enumerate(sides):
        bx = X + i * (cw + 30)
        d.rounded_rectangle([bx, y, bx + cw, y + 190], 16, fill=PANEL, outline=tuple(int(v * .6) for v in s['color']), width=2)
        d.rounded_rectangle([bx, y, bx + 10, y + 190], 5, fill=s['color'])
        d.text((bx + 34, y + 24), s['name'], font=font('b', 40), fill=s['color'])
        for j, l in enumerate(s['spec']):
            text_mixed(d, (bx + 34, y + 84 + j * 40), l, font('m', 26), font('r', 26), TEXT2)
    y += 190 + 54
    bar_x0, bar_w = X + 260, W - 2 * X - 260; BH = 52
    for sec in sections:
        d.text((X, y), sec['title'], font=font('b', 48), fill=WHITE)
        if sec.get('subtitle'):
            tx = X + d.textlength(sec['title'], font=font('b', 48)) + 20
            d.text((tx, y + 14), sec['subtitle'], font=font('r', 28), fill=MUTED)
        y += 76
        for r in sec['rows']:
            c = sides[r['side']]['color']
            d.text((X, y + 6), r['label'], font=font('r', 30), fill=TEXT2)
            d.rounded_rectangle([bar_x0, y, bar_x0 + bar_w, y + BH], 10, fill=(18, 30, 34))
            if r.get('pct') is not None:
                lo, hi = (r['pct'] if isinstance(r['pct'], tuple) else (r['pct'], r['pct']))
                if hi > 0:
                    d.rounded_rectangle([bar_x0, y, bar_x0 + bar_w * hi / 100, y + BH], 10,
                                        fill=tuple(int(v * .45) for v in c) if lo != hi else c)
                if lo > 0 and lo != hi:
                    d.rounded_rectangle([bar_x0, y, bar_x0 + bar_w * lo / 100, y + BH], 10, fill=c)
            vf = font('b', 30)
            vw = d.textlength(r['value'], font=vf)
            d.text((bar_x0 + bar_w - vw - 20, y + 5), r['value'], font=vf, fill=WHITE)
            y += BH + 12
            if r.get('note'):
                d.text((bar_x0, y), r['note'], font=font('r', 26), fill=MUTED)
                y += 42
            y += 22
        y += 40
    d.line([X, H - 120, W - X, H - 120], fill=(30, 44, 48), width=2)
    d.text((X, H - 92), footnote, font=font('r', 26), fill=MUTED)
    hw = d.textlength(handle, font=font('r', 26))
    d.text((W - X - hw, H - 92), handle, font=font('r', 26), fill=MUTED)
    img.save(out, optimize=True)
    return img.size, y


# ---------- light theme (reference style) ----------
def _ink_top(d, s, f):
    """distance from baseline to ink top (negative number) for string s."""
    return d.textbbox((0, 0), s, font=f, anchor='ls')[1]


def pill(d, xy, text, color=L_ACCENT, size=31, h=62, width=4, fill=None):
    """Rounded outline tag like the reference cover's 'VPS 自建教程'. Returns (x1, y1)."""
    x, y = xy
    f = font('b', size)
    tw = d.textlength(text, font=f)
    x1 = x + tw + 2 * 30
    d.rounded_rectangle([x, y, x1, y + h], h // 2, outline=color, width=width, fill=fill)
    d.text(((x + x1) / 2, y + h / 2), text, font=f, fill=color, anchor='mm')
    return x1, y + h


def servers(img, origin=(1328, 227), n=3, filled=1, nodes=True):
    """Flat server rack + dashed links to 3 nodes (orange / hollow / ink), measured from the reference cover.
    origin = top-left of the first box (reference: 1328,227 on a 2000x800 canvas)."""
    d = ImageDraw.Draw(img)
    ox, oy = origin
    BW, BH, GAP, R, LW = 304, 92, 16, 20, 5
    node = [((412, 13), 'orange'), ((432, 173), 'hollow'), ((392, 323), 'ink')]
    for i in range(n):
        y = oy + i * (BH + GAP)
        box = [ox, y, ox + BW, y + BH]
        solid = (i == filled)
        d.rounded_rectangle(box, R, fill=L_INK if solid else L_PANEL, outline=L_INK, width=LW)
        cy = y + BH // 2
        d.ellipse([ox + 40, cy - 12, ox + 64, cy + 12], fill=L_ACCENT)
        d.rounded_rectangle([ox + 190, cy - 3, ox + 264, cy + 2], 2, fill=L_PANEL if solid else L_INK)
        if nodes and i < len(node):
            (nx, ny), kind = node[i]
            nx, ny = ox + nx, oy + ny
            sx, sy = ox + BW + 4, cy
            steps = int(((nx - sx) ** 2 + (ny - sy) ** 2) ** .5 // 14)
            for k in range(steps):
                t0, t1 = k / steps, (k + .55) / steps
                if (k + .55) / steps > 1 - 30 / max(1, ((nx - sx) ** 2 + (ny - sy) ** 2) ** .5):
                    break
                d.line([sx + (nx - sx) * t0, sy + (ny - sy) * t0, sx + (nx - sx) * t1, sy + (ny - sy) * t1],
                       fill=L_INK, width=4)
            r = 26
            if kind == 'orange':
                d.ellipse([nx - r, ny - r, nx + r, ny + r], fill=L_ACCENT)
            elif kind == 'hollow':
                d.ellipse([nx - r, ny - r, nx + r, ny + r], fill=L_PANEL, outline=L_INK, width=5)
            else:
                d.ellipse([nx - r, ny - r, nx + r, ny + r], fill=L_INK)


def terminal_light(img, box, lines, size=30, line_h=None):
    """Flat light terminal: white panel, 5px ink outline, ink title bar dots."""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, 20, fill=L_PANEL, outline=L_INK, width=5)
    d.line([x0 + 3, y0 + 58, x1 - 3, y0 + 58], fill=L_INK, width=4)
    for i, c in enumerate([L_ACCENT, L_PANEL, L_INK]):
        cx = x0 + 36 + i * 32
        d.ellipse([cx - 9, y0 + 20, cx + 9, y0 + 38], fill=c, outline=L_INK, width=3)
    m, cj = font('m', size), font('r', size)
    lh = line_h or int(size * 1.7)
    y = y0 + 88
    for t, c in lines:
        c = _lc(c)
        if t == '$_':
            ex = text_mixed(d, (x0 + 36, y), '$ ', m, cj, L_TEXT2)
            d.rectangle([ex, y + 4, ex + size * .55, y + size * 1.1], fill=L_ACCENT)
        else:
            text_mixed(d, (x0 + 36, y), t, m, cj, c)
        y += lh
    return y


def _cover_light(out, title_lines, subtitle, handle, kicker, term_lines, W, H, accent,
                 title_size, footer, illustration):
    accent = _lc(accent)
    img = Image.new('RGB', (W, H), L_BG)
    d = ImageDraw.Draw(img)
    if title_size is None:
        title_size = 168 if len(title_lines) == 1 else 118
    tf, sf = font('b', title_size), font('r', 46)
    lines = [[(t, _lc(c)) for t, c in segs] for segs in title_lines]
    # measure block: pill 62 + 59 gap + title ink + 45 gap + subtitle ink  (gaps from the reference cover)
    tops = [_ink_top(d, ''.join(t for t, _ in s), tf) for s in lines]
    line_adv = int(title_size * 1.12)
    title_ink = (len(lines) - 1) * line_adv + (-tops[-1]) + int(title_size * .10)
    sub_top = _ink_top(d, subtitle, sf)
    block = (62 + 59 if kicker else 0) + title_ink + 45 + (-sub_top) + 10
    y = max(80, int(336 - block / 2))          # reference block is centred on y≈336
    x = 140
    if kicker:
        k = kicker[2:] if kicker.startswith('> ') else kicker
        _, yb = pill(d, (x, y), k, color=accent)
        y = yb + 59
    base = y - tops[0]
    for segs in lines:
        xx = x
        for t, c in segs:
            d.text((xx, base), t, font=tf, fill=c, anchor='ls')
            xx += d.textlength(t, font=tf)
        base += line_adv
    base -= line_adv
    y = base + int(title_size * .10) + 45
    d.text((x + 3, y - sub_top), subtitle, font=sf, fill=L_TEXT2, anchor='ls')
    ff = font('r', 28)
    if footer:
        d.text((x, 691), ' · '.join(footer), font=ff, fill=L_MUTED)
    hw = d.textlength(handle, font=ff)
    d.text((W - 122 - hw, 691), handle, font=ff, fill=L_MUTED)
    dx = W - 2000
    if illustration == 'servers':
        servers(img, (1328 + dx, 227 + (H - 800) // 2))
    elif illustration == 'terminal' and term_lines:
        terminal_light(img, (1200 + dx, 175, W - 110, H - 175), term_lines)
    img.save(out, optimize=True)
    return img.size


def _compare_light(out, title, kicker, sides, sections, footnote, handle, W, H):
    if H is None:
        _, end = _compare_light('/tmp/_cardkit_probe.png', title, kicker, sides, sections, footnote, handle, W, 4000)
        H = end + 150
    img = Image.new('RGB', (W, H), L_BG)
    d = ImageDraw.Draw(img)
    X, y = 80, 70
    k = kicker[2:] if kicker.startswith('> ') else kicker
    pill(d, (X, y), k, size=26, h=54); y += 54 + 34
    segments(d, (X, y), [(t, _lc(c)) for t, c in title], font('b', 64)); y += 120
    cw = (W - 2 * X - 30) // 2
    for i, s in enumerate(sides):
        bx = X + i * (cw + 30)
        d.rounded_rectangle([bx, y, bx + cw, y + 190], 18, fill=L_PANEL, outline=L_INK, width=4)
        d.rounded_rectangle([bx + 22, y + 34, bx + 32, y + 156], 5, fill=s['color'])
        d.text((bx + 52, y + 24), s['name'], font=font('b', 40), fill=s['color'])
        for j, l in enumerate(s['spec']):
            text_mixed(d, (bx + 52, y + 84 + j * 40), l, font('m', 26), font('r', 26), L_TEXT2)
    y += 190 + 54
    bar_x0, bar_w = X + 260, W - 2 * X - 260; BH = 52
    for sec in sections:
        d.text((X, y), sec['title'], font=font('b', 48), fill=L_INK)
        if sec.get('subtitle'):
            tx = X + d.textlength(sec['title'], font=font('b', 48)) + 20
            d.text((tx, y + 14), sec['subtitle'], font=font('r', 28), fill=L_MUTED)
        y += 76
        for r in sec['rows']:
            c = sides[r['side']]['color']
            d.text((X, y + 6), r['label'], font=font('r', 30), fill=L_TEXT2)
            d.rounded_rectangle([bar_x0, y, bar_x0 + bar_w, y + BH], 12, fill=L_TRACK)
            hi = 0
            if r.get('pct') is not None:
                lo, hi = (r['pct'] if isinstance(r['pct'], tuple) else (r['pct'], r['pct']))
                pale = tuple(int(v * .45 + b * .55) for v, b in zip(c, L_BG))
                if hi > 0:
                    d.rounded_rectangle([bar_x0, y, bar_x0 + bar_w * hi / 100, y + BH], 12,
                                        fill=pale if lo != hi else c)
                if lo > 0 and lo != hi:
                    d.rounded_rectangle([bar_x0, y, bar_x0 + bar_w * lo / 100, y + BH], 12, fill=c)
            vf = font('b', 30)
            vw = d.textlength(r['value'], font=vf)
            vx = bar_x0 + bar_w - vw - 20
            on_bar = bar_w * hi / 100 > bar_w - vw - 30
            d.text((vx, y + 5), r['value'], font=vf, fill=L_PANEL if on_bar else L_INK)
            y += BH + 12
            if r.get('note'):
                d.text((bar_x0, y), r['note'], font=font('r', 26), fill=L_MUTED)
                y += 42
            y += 22
        y += 40
    d.line([X, H - 120, W - X, H - 120], fill=L_RULE, width=2)
    d.text((X, H - 92), footnote, font=font('r', 26), fill=L_MUTED)
    hw = d.textlength(handle, font=font('r', 26))
    d.text((W - X - hw, H - 92), handle, font=font('r', 26), fill=L_MUTED)
    img.save(out, optimize=True)
    return img.size, y

if __name__ == '__main__':
    print(cover('/tmp/cardkit-demo-cover.png', [[('Demo ', ACCENT), ('标题', WHITE)]], '副标题一句话',
                kicker='> cardkit demo', term_lines=[('$ echo hello', TEXT2), ('hello', ACCENT), ('$_', TEXT2)]))
