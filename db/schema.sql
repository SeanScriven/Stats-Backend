CREATE TABLE IF NOT EXISTS leagues (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    logo TEXT,
    country_name TEXT,
    country_code TEXT,
    country_flag TEXT
);

CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY,
    name TEXT,
    logo TEXT,
    country_name TEXT,
    country_code TEXT,
    country_flag TEXT,
    league_id INTEGER,
    FOREIGN KEY (league_id) REFERENCES leagues(id)
);

CREATE TABLE IF NOT EXISTS standings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id INTEGER,
    season INTEGER,
    team_id INTEGER,
    team_name TEXT,
    team_logo TEXT,
    position INTEGER,
    stage TEXT,
    group_name TEXT,
    played INTEGER,
    won INTEGER,
    drawn INTEGER,
    lost INTEGER,
    goals_for INTEGER,
    goals_against INTEGER,
    points INTEGER,
    form TEXT,
    FOREIGN KEY (league_id) REFERENCES leagues(id),
    FOREIGN KEY (team_id) REFERENCES teams(id),
    UNIQUE(league_id, season, team_id)
);

CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    league_id INTEGER,
    season INTEGER,
    date TEXT,
    time TEXT,
    timestamp INTEGER,
    week TEXT,
    status_long TEXT,
    status_short TEXT,
    home_team_id INTEGER,
    home_team_name TEXT,
    home_team_logo TEXT,
    away_team_id INTEGER,
    away_team_name TEXT,
    away_team_logo TEXT,
    score_home INTEGER,
    score_away INTEGER,
    period_first_home INTEGER,
    period_first_away INTEGER,
    period_second_home INTEGER,
    period_second_away INTEGER,
    FOREIGN KEY (league_id) REFERENCES leagues(id),
    FOREIGN KEY (home_team_id) REFERENCES teams(id),
    FOREIGN KEY (away_team_id) REFERENCES teams(id)
);