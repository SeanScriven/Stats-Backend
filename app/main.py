import os
import httpx
from dotenv import load_dotenv
import time

from database import get_db, upsert_leagues, upsert_teams, upsert_standings, upsert_games

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("RUGBY_BASE_URL")
SEASON = int(os.getenv("SEASON"))

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

def fetch_standings_by_league(league_id: int = None):
    response = httpx.get(
        f"{BASE_URL}/standings",
        headers={"x-apisports-key": API_KEY},
        params={"league": league_id, "season": SEASON}
    )
    response.raise_for_status()
    raw = response.json()
    # response is a list of lists, flatten it
    nested = raw.get("response", [])
    return [item for sublist in nested for item in sublist]

def fetch_games_by_league(league_id: int = None):
    response = httpx.get(
        f"{BASE_URL}/games",
        headers={"x-apisports-key": API_KEY},
        params={"league": league_id, "season": SEASON}
    )
    response.raise_for_status()
    return response.json().get("response", [])

def main():
    conn = get_db()

    print("Fetching leagues from API...")
    leagues = fetch_leagues()
    print(f"Fetched {len(leagues)} leagues.")
    upsert_leagues(conn, leagues)

    print("Fetching teams, standings, and games for each league from API...")
    for league in leagues:
      league_id = league["id"]
      league_name = league["name"]
      print(f"  League: {league_name} (id: {league_id}) — ", end="")

      teams = fetch_teams_by_league(league_id)
      print(f"{len(teams)} teams found.")
      standings = fetch_standings_by_league(league_id)
      print(f"{len(standings)} standings found.")
      if teams:
        upsert_teams(conn, teams, league_id)
      if standings:
        upsert_standings(conn, standings, league_id, SEASON)
      games = fetch_games_by_league(league_id)
      print(f"{len(games)} games found.")
      if games:
        upsert_games(conn, games, league_id, SEASON)

      time.sleep(0.3)
    
    conn.close()
if __name__ == "__main__":
    main()