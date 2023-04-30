
import matplotlib.pyplot as plt
import numpy as np
from skimage import io, filters, measure, color

# Load satellite image of Kenya
image = io.imread('kenya_satellite_image.tif')

# Convert to grayscale and apply edge detection
gray = color.rgb2gray(image)
edges = filters.sobel(gray)

# Apply threshold to identify flooded areas
thresh = filters.threshold_otsu(gray)
binary = gray > thresh

# Label flooded areas
label_image = measure.label(binary)

# Create scatter plot of flooded areas
fig, ax = plt.subplots()
ax.set_title('Flooded Areas in Kenya')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
for region in measure.regionprops(label_image):
    # Skip small regions
    if region.area < 10:
        continue
    # Get coordinates of region centroid
    y, x = region.centroid
    # Add scatter plot point with color representing region size
    ax.scatter(x, y, c=region.area, cmap='Blues', alpha=0.5)
plt.show()

# Create bar chart of flooded areas by region
fig, ax = plt.subplots()
ax.set_title('Flooded Areas by Region in Kenya')
ax.set_xlabel('Region')
ax.set_ylabel('Area')
regions = []
areas = []
for region in measure.regionprops(label_image):
    # Skip small regions
    if region.area < 10:
        continue
    # Get region label and area
    regions.append(str(region.label))
    areas.append(region.area)
ax.bar(regions, areas)
plt.show()

# Create pie chart of flooded areas by region
fig, ax = plt.subplots()
ax.set_title('Flooded Areas by Region in Kenya')
regions = []
areas = []
for region in measure.regionprops(label_image):
    # Skip small regions
    if region.area < 10:
        continue
    # Get region label and area
    regions.append(str(region.label))
    areas.append(region.area)
ax.pie(areas, labels=regions, autopct='%1.1f%%')
plt.show()

