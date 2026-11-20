"""
draw_lib.py - Rendering library for news-image-20261119

Provides:
- Robust font loading from /usr/share/fonts/truetype/noto/ with fallbacks
- Text wrapping and fit-to-box measurement utilities
- Flat illustration primitives
- 14 per-story vector illustration functions following design-spec.md motifs
- Standard card renderer function
"""

import os
import math
import textwrap
from PIL import Image, ImageDraw, ImageFont

# -----------------------------------------------------------------------------
# 1. FONT LOADING
# -----------------------------------------------------------------------------

FONT_DIR = "/usr/share/fonts/truetype/noto"

FONT_CANDIDATES = {
    "Black": [
        "NotoSans-Black.ttf",
        "NotoSansBlack.ttf",
        "NotoSans-Bold.ttf",
        "DejaVuSans-Bold.ttf"
    ],
    "Bold": [
        "NotoSans-Bold.ttf",
        "NotoSansBold.ttf",
        "DejaVuSans-Bold.ttf"
    ],
    "ExtraCondensedBold": [
        "NotoSans-ExtraCondensedBold.ttf",
        "NotoSansExtraCondensed-Bold.ttf",
        "NotoSans-Bold.ttf",
        "DejaVuSans-Bold.ttf"
    ],
    "ExtraCondensed": [
        "NotoSans-ExtraCondensed.ttf",
        "NotoSansExtraCondensed-Regular.ttf",
        "NotoSans-Regular.ttf",
        "DejaVuSans.ttf"
    ],
    "Regular": [
        "NotoSans-Regular.ttf",
        "NotoSansRegular.ttf",
        "DejaVuSans.ttf"
    ],
    "Italic": [
        "NotoSans-Italic.ttf",
        "NotoSansItalic.ttf",
        "DejaVuSans-Oblique.ttf"
    ]
}

_FONT_CACHE = {}

def get_font(font_key, size):
    """
    Load a truetype font by key ('Black', 'Bold', 'ExtraCondensedBold', 'ExtraCondensed', 'Regular', 'Italic')
    and requested size. Caches loaded fonts.
    """
    cache_key = (font_key, int(size))
    if cache_key in _FONT_CACHE:
        return _FONT_CACHE[cache_key]

    font_obj = None
    candidates = FONT_CANDIDATES.get(font_key, FONT_CANDIDATES["Regular"])

    for filename in candidates:
        filepath = os.path.join(FONT_DIR, filename)
        if os.path.exists(filepath):
            try:
                font_obj = ImageFont.truetype(filepath, int(size))
                break
            except Exception:
                pass

    if font_obj is None:
        # Fallback to PIL default
        try:
            font_obj = ImageFont.load_default()
        except Exception:
            font_obj = ImageFont.load_default()

    _FONT_CACHE[cache_key] = font_obj
    return font_obj


# -----------------------------------------------------------------------------
# 2. TEXT MEASUREMENT AND WRAPPING HELPERS
# -----------------------------------------------------------------------------

def measure_text(text, font, draw=None):
    """Return (width, height) of text using font."""
    if not text:
        return 0, 0
    if draw is not None and hasattr(draw, 'textbbox'):
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    if hasattr(font, 'getbbox'):
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    elif hasattr(font, 'getsize'):
        return font.getsize(text)
    return len(text) * 8, 12

def wrap_text(text, font, max_width, draw=None):
    """
    Wrap text into a list of lines fitting max_width.
    """
    words = text.split()
    if not words:
        return []

    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        w, _ = measure_text(test_line, font, draw)
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # Single long word exceeds line width
                lines.append(word)
                current_line = []

    if current_line:
        lines.append(' '.join(current_line))

    return lines

def fit_text_to_box(text, font_key, max_width, max_height, start_size=20, min_size=8, max_lines=None, draw=None):
    """
    Find optimal font size and wrapped lines to fit text inside (max_width, max_height).
    Returns (font, wrapped_lines, line_height).
    """
    for size in range(int(start_size), int(min_size) - 1, -1):
        font = get_font(font_key, size)
        lines = wrap_text(text, font, max_width, draw)
        if max_lines and len(lines) > max_lines:
            continue
        
        _, single_h = measure_text("Ag", font, draw)
        spacing = max(2, int(size * 0.2))
        total_h = len(lines) * single_h + max(0, len(lines) - 1) * spacing
        
        if total_h <= max_height:
            return font, lines, single_h

    # Return min size with truncation if needed
    font = get_font(font_key, min_size)
    lines = wrap_text(text, font, max_width, draw)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        if lines:
            lines[-1] = lines[-1].rstrip('.,;: ') + "…"
    _, single_h = measure_text("Ag", font, draw)
    return font, lines, single_h

def draw_wrapped_text(draw, lines, font, x, y, max_width, line_height, color="#101418", spacing=2, align="left"):
    """
    Draw list of text lines starting at (x, y).
    """
    curr_y = y
    for line in lines:
        w, _ = measure_text(line, font, draw)
        if align == "center":
            line_x = x + (max_width - w) / 2
        elif align == "right":
            line_x = x + max_width - w
        else:
            line_x = x
        draw.text((line_x, curr_y), line, font=font, fill=color)
        curr_y += line_height + spacing
    return curr_y


# -----------------------------------------------------------------------------
# 3. COLOR PALETTE & PRIMITIVES
# -----------------------------------------------------------------------------

COLORS = {
    "bg_paper": "#F7F4EE",
    "ink": "#101418",
    "card_bg": "#FFFFFF",
    "card_border": "#D8D2C4",
    "text_grey": "#4A525D",
    "red_accent": "#D9381E",
    "blue_accent": "#1E56A0",
    "teal_accent": "#2B7A78",
    "amber_accent": "#B85B14",
    "green_accent": "#2D6A4F",
    "purple_accent": "#8338EC",
    "gold_accent": "#E5A93C",
    "dark_navy": "#0F172A",
}

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    """Draw rounded rectangle with compatible method."""
    x0, y0, x1, y1 = bbox
    if hasattr(draw, 'rounded_rectangle'):
        draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)
    else:
        draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)

def draw_star(draw, center, r_outer, r_inner, points=5, fill=None, outline=None):
    """Draw n-pointed star."""
    cx, cy = center
    pts = []
    angle_step = math.pi / points
    for i in range(2 * points):
        r = r_outer if i % 2 == 0 else r_inner
        angle = i * angle_step - math.pi / 2
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, fill=fill, outline=outline)


# -----------------------------------------------------------------------------
# 4. STORY ILLUSTRATIONS (14 MOTIFS)
# -----------------------------------------------------------------------------

def draw_ill_1_icj(draw, bbox):
    """1. ICJ genocide verdict: Scales of Justice + Myanmar silhouette."""
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], fill="#1A2536") # Dark Navy

    cx, cy = x + w * 0.5, y + h * 0.5
    scale_w, scale_h = w * 0.55, h * 0.6

    # Myanmar map outline background (simplified polygon)
    map_pts = [
        (cx - w * 0.35, cy - h * 0.3),
        (cx - w * 0.22, cy - h * 0.38),
        (cx - w * 0.15, cy - h * 0.25),
        (cx - w * 0.10, cy + h * 0.1),
        (cx - w * 0.18, cy + h * 0.38),
        (cx - w * 0.28, cy + h * 0.15),
        (cx - w * 0.38, cy - h * 0.1),
    ]
    draw.polygon(map_pts, fill="#2C3E55", outline="#3E5470")

    # Scales of Justice in Gold
    gold = "#E5A93C"
    # Center pillar
    draw.line([(cx, cy - scale_h * 0.4), (cx, cy + scale_h * 0.4)], fill=gold, width=3)
    draw.line([(cx - 12, cy + scale_h * 0.4), (cx + 12, cy + scale_h * 0.4)], fill=gold, width=3)
    # Top beam
    beam_y = cy - scale_h * 0.25
    beam_l = cx - scale_w * 0.45
    beam_r = cx + scale_w * 0.45
    draw.line([(beam_l, beam_y), (beam_r, beam_y)], fill=gold, width=3)

    # Left pan
    draw.line([(beam_l, beam_y), (beam_l - 10, beam_y + 20)], fill=gold, width=1)
    draw.line([(beam_l, beam_y), (beam_l + 10, beam_y + 20)], fill=gold, width=1)
    draw.arc([beam_l - 14, beam_y + 15, beam_l + 14, beam_y + 28], start=0, end=180, fill=gold, width=2)

    # Right pan
    draw.line([(beam_r, beam_y), (beam_r - 10, beam_y + 20)], fill=gold, width=1)
    draw.line([(beam_r, beam_y), (beam_r + 10, beam_y + 20)], fill=gold, width=1)
    draw.arc([beam_r - 14, beam_y + 15, beam_r + 14, beam_y + 28], start=0, end=180, fill=gold, width=2)


def draw_ill_2_summit(draw, bbox):
    """2. Shenzhen Summit: Three flags / handshake / table."""
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], fill="#242933") # Dark Charcoal

    # Three flag panels (US, CN, RU)
    pw = w * 0.26
    ph = h * 0.55
    py = y + h * 0.22

    # Flag 1: US (Left)
    px1 = x + w * 0.08
    draw.rectangle([px1, py, px1 + pw, py + ph], fill="#B22234")
    draw.rectangle([px1, py, px1 + pw * 0.5, py + ph * 0.5], fill="#3C3B6E")
    draw.rectangle([px1, py + ph * 0.5, px1 + pw, py + ph * 0.65], fill="#FFFFFF")

    # Flag 2: CN (Center)
    px2 = x + w * 0.37
    draw.rectangle([px2, py, px2 + pw, py + ph], fill="#DE2910")
    draw_star(draw, (px2 + pw * 0.3, py + ph * 0.3), 6, 3, points=5, fill="#FFDE00")

    # Flag 3: RU (Right)
    px3 = x + w * 0.66
    draw.rectangle([px3, py, px3 + pw, py + ph], fill="#FFFFFF")
    draw.rectangle([px3, py + ph * 0.33, px3 + pw, py + ph * 0.66], fill="#0039A6")
    draw.rectangle([px3, py + ph * 0.66, px3 + pw, py + ph], fill="#D52B1E")

    # Round summit table arc at bottom
    draw.ellipse([x + w * 0.2, y + h * 0.65, x + w * 0.8, y + h * 1.1], fill="#1E232A", outline="#4C566A", width=2)


def draw_ill_3_ipo(draw, bbox):
    """3. Anthropic IPO: Upward candlestick chart + ANTH ticker."""
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], fill="#141923") # Dark Tech

    # Gridlines
    for i in range(1, 4):
        gy = y + h * (i / 4.0)
        draw.line([(x, gy), (x + w, gy)], fill="#222B3A", width=1)

    # Candlesticks
    bars = [
        (0.18, 0.70, 0.60, 0.78, False), # Red
        (0.35, 0.65, 0.48, 0.72, True),  # Green
        (0.52, 0.52, 0.35, 0.58, True),  # Green
        (0.72, 0.42, 0.18, 0.48, True),  # Green Big Jump
    ]

    for bx_ratio, open_r, close_r, low_r, is_green in bars:
        bx = x + w * bx_ratio
        open_y = y + h * open_r
        close_y = y + h * close_r
        high_y = y + h * (min(open_r, close_r) - 0.08)
        low_y = y + h * low_r

        color = "#00E676" if is_green else "#FF5252"
        # Wick
        draw.line([(bx, high_y), (bx, low_y)], fill=color, width=2)
        # Body
        top_y, bot_y = min(open_y, close_y), max(open_y, close_y)
        draw.rectangle([bx - 6, top_y, bx + 6, bot_y], fill=color)

    # Big upward trend arrow
    draw.line([(x + w * 0.15, y + h * 0.75), (x + w * 0.82, y + h * 0.22)], fill="#00E676", width=3)


def draw_ill_4_markets(draw, bbox):
    """4. Wall St Market drop: Downward red arrow over index chart."""
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], fill="#2A1215") # Dark Red Grey

    # Gridlines
    for i in range(1, 4):
        gy = y + h * (i / 4.0)
        draw.line([(x, gy), (x + w, gy)], fill="#3D1A1E", width=1)

    # Downward line chart
    points = [
        (x + w * 0.10, y + h * 0.25),
        (x + w * 0.28, y + h * 0.30),
        (x + w * 0.45, y + h * 0.22),
        (x + w * 0.65, y + h * 0.55),
        (x + w * 0.88, y + h * 0.80),
    ]
    draw.line(points, fill="#FF5252", width=3)

    # Polygon under line filled translucent red
    poly = points + [(x + w * 0.88, y + h * 0.92), (x + w * 0.10, y + h * 0.92)]
    draw.polygon(poly, fill="#42181C")

    # Big Down Arrow
    ax = x + w * 0.80
    ay = y + h * 0.65
    draw.polygon([(ax - 10, ay), (ax + 10, ay), (ax + 10, ay + 12), (ax + 18, ay + 12), (ax, ay + 26), (ax - 18, ay + 12), (ax - 10, ay + 12)], fill="#FF2A2A")


def draw_ill_5_crimea(draw, bbox):
    """5. Crimean Bridge: Bridge silhouette with gap/explosion."""
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], fill="#1C2530") # Night Sky

    # Water at bottom
    draw.rectangle([x, y + h * 0.68, x + w, y + h], fill="#0F1720")

    # Bridge roadbed
    by = y + h * 0.55
    draw.rectangle([x + w * 0.05, by, x + w * 0.95, by + 8], fill="#64748B")

    # Bridge Arches (Left span, Right span, missing middle)
    draw.arc([x + w * 0.08, by - 25, x + w * 0.42, by + 15], start=180, end=360, fill="#94A3B8", width=3)
    draw.arc([x + w * 0.58, by - 25, x + w * 0.92, by + 15], start=180, end=360, fill="#94A3B8", width=3)

    # Gap / Explosion impact in center
    cx = x + w * 0.50
    draw.polygon([(cx - 15, by - 12), (cx - 2, by - 22), (cx + 5, by - 10), (cx + 18, by - 25), (cx + 10, by + 5), (cx - 10, by + 2)], fill="#FF7043")
    draw.polygon([(cx - 8, by - 8), (cx, by - 16), (cx + 8, by - 5)], fill="#FFD54F")


def draw_ill_6_berlin(draw, bbox):
    """6. Berlin Diplomacy: EU Circle of Stars + Table."""
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], fill="#0F2042") # EU Blue

    cx, cy = x + w * 0.5, y + h * 0.48
    r = min(w, h) * 0.32

    # Circle of 12 stars
    for i in range(12):
        angle = i * (2 * math.pi / 12) - math.pi / 2
        sx = cx + r * math.cos(angle)
        sy = cy + r * math.sin(angle)
        draw_star(draw, (sx, sy), 5, 2.5, points=5, fill="#FFD700")

    # Central diplomatic negotiation table
    draw.ellipse([cx - w * 0.18, cy - h * 0.12, cx + w * 0.18, cy + h * 0.12], fill="#1E3A8A", outline="#60A5FA", width=2)


def draw_ill_7_riyadh(draw, bbox):
    """7. Riyadh PIF Tower: Tall skyscraper silhouette with impact mark."""
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], fill="#221A28") # Dusk Sky

    cx = x + w * 0.5
    # PIF Tower silhouette
    tw = w * 0.24
    ty0 = y + h * 0.12
    ty1 = y + h * 0.90

    # Tapered tower
    tower_pts = [
        (cx - tw * 0.3, ty0),
        (cx + tw * 0.3, ty0),
        (cx + tw * 0.5, ty1),
        (cx - tw * 0.5, ty1),
    ]
    draw.polygon(tower_pts, fill="#4A5568", outline="#718096")

    # Impact burst mark on upper middle floor
    imp_y = y + h * 0.38
    draw.polygon([(cx - 14, imp_y - 6), (cx - 2, imp_y - 12), (cx + 12, imp_y - 4), (cx + 4, imp_y + 8), (cx - 8, imp_y + 6)], fill="#FFAB40")
    draw.ellipse([cx - 4, imp_y - 4, cx + 4, imp_y + 4], fill="#FFD54F")


def draw_ill_8_hormuz(draw, bbox):
    """8. Strait of Hormuz Tanker: Tanker ship + flame in narrow strait."""
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], fill="#0F172A") # Water background

    # Coastline masses top and bottom
    draw.polygon([(x, y), (x + w, y), (x + w, y + h * 0.25), (x + w * 0.6, y + h * 0.35), (x, y + h * 0.20)], fill="#334155")
    draw.polygon([(x, y + h), (x + w, y + h), (x + w, y + h * 0.75), (x + w * 0.4, y + h * 0.65), (x, y + h * 0.80)], fill="#334155")

    # Tanker Ship in center channel
    sx = x + w * 0.30
    sy = y + h * 0.48
    ship_pts = [
        (sx, sy),
        (sx + w * 0.35, sy),
        (sx + w * 0.42, sy + 10),
        (sx - w * 0.04, sy + 10),
    ]
    draw.polygon(ship_pts, fill="#64748B")
    # Superstructure
    draw.rectangle([sx + w * 0.05, sy - 8, sx + w * 0.12, sy], fill="#94A3B8")

    # Fire / Flame on ship
    fx = sx + w * 0.22
    fy = sy - 4
    draw.polygon([(fx - 8, fy), (fx, fy - 16), (fx + 4, fy - 6), (fx + 10, fy - 18), (fx + 12, fy)], fill="#F97316")
    draw.polygon([(fx - 3, fy), (fx + 2, fy - 10), (fx + 7, fy)], fill="#EF4444")


def draw_ill_9_gaza(draw, bbox):
    """9. Gaza Yellow Line: Map area with prominent yellow dashed line."""
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], fill="#29261D") # Earthy dark tone

    # Grid map lines
    for i in range(1, 5):
        draw.line([(x + w * (i / 5.0), y), (x + w * (i / 5.0), y + h)], fill="#3D3A2F", width=1)

    # Dashed Yellow Line corridor across map
    ly = y + h * 0.5
    for dash_x in range(int(x + w * 0.08), int(x + w * 0.92), 16):
        draw.line([(dash_x, ly), (dash_x + 10, ly)], fill="#FACC15", width=4)

    # Military indicator / watchtower
    cx = x + w * 0.5
    draw.rectangle([cx - 10, ly - 22, cx + 10, ly - 10], fill="#D97706")
    draw.polygon([(cx - 10, ly - 22), (cx, ly - 30), (cx + 10, ly - 22)], fill="#B45309")


def draw_ill_10_cop31(draw, bbox):
    """10. COP31 Climate: Globe + Leaf + strike-through oil drop."""
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], fill="#142E23") # Dark Green

    cx, cy = x + w * 0.5, y + h * 0.5
    r = min(w, h) * 0.35

    # Globe circle
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#1E4636", outline="#34D399", width=2)
    draw.ellipse([cx - r * 0.5, cy - r, cx + r * 0.5, cy + r], outline="#22C55E", width=1)
    draw.line([(cx - r, cy), (cx + r, cy)], fill="#22C55E", width=1)

    # Leaf silhouette
    leaf_pts = [
        (cx - 10, cy + 15),
        (cx - 20, cy - 10),
        (cx, cy - 25),
        (cx + 20, cy - 10),
        (cx + 10, cy + 15),
    ]
    draw.polygon(leaf_pts, fill="#10B981")

    # Strike-through red line
    draw.line([(cx - r * 0.7, cy + r * 0.7), (cx + r * 0.7, cy - r * 0.7)], fill="#EF4444", width=3)


def draw_ill_11_bepicolombo(draw, bbox):
    """11. BepiColombo: Mercury planet with oversized core + orbiting probe."""
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], fill="#0B0F19") # Space Black

    cx, cy = x + w * 0.45, y + h * 0.5
    r = min(w, h) * 0.34

    # Mercury planet body
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#475569")
    # Oversized core inner circle
    draw.ellipse([cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7], fill="#64748B", outline="#94A3B8", width=2)

    # Orbit ellipse line
    draw.ellipse([cx - r * 1.3, cy - r * 0.6, cx + r * 1.3, cy + r * 0.6], outline="#38BDF8", width=1)

    # Probe on orbit
    px = cx + r * 1.1
    py = cy - r * 0.3
    draw.rectangle([px - 6, py - 4, px + 6, py + 4], fill="#CBD5E1")
    # Solar wings
    draw.line([(px - 16, py), (px + 16, py)], fill="#38BDF8", width=3)


def draw_ill_12_voyager(draw, bbox):
    """12. Voyager 1: Spacecraft + distance beam from Sun."""
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], fill="#090D16") # Deep Space

    # Sun dot left
    sx, sy = x + w * 0.12, y + h * 0.5
    draw.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill="#FBBF24")

    # Distance ray stretching right
    draw.line([(sx, sy), (x + w * 0.8, sy)], fill="#F59E0B", width=2)

    # Voyager 1 probe
    vx, vy = x + w * 0.75, sy
    # Dish antenna
    draw.arc([vx - 14, vy - 14, vx + 14, vy + 14], start=110, end=250, fill="#E2E8F0", width=3)
    # Body bus
    draw.rectangle([vx + 2, vy - 4, vx + 10, vy + 4], fill="#94A3B8")
    # Magnetometer boom
    draw.line([(vx + 10, vy), (vx + 24, vy - 10)], fill="#CBD5E1", width=1)


def draw_ill_13_gta(draw, bbox):
    """13. GTA VI: Controller silhouette + Roman numeral VI."""
    x, y, w, h = bbox
    # Neon Vice City Gradient background approximation
    draw.rectangle([x, y, x + w, y + h], fill="#3B0764") # Purple
    draw.rectangle([x, y + h * 0.5, x + w, y + h], fill="#831843") # Deep Pink

    cx, cy = x + w * 0.5, y + h * 0.48

    # Game controller outline
    cw, ch = w * 0.55, h * 0.45
    draw_rounded_rect(draw, [cx - cw * 0.5, cy - ch * 0.5, cx + cw * 0.5, cy + ch * 0.5], radius=10, fill="#1E1B4B", outline="#F43F5E", width=2)

    # Roman numeral VI
    f = get_font("ExtraCondensedBold", int(h * 0.42))
    w_vi, _ = measure_text("VI", f, draw)
    draw.text((cx - w_vi / 2, cy - h * 0.24), "VI", font=f, fill="#FACC15")


def draw_ill_14_nvidia(draw, bbox):
    """14. Nvidia: Microchip with Subpoena stamp."""
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], fill="#0F172A") # Dark Slate

    cx, cy = x + w * 0.5, y + h * 0.5
    cs = min(w, h) * 0.52

    # Microchip body
    draw.rectangle([cx - cs * 0.5, cy - cs * 0.5, cx + cs * 0.5, cy + cs * 0.5], fill="#1E293B", outline="#22C55E", width=2)
    # Inner silicon die
    draw.rectangle([cx - cs * 0.28, cy - cs * 0.28, cx + cs * 0.28, cy + cs * 0.28], fill="#0F172A", outline="#4ADE80", width=1)

    # Pin grid indicators
    for i in range(-3, 4, 2):
        draw.line([(cx + i * 8, cy - cs * 0.5), (cx + i * 8, cy - cs * 0.5 - 6)], fill="#22C55E", width=2)
        draw.line([(cx + i * 8, cy + cs * 0.5), (cx + i * 8, cy + cs * 0.5 + 6)], fill="#22C55E", width=2)

    # Subpoena Stamp Banner across
    draw.rectangle([x + w * 0.1, cy - 12, x + w * 0.9, cy + 12], fill="#DC2626")
    stamp_f = get_font("ExtraCondensedBold", 13)
    sw, _ = measure_text("SUBPOENAED", stamp_f, draw)
    draw.text((cx - sw / 2, cy - 7), "SUBPOENAED", font=stamp_f, fill="#FFFFFF")


ILL_FUNCTIONS = {
    1: draw_ill_1_icj,
    2: draw_ill_2_summit,
    3: draw_ill_3_ipo,
    4: draw_ill_4_markets,
    5: draw_ill_5_crimea,
    6: draw_ill_6_berlin,
    7: draw_ill_7_riyadh,
    8: draw_ill_8_hormuz,
    9: draw_ill_9_gaza,
    10: draw_ill_10_cop31,
    11: draw_ill_11_bepicolombo,
    12: draw_ill_12_voyager,
    13: draw_ill_13_gta,
    14: draw_ill_14_nvidia
}

KICKER_CHIPS = {
    1: "9-6 VOTE",
    2: "SHENZHEN SUMMIT",
    3: "ANTH $81bn IPO",
    4: "S&P -2.02%",
    5: "BRIDGE STRIKE",
    6: "BERLIN TALKS",
    7: "RIYADH TOWER",
    8: "HORMUZ TANKER",
    9: "GAZA YELLOW LINE",
    10: "COP31 DRAFT",
    11: "MERCURY ORBIT",
    12: "1 LIGHT-DAY",
    13: "24.58M COPIES",
    14: "NVIDIA SUBPOENA"
}


# -----------------------------------------------------------------------------
# 5. CARD RENDERER
# -----------------------------------------------------------------------------

CATEGORY_COLORS = {
    "ASIA/LEGAL": COLORS["red_accent"],
    "ASIA/DIPLOMACY": COLORS["blue_accent"],
    "BUSINESS/TECH": COLORS["blue_accent"],
    "MARKETS": COLORS["red_accent"],
    "EUROPE/WAR": COLORS["teal_accent"],
    "EUROPE/DIPLOMACY": COLORS["teal_accent"],
    "MIDDLE EAST": COLORS["amber_accent"],
    "MIDDLE EAST/ENERGY": COLORS["amber_accent"],
    "CLIMATE": COLORS["green_accent"],
    "SPACE": COLORS["dark_navy"],
    "CULTURE/GAMES": COLORS["purple_accent"],
    "TECH": COLORS["red_accent"],
}

def draw_card(draw, card_data, bbox):
    """
    Renders a standard news story card inside bbox = (x, y, width, height).
    """
    x, y, w, h = bbox
    rank = card_data.get("rank", 1)
    category = card_data.get("category", "WORLD")
    source = card_data.get("source", "REUTERS")
    text = card_data.get("text", "")

    # Card background & clean border
    draw_rounded_rect(draw, [x, y, x + w, y + h], radius=4, fill=COLORS["card_bg"], outline=COLORS["card_border"], width=1)

    pad = 6
    inner_w = w - 2 * pad
    
    # 1. Illustration Band
    ill_h = int(h * 0.52)
    ill_bbox = (x + pad, y + pad, inner_w, ill_h)
    
    ill_fn = ILL_FUNCTIONS.get(rank, draw_ill_1_icj)
    ill_fn(draw, ill_bbox)

    # Kicker Chip Top-Left inside illustration
    chip_text = KICKER_CHIPS.get(rank, category)
    chip_f = get_font("ExtraCondensedBold", 10)
    cw, ch = measure_text(chip_text, chip_f, draw)
    chip_pad = 4
    draw_rounded_rect(draw, [x + pad + 4, y + pad + 4, x + pad + 4 + cw + 2 * chip_pad, y + pad + 4 + ch + 2 * chip_pad], radius=3, fill="#101418")
    draw.text((x + pad + 4 + chip_pad, y + pad + 4 + chip_pad), chip_text, font=chip_f, fill="#FFFFFF")

    # 2. Metadata / Kicker Line under illustration
    curr_y = y + pad + ill_h + 4
    cat_color = CATEGORY_COLORS.get(category, COLORS["ink"])
    kicker_f = get_font("ExtraCondensedBold", 10)
    meta_left = f"{rank}. {category}"
    draw.text((x + pad, curr_y), meta_left, font=kicker_f, fill=cat_color)

    src_f = get_font("Italic", 9)
    src_text = f"Src: {source}"
    sw, _ = measure_text(src_text, src_f, draw)
    draw.text((x + w - pad - sw, curr_y), src_text, font=src_f, fill=COLORS["text_grey"])

    curr_y += 14

    # 3. Headline & Standfirst Text Fitting
    rem_h = (y + h - pad) - curr_y
    head_max_h = int(rem_h * 0.58)
    body_max_h = rem_h - head_max_h

    # Split story text into headline and standfirst
    sentences = text.split(". ")
    if len(sentences) >= 2:
        headline_str = sentences[0] + "."
        standfirst_str = ". ".join(sentences[1:])
    else:
        headline_str = text
        standfirst_str = ""

    # Fit Headline (Bold ExtraCondensed or Bold)
    head_font, head_lines, head_lh = fit_text_to_box(
        headline_str,
        "ExtraCondensedBold",
        inner_w,
        head_max_h,
        start_size=15,
        min_size=10,
        max_lines=2,
        draw=draw
    )
    curr_y = draw_wrapped_text(draw, head_lines, head_font, x + pad, curr_y, inner_w, head_lh, color=COLORS["ink"], spacing=1)

    # Fit Standfirst if space allows
    curr_y += 2
    body_rem_h = (y + h - pad) - curr_y
    if body_rem_h >= 12 and standfirst_str:
        body_font, body_lines, body_lh = fit_text_to_box(
            standfirst_str,
            "Regular",
            inner_w,
            body_rem_h,
            start_size=10,
            min_size=8,
            max_lines=2,
            draw=draw
        )
        draw_wrapped_text(draw, body_lines, body_font, x + pad, curr_y, inner_w, body_lh, color=COLORS["text_grey"], spacing=1)
