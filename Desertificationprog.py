
import pandas as pd
import matplotlib.pyplot as plt

# Load data from a CSV file
data = pd.read_csv('desertification_data.csv')

# Create a line chart to show changes in temperature over time
plt.plot(data['year'], data['temperature'])
plt.title('Temperature changes in desert areas over time')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.show()

# Create a scatter plot to show the relationship between rainfall and vegetation cover
plt.scatter(data['rainfall'], data['vegetation_cover'])
plt.title('Relationship between rainfall and vegetation cover in desert areas')
plt.xlabel('Rainfall (mm)')
plt.ylabel('Vegetation cover (%)')
plt.show()

# Create a heatmap to show the distribution of desert areas
plt.hist2d(data['longitude'], data['latitude'], bins=(50, 50), cmap=plt.cm.jet)
plt.title('Distribution of desert areas in Kenya')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.colorbar()
plt.show()
