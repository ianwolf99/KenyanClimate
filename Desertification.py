import ee
from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt

# Initialize Google Earth Engine
ee.Authenticate()
ee.Initialize()

# Configure Logstash details
LOGSTASH_HOST = 'localhost'
LOGSTASH_PORT = 5000

# Configure Elasticsearch connection
es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])

# Configure desertification indicators
INDICATORS = ['indicator_1', 'indicator_2', 'indicator_3']  # Replace with actual indicator names

# Fetch historical data using Google Earth Engine
def fetch_historical_data():
    # Define the region of interest (Kenya)
    roi = ee.Geometry.Rectangle([33.501, -4.669, 41.899, 5.202])

    data = []
    for indicator in INDICATORS:
        collection = ee.ImageCollection('YOUR_COLLECTION_ID').select(indicator)  # Replace with the actual collection ID
        series = collection.getRegion(roi, 40)  # Fetch data for 40 years

        # Process the series data
        headers = series.get(0).getInfo()
        rows = series.get(1).getInfo()

        for row in rows:
            year = row[0]
            values = row[4:]  # Adjust indices based on the structure of your data

            # Save the data point
            data.append({
                'year': year,
                'indicator': indicator,
                'values': values
            })

    return data

# Index data into Elasticsearch using Logstash
def index_data(data):
    for entry in data:
        document = {
            'year': entry['year'],
            'indicator': entry['indicator'],
            'values': entry['values']
        }

        es.index(index='desertification_data', doc_type='desert_data', body=document)
        # Send data to Logstash for indexing
        logstash_data = {
            'index': 'desertification_data',
            'type': 'desert_data',
            'body': document
        }
        requests.post(f"http://{LOGSTASH_HOST}:{LOGSTASH_PORT}/_bulk", json=logstash_data)

# Fetch historical data
historical_data = fetch_historical_data()

if historical_data:
    # Index data into Elasticsearch using Logstash
    index_data(historical_data)
    print("Data indexed successfully.")

    # Retrieve data from Elasticsearch
    def retrieve_data():
        query = {
            'query': {
                'match_all': {}
            },
            'size': 5000  # Increase the size if you have more data
        }

        result = es.search(index='desertification_data', doc_type='desert_data', body=query)
        hits = result['hits']['hits']
        data = [hit['_source'] for hit in hits]
        return data

    # Retrieve data from Elasticsearch
    data = retrieve_data()

    # Visualize the data using Matplotlib
    plt.figure(figsize=(12, 8))

    for indicator in INDICATORS:
        # Filter data for the current indicator
        filtered_data = [entry for entry in data if entry['indicator'] == indicator]
        years = [entry['year'] for entry in filtered_data]
        values = [entry['values'] for entry in filtered_data]

        # Plotting the data
        plt.plot(years, values, label=indicator)

    # Add chart labels and title
    plt.xlabel('Year')
    plt.ylabel('Indicator Value')
    plt.title('Desertification Indicators in Kenya')

    # Add legend
    plt.legend()

    # Save the chart as an image or display it
    # Uncomment the appropriate line based on your preference

    # Save the chart as an image
    # plt.savefig('desertification_chart.png')

    # Display the chart
    plt.show()

else:
    print("Failed to fetch historical data.")
