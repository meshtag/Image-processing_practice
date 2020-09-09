import matplotlib.pyplot as plt 
import numpy as np

orig_img=plt.imread('edge-detection.png')
orig_img_arr=np.array(orig_img)
img_op=np.zeros_like(orig_img_arr)

avg_ker=1/16*np.array([
    [1,2,1],
    [2,4,2],
    [1,2,1]
])

y_kernel=np.array([
    [-1,-2,-1],
    [ 0, 0, 0],
    [ 1, 2, 1]
])
x_kernel=np.array([[-1,0,1],
                    [-2,0,2],
                    [-1,0,1]])

sobel=x_kernel+y_kernel
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
def rgb2gray(img):
    r,g,b = img[:,:,0],img[:,:,1],img[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def convolution(ker_mat,img):
    xk,yk = ker_mat.shape
    x,y = img.shape
    img_pad=np.zeros((x+xk-1,y+yk-1))
    img_pad[xk-int(xk/2)-1:xk-1-int(xk/2)+x,yk-int(yk/2)-1:yk-int(yk/2)-1+y]=img
    op_img=np.zeros_like(img)
    for x1 in range(int(xk/2),int(xk/2)+x):
        for y1 in range(int(yk/2),int(yk/2)+y):
                op_img[x1-int(xk/2),y1-int(yk/2)]=(ker_mat*img_pad[x1-int(xk/2):x1-int(xk/2)+xk,y1-int(yk/2):y1-int(yk/2)+yk]).sum()
    return op_img

img_op=convolution(sobel,convolution(avg_ker,rgb2gray(orig_img_arr)))
#img_op=rgb2gray(orig_img_arr)#Grayscaling deletes one channel and hence reduces the no. of dimensions present in the image to 2 from 3.
print(img_op.shape)
plt.imshow(img_op)
plt.show()

res_orig=convolution(gaussian_blur5x5_sigma1,rgb2gray(orig_img_arr))
res_origx=convolution(x_kernel,res_orig)
res_origy=convolution(y_kernel,res_orig)
res_orig_op=np.hypot(res_origx,res_origy)
plt.imshow(res_orig_op)
plt.show()
res_orig_conv_op=Image.fromarray(res_orig_op).convert('RGB')#For converting the image in rgb to avoid the blue background.
#But it is not working as intended with images processed from matplotlib library,works fine with pillow.
plt.imshow(res_orig_conv_op)
plt.show()
