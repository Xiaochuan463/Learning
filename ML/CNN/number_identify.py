'''
identify handwriten numbers

datasets: MNIST
'''
import gzip
import numpy as np
from convolution import Convolution
from convolution import Pooling
from convolution import Fullconnect

TRAIN_IMAGE = "ML\\CNN\\datas\\train-images-idx3-ubyte.gz"
TRAIN_LABEL = "ML\\CNN\\datas\\train-labels-idx1-ubyte.gz"
TEST_IMAGE = "ML\\CNN\\datas\\t10k-images-idx3-ubyte.gz"
TEST_LABEL = "ML\\CNN\\datas\\t10k-labels-idx1-ubyte.gz"
NULL = None

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

class Node:
    '''
    chain node of cnn. Like a struct in c
    Varibles:
        next: pointer to next node
        prev: pointer to previous node
        data: corrent layer
    '''
    def __init__(self) -> None:
        self.next = None
        self.prev = None
        self.data = None

class Cnn:
    '''
    Convolution neural network

    Variables:
        head: head pointer of cnn chain
    Functions:
        forward: foreward propagation
        backward: backward propagation
        train: a loop contains a foreward and a backward propagation and intergation
        append: add a node in the end

    '''
    def __init__(self) -> None:
        '''
        initialize the class
        new a enpty head
        '''
        self.head = Node()
        self.head.next = self.head
        self.head.prev = self.head

    def append(self, vtype, shape) -> None:
        '''
        add a node according to type
        
        Parameters:
            type(string): "pool", "convolution", "full"
        Returns:
            None
        '''
        tmp = Node()
        if "pool" == vtype:
            tmp.data = Pooling(shape)
        elif "convolution" == vtype:
            tmp.data = Convolution(shape)
        elif "full" == vtype:
            tmp.data = Fullconnect(shape)
        else:
            return
        tmp.prev = self.head.prev
        tmp.next = self.head
        self.head.prev.next = tmp
        self.head.prev = tmp

    def forward(self, data) -> np.ndarray:
        '''
        forward propagation of cnn.
        
        Parameters:
            data(np.ndarray): input data
        Returns:
            result(np.ndarray): output data
        '''
        tmp = self.head.next
        if tmp != self.head:
            tmp.data.forward(data)
            tmp = tmp.next
        while tmp is not None and tmp != self.head:
            tmp.data.forward(tmp.prev.data.output_data)
            tmp = tmp.next
        return self.head.prev.data.output_data

    def backward(self, result) -> None:
        '''
        forward propagation of cnn.
        
        Parameters:
            result(np.ndarray): real result
        Returns:
            None
        '''
        tmp = self.head.prev
        if tmp != self.head:
            tmp.data.get_error(result)
            tmp.data.backward()
            tmp = tmp.prev
        while tmp is not None and tmp != self.head:
            tmp.data.backward(tmp.next.data.prev_error)
            tmp = tmp.prev

    def train(self, data, result, epochs, rate) -> None:
        '''
        train data using forward and backward

        Parameters:
            data: input datas
            result: real result
            epochs: epochs to train
            rate: study rate
        '''
        for epoch in range(epochs):
            self.forward(data)
            self.backward(result=result)
            tmp = self.head.next
            while tmp is not None and tmp != self.head:
                tmp.data.intergate(rate)
                tmp = tmp.next
