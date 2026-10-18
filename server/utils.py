import math
from math import asin, sqrt, sin, cos

EARTH_RADIUS = 6371000

def calculate_distance(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    delta_lat = lat1_rad - lat2_rad
    delta_lon = lon1_rad - lon2_rad

    distance = 2 * EARTH_RADIUS * asin(sqrt(sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2))
    return distance