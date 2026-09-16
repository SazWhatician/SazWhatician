import xml.etree.ElementTree as ET
import os
from PIL import ImageFont

font_host_sb12 = ImageFont.truetype("fonts/HostGrotesk-SemiBold.ttf", 12)
font_host_reg11 = ImageFont.truetype("fonts/HostGrotesk-Regular.ttf", 11)
font_inst_reg14 = ImageFont.truetype("fonts/InstrumentSerif-Regular.ttf", 14)
font_inst_it14 = ImageFont.truetype("fonts/InstrumentSerif-Italic.ttf", 14)
font_inst_it20 = ImageFont.truetype("fonts/InstrumentSerif-Italic.ttf", 20)

def get_text_bounds(t):
    txt = t.text or ""
    f_size = float(t.attrib.get("font-size", 12))
    f_weight = t.attrib.get("font-weight", "normal")
    anchor = t.attrib.get("text-anchor", "start")
    cls = t.attrib.get("class", "")
    tx = float(t.attrib.get("x", 0))

    if "host-grotesk" in cls:
        if f_weight in ["600", "700", "bold"]:
            font = font_host_sb12
        else:
            font = font_host_reg11
    else:
        if "italic" in cls or t.attrib.get("font-style") == "italic":
            font = font_inst_it20 if f_size >= 18 else font_inst_it14
        else:
            font = font_inst_reg14


    bb = font.getbbox(txt)
    w = bb[2] - bb[0]

    if anchor == "middle":
        left = tx - w / 2.0
        right = tx + w / 2.0
    elif anchor == "end":
        left = tx - w
        right = tx
    else: # start
        left = tx
        right = tx + w

    return left, right, w, txt

def inspect_svg(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()
    viewbox = root.attrib.get("viewBox", "0 0 1000 400").split()
    card_w = float(viewbox[2])
    card_h = float(viewbox[3])

    errors = []
    print(f"\n[INSPECTING] {svg_file} (Canvas: {card_w}x{card_h})")

    for g in root.iter("{http://www.w3.org/2000/svg}g"):
        rect = g.find("{http://www.w3.org/2000/svg}rect")
        texts = g.findall("{http://www.w3.org/2000/svg}text")
        
        if rect is not None and len(texts) > 0:
            rx = float(rect.attrib.get("x", 0))
            rw = float(rect.attrib.get("width", 0))
            rect_left = rx
            rect_right = rx + rw

            for t in texts:
                t_left, t_right, t_w, txt = get_text_bounds(t)
                
                # Check containment
                left_overflow = rect_left - t_left
                right_overflow = t_right - rect_right

                if left_overflow > 0.5 or right_overflow > 0.5:
                    err = f"OVERFLOW: '{txt}' (span: {t_left:.1f}..{t_right:.1f} vs rect: {rect_left:.1f}..{rect_right:.1f}, over by {max(left_overflow, right_overflow):.1f}px)"
                    errors.append(err)
                    print(f"  [X] {err}")
                else:
                    pad_l = t_left - rect_left
                    pad_r = rect_right - t_right
                    # print(f"  [OK] '{txt[:20]}' in [{rect_left:.0f}..{rect_right:.0f}] (pads: L={pad_l:.1f}, R={pad_r:.1f})")

    if not errors:
        print(f"  --> ALL TEXT CONTAINED IN {svg_file}! (0 errors)")
    return errors

if __name__ == "__main__":
    files = [
        "assets/hero-banner.svg",
        "assets/telemetry-hud.svg",
        "assets/dr-debug-card.svg",
        "assets/polaris-card.svg",
        "assets/medscan-card.svg",
        "assets/ethos-card.svg"
    ]
    total_errs = 0
    for f in files:
        errs = inspect_svg(f)
        total_errs += len(errs)
    
    print(f"\nTOTAL VIOLATIONS FOUND: {total_errs}")
