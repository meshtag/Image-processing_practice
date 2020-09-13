import matplotlib.pyplot as plt 
import numpy as np

orig_img=plt.imread('filter.png')
orig_img_arr=np.array(orig_img)
print('Image shape is '+str(orig_img_arr.shape))
box_blur=np.array([
    [1/9,1/9,1/9],
    [1/9,1/9,1/9],
    [1/9,1/9,1/9]
])
sharpen=np.array([
[0,-1,0],
[-1,5,-1],
[0,-1,0]
])
sharpen7=np.array([
    [-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,49,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1]
])
sharpen5=np.array([
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1],
    [-1,-1,25,-1,-1],
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1]
])
gaussian_blur=np.array([[1,  4,  6,  4, 1],
                         [4, 16, 24, 16, 4],
                         [6, 24, 36, 24, 6],
                         [4, 16, 24, 16, 4],
                         [1,  4,  6,  4, 1]])/256
                         
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

res_img = convolution(sharpen5,orig_img_arr)
plt.imshow(res_img)
plt.text(250,-5,"sharpen")
plt.savefig('res_sharpen')
plt.show()