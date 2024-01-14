import logging
from requests import get
import json
from google.cloud import bigquery, storage
from datetime import datetime
import pytz
from itertools import chain

import constants as cons

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_error(message, exception):
    """Registra mensagens de erro."""
    logger.error(message)
    logger.error(exception)

def get_data(task, filename):
    """Obtém dados de uma fonte específica."""
    logger.info(f"Obtendo dados para tarefa: {task}")
    QUERY = cons.CITYS_QUERY if task == "forecast" else cons.ROUTES_QUERY
    
    try:
        bq = bigquery.Client()
        return call_api([dict(row) for row in bq.query(QUERY).result()], task, filename)

    except Exception as e:
        log_error("Erro ao consultar o BigQuery", e)

def call_api(data, task, filename):
    """Chama a API e processa os dados."""
    if task == "forecast":
        for city in data:
            process_forecast(city)
        generate_json(list(chain.from_iterable([item['info'] for item in data])), task, filename)
    elif task == "traffic":
        for route in data:
            process_traffic(route)
        generate_json([route['info'] for route in data], task, filename)

def process_forecast(city):
    """Processa os dados de previsão do tempo para uma cidade."""
    url_call = cons.FORECAST_URL + f"latitude={city['lat']}&longitude={city['lon']}"
    try:
        forecast = get(url_call).json()
        city['info'] = generate_forecast_info(forecast, city)
    except Exception as e:
        log_error(f"Erro ao obter previsão para a cidade {city['id']}", e)

def generate_forecast_info(forecast, city):
    """Gera informações de previsão do tempo a partir dos dados brutos."""
    return [
        {
            "date": str(datetime.strptime(forecast['hourly']['time'][i], '%Y-%m-%dT%H:%M').date()),
            "hour": str(datetime.strptime(forecast['hourly']['time'][i], '%Y-%m-%dT%H:%M').time()),
            "temperature": forecast['hourly']['temperature_2m'][i],
            "humidity": forecast['hourly']['relative_humidity_2m'][i],
            "precipitation": forecast['hourly']['precipitation'][i],
            "id": f"C{city['id']}D{forecast['hourly']['time'][i]}H{forecast['hourly']['time'][i]}",
            "city": city['id'],
        } for i in range(0, 24)
    ]

def process_traffic(route):
    """Processa os dados de tráfego para uma rota."""
    url_call = "https://api.tomtom.com/routing/1/calculateRoute/{},{}:{},{}/json?key={}".format(
        route['origin_lat'], 
        route['origin_lon'],
        route['dest_lat'], 
        route['dest_lon'],
        cons.API_KEY
    )
    try:
        route['info'] = generate_traffic_info(get(url_call).json(), route)
    except Exception as e:
        log_error(f"Erro ao obter informações para a rota {route['route_id']}", e)

def generate_traffic_info(response, route):
    """Gera informações de tráfego a partir dos dados brutos."""
    summary = response['routes'][0]["summary"]
    summary['departureTime'] = summary['departureTime'][:-6]
    summary['arrivalTime'] = summary['arrivalTime'][:-6]
    summary['id'] = datetime.fromisoformat(summary['departureTime']).replace(tzinfo=pytz.utc).strftime('%y%m%d%H%M')
    summary['route'] = route['route_id']
    return summary

def generate_json(data, task, filename):
    """Gera um arquivo JSON localmente e o envia para o Cloud Storage."""
    logger.info(f"Gerando arquivo {task}.json")
    with open(f"/tmp/{filename}", 'w') as f:
        f.write('\n'.join(json.dumps(row) for row in data)) 
    
    return upload_json(filename, task)

def upload_json(filename, task):
    """Faz o upload do arquivo JSON para o Cloud Storage."""
    logger.info(f"Fazendo upload do arquivo {task}.json para o GCS")
    try:
        client = storage.Client()
        bucket = client.bucket(cons.BUCKET_NAME)
        blob = bucket.blob(f"{task}/{filename}")
        blob.upload_from_filename(f"/tmp/{filename}")
    except Exception as e:
        log_error(f"Erro ao fazer upload do arquivo {task}.json para o GCS", e)
    
    return f"{task}/{filename}"

def api_to_gcs(request):
    """Função principal chamada pelo Cloud Function."""
    request_json = request.get_json(silent=True)
    
    return get_data(request_json['task'], f"{request_json['task']}_{request_json['datetime']}.json")

