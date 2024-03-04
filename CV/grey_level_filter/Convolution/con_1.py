from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate2d

image = Image.open("CV\\grey_level_filter\\datas\\stars.jpg")
gray_image = image.convert('L')
gray_array = np.array(gray_image)
r = gray_array
MIN_GRAY_LEVEL = np.min(gray_array)
MAX_GRAY_LEVEL = np.max(gray_array)
HEIGHT = gray_array.shape[0]
WIDTH = gray_array.shape[1]

kernel = np.array([[1,1,1],
                   [1,1,1],
                   [1,1,1]])

def scale_grayscale(image, new_min, new_max):
    ''' 获取原始图像的最小值和最大值'''
    min_value = np.min(image)
    max_value = np.max(image)
    
    # 对图像进行线性缩放
    scaled_image = (image - min_value) * (new_max - new_min) / (max_value - min_value) + new_min
    
    return scaled_image

pad_height = max(((kernel.shape[0] - 1) // 2), 5)
pad_width = max(((kernel.shape[1] - 1) // 2), 5)
for i in range(1):
        
        padded_image = np.pad(r, ((pad_height, pad_height), (pad_width, pad_width)),
                               mode='edge')
        end = np.zeros(gray_array.shape)

        for j in range(pad_height, padded_image.shape[0] - pad_height):
                for k in range(pad_width, padded_image.shape[1] - pad_width):
                        neighborhood = padded_image[j - pad_height:j + pad_height + 1, k - pad_width:k + pad_width + 1]
                        end[j - pad_height, k - pad_width] = np.median(neighborhood)
        
        padded_image = np.pad(end, ((pad_height, pad_height), (pad_width, pad_width)),
                               mode='edge')
        for j in range(pad_height, padded_image.shape[0] - pad_height):
                for k in range(pad_width, padded_image.shape[1] - pad_width):
                        neighborhood = padded_image[j - pad_height:j + pad_height + 1, k - pad_width:k + pad_width + 1]
                        end[j - pad_height, k - pad_width] = np.max(neighborhood) - np.min(neighborhood)
        end = scale_grayscale(end, 0, 255)
        #end = correlate2d(padded_image, kernel,mode="valid") // 8
        #c = r // (1 + end)
        #bi = np.where(c > 0, 255, 0)
#end = scale_grayscale(end, 0, 1)
#end = np.round(end)
end = scale_grayscale(end, 0, 255)
plt.subplot(1, 2, 1)
plt.imshow(gray_array, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(end, cmap='gray')
plt.title('Equalized Image')
plt.axis('off')

plt.show()