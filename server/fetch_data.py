import sqlite3
import zipfile

from database import DB_FILE
import httpx

GTFS_URLS = ["https://gtfs.ztp.krakow.pl/GTFS_KRK_T.zip", "https://gtfs.ztp.krakow.pl/GTFS_KRK_A.zip",
              "https://gtfs.ztp.krakow.pl/GTFS_KRK_M.zip"]

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
    for url in GTFS_URLS:
        stop_type = url.split("_")[-1].split(".")[0].lower()
        r = httpx.get(url)
        r.raise_for_status()

        with open(f'gtfs_{stop_type}.zip', "wb") as f:
            f.write(r.content)

        with zipfile.ZipFile(f'gtfs_{stop_type}.zip', 'r') as zip_ref:
            zip_ref.extract('stops.txt', path=f'gtfs_{stop_type}')

    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    with open(f"gtfs_t/stops.txt") as f:
        next(f)
        data = []
        for line in f:
            stop = get_stop(line, "tram")
            data.append(stop)

        cur.executemany("INSERT OR REPLACE INTO stops (stop_id, name, lat, lon, type) VALUES (?, ?, ?, ?, ?)", data)

    with open("gtfs_a/stops.txt") as f:
        next(f)
        data = []
        for line in f:
            stop = get_stop(line, "bus")
            data.append(stop)

        cur.executemany("INSERT OR REPLACE INTO stops (stop_id, name, lat, lon, type) VALUES (?, ?, ?, ?, ?)", data)

    with open("gtfs_m/stops.txt") as f:
        next(f)
        data = []
        for line in f:
            stop = get_stop(line, "mobilis")
            data.append(stop)

        cur.executemany("INSERT OR REPLACE INTO stops (stop_id, name, lat, lon, type) VALUES (?, ?, ?, ?, ?)", data)

    con.commit()
    con.close()