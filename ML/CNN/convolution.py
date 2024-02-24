'''
Using cpu
Classes:
    Layer -- abstract base class
    Convolution
    Pooling
    Fullconnect
'''
from abc import ABC, abstractmethod
import numpy as np
from scipy.signal import correlate2d

class Layer(ABC):
    '''
    Variables:
        err:        the error of last convolution
        prev_err:the error to be propagate
        input_data: the last input data
        output_data:the last output data
        layer_type: the type of this layer(base, convolution, pool, full)

    Functions:
        forward:            the forward propagation compute
        backward:           compute and backward propagate error
        intergate:          intergate the layer parameter if needed
    '''
    @abstractmethod
    def __init__(self) -> None:
        '''
        initialize variables:
            err, prev_err, input_data, output_data, layer_type
        '''
        super().__init__()
        self.err = None
        self.prev_err = None
        self.input_data = None
        self.output_data = None
        self.layer_type = "base"

    @abstractmethod
    def forward(self, input_data) -> np.ndarray:
        '''
        forward propagate input data. Both input and ouput will be stored

        Parameters:
            input_data(np.ndarray)
        Return:
            output_data(np.ndarray)
        '''
        return self.output_data

    @abstractmethod
    def backward(self, this_error) -> np.ndarray:
        '''
        compute previous error base on this error
        
        Parameters:
            this_error(np.ndarry): the error of this layer getting from next layer
                or computer based on result
        Returns:
            previous error
        '''
        return self.prev_err

    @abstractmethod
    def intergate(self, rate) -> None:
        '''
        intergrate according to corrent error

        Parameters:
            None
        Returns:
            None     
        '''

class Convolution(Layer):
    '''
    Variables:
        kernel:     convolution kernel
        shape:      the shape of kernel
        err:        the error of last convolution
        prev_err:the error to be propagate
        grad:       the graded of the kernel
        input_data: the last input data
        output_data:the last output data
        layer_type: the type of this layer(con, pool, full)

    Functions:
        forward:            the forward propagation compute
        backward:           compute and backward propagate error
        intergate:          intergate the layer parameter if needed
    '''
    def __init__(self, shape) -> None:
        '''
        initialize the convolution class.

        Parameters: 
            shape(tuple)
        Return: 
            None
        '''
        super().__init__()
        if not isinstance(shape, tuple):
            raise ValueError("Shape must be a turple!")
        self.kernel = np.random.rand(*shape)
        self.grad = None
        self.layer_type = "convolution"

    def forward(self, input_data) -> np.ndarray:
        '''
        Convolute input data. Both input and ouput will be stored

        Parameters:
            input_data(np.ndarray)
        Return:
            output_data(np.ndarray)
        '''
        self.input_data = input_data
        pad_height = max(self.kernel.shape[0] - 1, 0)
        pad_width = max(self.kernel.shape[1] - 1, 0)
        padded_image = np.pad(input_data, ((pad_height, pad_height),
            (pad_width, pad_width)), mode='constant', constant_values=0)
        self.output_data = correlate2d(padded_image, self.kernel,mode="valid")
        self.output_data = np.maximum(0, self.output_data)
        return self.output_data

    def backward(self, this_error) -> np.ndarray:
        '''
        get previous error from this error, both of them will be stored in this class
        
        Parameter:
            this_err(np.ndarray): error of conpute of this layer
        Returns:
            prev_err(np.ndarray): error of previous layer 
        '''
        if not isinstance(this_error, np.ndarray):
            raise ValueError("Not a ndarray")
        self.err = this_error
        flip_err = np.flip(self.err)
        self.prev_err = correlate2d(flip_err, self.kernel)
        return self.prev_err

    def intergate(self, rate) -> None:
        '''
        Compute grad based on error and input_data

        Parameter:
            None
        Returns:
            None
        '''
        pad_height = max(self.err.shape[0] - 1, 0)
        pad_width = max(self.err.shape[1] - 1, 0)
        padded = np.pad(self.input_data, ((pad_height, pad_height),
            (pad_width, pad_width)), mode='constant', constant_values=0)
        self.grad = correlate2d(padded, self.err)
        self.kernel -= rate * self.grad

class Pooling(Layer):
    '''
    Pooling layer

    Variables:
        err:        the error of last convolution
        prev_err:   the error to be propagate
        input_data: the last input data
        output_data:the last output data
        layer_type: the type of this layer(base, con, pool, full)
    
    Functions:
        forward:            the forward propagation compute
        backward:           compute and backward propagate error
    '''
    def __init__(self, pool_size) -> None:
        '''
        inilize Pooling layer
        '''
        super().__init__()
        self.layer_type = "pool"
        self.pool_size = pool_size

    def forward(self, input_data) -> np.ndarray:
        '''
        pool the array, both of input and output will be stored 

        Parameters:
            input_data
        Returns:
            ouput_data
        '''
        self.input_data = input_data
        height, width = input_data.shape
        pool_height, pool_width = self.pool_size
        pooled_height = height // pool_height
        pooled_width = width // pool_width
        pooled_feature_map = np.zeros((pooled_height, pooled_width))
        for i in range(pooled_height):
            for j in range(pooled_width):
                start_h = i * pool_height
                end_h = start_h + pool_height
                start_w = j * pool_width
                end_w = start_w + pool_width
                pooled_feature_map[i, j] = np.max(self.input_data[start_h:end_h, start_w:end_w])
        self.output_data = pooled_feature_map
        return pooled_feature_map

    def backward(self, this_error) -> np.ndarray:
        '''
        Propagate error to previous layer

        Parameter:
            err(np.ndarray): error from this layer
        Returns:
            prev_err(np.ndarray): error to previous layer
        '''
        self.err = this_error
        prev_error = np.zeros_like(self.input_data)
        pool_height, pool_width = self.pool_size
        for i in range(self.output_data.shape[0]):
            for j in range(self.output_data.shape[1]):
                start_h = i * pool_height
                end_h = start_h + pool_height
                start_w = j * pool_width
                end_w = start_w + pool_width
                max_index = np.unravel_index(np.argmax(self.input_data[start_h:end_h,
                                            start_w:end_w]), (pool_height, pool_width))
                prev_error[start_h:end_h, start_w:end_w][max_index] = this_error[i, j]
        self.prev_err = prev_error
        return self.prev_err

    def intergate(self, rate) -> None:
        '''
        pool layer do not need intergate
        '''
        return

class Fullconnect(Layer):
    '''
    Variables:
        err:        the error of last convolution
        prev_err:   the error to be propagate
        input_data: the last input data
        output_data:the last output data
        layer_type: the type of this layer(base, convolution, pool, full)
        weight:     the weight of nodes
        grad:       the grad of weights
        bias:       the bias of compute

    Functions:
        forward:            the forward propagation compute
        backward:           compute and backward propagate error
        intergate:          intergate the layer parameter if needed
    '''
    def __init__(self, shape) -> None:
        '''
        initialize the convolution class.

        Parameters: 
            shape(tuple)
        Return: 
            None
        '''
        super().__init__()
        self.layer_type = "full"
        self.weight = np.random.rand(*shape)
        self.bias = np.random.randn(shape[0], 1)
        self.grad = None

    def forward(self, input_data) -> np.ndarray:
        self.input_data = input_data
        self.output_data = np.matmul(self.input_data, self.weight) + self.bias
        self.output_data = 1 / (1 + np.exp(-1 * self.output_data))
        return self.output_data

    def backward(self, this_error = None) -> np.ndarray:
        '''
        get previous error from this error, both of them will be stored in this class
        
        Parameter:
            this_err(np.ndarray): error of conpute of this layer
        Returns:
            prev_err(np.ndarray): error of previous layer 
        '''
        der = self.output_data * (1 - self.output_data)
        self.grad = np.multiply(self.err, der)
        self.prev_err = np.matmul(self.grad, self.weight.T)
        return self.prev_err

    def get_error(self, result)-> np.ndarray:
        '''
        if this layer is the last layer, this function should be call to get initial error
        
        Parameters:
            output_data(np.ndarray): real result
        Returns:
            previous layer error
        '''
        self.err = self.output_data - result

    def intergate(self, rate) -> None:
        grad = self.input_data.T.dot(self.grad)
        self.weight -= grad * rate
        self.bias -= rate * np.sum(self.grad,axis=0)
