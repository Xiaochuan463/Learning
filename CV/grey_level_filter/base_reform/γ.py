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

C = 4
GAMA = 1.5

r = C * np.power(r, GAMA)

plt.imshow(r, cmap='gray')
plt.axis('off')  # 关闭坐标轴
plt.show()