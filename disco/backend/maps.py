from datetime import datetime
import geopy.distance
import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two latitude/longitude points on Earth using the Haversine formula.

    Parameters:
        lat1, lon1: Latitude and longitude of the first point in decimal degrees.
        lat2, lon2: Latitude and longitude of the second point in decimal degrees.

    Returns:
        Distance in kilometers (float).
    """
    # Earth's radius in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Calculate the differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Apply the Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance
    distance = R * c
    return distance


def get_distance_and_duration(
    source_latitude,
    source_longitude,
    destination_latitude,
    destination_longitude,
    retry_count=0,
):
    distance_matrix = haversine_distance(
        source_latitude,
        source_longitude,
        destination_latitude,
        destination_longitude,
    )

    if distance_matrix:
        return distance_matrix
    elif retry_count < 3:
        retry_count += 1
        return get_distance_and_duration(
            source_latitude,
            source_longitude,
            destination_latitude,
            destination_longitude,
            retry_count,
        )
    else:
        raise ValueError(extra_information=distance_matrix)


def get_address(latitude, longitude):
    geocode_result = gmaps.reverse_geocode((latitude, longitude))
    if geocode_result:
        return geocode_result[0]["formatted_address"]
    else:
        return "Unmarked Location"


def get_displacement(location1, location2):

    return geopy.distance.geodesic(
        location1, location2
    ).meters
