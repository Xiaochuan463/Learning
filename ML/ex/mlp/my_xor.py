"""
A neural netwoerk to generate Xor

Now, it is trained to be a 2-4 encoder

and maybe an adder?

It real name is mlp

with regularization
"""


import numpy as np
from weight import Weight

x = [[0., 0.],
     [0., 1.],
     [1., 0.],
     [1., 1.]]
y = [[0.,0.],
     [0.,1.],
     [0.,1.],
     [1.,0.]]

x = np.array(x)
y = np.array(y)

INPUT_NODES = x.shape[1]
HIDDEN_NODES_I = 3
HIDDEN_NODES_II = 5
OUTPUT_NODES = y.shape[1]
STUDY_RATE = 0.1
REGULARIZATION_RATE = 0.00005

STEP = 50000

ih = Weight(INPUT_NODES, HIDDEN_NODES_I)
hihii = Weight(HIDDEN_NODES_I, HIDDEN_NODES_II)
ho = Weight(HIDDEN_NODES_II, OUTPUT_NODES)

for i in range(STEP):

    #forward propagation
    hidden_layer = ih.get_output(input_data=x)
    h2 = hihii.get_output(input_data=ih.output_data)
    end = ho.get_output(input_data=hihii.output_data)

    #backward propagation
    ho.get_derivative(next_weight= None, result= y, is_end= True)
    hihii.get_derivative(ho)
    ih.get_derivative(hihii)

    #update using gradient decent
    ho.update(STUDY_RATE, REGULARIZATION_RATE)
    hihii.update(STUDY_RATE, REGULARIZATION_RATE)
    ih.update(STUDY_RATE, REGULARIZATION_RATE)
print((end))
print(np.round(end))
