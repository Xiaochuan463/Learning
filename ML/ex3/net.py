#train a XOR gate.

import layer
import numpy as np

l1 = layer.layer(2,2)
l2 = layer.layer(2,2)
l3 = layer.layer(2,2)

x = [[0,0],
    [0,1],
    [1,0],
    [1,1]]
y = [[0],
     [1],
     [1],
     [0]]
x = np.array(x)
y = np.array(y)

o_to_i = l1.computeOut(x)
i_to_ii = l2.computeOut(l1.a)
ii_to_iii = l3.computeOut(l2.a)

print(l3.a)