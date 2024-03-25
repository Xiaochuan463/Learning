import numpy as np


WEIGHT = np.array([[2],[8],[3]])

x = np.random.random((3,500))
x = np.matmul(np.array([[800,0,0],[0,300,0],[0,0,500]]), x)
y = np.matmul(WEIGHT.T, x)
y_mean = y.mean()
new_y = np.where(y > y_mean, 1, 0)
print(new_y.shape)
print(x.shape)
result = np.vstack((x, new_y)).T
result = (np.floor(result + 0.5)).astype(int)
print(result)
#np.savetxt("knn_try.csv", result, delimiter=',', fmt="%d")
print("succeed!")