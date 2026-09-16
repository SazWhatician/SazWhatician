import base64
import os
import xml.etree.ElementTree as ET

def get_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def build_hero_banner():
    b64_violin = get_b64("assets/violin-opt.png")
    b64_cloud1 = get_b64("assets/cloud1-opt.png")
    b64_cloud2 = get_b64("assets/cloud2-opt.png")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 480" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Saswat Mohanty — Haute Craft in Systems, Intelligence and Art">
  <defs>
    <!-- Background Velvet Burgundy Gradient -->
    <linearGradient id="heroVelvetBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#110307">
        <animate attributeName="stop-color" values="#110307;#1a050d;#110307" dur="14s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" stop-color="#220814">
        <animate attributeName="stop-color" values="#220814;#2c0a19;#220814" dur="14s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#0e0205">
        <animate attributeName="stop-color" values="#0e0205;#16030a;#0e0205" dur="14s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <!-- Champagne / Ivory Text Gradient -->
    <linearGradient id="heroChampagne" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="40%" stop-color="#F4E9DC"/>
      <stop offset="70%" stop-color="#EADBCE"/>
      <stop offset="100%" stop-color="#C7AF96"/>
    </linearGradient>

    <!-- Hairline Fade Line -->
    <linearGradient id="heroFadeLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D8C5B2" stop-opacity="0"/>
      <stop offset="15%" stop-color="#D8C5B2" stop-opacity="0.75"/>
      <stop offset="50%" stop-color="#FFFDF9" stop-opacity="0.95"/>
      <stop offset="85%" stop-color="#D8C5B2" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#D8C5B2" stop-opacity="0"/>
    </linearGradient>

    <!-- Soft Glow Filter -->
    <filter id="heroSoftGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Ambient Wine Spotlight Filter -->
    <filter id="heroSpotlight" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Curved Flow Paths for Floating Starlight Dust -->
    <path id="flowTrackA" d="M 60 240 C 260 120, 480 360, 720 200 C 920 80, 1080 320, 1140 240 C 1080 360, 720 120, 480 280 C 260 380, 120 300, 60 240" fill="none"/>
  </defs>

  <style>
    .cursive-brand {{
      font-family: 'Great Vibes', 'Alex Brush', 'Playfair Display', 'Cormorant Garamond', 'Bickham Script Pro', cursive, serif;
    }}
    .serif-brand {{
      font-family: 'Playfair Display', 'Cormorant Garamond', Georgia, serif;
    }}
  </style>

  <!-- Base Canvas -->
  <rect width="1200" height="480" fill="url(#heroVelvetBg)"/>

  <!-- Radial Ambient Atmosphere (Deep Wine & Noble Olive) -->
  <circle cx="280" cy="240" r="280" fill="#6A1B31" opacity="0.22" filter="url(#heroSpotlight)"/>
  <circle cx="920" cy="220" r="260" fill="#4A5538" opacity="0.18" filter="url(#heroSpotlight)"/>
  <circle cx="600" cy="220" r="340" fill="#83223E" opacity="0.16" filter="url(#heroSpotlight)"/>

  <!-- Billowing Golden-Hour Clouds (Cloud 1 & Cloud 2) Drifting Gently in Background -->
  <g opacity="0.32">
    <!-- Cloud 2 drifting on the left horizon -->
    <g>
      <animateTransform attributeName="transform" type="translate" values="0,0; -18,6; 0,0" dur="22s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1; 0.4 0 0.6 1"/>
      <image href="data:image/png;base64,{b64_cloud2}" x="-40" y="160" width="560" height="280" preserveAspectRatio="xMidYMid meet"/>
    </g>
    <!-- Cloud 1 drifting across the center & right base -->
    <g>
      <animateTransform attributeName="transform" type="translate" values="0,0; 22,-6; 0,0" dur="26s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1; 0.4 0 0.6 1"/>
      <image href="data:image/png;base64,{b64_cloud1}" x="520" y="150" width="620" height="310" preserveAspectRatio="xMidYMid meet"/>
    </g>
  </g>

  <!-- The Classical Painter with Violin Companion (Taking Prominent Position on the Right) -->
  <g opacity="0.92">
    <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0" dur="6s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
    <!-- Soft warm rim spotlight behind the painter -->
    <circle cx="940" cy="260" r="180" fill="#83223E" opacity="0.25" filter="url(#heroSpotlight)"/>
    <circle cx="920" cy="280" r="140" fill="#5B6648" opacity="0.20" filter="url(#heroSpotlight)"/>
    <image href="data:image/png;base64,{b64_violin}" x="740" y="45" width="370" height="425" preserveAspectRatio="xMidYMid meet"/>
  </g>

  <!-- Floating Champagne Starlight Dust -->
  <g filter="url(#heroSoftGlow)">
    <circle r="3" fill="#FFFDF9" opacity="0.85">
      <animateMotion dur="20s" repeatCount="indefinite">
        <mpath href="#flowTrackA"/>
      </animateMotion>
    </circle>
    <circle r="2" fill="#8E9F70" opacity="0.75">
      <animateMotion dur="20s" repeatCount="indefinite" begin="-10s">
        <mpath href="#flowTrackA"/>
      </animateMotion>
    </circle>
  </g>

  <!-- Symmetrical Ornate Dual Hairline Frame -->
  <rect x="24" y="24" width="1152" height="432" rx="20" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.45"/>
  <rect x="30" y="30" width="1140" height="420" rx="16" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.35"/>

  <!-- Baroque Corner Flourishes -->
  <g stroke="#EADBCE" stroke-width="1.1" fill="none" opacity="0.85">
    <!-- Top-Left -->
    <path d="M 40 72 C 40 50, 50 40, 72 40"/>
    <path d="M 46 82 C 46 56, 56 46, 82 46"/>
    <circle cx="44" cy="44" r="2.2" fill="#D8C5B2"/>
    <circle cx="72" cy="40" r="1.5" fill="#8E9F70"/>
    <!-- Top-Right -->
    <path d="M 1160 72 C 1160 50, 1150 40, 1128 40"/>
    <path d="M 1154 82 C 1154 56, 1144 46, 1118 46"/>
    <circle cx="1156" cy="44" r="2.2" fill="#D8C5B2"/>
    <circle cx="1128" cy="40" r="1.5" fill="#8E9F70"/>
    <!-- Bottom-Left -->
    <path d="M 40 408 C 40 430, 50 440, 72 440"/>
    <path d="M 46 398 C 46 424, 56 434, 82 434"/>
    <circle cx="44" cy="436" r="2.2" fill="#D8C5B2"/>
    <circle cx="72" cy="440" r="1.5" fill="#8E9F70"/>
    <!-- Bottom-Right -->
    <path d="M 1160 408 C 1160 430, 1150 440, 1128 440"/>
    <path d="M 1154 398 C 1154 424, 1144 434, 1118 434"/>
    <circle cx="1156" cy="436" r="2.2" fill="#D8C5B2"/>
    <circle cx="1128" cy="440" r="1.5" fill="#8E9F70"/>
  </g>

  <!-- Top Header Row: Symmetrical Margins at 64px -->
  <text x="64" y="62" class="serif-brand" font-style="italic" font-size="13.5" fill="#D8C5B2" letter-spacing="4">the private atelier of</text>
  <text x="1136" y="62" text-anchor="end" class="serif-brand" font-style="italic" font-size="13" fill="#8E9F70" letter-spacing="3">— haute ingénierie · edition mmxxiv —</text>
  <line x1="64" y1="76" x2="1136" y2="76" stroke="url(#heroFadeLine)" stroke-width="0.7"/>

  <!-- LEFT & CENTER EDITORIAL CONTENT (Balanced at X=64 to X=720) -->
  <g transform="translate(64, 110)">
    <!-- Monogram Crest & Floral Flourish -->
    <g transform="translate(24, 14)">
      <circle cx="16" cy="16" r="16" fill="#1c0712" stroke="#74825C" stroke-width="0.9"/>
      <circle cx="16" cy="16" r="13" fill="none" stroke="#D8C5B2" stroke-width="0.5" stroke-dasharray="2 3">
        <animateTransform attributeName="transform" type="rotate" from="0 16 16" to="360 16 16" dur="30s" repeatCount="indefinite"/>
      </circle>
      <text x="16" y="22" text-anchor="middle" class="cursive-brand" font-style="italic" font-size="17" fill="url(#heroChampagne)">S</text>
      <!-- Sub-label -->
      <text x="46" y="21" class="serif-brand" font-style="italic" font-size="13" fill="#8E9F70" letter-spacing="2.5">MAISON SASWAT · ARTISAN &amp; ENGINEER</text>
    </g>

    <!-- Main Name: SASWAT MOHANTY in Curvy Designer Brand High-Fashion Typography -->
    <g transform="translate(0, 88)">
      <!-- Curvy Cursive Designer Script Swash Name -->
      <text x="4" y="0" class="cursive-brand" font-style="italic" font-weight="700" font-size="82" fill="url(#heroChampagne)" filter="url(#heroSoftGlow)" letter-spacing="3">
        Saswat Mohanty
      </text>
      <!-- Fine Gold Calligraphic Under-Swash -->
      <path d="M 6 16 C 140 32, 340 -6, 520 20 C 560 26, 600 24, 640 18" fill="none" stroke="url(#heroFadeLine)" stroke-width="1.2"/>
      <circle cx="520" cy="20" r="2.5" fill="#8E9F70"/>
    </g>

    <!-- Literary Philosophy Subtitle -->
    <text x="4" y="148" class="serif-brand" font-style="italic" font-size="20" fill="#EADBCE" letter-spacing="2">
      "Systems that ship. Interfaces that breathe. Craft that endures."
    </text>

    <!-- Precision Capability Pills (Symmetrically Aligned) -->
    <g transform="translate(0, 196)" class="serif-brand" font-size="12" letter-spacing="2">
      <!-- Pill 1: Systems Architecture -->
      <g transform="translate(85, 0)">
        <rect x="-85" y="-14" width="170" height="28" rx="14" fill="#181e13" stroke="#74825C" stroke-width="0.8"/>
        <circle cx="-68" cy="0" r="3" fill="#8E9F70"/>
        <text x="6" y="4" text-anchor="middle" fill="#F6F0E6" font-style="italic">Systems Builder</text>
      </g>
      <!-- Pill 2: Intelligent Agents -->
      <g transform="translate(268, 0)">
        <rect x="-85" y="-14" width="170" height="28" rx="14" fill="#240a15" stroke="#9E2D4C" stroke-width="0.8"/>
        <circle cx="-68" cy="0" r="3" fill="#9E2D4C"/>
        <text x="6" y="4" text-anchor="middle" fill="#F6F0E6" font-style="italic">Intelligent Agents</text>
      </g>
      <!-- Pill 3: Interface Motion -->
      <g transform="translate(451, 0)">
        <rect x="-85" y="-14" width="170" height="28" rx="14" fill="#181e13" stroke="#74825C" stroke-width="0.8"/>
        <circle cx="-68" cy="0" r="3" fill="#8E9F70"/>
        <text x="6" y="4" text-anchor="middle" fill="#F6F0E6" font-style="italic">Interface Motion</text>
      </g>
      <!-- Pill 4: Visionary AI -->
      <g transform="translate(634, 0)">
        <rect x="-85" y="-14" width="170" height="28" rx="14" fill="#240a15" stroke="#9E2D4C" stroke-width="0.8"/>
        <circle cx="-68" cy="0" r="3" fill="#9E2D4C"/>
        <text x="6" y="4" text-anchor="middle" fill="#F6F0E6" font-style="italic">Visionary AI</text>
      </g>
    </g>
  </g>

  <!-- Bottom Rail: Perfectly Aligned Margin at Y=424 -->
  <line x1="64" y1="424" x2="1136" y2="424" stroke="url(#heroFadeLine)" stroke-width="0.5" opacity="0.6"/>
  <g transform="translate(64, 446)">
    <circle cx="0" cy="0" r="4" fill="#8E9F70" filter="url(#heroSoftGlow)">
      <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="14" y="4" class="serif-brand" font-style="italic" font-size="13" fill="#8E9F70" letter-spacing="2">available for collaboration · answering with care</text>
  </g>
  <text x="1136" y="450" text-anchor="end" class="serif-brand" font-style="italic" font-size="13" fill="#D8C5B2" letter-spacing="2.5">bhubaneswar / new delhi · ist · utc+05:30</text>
</svg>'''
    with open("assets/hero-banner.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("hero-banner.svg generated successfully.")

def build_telemetry_hud():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Saswat Mohanty — Live Telemetry and Repository Counters">
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
    <!-- Card dimensions: width=436, height=236. Digits vertically span y=95 to y=175 (height=80) -->
    <!-- Left Card: Commits (305) -->
    <clipPath id="clipCommitC1"><rect x="36" y="96" width="56" height="82"/></clipPath>
    <clipPath id="clipCommitC2"><rect x="94" y="96" width="56" height="82"/></clipPath>
    <clipPath id="clipCommitC3"><rect x="152" y="96" width="56" height="82"/></clipPath>

    <!-- Right Card: Repos (31) -->
    <clipPath id="clipRepoR1"><rect x="36" y="96" width="56" height="82"/></clipPath>
    <clipPath id="clipRepoR2"><rect x="94" y="96" width="56" height="82"/></clipPath>
  </defs>

  <style>
    .serif-brand { font-family: 'Playfair Display', 'Cormorant Garamond', Georgia, serif; }
    .cursive-brand { font-family: 'Great Vibes', 'Alex Brush', 'Playfair Display', 'Cormorant Garamond', cursive, serif; }

    .reel {
      animation-timing-function: cubic-bezier(0.16, 1, 0.3, 1);
      animation-fill-mode: forwards;
      animation-iteration-count: 1;
    }
    /* Digit line height = 80px */
    .roll-c100 { animation-name: kfC100; animation-duration: 2.2s; animation-delay: 0.1s; }
    .roll-c010 { animation-name: kfC010; animation-duration: 2.5s; animation-delay: 0.2s; }
    .roll-c001 { animation-name: kfC001; animation-duration: 2.8s; animation-delay: 0.15s; }

    .roll-r10  { animation-name: kfR10;  animation-duration: 2.0s; animation-delay: 0.25s; }
    .roll-r01  { animation-name: kfR01;  animation-duration: 2.4s; animation-delay: 0.3s; }

    @keyframes kfC100 { from { transform: translateY(0); } to { transform: translateY(-240px); } }
    @keyframes kfC010 { from { transform: translateY(0); } to { transform: translateY(-800px); } }
    @keyframes kfC001 { from { transform: translateY(0); } to { transform: translateY(-400px); } }

    @keyframes kfR10  { from { transform: translateY(0); } to { transform: translateY(-240px); } }
    @keyframes kfR01  { from { transform: translateY(0); } to { transform: translateY(-80px); } }

    .bar-grow {
      transform-origin: left center;
      animation: kfBar 2.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      transform: scaleX(0);
    }
    @keyframes kfBar { to { transform: scaleX(1); } }
  </style>

  <!-- Background -->
  <rect width="1000" height="360" rx="28" fill="url(#cntBg)"/>

  <!-- Ornate Dual Border: Margins at 16px -->
  <rect x="16" y="16" width="968" height="328" rx="22" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.38"/>
  <rect x="22" y="22" width="956" height="316" rx="18" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.3"/>

  <!-- Header Row: Margins at 48px -->
  <text x="48" y="50" class="serif-brand" font-style="italic" font-size="14" fill="#D8C5B2" letter-spacing="3">telemetry index · live git chronicle</text>
  <text x="952" y="50" text-anchor="end" class="serif-brand" font-style="italic" font-size="13" fill="#8E9F70" letter-spacing="2.5">verified author records · @SazWhatician</text>
  <line x1="48" y1="62" x2="952" y2="62" stroke="url(#cntGold)" stroke-width="0.6"/>

  <!-- LEFT CARD: COMMITS (305+) · Position at X=48, Y=78, Width=438, Height=238 -->
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
      <text x="44" y="21" class="serif-brand" font-style="italic" font-size="15" fill="#EADBCE" letter-spacing="2">AUTHENTIC COMMITS</text>
    </g>

    <!-- DIGIT 1 (Hundreds -> 3) centered in clip box x=36..92, center=64 -->
    <g clip-path="url(#clipCommitC1)">
      <g class="reel roll-c100 serif-brand" font-size="78" font-weight="700" fill="url(#cntNumeral)" text-anchor="middle">
        <text x="64" y="166">0</text>
        <text x="64" y="246">1</text>
        <text x="64" y="326">2</text>
        <text x="64" y="406">3</text>
      </g>
    </g>

    <!-- DIGIT 2 (Tens -> 0) centered in clip box x=94..150, center=122 -->
    <g clip-path="url(#clipCommitC2)">
      <g class="reel roll-c010 serif-brand" font-size="78" font-weight="700" fill="url(#cntNumeral)" text-anchor="middle">
        <text x="122" y="166">0</text>
        <text x="122" y="246">7</text>
        <text x="122" y="326">8</text>
        <text x="122" y="406">9</text>
        <text x="122" y="486">3</text>
        <text x="122" y="566">2</text>
        <text x="122" y="646">1</text>
        <text x="122" y="726">6</text>
        <text x="122" y="806">8</text>
        <text x="122" y="886">9</text>
        <text x="122" y="966">0</text>
      </g>
    </g>

    <!-- DIGIT 3 (Ones -> 5) centered in clip box x=152..208, center=180 -->
    <g clip-path="url(#clipCommitC3)">
      <g class="reel roll-c001 serif-brand" font-size="78" font-weight="700" fill="url(#cntNumeral)" text-anchor="middle">
        <text x="180" y="166">0</text>
        <text x="180" y="246">1</text>
        <text x="180" y="326">2</text>
        <text x="180" y="406">3</text>
        <text x="180" y="486">4</text>
        <text x="180" y="566">5</text>
      </g>
    </g>

    <!-- Plus Sign Badge: perfectly positioned next to digits -->
    <text x="216" y="148" class="serif-brand" font-style="italic" font-weight="700" font-size="44" fill="#8E9F70">+</text>

    <!-- Metric Pill on the right -->
    <g transform="translate(280, 126)">
      <rect x="0" y="-12" width="130" height="24" rx="12" fill="#181e13" stroke="#74825C" stroke-width="0.7"/>
      <circle cx="14" cy="0" r="3" fill="#8E9F70">
        <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
      </circle>
      <text x="72" y="4" text-anchor="middle" class="serif-brand" font-style="italic" font-size="11.5" fill="#EADBCE">VERIFIED LOG</text>
    </g>

    <!-- Hairline progress bar & footer (symmetrically padded at 28px) -->
    <rect x="28" y="194" width="382" height="2" rx="1" fill="#260b19"/>
    <rect class="bar-grow" x="28" y="194" width="382" height="2" rx="1" fill="url(#cntGold)"/>
    <text x="28" y="216" class="serif-brand" font-style="italic" font-size="12" fill="#8E9F70">Author commits across repositories</text>
    <text x="410" y="216" text-anchor="end" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">305+ and counting</text>
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
      <text x="44" y="21" class="serif-brand" font-style="italic" font-size="15" fill="#EADBCE" letter-spacing="2">PUBLIC REPOSITORIES</text>
    </g>

    <!-- DIGIT 1 (Tens -> 3) centered in clip box x=36..92, center=64 -->
    <g clip-path="url(#clipRepoR1)">
      <g class="reel roll-r10 serif-brand" font-size="78" font-weight="700" fill="url(#cntNumeral)" text-anchor="middle">
        <text x="64" y="166">0</text>
        <text x="64" y="246">1</text>
        <text x="64" y="326">2</text>
        <text x="64" y="406">3</text>
      </g>
    </g>

    <!-- DIGIT 2 (Ones -> 1) centered in clip box x=94..150, center=122 -->
    <g clip-path="url(#clipRepoR2)">
      <g class="reel roll-r01 serif-brand" font-size="78" font-weight="700" fill="url(#cntNumeral)" text-anchor="middle">
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
      <text x="82" y="4" text-anchor="middle" class="serif-brand" font-style="italic" font-size="11.5" fill="#EADBCE">FLAGSHIP BUILDS</text>
    </g>

    <!-- Hairline progress bar & footer (symmetrically padded at 28px) -->
    <rect x="28" y="194" width="382" height="2" rx="1" fill="#260b19"/>
    <rect class="bar-grow" x="28" y="194" width="382" height="2" rx="1" fill="url(#cntOlive)" style="animation-delay: 0.2s;"/>
    <text x="28" y="216" class="serif-brand" font-style="italic" font-size="12" fill="#8E9F70">AI agents, vision models, &amp; motion canvases</text>
    <text x="410" y="216" text-anchor="end" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">Active Portfolio</text>
  </g>
</svg>'''
    with open("assets/telemetry-hud.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("telemetry-hud.svg generated successfully.")

def build_polaris_card():
    b64_polaris = get_b64("assets/polaris-standalone-opt2.png")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Polaris — The Research Canvas That Reads Like Paper">
  <defs>
    <!-- Background Velvet Burgundy Gradient -->
    <linearGradient id="polBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#120308"/>
      <stop offset="50%" stop-color="#1e0714"/>
      <stop offset="100%" stop-color="#0e0206"/>
    </linearGradient>

    <!-- Cosmic Chamber Radial Gradient -->
    <radialGradient id="polChamber" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#220a2e" stop-opacity="0.9"/>
      <stop offset="55%" stop-color="#15061c" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#0d0208" stop-opacity="0.95"/>
    </radialGradient>

    <!-- Champagne Text Gradient -->
    <linearGradient id="polChampagne" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="45%" stop-color="#EADBCE"/>
      <stop offset="100%" stop-color="#C7AF96"/>
    </linearGradient>

    <!-- Hairline Fade Divider -->
    <linearGradient id="polFadeLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D8C5B2" stop-opacity="0"/>
      <stop offset="25%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#FFFDF9" stop-opacity="1"/>
      <stop offset="75%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#D8C5B2" stop-opacity="0"/>
    </linearGradient>

    <!-- Cosmic Blue/Violet Glow Filter -->
    <filter id="polCosmicGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="polSoftGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Constellation Lattice Pattern -->
    <pattern id="polLattice" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M 18 0 Q 27 9 36 18 Q 27 27 18 36 Q 9 27 0 18 Q 9 9 18 0 Z" fill="none" stroke="#D8C5B2" stroke-width="0.3" opacity="0.05"/>
    </pattern>
  </defs>

  <style>
    .serif-brand {{ font-family: 'Playfair Display', 'Cormorant Garamond', Georgia, serif; }}
    .cursive-brand {{ font-family: 'Great Vibes', 'Alex Brush', 'Playfair Display', 'Cormorant Garamond', cursive, serif; }}
  </style>

  <!-- Card Background -->
  <rect width="1000" height="440" rx="28" fill="url(#polBg)"/>
  <rect width="1000" height="440" rx="28" fill="url(#polLattice)"/>

  <!-- Ornate Dual Hairlines -->
  <rect x="16" y="16" width="968" height="408" rx="22" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.4"/>
  <rect x="22" y="22" width="956" height="396" rx="18" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.3"/>

  <!-- Baroque Corner Flourishes -->
  <g stroke="#EADBCE" stroke-width="1.1" fill="none" opacity="0.85">
    <path d="M 28 54 C 28 36, 36 28, 54 28"/>
    <circle cx="32" cy="32" r="1.8" fill="#D8C5B2"/>
    <path d="M 972 54 C 972 36, 964 28, 946 28"/>
    <circle cx="968" cy="32" r="1.8" fill="#D8C5B2"/>
    <path d="M 28 386 C 28 404, 36 412, 54 412"/>
    <circle cx="32" cy="408" r="1.8" fill="#D8C5B2"/>
    <path d="M 972 386 C 972 404, 964 412, 946 412"/>
    <circle cx="968" cy="408" r="1.8" fill="#D8C5B2"/>
  </g>

  <!-- LEFT: 3D POLARIS ORB CHAMBER (Width=320, Height=344) -->
  <g transform="translate(48, 48)">
    <rect width="320" height="344" rx="20" fill="url(#polChamber)" stroke="#74825C" stroke-width="0.8"/>
    <rect x="6" y="6" width="308" height="332" rx="16" fill="none" stroke="#D8C5B2" stroke-width="0.4" opacity="0.4"/>

    <!-- Concentric Celestial Rings -->
    <circle cx="160" cy="165" r="128" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.35"/>
    <circle cx="160" cy="165" r="136" fill="none" stroke="#D8C5B2" stroke-width="0.4" stroke-dasharray="3 4" opacity="0.3">
      <animateTransform attributeName="transform" type="rotate" from="0 160 165" to="360 160 165" dur="35s" repeatCount="indefinite"/>
    </circle>

    <!-- Cosmic Glow behind logo -->
    <circle cx="160" cy="165" r="100" fill="#3B82F6" opacity="0.18" filter="url(#polCosmicGlow)">
      <animate attributeName="opacity" values="0.12;0.25;0.12" dur="4s" repeatCount="indefinite"/>
    </circle>

    <!-- Animated Floating Polaris 'P' Logo -->
    <g>
      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0" dur="4.2s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
      <image href="data:image/png;base64,{b64_polaris}" x="50" y="45" width="220" height="240" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <!-- Bottom Status Pill -->
    <g transform="translate(160, 316)">
      <rect x="-75" y="-12" width="150" height="24" rx="12" fill="#170c26" stroke="#8E9F70" stroke-width="0.8"/>
      <circle cx="-56" cy="0" r="3.5" fill="#38BDF8" filter="url(#polSoftGlow)">
        <animate attributeName="opacity" values="1;0.35;1" dur="1.8s" repeatCount="indefinite"/>
      </circle>
      <text x="8" y="4" text-anchor="middle" class="serif-brand" font-style="italic" font-size="12" fill="#EADBCE" letter-spacing="1.5">RESEARCH ENGINE</text>
    </g>
  </g>

  <!-- RIGHT: EDITORIAL SPECIFICATION (X=406, Width=540, Margin=54) -->
  <g transform="translate(406, 56)">
    <!-- Eyebrow Subheading -->
    <text x="0" y="16" class="serif-brand" font-style="italic" font-size="13" fill="#8E9F70" letter-spacing="3.5">FLAGSHIP COGNITIVE CANVAS · MISSION 02</text>

    <!-- Grand Flowy Title: POLARIS -->
    <text x="0" y="62" class="serif-brand" font-weight="700" font-size="44" fill="url(#polChampagne)" filter="url(#polSoftGlow)" letter-spacing="4">POLARIS</text>

    <!-- Cursive Literary Quote -->
    <text x="0" y="94" class="serif-brand" font-style="italic" font-size="18" fill="#EADBCE" letter-spacing="1">
      "A research canvas that reads like paper — grounded answers with citations."
    </text>

    <!-- Curvy Hairline Divider with Pearl -->
    <line x1="0" y1="116" x2="540" y2="116" stroke="url(#polFadeLine)" stroke-width="0.8"/>
    <circle cx="270" cy="116" r="2.5" fill="#D8C5B2"/>

    <!-- 2x2 LUXURY CAPABILITY SPECIFICATION MATRIX -->
    <g transform="translate(0, 136)">
      <!-- Cell 1: Citation-Grounded Synthesis -->
      <g transform="translate(0, 0)">
        <rect width="258" height="66" rx="14" fill="#1b0813" stroke="#74825C" stroke-width="0.7"/>
        <circle cx="20" cy="22" r="3" fill="#8E9F70"/>
        <text x="32" y="25" class="serif-brand" font-style="italic" font-weight="600" font-size="13" fill="#F6F0E6" letter-spacing="1">Grounded Synthesis</text>
        <text x="32" y="46" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">Citations, honest gaps, verified facts</text>
      </g>
      <!-- Cell 2: LangGraph State Core -->
      <g transform="translate(276, 0)">
        <rect width="264" height="66" rx="14" fill="#1e0915" stroke="#9E2D4C" stroke-width="0.7"/>
        <circle cx="20" cy="22" r="3" fill="#9E2D4C"/>
        <text x="32" y="25" class="serif-brand" font-style="italic" font-weight="600" font-size="13" fill="#F6F0E6" letter-spacing="1">LangGraph Cognitive Loop</text>
        <text x="32" y="46" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">Multi-turn agentic deliberation</text>
      </g>
    </g>

    <g transform="translate(0, 218)">
      <!-- Cell 3: Paper Typography & Quiet Motion -->
      <g transform="translate(0, 0)">
        <rect width="258" height="66" rx="14" fill="#1e0915" stroke="#9E2D4C" stroke-width="0.7"/>
        <circle cx="20" cy="22" r="3" fill="#9E2D4C"/>
        <text x="32" y="25" class="serif-brand" font-style="italic" font-weight="600" font-size="13" fill="#F6F0E6" letter-spacing="1">Quiet Typography</text>
        <text x="32" y="46" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">Editorial layout designed for long reading</text>
      </g>
      <!-- Cell 4: Streaming Architecture -->
      <g transform="translate(276, 0)">
        <rect width="264" height="66" rx="14" fill="#1b0813" stroke="#74825C" stroke-width="0.7"/>
        <circle cx="20" cy="22" r="3" fill="#8E9F70"/>
        <text x="32" y="25" class="serif-brand" font-style="italic" font-weight="600" font-size="13" fill="#F6F0E6" letter-spacing="1">Streaming Latency</text>
        <text x="32" y="46" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">Real-time token dispatch &amp; UI render</text>
      </g>
    </g>

    <!-- Bottom Footer Row: Stack & Repository Link -->
    <g transform="translate(0, 314)">
      <line x1="0" y1="0" x2="540" y2="0" stroke="url(#polFadeLine)" stroke-width="0.6"/>
      <g transform="translate(0, 18)" class="serif-brand" font-style="italic" font-size="12">
        <text x="0" y="4" fill="#8E9F70">STACK: Next.js · TypeScript · LangGraph · Gemini</text>
        <text x="540" y="4" text-anchor="end" fill="#EADBCE">github.com/SazWhatician/Polaris ↗</text>
      </g>
    </g>
  </g>
</svg>'''
    with open("assets/polaris-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("polaris-card.svg generated successfully.")

def build_medscan_card():
    b64_medscan = get_b64("assets/MedScanAI-opt2.png")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="MedScan AI — Vision Models for the Clinic">
  <defs>
    <!-- Background Velvet Burgundy Gradient -->
    <linearGradient id="medBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#120308"/>
      <stop offset="50%" stop-color="#1f0714"/>
      <stop offset="100%" stop-color="#0e0206"/>
    </linearGradient>

    <!-- Clinic Diagnostic Alcove -->
    <radialGradient id="medChamber" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#0a1e24" stop-opacity="0.9"/>
      <stop offset="55%" stop-color="#071419" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#0d0208" stop-opacity="0.95"/>
    </radialGradient>

    <!-- Champagne Text Gradient -->
    <linearGradient id="medChampagne" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="45%" stop-color="#EADBCE"/>
      <stop offset="100%" stop-color="#C7AF96"/>
    </linearGradient>

    <!-- Hairline Fade Line -->
    <linearGradient id="medFadeLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D8C5B2" stop-opacity="0"/>
      <stop offset="25%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#FFFDF9" stop-opacity="1"/>
      <stop offset="75%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#D8C5B2" stop-opacity="0"/>
    </linearGradient>

    <!-- Cyan ECG Pulse Sweep Gradient -->
    <linearGradient id="ecgGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#06B6D4" stop-opacity="0"/>
      <stop offset="50%" stop-color="#22D3EE" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#06B6D4" stop-opacity="0"/>
    </linearGradient>

    <filter id="medCyanGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="medSoftGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Lattice Grid -->
    <pattern id="medLattice" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M 18 0 Q 27 9 36 18 Q 27 27 18 36 Q 9 27 0 18 Q 9 9 18 0 Z" fill="none" stroke="#D8C5B2" stroke-width="0.3" opacity="0.05"/>
    </pattern>
  </defs>

  <style>
    .serif-brand {{ font-family: 'Playfair Display', 'Cormorant Garamond', Georgia, serif; }}
    .cursive-brand {{ font-family: 'Great Vibes', 'Alex Brush', 'Playfair Display', 'Cormorant Garamond', cursive, serif; }}
  </style>

  <!-- Card Background -->
  <rect width="1000" height="440" rx="28" fill="url(#medBg)"/>
  <rect width="1000" height="440" rx="28" fill="url(#medLattice)"/>

  <!-- Ornate Dual Hairlines -->
  <rect x="16" y="16" width="968" height="408" rx="22" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.4"/>
  <rect x="22" y="22" width="956" height="396" rx="18" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.3"/>

  <!-- Baroque Corner Flourishes -->
  <g stroke="#EADBCE" stroke-width="1.1" fill="none" opacity="0.85">
    <path d="M 28 54 C 28 36, 36 28, 54 28"/>
    <circle cx="32" cy="32" r="1.8" fill="#D8C5B2"/>
    <path d="M 972 54 C 972 36, 964 28, 946 28"/>
    <circle cx="968" cy="32" r="1.8" fill="#D8C5B2"/>
    <path d="M 28 386 C 28 404, 36 412, 54 412"/>
    <circle cx="32" cy="408" r="1.8" fill="#D8C5B2"/>
    <path d="M 972 386 C 972 404, 964 412, 946 412"/>
    <circle cx="968" cy="408" r="1.8" fill="#D8C5B2"/>
  </g>

  <!-- LEFT: CLINICAL VISION CHAMBER (Width=320, Height=344) -->
  <g transform="translate(48, 48)">
    <rect width="320" height="344" rx="20" fill="url(#medChamber)" stroke="#74825C" stroke-width="0.8"/>
    <rect x="6" y="6" width="308" height="332" rx="16" fill="none" stroke="#D8C5B2" stroke-width="0.4" opacity="0.4"/>

    <!-- Concentric Medical Scanner Rings -->
    <circle cx="160" cy="165" r="128" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.35"/>
    <circle cx="160" cy="165" r="136" fill="none" stroke="#D8C5B2" stroke-width="0.4" stroke-dasharray="3 4" opacity="0.3">
      <animateTransform attributeName="transform" type="rotate" from="0 160 165" to="360 160 165" dur="32s" repeatCount="indefinite"/>
    </circle>

    <!-- Cyan Pulse Glow Behind Logo -->
    <circle cx="160" cy="165" r="90" fill="#06B6D4" opacity="0.16" filter="url(#medCyanGlow)">
      <animate attributeName="opacity" values="0.10;0.24;0.10" dur="2.4s" repeatCount="indefinite"/>
    </circle>

    <!-- Animated Floating MedScan 'M' Logo -->
    <g>
      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
      <image href="data:image/png;base64,{b64_medscan}" x="50" y="45" width="220" height="240" preserveAspectRatio="xMidYMid meet"/>
      <!-- Sweeping Vital ECG Diagnostic Line across the chamber -->
      <line x1="50" y1="165" x2="270" y2="165" stroke="url(#ecgGrad)" stroke-width="1.8" filter="url(#medSoftGlow)" opacity="0.75">
        <animate attributeName="y1" values="80;250;80" dur="4.2s" repeatCount="indefinite"/>
        <animate attributeName="y2" values="80;250;80" dur="4.2s" repeatCount="indefinite"/>
      </line>
    </g>

    <!-- Bottom Status Pill -->
    <g transform="translate(160, 316)">
      <rect x="-75" y="-12" width="150" height="24" rx="12" fill="#071d22" stroke="#74825C" stroke-width="0.8"/>
      <circle cx="-56" cy="0" r="3.5" fill="#22D3EE" filter="url(#medSoftGlow)">
        <animate attributeName="opacity" values="1;0.35;1" dur="1.4s" repeatCount="indefinite"/>
      </circle>
      <text x="8" y="4" text-anchor="middle" class="serif-brand" font-style="italic" font-size="12" fill="#EADBCE" letter-spacing="1.5">CLINICAL SCANNER</text>
    </g>
  </g>

  <!-- RIGHT: EDITORIAL SPECIFICATION (X=406, Width=540, Margin=54) -->
  <g transform="translate(406, 56)">
    <!-- Eyebrow Subheading -->
    <text x="0" y="16" class="serif-brand" font-style="italic" font-size="13" fill="#8E9F70" letter-spacing="3.5">FLAGSHIP MEDICAL VISION · MISSION 03</text>

    <!-- Grand Title: MEDSCAN AI -->
    <text x="0" y="62" class="serif-brand" font-weight="700" font-size="44" fill="url(#medChampagne)" filter="url(#medSoftGlow)" letter-spacing="4">MEDSCAN AI</text>

    <!-- Cursive Literary Quote -->
    <text x="0" y="94" class="serif-brand" font-style="italic" font-size="18" fill="#EADBCE" letter-spacing="1">
      "Vision models for the clinic — lesion detection, heatmap signal, careful pixel analysis."
    </text>

    <!-- Curvy Hairline Divider with Pearl -->
    <line x1="0" y1="116" x2="540" y2="116" stroke="url(#medFadeLine)" stroke-width="0.8"/>
    <circle cx="270" cy="116" r="2.5" fill="#D8C5B2"/>

    <!-- 2x2 LUXURY CAPABILITY SPECIFICATION MATRIX -->
    <g transform="translate(0, 136)">
      <!-- Cell 1: Lesion & Pathology Segmentation -->
      <g transform="translate(0, 0)">
        <rect width="258" height="66" rx="14" fill="#1b0813" stroke="#74825C" stroke-width="0.7"/>
        <circle cx="20" cy="22" r="3" fill="#8E9F70"/>
        <text x="32" y="25" class="serif-brand" font-style="italic" font-weight="600" font-size="13" fill="#F6F0E6" letter-spacing="1">Lesion Segmentation</text>
        <text x="32" y="46" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">Deep CNN &amp; Vision Transformer backbone</text>
      </g>
      <!-- Cell 2: Grad-CAM Explainability -->
      <g transform="translate(276, 0)">
        <rect width="264" height="66" rx="14" fill="#1e0915" stroke="#9E2D4C" stroke-width="0.7"/>
        <circle cx="20" cy="22" r="3" fill="#9E2D4C"/>
        <text x="32" y="25" class="serif-brand" font-style="italic" font-weight="600" font-size="13" fill="#F6F0E6" letter-spacing="1">Heatmap Attribution</text>
        <text x="32" y="46" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">Grad-CAM visual trust for radiologists</text>
      </g>
    </g>

    <g transform="translate(0, 218)">
      <!-- Cell 3: Second-Opinion Signal -->
      <g transform="translate(0, 0)">
        <rect width="258" height="66" rx="14" fill="#1e0915" stroke="#9E2D4C" stroke-width="0.7"/>
        <circle cx="20" cy="22" r="3" fill="#9E2D4C"/>
        <text x="32" y="25" class="serif-brand" font-style="italic" font-weight="600" font-size="13" fill="#F6F0E6" letter-spacing="1">Clinician Co-Pilot</text>
        <text x="32" y="46" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">High-recall screening for triage workflows</text>
      </g>
      <!-- Cell 4: DICOM & High-Res Pipeline -->
      <g transform="translate(276, 0)">
        <rect width="264" height="66" rx="14" fill="#1b0813" stroke="#74825C" stroke-width="0.7"/>
        <circle cx="20" cy="22" r="3" fill="#8E9F70"/>
        <text x="32" y="25" class="serif-brand" font-style="italic" font-weight="600" font-size="13" fill="#F6F0E6" letter-spacing="1">DICOM High-Res Pipe</text>
        <text x="32" y="46" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">PyTorch, TorchVision &amp; OpenCV core</text>
      </g>
    </g>

    <!-- Bottom Footer Row: Stack & Repository Link -->
    <g transform="translate(0, 314)">
      <line x1="0" y1="0" x2="540" y2="0" stroke="url(#medFadeLine)" stroke-width="0.6"/>
      <g transform="translate(0, 18)" class="serif-brand" font-style="italic" font-size="12">
        <text x="0" y="4" fill="#8E9F70">STACK: PyTorch · OpenCV · TorchVision · Medical AI</text>
        <text x="540" y="4" text-anchor="end" fill="#EADBCE">github.com/SazWhatician/MedScan-AI ↗</text>
      </g>
    </g>
  </g>
</svg>'''
    with open("assets/medscan-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("medscan-card.svg generated successfully.")

def build_dr_debug_card_refined():
    # Make sure dr-debug-card has identical alignment and luxury brand styling
    b64_debug = get_b64("assets/dr-debug-mascot-opt.png")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Dr.Debug — The Autonomous AI Debugging Agent">
  <defs>
    <!-- Background Velvet Burgundy Gradient -->
    <linearGradient id="dbgBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#120308"/>
      <stop offset="50%" stop-color="#1f0714"/>
      <stop offset="100%" stop-color="#0e0206"/>
    </linearGradient>

    <!-- Lab Chamber Radial Gradient -->
    <radialGradient id="dbgChamber" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#2a0d1c" stop-opacity="0.9"/>
      <stop offset="55%" stop-color="#190610" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#0d0206" stop-opacity="0.95"/>
    </radialGradient>

    <!-- Champagne / Ivory Text Gradient -->
    <linearGradient id="dbgGold" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="45%" stop-color="#EADBCE"/>
      <stop offset="100%" stop-color="#C7AF96"/>
    </linearGradient>

    <!-- Hairline Fade Gradient -->
    <linearGradient id="dbgFadeLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D8C5B2" stop-opacity="0"/>
      <stop offset="25%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#FFFDF9" stop-opacity="1"/>
      <stop offset="75%" stop-color="#D8C5B2" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#D8C5B2" stop-opacity="0"/>
    </linearGradient>

    <!-- Scanner Line Gradient -->
    <linearGradient id="dbgScan" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8E9F70" stop-opacity="0"/>
      <stop offset="50%" stop-color="#44FF44" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#8E9F70" stop-opacity="0"/>
    </linearGradient>

    <!-- Soft Glow Filter -->
    <filter id="dbgGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="dbgPotionGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Lattice Pattern -->
    <pattern id="dbgLattice" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M 18 0 Q 27 9 36 18 Q 27 27 18 36 Q 9 27 0 18 Q 9 9 18 0 Z" fill="none" stroke="#D8C5B2" stroke-width="0.3" opacity="0.05"/>
    </pattern>
  </defs>

  <style>
    .serif-brand {{ font-family: 'Playfair Display', 'Cormorant Garamond', Georgia, serif; }}
    .cursive-brand {{ font-family: 'Great Vibes', 'Alex Brush', 'Playfair Display', 'Cormorant Garamond', cursive, serif; }}
  </style>

  <!-- Card Background -->
  <rect width="1000" height="440" rx="28" fill="url(#dbgBg)"/>
  <rect width="1000" height="440" rx="28" fill="url(#dbgLattice)"/>

  <!-- Ornate Dual Hairlines -->
  <rect x="16" y="16" width="968" height="408" rx="22" fill="none" stroke="#D8C5B2" stroke-width="0.8" opacity="0.4"/>
  <rect x="22" y="22" width="956" height="396" rx="18" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.3"/>

  <!-- Baroque Corner Flourishes -->
  <g stroke="#EADBCE" stroke-width="1.1" fill="none" opacity="0.85">
    <path d="M 28 54 C 28 36, 36 28, 54 28"/>
    <circle cx="32" cy="32" r="1.8" fill="#D8C5B2"/>
    <path d="M 972 54 C 972 36, 964 28, 946 28"/>
    <circle cx="968" cy="32" r="1.8" fill="#D8C5B2"/>
    <path d="M 28 386 C 28 404, 36 412, 54 412"/>
    <circle cx="32" cy="408" r="1.8" fill="#D8C5B2"/>
    <path d="M 972 386 C 972 404, 964 412, 946 412"/>
    <circle cx="968" cy="408" r="1.8" fill="#D8C5B2"/>
  </g>

  <!-- LEFT: DR. DEBUG LAB ALCOVE (Width=320, Height=344) -->
  <g transform="translate(48, 48)">
    <rect width="320" height="344" rx="20" fill="url(#dbgChamber)" stroke="#74825C" stroke-width="0.8"/>
    <rect x="6" y="6" width="308" height="332" rx="16" fill="none" stroke="#D8C5B2" stroke-width="0.4" opacity="0.4"/>

    <!-- Concentric Decorative Rings -->
    <circle cx="160" cy="165" r="128" fill="none" stroke="#74825C" stroke-width="0.5" opacity="0.35"/>
    <circle cx="160" cy="165" r="136" fill="none" stroke="#D8C5B2" stroke-width="0.4" stroke-dasharray="3 4" opacity="0.3">
      <animateTransform attributeName="transform" type="rotate" from="0 160 165" to="360 160 165" dur="30s" repeatCount="indefinite"/>
    </circle>

    <!-- Rising Potion Bubbles -->
    <g fill="#44FF44" opacity="0.5" filter="url(#dbgGlow)">
      <circle cx="120" cy="280" r="3">
        <animate attributeName="cy" values="280;100" dur="4s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0;0.7;0" dur="4s" repeatCount="indefinite"/>
      </circle>
      <circle cx="200" cy="290" r="2">
        <animate attributeName="cy" values="290;90" dur="5s" repeatCount="indefinite" begin="-2s"/>
        <animate attributeName="opacity" values="0;0.6;0" dur="5s" repeatCount="indefinite" begin="-2s"/>
      </circle>
      <circle cx="150" cy="270" r="2.5">
        <animate attributeName="cy" values="270;110" dur="3.5s" repeatCount="indefinite" begin="-1.2s"/>
        <animate attributeName="opacity" values="0;0.8;0" dur="3.5s" repeatCount="indefinite" begin="-1.2s"/>
      </circle>
    </g>

    <!-- Animated Mascot with Floating Physics -->
    <g>
      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
      <image href="data:image/png;base64,{b64_debug}" x="40" y="32" width="240" height="262" preserveAspectRatio="xMidYMid meet"/>
      <!-- Soft Scanner Beam sweeping vertically across Dr.Debug -->
      <line x1="60" y1="50" x2="260" y2="50" stroke="url(#dbgScan)" stroke-width="1.6" filter="url(#dbgGlow)" opacity="0.65">
        <animate attributeName="y1" values="50;270;50" dur="4.8s" repeatCount="indefinite"/>
        <animate attributeName="y2" values="50;270;50" dur="4.8s" repeatCount="indefinite"/>
      </line>
    </g>

    <!-- Bottom Capsule Base Status -->
    <g transform="translate(160, 316)">
      <rect x="-75" y="-12" width="150" height="24" rx="12" fill="#151b11" stroke="#74825C" stroke-width="0.8"/>
      <circle cx="-56" cy="0" r="3.5" fill="#44FF44" filter="url(#dbgGlow)">
        <animate attributeName="opacity" values="1;0.35;1" dur="1.8s" repeatCount="indefinite"/>
      </circle>
      <text x="8" y="4" text-anchor="middle" class="serif-brand" font-style="italic" font-size="12" fill="#EADBCE" letter-spacing="1.5">DIAGNOSTIC ACTIVE</text>
    </g>
  </g>

  <!-- RIGHT: EDITORIAL SPECIFICATION (X=406, Width=540, Margin=54) -->
  <g transform="translate(406, 56)">
    <!-- Eyebrow Subheading -->
    <text x="0" y="16" class="serif-brand" font-style="italic" font-size="13" fill="#8E9F70" letter-spacing="3.5">FLAGSHIP AUTONOMOUS AGENT · MISSION 01</text>

    <!-- Grand Title: DR. DEBUG -->
    <text x="0" y="62" class="serif-brand" font-weight="700" font-size="44" fill="url(#dbgGold)" filter="url(#dbgGlow)" letter-spacing="4">DR. DEBUG</text>

    <!-- Cursive Literary Quote -->
    <text x="0" y="94" class="serif-brand" font-style="italic" font-size="18" fill="#EADBCE" letter-spacing="1">
      "The debugger that debugs itself — traces errors, writes the RCA, and opens the PR."
    </text>

    <!-- Curvy Hairline Divider with Pearl -->
    <line x1="0" y1="116" x2="540" y2="116" stroke="url(#dbgFadeLine)" stroke-width="0.8"/>
    <circle cx="270" cy="116" r="2.5" fill="#D8C5B2"/>

    <!-- 2x2 LUXURY CAPABILITY SPECIFICATION MATRIX -->
    <g transform="translate(0, 136)">
      <!-- Cell 1: Autonomous RCA Engine -->
      <g transform="translate(0, 0)">
        <rect width="258" height="66" rx="14" fill="#1b0813" stroke="#74825C" stroke-width="0.7"/>
        <circle cx="20" cy="22" r="3" fill="#8E9F70"/>
        <text x="32" y="25" class="serif-brand" font-style="italic" font-weight="600" font-size="13" fill="#F6F0E6" letter-spacing="1">Autonomous RCA Engine</text>
        <text x="32" y="46" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">Deep runtime trace &amp; AST synthesis</text>
      </g>
      <!-- Cell 2: LangGraph State Core -->
      <g transform="translate(276, 0)">
        <rect width="264" height="66" rx="14" fill="#1e0915" stroke="#9E2D4C" stroke-width="0.7"/>
        <circle cx="20" cy="22" r="3" fill="#9E2D4C"/>
        <text x="32" y="25" class="serif-brand" font-style="italic" font-weight="600" font-size="13" fill="#F6F0E6" letter-spacing="1">LangGraph State Core</text>
        <text x="32" y="46" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">Claude 3.5 Sonnet agent graph</text>
      </g>
    </g>

    <g transform="translate(0, 218)">
      <!-- Cell 3: Zero-Touch PR Workflow -->
      <g transform="translate(0, 0)">
        <rect width="258" height="66" rx="14" fill="#1e0915" stroke="#9E2D4C" stroke-width="0.7"/>
        <circle cx="20" cy="22" r="3" fill="#9E2D4C"/>
        <text x="32" y="25" class="serif-brand" font-style="italic" font-weight="600" font-size="13" fill="#F6F0E6" letter-spacing="1">Signed Pull Requests</text>
        <text x="32" y="46" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">Generates unit tests &amp; commits patch</text>
      </g>
      <!-- Cell 4: Observability Native -->
      <g transform="translate(276, 0)">
        <rect width="264" height="66" rx="14" fill="#1b0813" stroke="#74825C" stroke-width="0.7"/>
        <circle cx="20" cy="22" r="3" fill="#8E9F70"/>
        <text x="32" y="25" class="serif-brand" font-style="italic" font-weight="600" font-size="13" fill="#F6F0E6" letter-spacing="1">Observability Native</text>
        <text x="32" y="46" class="serif-brand" font-style="italic" font-size="12" fill="#D8C5B2">FastAPI, Docker &amp; Sentry telemetry</text>
      </g>
    </g>

    <!-- Bottom Footer Row: Stack Badges & Repository Link -->
    <g transform="translate(0, 314)">
      <line x1="0" y1="0" x2="540" y2="0" stroke="url(#dbgFadeLine)" stroke-width="0.6"/>
      <g transform="translate(0, 18)" class="serif-brand" font-style="italic" font-size="12">
        <text x="0" y="4" fill="#8E9F70">STACK: TypeScript · Python · Claude · Docker</text>
        <text x="540" y="4" text-anchor="end" fill="#EADBCE">github.com/SazWhatician/Dr.Debug ↗</text>
      </g>
    </g>
  </g>
</svg>'''
    with open("assets/dr-debug-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("dr-debug-card.svg generated successfully.")

if __name__ == "__main__":
    build_hero_banner()
    build_telemetry_hud()
    build_polaris_card()
    build_medscan_card()
    build_dr_debug_card_refined()

    # Verify all SVGs
    for f in ["assets/hero-banner.svg", "assets/telemetry-hud.svg", "assets/dr-debug-card.svg", "assets/polaris-card.svg", "assets/medscan-card.svg"]:
        ET.parse(f)
        print(f"Validated XML: {f}")
