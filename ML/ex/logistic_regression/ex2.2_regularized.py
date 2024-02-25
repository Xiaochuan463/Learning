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
        for i in range(2, 8):
            for j in range(0, i):
                self.x = np.column_stack((self.x,np.multiply(self.data[:,0]**(i-1-j),self.data[:,1]**j)))
        self.theta = np.ones((self.x.shape[1],1))

    def h(self):
        return 1 / (1 + np.exp(-1 * np.matmul(self.x,self.theta)))

    
    def Itergrate(self,step,alpha,la):
        for i in range(0,step):
            g = (1 / self.x.shape[0]) * np.dot(self.x.T, (self.h() - self.y))
            self.theta -= alpha*g
            self.theta[1:] = self.theta[1:] * (1 - alpha * (la/self.x.shape[0]))
            if(np.linalg.norm(g) < 0.002):
                print("Gradient is too small!")
                return
    
    
    def plot(self):

        x1 = np.linspace(-1, 1.5, 100)
        x2 = np.linspace(-1, 1.5, 100)
        x1, x2 = np.meshgrid(x1, x2)
        t = 0
        z = np.zeros_like(x1)
        for i in range(1, 8):
            for j in range(0, i):
                z += self.theta[t] * (x1**(i-1-j)) * (x2**j)
                t += 1
        z = 1 / (1 + np.exp(-z))  # 计算预测概率值
        z = (z > 0.5).astype(int)  # 将概率值转换为类别标签
        plt.contourf(x1, x2, z, alpha=0.3)  # 绘制决策边界
        class_0 = self.data[self.data[:, 2] == 0]
        class_1 = self.data[self.data[:, 2] == 1]
        plt.scatter(class_0[:, 0], class_0[:, 1], color='blue', label='Class 0')
        plt.scatter(class_1[:, 0], class_1[:, 1], color='red', label='Class 1')
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.legend()
        plt.show()

lR = logisticRegression(".\ML\ex\logistic_regression\data\ex2data2.txt")
#print(lR.h())

rate = 0.0003
punish = 156
step = 1000000

lR.Itergrate(step, alpha=rate, la=punish)
print(lR.theta)
print(1 - rate * (punish/lR.x.shape[0]))

lR.plot()
i = 0
i += 1
i += 1
i += 1
i += 1
