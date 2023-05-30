import requests
from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt

# Configure Elasticsearch connection
es = Elasticsearch('localhost:9200')  # Replace with the appropriate Elasticsearch host and port

# Configure WeatherAPI details
API_KEY = 'YOUR_API_KEY'  # Replace with your WeatherAPI API key
API_URL = 'https://api.weatherapi.com/v1/climate/monthly.json'
LOCATION = 'Kenya'

# Fetch historical climatic data using the API
def fetch_historical_data():
    climate_data = []
    for year in range(1983, 2023):  # Replace with the desired range of years
        query_params = {
            'key': API_KEY,
            'q': LOCATION,
            'format': 'json',
            'year': year
        }

        response = requests.get(API_URL, params=query_params)
        if response.status_code == 200:
            year_data = response.json()
            climate_data.extend(year_data['month'])
        else:
            print(f"Failed to fetch historical data for year {year}")

    return climate_data

# Index climatic data into Elasticsearch
def index_climatic_data(data):
    for month in data:
        document = {
            'timestamp': month['index']['year'] + '-' + month['index']['month'],
            'temperature': month['avgtemp'],
            'precipitation': month['totalprecip'],
            'humidity': month['avghumidity'],
            'wind_speed': month['avgwindspeed']
        }
        es.index(index='kenya_climate', doc_type='climate_data', body=document)

# Fetch historical data
historical_data = fetch_historical_data()

if historical_data:
    # Index climatic data into Elasticsearch
    index_climatic_data(historical_data)
    print("Climatic data indexed successfully.")

    # Retrieve indexed data from Elasticsearch
    def retrieve_data():
        query = {
            'query': {
                'match_all': {}
            },
            'size': 5000  # Increase the size if you have more data
        }

        result = es.search(index='kenya_climate', doc_type='climate_data', body=query)
        hits = result['hits']['hits']
        data = [hit['_source'] for hit in hits]
        return data

    # Retrieve data from Elasticsearch
    data = retrieve_data()

    # Convert data to pandas DataFrame
    df = pd.DataFrame(data)

    # Convert timestamp to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Plotting temperature, precipitation, humidity, and wind speed
    plt.figure(figsize=(12, 8))

    # Temperature
    plt.subplot(2, 2, 1)
    plt.plot(df['timestamp'], df['temperature'])
    plt.title('Temperature')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')

    # Precipitation
    plt.subplot(2, 2, 2)
    plt.plot(df['timestamp'], df['precipitation'])
    plt.title('Precipitation')
    plt.xlabel('Year')
    plt.ylabel('Precipitation (mm)')

    # Humidity
    plt.subplot(2, 2, 3)
    plt.plot(df['timestamp'], df['humidity'])
    plt.title('Humidity')
    plt.xlabel('Year')
    plt.ylabel('Humidity (%)')

    # Wind Speed
    plt.subplot(2, 2, 4)
    plt.plot(df['timestamp'], df['wind_speed'])
    plt.title('Wind Speed')
    plt.xlabel('Year')
    plt.ylabel('Wind Speed (km/h)')

    plt.tight_layout()
    plt.show()

else:
    print("Failed to index climatic data.")
