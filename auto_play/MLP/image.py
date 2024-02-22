"""
doc
"""
import time
import torch
import matplotlib.pyplot as plt
from PIL import ImageGrab
from PIL import Image, ImageOps
import numpy as np
import keyboard
from weight_gpu import Weight
import pyautogui


INPUT_NODES = 750
HIDDEN_NODES = 1000
OUTPUT_NODES = 4
STUDY_RATE = 1
REGULARIZATION_RATE = 0.0005
pyautogui.FAILSAFE = False

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 定义游戏场景的区域
region = (0, 0, 800, 600)  # 这里假设游戏窗口大小为 800x600，你需要根据实际情况调整

def resize_image(image_array, new_height, new_width):
    """
    doc
    """
    # 转换为 Pillow 图像对象
    image = Image.fromarray(image_array)
    
    # 调整图像大小
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    
    # 将调整大小后的图像转换回 NumPy 数组
    resized_image_array = np.array(resized_image)
    
    resized_image_array = torch.from_numpy(resized_image_array)

    return resized_image_array
# 定义捕获游戏场景的函数
def capture_screen(region):
    """
    doc
    """
    return ImageGrab.grab(bbox=region)
# 将彩色图像转换为灰度图像
def convert_to_gray(image):
    """
    doc
    """
    return image.convert('L')
#捕获数据
def catch_data():
    screen = capture_screen(region)
    d = convert_to_gray(screen)
    d = np.array(d)[250 :500, :]
    #d = np.array(ImageOps.equalize(d))
    d = np.array(d)
    # 二值化
    d[d > 150] = 200
    d[d <= 150] = 20
    return d



start_time = time.time()

r = catch_data()

while True:
    #每1/30秒处理捕获一次数据, 并更新图像
    if time.time() - start_time >= 1/30:
        start_time = time.time()
        r = catch_data()
        plt.imshow(r, cmap='gray')
        plt.pause(0.001)  # 等待一小段时间以便更新图像
        # 清除当前图像以便更新
        plt.clf()


             
    #存储data以及权重至硬盘
    if keyboard.is_pressed('q'):
        break
