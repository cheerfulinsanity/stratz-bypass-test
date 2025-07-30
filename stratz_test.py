import requests
import os

# 🔐 Secure token + target Steam32 ID
TOKEN = os.getenv("TOKEN")
STEAM_ID = int(os.getenv("STEAM_ID", "84228471"))

QUERY = """
query GetMatch($steamId: Long!) {
  player(steamAccountId: $steamId) {
    matches(request: {take: 1}) {
      id
      didWin
      durationSeconds
      players {
        steamAccountId
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
        print(f"✅ Match ID: {match['id']} — Duration: {match['durationSeconds']}s — Win: {match['didWin']}")
        for p in match["players"]:
            print(f"🧙 {p['hero']['name']}: {p['kills']}/{p['deaths']}/{p['assists']}")
    except Exception:
        print("❌ Error:", res.text)

if __name__ == "__main__":
    fetch_latest_match(STEAM_ID)
