import os

DB_HOSTNAME = os.environ.get('DB_HOSTNAME')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

CONNECTION_STRING = f"host={DB_HOSTNAME} user={DB_USERNAME} password={DB_PASSWORD} dbname={DB_USERNAME}"


API_KEY = os.environ.get('API_KEY')