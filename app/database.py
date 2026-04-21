import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "rugby.db"
SCHEMA_PATH = Path(__file__).parent.parent / "db" / "schema.sql"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn):
    schema = SCHEMA_PATH.read_text()
    conn.executescript(schema)
    conn.commit()
    print("Database initialised.")

def upsert_leagues(conn, leagues: list):
    rows = [
        (
            league["id"],
            league["name"],
            league["type"],
            league["logo"],
            league["country"]["name"],
            league["country"]["code"],
            league["country"]["flag"],
        )
        for league in leagues
    ]

    conn.executemany("""
        INSERT INTO leagues (id, name, type, logo, country_name, country_code, country_flag)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name=excluded.name,
            type=excluded.type,
            logo=excluded.logo,
            country_name=excluded.country_name,
            country_code=excluded.country_code,
            country_flag=excluded.country_flag
    """, rows)

    conn.commit()
    print(f"Upserted {len(rows)} leagues into the database.")

def upsert_teams(conn, teams: list, league_id: int):
    rows = [
        (
            team["id"],
            team["name"],
            team["logo"],
            team["country"]["name"],
            team["country"]["code"],
            team["country"]["flag"],
            league_id
        )
        for team in teams
    ]

    conn.executemany("""
        INSERT INTO teams (id, name, logo, country_name, country_code, country_flag, league_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name=excluded.name,
            logo=excluded.logo,
            country_name=excluded.country_name,
            country_code=excluded.country_code,
            country_flag=excluded.country_flag,
            league_id=excluded.league_id
    """, rows)

    conn.commit()
    print(f"Upserted {len(rows)} teams into the database.")

def upsert_standings(conn, standings: list, league_id: int, season: int):
    rows = [
        (
            league_id,
            season,
            standing["team"]["id"],
            standing["team"]["name"],
            standing["team"]["logo"],
            standing["position"],
            standing["stage"],
            standing["group"]["name"] if standing.get("group") else None,
            standing["games"]["played"],
            standing["games"]["win"]["total"],
            standing["games"]["draw"]["total"],
            standing["games"]["lose"]["total"],
            standing["goals"]["for"],
            standing["goals"]["against"],
            standing["points"],
            standing["form"],
        )
        for standing in standings
    ]

    conn.executemany("""
        INSERT INTO standings (
            league_id, season, team_id, team_name, team_logo,
            position, stage, group_name, played, won, drawn, lost,
            goals_for, goals_against, points, form
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(league_id, season, team_id) DO UPDATE SET
            team_name=excluded.team_name,
            team_logo=excluded.team_logo,
            position=excluded.position,
            stage=excluded.stage,
            group_name=excluded.group_name,
            played=excluded.played,
            won=excluded.won,
            drawn=excluded.drawn,
            lost=excluded.lost,
            goals_for=excluded.goals_for,
            goals_against=excluded.goals_against,
            points=excluded.points,
            form=excluded.form
    """, rows)

    conn.commit()
    print(f"Upserted {len(rows)} standings for league {league_id} season {season}.")

def upsert_games(conn, games: list, league_id: int, season: int):
    rows = [
        (
            game["id"],
            league_id,
            season,
            game["date"],
            game["time"],
            game["timestamp"],
            game["week"],
            game["status"]["long"],
            game["status"]["short"],
            game["teams"]["home"]["id"],
            game["teams"]["home"]["name"],
            game["teams"]["home"]["logo"],
            game["teams"]["away"]["id"],
            game["teams"]["away"]["name"],
            game["teams"]["away"]["logo"],
            game["scores"]["home"],
            game["scores"]["away"],
            game["periods"]["first"]["home"],
            game["periods"]["first"]["away"],
            game["periods"]["second"]["home"],
            game["periods"]["second"]["away"],
        )
        for game in games
    ]

    conn.executemany("""
        INSERT INTO games (
            id, league_id, season, date, time, timestamp, week,
            status_long, status_short,
            home_team_id, home_team_name, home_team_logo,
            away_team_id, away_team_name, away_team_logo,
            score_home, score_away,
            period_first_home, period_first_away,
            period_second_home, period_second_away
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            status_long=excluded.status_long,
            status_short=excluded.status_short,
            score_home=excluded.score_home,
            score_away=excluded.score_away,
            period_first_home=excluded.period_first_home,
            period_first_away=excluded.period_first_away,
            period_second_home=excluded.period_second_home,
            period_second_away=excluded.period_second_away
    """, rows)

    conn.commit()
    print(f"Upserted {len(rows)} games for league {league_id} season {season}.")