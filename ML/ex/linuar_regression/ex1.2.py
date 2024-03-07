import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def normalize_matrix_columns(matrix):
    # 计算每一列的均值和标准差
    mean_values = np.mean(matrix, axis=0)
    std_dev_values = np.std(matrix, axis=0)

    # 对每一列进行归一化
    normalized_matrix = (matrix - mean_values) / std_dev_values

    return normalized_matrix



class multiRegression:
    def __init__(self, filename):
        self.data = []
        if(isinstance(filename, str)):
            with open(filename,'r') as files:
                lines = files.readlines()
            for line in lines:
                line = line.split(',')
                row = []
                for ele in line:
                    row.append(float(ele))
                self.data.append(row)
            self.data = normalize_matrix_columns(np.array(self.data))
            self.x = np.ones((self.data.shape[0],1))
            self.y = np.array(self.data[:,-1]).reshape(-1,1)
            for i in range(0, self.data.shape[1]-1):
                self.x = np.column_stack((self.x,self.data[:,i]))
            self.theta = np.ones((self.x.shape[1],1))


    def mseIterateCpu(self, step, alpha):
        xt = self.x
        yt = self.y
        thetat = self.theta
        for i in range(0,step):
            mse = (-2/xt.shape[1])*np.matmul(xt.T,(yt - np.matmul(xt,thetat)))
            thetat -= alpha*mse 

    def plot(self):
        x = self.data[:,0]
        y = self.data[:,1]
        z = self.data[:,2]

        t = self.theta

        _x = np.linspace(-5,5,5)
        _y = np.linspace(-5,5,5)
        _x,_y = np.meshgrid(_x,_y)
        plane = t[0][0] + t[1][0]*_x + t[2][0]*_y

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(x, y, z, marker='o', label='Points')
        ax.plot_surface(_x, _y, plane, alpha=0.5,color='c', edgecolors='k', label='Plane')
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_zlabel('Z Coordinate')
        ax.set_title('Scatter Plot of 3D Points')
        ax.legend()

        # 显示图形
        plt.show()

mR = multiRegression(".\ML\ex\linuar_regression\data\ex1data2.txt")

mR.mseIterateCpu(10000,0.000003)
print(mR.theta)
mR.plot()

