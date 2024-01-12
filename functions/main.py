import psycopg2 as psy
from requests import get

import constants as cons

def insert_city(city: str):

    city = get_city_infos(city)
    
    print(f"Inserting {city} DATA!")

    if city['infos'] != 'Not Found':
    
        try:
            connection = psy.connect(cons.CONNECTION_STRING)
            
        except Exception as e:
            raise e

        cursor = connection.cursor()
        cursor.execute(f"""
                    INSERT INTO "public"."city"
                    (id, name, country_code, latitude, longitude)
                    VALUES 
                    ({city['infos']['id']}, '{city['infos']['name']}', '{city['infos']['country_code']}', {city['infos']['latitude']}, {city['infos']['longitude']}) 
                    """)

        connection.commit()
        cursor.close()
        connection.close()

        return f"{city['infos']['name']} added succesfully!"
    
    else:
        
        return f"City NOT found!"

def insert_route(citys: list):
    
    origin = get_city_infos(citys[0])
    destination = get_city_infos(citys[1])

    try:
        connection = psy.connect(cons.CONNECTION_STRING)
    except Exception as e:
        raise e
    
    cursor = connection.cursor()

    cursor.execute(f"""
                INSERT INTO "public"."route"
                (origin, destination)
                VALUES
                {origin['infos']['id'], destination['infos']['id']}
                """)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return f"Route added succesfully!"

def get_city_infos(city: str):

    print(f'Getting {city} Infos')

    url_call = cons.COORDINATES_URL + city

    try:
        infos = get(url_call).json()

        if 'results' in infos:
            
            city = {
                "infos": infos['results'][0]
            }
        
        else:

            city = {
                "infos": 'Not Found'
            }

        return city

    except Exception as e:

        raise e
    
def insert(request):

    if request['request'] == 'city':

        return insert_city(request['city'])
    
    elif request['request'] == 'route':

        return insert_route(request['citys'])
    
    else:

        return "Invalid REQUEST!"
    