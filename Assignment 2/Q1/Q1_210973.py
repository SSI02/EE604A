import cv2
import numpy as np
# from sklearn.cluster import KMeans


def solution(image_path):
    # Load the image
    image = cv2.imread(image_path)

    image = cv2.pyrMeanShiftFiltering(image , 30 , 40)

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Extract the hue channel
    hue_channel = image_hsv[:, :, 0]
    sat_channel = image_hsv[:, :, 1]
    value_channel = image_hsv[:, :, 2]

    test = hue_channel.copy()
    l,m = test.shape
    for i in range(0,l):
        for j in range(0,m):
            if(test[i][j]<=20 and sat_channel[i][j]>=100 and value_channel[i][j]>=100):
                test[i][j] = 255
            else:
                test[i][j] = 0
    test = np.stack([test, test, test], axis = -1)
    return test


    # cv2.imshow('hello' , solution('test/lava101.jpg'))
im1 = cv2.imread('test/lava101.jpg')
cv2.imshow('Hello' , im1)
cv2.imshow('hello' , solution('test/lava101.jpg'))
cv2.waitKey(0)
cv2.destroyAllWindows()