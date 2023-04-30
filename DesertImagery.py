
import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Open the satellite image
image_file = "path/to/satellite/image.tif"
with rasterio.open(image_file) as src:
    img = src.read()
    profile = src.profile
    nodata = src.nodata

# Preprocessing - set nodata values to NaN and scale the pixel values to [0, 1]
img = img.astype(np.float32)
img[img == nodata] = np.nan
img = img / np.nanmax(img)

# Calculate NDVI
red_band = img[3]  # assuming the red band is at index 3
nir_band = img[4]  # assuming the near-infrared band is at index 4
ndvi = (nir_band - red_band) / (nir_band + red_band)

# Plot the NDVI data
plt.imshow(ndvi, cmap="RdYlGn")
plt.colorbar()
plt.title("NDVI")
plt.show()
