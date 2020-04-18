import numpy as np
from PIL import Image
import os
from tqdm import tqdm
import pickle as pkl
from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

###################

class Similarity():

    def __init__(self,name):
        self.name = name
        self.asPIL = False

    def calc_dist(self, *args):
        raise NotImplementedError('Base class \'Similarity\' does not implement method \'calc_sim\'')

    def get_im(self,image):
        if self.asPIL == True: return Image.open(image).convert('RGB')
        else: return image

    def order_images(self,ref_im,im_list):

        sims = []
        ref_image = self.get_im(ref_im)

        for img in tqdm(im_list):
            output = self.calc_dist(ref_image,self.get_im(img))
            sims.append(output)

        pkl.dump(im_list,open('Messing(delete)/'+self.name+'_list.pkl','wb'))
        pkl.dump(sims,open('Messing(delete)/'+self.name+'_sims.pkl','wb'))

        return np.argsort(sims)

class grid_dist(Similarity):

    def __init__(self, grid_size=(10,10)):
        self.grid_size=grid_size
        Similarity.__init__(self,'Grid_Sim')
        self.asPIL = True

    def calc_dist(self,im1,im2):

        arr1 = np.array(im1.resize(self.grid_size))
        arr2 = np.array(im2.resize(self.grid_size))

        return np.sum(abs(arr1.astype(int)-arr2.astype(int)))

class vgg_dist(Similarity):

    def __init__(self):

        # load the model
        model = VGG16()
        # re-structure the model
        model.layers.pop()
        self.model = Model(inputs=model.inputs, outputs=model.layers[-1].output)

        Similarity.__init__(self,'VGG_Sim')

    def calc_dist(self,im1,im2):

        image1 = load_img(im1, target_size=(224, 224))
        image2 = load_img(im2, target_size=(224, 224))
        # convert the image pixels to a numpy array
        image1 = img_to_array(image1)
        image2 = img_to_array(image2)
        # reshape data for the model
        image1 = image1.reshape((1, image1.shape[0], image1.shape[1], image1.shape[2]))
        image2 = image2.reshape((1, image2.shape[0], image2.shape[1], image2.shape[2]))
        # prepare the image for the VGG model
        image1 = preprocess_input(image1)
        image2 = preprocess_input(image2)
        # get features
        feature1 = self.model.predict(image1, verbose=0).reshape((4096))
        feature2 = self.model.predict(image2, verbose=0).reshape((4096))

        cos_sim = np.dot(feature1,feature2)/(np.linalg.norm(feature1)*np.linalg.norm(feature1))
        cos_dist = 1-cos_sim
        return cos_dist

###################

def test_metric(metric,testim,testset,nrows):

    sorted_indexes = metric.order_images(testim,testset)

    sim = [testset[i] for i in sorted_indexes[:nrows*nrows]]

    imdim = int(1000/nrows)

    background = Image.new('RGB', (imdim*nrows, imdim*nrows), (255, 255, 255))
    #background2 = Image.new('RGB', (testsize[0]*nrows, testsize[1]*nrows), (255, 255, 255))
    #background3 = Image.new('RGB', (imdim*nrows, imdim*nrows), (255, 255, 255))


    for i in tqdm(range(len(sim))):
        offset = ((i%nrows)*imdim,int(i/nrows)*imdim)
        background.paste(Image.open(sim[i]).resize((imdim,imdim)), offset)

    # for i in tqdm(range(len(sim))):
    #     offset = ((i%nrows)*testsize[0],int(i/nrows)*testsize[1])
    #     background2.paste(Image.open(sim[i]).resize(testsize), offset)
    #
    # for i in tqdm(range(len(sim))):
    #     offset = ((i%nrows)*imdim,int(i/nrows)*imdim)
    #     background3.paste(Image.fromarray(diff[i].astype('uint8'),mode='RGB').convert('RGB').resize((imdim,imdim)), offset)

    Image.open(testim).show()
    background.show()
    # background2.resize((imdim*nrows, imdim*nrows)).show()
    # background3.show()

def display_from_set(set,nrows):

    sim = [set[i] for i in range(nrows**2)]
    imdim = int(1000 / nrows)
    background = Image.new('RGB', (imdim * nrows, imdim * nrows), (255, 255, 255))

    for i in tqdm(range(len(sim))):
        offset = ((i%nrows)*imdim,int(i/nrows)*imdim)
        background.paste(Image.open(sim[i]).resize((imdim,imdim)), offset)

    background.show()


###################

def combine_metrics(mlist,testim,testset,weights=0):

    arg_metalist = np.zeros(len(testset))

    for i,metric in enumerate(mlist):
        multiplier = 1
        if weights:
            multiplier *= weights[i]
        arg_metalist += weights*np.array(np.argsort(metric.order_images(testim,testset)))

    pkl.dump(np.argsort(arg_metalist),open('Messing(delete)/combined.pkl','wb'))
    return np.argsort(arg_metalist)



if __name__ == '__main__':
    testsize = (20,20)
    imset = ['data/playlists/best2_rscale/'+i for i in os.listdir('data/playlists/best2_rscale') if 'pic' in i]
    gs = grid_dist(testsize)
    vg = vgg_dist()

    nrows = 8
    testim = imset[413]
    testset = imset

    sorted = combine_metrics([gs,vg],testim,testset)
    Image.open(testim).show()
    display_from_set([testset[i] for i in sorted][:nrows**2],nrows)

    #test_metric(vg,imset[329],imset,nrows)