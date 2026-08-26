import os
import html
import random
import xml.etree.ElementTree as ET
from PIL import Image, ImageEnhance, ImageOps

def create_ascii_svg():
    img_path = "saswatt.jpeg"
    if not os.path.exists(img_path):
        print("Image not found:", img_path)
        return

    img = Image.open(img_path)
    # Focus on head, hair, glasses, face & collar
    # Image is (1067, 1600)
    face = img.crop((260, 140, 800, 800))

    # Convert to grayscale
    gray = face.convert("L")

    # High quality enhancement
    gray = ImageOps.autocontrast(gray, cutoff=(1, 1))
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(1.4)
    sharp = ImageEnhance.Sharpness(gray)
    gray = sharp.enhance(1.8)

    width = 58
    char_aspect = 0.52
    height = int(width * (gray.height / gray.width) * char_aspect)
    resized = gray.resize((width, height), Image.Resampling.LANCZOS)

    # Safe characters for XML (no raw & < > " ')
    ramp = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    pixels = list(resized.getdata())

    random.seed(42)
    lines = []
    glitch_lines = []

    for r in range(height):
        line = ""
        g_line = ""
        for c in range(width):
            val = pixels[r * width + c]
            idx = int(val / 256 * len(ramp))
            if idx >= len(ramp):
                idx = len(ramp) - 1
            char = ramp[idx]
            line += char
            
            # Glitch frame: occasionally shift or replace with matrix symbols
            if random.random() < 0.04:
                g_char = random.choice("01/[]{}~#@*+=-")
            else:
                g_char = char
            g_line += g_char

        lines.append(line)
        glitch_lines.append(g_line)

    svg_width = 480
    svg_height = 580

    text_spans = []
    text_spans_glitch = []
    y_start = 74
    line_spacing = 11.2

    for i, line in enumerate(lines):
        escaped = html.escape(line, quote=True)
        y = y_start + i * line_spacing
        text_spans.append(f'<tspan x="22" y="{y:.1f}">{escaped}</tspan>')

    for i, line in enumerate(glitch_lines):
        escaped = html.escape(line, quote=True)
        y = y_start + i * line_spacing
        text_spans_glitch.append(f'<tspan x="22" y="{y:.1f}">{escaped}</tspan>')

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="100%">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080c14" stop-opacity="0.97"/>
      <stop offset="45%" stop-color="#0d1117" stop-opacity="0.98"/>
      <stop offset="100%" stop-color="#19092b" stop-opacity="0.97"/>
    </linearGradient>

    <linearGradient id="neonBorder" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#A855F7">
        <animate attributeName="stop-color" values="#A855F7;#22D3EE;#F472B6;#7B2CBF;#A855F7" dur="6s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" stop-color="#22D3EE">
        <animate attributeName="stop-color" values="#22D3EE;#F472B6;#A855F7;#22D3EE" dur="6s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#F472B6">
        <animate attributeName="stop-color" values="#F472B6;#7B2CBF;#22D3EE;#F472B6" dur="6s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <linearGradient id="asciiTextGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#C084FC"/>
      <stop offset="35%" stop-color="#F1F5F9"/>
      <stop offset="70%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#F472B6"/>
    </linearGradient>

    <linearGradient id="hoverTextGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22D3EE"/>
      <stop offset="50%" stop-color="#A855F7"/>
      <stop offset="100%" stop-color="#F472B6"/>
    </linearGradient>

    <linearGradient id="scanlineGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#22D3EE" stop-opacity="0"/>
      <stop offset="50%" stop-color="#22D3EE" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#A855F7" stop-opacity="0"/>
    </linearGradient>

    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <style>
    .ascii-card {{
      cursor: pointer;
      transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), filter 0.4s ease;
      transform-origin: center center;
    }}
    .ascii-card:hover {{
      transform: translateY(-8px) scale(1.025);
      filter: drop-shadow(0 0 24px rgba(168, 85, 247, 0.5)) drop-shadow(0 0 45px rgba(34, 211, 238, 0.3));
    }}
    .ascii-art {{
      font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Courier New', monospace;
      font-size: 8px;
      font-weight: 700;
      letter-spacing: 1.1px;
      fill: url(#asciiTextGrad);
      transition: fill 0.3s ease, letter-spacing 0.3s ease, transform 0.3s ease;
    }}
    .ascii-card:hover .ascii-art {{
      fill: url(#hoverTextGrad);
      letter-spacing: 1.25px;
    }}
    .scanline {{
      animation: scanAnim 3.6s linear infinite;
    }}
    .ascii-card:hover .scanline {{
      animation: scanAnim 1.4s linear infinite;
    }}
    @keyframes scanAnim {{
      0% {{ transform: translateY(40px); opacity: 0; }}
      12% {{ opacity: 1; }}
      88% {{ opacity: 1; }}
      100% {{ transform: translateY(500px); opacity: 0; }}
    }}
    .floating-hud {{
      animation: hudFloat 4.5s ease-in-out infinite;
    }}
    @keyframes hudFloat {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(-4px); }}
    }}
    .status-blink {{
      animation: blinkLed 1.2s infinite;
    }}
    @keyframes blinkLed {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.2; }}
    }}
    .grid-line {{
      stroke: rgba(168, 85, 247, 0.12);
      stroke-width: 1;
    }}
    .glitch-layer {{
      opacity: 0;
      animation: glitchFlash 4.5s infinite;
    }}
    @keyframes glitchFlash {{
      0%, 92%, 100% {{ opacity: 0; transform: translateX(0); }}
      93% {{ opacity: 0.85; transform: translateX(-2.5px); fill: #22D3EE; }}
      95% {{ opacity: 0.95; transform: translateX(2.5px); fill: #F472B6; }}
      97% {{ opacity: 0.5; transform: translateX(-1px); fill: #A855F7; }}
    }}
    .corner-bracket {{
      stroke: #22D3EE;
      stroke-width: 2.5;
      fill: none;
      filter: url(#glow);
      transition: stroke 0.3s ease;
    }}
    .ascii-card:hover .corner-bracket {{
      stroke: #F472B6;
    }}
  </style>

  <!-- Interactive Card -->
  <g class="ascii-card">
    <!-- Card Frame -->
    <rect x="6" y="6" width="{svg_width - 12}" height="{svg_height - 12}" rx="16" fill="url(#cardGrad)" stroke="url(#neonBorder)" stroke-width="2.2" />

    <!-- HUD Grid lines -->
    <line x1="6" y1="46" x2="{svg_width - 6}" y2="46" class="grid-line" stroke-width="1.5" stroke="rgba(168,85,247,0.25)"/>
    <line x1="6" y1="{svg_height - 40}" x2="{svg_width - 6}" y2="{svg_height - 40}" class="grid-line" stroke-width="1.5" stroke="rgba(34,211,238,0.25)"/>

    <!-- Sci-Fi Corner Brackets -->
    <path d="M 16 26 L 16 16 L 26 16" class="corner-bracket" />
    <path d="M {svg_width - 26} 16 L {svg_width - 16} 16 L {svg_width - 16} 26" class="corner-bracket" />
    <path d="M 16 {svg_height - 26} L 16 {svg_height - 16} L 26 {svg_height - 16}" class="corner-bracket" />
    <path d="M {svg_width - 26} {svg_height - 16} L {svg_width - 16} {svg_height - 16} L {svg_width - 16} {svg_height - 26}" class="corner-bracket" />

    <!-- Top Status Bar -->
    <g transform="translate(18, 20)">
      <circle cx="6" cy="6" r="4.5" fill="#EF4444" opacity="0.85"/>
      <circle cx="20" cy="6" r="4.5" fill="#F59E0B" opacity="0.85"/>
      <circle cx="34" cy="6" r="4.5" fill="#10B981" opacity="0.85"/>

      <!-- Live Bio-Matrix Badge -->
      <g transform="translate(56, -2)">
        <rect x="0" y="0" width="112" height="17" rx="4" fill="rgba(168,85,247,0.18)" stroke="#A855F7" stroke-width="0.8"/>
        <circle cx="8" cy="8.5" r="3.2" fill="#22D3EE" class="status-blink"/>
        <text x="18" y="12" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="700" fill="#22D3EE" letter-spacing="0.5">BIO-ASCII v4.2</text>
      </g>

      <text x="{svg_width - 48}" y="11" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="9" fill="#94A3B8" font-weight="600">SYS::SASWAT_MOHANTY</text>
    </g>

    <!-- ASCII Motion Artwork -->
    <g class="floating-hud">
      <!-- Primary Stream -->
      <text class="ascii-art" xml:space="preserve">
        {"".join(text_spans)}
      </text>

      <!-- Glitch Stream -->
      <text class="ascii-art glitch-layer" xml:space="preserve">
        {"".join(text_spans_glitch)}
      </text>
    </g>

    <!-- Holographic Laser Scanline -->
    <g>
      <rect class="scanline" x="10" y="0" width="{svg_width - 20}" height="20" fill="url(#scanlineGrad)" opacity="0.75" />
    </g>

    <!-- Bottom Telemetry HUD Bar -->
    <g transform="translate(20, {svg_height - 23})">
      <text x="0" y="7" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="600" fill="#22D3EE">
        ⚡ HOVER / INTERACT
      </text>
      <text x="{svg_width - 40}" y="7" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="600" fill="#A855F7">
        60 FPS CYBERNETIC AVATAR
      </text>
    </g>
  </g>
</svg>
'''
    with open("ascii_avatar.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    # Verify XML
    ET.fromstring(svg_content)
    print("Generated and validated ascii_avatar.svg successfully!")

if __name__ == "__main__":
    create_ascii_svg()
