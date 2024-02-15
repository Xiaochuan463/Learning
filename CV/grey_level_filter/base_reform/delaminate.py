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


def delaminate(x):
    if x < 100:
        return 0
    elif x > 155:
       return 255 
    else:
        return 125

for h in range(HEIGHT):
    for w in range(WIDTH):
        r[h,w] = delaminate(r[h,w])

plt.imshow(r, cmap='gray')
plt.axis('off')  # 关闭坐标轴
plt.show()