import requests

# 🔐 Your Stratz API token (keep private)
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiYWUyNTE3YTQtMTMwZS00MWFjLTkzMWYtMmFjNjZlMGVkMjMyIiwiU3RlYW1JZCI6Ijg0MjI4NDcxIiwibmJmIjoxNzUxODE0NjA0LCJleHAiOjE3ODMzNTA2MDQsImlhdCI6MTc1MTgxNDYwNCwiaXNzIjoiaHR0cHM6Ly9hcGkuc3RyYXR6LmNvbSJ9.fCe3q7P6VBgbPHqP-EZVjUVbU2Dk3aGufqTrjdQ3Ysw"

# 🧙 Replace this with any Steam32 ID
STEAM_ID = 84228471

# 🔎 GraphQL query
QUERY = """
query GetMatch($steamId: Long!) {
  player(steamAccountId: $steamId) {
    matches(request: {take: 1}) {
      id
      didWin
      durationSeconds
      startDateTime
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
    url = "https://api.stratz.com/graphql"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "STRATZ_API"
    }
    payload = {
        "query": QUERY,
        "variables": { "steamId": steam_id }
    }

    response = requests.post(url, headers=headers, json=payload)
    
    try:
        data = response.json()
        match = data["data"]["player"]["matches"][0]
        print(f"✅ Match ID: {match['id']} — Duration: {match['durationSeconds']}s — Win: {match['didWin']}")
        for p in match["players"]:
            print(f"🧙 {p['hero']['name']}: {p['kills']}/{p['deaths']}/{p['assists']}")
    except Exception as e:
        print("❌ Failed to fetch or parse match:")
        print(response.text)
        raise

if __name__ == "__main__":
    fetch_latest_match(STEAM_ID)
