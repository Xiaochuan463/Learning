# learned

## ----根据example.py

* 目标：训练一个异或门神经网络
* 结构：
    输入：真值表4*2，每行是一组输入
    结果：真值表4*1，每行是一个结果

    输入层：2个节点--特征有两个
    隐藏层：4个节点--可自由选择
    输出层：1个节点--输出1 or 0

* 实现过程：
    初始化：
        确定两个计算过程对应的矩阵；

    计算前向传播：
        第一次计算：由输入算出第一次前向传播的结果
            具体细节由tks_com1.jpg给出
        第二次计算：由第一次前向传播得到第二次前向传播。
            细节同第一次

    计算反向传播：
        首先，计算出输出层的误差
        然后，根据下一层的误差算出当前层的误差
        最后，根据用误差算出的梯度进行梯度下降。
           
        细节见tks_com2.jpg

    输出：
        输出训练结果
        