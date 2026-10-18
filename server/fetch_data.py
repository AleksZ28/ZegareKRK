import sqlite3
import time
import zipfile
from google.transit import gtfs_realtime_pb2
from database import DB_FILE
import httpx

GTFS_URLS = ["https://gtfs.ztp.krakow.pl/GTFS_KRK_T.zip", "https://gtfs.ztp.krakow.pl/GTFS_KRK_A.zip",
              "https://gtfs.ztp.krakow.pl/GTFS_KRK_M.zip"]

TRIP_URLS = ["https://gtfs.ztp.krakow.pl/TripUpdates_T.pb", "https://gtfs.ztp.krakow.pl/TripUpdates_A.pb",
             "https://gtfs.ztp.krakow.pl/TripUpdates_M.pb"]

cached_departures = {}
last_fetch_time = 0

def get_stop(line, stop_type):
    line = line.split(",")
    stop_id = line[0]
    stop_name = line[2].replace('"', '')
    stop_lat = float(line[4])
    stop_lon = float(line[5])
    stop_type = stop_type


    data = (stop_id, stop_name, stop_lat, stop_lon, stop_type)

    return data

def get_route(line):
    line = line.split(",")
    route_id = line[0].replace('"', '')
    route_name = line[2].replace('"', '')

    data = (route_id, route_name)
    return data

def get_trip(line, vehicle_type):
    line = line.split(",")

    if vehicle_type == "t":
        trip_id = line[0].replace('"', '')
        route_id = line[1].replace('"', '')
    else:
        trip_id = line[2].replace('"', '')
        route_id = line[0].replace('"', '')

    trip_headsign = line[3].replace('"', '')

    data = (trip_id, route_id, trip_headsign)
    return data

def get_trip_data(trip_id):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    try:
        res = cur.execute(
        """
            SELECT routes.name, trips.headsign
            FROM trips
            INNER JOIN routes ON trips.route_id = routes.route_id
            WHERE trip_id = ?
            """,
            (trip_id,)
        )
        row = res.fetchone()
    finally:
        con.close()

    if row is None:
        return None, None

    route_name, trip_headsign = row

    return route_name, trip_headsign

def update_gtfs_static():
    for url in GTFS_URLS:
        stop_type = url.split("_")[-1].split(".")[0].lower()
        r = httpx.get(url)
        r.raise_for_status()

        with open(f'gtfs_{stop_type}.zip', "wb") as f:
            f.write(r.content)

        with zipfile.ZipFile(f'gtfs_{stop_type}.zip', 'r') as zip_ref:
            zip_ref.extract('stops.txt', path=f'gtfs_{stop_type}')
            zip_ref.extract('routes.txt', path=f'gtfs_{stop_type}')
            zip_ref.extract('trips.txt', path=f'gtfs_{stop_type}')

    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    vehicle_types = ["t", "a", "m"]
    stops_data = []

    for vehicle in vehicle_types:
        with open(f"gtfs_{vehicle}/stops.txt") as f:
            next(f)
            for line in f:
                if vehicle == "t":
                    stop = get_stop(line, "tram")
                elif vehicle == "a":
                    stop = get_stop(line, "bus")
                elif vehicle == "m":
                    stop = get_stop(line, "mobilis")

                stops_data.append(stop)

    cur.executemany("INSERT OR REPLACE INTO stops (stop_id, name, lat, lon, type) VALUES (?, ?, ?, ?, ?)", stops_data)

    routes_data = []

    for vehicle in vehicle_types:
        with open(f"gtfs_{vehicle}/routes.txt") as f:
            next(f)
            for line in f:
                route = get_route(line)
                routes_data.append(route)

    cur.executemany("INSERT OR REPLACE INTO routes (route_id, name) VALUES (?, ?)", routes_data)

    trips_data = []

    for vehicle in vehicle_types:
        with open(f"gtfs_{vehicle}/trips.txt") as f:
            next(f)
            for line in f:
                route = get_trip(line, vehicle)
                trips_data.append(route)

    cur.executemany("INSERT OR REPLACE INTO trips (trip_id, route_id, headsign) VALUES (?, ?, ?)", trips_data)

    con.commit()
    con.close()

def fetch_departures():
    global cached_departures, last_fetch_time

    if time.time() - last_fetch_time < 20:
        return cached_departures

    departures = {}

    for url in TRIP_URLS:
        r = httpx.get(url)
        r.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(r.content)

        for entity in feed.entity:
            if entity.trip_update:
                trip_id = entity.trip_update.trip.trip_id
                line, headsign = get_trip_data(trip_id)

                if line is None:
                    continue

                for stop_time_update in entity.trip_update.stop_time_update:
                    stop_id = stop_time_update.stop_id

                    if stop_time_update.HasField("departure"):
                        departure = stop_time_update.departure.time
                    else:
                        departure = None

                    if departure is None:
                        continue

                    departures.setdefault(stop_id, []).append({
                        "time": departure,
                        "line": line,
                        "headsign": headsign,
                    })

    for stop_id in departures:
        departures[stop_id].sort(
            key=lambda departure: departure["time"]
        )

    cached_departures = departures.copy()
    last_fetch_time = time.time()

    return departures