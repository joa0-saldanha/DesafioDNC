import os

FORECAST_URL = f"https://api.open-meteo.com/v1/forecast?hourly=temperature_2m,relative_humidity_2m,precipitation&timezone=America%2FSao_Paulo&forecast_days=1&"
BUCKET_NAME = "dnc-forecast-traffic-data"
API_KEY = os.environ.get('API_KEY')

CITYS_QUERY = """SELECT 
                    id, 
                    latitude as lat, 
                    longitude as lon
                FROM DNC.city"""

ROUTES_QUERY = """
        SELECT
            r.id AS route_id,
            o.latitude AS origin_lat,
            o.longitude AS origin_lon,
            d.latitude AS dest_lat,
            d.longitude AS dest_lon
        FROM DNC.route r
        LEFT JOIN DNC.city AS o 
            ON r.origin = o.id
        LEFT JOIN DNC.city AS d 
            ON r.destination = d.id;
    """