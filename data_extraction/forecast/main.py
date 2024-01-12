from requests import get
import psycopg2 as psy
from datetime import datetime

import constants as cons

def get_citys():
    print("Getting CITIES!")
    
    try:
        with psy.connect(cons.CONNECTION_STRING) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, latitude, longitude FROM public.city")
                citys = [{'id': route[0], 'lat': route[1], 'lon': route[2]} for route in cursor.fetchall()]

        return get_forecast(citys)

    except Exception as e:
        raise e

def get_forecast(citys):
    print('Getting FORECAST!')

    for city in citys:
        url_call = cons.FORECAST_URL + f"latitude={city['lat']}&longitude={city['lon']}"
        
        try:
            forecast = get(url_call).json()

            city['forecast'] = [
                {
                    "date": datetime.strptime(forecast['hourly']['time'][i], '%Y-%m-%dT%H:%M').date(),
                    "hour": datetime.strptime(forecast['hourly']['time'][i], '%Y-%m-%dT%H:%M').time(),
                    "temperature": forecast['hourly']['temperature_2m'][i],
                    "humidity": forecast['hourly']['relative_humidity_2m'][i],
                    "precipitation": forecast['hourly']['precipitation'][i]
                } for i in range(0, 24)
            ]

        except Exception as e:
            raise e

    return insert_forecast(citys)

def insert_forecast(citys):
    print("Inserting FORECAST to the DATABASE!")

    try:
        with psy.connect(cons.CONNECTION_STRING) as connection:
            with connection.cursor() as cursor:
                for city in citys:
                    for forecast in city['forecast']:
                        cursor.execute("""
                            INSERT INTO public.forecast
                            (date, hour, city, temperature, humidity, precipitation)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """, (forecast['date'], forecast['hour'], city['id'], forecast['temperature'], forecast['humidity'], forecast['precipitation']))
                connection.commit()

        return 'Ok'

    except Exception as e:
        raise e

def forecast(request):
    if request == 'get_forecast':
        return get_citys()
    else:
        return 'Invalid request!'
