import numpy as np

class layer:
    def __init__(self, numberOfInput, numberOfNodes):
        n = numberOfNodes
        m = numberOfInput
        self.numberOfNodes = numberOfNodes
        self.numberOfInput = numberOfInput
        self.theta = np.zeros((n,m))
        self.bias = np.zeros((n,1))

    def computeOut(self,input):
        z = np.matmul(self.theta,input) + self.bias
        self.a = 1 / (1 + np.exp(-z))
        return self.a
    
    def computeError(self,nextError,nextTheta):
        if((not isinstance(nextTheta,np.ndarray)) or (not isinstance(nextError,np.ndarray))):
            return None
        self.error = np.matmul(nextTheta.T, nextError) * (self.a*(1-self.a))
        return self.error
    
    def update(self, rate, input):
        self.theta -= rate * np.matmul(self.error,input.T)
        self.bias -= rate * np.sum(self.error, axis=1, keepdims=True)