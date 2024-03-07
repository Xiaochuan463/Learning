from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

image = Image.open("CV\grey_level_filter\datas\stars.jpg")
gray_image = image.convert('L')
gray_array = np.array(gray_image)
MIN_GRAY_LEVEL = np.min(gray_array)
MAX_GRAY_LEVEL = np.max(gray_array)
HEIGHT = gray_array.shape[0]
WIDTH = gray_array.shape[1]

gray_array = MAX_GRAY_LEVEL - gray_array

plt.imshow(gray_array, cmap='gray')
plt.axis('off')  # 关闭坐标轴
plt.show()