'''
Try to get data from .idx3-ubyte and .idx1-ubyte
'''
import gzip
import numpy as np
import matplotlib.pyplot as plt

def load_idx3_ubyte(file_path):
    '''
    load images
    '''
    with gzip.open(file_path, 'rb') as f:
        # 读取文件头部信息
        magic_number = int.from_bytes(f.read(4), byteorder='big')
        num_images = int.from_bytes(f.read(4), byteorder='big')
        num_rows = int.from_bytes(f.read(4), byteorder='big')
        num_cols = int.from_bytes(f.read(4), byteorder='big')
        # 读取图像数据
        buf = f.read(num_images * num_rows * num_cols)
        data = np.frombuffer(buf, dtype=np.uint8)
        data = data.reshape(num_images, num_rows, num_cols)
        return data

def load_idx1_ubyte(file_path):
    '''
    load labels
    '''
    with gzip.open(file_path, 'rb') as f:
        # 读取文件头部信息
        magic_number = int.from_bytes(f.read(4), byteorder='big')
        num_items = int.from_bytes(f.read(4), byteorder='big')
        
        # 读取标签数据
        buf = f.read(num_items)
        labels = np.frombuffer(buf, dtype=np.uint8)
        
        return labels

def show_images(images, num_samples=5):
    '''
    show some images 
    '''
    fig, axes = plt.subplots(1, num_samples, figsize=(num_samples * 2, 2))
    for i in range(num_samples):
        axes[i].imshow(images[i], cmap='gray')
        axes[i].axis('on')
    plt.show()
FILE_PATH = 'ML\\CNN\\datas\\train-images-idx3-ubyte.gz'  # 替换为你的文件路径
images = load_idx3_ubyte(FILE_PATH)
print(images.shape)  # 输出图像数据的形状
# 示例用法：显示前5张图像
show_images(images, num_samples=10)