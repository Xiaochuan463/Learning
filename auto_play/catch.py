import torch
import time
import matplotlib.pyplot as plt
from PIL import ImageGrab
from PIL import Image
import numpy as np
import keyboard
import pyautogui
import pickle

def resize_image(image_array, new_height, new_width):
    # 转换为 Pillow 图像对象
    image = Image.fromarray(image_array)
    
    # 调整图像大小
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    
    # 将调整大小后的图像转换回 NumPy 数组
    resized_image_array = np.array(resized_image)
    
    return resized_image_array

# 将图像处理操作放在 GPU 上运行
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 定义捕获游戏场景的函数
def capture_screen(region):
    return ImageGrab.grab(bbox=region)

# 将彩色图像转换为灰度图像
def convert_to_gray(image):
    return image.convert('L')

# 定义游戏场景的区域
region = (0, 0, 800, 600)  # 这里假设游戏窗口大小为 800x600，你需要根据实际情况调整

# 控制捕获频率为每秒 30 次
capture_interval = 1 / 30  # 单位为秒

#数据存储的数组
data =[]

#状态
study = True

# 主循环
while True:
    catch_time = time.time()
    start_time = time.time()
    screen = capture_screen(region)
    gray_screen = convert_to_gray(screen)
    gray_array = np.array(gray_screen)[200 :, :]
    r = resize_image(gray_array, 100, 100)
    # 将图像转换为 PyTorch 张量并移动到 GPU 上
    r = torch.from_numpy(r).to(device)
    #二值化
    r = r[20 :60, :]
    r[r > 150] = 200
    r[r <= 150] = 20  
    if time.time() - catch_time >= 2:
        r_in = r.flatten()
        y_in = []
        # 检查上箭头键是否被按下
        y_in.append(int(keyboard.is_pressed('up')))
        y_in.append(int(keyboard.is_pressed('left')))
        y_in.append(int(keyboard.is_pressed('down')))
        y_in.append(int(keyboard.is_pressed('right')))
        r_in = torch.tensor(r_in)
        y_in = torch.tensor(y_in)
        data.append([r_in,y_in])
        if len(data) > 2000:
            data.pop(0)





















    # 显示灰度图像
    plt.imshow(r.cpu().numpy(), cmap='gray')
    plt.pause(0.001)  # 等待一小段时间以便更新图像
    # 清除当前图像以便更新
    plt.clf()
    # 计算捕获和显示所花费的时间
    elapsed_time = time.time() - start_time
    # 计算需要等待的时间，以保持捕获频率为每秒 30 次
    sleep_time = max(0, capture_interval - elapsed_time)
    # 等待一段时间以便下一次捕获
    time.sleep(sleep_time)

    if keyboard.is_pressed('q'):
        with open('auto_play\\data.pkl', 'wb') as f:
            pickle.dump(data, f)
        break
