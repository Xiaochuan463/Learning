import numpy as np
import matplotlib.pyplot as plt
import torch as tc
'''
fp = ".\ex1\data\ex1data1.txt"
with open(fp,'r') as files:
    lines = files.readlines()

data = []
for line in lines:
    line = line.split(',')
    row = []
    for ele in line:
        row.append(float(ele))
    data.append(row)
data = np.array(data)
x = np.array(data[:,0]).reshape(-1,1)
y = np.array(data[:,1]).reshape(-1,1)
one = np.ones((x.size,1))
x = np.column_stack((one,x))
'''

class linearRegression:
   
    def __init__(self,filename):
        self.data = []
        self.x = []
        self.y = []
        self.theta = []
        data = self.data
        if(isinstance(filename, str)):
            with open(filename,'r') as files:
                lines = files.readlines()
            for line in lines:
                line = line.split(',')
                row = []
                for ele in line:
                    row.append(float(ele))
                data.append(row)
        data = np.array(data)
        self.x = np.array(data[:,0]).reshape(-1,1)
        self.y = np.array(data[:,1]).reshape(-1,1)
        self.x = np.column_stack((np.ones((self.x.size,1)),self.x))
        self.theta = np.ones((self.x.shape[1],1))
        self.data = np.array(data)
        return 
    def print(self):
        print(self.x)
        print(self.y)
        print(self.theta)

    def iterate(self,step,alpha):
        for i in range(0,step):
            tmp = np.zeros((self.theta.shape[0],self.theta.shape[1]))
            for m in range(0,self.x.shape[1]):
                tmp += (self.x[m]@self.theta - self.y[m])*(self.x[m].reshape(-1,1))
            tmp *=  alpha / self.x.shape[1]
            self.theta -= tmp


    '''
    这是个GPU运算示例，在线性回归的最简单情况下，需要串行运算，所以GPU还是比较慢的。
    '''
    def mseIterateGpu(self, step, alpha):
        xt = tc.from_numpy(self.x).float().cuda()
        yt = tc.from_numpy(self.y).float().cuda()
        thetat = tc.from_numpy(self.theta).float().cuda()
        for i in range(0,step):
            mse = (-2/xt.shape[1])*tc.matmul(xt.T,(yt - tc.matmul(xt,thetat)))
            thetat -= alpha*mse 
        self.theta = thetat.cpu().numpy()
        self.x = xt.cpu().numpy()
        self.y = yt.cpu().numpy()

    def mseIterateCpu(self, step, alpha):
        xt = self.x
        yt = self.y
        thetat = self.theta
        for i in range(0,step):
            mse = (-2/xt.shape[1])*np.matmul(xt.T,(yt - np.matmul(xt,thetat)))
            thetat -= alpha*mse 

           
           
    def plot(self):
        x = np.array([-3,5,10,15,20,25])
        y = self.theta[0] + self.theta[1]*x 
        plt.scatter(self.data[:,0],self.data[:,1])
        plt.plot(x,y,color = "red")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        #plt.legend()
        plt.show()
    

lr = linearRegression(".\ML\ex1\data\ex1data1.txt")



lr.mseIterateCpu(900000,0.000003)
print(lr.theta)
lr.plot()



