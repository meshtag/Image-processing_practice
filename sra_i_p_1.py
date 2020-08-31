import PIL
from PIL import Image
im=Image.open('rotate.png')
i=int(input('Enter the desired angle of rotation for the image- '))
im=im.rotate(i,PIL.Image.NEAREST,expand = 1)
im.show()