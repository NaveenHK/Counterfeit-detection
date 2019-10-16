import os
import numpy as np
import tensorflow as tf
import vgg19
from sklearn.decomposition import PCA
import pickle
import skimage
import skimage.io
import skimage.transform
from PIL import Image
from sklearn import random_projection
import time
import random
import sys

# parameters
batch_size = 100
set_num = 100000
# s = int(sys.argv[1])
icon_location = "sample_icons/"
store_location = "data/"
LOG_FILE = open("log.txt", "a")
os.system("mkdir " + store_location + "cont_sty1")

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
    print(str(TMP_STRING))
    LOG_FILE.write(str(TMP_STRING))
    LOG_FILE.write("\n")
    LOG_FILE.flush()


######################## Pipe line  ####################

# create tf model
with tf.device('/cpu'):
    vgg = vgg19.Vgg19("vgg19.npy")
    tf_images = tf.placeholder("float", [batch_size, 224, 224, 3])
    # tf_rp_matrix = tf.placeholder("float", [512 * 512, 4096])
    # tf_rp_matrix = tf.SparseTensor(indices, coo.data, coo.shape)
    vgg.build(tf_images)
    tf_conv5_1 = vgg.conv5_1
    tf_features = tf.reshape(tf_conv5_1, [batch_size, 196, 512]) / 196 / 512
    tf_style = tf.matmul(tf.transpose(tf_features, [0, 2, 1]), tf_features)
    # tf_style = tf.reshape(tf.matmul(tf.transpose(tf_features, [0, 2, 1]), tf_features), [batch_size_all, -1])
    # tf_style = tf.transpose(tf.sparse_tensor_dense_matmul(tf_rp_matrix, tf_style1))
    tf_content = vgg.fc7


# create a new random projection matrix for each batch
# transformer = random_projection.SparseRandomProjection(n_components=4096)
# use the same random projection matrix for each bach
transformer = pickle.load(open("transformer.pickle", "rb"))
list_icons_all = np.load("../icon_list.npy")

with tf.Session() as sess:

    for s in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        list_icons = list_icons_all[s * set_num:(s + 1) * set_num]
        # list_icons = np.load("../icon_list.npy")[162000:170000]
        Big_file = np.ndarray((set_num, 2 + 4096 * 2), dtype=object)
        for batch in range(int(len(list_icons) / batch_size)):
            start_time = time.time()

            batch_icons = np.ndarray((batch_size, 224, 224, 3))
            c = 0
            for icon in list_icons[batch * batch_size:(batch + 1) * batch_size]:
                try:
                    np_image = get_img([icon])
                except Exception as e:
                    np_image = np.zeros((224, 224, 3))
                    logEntry(icon)

                batch_icons[c] = np_image
                c += 1

            np_style, np_content = sess.run([tf_style, tf_content], feed_dict={tf_images: batch_icons})
            Big_file[batch * batch_size:(batch + 1) * batch_size, 0] = list_icons[batch * batch_size:(batch + 1) * batch_size]
            Big_file[batch * batch_size:(batch + 1) * batch_size, 2:4098] = np_content
            style_mat = np.ndarray((batch_size, 256 * 513), dtype=object)
            for i in range(batch_size):
                np_style1 = np_style[i][np.triu_indices(512)]
                style_mat[i] = np_style1

            rp_mat = transformer.transform(style_mat)
            Big_file[batch * batch_size:(batch + 1) * batch_size, 4098:] = rp_mat
            end_time = time.time()
            logEntry(str(s) + "\t" + str(batch) + "\t" + str(end_time - start_time) + "\t" + str(np.where(list_icons_all == icon)))

        # pickle.dump(transformer, open("transformer.pickle", "wb"))
        np.save(store_location + "cont_sty1/Big_file_" + str(s) + ".npy", Big_file)


# Big_file = np.ndarray((set_num, 2 + 4096 * 2), dtype=object)
# style_mat = np.ndarray((set_num, 256 * 513), dtype=object)
# with tf.Session() as sess:
#     c = 0
#     for icon in list_icons:

#         np_image = get_img([icon])

#         np_style, np_content = sess.run([tf_style, tf_content], feed_dict={tf_images: np_image})
#         Big_file[c, 0] = icon
#         Big_file[c, 2:4098] = np_content

#         np_style1 = np_style[0][np.triu_indices(512)]
#         style_mat[c] = np_style1

#         c += 1
#         print(c)

#     rp_mat = transformer.fit_transform(style_mat)
#     Big_file[:, 4098:] = rp_mat

#     np.save(store_location + "cont_sty1/Big_file_" + "0" + ".npy", Big_file)

#     pickle.dump(transformer, open("transformer.pickle", "wb"))


# /srv/suranga/images/767/com.wallpaperforiphone6plus.bosubay.jpg
