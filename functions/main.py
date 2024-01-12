import psycopg2 as psy
from requests import get

import constants as cons

def insert_city(city_name: str):
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
    if request['request'] == 'city':
        return insert_city(request['city'])
    elif request['request'] == 'route':
        return insert_route(request['citys'])
    else:
        return "Invalid REQUEST!"
