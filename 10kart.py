# import os
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


import tensorflow as tf
from general_funcs import *
from keras.models import load_model, Model
from keras.layers import Input
from math import floor
from PIL import Image
from keras.datasets import mnist
import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
from string import ascii_lowercase
from keras.preprocessing.image import ImageDataGenerator

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


config = tf.ConfigProto()
config.gpu_options.allow_growth = False
sess = tf.Session(config=config)

folder = 'highres'


n_model = 'auto_test/model-ep090-loss0.495-val_loss0.477'
image_folder = 'vid_ims'
num_digits = 10
interpolate = 18
# end1 = 33
# end2 = 68
bigsize = (1280,1280)
smallsize = (96,96)
input_img = (96, 96, 3)


data_gen = ImageDataGenerator(
        featurewise_std_normalization=True,
        rescale=1./255,
        #horizontal_flip=True,
        #rotation_range=5,
        #width_shift_range=0.05,
        #height_shift_range=0.05,
        #zoom_range=[0.95, 1.05],
        #horizontal_flip=True,
        )

train_gen = data_gen.flow_from_directory(folder,
                                         interpolation='bicubic',
                                         target_size=bigsize,
                                         class_mode=None,
                                         batch_size = 1)



modelfile = 'models/' + n_model + '.h5'
autoencoder = load_model(modelfile)
end1 = floor((len(autoencoder.layers)/2))
# print(end1)
end2 = len(autoencoder.layers)
#input_size = tuple([i.value for i in autoencoder.layers[end1-1].shape][1:])
input_size = autoencoder.layers[end1-1].output_shape[1:]

print(input_size)
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
decoder.summary()




flist = ['highres/'+f for f in os.listdir('highres')]

# Imageen(flist[0]).convert('RGB').show()

biglist = [resize_arr(np.array(Image.open(f).convert('RGB')),bigsize) for f in flist]
smallist = [resize_arr(np.array(Image.open(f).convert('RGB')),smallsize) for f in flist]






# img = train_gen.next()
# encoded_img = encoder.predict(img)


images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
for image in images:
    os.remove(image_folder+'/' + image)


L = list(ascii_lowercase) + [letter1+letter2 for letter1 in ascii_lowercase for letter2 in ascii_lowercase]
L = sorted(L)
j = 1


big_img = biglist[0]
im = Image.fromarray((big_img).astype('uint8'))
im.show()
small_img = smallist[0]


####RESIZE ARRAY NOT WORKING!!



for digit in range(1,num_digits):

    ilist = [0] * interpolate
    i1 = ilist[0] = encoder.predict(np.array([small_img])*(1/255))

    for i in range(interpolate):

        result = resize_arr(np.array(decoder.predict(i1)[0]*255).astype('uint8'),bigsize)


        # Image.fromarray((decoder.predict(i1)[0]*255).astype('uint8')).show()
        # Image.fromarray((result*255).astype('uint8')).show()

        #print(result)

        #Image.fromarray(result).show()
        temp_im = big_img + ((result-big_img)/interpolate)*i
        n1 = image_folder+"/im" + L[j - 1] + ".png"
        im = Image.fromarray((temp_im).astype('uint8'))
        #im.show()
        im.save(n1)
        j += 1



    big_img = biglist[digit]
    small_img = smallist[digit]

    print(small_img.shape)
    i2 = encoder.predict(small_img.reshape(((1,) + input_img))*(1/255))
    diff = (i2 - i1)

    for i in range(1, interpolate):
        di = diff * (i / interpolate)
        i_n = i1 + di
        ilist[i] = i_n

    for i in ilist:


        result = resize_arr(np.array(decoder.predict(i)[0]*255).astype('uint8'),bigsize)
        n1 = image_folder+"/im" + L[j - 1] + ".png"
        im = Image.fromarray((result*255).astype('uint8'))
        im.save(n1)
        j += 1

    for i in range(interpolate):
        result = resize_arr(np.array(decoder.predict(i2)[0]*255).astype('uint8'),bigsize)
        #result = decoder.predict(i2.reshape(((1,) + input_size)))
        temp_im = result + ((big_img-result)/interpolate)*i
        n1 = image_folder+"/im" + L[j - 1] + ".png"
        im = Image.fromarray((temp_im*255).astype('uint8'))
        im.save(n1)
        j += 1



    print('completed: ',digit,'/',num_digits-1)


################



fps = 14

#image_folder = 'images'
video_name = 'videonew3.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

fourcc = cv2.VideoWriter_fourcc(*'MPEG')
video = cv2.VideoWriter(video_name, fourcc, fps, (width,height))

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