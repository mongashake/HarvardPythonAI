if we use only one layer of dense connections as the input layer, flatten it, and output to a dense layer of NUM_CATEGORIES nodes, we get a decent result. Over 85% accuracy and less than 0.9 loss. 
This is drastically changed if we add more hidden layers ( experimented with two dense layers of 64 and 128 nodes each). The accuracy drops significantly and reaches 0.05. The might happen because we did not use convolution so the network is just learning on the basis of pixels and colors instead of features. We should extract features using 2D Convolution so pass the resulting images (they will be smaller without padding) and learn on them. That should perform better. The number of kernels to be used is still not clear.

Used a 2D Convolution layer with 24 3x3 kernels as the input layer and noticed significant improvement. The accuracy reached 0.91 and the loss reached 0.98. This shows that convolution is really helpful as it extracts features and the network learns on them. We can try to use a convolution layer and a pooling layer, followed by another convolution layer and a dense layer. 

Added a 2x2 MaxPool2D layer ( after 2D Convolution input layer and before Flattening). Accuracy increased to 0.93 and loss decreased to 0.57. Slight improvement. Should try another a dense network in the end or a 2DConv next.

Added a 128 node dense network before the output. Accuracy is 0.93 and loss is 0.49. No significant improvement. Will try another layer of 2DConv.

Added a 2DConv layer with 24 3x3 kernels after the first round of 2DConv and MaxPooling2D. Decent improvement. Accuracy increased to 0.9566 and loss reduced to 0.3. Should add more convolution layers.

Added another 2DConv layer with 4 3x3 kernels. Accuracy drops completely when the layer has less kernels. Replaced 4 layers with 24 and accuracy went back up to 0.95. Technically this layer provides no further advantage after the last one. should try MaxPooling2D

added a MaxPooling2D layer. accuracy 0.93. No improvement. Need something else.
increased second last dense layer from 128 to 256. accuracy 0.94 and loss 0.2. Meh.


After some experiments, this is the config: 24 3x3 2DConv, 2x2 MaxPool2D, 24 3x3 2DConv, Flatten, Dense 128, Dense 256, and the secret ingredient - dropout 0.4. Great results. Accuracy 0.97 and loss 0.15. Ran again - Accuracy 0.94. Damn.

Final Observation: 32 3x3 2DConv (as input), 32 3x3 2DConv, 2x2 MaxPool2D, 32 3x3 2DConv, 2x2 MaxPool2D, Flatten, Dense 256, Dense 128, and the secret ingredient - dropout 0.4. The dense nodes maintain a pyramid shape so I think that helps. Learns properly from data early on and improves backpropagation. Slowly decreasing nodes reduce noise. Tried 3 or 4 runs. Accuracy 0.97 0.98.