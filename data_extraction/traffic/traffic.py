from requests import get
import psycopg2 as psy
import json

import constants as cons
    
def get_routes():

    print("Getting ROUTES information!")

    try:
        connection = psy.connect(cons.CONNECTION_STRING)
    except Exception as e:
        raise e

    cursor = connection.cursor()
    cursor.execute(f"""
                SELECT
                     r.id            AS route_id
                    ,o.latitude      AS origin_lat
                    ,o.longitude     AS origin_lon
                    ,d.latitude      AS dest_lat
                    ,d.longitude     AS dest_lon
                FROM route r
                LEFT JOIN city AS o 
                   ON r.origin = o.id
                LEFT JOIN city AS d 
                   ON r.destination = d.id;
                """)
    
    routes = [{
        'id': route[0],
        'origin': (route[1],route[2]),
        'destination': (route[3],route[4])
    } for route in cursor.fetchall()]

    cursor.close()
    connection.close()

    return get_traffic(routes)

def get_traffic(routes):

    print("Inserting TRAFFIC information into the DATABASE!")

    try:
        connection = psy.connect(cons.CONNECTION_STRING)
    except Exception as e:
        raise e
    
    for route in routes:

        url_call = f"https://api.tomtom.com/routing/1/calculateRoute/{route['origin'][0]},{route['origin'][1]}:{route['destination'][0]},{route['destination'][1]}/json?key={cons.API_KEY}"

        try:
            info = get(url_call).json()['routes'][0]["summary"]
        except Exception as e:
            raise e

        cursor = connection.cursor()

        cursor.execute(f"""
                INSERT INTO "public"."traffic"
                (route, distance_in_meters, departure_time, arrival_time, travel_time_in_seconds, traffic_delay_in_seconds, traffic_distance_in_meters)
                VALUES 
                ({route['id']}, '{info['lengthInMeters']}', '{info['departureTime']}', '{info['arrivalTime']}', {info['travelTimeInSeconds']}, {info['trafficDelayInSeconds']}, {info['trafficLengthInMeters']}) 
                """)
        
        connection.commit()
        cursor.close()

    connection.close()

    return 'Ok'

def traffic(request):

    if request == 'get_traffic':

        return get_routes()    
    else:

        return 'Invalid request!'





