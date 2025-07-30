import requests
import os

TOKEN = os.getenv("TOKEN")
STEAM_ID = int(os.getenv("STEAM_ID", "84228471"))

QUERY = """
query GetMatch($steamId: Long!) {
  player(steamAccountId: $steamId) {
    matches(request: {take: 1}) {
      id
      durationSeconds
      startDateTime
      playerSlot(steamAccountId: $steamId) {
        hero { name }
        kills
        deaths
        assists
        matchResult
      }
    }
  }
}
"""

def fetch_latest_match(steam_id):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "STRATZ_API"
    }
    payload = {
        "query": QUERY,
        "variables": { "steamId": steam_id }
    }

    res = requests.post("https://api.stratz.com/graphql", headers=headers, json=payload)
    try:
        data = res.json()
        match = data["data"]["player"]["matches"][0]
        player = match["playerSlot"]
        result = player["matchResult"]
        win_str = "🏆 Win" if result == "Win" else "💀 Loss" if result == "Loss" else "❓ Unknown"
        print(f"✅ Match ID: {match['id']} — Duration: {match['durationSeconds']}s")
        print(f"🧙 {player['hero']['name']}: {player['kills']}/{player['deaths']}/{player['assists']} — {win_str}")
    except Exception:
        print("❌ Error:", res.text)

if __name__ == "__main__":
    fetch_latest_match(STEAM_ID)
