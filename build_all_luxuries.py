import base64
import os
import xml.etree.ElementTree as ET
from PIL import Image, ImageFont

def get_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Base64 encoded WOFF2 fonts for direct zero-latency in-SVG embedding
b64_host_grotesk_normal = get_b64("fonts/HostGrotesk-Normal.woff2")
b64_host_grotesk_italic = get_b64("fonts/HostGrotesk-Italic.woff2")
b64_instrument_serif_normal = get_b64("fonts/InstrumentSerif-Normal.woff2")
b64_instrument_serif_italic = get_b64("fonts/InstrumentSerif-Italic.woff2")

SHARED_FONTS_CSS = f'''
    @import url('https://fonts.googleapis.com/css2?family=Host+Grotesk:ital,wght@0,300..800;1,300..800&amp;family=Instrument+Serif:ital@0;1&amp;display=swap');

    @font-face {{
      font-family: 'Host Grotesk';
      font-style: normal;
      font-weight: 300 800;
      font-display: swap;
      src: url(data:font/woff2;base64,{b64_host_grotesk_normal}) format('woff2');
    }}
    @font-face {{
      font-family: 'Host Grotesk';
      font-style: italic;
      font-weight: 300 800;
      font-display: swap;
      src: url(data:font/woff2;base64,{b64_host_grotesk_italic}) format('woff2');
    }}
    @font-face {{
      font-family: 'Instrument Serif';
      font-style: normal;
      font-weight: 400;
      font-display: swap;
      src: url(data:font/woff2;base64,{b64_instrument_serif_normal}) format('woff2');
    }}
    @font-face {{
      font-family: 'Instrument Serif';
      font-style: italic;
      font-weight: 400;
      font-display: swap;
      src: url(data:font/woff2;base64,{b64_instrument_serif_italic}) format('woff2');
    }}

    .host-grotesk {{
      font-family: "Host Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-optical-sizing: auto;
      font-style: normal;
    }}
    .instrument-serif-regular {{
      font-family: "Instrument Serif", Georgia, serif;
      font-weight: 400;
      font-style: normal;
    }}
    .instrument-serif-regular-italic {{
      font-family: "Instrument Serif", Georgia, serif;
      font-weight: 400;
      font-style: italic;
    }}
    .serif-brand {{
      font-family: "Instrument Serif", Georgia, serif;
    }}
    .cursive-brand {{
      font-family: "Instrument Serif", Georgia, serif;
      font-style: italic;
    }}
'''

# Font measurement setup using real TTF files
font_host_semibold12 = ImageFont.truetype("fonts/HostGrotesk-SemiBold.ttf", 12)
font_host_regular11 = ImageFont.truetype("fonts/HostGrotesk-Regular.ttf", 11)

def check_string(txt, max_w, font):
    bb = font.getbbox(txt)
    w = bb[2] - bb[0]
    assert w <= max_w, f"Text '{txt}' width {w}px exceeds allowed {max_w}px!"
    return w

def make_cell(x, y, w, h, icon_col, title, desc1, desc2, stroke_col="#74825C", fill_col="#1b0813"):
    max_w = w - 32 - 14 # 32px left indent, 14px right margin = 264px ceiling
    check_string(title, max_w, font_host_semibold12)
    check_string(desc1, max_w, font_host_regular11)
    if desc2:
        check_string(desc2, max_w, font_host_regular11)
    
    t_xml = title.replace("&", "&amp;")
    d1_xml = desc1.replace("&", "&amp;")
    d2_xml = desc2.replace("&", "&amp;") if desc2 else ""

    desc2_markup = f'<text x="32" y="58" class="host-grotesk" font-size="10.5" fill="#D8C5B2">{d2_xml}</text>' if desc2 else ''

    return f'''<g transform="translate({x}, {y})">
        <rect width="{w}" height="{h}" rx="14" fill="{fill_col}" stroke="{stroke_col}" stroke-width="0.7"/>
        <circle cx="18" cy="22" r="3" fill="{icon_col}"/>
        <text x="32" y="24" class="host-grotesk" font-weight="600" font-size="12" fill="#F6F0E6" letter-spacing="0.5">{t_xml}</text>
        <text x="32" y="42" class="host-grotesk" font-size="10.5" fill="#D8C5B2">{d1_xml}</text>
        {desc2_markup}
      </g>'''

def build_hero_banner():
    b64_damnn = get_b64("assets/damnn-opt.png")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 520" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Saswat Mohanty — Where Classical Intellect Meets Autonomous Systems">
  <defs>
    <linearGradient id="heroVelvetBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#110307">
        <animate attributeName="stop-color" values="#110307;#1a050d;#110307" dur="14s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" stop-color="#220814">
        <animate attributeName="stop-color" values="#220814;#2b0a19;#220814" dur="14s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#0e0205">
        <animate attributeName="stop-color" values="#0e0205;#15030a;#0e0205" dur="14s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <linearGradient id="heroChampagne" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="40%" stop-color="#F4E9DC"/>
      <stop offset="70%" stop-color="#EADBCE"/>
      <stop offset="100%" stop-color="#C7AF96"/>
    </linearGradient>

    <linearGradient id="heroFadeLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D8C5B2" stop-opacity="0"/>
      <stop offset="15%" stop-color="#D8C5B2" stop-opacity="0.75"/>
      <stop offset="50%" stop-color="#FFFDF9" stop-opacity="0.95"/>
      <stop offset="85%" stop-color="#D8C5B2" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#D8C5B2" stop-opacity="0"/>
    </linearGradient>

    <filter id="heroSoftGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="heroSpotlight" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Fade mask for Renaissance philosophers background -->
    <linearGradient id="damnnFade" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="25%" stop-color="#FFFFFF" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="1"/>
    </linearGradient>
    <mask id="damnnMask">
      <rect x="520" y="60" width="640" height="420" fill="url(#damnnFade)"/>
    </mask>
  </defs>

  <style>
{SHARED_FONTS_CSS}
  </style>

  <!-- Base Velvet Canvas -->
  <rect width="1200" height="520" fill="url(#heroVelvetBg)"/>

  <!-- Ambient Wine & Sage Glow Spotlights -->
  <circle cx="280" cy="260" r="280" fill="#6A1B31" opacity="0.22" filter="url(#heroSpotlight)"/>
  <circle cx="920" cy="260" r="280" fill="#4A5538" opacity="0.20" filter="url(#heroSpotlight)"/>
  <circle cx="640" cy="240" r="320" fill="#83223E" opacity="0.16" filter="url(#heroSpotlight)"/>

  <!-- The Classical Philosophers & MacBook Painting as Background Art -->
  <g mask="url(#damnnMask)" opacity="0.88">
    <animateTransform attributeName="transform" type="translate" values="0,0; 0,-6; 0,0" dur="6s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
    <!-- Soft screen glow around the laptop -->
    <circle cx="910" cy="380" r="140" fill="#EADBCE" opacity="0.18" filter="url(#heroSpotlight)"/>
    <image href="data:image/png;base64,{b64_damnn}" x="520" y="100" width="640" height="360" preserveAspectRatio="xMidYMid meet"/>
  </g>

  <!-- Symmetrical Dual Hairline Frame (Margins at 24px/30px) -->
  <rect x="24" y="24" width="1152" height="472" rx="20" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.45"/>
  <rect x="30" y="30" width="1140" height="460" rx="16" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.35"/>

  <!-- Baroque Corner Flourishes -->
  <g stroke="#EADBCE" stroke-width="1.1" fill="none" opacity="0.85">
    <path d="M 40 72 C 40 50, 50 40, 72 40"/>
    <path d="M 46 82 C 46 56, 56 46, 82 46"/>
    <circle cx="44" cy="44" r="2.2" fill="#D8C5B2"/>
    <circle cx="72" cy="40" r="1.5" fill="#8E9F70"/>
    <path d="M 1160 72 C 1160 50, 1150 40, 1128 40"/>
    <path d="M 1154 82 C 1154 56, 1144 46, 1118 46"/>
    <circle cx="1156" cy="44" r="2.2" fill="#D8C5B2"/>
    <circle cx="1128" cy="40" r="1.5" fill="#8E9F70"/>
    <path d="M 40 448 C 40 470, 50 480, 72 480"/>
    <path d="M 46 438 C 46 464, 56 474, 82 474"/>
    <circle cx="44" cy="476" r="2.2" fill="#D8C5B2"/>
    <circle cx="72" cy="480" r="1.5" fill="#8E9F70"/>
    <path d="M 1160 448 C 1160 470, 1150 480, 1128 480"/>
    <path d="M 1154 438 C 1154 464, 1144 474, 1118 474"/>
    <circle cx="1156" cy="476" r="2.2" fill="#D8C5B2"/>
    <circle cx="1128" cy="480" r="1.5" fill="#8E9F70"/>
  </g>

  <!-- Top Header Row in Host Grotesk -->
  <text x="64" y="62" class="host-grotesk" font-size="11.5" font-weight="600" fill="#D8C5B2" letter-spacing="3.5">THE PRIVATE ATELIER OF</text>
  <text x="1136" y="62" text-anchor="end" class="host-grotesk" font-size="11.5" font-weight="600" fill="#8E9F70" letter-spacing="3.5">— HAUTE INGÉNIERIE · EDITION MMXXIV —</text>
  <line x1="64" y1="76" x2="1136" y2="76" stroke="url(#heroFadeLine)" stroke-width="0.7"/>

  <!-- LEFT EDITORIAL COLUMN (Cleanly bounded inside X=64 to X=540) -->
  <g transform="translate(64, 116)">
    <!-- Monogram Emblem & Sub-label -->
    <g transform="translate(0, 12)">
      <circle cx="16" cy="16" r="16" fill="#1c0712" stroke="#74825C" stroke-width="0.9"/>
      <circle cx="16" cy="16" r="13" fill="none" stroke="#D8C5B2" stroke-width="0.5" stroke-dasharray="2 3">
        <animateTransform attributeName="transform" type="rotate" from="0 16 16" to="360 16 16" dur="30s" repeatCount="indefinite"/>
      </circle>
      <text x="16" y="23" text-anchor="middle" class="instrument-serif-regular-italic" font-size="20" fill="url(#heroChampagne)">S</text>
      <text x="44" y="21" class="host-grotesk" font-size="11.5" font-weight="600" fill="#8E9F70" letter-spacing="2.5">MAISON SASWAT · ARTISAN &amp; BUILDER</text>
    </g>

    <!-- Main Name: Instrument Serif Italic Luxury Typography -->
    <g transform="translate(0, 92)">
      <text x="0" y="0" class="instrument-serif-regular-italic" font-size="80" fill="url(#heroChampagne)" filter="url(#heroSoftGlow)" letter-spacing="2">
        Saswat Mohanty
      </text>
      <!-- Calligraphic Gold Under-Swash -->
      <path d="M 0 16 C 120 30, 280 -4, 440 18" fill="none" stroke="url(#heroFadeLine)" stroke-width="1.2"/>
      <circle cx="440" cy="18" r="2.5" fill="#8E9F70"/>
    </g>

    <!-- Literary Philosophy Quote in Instrument Serif Italic -->
    <text x="0" y="152" class="instrument-serif-regular-italic" font-size="20" fill="#EADBCE" letter-spacing="1">
      "Systems that ship. Interfaces that breathe. Craft that endures."
    </text>
    <text x="0" y="180" class="host-grotesk" font-size="12" font-weight="400" fill="#8E9F70" letter-spacing="1.5">
      Where classical philosophy meets modern runtime intelligence.
    </text>

    <!-- Precision Capability Pills in Host Grotesk -->
    <g transform="translate(0, 226)" class="host-grotesk" font-size="10" font-weight="600" letter-spacing="1">
      <g transform="translate(80, 0)">
        <rect x="-80" y="-13" width="160" height="26" rx="13" fill="#181e13" stroke="#74825C" stroke-width="0.8"/>
        <circle cx="-64" cy="0" r="2.8" fill="#8E9F70"/>
        <text x="-50" y="3.5" fill="#F6F0E6">SYSTEMS BUILDER</text>
      </g>
      <g transform="translate(250, 0)">
        <rect x="-80" y="-13" width="160" height="26" rx="13" fill="#240a15" stroke="#9E2D4C" stroke-width="0.8"/>
        <circle cx="-64" cy="0" r="2.8" fill="#9E2D4C"/>
        <text x="-50" y="3.5" fill="#F6F0E6">INTELLIGENT AGENTS</text>
      </g>
      <g transform="translate(420, 0)">
        <rect x="-80" y="-13" width="160" height="26" rx="13" fill="#181e13" stroke="#74825C" stroke-width="0.8"/>
        <circle cx="-64" cy="0" r="2.8" fill="#8E9F70"/>
        <text x="-50" y="3.5" fill="#F6F0E6">INTERFACE MOTION</text>
      </g>
    </g>
  </g>

  <!-- Bottom Rail in Host Grotesk -->
  <line x1="64" y1="464" x2="1136" y2="464" stroke="url(#heroFadeLine)" stroke-width="0.5" opacity="0.6"/>
  <g transform="translate(64, 486)">
    <circle cx="0" cy="0" r="4" fill="#8E9F70" filter="url(#heroSoftGlow)">
      <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="14" y="4" class="host-grotesk" font-size="11" font-weight="600" fill="#8E9F70" letter-spacing="2">OPEN FOR VISIONARY INQUIRIES &amp; HIGH-CRAFT SYSTEMS</text>
  </g>
  <text x="1100" y="490" text-anchor="end" class="host-grotesk" font-size="11" font-weight="600" fill="#D8C5B2" letter-spacing="2.5">BHUBANESWAR / NEW DELHI · IST · UTC+05:30</text>
</svg>'''
    with open("assets/hero-banner.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("hero-banner.svg generated successfully.")

def build_dr_debug_card():
    b64_debug = get_b64("assets/dr-debug-mascot-opt.png")
    cell_w, cell_h = 310, 74

    c1 = make_cell(0, 0, cell_w, cell_h, "#8E9F70", "DockerBridge Logs", "Correlates client errors with", "live container logs & panics", stroke_col="#74825C", fill_col="#1b0813")
    c2 = make_cell(330, 0, cell_w, cell_h, "#9E2D4C", "Flight Recorder", "Buffers 30s of user interaction", "clicks, inputs & route changes", stroke_col="#9E2D4C", fill_col="#1e0915")
    c3 = make_cell(0, 86, cell_w, cell_h, "#9E2D4C", "Structured Context", "Compiles RFC-9457 XML state", "under 1,500 prompt tokens", stroke_col="#9E2D4C", fill_col="#1e0915")
    c4 = make_cell(330, 86, cell_w, cell_h, "#8E9F70", "Shadow DOM HUD", "Zero-pollution #dr-debug-root", "with Chrome DevTools panel", stroke_col="#74825C", fill_col="#1b0813")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 460" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Dr.Debug — Autonomous In-Browser AI Debugging &amp; Runtime Observability Agent">
  <defs>
    <linearGradient id="dbgBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#120308"/>
      <stop offset="50%" stop-color="#1f0714"/>
      <stop offset="100%" stop-color="#0e0206"/>
    </linearGradient>

    <radialGradient id="dbgChamber" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#2a0d1c" stop-opacity="0.9"/>
      <stop offset="55%" stop-color="#190610" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#0d0206" stop-opacity="0.95"/>
    </radialGradient>

    <linearGradient id="dbgGold" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="45%" stop-color="#EADBCE"/>
      <stop offset="100%" stop-color="#C7AF96"/>
    </linearGradient>

    <linearGradient id="dbgFadeLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D8C5B2" stop-opacity="0"/>
      <stop offset="25%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#FFFDF9" stop-opacity="1"/>
      <stop offset="75%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#D8C5B2" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="dbgScan" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8E9F70" stop-opacity="0"/>
      <stop offset="50%" stop-color="#44FF44" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#8E9F70" stop-opacity="0"/>
    </linearGradient>

    <filter id="dbgGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <pattern id="dbgLattice" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M 18 0 Q 27 9 36 18 Q 27 27 18 36 Q 9 27 0 18 Q 9 9 18 0 Z" fill="none" stroke="#D8C5B2" stroke-width="0.3" opacity="0.05"/>
    </pattern>
  </defs>

  <style>
{SHARED_FONTS_CSS}
  </style>

  <rect width="1080" height="460" rx="28" fill="url(#dbgBg)"/>
  <rect width="1080" height="460" rx="28" fill="url(#dbgLattice)"/>

  <!-- Ornate Dual Hairlines -->
  <rect x="16" y="16" width="1048" height="428" rx="22" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.4"/>
  <rect x="22" y="22" width="1036" height="416" rx="18" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.3"/>

  <!-- Baroque Corners -->
  <g stroke="#EADBCE" stroke-width="1.1" fill="none" opacity="0.85">
    <path d="M 28 54 C 28 36, 36 28, 54 28"/>
    <circle cx="32" cy="32" r="1.8" fill="#D8C5B2"/>
    <path d="M 1052 54 C 1052 36, 1044 28, 1026 28"/>
    <circle cx="1048" cy="32" r="1.8" fill="#D8C5B2"/>
    <path d="M 28 406 C 28 424, 36 432, 54 432"/>
    <circle cx="32" cy="428" r="1.8" fill="#D8C5B2"/>
    <path d="M 1052 406 C 1052 424, 1044 432, 1026 432"/>
    <circle cx="1048" cy="428" r="1.8" fill="#D8C5B2"/>
  </g>

  <!-- LEFT: DR. DEBUG LAB ALCOVE (Width=310, Height=364) -->
  <g transform="translate(48, 48)">
    <rect width="310" height="364" rx="20" fill="url(#dbgChamber)" stroke="#74825C" stroke-width="0.8"/>
    <rect x="6" y="6" width="298" height="352" rx="16" fill="none" stroke="#D8C5B2" stroke-width="0.4" opacity="0.4"/>

    <circle cx="155" cy="170" r="128" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.35"/>
    <circle cx="155" cy="170" r="136" fill="none" stroke="#D8C5B2" stroke-width="0.4" stroke-dasharray="3 4" opacity="0.3">
      <animateTransform attributeName="transform" type="rotate" from="0 155 170" to="360 155 170" dur="30s" repeatCount="indefinite"/>
    </circle>

    <!-- Rising Bubbles -->
    <g fill="#44FF44" opacity="0.5" filter="url(#dbgGlow)">
      <circle cx="115" cy="280" r="3"><animate attributeName="cy" values="280;100" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.7;0" dur="4s" repeatCount="indefinite"/></circle>
      <circle cx="195" cy="290" r="2"><animate attributeName="cy" values="290;90" dur="5s" repeatCount="indefinite" begin="-2s"/><animate attributeName="opacity" values="0;0.6;0" dur="5s" repeatCount="indefinite" begin="-2s"/></circle>
      <circle cx="145" cy="270" r="2.5"><animate attributeName="cy" values="270;110" dur="3.5s" repeatCount="indefinite" begin="-1.2s"/><animate attributeName="opacity" values="0;0.8;0" dur="3.5s" repeatCount="indefinite" begin="-1.2s"/></circle>
    </g>

    <!-- Animated Mascot -->
    <g>
      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
      <image href="data:image/png;base64,{b64_debug}" x="35" y="32" width="240" height="262" preserveAspectRatio="xMidYMid meet"/>
      <line x1="55" y1="50" x2="255" y2="50" stroke="url(#dbgScan)" stroke-width="1.6" filter="url(#dbgGlow)" opacity="0.65">
        <animate attributeName="y1" values="50;270;50" dur="4.8s" repeatCount="indefinite"/>
        <animate attributeName="y2" values="50;270;50" dur="4.8s" repeatCount="indefinite"/>
      </line>
    </g>

    <g transform="translate(155, 332)">
      <rect x="-85" y="-12" width="170" height="24" rx="12" fill="#151b11" stroke="#74825C" stroke-width="0.8"/>
      <circle cx="-64" cy="0" r="3.5" fill="#44FF44" filter="url(#dbgGlow)">
        <animate attributeName="opacity" values="1;0.35;1" dur="1.8s" repeatCount="indefinite"/>
      </circle>
      <text x="8" y="4" text-anchor="middle" class="host-grotesk" font-size="11" font-weight="600" fill="#EADBCE" letter-spacing="1.2">DIAGNOSTIC ACTIVE</text>
    </g>
  </g>

  <!-- RIGHT: EDITORIAL SPECIFICATION (X=390, Width=640) -->
  <g transform="translate(390, 56)">
    <text x="0" y="16" class="host-grotesk" font-size="12" font-weight="600" fill="#8E9F70" letter-spacing="3.5">AUTONOMOUS OBSERVABILITY · MISSION 01</text>
    <text x="0" y="62" class="instrument-serif-regular" font-size="44" fill="url(#dbgGold)" filter="url(#dbgGlow)" letter-spacing="3">DR. DEBUG</text>
    <text x="0" y="94" class="instrument-serif-regular-italic" font-size="16.5" fill="#EADBCE" letter-spacing="1">
      "Autonomous in-browser AI debugging &amp; runtime observability agent."
    </text>

    <line x1="0" y1="116" x2="640" y2="116" stroke="url(#dbgFadeLine)" stroke-width="0.8"/>
    <circle cx="320" cy="116" r="2.5" fill="#D8C5B2"/>

    <!-- 2x2 LUXURY CAPABILITY SPECIFICATION MATRIX (Zero Overflow Guaranteed) -->
    <g transform="translate(0, 134)">
      {c1}
      {c2}
      {c3}
      {c4}
    </g>

    <!-- Bottom Footer Row -->
    <g transform="translate(0, 328)">
      <line x1="0" y1="0" x2="640" y2="0" stroke="url(#dbgFadeLine)" stroke-width="0.6"/>
      <g transform="translate(0, 18)" class="host-grotesk" font-size="11.5">
        <text x="0" y="4" fill="#8E9F70" font-weight="500">STACK: TypeScript · Vite · LiteRT / WebLLM · Docker · Re-Act</text>
        <text x="640" y="4" text-anchor="end" fill="#EADBCE" font-weight="600">github.com/SazWhatician/Dr.Debug ↗</text>
      </g>
    </g>
  </g>
</svg>'''
    with open("assets/dr-debug-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("dr-debug-card.svg generated successfully.")

def build_polaris_card():
    b64_polaris = get_b64("assets/polaris-standalone-opt2.png")
    cell_w, cell_h = 310, 74

    c1 = make_cell(0, 0, cell_w, cell_h, "#8E9F70", "Grounded RAG Search", "Page-level bounding citations", "with instant token streaming", stroke_col="#74825C", fill_col="#1b0813")
    c2 = make_cell(330, 0, cell_w, cell_h, "#9E2D4C", "PaddleOCR Pipeline", "Background document ingestion", "indexed in Qdrant vector DB", stroke_col="#9E2D4C", fill_col="#1e0915")
    c3 = make_cell(0, 86, cell_w, cell_h, "#9E2D4C", "Concept Topology", "Interactive WebGL2 knowledge", "graph of prerequisite topics", stroke_col="#9E2D4C", fill_col="#1e0915")
    c4 = make_cell(330, 86, cell_w, cell_h, "#8E9F70", "Adaptive Revision", "LangGraph study planner &", "multimodal gap analysis", stroke_col="#74825C", fill_col="#1b0813")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 460" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Polaris — Haute Intelligence &amp; Academic AI Navigator">
  <defs>
    <linearGradient id="polBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#120308"/>
      <stop offset="50%" stop-color="#1e0714"/>
      <stop offset="100%" stop-color="#0e0206"/>
    </linearGradient>

    <radialGradient id="polChamber" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#220a2e" stop-opacity="0.9"/>
      <stop offset="55%" stop-color="#15061c" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#0d0208" stop-opacity="0.95"/>
    </radialGradient>

    <linearGradient id="polChampagne" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="45%" stop-color="#EADBCE"/>
      <stop offset="100%" stop-color="#C7AF96"/>
    </linearGradient>

    <linearGradient id="polFadeLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D8C5B2" stop-opacity="0"/>
      <stop offset="25%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#FFFDF9" stop-opacity="1"/>
      <stop offset="75%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#D8C5B2" stop-opacity="0"/>
    </linearGradient>

    <filter id="polCosmicGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <filter id="polSoftGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <pattern id="polLattice" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M 18 0 Q 27 9 36 18 Q 27 27 18 36 Q 9 27 0 18 Q 9 9 18 0 Z" fill="none" stroke="#D8C5B2" stroke-width="0.3" opacity="0.05"/>
    </pattern>
  </defs>

  <style>
{SHARED_FONTS_CSS}
  </style>

  <rect width="1080" height="460" rx="28" fill="url(#polBg)"/>
  <rect width="1080" height="460" rx="28" fill="url(#polLattice)"/>

  <rect x="16" y="16" width="1048" height="428" rx="22" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.4"/>
  <rect x="22" y="22" width="1036" height="416" rx="18" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.3"/>

  <g stroke="#EADBCE" stroke-width="1.1" fill="none" opacity="0.85">
    <path d="M 28 54 C 28 36, 36 28, 54 28"/><circle cx="32" cy="32" r="1.8" fill="#D8C5B2"/>
    <path d="M 1052 54 C 1052 36, 1044 28, 1026 28"/><circle cx="1048" cy="32" r="1.8" fill="#D8C5B2"/>
    <path d="M 28 406 C 28 424, 36 432, 54 432"/><circle cx="32" cy="428" r="1.8" fill="#D8C5B2"/>
    <path d="M 1052 406 C 1052 424, 1044 432, 1026 432"/><circle cx="1048" cy="428" r="1.8" fill="#D8C5B2"/>
  </g>

  <!-- LEFT: 3D POLARIS ORB CHAMBER -->
  <g transform="translate(48, 48)">
    <rect width="310" height="364" rx="20" fill="url(#polChamber)" stroke="#74825C" stroke-width="0.8"/>
    <rect x="6" y="6" width="298" height="352" rx="16" fill="none" stroke="#D8C5B2" stroke-width="0.4" opacity="0.4"/>

    <circle cx="155" cy="170" r="128" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.35"/>
    <circle cx="155" cy="170" r="136" fill="none" stroke="#D8C5B2" stroke-width="0.4" stroke-dasharray="3 4" opacity="0.3">
      <animateTransform attributeName="transform" type="rotate" from="0 155 170" to="360 155 170" dur="35s" repeatCount="indefinite"/>
    </circle>
    <circle cx="155" cy="170" r="100" fill="#3B82F6" opacity="0.18" filter="url(#polCosmicGlow)">
      <animate attributeName="opacity" values="0.12;0.25;0.12" dur="4s" repeatCount="indefinite"/>
    </circle>

    <g>
      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0" dur="4.2s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
      <image href="data:image/png;base64,{b64_polaris}" x="45" y="45" width="220" height="240" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <g transform="translate(155, 332)">
      <rect x="-85" y="-12" width="170" height="24" rx="12" fill="#170c26" stroke="#8E9F70" stroke-width="0.8"/>
      <circle cx="-64" cy="0" r="3.5" fill="#38BDF8" filter="url(#polSoftGlow)">
        <animate attributeName="opacity" values="1;0.35;1" dur="1.8s" repeatCount="indefinite"/>
      </circle>
      <text x="8" y="4" text-anchor="middle" class="host-grotesk" font-size="11" font-weight="600" fill="#EADBCE" letter-spacing="1.2">RESEARCH ENGINE</text>
    </g>
  </g>

  <!-- RIGHT: EDITORIAL SPECIFICATION (X=390, Width=640) -->
  <g transform="translate(390, 56)">
    <text x="0" y="16" class="host-grotesk" font-size="12" font-weight="600" fill="#8E9F70" letter-spacing="3.5">COGNITIVE ACADEMIC NAVIGATOR · MISSION 02</text>
    <text x="0" y="62" class="instrument-serif-regular" font-size="44" fill="url(#polChampagne)" filter="url(#polSoftGlow)" letter-spacing="3">POLARIS</text>
    <text x="0" y="94" class="instrument-serif-regular-italic" font-size="16.5" fill="#EADBCE" letter-spacing="1">
      "Haute Intelligence · Turn course notes &amp; syllabus into verified knowledge."
    </text>

    <line x1="0" y1="116" x2="640" y2="116" stroke="url(#polFadeLine)" stroke-width="0.8"/>
    <circle cx="320" cy="116" r="2.5" fill="#D8C5B2"/>

    <g transform="translate(0, 134)">
      {c1}
      {c2}
      {c3}
      {c4}
    </g>

    <g transform="translate(0, 328)">
      <line x1="0" y1="0" x2="640" y2="0" stroke="url(#polFadeLine)" stroke-width="0.6"/>
      <g transform="translate(0, 18)" class="host-grotesk" font-size="11.5">
        <text x="0" y="4" fill="#8E9F70" font-weight="500">STACK: Next.js 15 · FastAPI · Qdrant · PaddleOCR · WebGL2</text>
        <text x="640" y="4" text-anchor="end" fill="#EADBCE" font-weight="600">github.com/SazWhatician/Polaris ↗</text>
      </g>
    </g>
  </g>
</svg>'''
    with open("assets/polaris-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("polaris-card.svg generated successfully.")

def build_medscan_card():
    b64_medscan = get_b64("assets/MedScanAI-opt2.png")
    cell_w, cell_h = 310, 74

    c1 = make_cell(0, 0, cell_w, cell_h, "#8E9F70", "Ensemble Classifier", "High-recall skin lesion and", "melanoma detection ensemble", stroke_col="#74825C", fill_col="#1b0813")
    c2 = make_cell(330, 0, cell_w, cell_h, "#9E2D4C", "Deep CNN Radiography", "Pneumonia pathology screening", "from chest X-ray scans", stroke_col="#9E2D4C", fill_col="#1e0915")
    c3 = make_cell(0, 86, cell_w, cell_h, "#9E2D4C", "ANN Metabolic Model", "Predictive neural networks for", "early diabetes risk profiling", stroke_col="#9E2D4C", fill_col="#1e0915")
    c4 = make_cell(330, 86, cell_w, cell_h, "#8E9F70", "Grad-CAM Heatmaps", "Explainable visual attribution", "for clinician second opinions", stroke_col="#74825C", fill_col="#1b0813")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 460" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="MedScan AI — Clinical Tri-Model Vision &amp; Diagnostic Neural Intelligence">
  <defs>
    <linearGradient id="medBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#120308"/>
      <stop offset="50%" stop-color="#1f0714"/>
      <stop offset="100%" stop-color="#0e0206"/>
    </linearGradient>

    <radialGradient id="medChamber" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#0a1e24" stop-opacity="0.9"/>
      <stop offset="55%" stop-color="#071419" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#0d0208" stop-opacity="0.95"/>
    </radialGradient>

    <linearGradient id="medChampagne" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="45%" stop-color="#EADBCE"/>
      <stop offset="100%" stop-color="#C7AF96"/>
    </linearGradient>

    <linearGradient id="medFadeLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D8C5B2" stop-opacity="0"/>
      <stop offset="25%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#FFFDF9" stop-opacity="1"/>
      <stop offset="75%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#D8C5B2" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="ecgGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#06B6D4" stop-opacity="0"/>
      <stop offset="50%" stop-color="#22D3EE" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#06B6D4" stop-opacity="0"/>
    </linearGradient>

    <filter id="medCyanGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <filter id="medSoftGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <pattern id="medLattice" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M 18 0 Q 27 9 36 18 Q 27 27 18 36 Q 9 27 0 18 Q 9 9 18 0 Z" fill="none" stroke="#D8C5B2" stroke-width="0.3" opacity="0.05"/>
    </pattern>
  </defs>

  <style>
{SHARED_FONTS_CSS}
  </style>

  <rect width="1080" height="460" rx="28" fill="url(#medBg)"/>
  <rect width="1080" height="460" rx="28" fill="url(#medLattice)"/>

  <rect x="16" y="16" width="1048" height="428" rx="22" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.4"/>
  <rect x="22" y="22" width="1036" height="416" rx="18" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.3"/>

  <g stroke="#EADBCE" stroke-width="1.1" fill="none" opacity="0.85">
    <path d="M 28 54 C 28 36, 36 28, 54 28"/><circle cx="32" cy="32" r="1.8" fill="#D8C5B2"/>
    <path d="M 1052 54 C 1052 36, 1044 28, 1026 28"/><circle cx="1048" cy="32" r="1.8" fill="#D8C5B2"/>
    <path d="M 28 406 C 28 424, 36 432, 54 432"/><circle cx="32" cy="428" r="1.8" fill="#D8C5B2"/>
    <path d="M 1052 406 C 1052 424, 1044 432, 1026 432"/><circle cx="1048" cy="428" r="1.8" fill="#D8C5B2"/>
  </g>

  <!-- LEFT: CLINICAL VISION CHAMBER -->
  <g transform="translate(48, 48)">
    <rect width="310" height="364" rx="20" fill="url(#medChamber)" stroke="#74825C" stroke-width="0.8"/>
    <rect x="6" y="6" width="298" height="352" rx="16" fill="none" stroke="#D8C5B2" stroke-width="0.4" opacity="0.4"/>

    <circle cx="155" cy="170" r="128" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.35"/>
    <circle cx="155" cy="170" r="136" fill="none" stroke="#D8C5B2" stroke-width="0.4" stroke-dasharray="3 4" opacity="0.3">
      <animateTransform attributeName="transform" type="rotate" from="0 155 170" to="360 155 170" dur="32s" repeatCount="indefinite"/>
    </circle>
    <circle cx="155" cy="170" r="90" fill="#06B6D4" opacity="0.16" filter="url(#medCyanGlow)">
      <animate attributeName="opacity" values="0.10;0.24;0.10" dur="2.4s" repeatCount="indefinite"/>
    </circle>

    <g>
      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
      <image href="data:image/png;base64,{b64_medscan}" x="45" y="45" width="220" height="240" preserveAspectRatio="xMidYMid meet"/>
      <line x1="45" y1="165" x2="265" y2="165" stroke="url(#ecgGrad)" stroke-width="1.8" filter="url(#medSoftGlow)" opacity="0.75">
        <animate attributeName="y1" values="80;250;80" dur="4.2s" repeatCount="indefinite"/>
        <animate attributeName="y2" values="80;250;80" dur="4.2s" repeatCount="indefinite"/>
      </line>
    </g>

    <g transform="translate(155, 332)">
      <rect x="-85" y="-12" width="170" height="24" rx="12" fill="#071d22" stroke="#74825C" stroke-width="0.8"/>
      <circle cx="-64" cy="0" r="3.5" fill="#22D3EE" filter="url(#medSoftGlow)">
        <animate attributeName="opacity" values="1;0.35;1" dur="1.4s" repeatCount="indefinite"/>
      </circle>
      <text x="8" y="4" text-anchor="middle" class="host-grotesk" font-size="11" font-weight="600" fill="#EADBCE" letter-spacing="1.2">CLINICAL SCANNER</text>
    </g>
  </g>

  <!-- RIGHT: EDITORIAL SPECIFICATION (X=390, Width=640) -->
  <g transform="translate(390, 56)">
    <text x="0" y="16" class="host-grotesk" font-size="12" font-weight="600" fill="#8E9F70" letter-spacing="3.5">TRI-MODEL DIAGNOSTIC SUITE · MISSION 03</text>
    <text x="0" y="62" class="instrument-serif-regular" font-size="44" fill="url(#medChampagne)" filter="url(#medSoftGlow)" letter-spacing="3">MEDSCAN AI</text>
    <text x="0" y="94" class="instrument-serif-regular-italic" font-size="16.5" fill="#EADBCE" letter-spacing="1">
      "Clinical tri-model vision: skin cancer ensemble, CNN pneumonia, &amp; ANN diabetes."
    </text>

    <line x1="0" y1="116" x2="640" y2="116" stroke="url(#medFadeLine)" stroke-width="0.8"/>
    <circle cx="320" cy="116" r="2.5" fill="#D8C5B2"/>

    <g transform="translate(0, 134)">
      {c1}
      {c2}
      {c3}
      {c4}
    </g>

    <g transform="translate(0, 328)">
      <line x1="0" y1="0" x2="640" y2="0" stroke="url(#medFadeLine)" stroke-width="0.6"/>
      <g transform="translate(0, 18)" class="host-grotesk" font-size="11.5">
        <text x="0" y="4" fill="#8E9F70" font-weight="500">STACK: PyTorch · OpenCV · TorchVision · Grad-CAM · Deep Learning</text>
        <text x="640" y="4" text-anchor="end" fill="#EADBCE" font-weight="600">github.com/SazWhatician/MedScan-AI ↗</text>
      </g>
    </g>
  </g>
</svg>'''
    with open("assets/medscan-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("medscan-card.svg generated successfully.")

def build_ethos_card():
    b64_violin = get_b64("assets/violin-opt.png")
    b64_cloud1 = get_b64("assets/cloud1-opt.png")
    b64_cloud2 = get_b64("assets/cloud2-opt.png")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 380" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="The Engineering Manifesto &amp; Ethos — Saswat Mohanty">
  <defs>
    <linearGradient id="ethosBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#120308"/>
      <stop offset="50%" stop-color="#1f0714"/>
      <stop offset="100%" stop-color="#0e0206"/>
    </linearGradient>
    <linearGradient id="ethosGold" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="45%" stop-color="#EADBCE"/>
      <stop offset="100%" stop-color="#C7AF96"/>
    </linearGradient>
    <linearGradient id="ethosFadeLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D8C5B2" stop-opacity="0"/>
      <stop offset="25%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#FFFDF9" stop-opacity="1"/>
      <stop offset="75%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#D8C5B2" stop-opacity="0"/>
    </linearGradient>
    <filter id="ethosGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <style>
{SHARED_FONTS_CSS}
  </style>

  <rect width="1080" height="380" rx="26" fill="url(#ethosBg)"/>
  <rect x="16" y="16" width="1048" height="348" rx="20" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.4"/>
  <rect x="22" y="22" width="1036" height="336" rx="16" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.3"/>

  <!-- Left: Golden Clouds & Classical Painter with Violin Companion -->
  <g transform="translate(48, 30)">
    <g opacity="0.35">
      <animateTransform attributeName="transform" type="translate" values="0,0; -12,4; 0,0" dur="18s" repeatCount="indefinite"/>
      <image href="data:image/png;base64,{b64_cloud1}" x="-20" y="120" width="340" height="180" preserveAspectRatio="xMidYMid meet"/>
    </g>
    <g>
      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0" dur="5.5s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
      <image href="data:image/png;base64,{b64_violin}" x="25" y="10" width="260" height="315" preserveAspectRatio="xMidYMid meet"/>
    </g>
  </g>

  <!-- Right: The Engineering Manifesto & Laws (X=390, Width=640) -->
  <g transform="translate(390, 52)">
    <text x="0" y="16" class="host-grotesk" font-size="12" font-weight="600" fill="#8E9F70" letter-spacing="3.5">07 · THE MANIFESTO &amp; CODE ETHOS</text>
    <text x="0" y="58" class="instrument-serif-regular-italic" font-size="46" fill="url(#ethosGold)" filter="url(#ethosGlow)" letter-spacing="2">
      The Craft of Engineering
    </text>
    <line x1="0" y1="78" x2="640" y2="78" stroke="url(#ethosFadeLine)" stroke-width="0.8"/>

    <g transform="translate(0, 108)" class="instrument-serif-regular-italic" font-size="17" fill="#F6F0E6" letter-spacing="0.5">
      <g transform="translate(0, 0)">
        <circle cx="6" cy="-4" r="2.5" fill="#8E9F70"/>
        <text x="20" y="0">"Small teams. Careful code. Long patience."</text>
      </g>
      <g transform="translate(0, 32)">
        <circle cx="6" cy="-4" r="2.5" fill="#9E2D4C"/>
        <text x="20" y="0">"Latency is language. Every millisecond speaks."</text>
      </g>
      <g transform="translate(0, 64)">
        <circle cx="6" cy="-4" r="2.5" fill="#8E9F70"/>
        <text x="20" y="0">"Interfaces are trust — earn it in the micro-interactions."</text>
      </g>
      <g transform="translate(0, 96)">
        <circle cx="6" cy="-4" r="2.5" fill="#9E2D4C"/>
        <text x="20" y="0">"Measure twice · ship once · then watch the logs."</text>
      </g>
    </g>

    <line x1="0" y1="242" x2="640" y2="242" stroke="url(#ethosFadeLine)" stroke-width="0.6"/>
    <g transform="translate(0, 264)">
      <text x="0" y="0" class="instrument-serif-regular-italic" font-size="22" fill="#EADBCE">— Saswat Mohanty</text>
      <text x="640" y="0" text-anchor="end" class="host-grotesk" font-size="11.5" font-weight="600" fill="#8E9F70">AI Engineer · Systems &amp; Interfaces</text>
    </g>
  </g>
</svg>'''
    with open("assets/ethos-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("ethos-card.svg generated successfully.")

def build_telemetry_hud():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Saswat Mohanty — Live Telemetry and All-Time Contributions">
  <defs>
    <!-- Background Velvet Burgundy Gradient -->
    <linearGradient id="cntBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#120308"/>
      <stop offset="50%" stop-color="#1f0713"/>
      <stop offset="100%" stop-color="#0f0206"/>
    </linearGradient>

    <!-- Card Wine Gradient -->
    <linearGradient id="cntCard" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#230a17"/>
      <stop offset="100%" stop-color="#15040e"/>
    </linearGradient>

    <!-- Champagne Numeral Gradient -->
    <linearGradient id="cntNumeral" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="60%" stop-color="#EADBCE"/>
      <stop offset="100%" stop-color="#C7AF96"/>
    </linearGradient>

    <!-- Gold-Champagne Hairline Gradient -->
    <linearGradient id="cntGold" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D8C5B2" stop-opacity="0.1"/>
      <stop offset="50%" stop-color="#FFFDF9" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#D8C5B2" stop-opacity="0.1"/>
    </linearGradient>

    <!-- Olive Bar Gradient -->
    <linearGradient id="cntOlive" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#5B6648"/>
      <stop offset="50%" stop-color="#8E9F70"/>
      <stop offset="100%" stop-color="#5B6648"/>
    </linearGradient>

    <!-- Soft Glow Filter -->
    <filter id="cntGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Precise LOCAL Clip Paths (inside Card coordinate space) -->
    <!-- Left Card: All-Time Contributions (506) -->
    <clipPath id="clipCommitC1"><rect x="36" y="96" width="56" height="82"/></clipPath>
    <clipPath id="clipCommitC2"><rect x="94" y="96" width="56" height="82"/></clipPath>
    <clipPath id="clipCommitC3"><rect x="152" y="96" width="56" height="82"/></clipPath>

    <!-- Right Card: Public Repos (31) -->
    <clipPath id="clipRepoR1"><rect x="36" y="96" width="56" height="82"/></clipPath>
    <clipPath id="clipRepoR2"><rect x="94" y="96" width="56" height="82"/></clipPath>
  </defs>

  <style>
{SHARED_FONTS_CSS}

    .reel {{
      animation-timing-function: cubic-bezier(0.16, 1, 0.3, 1);
      animation-fill-mode: forwards;
      animation-iteration-count: 1;
    }}
    /* Digit line height = 80px */
    /* 506: C1 rolls to 5 (-400px), C2 rolls to 0 (-800px), C3 rolls to 6 (-480px) */
    .roll-c100 {{ animation-name: kfC100; animation-duration: 2.2s; animation-delay: 0.1s; }}
    .roll-c010 {{ animation-name: kfC010; animation-duration: 2.5s; animation-delay: 0.2s; }}
    .roll-c001 {{ animation-name: kfC001; animation-duration: 2.8s; animation-delay: 0.15s; }}

    .roll-r10  {{ animation-name: kfR10;  animation-duration: 2.0s; animation-delay: 0.25s; }}
    .roll-r01  {{ animation-name: kfR01;  animation-duration: 2.4s; animation-delay: 0.3s; }}

    @keyframes kfC100 {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-400px); }} }}
    @keyframes kfC010 {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-800px); }} }}
    @keyframes kfC001 {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-480px); }} }}

    @keyframes kfR10  {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-240px); }} }}
    @keyframes kfR01  {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-80px); }} }}

    .bar-grow {{
      transform-origin: left center;
      animation: kfBar 2.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      transform: scaleX(0);
    }}
    @keyframes kfBar {{ to {{ transform: scaleX(1); }} }}
  </style>

  <!-- Background -->
  <rect width="1000" height="360" rx="28" fill="url(#cntBg)"/>

  <!-- Ornate Dual Border: Margins at 16px -->
  <rect x="16" y="16" width="968" height="328" rx="22" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.38"/>
  <rect x="22" y="22" width="956" height="316" rx="18" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.3"/>

  <!-- Header Row in Host Grotesk: Margins at 48px -->
  <text x="48" y="50" class="host-grotesk" font-size="12" font-weight="600" fill="#D8C5B2" letter-spacing="3">TELEMETRY INDEX · LIVE GIT CHRONICLE</text>
  <text x="952" y="50" text-anchor="end" class="host-grotesk" font-size="12" font-weight="600" fill="#8E9F70" letter-spacing="2.5">VERIFIED ALL-TIME RECORDS · @SazWhatician</text>
  <line x1="48" y1="62" x2="952" y2="62" stroke="url(#cntGold)" stroke-width="0.6"/>

  <!-- LEFT CARD: ALL-TIME CONTRIBUTIONS (506+) · Position at X=48, Y=78, Width=438, Height=238 -->
  <g transform="translate(48, 78)">
    <rect width="438" height="238" rx="20" fill="url(#cntCard)" stroke="#74825C" stroke-width="0.8" opacity="0.95"/>
    <rect x="6" y="6" width="426" height="226" rx="16" fill="none" stroke="#D8C5B2" stroke-width="0.4" opacity="0.35"/>

    <!-- Corner Baroque Insets -->
    <path d="M 14 30 C 14 18, 18 14, 30 14" fill="none" stroke="#EADBCE" stroke-width="1"/>
    <path d="M 424 30 C 424 18, 420 14, 408 14" fill="none" stroke="#EADBCE" stroke-width="1"/>
    <path d="M 14 208 C 14 220, 18 224, 30 224" fill="none" stroke="#EADBCE" stroke-width="1"/>
    <path d="M 424 208 C 424 220, 420 224, 408 224" fill="none" stroke="#EADBCE" stroke-width="1"/>

    <!-- Header inside card -->
    <g transform="translate(28, 28)">
      <circle cx="16" cy="16" r="16" fill="#1b0610" stroke="#9E2D4C" stroke-width="0.8"/>
      <path d="M 6 16 H 11 M 21 16 H 26" stroke="#EADBCE" stroke-width="2" stroke-linecap="round"/>
      <circle cx="16" cy="16" r="5" stroke="#EADBCE" stroke-width="2" fill="none"/>
      <text x="44" y="21" class="instrument-serif-regular-italic" font-size="16" fill="#EADBCE" letter-spacing="2">ALL-TIME CONTRIBUTIONS</text>
    </g>

    <!-- DIGIT 1 (Hundreds -> 5) centered in clip box x=36..92, center=64 -->
    <g clip-path="url(#clipCommitC1)">
      <g class="reel roll-c100 instrument-serif-regular" font-size="78" font-weight="700" fill="url(#cntNumeral)" text-anchor="middle">
        <text x="64" y="166">0</text>
        <text x="64" y="246">1</text>
        <text x="64" y="326">2</text>
        <text x="64" y="406">3</text>
        <text x="64" y="486">4</text>
        <text x="64" y="566">5</text>
      </g>
    </g>

    <!-- DIGIT 2 (Tens -> 0) centered in clip box x=94..150, center=122 -->
    <g clip-path="url(#clipCommitC2)">
      <g class="reel roll-c010 instrument-serif-regular" font-size="78" font-weight="700" fill="url(#cntNumeral)" text-anchor="middle">
        <text x="122" y="166">9</text>
        <text x="122" y="246">8</text>
        <text x="122" y="326">7</text>
        <text x="122" y="406">6</text>
        <text x="122" y="486">5</text>
        <text x="122" y="566">4</text>
        <text x="122" y="646">3</text>
        <text x="122" y="726">2</text>
        <text x="122" y="806">1</text>
        <text x="122" y="886">0</text>
        <text x="122" y="966">0</text>
      </g>
    </g>

    <!-- DIGIT 3 (Ones -> 6) centered in clip box x=152..208, center=180 -->
    <g clip-path="url(#clipCommitC3)">
      <g class="reel roll-c001 instrument-serif-regular" font-size="78" font-weight="700" fill="url(#cntNumeral)" text-anchor="middle">
        <text x="180" y="166">0</text>
        <text x="180" y="246">1</text>
        <text x="180" y="326">2</text>
        <text x="180" y="406">3</text>
        <text x="180" y="486">4</text>
        <text x="180" y="566">5</text>
        <text x="180" y="646">6</text>
      </g>
    </g>

    <!-- Plus Sign Badge: perfectly positioned next to digits -->
    <text x="216" y="148" class="instrument-serif-regular-italic" font-weight="700" font-size="44" fill="#8E9F70">+</text>

    <!-- Metric Pill on the right -->
    <g transform="translate(280, 126)">
      <rect x="0" y="-12" width="130" height="24" rx="12" fill="#181e13" stroke="#74825C" stroke-width="0.7"/>
      <circle cx="14" cy="0" r="3" fill="#8E9F70">
        <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
      </circle>
      <text x="72" y="4" text-anchor="middle" class="host-grotesk" font-size="10.5" font-weight="600" fill="#EADBCE">ALL-TIME CRAFT</text>
    </g>

    <!-- Hairline progress bar & footer (symmetrically padded at 28px) -->
    <rect x="28" y="194" width="382" height="2" rx="1" fill="#260b19"/>
    <rect class="bar-grow" x="28" y="194" width="382" height="2" rx="1" fill="url(#cntGold)"/>
    <text x="28" y="216" class="host-grotesk" font-size="11.5" fill="#8E9F70">Cumulative commits, pull requests &amp; code reviews</text>
    <text x="410" y="216" text-anchor="end" class="host-grotesk" font-size="11.5" font-weight="600" fill="#D8C5B2">506+ Logged</text>
  </g>

  <!-- RIGHT CARD: REPOSITORIES (31) · Position at X=514, Y=78, Width=438, Height=238 -->
  <g transform="translate(514, 78)">
    <rect width="438" height="238" rx="20" fill="url(#cntCard)" stroke="#74825C" stroke-width="0.8" opacity="0.95"/>
    <rect x="6" y="6" width="426" height="226" rx="16" fill="none" stroke="#D8C5B2" stroke-width="0.4" opacity="0.35"/>

    <!-- Corner Baroque Insets -->
    <path d="M 14 30 C 14 18, 18 14, 30 14" fill="none" stroke="#EADBCE" stroke-width="1"/>
    <path d="M 424 30 C 424 18, 420 14, 408 14" fill="none" stroke="#EADBCE" stroke-width="1"/>
    <path d="M 14 208 C 14 220, 18 224, 30 224" fill="none" stroke="#EADBCE" stroke-width="1"/>
    <path d="M 424 208 C 424 220, 420 224, 408 224" fill="none" stroke="#EADBCE" stroke-width="1"/>

    <!-- Header inside card -->
    <g transform="translate(28, 28)">
      <circle cx="16" cy="16" r="16" fill="#1b0610" stroke="#74825C" stroke-width="0.8"/>
      <path d="M 11 9 H 20 A 3 3 0 0 1 23 12 V 22 A 3 3 0 0 0 20 19 H 11 A 2 2 0 0 0 9 21 V 11 A 2 2 0 0 1 11 9 Z" stroke="#EADBCE" stroke-width="1.8" fill="none"/>
      <text x="44" y="21" class="instrument-serif-regular-italic" font-size="16" fill="#EADBCE" letter-spacing="2">PUBLIC REPOSITORIES</text>
    </g>

    <!-- DIGIT 1 (Tens -> 3) centered in clip box x=36..92, center=64 -->
    <g clip-path="url(#clipRepoR1)">
      <g class="reel roll-r10 instrument-serif-regular" font-size="78" font-weight="700" fill="url(#cntNumeral)" text-anchor="middle">
        <text x="64" y="166">0</text>
        <text x="64" y="246">1</text>
        <text x="64" y="326">2</text>
        <text x="64" y="406">3</text>
      </g>
    </g>

    <!-- DIGIT 2 (Ones -> 1) centered in clip box x=94..150, center=122 -->
    <g clip-path="url(#clipRepoR2)">
      <g class="reel roll-r01 instrument-serif-regular" font-size="78" font-weight="700" fill="url(#cntNumeral)" text-anchor="middle">
        <text x="122" y="166">0</text>
        <text x="122" y="246">1</text>
      </g>
    </g>

    <!-- Status pill on the right -->
    <g transform="translate(260, 126)">
      <rect x="0" y="-12" width="150" height="24" rx="12" fill="#240a15" stroke="#9E2D4C" stroke-width="0.7"/>
      <circle cx="14" cy="0" r="3" fill="#9E2D4C">
        <animate attributeName="opacity" values="1;0.4;1" dur="2.4s" repeatCount="indefinite"/>
      </circle>
      <text x="82" y="4" text-anchor="middle" class="host-grotesk" font-size="10.5" font-weight="600" fill="#EADBCE">FLAGSHIP BUILDS</text>
    </g>

    <!-- Hairline progress bar & footer (symmetrically padded at 28px) -->
    <rect x="28" y="194" width="382" height="2" rx="1" fill="#260b19"/>
    <rect class="bar-grow" x="28" y="194" width="382" height="2" rx="1" fill="url(#cntOlive)" style="animation-delay: 0.2s;"/>
    <text x="28" y="216" class="host-grotesk" font-size="11.5" fill="#8E9F70">AI agents, vision models, &amp; motion canvases</text>
    <text x="410" y="216" text-anchor="end" class="host-grotesk" font-size="11.5" font-weight="600" fill="#D8C5B2">31 Active Builds</text>
  </g>
</svg>'''
    with open("assets/telemetry-hud.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("telemetry-hud.svg generated successfully with 506+ all-time contributions.")

if __name__ == "__main__":
    build_hero_banner()
    build_dr_debug_card()
    build_polaris_card()
    build_medscan_card()
    build_ethos_card()
    build_telemetry_hud()

    # Validate XML of all SVGs
    for name in ["hero-banner.svg", "telemetry-hud.svg", "dr-debug-card.svg", "polaris-card.svg", "medscan-card.svg", "ethos-card.svg"]:
        path = os.path.join("assets", name)
        ET.parse(path)
        print(f"Validated XML: {name}")
