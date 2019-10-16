import os
import numpy as np
import tensorflow as tf
import vgg19
import scipy.io
import scipy.misc
import scipy.spatial.distance
import time
import math
from sklearn.decomposition import PCA
import random
import time
import pickle
import sys
import skimage
import skimage.io
import skimage.transform
from PIL import Image
from sklearn import random_projection

# parameters
batch_size_all = 1
icon_location = "sample_icons/"
store_location = "data/"
os.system("mkdir " + store_location + "/cont_sty1")

############################ UDF #######################

# returns image of shape [224, 224, 3]
# [height, width, depth]


def load_image(path):
    # load image
    # img = skimage.io.imread(path)
    img = np.array(Image.open(path).convert("RGB"))

    img = img / 255.0
    assert (0 <= img).all() and (img <= 1.0).all()
    # print(img.shape)
    # we crop image from center
    # short_edge = min(img.shape[:2])
    # yy = int((img.shape[0] - short_edge) / 2)
    # xx = int((img.shape[1] - short_edge) / 2)
    # crop_img = img[yy: yy + short_edge, xx: xx + short_edge]
    # resize to 224, 224
    resized_img = skimage.transform.resize(img, (224, 224), mode="constant")
    # print(resized_img.shape)
    return resized_img


def get_img(image_loc):
    images = np.ndarray(shape=(len(image_loc), 224, 224, 3))
    i = 0
    for img in image_loc:
        images[i] = load_image(img)
        i += 1
    return images


def get_img1(main_dir, image_name):
    images = np.ndarray(shape=(len(image_name), 224, 224, 3))
    i = 0
    for img in image_name:
        images[i] = load_image(main_dir + img)
        i += 1
    return images


def logEntry(TMP_STRING):
    LOG_FILE.write(str(TMP_STRING))
    LOG_FILE.write("\n")
    LOG_FILE.flush()
    print(str(TMP_STRING))

######################## Pipe line  ####################

# create tf model
with tf.device('/gpu'):
    vgg = vgg19.Vgg19("vgg19.npy")
    tf_images = tf.placeholder("float", [batch_size_all, 224, 224, 3])
    # tf_rp_matrix = tf.placeholder("float", [512 * 512, 4096])
    # tf_rp_matrix = tf.SparseTensor(indices, coo.data, coo.shape)
    vgg.build(tf_images)
    tf_conv5_1 = vgg.conv5_1
    tf_features = tf.reshape(tf_conv5_1, [batch_size_all, 196, 512]) / 196 / 512
    tf_style = tf.matmul(tf.transpose(tf_features, [0, 2, 1]), tf_features)
    # tf_style = tf.reshape(tf.matmul(tf.transpose(tf_features, [0, 2, 1]), tf_features), [batch_size_all, -1])
    # tf_style = tf.transpose(tf.sparse_tensor_dense_matmul(tf_rp_matrix, tf_style1))
    tf_content = vgg.fc7


dir_num = os.listdir(icon_location)[int(sys.argv[1]):int(sys.argv[2])]

# create a new random projection matrix for each batch
# transformer = random_projection.SparseRandomProjection(n_components=4096)
# use the same random projection matrix for each bach
transformer = pickle.load(open("transformer.pickle", "rb"))


with tf.Session() as sess:
    for dir_1 in dir_num:
        dir_2 = icon_location + str(dir_1)
        icons_name = os.listdir(dir_2)
        Big_file = np.ndarray((len(icons_name), 2 + 4096 * 2), dtype=object)

        counter = 0
        style_mat = np.ndarray((len(icons_name), 256 * 513), dtype=object)
        for i in icons_name:
            print(counter)
            np_image = get_img([dir_2 + "/" + i])
            np_style, np_content = sess.run([tf_style, tf_content], feed_dict={tf_images: np_image})
            np_style1 = np_style[0][np.triu_indices(512)]
            Big_file[counter, 0] = dir_2 + "/" + i
            Big_file[counter, 2:4098] = np_content
            style_mat[counter] = np_style1
            counter += 1

        # rp_mat = transformer.fit_transform(style_mat)
        rp_mat = transformer.transform(style_mat)
        Big_file[:, 4098:] = rp_mat
        np.save(store_location + "cont_sty1/Big_file_" + dir_1 + ".npy", Big_file)


# pickle.dump(transformer, open("transformer.pickle", "wb"))
