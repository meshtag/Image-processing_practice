import matplotlib.pyplot as plt 
import numpy as np

orig_img=plt.imread('edge-detection.png')
orig_img_arr=np.array(orig_img)
plt.imshow(orig_img_arr)
plt.show()
#Use 9x9 gaussian blur for greater accuracy.Difference of gaussian kernels can also be applied for even increasing accuracy.
gaussian_blur9x9=np.array([
    
[0,	0.000001,	0.000014,	0.000055,	0.000088,	0.000055,	0.000014,	0.000001,	0],
[0.000001,	0.000036,	0.000362,	0.001445,	0.002289,	0.001445,	0.000362,	0.000036,	0.000001],
[0.000014,	0.000362,	0.003672,	0.014648,	0.023205,	0.014648,	0.003672,	0.000362,	0.000014],
[0.000055,	0.001445,	0.014648,	0.058434,	0.092566,	0.058434,	0.014648,	0.001445,	0.000055],
[0.000088,	0.002289,	0.023205,	0.092566,	0.146634,	0.092566,	0.023205,	0.002289,	0.000088],
[0.000055,	0.001445,	0.014648,	0.058434,	0.092566,	0.058434,	0.014648,	0.001445,	0.000055],
[0.000014,	0.000362,	0.003672,	0.014648,	0.023205,	0.014648,	0.003672,	0.000362,	0.000014],
[0.000001,	0.000036,	0.000362,	0.001445,	0.002289,	0.001445,	0.000362,	0.000036,	0.000001],
[0,	0.000001,	0.000014,	0.000055,	0.000088,	0.000055,	0.000014,	0.000001,	0]
])

gaussian_blur5x5_sigma1=np.array([[1,  4,  6,  4, 1],
                         [4, 16, 24, 16, 4],
                         [6, 24, 36, 24, 6],
                         [4, 16, 24, 16, 4],
                         [1,  4,  6,  4, 1]])/256

gaussian_blur5x5_sigma2=np.array([
    
[0.023528,	0.033969,	0.038393,	0.033969,	0.023528],
[0.033969,	0.049045,	0.055432,	0.049045,	0.033969],
[0.038393,	0.055432,	0.062651,	0.055432,	0.038393],
[0.033969,	0.049045,	0.055432,	0.049045,	0.033969],
[0.023528,	0.033969,	0.038393,	0.033969,	0.023528]
])

gaussian_blur_DoG_2_1=gaussian_blur5x5_sigma2-gaussian_blur5x5_sigma1

y_kernel=np.array([
    [-1,-2,-1],
    [ 0, 0, 0],
    [ 1, 2, 1]
])
x_kernel=np.array([[-1,0,1],
                    [-2,0,2],
                    [-1,0,1]])
def convolution(ker_mat,img):
    xk,yk = ker_mat.shape
    x,y,z = img.shape
    img_pad=np.zeros((x+xk-1,y+yk-1,z))
    img_pad[xk-int(xk/2)-1:xk-1-int(xk/2)+x,yk-int(yk/2)-1:yk-int(yk/2)-1+y,:]=img
    op_img=np.zeros_like(img)
    for x1 in range(int(xk/2),int(xk/2)+x):
        for y1 in range(int(yk/2),int(yk/2)+y):
            for z1 in range(z):
                op_img[x1-int(xk/2),y1-int(yk/2),z1]=(ker_mat*img_pad[x1-int(xk/2):x1-int(xk/2)+xk,y1-int(yk/2):y1-int(yk/2)+yk,z1]).sum()
    return op_img


orig_img_arr = convolution(x_kernel,convolution(gaussian_blur5x5_sigma1,orig_img_arr))
res_img=np.zeros_like(orig_img_arr)
plt.imshow(orig_img_arr)
plt.text(250,-5,"Vertical Edge Detection")
plt.show()

orig_img_arr1=np.array(orig_img)
orig_img_arr1 = convolution(y_kernel,convolution(gaussian_blur5x5_sigma1,orig_img_arr))
plt.imshow(orig_img_arr1)
plt.text(250,-5,"Horizontal Edge Detection")
plt.show()

'''for x1 in range(1,x-1):
    for y1 in range(y):
        for z1 in range(z):
            res_img[x1,y1,z1]=orig_img_arr[x1+1,y1,z1]-orig_img_arr[x1-1,y1,z1]
plt.imshow(res_img)
plt.text(250,-5,"horizontal_edge_detection")
plt.show()

res_imgh=np.zeros_like(orig_img_arr)

for x1 in range(x):
    for y1 in range(1,y-1):
        for z1 in range(z):
            res_imgh[x1,y1,z1]=orig_img_arr[x1,y1+1,z1]-orig_img_arr[x1,y1-1,z1]
plt.imshow(res_imgh)
plt.text(250,-5,"vertical_edge_detection")
plt.show()'''