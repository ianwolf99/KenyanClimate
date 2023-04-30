
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, filters, measure

# Load the satellite image of Kenya
kenya_img = io.imread('kenya_satellite_image.jpg')

# Convert the image to grayscale
kenya_gray = color.rgb2gray(kenya_img)

# Detect edges using the Canny filter
edges = filters.sobel(kenya_gray)

# Use the edges to segment the image and find the flooded areas
flooded_areas = measure.label(edges < 0.05)

# Display the original image and the flooded areas
fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 5))
ax0.imshow(kenya_img)
ax0.set_title('Original Image')
ax1.imshow(flooded_areas, cmap='Blues')
ax1.set_title('Flooded Areas')

# Create a histogram of the flooded area sizes
area_sizes = [r.area for r in measure.regionprops(flooded_areas)]
plt.figure(figsize=(8, 6))
plt.hist(area_sizes, bins=50)
plt.title('Flooded Area Sizes')
plt.xlabel('Area (pixels)')
plt.ylabel('Count')

# Create a scatter plot of the flooded area sizes
x = np.arange(len(area_sizes))
plt.figure(figsize=(8, 6))
plt.scatter(x, area_sizes, c=area_sizes, cmap='Blues')
plt.title('Flooded Area Sizes')
plt.xlabel('Region')
plt.ylabel('Area (pixels)')

# Create a bar chart of the flooded area sizes
labels = ['Region {}'.format(i+1) for i in range(len(area_sizes))]
plt.figure(figsize=(8, 6))
plt.bar(labels, area_sizes, color=plt.cm.Blues(area_sizes/np.max(area_sizes)))
plt.title('Flooded Area Sizes')
plt.xlabel('Region')
plt.ylabel('Area (pixels)')

plt.show()
