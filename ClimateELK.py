import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Configure Elasticsearch connection
es = Elasticsearch('localhost:9200')  # Replace with the appropriate Elasticsearch host and port

# Configure WeatherAPI details
API_KEY = 'YOUR_API_KEY'  # Replace with your WeatherAPI API key
API_URL = 'https://api.weatherapi.com/v1/history.json'
LOCATION = 'Kenya'
START_DATE = '1993-01-01'  # Replace with your desired start date
END_DATE = '2022-12-31'  # Replace with your desired end date

# Fetch historical climatic data using the API
def fetch_historical_data():
    query_params = {
        'key': API_KEY,
        'q': LOCATION,
        'dt': START_DATE,
        'end_dt': END_DATE,
        'aqi': 'no',
        'tp': '24'  # 24-hourly interval
    }

    response = requests.get(API_URL, params=query_params)
    if response.status_code == 200:
        climate_data = response.json()
        return climate_data['forecast']['forecastday'][0]['hour']
    else:
        print("Failed to fetch historical data")
        return None

# Index climatic data into Elasticsearch
def index_climatic_data(data):
    bulk_data = []
    for entry in data:
        document = {
            '_index': 'kenya_climate',
            '_type': 'climate_data',
            '_source': {
                'timestamp': entry['time'],
                'temperature': entry['temp_c'],
                'precipitation': entry['precip_mm'],
                'humidity': entry['humidity'],
                'wind_speed': entry['wind_kph']
            }
        }
        bulk_data.append(document)
    
    bulk(es, bulk_data)

# Fetch historical data
historical_data = fetch_historical_data()

if historical_data:
    # Index climatic data into Elasticsearch
    index_climatic_data(historical_data)
    print("Climatic data indexed successfully.")
else:
    print("Failed to index climatic data.")

