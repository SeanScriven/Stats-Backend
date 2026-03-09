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

if __name__ == "__main__":
    conn = get_db()
    init_db(conn)
    conn.close()
    print("Setup complete. You can now run main.py")