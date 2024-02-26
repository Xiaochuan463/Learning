"""
hand writed number identiy

datasets: MNIST
"""
import os
import gzip
import pickle
import numpy as np
from nerve_net import Cnn

TRAIN_IMAGE = "ML\\CNN\\datas\\train-images-idx3-ubyte.gz"
TRAIN_LABEL = "ML\\CNN\\datas\\train-labels-idx1-ubyte.gz"
TEST_IMAGE = "ML\\CNN\\datas\\t10k-images-idx3-ubyte.gz"
TEST_LABEL = "ML\\CNN\\datas\\t10k-labels-idx1-ubyte.gz"
STORE_FILE = "ML\\CNN\\datas\\layers.bin"

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

train_image = load_idx3_ubyte(TRAIN_IMAGE)
train_label = load_idx1_ubyte(TRAIN_LABEL)
test_image = load_idx3_ubyte(TEST_IMAGE)
test_label = load_idx1_ubyte(TEST_LABEL)

if os.path.exists(STORE_FILE):
    with open(STORE_FILE, 'rb') as f:
        layers = pickle.load(f)
else:
    layers = Cnn()
    layers.append("convolution", (3, 3))
    layers.append("convolution", (3, 3))
    layers.append("pool", (2, 2))
    layers.append("convolution", (3, 3))
    layers.append("convolution", (3, 3))
    layers.append("pool", (2, 2))
    layers.append("convolution", (3, 3))
    layers.append("convolution", (3, 3))
    layers.append("pool", (2, 2))
    layers.append("full",(9, 9))

layers.train(data=train_image, result=train_label, epochs=1000, rate=0.1)

with open(STORE_FILE, 'wb') as file:
    serialized_layers = pickle.dumps(layers)
    file.write(serialized_layers)