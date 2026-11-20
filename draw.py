"""
draw.py - Full page composition for news-image-20261119 (entry.png)
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont

from draw_data import (
    HEADER,
    CARD_STORIES,
    NUMBERS_BAND,
    NUMBERS_BAND_RAW,
    EXTRAS,
    DATE_CHECK,
    SOURCE_CREDITS_RAW
)
from draw_lib import (
    get_font,
    measure_text,
    wrap_text,
    fit_text_to_box,
    draw_wrapped_text,
    draw_rounded_rect,
    draw_card,
    COLORS
)

def render_page():
    W, H = 1024, 1024
    img = Image.new("RGB", (W, H), COLORS["bg_paper"])
    draw = ImageDraw.Draw(img)

    margin = 12
    curr_y = margin

    # =========================================================================
    # ROW 0: MASTHEAD (h ~ 84)
    # =========================================================================
    mh_y = curr_y
    mh_w = W - 2 * margin

    # Outer border line under masthead
    # Red date chip left
    chip_f = get_font("ExtraCondensedBold", 11)
    chip_text = "NOV 19 / THU · 2026"
    cw, ch = measure_text(chip_text, chip_f, draw)
    draw_rounded_rect(draw, [margin, mh_y, margin + cw + 12, mh_y + 20], radius=3, fill=COLORS["red_accent"])
    draw.text((margin + 6, mh_y + 3), chip_text, font=chip_f, fill="#FFFFFF")

    # Kicker
    kicker_f = get_font("ExtraCondensedBold", 11)
    draw.text((margin + cw + 20, mh_y + 3), "THE DAY IN WORLD NEWS", font=kicker_f, fill=COLORS["text_grey"])

    # Stat block right
    stat_text = "48 STORIES / 7 REGIONS / ONE PAGE"
    sw, _ = measure_text(stat_text, kicker_f, draw)
    draw.text((W - margin - sw, mh_y + 3), stat_text, font=kicker_f, fill=COLORS["blue_accent"])

    # Giant Main Title / Date
    title_f = get_font("Black", 32)
    draw.text((margin, mh_y + 24), "Thursday 19 November 2026", font=title_f, fill=COLORS["ink"])

    # Subline
    sub_f = get_font("Italic", 10.5)
    sub_text = "Every story on this page happened, or was first reported, on Thursday 19 November 2026."
    draw.text((margin, mh_y + 64), sub_text, font=sub_f, fill=COLORS["text_grey"])

    curr_y = mh_y + 82
    draw.line([(margin, curr_y), (W - margin, curr_y)], fill=COLORS["ink"], width=2)
    curr_y += 4

    # =========================================================================
    # ROW 1: REGION STRIP (h ~ 20)
    # =========================================================================
    regions = [
        ("EUROPE", "10", "#1E56A0"),
        ("AMERICAS", "9", "#B85B14"),
        ("ASIA", "8", "#D9381E"),
        ("AFRICA", "3", "#2D6A4F"),
        ("MIDDLE EAST", "6", "#8338EC"),
        ("OCEANIA", "2", "#2B7A78"),
        ("WORLD", "7", "#0F172A"),
    ]

    strip_w = W - 2 * margin
    seg_w = strip_w / len(regions)
    reg_f = get_font("ExtraCondensedBold", 10)

    for idx, (reg_name, reg_cnt, reg_col) in enumerate(regions):
        rx0 = margin + idx * seg_w
        rx1 = margin + (idx + 1) * seg_w - 2
        draw.rectangle([rx0, curr_y, rx1, curr_y + 18], fill=reg_col)
        lbl = f"{reg_name} ({reg_cnt})"
        lw, _ = measure_text(lbl, reg_f, draw)
        draw.text((rx0 + (seg_w - lw) / 2, curr_y + 2), lbl, font=reg_f, fill="#FFFFFF")

    curr_y += 22

    # =========================================================================
    # ROW 2: "THE DAY IN NUMBERS" BAND (h ~ 36)
    # =========================================================================
    num_box_h = 34
    draw_rounded_rect(draw, [margin, curr_y, W - margin, curr_y + num_box_h], radius=3, fill="#EFECE6", outline=COLORS["card_border"])

    # 6 selected key stat badges across band
    stats = [
        ("S&P 500", "-2.02%"),
        ("Nikkei", "-4.68%"),
        ("Brent", "$89.72"),
        ("GTA VI", "24.58M"),
        ("Anthropic IPO", "$81bn"),
        ("Voyager 1", "26bn km"),
    ]

    stat_start_x = margin + 8
    stat_avail_w = W - 2 * margin - 16
    stat_item_w = stat_avail_w / len(stats)

    val_f = get_font("ExtraCondensedBold", 12)
    lbl_f = get_font("Regular", 9)

    for i, (label, val) in enumerate(stats):
        sx = stat_start_x + i * stat_item_w
        vw, _ = measure_text(val, val_f, draw)
        lw, _ = measure_text(label, lbl_f, draw)
        # Center in item box
        draw.text((sx + (stat_item_w - vw) / 2, curr_y + 3), val, font=val_f, fill=COLORS["ink"])
        draw.text((sx + (stat_item_w - lw) / 2, curr_y + 18), label, font=lbl_f, fill=COLORS["text_grey"])
        if i < len(stats) - 1:
            draw.line([(sx + stat_item_w - 1, curr_y + 4), (sx + stat_item_w - 1, curr_y + 30)], fill=COLORS["card_border"], width=1)

    curr_y += num_box_h + 6

    # =========================================================================
    # ROWS 3-6: CARD GRID (14 CARDS)
    # =========================================================================
    grid_w = W - 2 * margin

    # Row 3 (3 cards: 1, 2, 3) h ~ 152
    r3_h = 152
    c3_w = (grid_w - 2 * 6) / 3
    for i in range(3):
        card_data = CARD_STORIES[i]
        cx = margin + i * (c3_w + 6)
        draw_card(draw, card_data, (cx, curr_y, c3_w, r3_h))
    curr_y += r3_h + 6

    # Row 4 (3 cards: 4, 5, 6) h ~ 152
    r4_h = 152
    for i in range(3):
        card_data = CARD_STORIES[3 + i]
        cx = margin + i * (c3_w + 6)
        draw_card(draw, card_data, (cx, curr_y, c3_w, r4_h))
    curr_y += r4_h + 6

    # Row 5 (4 cards: 7, 8, 9, 10) h ~ 128
    r5_h = 128
    c4_w = (grid_w - 3 * 5) / 4
    for i in range(4):
        card_data = CARD_STORIES[6 + i]
        cx = margin + i * (c4_w + 5)
        draw_card(draw, card_data, (cx, curr_y, c4_w, r5_h))
    curr_y += r5_h + 5

    # Row 6 (4 cards: 11, 12, 13, 14) h ~ 128
    r6_h = 128
    for i in range(4):
        card_data = CARD_STORIES[10 + i]
        cx = margin + i * (c4_w + 5)
        draw_card(draw, card_data, (cx, curr_y, c4_w, r6_h))
    curr_y += r6_h + 6

    # =========================================================================
    # ROW 7: BOTTOM SPLIT (MAP + EXTRAS) (h ~ 190)
    # =========================================================================
    bs_y = curr_y
    bs_h = 190
    map_w = 340
    extras_w = grid_w - map_w - 8

    # Left: Map Box
    draw_rounded_rect(draw, [margin, bs_y, margin + map_w, bs_y + bs_h], radius=4, fill="#111827", outline=COLORS["card_border"])
    map_title_f = get_font("ExtraCondensedBold", 11)
    draw.text((margin + 8, bs_y + 6), "WHERE IT HAPPENED (STORY MAP)", font=map_title_f, fill="#38BDF8")

    # Dotted Map Background Area
    map_area_x = margin + 8
    map_area_y = bs_y + 22
    map_area_w = map_w - 16
    map_area_h = bs_h - 30

    # Draw grid of dots for world map feeling
    for dx in range(map_area_x + 5, map_area_x + map_area_w - 5, 8):
        for dy in range(map_area_y + 5, map_area_y + map_area_h - 5, 8):
            draw.rectangle([dx, dy, dx + 1, dy + 1], fill="#1F2937")

    # Story Pins (1..14) positioned approx on world coordinates
    pins = [
        (1, 0.72, 0.50),  # Myanmar
        (2, 0.76, 0.42),  # Shenzhen
        (3, 0.22, 0.38),  # New York/Nasdaq
        (4, 0.20, 0.42),  # Wall St
        (5, 0.58, 0.32),  # Crimea
        (6, 0.50, 0.30),  # Berlin
        (7, 0.60, 0.48),  # Riyadh
        (8, 0.62, 0.52),  # Hormuz
        (9, 0.56, 0.46),  # Gaza
        (10, 0.55, 0.40), # Turkey
        (11, 0.88, 0.22), # Space Mercury
        (12, 0.92, 0.75), # Space Voyager
        (13, 0.25, 0.52), # Miami GTA
        (14, 0.15, 0.40), # California
    ]

    pin_f = get_font("ExtraCondensedBold", 9)
    for p_num, px_r, py_r in pins:
        px = int(map_area_x + px_r * map_area_w)
        py = int(map_area_y + py_r * map_area_h)
        # Red pin circle
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=COLORS["red_accent"], outline="#FFFFFF")
        num_str = str(p_num)
        nw, _ = measure_text(num_str, pin_f, draw)
        draw.text((px - nw / 2, py - 5), num_str, font=pin_f, fill="#FFFFFF")

    # Right: Extras Box (34 More Stories)
    ext_x = margin + map_w + 8
    draw_rounded_rect(draw, [ext_x, bs_y, W - margin, bs_y + bs_h], radius=4, fill=COLORS["card_bg"], outline=COLORS["card_border"])
    ext_title_f = get_font("ExtraCondensedBold", 11)
    draw.text((ext_x + 8, bs_y + 6), f"ALSO ON THURSDAY 19 NOVEMBER — {len(EXTRAS)} MORE STORIES", font=ext_title_f, fill=COLORS["red_accent"])

    # 2 columns for EXTRAS list
    ext_col_w = (extras_w - 20) / 2
    ext_f = get_font("Regular", 8)

    half_count = (len(EXTRAS) + 1) // 2
    for i, ext_item in enumerate(EXTRAS):
        col = 0 if i < half_count else 1
        row = i if col == 0 else (i - half_count)
        
        ex = ext_x + 8 + col * (ext_col_w + 8)
        ey = bs_y + 22 + row * 9.2
        
        if ey + 8 < bs_y + bs_h - 4:
            # Truncate line to col width
            fitted_f, lines, _ = fit_text_to_box(ext_item, "Regular", ext_col_w, 10, start_size=8, min_size=7, max_lines=1, draw=draw)
            if lines:
                draw.text((ex, ey), lines[0], font=fitted_f, fill=COLORS["ink"])

    curr_y = bs_y + bs_h + 5

    # =========================================================================
    # ROW 8: DATE-CHECK BOX (h ~ 32)
    # =========================================================================
    dc_h = 32
    draw_rounded_rect(draw, [margin, curr_y, W - margin, curr_y + dc_h], radius=3, fill="#FFFBEB", outline="#FCD34D")

    dc_title_f = get_font("ExtraCondensedBold", 10)
    draw.text((margin + 6, curr_y + 4), "DATE CHECK (Left out on purpose - belongs to other days):", font=dc_title_f, fill="#B45309")

    dc_body_f = get_font("Regular", 8.5)
    dc_text = " · ".join(DATE_CHECK)
    fitted_dc_f, dc_lines, _ = fit_text_to_box(dc_text, "Regular", grid_w - 12, 14, start_size=8.5, min_size=7, max_lines=1, draw=draw)
    if dc_lines:
        draw.text((margin + 6, curr_y + 17), dc_lines[0], font=fitted_dc_f, fill="#78350F")

    curr_y += dc_h + 4

    # =========================================================================
    # ROW 9: FOOTER (h ~ 16)
    # =========================================================================
    ft_f = get_font("Regular", 8)
    draw.text((margin, curr_y), f"Sources: {SOURCE_CREDITS_RAW}", font=ft_f, fill=COLORS["text_grey"])

    right_ft = "Verified World News · Original Drawings"
    rw, _ = measure_text(right_ft, ft_f, draw)
    draw.text((W - margin - rw, curr_y), right_ft, font=ft_f, fill=COLORS["text_grey"])

    # Save quantized 256 color PNG
    output_path = "/downloads/makefun/build/repo/entry.png"
    img_quant = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    img_quant.save(output_path, optimize=True)
    print(f"Successfully generated {output_path} (size: {os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    render_page()
