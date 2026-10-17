import sqlite3

DB_FILE = "gtfs.db"

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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS routes (
            route_id TEXT PRIMARY KEY,
            name TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            trip_id TEXT PRIMARY KEY,
            route_id TEXT,
            headsign TEXT,
            FOREIGN KEY (route_id) REFERENCES routes (route_id)
        )
    """)

    con.commit()
    con.close()

