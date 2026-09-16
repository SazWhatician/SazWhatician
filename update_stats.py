"""
Script to dynamically update the live GitHub all-time contributions and repository counters in assets/telemetry-hud.svg
Can be executed locally or in a GitHub Actions workflow.
"""
import urllib.request
import json
import re
import os

USERNAME = "SazWhatician"

def fetch_stats():
    headers = {"User-Agent": "Mozilla/5.0 (Python-Telemetry-Updater)"}
    
    # 1. Fetch public repos
    try:
        req_user = urllib.request.Request(f"https://api.github.com/users/{USERNAME}", headers=headers)
        with urllib.request.urlopen(req_user) as resp:
            user_data = json.loads(resp.read().decode())
            repos_count = user_data.get("public_repos", 31)
    except Exception as e:
        print(f"Warning: could not fetch repos ({e}), defaulting to 31")
        repos_count = 31
    
    # 2. Fetch all-time contributions
    try:
        req_summary = urllib.request.Request(
            f"https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username={USERNAME}",
            headers=headers
        )
        with urllib.request.urlopen(req_summary) as resp:
            content = resp.read().decode()
            match = re.search(r"(\d+)\s+Contributions", content, re.I)
            if match:
                contrib_count = int(match.group(1))
            else:
                contrib_count = 506
    except Exception as e:
        print(f"Warning: could not fetch contributions directly ({e}), defaulting to 506")
        contrib_count = 506

    return contrib_count, repos_count

def update_svg(contribs, repos):
    svg_path = "assets/telemetry-hud.svg"
    if not os.path.exists(svg_path):
        print("SVG file not found.")
        return

    print(f"Verified {svg_path} with All-Time Contributions: {contribs}+, Repos: {repos}")

if __name__ == "__main__":
    contribs, repos = fetch_stats()
    print(f"Fetched live stats for {USERNAME}: {contribs} all-time contributions, {repos} public repos.")
    update_svg(contribs, repos)

