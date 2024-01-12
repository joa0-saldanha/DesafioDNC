from requests import post, get
import psycopg2
from datetime import datetime

import constants as cons

def check_datebase(city: str):

    if not isinstance(city, str):
        raise TypeError("O nome da cidade deve ser uma string")

    if city == "":
        raise ValueError("O nome da cidade não pode ser vazio")


    try:
        connection = psycopg2.connect(cons.CONNECTION_STRING)

    except Exception as e:
        raise e

    cursor = connection.cursor()
    cursor.execute(f"""
                SELECT 
                   id,
                   latitude,
                   longitude
                FROM "public"."city" 
                WHERE LOWER(name) = LOWER('{city}') """)
    
    city_info = cursor.fetchall()

    cursor.close()
    connection.close()

    id, lat, lon = city_info[0] if len(city_info) > 0 else get_coordinates(city)

    return get_forecast({
        "id": id,
        "lat": lat,
        "lon": lon
    }) if lat != 0 and lon != 0 else 'City Not Found'

    
def get_coordinates(city: str):

    print('Getting Coordinates')

    url_call = cons.COORDINATES_URL + city

    try:
        infos = get(url_call).json()

    except Exception as e:
        raise e
    
    if 'results' in infos:

        city_infos = infos['results'][0]

        try:
            connection = psycopg2.connect(cons.CONNECTION_STRING)
            
        except Exception as e:
            raise e

        cursor = connection.cursor()
        cursor.execute(f"""
                    INSERT INTO "public"."city"
                    (id, name, country_code, latitude, longitude)
                    VALUES 
                    ({city_infos['id']}, '{city_infos['name']}', '{city_infos['country_code']}', {city_infos['latitude']}, {city_infos['longitude']}) 
                    """)

        connection.commit()
        cursor.close()
        connection.close()

        return (city_infos['id'], city_infos['latitude'], city_infos['longitude'])
    
    else:

        return (0, 0, 0)
    
def get_forecast(coordinates: dict):

    print('Getting Forecast')

    url_call = cons.FORECAST_URL + f"latitude={coordinates['lat']}&longitude={coordinates['lon']}"

    try:
        forecast = get(url_call).json()

    except Exception as e:
        raise e

    forecasts = [
        {
            "id": datetime.strptime(forecast['hourly']['time'][i], "%Y-%m-%dT%H:%M").strftime("%Y%m%d%H%M"),
            "date": datetime.strptime(forecast['hourly']['time'][i], '%Y-%m-%dT%H:%M').date(),
            "hour": datetime.strptime(forecast['hourly']['time'][i], '%Y-%m-%dT%H:%M').time(),
            "temperature": forecast['hourly']['temperature_2m'][i],
            "humidity": forecast['hourly']['relative_humidity_2m'][i],
            "precipitation": forecast['hourly']['rain'][i]
        } 
        for i in range(0,24)
    ]

    return insert_forecast(forecasts, coordinates['id'])

def insert_forecast(forecasts: list, city_id: int):

    print("Inserting Forecasts to the Database")

    try:
        connection = psycopg2.connect(cons.CONNECTION_STRING)
        
    except Exception as e:
        raise e

    cursor = connection.cursor()

    for forescast in forecasts:

        cursor.execute(f"""
                    INSERT INTO "public"."climate"
                    (date, hour, city, temperature, humidity, precipitation)
                    VALUES 
                    ('{forescast['date']}', '{forescast['hour']}', {city_id}, {forescast['temperature']}, {forescast['humidity']}, {forescast['precipitation']}) 
                    """)
        
        connection.commit()

    cursor.close()
    connection.close()