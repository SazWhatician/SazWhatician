"""
Script to dynamically update the live GitHub all-time contributions and repository counters in assets/telemetry-hud.svg
Can be executed locally or in a GitHub Actions workflow.
"""
import urllib.request
import json
import re
import os
import xml.etree.ElementTree as ET
from generate_cards import generate_telemetry_hud

USERNAME = "SazWhatician"

def fetch_stats():
    headers = {"User-Agent": "Mozilla/5.0 (Python-Telemetry-Updater)"}
    
    # 1. Fetch public repos
    try:
        req_user = urllib.request.Request(f"https://api.github.com/users/{USERNAME}", headers=headers)
        with urllib.request.urlopen(req_user, timeout=10) as resp:
            user_data = json.loads(resp.read().decode())
            repos_count = user_data.get("public_repos", 35)
    except Exception as e:
        print(f"Warning: could not fetch repos ({e}), defaulting to 35")
        repos_count = 35
    
    # 2. Fetch all-time contributions
    try:
        req_summary = urllib.request.Request(
            f"https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username={USERNAME}",
            headers=headers
        )
        with urllib.request.urlopen(req_summary, timeout=10) as resp:
            content = resp.read().decode()
            match = re.search(r"(\d+)\s+Contributions", content, re.I)
            if match:
                contrib_count = int(match.group(1))
            else:
                contrib_count = 574
    except Exception as e:
        print(f"Warning: could not fetch contributions directly ({e}), defaulting to 574")
        contrib_count = 574

    return contrib_count, repos_count

def update_svg(contribs, repos):
    svg_path = "assets/telemetry-hud.svg"
    svg_content = generate_telemetry_hud(contribs, repos)
    
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    # Validate XML
    ET.parse(svg_path)
    print(f"Successfully generated & validated {svg_path} with Contributions: {contribs}+, Repos: {repos}")

if __name__ == "__main__":
    contribs, repos = fetch_stats()
    print(f"Fetched live stats for {USERNAME}: {contribs} all-time contributions, {repos} public repos.")
    update_svg(contribs, repos)
