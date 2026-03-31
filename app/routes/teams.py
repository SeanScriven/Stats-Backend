from fastapi import APIRouter
from app.database import get_db

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.get("/")
def get_teams():
    conn = get_db()
    rows = conn.execute("SELECT * FROM teams").fetchall()
    conn.close()
    teams = [dict(row) for row in rows]
    return teams

@router.get("/{team_id}")
def get_team(team_id: int):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM teams WHERE id = ?", (team_id,)
    ).fetchone()
    conn.close()
    if not row:
        return {"error": "Team not found"}
    return dict(row)
