# stratz_test.py

import json
import requests

STRATZ_GRAPHQL_URL = "https://api.stratz.com/graphql"
STEAM_ID = 84228471  # Your Steam32 ID

# Your Stratz API token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiYWUyNTE3YTQtMTMwZS00MWFjLTkzMWYtMmFjNjZlMGVkMjMyIiwiU3RlYW1JZCI6Ijg0MjI4NDcxIiwibmJmIjoxNzUxODE0NjA0LCJleHAiOjE3ODMzNTA2MDQsImlhdCI6MTc1MTgxNDYwNCwiaXNzIjoiaHR0cHM6Ly9hcGkuc3RyYXR6LmNvbSJ9.fCe3q7P6VBgbPHqP-EZVjUVbU2Dk3aGufqTrjdQ3Ysw"

QUERY = """
query($steamAccountId: Long!) {
  player(steamAccountId: $steamAccountId) {
    matches(request: {take: 1}) {
      id
      startDateTime
      durationSeconds
      isRanked
      lobbyType
      players {
        steamAccountId
        kills
        deaths
        assists
        hero { name }
      }
    }
  }
}
"""

def fetch_data():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "STRATZ_API"
    }

    payload = {
        "query": QUERY,
        "variables": { "steamAccountId": STEAM_ID }
    }

    response = requests.post(STRATZ_GRAPHQL_URL, headers=headers, json=payload)

    try:
        data = response.json()
        match = data["data"]["player"]["matches"][0]
        print(f"🎯 Match ID: {match['id']}")
        for player in match["players"]:
            print(f"🧙 {player['hero']['name']} — {player['kills']}/{player['deaths']}/{player['assists']}")
    except Exception as e:
        print("❌ Error parsing response:", response.text)

# Run the function
if __name__ == "__main__":
    fetch_data()
