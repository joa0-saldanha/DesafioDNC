from requests import get
import psycopg2 as psy
from datetime import datetime, timedelta, timezone
import json

import constants as cons

def get_routes():
    """
        Retrieves route information from the database and prepares the data for fetching traffic information.

        Returns:
            list: List of dictionaries representing routes, including origin and destination coordinates.
    """

    print("Getting ROUTES information!")

    try:
        with psy.connect(cons.CONNECTION_STRING) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        r.id AS route_id,
                        o.latitude AS origin_lat,
                        o.longitude AS origin_lon,
                        d.latitude AS dest_lat,
                        d.longitude AS dest_lon
                    FROM route r
                    LEFT JOIN city AS o 
                        ON r.origin = o.id
                    LEFT JOIN city AS d 
                        ON r.destination = d.id;
                """)
                routes = [{'id': route[0], 'origin': (route[1], route[2]), 'destination': (route[3], route[4])} for route in cursor.fetchall()]

        return get_traffic(routes)

    except Exception as e:
        raise e

def get_traffic(routes: list):
    """
        Retrieves traffic information for each route using the TomTom API.

        Parameters:
            routes (list): List of dictionaries representing routes.

        Returns:
            None
    """

    print("Getting TRAFFIC information!")

    for route in routes:
        url_call = f"https://api.tomtom.com/routing/1/calculateRoute/{route['origin'][0]},{route['origin'][1]}:{route['destination'][0]},{route['destination'][1]}/json?key={cons.API_KEY}"
        
        try:
            route['info'] = get(url_call).json()['routes'][0]["summary"]

        except Exception as e:
            raise e

    return insert_traffic(routes)

def insert_traffic(routes: list):
    """
        Inserts traffic information into the database for each route.

        Parameters:
            routes (list): List of dictionaries representing routes with traffic information.

        Returns:
            str: String indicating the success of the operation.
    """
    print("Inserting TRAFFIC information into the DATABASE!")

    try:
        with psy.connect(cons.CONNECTION_STRING) as connection:
            for route in routes:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO public.traffic
                        (route, distance_in_meters, departure_time, arrival_time, travel_time_in_seconds, traffic_delay_in_seconds, traffic_distance_in_meters)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        route['id'],
                        route['info']['lengthInMeters'],
                        datetime.strptime(route['info']['departureTime'], "%Y-%m-%dT%H:%M:%S%z").astimezone(timezone(timedelta(hours=-3))).strftime("%Y-%m-%d %H:%M:%S %z"),
                        datetime.strptime(route['info']['arrivalTime'], "%Y-%m-%dT%H:%M:%S%z").astimezone(timezone(timedelta(hours=-3))).strftime("%Y-%m-%d %H:%M:%S %z"),
                        route['info']['travelTimeInSeconds'],
                        route['info']['trafficDelayInSeconds'],
                        route['info']['trafficLengthInMeters']
                    ))
                connection.commit()

        return 'Ok'

    except Exception as e:
        raise e

def traffic(request):
    """
        Acts as an entry point for fetching traffic-related information. 
        Determines the type of request and triggers the appropriate actions.

        Parameters:
            request (str): Type of request, should be 'get_traffic'.

        Returns:
            - If the request is 'get_traffic', it returns the traffic information.
            - Otherwise, it returns 'Invalid request!'.
    """
    request_json = request.get_json(silent=True)

    task = request_json['task']

    if task == 'get_traffic':
        return get_routes()
    else:
        return 'Invalid request!'
