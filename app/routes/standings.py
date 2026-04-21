from fastapi import APIRouter
from app.database import get_db

router = APIRouter(prefix="/standings", tags=["Standings"])


@router.get("/")
def get_standings(league_id: int | None = None, season: int | None = None):
    conn = get_db()

    query = "SELECT * FROM standings WHERE 1=1"
    params = []

    if league_id:
        query += " AND league_id = ?"
        params.append(league_id)

    if season:
        query += " AND season = ?"
        params.append(season)

    query += " ORDER BY position ASC"

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]