import os
import numpy as np
from sklearn.decomposition import PCA
import skimage
import skimage.io
import skimage.transform
from PIL import Image
from sklearn import random_projection
import cv2


# parameters
batch_size_all = 1
batch_size_quary = 1
best_simalr = 10

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


main_dir = "sample_icons/"
dir_num = os.listdir(main_dir)[0:1]

sift = cv2.SIFT()

for dir_1 in dir_num:
    dir_2 = main_dir + str(dir_1)
    icons_name = os.listdir(dir_2)
    Big_file = []

    counter = 0
    for i in icons_name:
        print(counter)
        np_image = get_img([dir_2 + "/" + i])
        gray_p = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
        (kps_p, descs_p) = sift.detectAndCompute(gray_p, None)
        Big_file.append([dir_2 + "/" + i, descs_p])
        counter += 1

    np.save("data/sift/Big_file_" + dir_1 + ".npy", Big_file)
