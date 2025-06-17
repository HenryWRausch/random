import sqlite3

DATABASE = 'database.db'

conn = sqlite3.connect(DATABASE)

queries = [
'''
CREATE TABLE IF NOT EXISTS Player_List (
    reference_id TEXT PRIMARY KEY,  -- unique Hockey-Reference identifier
    name TEXT NOT NULL,             -- full player name, may contain diacritics
    name_flat TEXT NOT NULL,        -- diacritics-stripped name for easier search
    position TEXT NOT NULL,         -- player position, as given
    first_year INTEGER NOT NULL,    -- debut year
    last_year INTEGER NOT NULL,     -- final year
    hof INTEGER NOT NULL CHECK (hof IN (0, 1))  -- Hall of Fame status: 1 = yes, 0 = no
);
'''
,
'''
CREATE TABLE goalie_overview (
    id TEXT PRIMARY KEY,
    season TEXT, 
    team TEXT,
    games_played INTEGER,
    games_started INTEGER,
    wins INTEGER,
    losses INTEGER,
    ties_plus_overtime_losses INTEGER,
    goals_against INTEGER,
    shots_against INTEGER,
    save_percentage REAL,
    goals_against_average REAL,
    shutouts INTEGER,
    time_on_ice_seconds INTEGER,
    quality_starts INTEGER,
    quality_start_percentage REAL,
    really_bad_starts INTEGER,
    goals_against_above_league_avg REAL,
    goals_saved_above_average REAL,
    adjusted_goals_against_average REAL,
    games_played_as_starter INTEGER,
    goals_scored INTEGER,
    assists INTEGER,
    points INTEGER,
    penalty_minutes INTEGER,
    awards TEXT -- store as JSON array or comma-separated string
);
''']



for query in queries:
    conn.execute(query)
conn.close()