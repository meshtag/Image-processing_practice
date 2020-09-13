import matplotlib.pyplot as plt 
import numpy as np
img=plt.imread('roi_ball.jpg')
print(img.shape)
plt.imshow(img)
plt.show()
img1=plt.imread('roi.jpg')
img1_arr=np.array(img1)
img1_arr[820:1027,250:477,:]=img
plt.imshow(img1_arr)
plt.show()