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

C = 0.3


r = C * np.log2(1 + r)

plt.imshow(r, cmap='gray')
plt.axis('off')  # 关闭坐标轴

print(np.min(gray_array),"   ",np.max(gray_array))

plt.show()