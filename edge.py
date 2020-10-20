import os
import time
import math
import numpy as np
from scipy.spatial import distance as dist
import cv2
from imutils import perspective
from imutils import contours
import imutils
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from skimage import feature, io
from skimage.color import rgb2gray, label2rgb
from skimage.filters import threshold_otsu, threshold_local
from skimage.measure import label, regionprops
from skimage import morphology


start = time.time()
def con_rm_L(array):
    for r_pixel in range(1088):
        for c_pixel in range(1920):
            ## remove the colorful connection
            if (array[r_pixel, c_pixel, 2] - array[r_pixel, c_pixel, 1] > 60) and (array[r_pixel, c_pixel, 2] - array[r_pixel, c_pixel, 0] > 10):
            # if array[r_pixel, c_pixel, 0] - array[r_pixel, c_pixel, 2] > 50: # RaspberryPi rev 1.3
                array[r_pixel, c_pixel] = [0,0,0]
    return array

def con_rm_R(array):
    for r_pixel in range(1088):
        for c_pixel in range(1920):
            ## remove the colorful connection
            if (array[r_pixel, c_pixel, 2] - array[r_pixel, c_pixel, 1] > 60) and (array[r_pixel, c_pixel, 2] - array[r_pixel, c_pixel, 0] > 10):
            # if array[r_pixel, c_pixel, 0] - array[r_pixel, c_pixel, 2] > 50: # RaspberryPi rev 1.3
                array[r_pixel, c_pixel] = [0,0,0]
    return array

def rgb2grey(array):
    gr = rgb2gray(array)
    gr = gr*256
    return gr

def thresholding(array):
    thresh_l = threshold_otsu(array)
    C_otsu = array > thresh_l
    C_otsu_1 = morphology.closing(C_otsu)
    C_otsu_2 = morphology.opening(C_otsu_1)
    return C_otsu_2.astype(np.uint8) * 255

def filter(array):
    num_pixel = []
    labels, num = label(array, connectivity=2, return_num=True)
    for idx, i in enumerate(range(1, num)):
        total_pixel = np.sum(labels == i)
        num_pixel.append(total_pixel)
    num_pixel_t = num_pixel.copy()
    num_pixel_t.sort()
    #print(num_pixel, num_pixel_t)
    needle_num = num_pixel_t[-2]
    needle_idx = num_pixel.index(needle_num) + 1
    #print(needle_idx)
    needle_img = (labels == needle_idx)
    return needle_img

def main():
    path = r'C:\Users\Z0046DDV\Desktop\KEM120 Mammogram Device Accessories Recognition\Night'
    i = 17
    C1 = io.imread(os.path.join(path,'L_{}.png'.format(i)), as_gray=False)
    #img_eq_L = exposure.equalize_hist(C1)
    C2 = io.imread(os.path.join(path,'R_{}.png'.format(i)), as_gray=False)
    #img_eq_R = exposure.equalize_hist(C2)
    ## Filter connection part
    C1 = con_rm_L(C1)
    io.imsave(os.path.join(path,"Lf.png"),C1)
    C2 = con_rm_R(C2)
    io.imsave(os.path.join(path,"Rf.png"),C2)

    ## RGB to Grey
    C1gr = rgb2grey(C1)
    io.imsave(os.path.join(path,"Lg.png"),C1gr)
    C2gr = rgb2grey(C2)
    io.imsave(os.path.join(path,"Rg.png"),C2gr)

    ## Otsu threshold
    C1_otsu = thresholding(C1gr)
    io.imsave(os.path.join(path,"L_thres.png"), C1_otsu)
    C2_otsu = thresholding(C2gr)
    io.imsave(os.path.join(path,"R_thres.png"), C2_otsu)

    ## remove everything, leave only the needle part
    l_needle_img = filter(C1_otsu)
    io.imsave(os.path.join(path, "L_Needle.png"), l_needle_img)

    r_needle_img = filter(C2_otsu)
    io.imsave(os.path.join(path, "R_Needle.png"), r_needle_img)


    end = time.time()
    print(end-start)
if __name__ == '__main__':
    main()