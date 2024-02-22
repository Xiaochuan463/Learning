"""
doc
"""
import pickle
import time
import os
import torch
import matplotlib.pyplot as plt
from PIL import ImageGrab
from PIL import Image
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
#数据存储的数组
data =[]
#状态
#0 学习  1 获取数据 2 应用
mode = 0
#MLP
ih = Weight(INPUT_NODES, HIDDEN_NODES)
hihii = Weight(HIDDEN_NODES, HIDDEN_NODES)
ho = Weight(HIDDEN_NODES, OUTPUT_NODES)

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
    gray_screen = convert_to_gray(screen)
    gray_array = np.array(gray_screen)[200 :, :]
    d = resize_image(gray_array, 50, 50)[10 :25, :].to(device)
    
    # 二值化
    d[d > 150] = 200
    d[d <= 150] = 20
    return d
#存入内存
def stor_data(datas,_r):
    """
    doc
    """
    r_in = _r.flatten().reshape(1, -1).to(device)
    y_in = []
    # 检查上箭头键是否被按下
    y_in.append(int(keyboard.is_pressed('up')))
    y_in.append(int(keyboard.is_pressed('left')))
    y_in.append(int(keyboard.is_pressed('down')))
    y_in.append(int(keyboard.is_pressed('right')))
    y_in = torch.tensor(y_in).reshape(1,-1)
    datas.append([r_in,y_in])
    if len(datas) > 2000:
        datas.pop(0)
#迭代
def iterate_once(x,y):
    #forward propagation
    ih.get_output(input_data=x)
    hihii.get_output(input_data=ih.output_data)
    ho.get_output(input_data=hihii.output_data)
    #backward propagation
    ho.get_derivative(next_weight= None, result= y, is_end= True)
    hihii.get_derivative(ho)
    ih.get_derivative(hihii)
    #update using gradient decent
    ho.update(STUDY_RATE, REGULARIZATION_RATE)
    hihii.update(STUDY_RATE, REGULARIZATION_RATE)
    ih.update(STUDY_RATE, REGULARIZATION_RATE)

if os.path.exists('auto_play\\data.pkl'):
    with open('auto_play\\data.pkl', 'rb') as f:
        data = pickle.load(f)
if os.path.exists('auto_play\\weights.pkl'):
    with open('auto_play\\weights.pkl', 'rb') as f:
        weights_dict = pickle.load(f)
        ih = weights_dict['ih']
        hihii = weights_dict['hihii']
        ho = weights_dict['ho']
        print(ho.weight)
        print(ih.weight)
        print(hihii.weight)

catch_time = time.time()
train_time = time.time()
start_time = time.time()

r = catch_data()

while True:

    if (mode == 0):
        #提取数据
        sub_arrays = [sample[0][0:1800].to(device) for sample in data]
        x = torch.cat(sub_arrays, axis=0)
        sub_arrays = [sample[1][0:1800].to(device) for sample in data]
        y = torch.cat(sub_arrays, axis=0)
        if time.time() - train_time > 300:
            with open('auto_play\\weight.pkl', 'wb') as f:
                weights_dict = {'ih': ih, 'hihii': hihii, 'ho': ho}
                pickle.dump(weights_dict, f)
                print("auto saved")
                train_time = time.time()
        while mode == 0:
            iterate_once(x,y)
            if keyboard.is_pressed('0'):
                mode = 0
                print("Now mode is study")
            if keyboard.is_pressed('1'):
                mode = 1
                print("Now mode is getData")
            if keyboard.is_pressed('2'):
                mode = 2
                print("Now mode is Apply")    
            if keyboard.is_pressed('p'):
                print("--------------------------------")
                print(ho.weight)
                print(ih.weight)
                print(hihii.weight)
   
    #每1/30秒处理捕获一次数据, 并更新图像
    if (mode == 2) and time.time() - start_time >= 1/30:
        start_time = time.time()
        r = catch_data()
        plt.imshow(r.cpu().numpy(), cmap='gray')
        plt.pause(0.001)  # 等待一小段时间以便更新图像
        # 清除当前图像以便更新
        plt.clf()

        hidden_layer = ih.get_output(input_data=r.flatten())
        h2 = hihii.get_output(input_data=ih.output_data)
        res = ho.get_output(input_data=hihii.output_data)
        print(res)
        if res[0,0] >= 0.5:
            pyautogui.keyDown('up')
        else:
            pyautogui.keyUp('up')

        if res[0,1] >= 0.5:
            pyautogui.keyDown('left')
        else:
            pyautogui.keyUp('left')

        if res[0,2] >= 0.5:
            pyautogui.keyDown('down')
        else:
            pyautogui.keyUp('down')

        if res[0,3] >= 0.5:
            pyautogui.keyDown('right')
        else:
            pyautogui.keyUp('right')
             
    #每两秒取一次数据
    if (mode == 1) and time.time() - catch_time >= 0.3:
        r = catch_data()
        catch_time = time.time()
        stor_data(data,r)       
    
       
    #切换模式
    if keyboard.is_pressed('0'):
        mode = 0
        print("Now mode is study")
    if keyboard.is_pressed('1'):
        mode = 1
        print("Now mode is getData")
    if keyboard.is_pressed('2'):
        mode = 2
        print("Now mode is Apply")
    #数据集数量
    if keyboard.is_pressed('d'):
        print("Now we have ",len(data)," datas")
    #存储data以及权重至硬盘
    if keyboard.is_pressed('q'):
        with open('auto_play\\data.pkl', 'wb') as f:
            pickle.dump(data, f)
        with open('auto_play\\weights.pkl', 'wb') as f:
            weights_dict = {'ih': ih, 'hihii': hihii, 'ho': ho}
            pickle.dump(weights_dict, f)
        break
print(ho.weight)
print(ih.weight)
print(hihii.weight)