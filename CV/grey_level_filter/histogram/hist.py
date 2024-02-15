from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

image = Image.open("CV\grey_level_filter\datas\stars.jpg")
gray_image = image.convert('L')
gray_array = np.array(gray_image)
r = gray_array
MIN_GRAY_LEVEL = np.min(gray_array)
MAX_GRAY_LEVEL = np.max(gray_array)
HEIGHT = gray_array.shape[0]
WIDTH = gray_array.shape[1]


r = np.floor(np.log2(1 + r))

histogram, bins = np.histogram(r.flatten(), bins = 8, range = (0,7))

#plt.imshow(r, cmap='gray')

plt.plot(histogram, color='black')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.title('Grayscale Histogram')


plt.axis('on')  # 关闭坐标轴
plt.show()