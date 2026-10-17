import sqlite3

DB_FILE = "stops.db"

def init_db():
    con = sqlite3.connect(DB_FILE)

    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stops (
            stop_id TEXT,
            name TEXT,
            lat REAL,
            lon REAL,
            type TEXT,
            PRIMARY KEY (stop_id, type)
        )
    """)

    con.commit()
    con.close()

