"""
Filters Module
Provides image processing utilities including adding a frame and applying the Kuwahara filter.
"""

from PIL import Image
import numpy as np
import copy

def add_frame(img):
    """
    Adds a 2-pixel frame to an image by extending edge pixels.

    Parameters:
        img (PIL.Image): Original image.

    Returns:
        np.ndarray: Image with added frame.
    """
    image = np.array(img)
    height, width, channels = image.shape
    framed_image = np.zeros((height + 4, width + 4, channels), dtype=np.uint8)
    framed_image[2:height+2, 2:width+2] = image

    for c in range(channels):
        framed_image[0:2, 2:width+2, c] = image[0, :, c]
        framed_image[height+2:height+4, 2:width+2, c] = image[height-1, :, c]
        framed_image[:, 0:2, c] = framed_image[:, 2:4, c]
        framed_image[:, width+2:width+4, c] = framed_image[:, width:width+2, c]

    return framed_image

def kuwahara(image):
    """
    Applies Kuwahara filter to an image to reduce noise while preserving edges.

    Parameters:
        image (PIL.Image): Original image.

    Returns:
        np.ndarray: Filtered image.
    """
    k = add_frame(image)
    k_copy = copy.deepcopy(k)
    height, width, channels = k.shape

    for i in range(2, height-2):
        for j in range(2, width-2):
            a = k[i-2:i+1, j-2:j+1]
            b = k[i-2:i+1, j-1:j+2]
            c = k[i-2:i+1, j:j+3]
            d = k[i-1:i+2, j-2:j+3]

            vars_ = [np.var(a, axis=(0,1), ddof=1),
                     np.var(b, axis=(0,1), ddof=1),
                     np.var(c, axis=(0,1), ddof=1),
                     np.var(d, axis=(0,1), ddof=1)]

            min_var_index = np.argmin(vars_)
            if min_var_index == 0:
                mean_val = np.mean(a, axis=(0,1))
            elif min_var_index == 1:
                mean_val = np.mean(b, axis=(0,1))
            elif min_var_index == 2:
                mean_val = np.mean(c, axis=(0,1))
            else:
                mean_val = np.mean(d, axis=(0,1))

            k_copy[i-1, j-1] = mean_val

    return k_copy
