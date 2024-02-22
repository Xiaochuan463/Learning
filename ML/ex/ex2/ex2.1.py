import numpy as np
import matplotlib.pyplot as plt


class logisticRegression:
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
        self.data = np.array(self.data)
        self.x = np.ones((self.data.shape[0],1))
        self.y = np.array(self.data[:,-1]).reshape(-1,1)
        for i in range(0, self.data.shape[1]-1):
            self.x = np.column_stack((self.x,self.data[:,i]))
        self.theta = np.zeros((self.x.shape[1],1))

    def h(self):
        return 1 / (1 + np.exp(-1 * np.matmul(self.x,self.theta)))


    def Itergrate(self,step,alpha):
        for i in range(0,step):
            #j = (1 / self.x.shape[0])*(np.dot(self.y.T,np.log(self.h())) + np.dot((1-self.y).T,np.log(self.h())))
            g = (1 / self.x.shape[0]) * np.dot(self.x.T, (self.h() - self.y))
            self.theta -= alpha*g

    def plot(self):
        x = np.linspace(20,120,20)
        A = self.theta[1]
        B = self.theta[2]
        C = self.theta[0]
        m = -A/B
        b = -C/B
        class_0 = self.data[self.data[:, 2] == 0]
        class_1 = self.data[self.data[:, 2] == 1]
        y = m*x+b 
        plt.scatter(class_0[:, 0], class_0[:, 1], color='blue', label='Class 0')
        plt.scatter(class_1[:, 0], class_1[:, 1], color='red', label='Class 1')
        plt.plot(x,y,color = "green")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        #plt.legend()
        plt.show()

lR = logisticRegression(".\ML\ex2\data\ex2data1.txt")
#print(lR.h())

lR.Itergrate(10000000, 0.0003)
print(lR.theta)

lR.plot()
i = 0
i += 1
i += 1
i += 1
i += 1
