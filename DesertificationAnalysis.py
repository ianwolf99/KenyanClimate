

import numpy as np
import matplotlib.pyplot as plt
from skimage import io, filters, color, measure, morphology

# Load satellite imagery of Kenya
img = io.imread('kenya_satellite_image.tif')

# Convert the image to grayscale
gray = color.rgb2gray(img)

# Apply a median filter to reduce noise
gray = filters.median(gray, morphology.disk(5))

# Apply a threshold to segment the image into foreground and background
thresh = filters.threshold_otsu(gray)
binary = gray > thresh

# Remove small objects and holes in the foreground
binary = morphology.remove_small_objects(binary, min_size=1000)
binary = morphology.remove_small_holes(binary, area_threshold=1000)

# Label connected regions of the foreground
labels = measure.label(binary)

# Calculate the area of each labeled region
areas = np.array([r.area for r in measure.regionprops(labels)])

# Calculate the total area of the foreground
total_area = np.sum(areas)

# Calculate the percentage of the image covered by the foreground
coverage = total_area / (gray.shape[0] * gray.shape[1]) * 100

# Print the percentage of the image covered by the foreground
print(f"The percentage of the image covered by the foreground is: {coverage:.2f}%")

# Visualize the original image and the segmented foreground
fig, ax = plt.subplots(ncols=2, figsize=(10, 5))
ax[0].imshow(img)
ax[0].set_title('Original Image')
ax[1].imshow(binary, cmap='gray')
ax[1].set_title('Segmented Foreground')
plt.show()
