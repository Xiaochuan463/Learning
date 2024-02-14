"""
A neural netwoerk to generate Xor
"""


import numpy as np
from weight import Weight

x = [[0., 0.], [0., 1.], [1., 0.],[1., 1.]]
y = [[0.], [1.], [1.], [0.]]

x = np.array(x)
y = np.array(y)

INPUT_NODES = 2
HIDDEN_NODES = 3
OUTPUT_NODES = 1
STUDY_RATE = 0.1

STEP = 10000

ih = Weight(INPUT_NODES, HIDDEN_NODES)
ho = Weight(HIDDEN_NODES, OUTPUT_NODES)

for i in range(STEP):

    #forward propagation
    hidden_layer = ih.get_output(input_data=x)
    end = ho.get_output(input_data=ih.output_data)

    #backward propagation
    ho.get_derivative(next_weight= None, result= y, is_end= True)
    ih.get_derivative(ho)

    #update using gradient decent
    ho.update(STUDY_RATE)
    ih.update(STUDY_RATE)

print(end)
