"""
V4 renderer: broadsheet front page of Thursday 19 November 2026.
Readability-first with breadth: 3 hero + 3 secondary + 4 compact cards, 18 curated extras.
Facts come ONLY from draw_data.py (verified news-data.md). 1024x1024, flat colors, quantized <=256 colors.
"""
from PIL import Image, ImageDraw
from draw_lib import (
    COLORS, get_font, measure_text, wrap_text, fit_text_to_box, draw_wrapped_text,
    draw_rounded_rect, draw_ill_1_icj, draw_ill_2_summit, draw_ill_3_ipo,
    draw_ill_5_crimea, draw_ill_7_riyadh, draw_ill_10_cop31, draw_ill_13_gta,
)

W, H = 1024, 1024
MARGIN = 30
INK = COLORS["ink"]
GREY = COLORS["text_grey"]
RED = COLORS["red_accent"]
BORDER = COLORS["card_border"]
PAPER = COLORS["bg_paper"]
CHIP_COL = {"REPORTED": "#2E7D32", "CLAIM": "#B26A00", "FORECAST": "#1565C0"}

def chip(draw, x, y, label, bg):
    f = get_font("ExtraCondensedBold", 10)
    tw, _ = measure_text(label, f, draw)
    draw_rounded_rect(draw, [x, y, x + tw + 12, y + 15], radius=3, fill=bg)
    draw.text((x + 6, y + 2), label, font=f, fill="#FFFFFF")

def kicker(draw, x, y, text, status=None):
    f = get_font("ExtraCondensedBold", 13)
    draw.text((x, y), text, font=f, fill=RED)
    if status:
        kw, _ = measure_text(text, f, draw)
        chip(draw, x + kw + 8, y, status, CHIP_COL[status])

def draw_ill_clipped(base_img, ill_fn, box):
    x, y, w, h = box
    tmp = Image.new("RGB", (max(1, int(w)), max(1, int(h))), PAPER)
    td = ImageDraw.Draw(tmp)
    ill_fn(td, (0, 0, w, h))
    base_img.paste(tmp, (int(x), int(y)))

def draw_story_card(draw, bbox, ill_fn, kick, status, headline, standfirst, source, ill_h, head_start, head_min, head_lines, sf_size):
    x, y, w, h = bbox
    draw_rounded_rect(draw, [x, y, x + w, y + h], radius=4, fill="#FFFFFF", outline=BORDER)
    if ill_fn:
        draw_ill_clipped(BASE_IMG, ill_fn, (x + 2, y + 2, w - 4, ill_h))
    cy = y + (ill_h + 8 if ill_fn else 10)
    pad = 12
    kicker(draw, x + pad, cy, kick, status)
    cy += 21
    hf, hlines, hlh = fit_text_to_box(headline, "ExtraCondensedBold", w - 2 * pad, head_lines * (head_start + 8), start_size=head_start, min_size=head_min, max_lines=head_lines, draw=draw)
    cy = draw_wrapped_text(draw, hlines, hf, x + pad, cy, w - 2 * pad, hlh, color=INK, spacing=3)
    cy += 4
    sf, slines, slh = fit_text_to_box(standfirst, "Regular", w - 2 * pad, 2 * (sf_size + 4), start_size=sf_size, min_size=12, max_lines=2, draw=draw)
    draw_wrapped_text(draw, slines, sf, x + pad, cy, w - 2 * pad, slh, color=GREY, spacing=2)
    src_f = get_font("Italic", 11)
    draw.text((x + pad, y + h - 18), source, font=src_f, fill=GREY)

def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    global BASE_IMG
    BASE_IMG = img

    # 1. MASTHEAD
    strip_f = get_font("ExtraCondensedBold", 15)
    draw.text((MARGIN, 10), "THE WORLD IN ONE DAY", font=strip_f, fill=RED)
    rt = "ONE PAGE · EVERY STORY FROM THIS ONE DAY"
    rw, _ = measure_text(rt, strip_f, draw)
    draw.text((W - MARGIN - rw, 10), rt, font=strip_f, fill=GREY)
    date_f = get_font("ExtraCondensedBold", 58)
    draw.text((MARGIN - 2, 26), "Thursday 19 November 2026", font=date_f, fill=INK)
    sf_f = get_font("Italic", 18)
    draw.text((MARGIN, 94), "Trump, Xi and Putin share one table  ·  GTA VI launches to 24.58M copies  ·  Anthropic's record IPO debuts", font=sf_f, fill=GREY)
    draw.line([(MARGIN, 122), (W - MARGIN, 122)], fill=INK, width=2)

    # 2. NUMBERS STRIP
    stats = [("S&P 500", "-2.02%"), ("Nikkei", "-4.68%"), ("Brent", "$89.72"), ("Gold", "$3,729"), ("Bitcoin", "$62.2K"), ("Anthropic raise", "$81bn"), ("GTA VI day one", "24.58M"), ("Voyager 1", "26bn km")]
    ny, nh = 130, 58
    cw = (W - 2 * MARGIN - 7 * 6) / 8
    for i, (lbl, val) in enumerate(stats):
        cx = MARGIN + i * (cw + 6)
        draw_rounded_rect(draw, [cx, ny, cx + cw, ny + nh], radius=3, fill="#EFECE6", outline=BORDER)
        vf = get_font("ExtraCondensedBold", 21)
        vw, _ = measure_text(val, vf, draw)
        draw.text((cx + (cw - vw) / 2, ny + 5), val, font=vf, fill=INK)
        lf = get_font("Regular", 10)
        lw, _ = measure_text(lbl, lf, draw)
        draw.text((cx + (cw - lw) / 2, ny + 37), lbl, font=lf, fill=GREY)

    # 3. HERO ROW
    hy, hh = 198, 284
    hw = (W - 2 * MARGIN - 2 * 16) / 3
    heroes = [
        (draw_ill_2_summit, "SHENZHEN · SUMMIT", "REPORTED", "Trump, Xi and Putin hold first three-way summit", "Four-point declaration: nuclear risk, UN reform, oil and gas, court limits. No Ukraine or Iran mention.", "AP · AFP"),
        (draw_ill_13_gta, "GAMES · CULTURE", "REPORTED", "GTA VI out after 13-year wait; \"GTA flu\" hits work", "24.58M day-one copies (~$2.36bn); global leave +32% (Remote), UK sick +56%.", "Rockstar · Guardian · Independent"),
        (draw_ill_3_ipo, "NASDAQ · MARKETS", "REPORTED", "Anthropic debuts up 17% after history's largest IPO", "$83 offer, opened ~$111.50, raised ~$81bn at a ~$1.5tn valuation.", "Reuters · CNBC"),
    ]
    for i, (ill, k, st, hl, sf, src) in enumerate(heroes):
        draw_story_card(draw, (MARGIN + i * (hw + 16), hy, hw, hh), ill, k, st, hl, sf, src, ill_h=136, head_start=28, head_min=21, head_lines=3, sf_size=14)

    # 4. SECONDARY ROW
    sy, sh = 492, 200
    secs = [
        (draw_ill_5_crimea, "CRIMEA · WAR", "REPORTED", "Ukraine hits Crimean Bridge third time in four days", "Russia halts traffic; span damage visible.", "AFP"),
        (draw_ill_7_riyadh, "RIYADH · GULF", "CLAIM", "Houthi missile hits Riyadh's tallest tower", "PIF Tower windows broken; no injuries reported.", "AFP · SPA"),
        (draw_ill_10_cop31, "COP31 · CLIMATE", "REPORTED", "COP31 draft drops fossil-fuel language", "African nations demand more climate finance.", "Reuters"),
    ]
    for i, (ill, k, st, hl, sf, src) in enumerate(secs):
        draw_story_card(draw, (MARGIN + i * (hw + 16), sy, hw, sh), ill, k, st, hl, sf, src, ill_h=56, head_start=21, head_min=16, head_lines=2, sf_size=12)

    # 5. COMPACT ROW (4 text cards)
    ty, th = 700, 148
    tw = (W - 2 * MARGIN - 3 * 12) / 4
    minis = [
        ("BERLIN · DIPLOMACY", "REPORTED", "European allies claim united line for Russia talks", "Kushner cites Article 5-style guarantees for Ukraine.", "Reuters"),
        ("HORMUZ · ENERGY", "REPORTED", "Tanker ablaze after mine as Iran steps up attacks", "Senate rejects war-powers curb 51-48; Brent $89.72.", "Reuters · IEA"),
        ("GAZA · CEASEFIRE", "REPORTED", "First Israeli ground op past the Yellow Line", "Army says a tunnel was dismantled; Hamas calls it a violation.", "AP"),
        ("THE HAGUE · JUSTICE", "REPORTED", "World Court: Myanmar committed genocide", "9-6: ICJ holds Myanmar responsible for 2017 Rohingya genocide.", "ICJ · Reuters"),
    ]
    for i, (k, st, hl, sf, src) in enumerate(minis):
        draw_story_card(draw, (MARGIN + i * (tw + 12), ty, tw, th), None, k, st, hl, sf, src, ill_h=0, head_start=16, head_min=12, head_lines=3, sf_size=11)

    # 6. EXTRAS PANEL
    ey, eh = 856, 128
    draw_rounded_rect(draw, [MARGIN, ey, W - MARGIN, ey + eh], radius=4, fill="#FFFFFF", outline=BORDER)
    et_f = get_font("ExtraCondensedBold", 15)
    draw.text((MARGIN + 12, ey + 6), "ALSO ON THURSDAY 19 NOVEMBER", font=et_f, fill=RED)
    extras = [
        ("TECH", "Nvidia subpoenaed over China chip disclosures"),
        ("SPACE", "BepiColombo enters Mercury orbit, second ever"),
        ("SPACE", "Voyager 1 now a full light-day from Earth"),
        ("ODISHA", "Cyclone Akvan nears India; landfall due Friday"),
        ("DHAKA", "Hasina supporters torch property; ~300 arrests"),
        ("DAKAR", "Dozens missing after migrant boat capsizes"),
        ("CARACAS", "US and Venezuela sign military cooperation"),
        ("NAIROBI", "US consortium wins Mrima Hill minerals deal"),
        ("COPENHAGEN", "Parliament ratifies US-Greenland pact"),
        ("GENEVA", "589 million children live in conflict zones"),
        ("COX'S BAZAR", "Rohingya refugees cheer the ICJ verdict"),
        ("GAZA", "Abu Safiya's detention extended 6 months"),
        ("WASHINGTON", "Democrats grill DHS chief over FAA stop"),
        ("MADRID", "Sánchez admits mistakes; Spain votes 29 Nov"),
        ("CAIRO", "IMF deal unlocks $2.3bn for Egypt"),
        ("JUNEAU", "Peltola wins Alaska seat; Democrats reach 56"),
        ("BANGKOK", "Iran keeper Beiranvand named AFC's best"),
        ("MANCHESTER", "Pochettino starts as Man United coach"),
    ]
    item_f = get_font("Regular", 12)
    lead_f = get_font("ExtraCondensedBold", 12)
    col_w = (W - 2 * MARGIN - 24) / 3
    for i, (lead, txt) in enumerate(extras):
        col, row = divmod(i, 6)
        ix = MARGIN + 12 + col * (col_w + 12)
        iy = ey + 28 + row * 16
        draw.text((ix, iy), lead, font=lead_f, fill=INK)
        lw, _ = measure_text(lead, lead_f, draw)
        draw.text((ix + lw + 5, iy), txt, font=item_f, fill=GREY)

    # 7. FOOTER / DATE CHECK
    fy = 990
    draw.line([(MARGIN, fy - 6), (W - MARGIN, fy - 6)], fill=BORDER, width=1)
    dc_f = get_font("ExtraCondensedBold", 12)
    draw.text((MARGIN, fy), "DATE CHECK", font=dc_f, fill=RED)
    dw, _ = measure_text("DATE CHECK", dc_f, draw)
    # hand-drawn check mark (font has no check glyph)
    draw.line([(MARGIN + dw + 6, fy + 7), (MARGIN + dw + 10, fy + 11)], fill="#2E7D32", width=2)
    draw.line([(MARGIN + dw + 10, fy + 11), (MARGIN + dw + 18, fy + 2)], fill="#2E7D32", width=2)
    dct_f = get_font("Regular", 11)
    draw.text((MARGIN + dw + 24, fy), "Every story here happened, or was first reported, on 19 November 2026. Gold/BTC: 19 Nov quotes (Reuters). Left out: EU loan (18th) · COP31 close (20th) · Akvan landfall (20th)", font=dct_f, fill=GREY)
    draw.text((MARGIN, fy + 17), "Claims are attributed, not stated as fact · Sources: Reuters, AP, AFP, BBC, Euronews, ICJ, NASA, ESA, IMD · Original drawings", font=dct_f, fill=GREY)

    img = img.quantize(colors=256, method=Image.MEDIANCUT).convert("RGB")
    img.save("entry.png", optimize=True)
    import os
    print(f"Successfully generated {os.path.abspath('entry.png')} (size: {os.path.getsize('entry.png')} bytes)")

if __name__ == "__main__":
    main()
