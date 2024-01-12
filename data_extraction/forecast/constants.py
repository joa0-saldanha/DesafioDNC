import os

DB_HOSTNAME = os.environ.get('DB_HOSTNAME')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')

CONNECTION_STRING = f"host={DB_HOSTNAME} user={DB_USERNAME} password={DB_PASSWORD} dbname={DB_DATABASE}"


COORDINATES_URL = f"https://geocoding-api.open-meteo.com/v1/search?count=1&language=en&format=json&name="
FORECAST_URL = f"https://api.open-meteo.com/v1/forecast?hourly=temperature_2m,relative_humidity_2m,rain&daily=precipitation_hours&timezone=America%2FSao_Paulo&forecast_days=1&"