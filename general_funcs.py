from PIL import Image
import numpy as np


def resize_array(arr,size):
    im = Image.fromarray(arr)#.astype('uint8'),mode='RGB')
    im = im.resize(size,resample=Image.BICUBIC)
    return np.array(im)

