import os

#DB_HOSTNAME = os.environ.get('DB_HOSTNAME')
#DB_USERNAME = os.environ.get('DB_USERNAME')
#DB_PASSWORD = os.environ.get('DB_PASSWORD')
#DB_DATABASE = os.environ.get('DB_DATABASE')

DB_HOSTNAME = "tuffi.db.elephantsql.com"
DB_USERNAME = "kvjxenby"
DB_PASSWORD = "h8DyBZWHpl6Iw_5XxjyKOKRds1ejIHOO"
DB_DATABASE = "kvjxenby"

CONNECTION_STRING = f"host={DB_HOSTNAME} user={DB_USERNAME} password={DB_PASSWORD} dbname={DB_DATABASE}"

COORDINATES_URL = f"https://geocoding-api.open-meteo.com/v1/search?count=1&language=en&format=json&name="