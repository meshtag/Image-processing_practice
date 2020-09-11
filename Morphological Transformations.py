from PIL import Image
import numpy as np
import matplotlib.pyplot as plt 

#orig_img=Image.open('morphological.png')
orig_img=plt.imread('morphological.png')
structuring_element=np.array([[0, 1, 0],
                              [1, 1, 1],
                              [0, 1, 0]])

def convolution_dilation(ker_mat,img):
    xk,yk = ker_mat.shape
    x,y = img.shape
    img_pad=np.zeros((x+xk-1,y+yk-1))
    img_pad[xk-int(xk/2)-1:xk-1-int(xk/2)+x,yk-int(yk/2)-1:yk-int(yk/2)-1+y]=img
    op_img=np.zeros_like(img)
    for x1 in range(int(xk/2),int(xk/2)+x):
        for y1 in range(int(yk/2),int(yk/2)+y):
                sum=(ker_mat*img_pad[x1-int(xk/2):x1-int(xk/2)+xk,y1-int(yk/2):y1-int(yk/2)+yk]).sum()
                if(sum>0):
                    op_img[x1-int(xk/2),y1-int(yk/2)]=1
                else:
                    op_img[x1-int(xk/2),y1-int(yk/2)]=0
    return op_img

def convolution_erosion(ker_mat,img):
    xk,yk = ker_mat.shape
    x,y = img.shape
    img_pad=np.zeros((x+xk-1,y+yk-1))
    img_pad[xk-int(xk/2)-1:xk-1-int(xk/2)+x,yk-int(yk/2)-1:yk-int(yk/2)-1+y]=img
    op_img=np.zeros_like(img)
    for x1 in range(int(xk/2),int(xk/2)+x):
        for y1 in range(int(yk/2),int(yk/2)+y):
                sum=(ker_mat*img_pad[x1-int(xk/2):x1-int(xk/2)+xk,y1-int(yk/2):y1-int(yk/2)+yk]).sum()
                if sum==5:
                    op_img[x1-int(xk/2),y1-int(yk/2)]=1
                else:
                    op_img[x1-int(xk/2),y1-int(yk/2)]=0
    return op_img

def rgb2gray(img):
    r,g,b = img[:,:,0],img[:,:,1],img[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def gray2binary(gray):
    return (127 < gray) & (gray <= 255)

im = gray2binary(rgb2gray(np.array(Image.open('morphological.png'))))
im_dilation=convolution_dilation(structuring_element,im)
im_erosion=convolution_erosion(structuring_element,im)
im_ot=convolution_erosion(structuring_element,convolution_dilation(structuring_element,im))
pil_img_d=Image.fromarray(im_dilation).convert('RGB')
pil_img_e=Image.fromarray(im_erosion).convert('RGB')
pil_img_ot=Image.fromarray(im_ot).convert('RGB')
#pil_img.save('result_dilation.png')
plt.imshow(orig_img)
plt.text(0,-5,"Original Image")
plt.show()
plt.imshow(pil_img_d)
plt.text(0,-5,"Dilation")
plt.show()
plt.imshow(pil_img_e)
plt.text(0,-5,"Erosion")
plt.show()
plt.imshow(pil_img_ot)
plt.text(0,-5,"Opening Transformation")
plt.show()