import numpy
import math
import imageio
from PIL import Image,ImageEnhance
from io import BytesIO

def captcha_solver(img_data):
    image = Image.open(BytesIO(img_data))
    enhancer = ImageEnhance.Contrast(image)
    im_output = enhancer.enhance(10)
    image = im_output

    # image = Image.open(image)
    image = numpy.array(image, dtype=numpy.uint8)


    for i in range(100,250):
        segments=[]
        pixels = list(image[i])
        mbi_250 = [0 == (sum(pixel) / len(pixel)) for pixel in pixels]
        indices = [i for i, x in enumerate(mbi_250) if x == True]
        for i in range(len(indices)-80):
            if indices[i] == indices[i+80]-80:
                    return indices[i] # offseti nga pozicionimi i copezes

            if indices[i] == indices[i+23]-23 and indices[i+56] == indices[i+80]-56:
                    return indices[i] # offseti nga pozicionimi i copezes
    return False



