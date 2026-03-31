from fastapi import APIRouter
from app.database import get_db

router = APIRouter(prefix="/leagues", tags=["Leagues"])

@router.get("/")
def get_leagues():
    conn = get_db()
    rows = conn.execute("SELECT * FROM leagues").fetchall()
    conn.close()
    leagues = [dict(row) for row in rows]
    return leagues

@router.get("/{league_id}")
def get_league(league_id: int):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM leagues WHERE id = ?", (league_id,)
    ).fetchone()
    conn.close()
    if not row:
        return {"error": "League not found"}
    return dict(row)
