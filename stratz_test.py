# stratz_test.py

import asyncio
import json
import requests
from playwright.async_api import async_playwright

STRATZ_GRAPHQL_URL = "https://api.stratz.com/graphql"
STEAM_ID = 84228471  # Your Steam32 ID

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

async def fetch_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Go to Stratz.com and wait a moment for scripts to load
        await page.goto("https://stratz.com")
        await page.wait_for_timeout(5000)

        # Try to extract the token from localStorage
        token = await page.evaluate("localStorage.getItem('token')")
        if not token:
            print("⚠️ Failed to retrieve token from localStorage.")
            return

        print(f"✅ Got token: {token[:16]}...")

        # Perform the GraphQL query
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
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

        await browser.close()

# Run the function
asyncio.run(fetch_data())

