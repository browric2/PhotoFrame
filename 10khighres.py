# import os
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


import tensorflow as tf
import random
from general_funcs import resize_array
from keras.models import load_model, Model
from keras.layers import Input
from math import floor
from PIL import Image
import numpy as np
import cv2
import os
from string import ascii_lowercase
from keras.preprocessing.image import ImageDataGenerator
from skimage.filters import gaussian
from time import time

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


config = tf.ConfigProto()
config.gpu_options.allow_growth = False
sess = tf.Session(config=config)

folder = 'data/playlists/best2'


n_model = 'model-ep090-loss0.495-val_loss0.477'
image_folder = 'vid_ims'
num_digits = 100
interpolate = 18
# end1 = 33
# end2 = 68
bigsize = (1280,1280)
smallsize = (96,96)
input_img = (96, 96, 3)


data_gen = ImageDataGenerator(
        featurewise_std_normalization=True,
        rescale=1./255,
        )

train_gen = data_gen.flow_from_directory(folder,
                                         interpolation='bicubic',
                                         target_size=bigsize,
                                         class_mode=None,
                                         batch_size = 1)



modelfile = 'models/auto_test/' + n_model + '.h5'
autoencoder = load_model(modelfile)
end1 = floor((len(autoencoder.layers)/2))
end2 = len(autoencoder.layers)
input_size = autoencoder.layers[end1-1].output_shape[1:]

encoded_input = Input(input_size)
first_input = Input(shape=input_img)
x = autoencoder.layers[0](first_input)

for l in range(1,end1):
    x = autoencoder.layers[l](x)
    print(autoencoder.layers[l].name)
encoder = Model(first_input,x)

y = autoencoder.layers[end1](encoded_input)
for l in range(end1+1,end2):
    y = autoencoder.layers[l](y)
decoder = Model(encoded_input,y)
#decoder.summary()




flist = ['data/playlists/best2/'+f for f in os.listdir('data/playlists/best2')]
random.shuffle(flist)

flist = flist[:num_digits]

biglist = [resize_array(np.array(Image.open(f).convert('RGB')),bigsize) for f in flist]
smallist = [resize_array(np.array(Image.open(f).convert('RGB')),smallsize) for f in flist]


images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
for image in images:
    os.remove(image_folder+'/' + image)


L = list(ascii_lowercase) + [letter1+letter2+letter3 for letter1 in ascii_lowercase for letter2 in ascii_lowercase for letter3 in ascii_lowercase]
L = sorted(L)
j = 1


big_img = biglist[0]
im = Image.fromarray((big_img).astype('uint8'))
small_img = smallist[0]



for digit in range(1,num_digits):

    ilist = [0] * interpolate
    i1 = ilist[0] = encoder.predict(np.array([small_img])*(1/255))
    result = resize_array(np.array(decoder.predict(i1)[0] * 255).astype('uint8'), bigsize)
    result = (gaussian(result,sigma=8)*255).astype('uint8')

    for i in range(interpolate):

        temp_im = big_img + ((result.astype('int')-big_img.astype('int'))/interpolate)*i
        n1 = image_folder+"/im" + L[j - 1] + ".png"
        im = Image.fromarray((temp_im).astype('uint8'))
        im.save(n1)
        j += 1


    t1 = time()
    big_img = biglist[digit]
    small_img = smallist[digit]

    i2 = encoder.predict(small_img.reshape(((1,) + input_img))*(1/255))
    diff = (i2 - i1)

    for i in range(1, interpolate):
        di = diff * (i / interpolate)
        i_n = i1 + di
        ilist[i] = i_n

    for i in ilist:

        result = np.array(decoder.predict(i)[0])
        # print(result)
        # gaussian(result, sigma=1)
        result = (gaussian(result,sigma=1)*255).astype('uint8')
        result = resize_array(result,bigsize)
        n1 = image_folder+"/im" + L[j - 1] + ".png"
        im = Image.fromarray(result)
        im.save(n1)
        j += 1


    t2 = time()
    print(t2-t1)

    result = resize_array(np.array(decoder.predict(i2)[0] * 255).astype('uint8'), bigsize)
    result = (gaussian(result,sigma=8)*255).astype('uint8')

    for i in range(interpolate):
        temp_im = result + ((big_img.astype('int')-result.astype('int'))/interpolate)*i
        n1 = image_folder+"/im" + L[j - 1] + ".png"
        im = Image.fromarray((temp_im).astype('uint8'))
        im.save(n1)
        j += 1



    print('completed: ',digit,'/',num_digits-1)


################



fps = 19

video_name = 'videonew3.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

fourcc = cv2.VideoWriter_fourcc(*'MPEG')
video = cv2.VideoWriter(video_name, 0, fps, (width,height))

p = 1
for image in images:
    for i in range(0,p,1):
        video.write(cv2.imread(os.path.join(image_folder, image)))

numend = 5
for i in range(0,numend):
    image = image[-1]
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()