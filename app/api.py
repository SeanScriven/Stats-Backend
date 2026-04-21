import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import leagues, teams, standings, games

app = FastAPI()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(leagues.router)
app.include_router(teams.router)
app.include_router(standings.router)
app.include_router(games.router)

@app.get("/")
def root():
    return {"message": "Rugby API is running"}