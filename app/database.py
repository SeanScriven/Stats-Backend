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

def upsert_teams(conn, teams: list):
    rows = [
        (
            team["id"],
            team["name"],
            team["logo"],
            team["country"]["name"],
            team["country"]["code"],
            team["country"]["flag"],
        )
        for team in teams
    ]

    conn.executemany("""
        INSERT INTO teams (id, name, logo, country_name, country_code, country_flag)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name=excluded.name,
            logo=excluded.logo,
            country_name=excluded.country_name,
            country_code=excluded.country_code,
            country_flag=excluded.country_flag
    """, rows)

    conn.commit()
    print(f"Upserted {len(rows)} teams into the database.")
