from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

image = Image.open("CV\\grey_level_filter\\datas\\stars.jpg")
gray_image = image.convert('L')
gray_array = np.array(gray_image)
r = gray_array
MIN_GRAY_LEVEL = np.min(gray_array)
MAX_GRAY_LEVEL = np.max(gray_array)
HEIGHT = gray_array.shape[0]
WIDTH = gray_array.shape[1]


#r = np.floor(np.log2(1 + r))
r_end = r.astype(int)

histogram, bins = np.histogram(r.flatten(), bins = 256, range = (0,255))




pdf = histogram / np.sum(histogram)
cdf = pdf.cumsum()
r_end = (cdf[r_end] * 255).astype(np.uint8)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(r, cmap='gray')
plt.title('Original Image')

plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(r_end, cmap='gray')
plt.title('Equalized Image')
plt.axis('off')

plt.show()









