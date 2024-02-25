import numpy as np
import matplotlib.pyplot as plt
import torch as tc


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
   

    def mseIterate(self, step, alpha,la):
        xt = self.x
        yt = self.y
        theta = self.theta
        for i in range(0,step):
            mse = (-2/xt.shape[1])*np.matmul(xt.T,(yt - np.matmul(xt,theta)))
            self.theta = theta - alpha*mse
            self.theta[1:] = theta[1:] * (1 - alpha * (la / xt.shape[0]))
        

           
           
    def plot(self):
        x = np.array([-3,5,10,15,20,25])
        y = self.theta[0] + self.theta[1]*x 
        plt.scatter(self.data[:,0],self.data[:,1])
        plt.plot(x,y,color = "red")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        #plt.legend()
        plt.show()
    

lr = linearRegression(".\ML\ex\linuar_regression\data\ex1data1.txt")

rate = 0.003
punish = 5000
step = 1000000

lr.mseIterate(1000000,rate,punish)
print(1 - rate * (punish / lr.x.shape[0]))
print(lr.theta)
lr.plot()


