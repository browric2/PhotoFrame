import tensorflow as tf
import os
from keras.layers import Input, Flatten, Dense, Conv2D, MaxPooling2D, UpSampling2D,\
    BatchNormalization, Activation, Cropping2D, Reshape, Dropout
from keras.models import Model
from keras.optimizers import Adam

from keras.utils import plot_model
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, EarlyStopping
from matplotlib import pyplot as plt

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def fixed_generator(generator):
    for batch in generator:
        yield (batch, batch)


config = tf.ConfigProto()
config.gpu_options.allow_growth = False
session = tf.Session(config=config)

folder = 'data/auto_test/'

#12 16 256

input_img = Input(shape=(96, 96, 3))


x = Conv2D(128, (3, 3), padding='same',activation='relu')(input_img)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(128, (3, 3), padding='same',activation='relu')(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(128, (3, 3), padding='same',activation='relu')(x)

encoded = MaxPooling2D((2, 2), padding='same')(x)

#x = BatchNormalization(axis=3)(x)
#x = Cropping2D(((0,0),(1,0)))(x)

x = Conv2D(128, (3, 3), padding='same',activation='relu')(encoded)
x = UpSampling2D((2, 2))(x)
x = Conv2D(128, (3, 3), padding='same',activation='relu')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(128, (3, 3), padding='same',activation='relu')(x)
x = UpSampling2D((2, 2))(x)
decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)


autoencoder = Model(input_img, decoded)
autoencoder.summary()

print(tuple([i.value for i in encoded.shape][1:]))

Ad = Adam(lr=0.000005)

autoencoder.compile(optimizer=Ad, loss='binary_crossentropy')
#plot_model(autoencoder, to_file='model.png', show_shapes=True)
###############

data_gen = ImageDataGenerator(
        featurewise_std_normalization=True,
        validation_split = 0.2,
        rescale=1./255,
        horizontal_flip=True,
        rotation_range=5,
        width_shift_range=0.05,
        height_shift_range=0.05,
        zoom_range=[0.95, 1.05],
        )

train_gen = data_gen.flow_from_directory(folder,
                                         target_size=(96, 96),
                                         class_mode=None,
                                         batch_size = 1,
                                         interpolation='bilinear',
                                         subset='training',)

test_gen = data_gen.flow_from_directory(folder,
                                        target_size=(96, 96),
                                        #save_to_dir='jaffe_edit/',
                                        class_mode=None,
                                        interpolation='bilinear',
                                        batch_size=1,
                                        subset='validation')


checkfile = 'models/auto_test/model-ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5'
callbacks = [
    EarlyStopping(
        monitor='val_loss',
        patience=50,
        mode='min',
        verbose=1),
    ModelCheckpoint(checkfile,
        monitor='val_loss',
        save_best_only=True,
        mode='min',
        verbose=1)
]
history = autoencoder.fit_generator(
        fixed_generator(train_gen),
        steps_per_epoch=20,
        validation_steps=20,
        shuffle=True,
        epochs=200,
        validation_data=fixed_generator(test_gen),
        callbacks=callbacks
        )

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


#encoder = Model(input_img, encoded)
encoded_input = Input(shape=tuple([i.value for i in encoded.shape][1:]))
#decoder = Model(encoded, decoded)
img = train_gen.next()
encoded_img = autoencoder.predict(img)

orig = img.reshape((96, 96,3))
plt.imshow(orig)
plt.axis('off')
plt.show()

result = encoded_img.reshape((96, 96,3))
plt.imshow(result)
plt.axis('off')
plt.show()