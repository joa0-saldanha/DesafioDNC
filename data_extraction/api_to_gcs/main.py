from requests import get
import json
from google.cloud import bigquery, storage
from datetime import datetime
import pytz

import constants as cons

def get_data(task: str , filename: str):
    print(f"Getting CITYS data!") if task == "forecast" else print(f"Getting ROUTES data!")

    QUERY = cons.CITYS_QUERY if task == "forecast" else cons.ROUTES_QUERY
    
    try:
        bq = bigquery.Client()

        return call_api([dict(row) for row in bq.query(QUERY).result()], task, filename)

    except Exception as e:
        raise e

def call_api(data: list, task: str , filename: str):

    if task == "forecast":

        print('Getting FORECAST information!')

        for city in data:
            url_call = cons.FORECAST_URL + f"latitude={city['lat']}&longitude={city['lon']}"
            
            try:
                forecast = get(url_call).json()

                city['info'] = [
                    {
                        "date": str(datetime.strptime(forecast['hourly']['time'][i], '%Y-%m-%dT%H:%M').date()),
                        "hour": str(datetime.strptime(forecast['hourly']['time'][i], '%Y-%m-%dT%H:%M').time()),
                        "temperature": forecast['hourly']['temperature_2m'][i],
                        "humidity": forecast['hourly']['relative_humidity_2m'][i],
                        "precipitation": forecast['hourly']['precipitation'][i]
                    } for i in range(0, 24)
                ]

                for forecast in city['info']:
                    forecast['id'] = f"C{city['id']}D{forecast['date']}H{forecast['hour']}"

            except Exception as e:
                raise e
            
        return generate_json(data, task, filename)
    
    else:

        print("Getting TRAFFIC information!")

        for route in data:
            url_call = "https://api.tomtom.com/routing/1/calculateRoute/{},{}:{},{}/json?key={}".format(
                route['origin_lat'], 
                route['origin_lon'],
                route['dest_lat'], 
                route['dest_lon'],
                cons.API_KEY
            )

            try:
                route['info'] = get(url_call).json()['routes'][0]["summary"]
                route['info']['id'] = datetime.fromisoformat(route['info']['departureTime'][:-6]).replace(tzinfo=pytz.utc).strftime('%y%m%d%H%M')
                route['info']['route'] = route['route_id']

            except Exception as e:
                print(f"Error getting info for route {route['route_id']}")
                print(e)
                pass

        return generate_json(data, task, filename)

def generate_json(data: list, task: str, filename: str):
    print(f"Generating {task} .json!")

    with open(f"/tmp/{filename}", 'w') as f:
        f.write('\n'.join(json.dumps(row['info']) for row in data))

    return upload_json(filename, task)

def upload_json(filename: str, task: str):
    print(f"Uploading {task} .json file to GCS!")

    try:
        client = storage.Client()
        bucket = client.bucket(cons.BUCKET_NAME)
        blob = bucket.blob(f"{task}/{filename}")
        blob.upload_from_filename(f"/tmp/{filename}")
    except Exception as e:
        raise e
    
    return f"{task}/{filename}"

def api_to_gcs(request):
    request_json = request.get_json(silent=True)

    return get_data(request_json['task'], f"{request_json['task']}_{request_json['datetime']}.json")
