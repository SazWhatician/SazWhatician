import base64
import os
import xml.etree.ElementTree as ET
from PIL import ImageFont

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
'''

# Font measurement setup using real TTF files
font_host_semibold12 = ImageFont.truetype("fonts/HostGrotesk-SemiBold.ttf", 12)
font_host_regular11 = ImageFont.truetype("fonts/HostGrotesk-Regular.ttf", 11)

def check_string(txt, max_w, font):
    bb = font.getbbox(txt)
    w = bb[2] - bb[0]
    assert w <= max_w, f"Text '{txt}' width {w}px exceeds allowed {max_w}px!"
    return w

def make_compact_cell(x, y, w, h, icon_col, title, desc1, desc2="", stroke_col="#74825C", fill_col="#1b0813"):
    max_w = w - 28 - 10
    check_string(title, max_w, font_host_semibold12)
    check_string(desc1, max_w, font_host_regular11)
    if desc2:
        check_string(desc2, max_w, font_host_regular11)
    
    t_xml = title.replace("&", "&amp;")
    d1_xml = desc1.replace("&", "&amp;")
    d2_xml = desc2.replace("&", "&amp;") if desc2 else ""

    desc2_markup = f'<text x="28" y="47" class="host-grotesk" font-size="9.5" fill="#8E9F70">{d2_xml}</text>' if desc2 else ''

    return f'''<g transform="translate({x}, {y})">
        <rect width="{w}" height="{h}" rx="12" fill="{fill_col}" stroke="{stroke_col}" stroke-width="0.7"/>
        <circle cx="16" cy="18" r="2.8" fill="{icon_col}"/>
        <text x="28" y="20" class="host-grotesk" font-weight="600" font-size="11" fill="#F6F0E6" letter-spacing="0.5">{t_xml}</text>
        <text x="28" y="34" class="host-grotesk" font-size="9.5" fill="#D8C5B2">{d1_xml}</text>
        {desc2_markup}
      </g>'''

def generate_dr_debug_card():
    b64_debug = get_b64("assets/dr-debug-mascot-opt.png")
    cell_w, cell_h = 254, 54

    c1 = make_compact_cell(0, 0, cell_w, cell_h, "#8E9F70", "DockerBridge Logs", "Live container panics & logs", "Correlates client exceptions", stroke_col="#74825C", fill_col="#1b0813")
    c2 = make_compact_cell(270, 0, cell_w, cell_h, "#9E2D4C", "Flight Recorder", "30s interaction buffer", "Clicks, inputs & route diffs", stroke_col="#9E2D4C", fill_col="#1e0915")
    c3 = make_compact_cell(540, 0, cell_w, cell_h, "#8E9F70", "Shadow DOM HUD", "Zero-pollution root panel", "Chrome DevTools integration", stroke_col="#74825C", fill_col="#1b0813")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 248" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Dr.Debug — Autonomous In-Browser AI Debugging &amp; Runtime Observability Agent">
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

  <rect width="1080" height="248" rx="24" fill="url(#dbgBg)"/>
  <rect width="1080" height="248" rx="24" fill="url(#dbgLattice)"/>

  <!-- Ornate Dual Hairlines -->
  <rect x="14" y="14" width="1052" height="220" rx="18" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.4"/>
  <rect x="20" y="20" width="1040" height="208" rx="14" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.3"/>

  <!-- Baroque Corners -->
  <g stroke="#EADBCE" stroke-width="1.1" fill="none" opacity="0.85">
    <path d="M 26 46 C 26 30, 32 24, 48 24"/>
    <circle cx="28" cy="28" r="1.8" fill="#D8C5B2"/>
    <path d="M 1054 46 C 1054 30, 1048 24, 1032 24"/>
    <circle cx="1052" cy="28" r="1.8" fill="#D8C5B2"/>
    <path d="M 26 202 C 26 218, 32 224, 48 224"/>
    <circle cx="28" cy="220" r="1.8" fill="#D8C5B2"/>
    <path d="M 1054 202 C 1054 218, 1048 224, 1032 224"/>
    <circle cx="1052" cy="220" r="1.8" fill="#D8C5B2"/>
  </g>

  <!-- LEFT: COMPACT ALCOVE (Width=200, Height=196) -->
  <g transform="translate(30, 26)">
    <rect width="200" height="196" rx="16" fill="url(#dbgChamber)" stroke="#74825C" stroke-width="0.8"/>
    <rect x="5" y="5" width="190" height="186" rx="13" fill="none" stroke="#D8C5B2" stroke-width="0.4" opacity="0.4"/>

    <circle cx="100" cy="86" r="64" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.35"/>
    <circle cx="100" cy="86" r="70" fill="none" stroke="#D8C5B2" stroke-width="0.4" stroke-dasharray="3 4" opacity="0.3">
      <animateTransform attributeName="transform" type="rotate" from="0 100 86" to="360 100 86" dur="30s" repeatCount="indefinite"/>
    </circle>

    <!-- Animated Mascot -->
    <g>
      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-6; 0,0" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
      <image href="data:image/png;base64,{b64_debug}" x="22" y="12" width="156" height="148" preserveAspectRatio="xMidYMid meet"/>
      <line x1="32" y1="20" x2="168" y2="20" stroke="url(#dbgScan)" stroke-width="1.5" filter="url(#dbgGlow)" opacity="0.7">
        <animate attributeName="y1" values="20;140;20" dur="4.2s" repeatCount="indefinite"/>
        <animate attributeName="y2" values="20;140;20" dur="4.2s" repeatCount="indefinite"/>
      </line>
    </g>

    <g transform="translate(100, 172)">
      <rect x="-75" y="-10" width="150" height="20" rx="10" fill="#151b11" stroke="#74825C" stroke-width="0.7"/>
      <circle cx="-56" cy="0" r="3" fill="#44FF44" filter="url(#dbgGlow)">
        <animate attributeName="opacity" values="1;0.35;1" dur="1.8s" repeatCount="indefinite"/>
      </circle>
      <text x="6" y="3.5" text-anchor="middle" class="host-grotesk" font-size="10" font-weight="600" fill="#EADBCE" letter-spacing="1">DIAGNOSTIC ACTIVE</text>
    </g>
  </g>

  <!-- RIGHT: EDITORIAL SPECIFICATION (X=254, Width=794) -->
  <g transform="translate(254, 26)">
    <text x="0" y="14" class="host-grotesk" font-size="11" font-weight="600" fill="#8E9F70" letter-spacing="3.5">AUTONOMOUS OBSERVABILITY · MISSION 01</text>
    <text x="0" y="48" class="instrument-serif-regular" font-size="36" fill="url(#dbgGold)" filter="url(#dbgGlow)" letter-spacing="2">DR. DEBUG</text>
    <text x="0" y="68" class="instrument-serif-regular-italic" font-size="15" fill="#EADBCE" letter-spacing="0.5">
      "Autonomous in-browser AI debugging &amp; runtime observability agent."
    </text>

    <line x1="0" y1="82" x2="794" y2="82" stroke="url(#dbgFadeLine)" stroke-width="0.8"/>
    <circle cx="397" cy="82" r="2.2" fill="#D8C5B2"/>

    <!-- 3-PILL COMPACT CAPABILITY MATRIX -->
    <g transform="translate(0, 96)">
      {c1}
      {c2}
      {c3}
    </g>

    <!-- Bottom Footer Row -->
    <g transform="translate(0, 164)">
      <line x1="0" y1="0" x2="794" y2="0" stroke="url(#dbgFadeLine)" stroke-width="0.6"/>
      <g transform="translate(0, 18)" class="host-grotesk" font-size="10.5">
        <text x="0" y="0" fill="#8E9F70" font-weight="500">STACK: TypeScript · Vite · LiteRT / WebLLM · Docker · Re-Act</text>
        <text x="794" y="0" text-anchor="end" fill="#EADBCE" font-weight="600">github.com/SazWhatician/Dr.Debug ↗</text>
      </g>
    </g>
  </g>
</svg>'''

def generate_polaris_card():
    b64_polaris = get_b64("assets/polaris-standalone-opt2.png")
    cell_w, cell_h = 254, 54

    c1 = make_compact_cell(0, 0, cell_w, cell_h, "#8E9F70", "Grounded RAG", "Instant token streaming", "Page-level bounding citations", stroke_col="#74825C", fill_col="#1b0813")
    c2 = make_compact_cell(270, 0, cell_w, cell_h, "#9E2D4C", "Concept Topology", "WebGL2 knowledge graph", "Prerequisite concept mapping", stroke_col="#9E2D4C", fill_col="#1e0915")
    c3 = make_compact_cell(540, 0, cell_w, cell_h, "#8E9F70", "Adaptive Revision", "LangGraph study planner", "Multimodal diagnostic gap", stroke_col="#74825C", fill_col="#1b0813")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 248" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Polaris — Haute Intelligence &amp; Academic AI Navigator">
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

    <filter id="polGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <pattern id="polLattice" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M 18 0 Q 27 9 36 18 Q 27 27 18 36 Q 9 27 0 18 Q 9 9 18 0 Z" fill="none" stroke="#D8C5B2" stroke-width="0.3" opacity="0.05"/>
    </pattern>
  </defs>

  <style>
{SHARED_FONTS_CSS}
  </style>

  <rect width="1080" height="248" rx="24" fill="url(#polBg)"/>
  <rect width="1080" height="248" rx="24" fill="url(#polLattice)"/>

  <!-- Ornate Dual Hairlines -->
  <rect x="14" y="14" width="1052" height="220" rx="18" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.4"/>
  <rect x="20" y="20" width="1040" height="208" rx="14" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.3"/>

  <!-- Baroque Corners -->
  <g stroke="#EADBCE" stroke-width="1.1" fill="none" opacity="0.85">
    <path d="M 26 46 C 26 30, 32 24, 48 24"/>
    <circle cx="28" cy="28" r="1.8" fill="#D8C5B2"/>
    <path d="M 1054 46 C 1054 30, 1048 24, 1032 24"/>
    <circle cx="1052" cy="28" r="1.8" fill="#D8C5B2"/>
    <path d="M 26 202 C 26 218, 32 224, 48 224"/>
    <circle cx="28" cy="220" r="1.8" fill="#D8C5B2"/>
    <path d="M 1054 202 C 1054 218, 1048 224, 1032 224"/>
    <circle cx="1052" cy="220" r="1.8" fill="#D8C5B2"/>
  </g>

  <!-- LEFT: COMPACT ALCOVE (Width=200, Height=196) -->
  <g transform="translate(30, 26)">
    <rect width="200" height="196" rx="16" fill="url(#polChamber)" stroke="#74825C" stroke-width="0.8"/>
    <rect x="5" y="5" width="190" height="186" rx="13" fill="none" stroke="#D8C5B2" stroke-width="0.4" opacity="0.4"/>

    <circle cx="100" cy="86" r="64" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.35"/>
    <circle cx="100" cy="86" r="70" fill="none" stroke="#D8C5B2" stroke-width="0.4" stroke-dasharray="3 4" opacity="0.3">
      <animateTransform attributeName="transform" type="rotate" from="0 100 86" to="360 100 86" dur="30s" repeatCount="indefinite"/>
    </circle>
    <circle cx="100" cy="86" r="45" fill="#8E9F70" opacity="0.16" filter="url(#polGlow)">
      <animate attributeName="opacity" values="0.12;0.24;0.12" dur="2.8s" repeatCount="indefinite"/>
    </circle>

    <!-- Animated Core Image -->
    <g>
      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-6; 0,0" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
      <image href="data:image/png;base64,{b64_polaris}" x="25" y="14" width="150" height="144" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <g transform="translate(100, 172)">
      <rect x="-75" y="-10" width="150" height="20" rx="10" fill="#1b0817" stroke="#9E2D4C" stroke-width="0.7"/>
      <circle cx="-56" cy="0" r="3" fill="#9E2D4C" filter="url(#polGlow)">
        <animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/>
      </circle>
      <text x="6" y="3.5" text-anchor="middle" class="host-grotesk" font-size="10" font-weight="600" fill="#EADBCE" letter-spacing="1">COGNITIVE ORBIT</text>
    </g>
  </g>

  <!-- RIGHT: EDITORIAL SPECIFICATION (X=254, Width=794) -->
  <g transform="translate(254, 26)">
    <text x="0" y="14" class="host-grotesk" font-size="11" font-weight="600" fill="#8E9F70" letter-spacing="3.5">HAUTE INTELLIGENCE · MISSION 02</text>
    <text x="0" y="48" class="instrument-serif-regular" font-size="36" fill="url(#polChampagne)" filter="url(#polGlow)" letter-spacing="2">POLARIS</text>
    <text x="0" y="68" class="instrument-serif-regular-italic" font-size="15" fill="#EADBCE" letter-spacing="0.5">
      "A research canvas that reads like paper — grounded answers with citations."
    </text>

    <line x1="0" y1="82" x2="794" y2="82" stroke="url(#polFadeLine)" stroke-width="0.8"/>
    <circle cx="397" cy="82" r="2.2" fill="#D8C5B2"/>

    <!-- 3-PILL COMPACT CAPABILITY MATRIX -->
    <g transform="translate(0, 96)">
      {c1}
      {c2}
      {c3}
    </g>

    <!-- Bottom Footer Row -->
    <g transform="translate(0, 164)">
      <line x1="0" y1="0" x2="794" y2="0" stroke="url(#polFadeLine)" stroke-width="0.6"/>
      <g transform="translate(0, 18)" class="host-grotesk" font-size="10.5">
        <text x="0" y="0" fill="#8E9F70" font-weight="500">STACK: TypeScript · Next.js · Qdrant · PaddleOCR · LangGraph</text>
        <text x="794" y="0" text-anchor="end" fill="#EADBCE" font-weight="600">github.com/SazWhatician/Polaris ↗</text>
      </g>
    </g>
  </g>
</svg>'''

def generate_medscan_card():
    b64_medscan = get_b64("assets/MedScanAI-opt2.png")
    cell_w, cell_h = 254, 54

    c1 = make_compact_cell(0, 0, cell_w, cell_h, "#8E9F70", "Ensemble Classifier", "High-recall melanoma model", "Multi-class lesion detection", stroke_col="#74825C", fill_col="#1b0813")
    c2 = make_compact_cell(270, 0, cell_w, cell_h, "#9E2D4C", "Deep CNN Radiography", "Chest X-ray screening", "Pathology feature maps", stroke_col="#9E2D4C", fill_col="#1e0915")
    c3 = make_compact_cell(540, 0, cell_w, cell_h, "#8E9F70", "Grad-CAM Heatmaps", "Visual attribution heatmaps", "Clinician second opinions", stroke_col="#74825C", fill_col="#1b0813")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 248" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="MedScan AI — Clinical Tri-Model Vision &amp; Diagnostic Neural Intelligence">
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

  <rect width="1080" height="248" rx="24" fill="url(#medBg)"/>
  <rect width="1080" height="248" rx="24" fill="url(#medLattice)"/>

  <!-- Ornate Dual Hairlines -->
  <rect x="14" y="14" width="1052" height="220" rx="18" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.4"/>
  <rect x="20" y="20" width="1040" height="208" rx="14" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.3"/>

  <!-- Baroque Corners -->
  <g stroke="#EADBCE" stroke-width="1.1" fill="none" opacity="0.85">
    <path d="M 26 46 C 26 30, 32 24, 48 24"/><circle cx="28" cy="28" r="1.8" fill="#D8C5B2"/>
    <path d="M 1054 46 C 1054 30, 1048 24, 1032 24"/><circle cx="1052" cy="28" r="1.8" fill="#D8C5B2"/>
    <path d="M 26 202 C 26 218, 32 224, 48 224"/><circle cx="28" cy="220" r="1.8" fill="#D8C5B2"/>
    <path d="M 1054 202 C 1054 218, 1048 224, 1032 224"/><circle cx="1052" cy="220" r="1.8" fill="#D8C5B2"/>
  </g>

  <!-- LEFT: COMPACT CLINICAL ALCOVE -->
  <g transform="translate(30, 26)">
    <rect width="200" height="196" rx="16" fill="url(#medChamber)" stroke="#74825C" stroke-width="0.8"/>
    <rect x="5" y="5" width="190" height="186" rx="13" fill="none" stroke="#D8C5B2" stroke-width="0.4" opacity="0.4"/>

    <circle cx="100" cy="86" r="64" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.35"/>
    <circle cx="100" cy="86" r="70" fill="none" stroke="#D8C5B2" stroke-width="0.4" stroke-dasharray="3 4" opacity="0.3">
      <animateTransform attributeName="transform" type="rotate" from="0 100 86" to="360 100 86" dur="30s" repeatCount="indefinite"/>
    </circle>
    <circle cx="100" cy="86" r="45" fill="#06B6D4" opacity="0.16" filter="url(#medCyanGlow)">
      <animate attributeName="opacity" values="0.10;0.24;0.10" dur="2.4s" repeatCount="indefinite"/>
    </circle>

    <!-- Animated Core Image -->
    <g>
      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-6; 0,0" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
      <image href="data:image/png;base64,{b64_medscan}" x="25" y="14" width="150" height="144" preserveAspectRatio="xMidYMid meet"/>
      <line x1="32" y1="86" x2="168" y2="86" stroke="url(#ecgGrad)" stroke-width="1.6" filter="url(#medSoftGlow)" opacity="0.75">
        <animate attributeName="y1" values="30;140;30" dur="3.8s" repeatCount="indefinite"/>
        <animate attributeName="y2" values="30;140;30" dur="3.8s" repeatCount="indefinite"/>
      </line>
    </g>

    <g transform="translate(100, 172)">
      <rect x="-75" y="-10" width="150" height="20" rx="10" fill="#071d22" stroke="#74825C" stroke-width="0.8"/>
      <circle cx="-56" cy="0" r="3" fill="#22D3EE" filter="url(#medSoftGlow)">
        <animate attributeName="opacity" values="1;0.35;1" dur="1.4s" repeatCount="indefinite"/>
      </circle>
      <text x="6" y="3.5" text-anchor="middle" class="host-grotesk" font-size="10" font-weight="600" fill="#EADBCE" letter-spacing="1">CLINICAL SCANNER</text>
    </g>
  </g>

  <!-- RIGHT: EDITORIAL SPECIFICATION (X=254, Width=794) -->
  <g transform="translate(254, 26)">
    <text x="0" y="14" class="host-grotesk" font-size="11" font-weight="600" fill="#8E9F70" letter-spacing="3.5">TRI-MODEL DIAGNOSTIC SUITE · MISSION 03</text>
    <text x="0" y="48" class="instrument-serif-regular" font-size="36" fill="url(#medChampagne)" filter="url(#medSoftGlow)" letter-spacing="2">MEDSCAN AI</text>
    <text x="0" y="68" class="instrument-serif-regular-italic" font-size="15" fill="#EADBCE" letter-spacing="0.5">
      "Clinical tri-model vision: skin cancer ensemble, CNN pneumonia, &amp; ANN diabetes."
    </text>

    <line x1="0" y1="82" x2="794" y2="82" stroke="url(#medFadeLine)" stroke-width="0.8"/>
    <circle cx="397" cy="82" r="2.2" fill="#D8C5B2"/>

    <!-- 3-PILL COMPACT CAPABILITY MATRIX -->
    <g transform="translate(0, 96)">
      {c1}
      {c2}
      {c3}
    </g>

    <!-- Bottom Footer Row -->
    <g transform="translate(0, 164)">
      <line x1="0" y1="0" x2="794" y2="0" stroke="url(#medFadeLine)" stroke-width="0.6"/>
      <g transform="translate(0, 18)" class="host-grotesk" font-size="10.5">
        <text x="0" y="0" fill="#8E9F70" font-weight="500">STACK: PyTorch · OpenCV · TorchVision · Grad-CAM · Deep Learning</text>
        <text x="794" y="0" text-anchor="end" fill="#EADBCE" font-weight="600">github.com/SazWhatician/MedScan-AI ↗</text>
      </g>
    </g>
  </g>
</svg>'''

def generate_telemetry_hud(contribs=574, repos=35):
    contrib_str = str(contribs)
    repo_str = str(repos)

    def make_card_reels(num_str, prefix):
        clips = []
        styles = []
        groups = []
        x_start = 36
        w_box = 54
        gap = 4
        step = 58
        for i, ch in enumerate(num_str):
            d = int(ch)
            cid = f"{prefix}{i+1}"
            bx = x_start + i * step
            cx = bx + 27
            clips.append(f'<clipPath id="clip_{cid}"><rect x="{bx}" y="96" width="{w_box}" height="82"/></clipPath>')
            
            if d == 0:
                digits = ['9','8','7','6','5','4','3','2','1','0','0']
                dy = -800
            else:
                digits = [str(k) for k in range(d + 1)]
                dy = -(d * 80)
                
            dur = 2.0 + i * 0.3
            delay = 0.1 + i * 0.08
            kf_name = f"kf_{cid}"
            roll_cls = f"roll_{cid}"
            styles.append(f"    .{roll_cls} {{ animation-name: {kf_name}; animation-duration: {dur:.1f}s; animation-delay: {delay:.2f}s; }}")
            styles.append(f"    @keyframes {kf_name} {{ from {{ transform: translateY(0); }} to {{ transform: translateY({dy}px); }} }}")
            
            text_nodes = "\n".join([f'        <text x="{cx}" y="{166 + k * 80}">{dg}</text>' for k, dg in enumerate(digits)])
            groups.append(f'''    <!-- DIGIT {i+1} ({ch}) centered at x={cx} -->
    <g clip-path="url(#clip_{cid})">
      <g class="reel {roll_cls} instrument-serif-regular" font-size="78" font-weight="700" fill="url(#cntNumeral)" text-anchor="middle">
{text_nodes}
      </g>
    </g>''')
        return clips, styles, groups

    c_clips, c_styles, c_groups = make_card_reels(contrib_str, "CommitC")
    r_clips, r_styles, r_groups = make_card_reels(repo_str, "RepoR")

    all_clips = "\n    ".join(c_clips + r_clips)
    all_styles = "\n".join(c_styles + r_styles)
    c_group_svg = "\n".join(c_groups)
    r_group_svg = "\n".join(r_groups)

    plus_x = 36 + len(contrib_str) * 58 + 4

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Saswat Mohanty — Live Telemetry and All-Time Contributions">
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

    <!-- Dynamic LOCAL Clip Paths -->
    {all_clips}
  </defs>

  <style>
{SHARED_FONTS_CSS}

    .reel {{
      animation-timing-function: cubic-bezier(0.16, 1, 0.3, 1);
      animation-fill-mode: forwards;
      animation-iteration-count: 1;
    }}
{all_styles}

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

  <!-- LEFT CARD: ALL-TIME CONTRIBUTIONS · Position at X=48, Y=78, Width=438, Height=238 -->
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

{c_group_svg}

    <!-- Plus Sign Badge: positioned next to digits -->
    <text x="{plus_x}" y="148" class="instrument-serif-regular-italic" font-weight="700" font-size="44" fill="#8E9F70">+</text>

    <!-- Metric Pill on the right -->
    <g transform="translate(280, 126)">
      <rect x="0" y="-12" width="130" height="24" rx="12" fill="#181e13" stroke="#74825C" stroke-width="0.7"/>
      <circle cx="14" cy="0" r="3" fill="#8E9F70">
        <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
      </circle>
      <text x="72" y="4" text-anchor="middle" class="host-grotesk" font-size="10.5" font-weight="600" fill="#EADBCE">ALL-TIME CRAFT</text>
    </g>

    <!-- Hairline progress bar & footer -->
    <rect x="28" y="194" width="382" height="2" rx="1" fill="#260b19"/>
    <rect class="bar-grow" x="28" y="194" width="382" height="2" rx="1" fill="url(#cntGold)"/>
    <text x="28" y="216" class="host-grotesk" font-size="11.5" fill="#8E9F70">Cumulative commits, pull requests &amp; code reviews</text>
    <text x="410" y="216" text-anchor="end" class="host-grotesk" font-size="11.5" font-weight="600" fill="#D8C5B2">{contribs}+ Logged</text>
  </g>

  <!-- RIGHT CARD: REPOSITORIES · Position at X=514, Y=78, Width=438, Height=238 -->
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

{r_group_svg}

    <!-- Status pill on the right -->
    <g transform="translate(260, 126)">
      <rect x="0" y="-12" width="150" height="24" rx="12" fill="#240a15" stroke="#9E2D4C" stroke-width="0.7"/>
      <circle cx="14" cy="0" r="3" fill="#9E2D4C">
        <animate attributeName="opacity" values="1;0.4;1" dur="2.4s" repeatCount="indefinite"/>
      </circle>
      <text x="82" y="4" text-anchor="middle" class="host-grotesk" font-size="10.5" font-weight="600" fill="#EADBCE">FLAGSHIP BUILDS</text>
    </g>

    <!-- Hairline progress bar & footer -->
    <rect x="28" y="194" width="382" height="2" rx="1" fill="#260b19"/>
    <rect class="bar-grow" x="28" y="194" width="382" height="2" rx="1" fill="url(#cntOlive)" style="animation-delay: 0.2s;"/>
    <text x="28" y="216" class="host-grotesk" font-size="11.5" fill="#8E9F70">AI agents, vision models, &amp; motion canvases</text>
    <text x="410" y="216" text-anchor="end" class="host-grotesk" font-size="11.5" font-weight="600" fill="#D8C5B2">{repos} Active Builds</text>
  </g>
</svg>'''

def build_all(contribs=574, repos=35):
    cards = {
        "assets/dr-debug-card.svg": generate_dr_debug_card(),
        "assets/polaris-card.svg": generate_polaris_card(),
        "assets/medscan-card.svg": generate_medscan_card(),
        "assets/telemetry-hud.svg": generate_telemetry_hud(contribs, repos),
    }

    for path, content in cards.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        ET.parse(path)
        print(f"Generated & Validated XML: {path}")

if __name__ == "__main__":
    build_all(574, 35)
