import sqlite3
from database import DB_FILE

def get_stop(line, stop_type):
    line = line.split(",")
    stop_id = line[0]
    stop_name = line[2].replace('"', '')
    stop_lat = float(line[4])
    stop_lon = float(line[5])
    stop_type = stop_type


    data = (stop_id, stop_name, stop_lat, stop_lon, stop_type)

    return data

def update_stops():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    with open("stops_t.txt") as f:
        next(f)
        data = []
        for line in f:
            stop = get_stop(line, "tram")
            data.append(stop)

        cur.executemany("INSERT OR REPLACE INTO stops (stop_id, name, lat, lon, type) VALUES (?, ?, ?, ?, ?)", data)

    with open("stops_a.txt") as f:
        next(f)
        data = []
        for line in f:
            stop = get_stop(line, "bus")
            data.append(stop)

        cur.executemany("INSERT OR REPLACE INTO stops (stop_id, name, lat, lon, type) VALUES (?, ?, ?, ?, ?)", data)

    with open("stops_m.txt") as f:
        next(f)
        data = []
        for line in f:
            stop = get_stop(line, "mobilis")
            data.append(stop)

        cur.executemany("INSERT OR REPLACE INTO stops (stop_id, name, lat, lon, type) VALUES (?, ?, ?, ?, ?)", data)

    con.commit()
    con.close()