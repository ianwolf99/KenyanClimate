import ee
import requests
import json
from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt

# Configure Google Earth Engine
ee.Authenticate()  # Authenticate with your Google account
ee.Initialize()

# Configure Elasticsearch connection
#es = Elasticsearch('localhost:9200')  # Replace with the appropriate Elasticsearch host and port


# Replace the placeholders with your Elasticsearch endpoint URL and credentials
endpoint = 'https://elastic-search.shiftechafrica.com:9200'
#username = 'your-username'
#password = 'your-password'

# Initialize the Elasticsearch client
try:
    es = Elasticsearch([endpoint])
except Exception as e:
    print(f'{e}')    

# Configure Logstash details
logstash_url = 'https://elastic-search.shiftechafrica.com:9200'  # Replace with your Logstash URL
headers = {'Content-type': 'application/json'}

# Define the region of interest (Kenya)
roi = ee.Geometry.Polygon(
    [[[33.501224, 5.419361],
      [41.899900, 5.419361],
      [41.899900, -4.646513],
      [33.501224, -4.646513],
      [33.501224, 5.419361]]])

# Define the years for data collection
start_year = 1983
end_year = 2023

# Define the desertification indicators
#indicators = ['ndvi', 'evi','ndwi','lst','rainfall','et']  # Modify or add more indicators as needed
indicators = ['NDVI', 'EVI', 'NDWI', 'LST', 'RAINFALL', 'ET', 'SAVI', 'ALBEDO', 'FPAR', 'SOIL_moisture', 'LAND_COVER', 'BURN_AREA', 'SNOW_COVER', 'ch', 'WATER_QUALITY']
# Fetch historical data from Google Earth Engine
#
#ee.ImageCollection("MODIS/061/MOD13A1") # Fetch historical data from Google Earth Engine
def fetch_historical_data():
    data = []
    try:
        for year in range(start_year, end_year + 1):
            image_collection = ee.ImageCollection('MODIS/006/MOD13A1') \
                .filterDate(str(year), str(year + 1)) \
                .filterBounds(roi)

            for indicator in indicators:
                band_name = indicator.upper()
                image_collection = image_collection.select(indicator)
                image = image_collection.mean().set('year', year).set('indicator', indicator)
                data.append(image)

    except ee.EEException as e:
        print(f"Error occurred while fetching data from Google Earth Engine: {e}")
        return []

    return data

def write_to_logstash(data):
    for image in data:
        properties = image.getInfo()
        year = properties['properties']['year']
        indicator = properties['properties']['indicator']
        image_data = image.reduceRegion(ee.Reducer.mean(), roi, 250).getInfo()
        value = image_data.get(indicator)  # Retrieve the value with a default value of None
        if value is not None:
            document = {
                'year': year,
                'indicator': indicator,
                'value': value
            }
            response = requests.post(logstash_url, data=json.dumps(document), headers=headers)
            if response.status_code != 200:
                print("Failed to write data to Logstash")
        else:
            print(f"No data available for indicator '{indicator}'")

# Fetch historical desertification data
historical_data = fetch_historical_data()

if historical_data:
    # Write desertification data to Logstash
    write_to_logstash(historical_data)
    print("Desertification data written to Logstash successfully.")

    # Continue with Elasticsearch and visualization steps...

    # Retrieve indexed data from Elasticsearch
    def retrieve_data():
        query = {
            'query': {
                'match_all': {}
            },
            'size': 5000  # Increase the size if you have more data
        }

        result = es.search(index='kenya_desertification', doc_type='desertification_data', body=query)
        hits = result['hits']['hits']
        data = [hit['_source'] for hit in hits]
        return data

    # Retrieve data from Elasticsearch
    data = retrieve_data()

    # Convert data to pandas DataFrame
    import pandas as pd
    df = pd.DataFrame(data)

    # Convert year to datetime format
    df['year'] = pd.to_datetime(df['year'], format='%Y')

    # Plotting multiple chart types and formats with Matplotlib
    plt.figure(figsize=(12, 8))

    # Line plot
    plt.subplot(2, 2, 1)
    for indicator in indicators:
        plt.plot(df[df['indicator'] == indicator]['year'], df[df['indicator'] == indicator]['value'], label=indicator)
    plt.title('Desertification Indicators - Line Plot')
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.legend()

    # Bar plot
    plt.subplot(2, 2, 2)
    plt.bar(df['year'], df['value'])
    plt.title('Desertification Indicators - Bar Plot')
    plt.xlabel('Year')
    plt.ylabel('Value')

    # Scatter plot
    plt.subplot(2, 2, 3)
    plt.scatter(df['year'], df['value'])
    plt.title('Desertification Indicators - Scatter Plot')
    plt.xlabel('Year')
    plt.ylabel('Value')

    # Box plot
    plt.subplot(2, 2, 4)
    plt.boxplot([df[df['indicator'] == indicator]['value'] for indicator in indicators], labels=indicators)
    plt.title('Desertification Indicators - Box Plot')
    plt.xlabel('Indicator')
    plt.ylabel('Value')

    plt.tight_layout()
    plt.show()

else:
    print("Failed to fetch historical desertification data.")
