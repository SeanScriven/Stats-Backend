from fastapi import APIRouter
from app.database import get_db

router = APIRouter(prefix="/games", tags=["Games"])


@router.get("/")
def get_games(
    league_id: int | None = None,
    season: int | None = None,
    team_id: int | None = None,
    status: str | None = None,
):
    conn = get_db()

    query = "SELECT * FROM games WHERE 1=1"
    params = []

    if league_id:
        query += " AND league_id = ?"
        params.append(league_id)

    if season:
        query += " AND season = ?"
        params.append(season)

    if team_id:
        query += " AND (home_team_id = ? OR away_team_id = ?)"
        params.extend([team_id, team_id])

    if status:
        query += " AND status_short = ?"
        params.append(status)

    query += " ORDER BY timestamp ASC"

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/{game_id}")
def get_game(game_id: int):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM games WHERE id = ?", (game_id,)
    ).fetchone()
    conn.close()
    if not row:
        return {"error": "Game not found"}
    return dict(row)