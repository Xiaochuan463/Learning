import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)  # 打开摄像头

while(1):
    # 读取每一帧
    _, frame = cap.read()
    
    # 将BGR图像转换为HSV图像
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # 定义蓝色颜色的HSV范围
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    
    # 对HSV图像进行阈值处理，提取出蓝色区域
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    
    # 将原始图像和掩膜进行按位与操作，提取出蓝色物体
    res = cv.bitwise_and(frame, frame, mask=mask)
    
    # 显示原始图像、掩膜和提取出的蓝色物体
    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('res', res)
    
    # 检测按键，按下ESC键退出循环
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

# 关闭窗口并释放资源
cv.destroyAllWindows()
