import requests
import os

# 🔐 Secure token + target Steam32 ID
TOKEN = os.getenv("TOKEN")
STEAM_ID = int(os.getenv("STEAM_ID", "84228471"))

# ✅ Validated against sdl.gql schema
QUERY = """
query GetMatch($steamId: Long!) {
  player(steamAccountId: $steamId) {
    matches(request: {take: 1}) {
      id
      durationSeconds
      startDateTime
      players {
        steamAccountId
        matchResult
        hero { name }
        kills
        deaths
        assists
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
        print(f"✅ Match ID: {match['id']} — Duration: {match['durationSeconds']}s")

        for p in match["players"]:
            result = p["matchResult"]
            win_str = "🏆 Win" if result == "Win" else "💀 Loss" if result == "Loss" else "❓ Unknown"
            print(f"🧙 {p['hero']['name']}: {p['kills']}/{p['deaths']}/{p['assists']} — {win_str}")
    except Exception:
        print("❌ Error:", res.text)

if __name__ == "__main__":
    fetch_latest_match(STEAM_ID)
