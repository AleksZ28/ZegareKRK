import sqlite3
from database import DB_FILE
from fetch_data import fetch_departures
from utils import calculate_distance

def get_nearest_stops(lat, lon, radius):
    stops = []

    con = sqlite3.connect(DB_FILE)
    try:
        cur = con.cursor()

        for row in cur.execute("SELECT stop_id, name, lat, lon FROM stops"):
            distance = calculate_distance(lat, lon, row[2], row[3])
            if distance < radius:
                stops.append({
                    "stop_id": row[0],
                    "name": row[1],
                    "distance": distance,
                })

        stops.sort(key=lambda stop: stop["distance"])

    finally:
        con.close()
    return stops

def get_departures_from_stop(stop_id):
    departures = fetch_departures()

    departures_from_stop = departures.get(stop_id, [])

    return departures_from_stop