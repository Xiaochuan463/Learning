import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Weight:
    def __init__(self, prev_nodes, next_nodes):
        self.shape = (prev_nodes, next_nodes)
        self.bias = torch.rand(1, next_nodes).to(device)  # 初始化为PyTorch张量并移至GPU
        self.weight = torch.rand(self.shape[0], self.shape[1]).to(device)  # 初始化为PyTorch张量并移至GPU
        self.input_data = None
        self.output_data = None
        self.der = None
        self.err = None

    def sigmoid(self, z):
        return 1 / (1 + torch.exp(-z))

    def get_output(self, input_data):
        if not isinstance(input_data, torch.Tensor):
            return None
        input_data = input_data.clone().detach().to(torch.float32).to(device)
        self.input_data = input_data.to(device)  # 转换为PyTorch张量并移至GPU
        self.output_data = torch.matmul(self.input_data, self.weight) + self.bias
        self.output_data = self.sigmoid(self.output_data)
        return self.output_data

    def get_derivative(self, next_weight, result=None, is_end=False):
        
        if is_end:
            result = result.to(device)
            self.err = self.output_data - result
        else:
            self.err = torch.matmul(next_weight.der, next_weight.weight.T)
        self.der = torch.mul(self.err, self.output_data * (1 - self.output_data))
        return self.der

    def update(self, rate, regularization_rate):
        grad = torch.matmul(self.input_data.T, self.der)
        if not (regularization_rate > 1 or regularization_rate < 0):
            grad += regularization_rate * self.weight
        self.weight -= grad * rate
        self.bias -= rate * torch.sum(self.der, axis=0)
