import matplotlib.pyplot as plt 
import numpy as np
from PIL import Image

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

def convolution2(ker_mat,img):#For convolution of images with rgb values,kept here only for experimental purposes.
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

def non_max_suppression(img, D):
    M, N = img.shape
    Z = np.zeros((M,N), dtype=np.int32)
    angle = D * 180. / np.pi
    angle[angle < 0] += 180

    
    for i in range(1,M-1):
        for j in range(1,N-1):
            try:
                q = 255
                r = 255
                
               #angle 0
                if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                    q = img[i, j+1]
                    r = img[i, j-1]
                #angle 45
                elif (22.5 <= angle[i,j] < 67.5):
                    q = img[i+1, j-1]
                    r = img[i-1, j+1]
                #angle 90
                elif (67.5 <= angle[i,j] < 112.5):
                    q = img[i+1, j]
                    r = img[i-1, j]
                #angle 135
                elif (112.5 <= angle[i,j] < 157.5):
                    q = img[i-1, j-1]
                    r = img[i+1, j+1]

                if (img[i,j] >= q) and (img[i,j] >= r):
                    Z[i,j] = img[i,j]
                else:
                    Z[i,j] = 0

            except IndexError as e:
                pass
    
    return Z

def threshold(img, weak,strong,lowThresholdRatio=0.05, highThresholdRatio=0.09):
    highThreshold = img.max() * highThresholdRatio
    lowThreshold = highThreshold * lowThresholdRatio
    M, N = img.shape
    res = np.zeros((M,N), dtype=np.int32)
    weak = np.int32(weak)
    strong = np.int32(strong)
    strong_i, strong_j = np.where(img >= highThreshold)
    zeros_i, zeros_j = np.where(img < lowThreshold)
    weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))
    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak
    return (res, weak, strong)

def hysteresis(img, weak, strong=255):
    M, N = img.shape  
    for i in range(1, M-1):
        for j in range(1, N-1):
            if (img[i,j] == weak):
                try:
                    if ((img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
                        or (img[i, j-1] == strong) or (img[i, j+1] == strong)
                        or (img[i-1, j-1] == strong) or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError as e:
                    pass
    return img


img_op=convolution(sobel,convolution(avg_ker,rgb2gray(orig_img_arr)))
#img_op=rgb2gray(orig_img_arr)#Grayscaling deletes one channel and hence reduces the no. of dimensions present in the image to 2 from 3.
print(img_op.shape)
'''plt.imshow(img_op)
plt.show()'''

res_orig=rgb2gray(convolution2(gaussian_blur5x5_sigma2,orig_img_arr))
res_origx=convolution(x_kernel,res_orig)
res_origy=convolution(y_kernel,res_orig)
res_orig_op=np.hypot(res_origx,res_origy)
res_orig_op=res_orig_op/res_orig_op.max()*255
theta=np.arctan(res_origy/res_origx)
#res_orig_op=rgb2gray(res_orig_op)
res_orig_op=non_max_suppression(res_orig_op,theta)
weak=75
strong=255
canny_output_img=threshold(res_orig_op,weak,strong,0.05,0.09)
# applying hysteresis
res_orig_op=hysteresis(canny_output_img[0],canny_output_img[1],canny_output_img[2])


plt.imshow(res_orig_op)
plt.text(250,-5,"Canny Edge Detection output")
plt.show()
#res_orig_conv_op=Image.fromarray(res_orig_op).convert('RGB')#For the converting the image in rgb to avoid the blue background.
#But it is not working as intended with images processed from matplotlib library,works fine with pillow.
'''print(res_orig_op)
res_orig_conv_op=np.zeros_like(res_orig_op)
plt.imshow(res_orig_conv_op)
plt.show()
for x1 in range(res_orig_op.shape[0]):
    for y1 in range(res_orig_op.shape[1]):
        if(res_orig_op[x1,y1]>0):
            res_orig_conv_op[x1,y1]=0.5
plt.imshow(res_orig_conv_op)
plt.show()'''
