import os
import httpx
from dotenv import load_dotenv
import time

from database import get_db, upsert_leagues, upsert_teams

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("RUGBY_BASE_URL")
SEASON = 2024

# API-Sports requires the key in a specific header
headers = {
    "x-apisports-key": API_KEY,
    "x-rapidapi-host": "v1.rugby.api-sports.io"
}

def fetch_leagues():
    response = httpx.get(
        f"{BASE_URL}/leagues",
        headers={"x-apisports-key": API_KEY}
    )
    response.raise_for_status()
    return response.json()["response"]

def fetch_teams_by_league(league_id: int = None):
    response = httpx.get(
        f"{BASE_URL}/teams",
        headers={"x-apisports-key": API_KEY},
        params={"league": league_id, "season": SEASON}
    )
    response.raise_for_status()
    return response.json()["response"]

def main():
    conn = get_db()

    print("Fetching leagues from API...")
    leagues = fetch_leagues()
    print(f"Fetched {len(leagues)} leagues.")
    upsert_leagues(conn, leagues)

    print("Fetching teams for each league from API...")
    all_teams = []
    for league in leagues:
        league_id = league["id"]
        league_name = league["name"]
        print(f"\n--- League: {league_name} (id: {league_id}) ---")
        
        teams = fetch_teams_by_league(league_id)
        print(f"    Teams returned: {len(teams)}")
        all_teams.extend(teams)
        time.sleep(0.5)
    
    print(f"\nTotal teams collected: {len(all_teams)}")

    if all_teams:
        unique_teams = {team["id"]: team for team in all_teams}.values()
        upsert_teams(conn, list(unique_teams))
    else:
        print("No teams to insert — try changing SEASON.")

    conn.close()
if __name__ == "__main__":
    main()