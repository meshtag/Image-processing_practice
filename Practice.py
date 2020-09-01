from PIL import Image
import os
#im1=Image.open('rotate.png')
#im1.show()
#im1.save('rotate.jpg')#Easy conversion from png image to jpg image.
#We can also loop over a certain number of images and perform desired conversions instead of handling ont one single image at a particular time.
for f in os.listdir('.'):
    i=Image.open(f)
    if f.endswith('.jpg'):
        print(f+'  is a jpg image')
        fn,fext=os.path.splitext(f)
        i.save('Type Converted Images/{}.png'.format(fn))
    #elif f.endswith('.png'):#This conversion won't work and would give an error because jpg does not supports transparency.
     #   print(f+' is a png image')
      #  fn,fext=os.path.splitext(f)
       # i.save('Type Converted Images/{}.jpg'.format(fn))