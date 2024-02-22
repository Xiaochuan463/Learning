import numpy as np

# 准备数据集（假设已经准备好了训练集和测试集）
X_train = np.random.randn(100, 1, 28, 28)  # 假设训练集包含100张28x28的灰度图像
y_train = np.random.randint(0, 10, size=(100,))  # 假设训练集的标签是随机生成的

X_test = np.random.randn(20, 1, 28, 28)  # 假设测试集包含20张28x28的灰度图像
y_test = np.random.randint(0, 10, size=(20,))  # 假设测试集的标签是随机生成的

# 定义卷积层、池化层和全连接层
class SimpleCNN:
    def __init__(self):
        # 卷积层参数
        self.conv1_filters = 16
        self.conv1_kernel_size = 3
        self.conv1_stride = 1
        self.conv1_padding = 1
        
        self.conv2_filters = 32
        self.conv2_kernel_size = 3
        self.conv2_stride = 1
        self.conv2_padding = 1
        
        # 池化层参数
        self.pool_kernel_size = 2
        self.pool_stride = 2
        
        # 全连接层参数
        self.fc1_units = 128
        self.fc2_units = 10  # 假设输出类别为10
        
        # 初始化模型参数
        self.conv1_weights = np.random.randn(self.conv1_filters, self.conv1_kernel_size, self.conv1_kernel_size)
        self.conv1_bias = np.zeros(self.conv1_filters)
        
        self.conv2_weights = np.random.randn(self.conv2_filters, self.conv2_kernel_size, self.conv2_kernel_size)
        self.conv2_bias = np.zeros(self.conv2_filters)
        
        self.fc1_weights = np.random.randn(32 * 7 * 7, self.fc1_units)
        self.fc1_bias = np.zeros(self.fc1_units)
        
        self.fc2_weights = np.random.randn(self.fc1_units, self.fc2_units)
        self.fc2_bias = np.zeros(self.fc2_units)
        
        # 激活函数
        self.relu = lambda x: np.maximum(x, 0)
        
    def convolve2d(self, input_data, filters, bias, stride, padding):
        # 实现卷积操作
            # 获取输入数据的尺寸和通道数
        _, input_channels, input_height, input_width = input_data.shape
    # 获取滤波器的尺寸和通道数
        _, filter_channels, filter_height, filter_width = filters.shape
    
    # 计算卷积后的输出尺寸
        output_height = (input_height - filter_height + 2 * padding) // stride + 1
        output_width = (input_width - filter_width + 2 * padding) // stride + 1
    
    # 初始化卷积后的输出结果
        conv_output = np.zeros((1, filters.shape[0], output_height, output_width))
    
    # 对输入数据进行零填充
        padded_input = np.pad(input_data, ((0, 0), (0, 0), (padding, padding), (padding, padding)), mode='constant')
    
    # 对输入数据进行卷积操作
        for i in range(output_height):
            for j in range(output_width):
            # 获取当前窗口的数据
                window = padded_input[:, :, i * stride:i * stride + filter_height, j * stride:j * stride + filter_width]
            # 执行卷积操作
                conv_output[:, :, i, j] = np.sum(window * filters, axis=(2, 3)) + bias
            
        return conv_output
        
    
    def max_pooling2d(self, input_data, pool_size, stride):
        # 实现最大池化操作
         _, input_channels, input_height, input_width = input_data.shape
        # 计算池化后的输出尺寸
        output_height = (input_height - pool_size) // stride + 1
        output_width = (input_width - pool_size) // stride + 1
        # 初始化池化后的输出结果
        pooled_output = np.zeros((1, input_channels, output_height, output_width))
        # 执行最大池化操作
        for i in range(output_height):
            for j in range(output_width):
                 # 获取当前窗口的数据
                window = input_data[:, :, i * stride:i * stride + pool_size, j * stride:j * stride + pool_size]
            # 在通道维度上取每个窗口的最大值
                pooled_output[:, :, i, j] = np.max(window, axis=(2, 3))
        return pooled_output
    
    def forward(self, x):
        # 卷积层1
        conv1_output = self.convolve2d(x, self.conv1_weights, self.conv1_bias, self.conv1_stride, self.conv1_padding)
        conv1_output = self.relu(conv1_output)
        pooled1_output = self.max_pooling2d(conv1_output, self.pool_kernel_size, self.pool_stride)
        
        # 卷积层2
        conv2_output = self.convolve2d(pooled1_output, self.conv2_weights, self.conv2_bias, self.conv2_stride, self.conv2_padding)
        conv2_output = self.relu(conv2_output)
        pooled2_output = self.max_pooling2d(conv2_output, self.pool_kernel_size, self.pool_stride)
        
        # 展平
        flattened_output = pooled2_output.flatten()
        
        # 全连接层1
        fc1_output = np.dot(flattened_output, self.fc1_weights) + self.fc1_bias
        fc1_output = self.relu(fc1_output)
        
        # 全连接层2
        fc2_output = np.dot(fc1_output, self.fc2_weights) + self.fc2_bias
        
        return fc2_output

# 创建一个简单的CNN模型实例
model = SimpleCNN()

# 定义损失函数和优化器
def cross_entropy_loss(logits, labels):
    logits_exp = np.exp(logits - np.max(logits, axis=1, keepdims=True))
    logits_softmax = logits_exp / np.sum(logits_exp, axis=1, keepdims=True)
    loss = -np.mean(np.log(logits_softmax[np.arange(len(labels)), labels] + 1e-7))
    return loss

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

def update_parameters(model, lr):
    pass  # 可以使用梯度下降等优化算法来更新参数

# 定义训练函数
def train(model, X_train, y_train, num_epochs, lr):
    for epoch in range(num_epochs):
        total_loss = 0.0
        for i in range(len(X_train)):
            # 前向传播
            logits = model.forward(X_train[i])
            # 计算损失
            loss = cross_entropy_loss(logits, y_train[i])
            total_loss += loss
            # 反向传播并更新参数
            # 这里省略了反向传播和参数更新的代码，
