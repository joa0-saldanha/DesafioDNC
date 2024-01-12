import psycopg2 as psy
from requests import get

import constants as cons

def insert_city(city_name: str):
    """
        Inserts information about a city into the database.

        Parameters:
            city_name (str): The name of the city for which information will be inserted.

        Returns:
            str: Message indicating whether the insertion was successful or if the city was not found.
    """
    city_info = get_city_infos(city_name)

    print(f"Inserting {city_name} DATA!")

    if city_info['infos'] != 'Not Found':
        try:
            with psy.connect(cons.CONNECTION_STRING) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO public.city
                        (id, name, country_code, latitude, longitude)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        city_info['infos']['id'],
                        city_info['infos']['name'],
                        city_info['infos']['country_code'],
                        city_info['infos']['latitude'],
                        city_info['infos']['longitude']
                    ))
                connection.commit()
            
            return f"{city_info['infos']['name']} added successfully!"
        except Exception as e:
            raise e
    else:
        return f"City {city_name} NOT found!"

def insert_route(city_names: list):
    """
        Inserts information about a route into the database.

        Parameters:
            city_names (list): List containing the names of the origin and destination cities of the route.

        Returns:
            str: Message indicating whether the insertion of the route was successful.
    """
    origin_info = get_city_infos(city_names[0])
    destination_info = get_city_infos(city_names[1])

    try:
        with psy.connect(cons.CONNECTION_STRING) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO public.route
                    (origin, destination)
                    VALUES (%s, %s)
                """, (
                    origin_info['infos']['id'],
                    destination_info['infos']['id']
                ))
                connection.commit()
            
            return "Route added successfully!"
    except Exception as e:
        raise e

def get_city_infos(city_name: str):
    """
        Gets information about a city from a geolocation API.

        Parameters:
            city_name (str): The name of the city for which information will be obtained.

        Returns:
            dict: Dictionary containing information about the city.
    """
    print(f'Getting {city_name} Infos')
    url_call = cons.COORDINATES_URL + city_name

    try:
        infos = get(url_call).json()

        if 'results' in infos:
            city_info = {
                "infos": infos['results'][0]
            }
        else:
            city_info = {
                "infos": 'Not Found'
            }

        return city_info
    except Exception as e:
        raise e

def insert(request):
    """
        Acts as an entry point for inserting city or route information into the database.

        Parameters:
            request (dict): Dictionary containing information about the type of request and relevant data.

        Returns:
            - If the request is 'city', it returns a message indicating the success of the city insertion.
            - If the request is 'route', it returns a message indicating the success of the route insertion.
            - Otherwise, it returns "Invalid REQUEST!".
    """
    request = request.get_json(silent=True)

    if request['request'] == 'city':
        return insert_city(request['city'])
    elif request['request'] == 'route':
        return insert_route(request['citys'])
    else:
        return "Invalid REQUEST!"
