# import os
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


import tensorflow as tf
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

folder = 'data/auto_test'


n_model = 'auto_test/model-ep090-loss0.495-val_loss0.477'
image_folder = 'vid_ims'
num_digits = 10
interpolate = 18
# end1 = 33
# end2 = 68
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
                                         interpolation='bilinear',
                                         target_size=(96, 96),
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

img = train_gen.next()
encoded_img = encoder.predict(img)


print('hi2')
#redecoded_imgs = decoder.predict(encoded_imgs)
print('hi3')

orig = train_gen[0].reshape(input_img)
plt.imshow(orig)
plt.axis('off')
plt.show()

result = decoder.predict(encoded_img.reshape( ((1,)+input_size) ))
plt.imshow(result.reshape(input_img))
plt.axis('off')
plt.show()





images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
for image in images:
    os.remove(image_folder+'/' + image)


L = list(ascii_lowercase) + [letter1+letter2 for letter1 in ascii_lowercase for letter2 in ascii_lowercase]
L = sorted(L)
j = 1


for digit in range(0,num_digits-1):

    ilist = [0] * interpolate
    i1 = ilist[0] = encoder.predict(img)

    print(img.shape)
    print(i1.shape)

    for i in range(interpolate):
        result = decoder.predict(i1.reshape(((1,) + input_size)))
        temp_im = img + ((result-img)/interpolate)*i
        # plt.axis('off')
        # plt.imshow(temp_im.reshape(input_img))
        n1 = image_folder+"/a_im" + L[i] + ".png"
        im = Image.fromarray(temp_im)
        plt.savefig(n1)
        plt.close()


    img = train_gen.next()
    i2 = encoder.predict(img)
    diff = (i2 - i1)

    for i in range(1, interpolate):
        di = diff * (i / interpolate)
        i_n = i1 + di
        ilist[i] = i_n

    for i in ilist:
        result = decoder.predict(i.reshape( ((1,)+input_size) ))
        #result = decoder.predict(i)
        plt.axis('off')
        plt.imshow(result.reshape(input_img))
        #plt.gray()
        n1 = image_folder+"/im" + L[j - 1] + ".png"
        plt.savefig(n1)
        plt.close()
        j += 1

    for i in range(interpolate):
        result = decoder.predict(i2.reshape(((1,) + input_size)))
        temp_im = result + ((img-result)/interpolate)*i
        plt.axis('off')
        plt.imshow(temp_im.reshape(input_img))
        n1 = image_folder+"/z_im" + L[i] + ".png"
        plt.savefig(n1)
        plt.close()

    print('completed: ',digit+1,'/',num_digits-1)


################



fps = 14

#image_folder = 'images'
video_name = 'videonew3.mp4'

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