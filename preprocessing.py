import hashlib
import os
import numpy as np
from tqdm import tqdm
from PIL import Image, ExifTags
import pickle as pkl

file_ends = ['.jpg','.png','.bmp','.gif','.tiff','.jpeg','.jp2','.jif']

def hasher(f):
    h = hashlib.md5()
    with open(f,'rb') as afile:
        buf = open(f,'rb').read()
        h.update(buf)
    return h.hexdigest()

def preprocess_folder(name,current_loc,dest_loc,SHeight,SWidth,
                      downscale_dims=(5,5),from_root=True):

    os.mkdir(os.getcwd()+'\\'+dest_loc+'\\'+name)

    hashset = set()
    imnames = []

    downscale_features = {}

    imagelist = os.listdir(current_loc)
    for imagef in tqdm(imagelist):
        if imagef[-4:].lower() in file_ends or imagef[-5:].lower() in file_ends:
            imfile = current_loc+'/'+imagef
            hash = hasher(imfile)
            if hash not in hashset:

                im = Image.open(imfile)
                pre_ex = im._getexif()
                shape = ''

                if pre_ex != None:

                    exif = dict((ExifTags.TAGS[k], v) for k, v in pre_ex.items() if k in ExifTags.TAGS)


                    if exif['Orientation'] == 0 or exif['Orientation'] == 6:
                        im = im.rotate(270, expand=True)

                    elif exif['Orientation'] == 8:
                        im = im.rotate(90, expand=True)

                if im.size[0] > im.size[1]:
                    factor = im.size[1] / SHeight
                    imdims = (int(im.size[0] / factor), SHeight)
                    shape = 'wide'

                else:
                    factor = im.size[0] / SWidth
                    imdims = (SWidth, int(im.size[1] / factor))
                    shape = 'tall'

                oldf = imagef.split('.')[0]
                rscale_file = dest_loc + '/' + name+ '/' + oldf + '_rscale.png'
                im.thumbnail(imdims, Image.ANTIALIAS)

                im.save(rscale_file, 'png')
                hashset.add(hash)

                imstart = im.crop((0,0,SWidth,SHeight))

                if shape == 'wide':
                    imfinish = im.crop((im.size[0]-SWidth,0,im.size[0],SHeight))

                elif shape == 'tall':
                    imfinish = im.crop((9, im.size[1] - SHeight, SWidth, im.size[1]))

                splitw,splith = downscale_dims[0],downscale_dims[1]

                downscale_features[oldf] = (imagesplit(imstart,splitw,splith),imagesplit(imfinish,splitw,splith))
                imnames.append(oldf)

    pkl.dump(hashset,open(dest_loc+'/' + name+ '/hashset.pkl','wb'))
    pkl.dump(imnames,open(dest_loc+'/' + name+ '/imnames.pkl','wb'))
    pkl.dump(downscale_features,open(dest_loc+'/' + name+ '/downscale_features.pkl','wb'))


def imagesplit(imag,n1,n2):
    #new_arr = np.array([np.array(np.vsplit(np.hsplit(imarr, n)[i], n)) for i in range(n)]).reshape(!!!)
    im2 = np.array(imag.copy().resize((n1,n2)))
    return im2




def dif(thisfile,nextfile, features):
    sum = np.sum(np.abs(np.subtract(features[thisfile][0].astype(int),features[nextfile][1].astype(int))))
    return sum

def prob_dist(distranges):
    alist = [1/i for i in np.delete(np.arange(len(distranges)+1),0)]
    sum = np.sum(alist)#+len(sorted)
    alist = np.divide(alist,sum)
    return alist

def sample_dist(alist,distranges):
    # randx = np.random.random()
    # randy = np.random.random()
    # nearest_xi = (np.abs(randx))
    i = np.argmin(np.abs(alist - np.random.uniform(1, alist[-1])))

    return distranges[i]