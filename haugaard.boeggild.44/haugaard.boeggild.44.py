# -*- coding: utf-8 -*-
from __future__ import division
import math

import matplotlib.pyplot as plt

from csvImageRead import csvImageRead

__author__ = "Martin Simon Haugaard, Magnus Egede Bøggild"


def gradient(V):
    """
    Calculates the gradient from a given image
    :param V:
    :return:
    """
    N = len(V)
    imagelistdx = [[0 for _ in xrange(N)] for _ in xrange(N)]
    imagelistdy = [[0 for _ in xrange(N)] for _ in xrange(N)]
    for i in range(N):
        for j in range(N):
            if j < (N-1):
                (imagelistdx[i])[j] = (V[i])[j+1] - (V[i])[j]
            else:
                (imagelistdx[i])[j] = 0.0
    for i in range(N):
        for j in range(N):
            if i < (N-1):
               (imagelistdy[i])[j] = (V[i+1])[j] - (V[i])[j]
            else:
               (imagelistdy[i])[j] = 0.0
    return imagelistdy, imagelistdx

def gradNorm(V1, V2):
    """
    Takes two gradient images and returns the normalised image from the two input images
    :param V1:
    :param V2:
    :return:
    """
    N = len(V1)
    norm = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            (norm[i])[j] = math.sqrt(((V1[i])[j])**2.0 + ((V2[i])[j])**2.0)
    return norm


def divergence(V1, V2):
    """
    Takes two images, and returns the divergence from the two images.
    :param V1:
    :param V2:
    :return:
    """
    N = len(V1)
    div = [[0 for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if i > 0 and i < N-1:
                (div[i])[j] += (V1[i])[j]-(V1[i-1])[j]
            elif i == 0:
                (div[i])[j] += (V1[i])[j]
            else:
                (div[i])[j] += -(V1[i-1])[j]
#Mossa: Fjern disse
#    for i in range(N):
#        for j in range(N):
            if j > 0 and j < N-1:
                (div[i])[j] += (V2[i])[j]-(V2[i])[j-1]
            elif j == 0:
                (div[i])[j] += (V2[i])[j]
            elif j == N-1:
                (div[i])[j] += -(V2[i])[j-1]
    return div

if __name__ == "__main__":
# a)
    imageList = csvImageRead("Cameraman.csv")
    width = len(imageList)
    height = len(imageList[0])

    if width != height:
        print "The image provided is not of format NxN - beware!"
    # If no terminal print - then we're good to go.
    N = len(imageList)
    for i in range(N):
        for j in range(N):
            if imageList[i][j] < 0 or imageList[i][j] > 255:
                print "Image pixels (%d, %d) is not between [0, 255] - beware!" % (i, j)
    plt.figure("CameraMan - clean")
    plt.imshow(imageList, cmap="Greys_r")
    plt.show()
# b)
    img_x, img_y = gradient(imageList)
    plt.figure("ImageListDx")
    plt.imshow(img_x, cmap="Greys_r")
    plt.show()
    plt.figure("ImageListDy")
    plt.imshow(img_y, cmap="Greys_r")
    plt.show()
    # We find these similar to the examples provided
# c)
    norm = gradNorm(img_x, img_y)
    plt.figure("Normalised CameraMan")
    plt.imshow(norm, cmap="Greys_r")
    plt.show()
# d)
    div = divergence(img_x, img_y)
    plt.figure("Divergence CameraMan")
    plt.imshow(div, cmap="Greys_r")
    plt.show()
    # What are the properties of divergence?
    # It finds the contracts between the two given images.
    # Meaning it will highlight areas in the images, where neighboring pixels differ greatly,
    # like a white line in the middle of a black coat, a reflections,
    # or the outlines of a person black versus a white backdrop.
# e)
    # The following section is split into several lesser parts:
# 1)
    y = csvImageRead("CameramanNoisy.csv")

#2)
    my_tau = 0.248
    my_lambda = 0.08

#3)
    w1 = [[0.0 for _ in range(N)] for _ in range(N)]
    w2 = [[0.0 for _ in range(N)] for _ in range(N)]
    divW = divergence(w1, w2)

#4)
    ylambda = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            (ylambda[i])[j] = (y[i])[j] * my_lambda
#5)
    iterations = []
    for _ in range(20): # Should be 200, but that takes a while
        dVx = [[0 for _ in range(N)] for _ in range(N)]
        dVy = [[0 for _ in range(N)] for _ in range(N)]
#5.1 - calculate dVx, dVy
        dVx_divW, dVy_divW = gradient(divW)
        dVx_lambda, dVy_lambda = gradient(ylambda)
        for i in range(N):
            for j in range(N):
                (dVx[i])[j] = (dVx_lambda[i])[j] - (dVx_divW[i])[j]
                (dVy[i])[j] = (dVy_lambda[i])[j] - (dVy_divW[i])[j]
# 5.2 - calculate dWnorm, form dVx and dVy
        dWnorm = gradNorm(dVx, dVy)
# 5.3 - make descent step on w1 and w2, using dVx, dVy and tau
# Then normalise w1, w2 by diving their values by "1 + dWnorm*tau"
        for i in range(N):
            for j in range(N):
#Mossa: Det her er hvad der er i vejen
                (w1[i])[j] -= my_tau*(dVx[i])[j]
                (w2[i])[j] -= my_tau*(dVy[i])[j]
        # Normalizing
        for i in range(N):
            for j in range(N):
                (w1[i])[j] /= (1.0+(dWnorm[i])[j]*my_tau)
                (w2[i])[j] /= (1.0+(dWnorm[i])[j]*my_tau)
# We have a suspicion that the code above does not work properly, this is because it's the critical iteration part,
# but as shown later, it seems like each iteration doesn't improve much, if any on the noise of the image.

# 5.4 - update divW, using w1 and w2
        divW = divergence(w1, w2)
# 5.5 - calculate the value of the image for each iteration, and save as a list
        value = 0
        for i in range(N):
            for j in range(N):
#Mossa: Her var der også en fejl...
                value += ((ylambda[i])[j] - (divW[i])[j])**2
        value = (value)/2.0
        iterations.append(value)
        # Visual pointer as the end of each iteration.
        print ".",

# 6 - Iteration done - time to plot:
    X = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            # Calculate X
            (X[i])[j] = (y[i])[j] - 1/my_lambda * (divW[i])[j]
    plt.figure(1)
    # Plotting the new image, X
    plt.subplot(211)
    plt.imshow(X, cmap="Greys_r")
    plt.subplot(212)
    # Plot the value for each iteration
    plt.plot(iterations)
    plt.show()

#f)
    # see e) 5.5 in the code above for implementation,
    # Does it behave as expected?!
    # Sadly, no,
    # We expected the image to improve for each iteration, meaning that the value calculated in step e) 5.5 should start
    # off high, and then become lower for each new iteration, until an "optimal" noise reduced image is reached,
    # where each new iteration, neither improves on, or adds more noise to the image.
    # This does not happen in our code however, and instead we see the value more or less static, with each new
    # iteration either adding or removing some noise, but the overall impression is that our noise reduction is broken.

#g)
    # What effect does the size of lambda have on the algorithm in e)?
    # The size of lambda will determine how big an effect the noise found in the image, will effect the image itself.
    # If set too high, there will be almost no different, as the values on which the iterations are done, will be too
    # high for proper noise detection, the difference between the values will be relatively low compared to the values
    # themselves. If lambda is set too low however, every little change in value between neighboring pixels will seem
    # huge, and most of the image will be determined as noise, causing more harm than good.

    """
    As mentioned above, we did not manage to achieve any actual noise reduction in our image.
    This can be either due to faulty implementation, causing coordinates to miss, never actually fixing noise where
    needed, or it could be due to mistakes done in the iterations. Either way, we feel like we're very close to having
    a functional code. As all the helper functions declared before main seem to work properly, and we've implemented the
    iteration as best we could.
    """