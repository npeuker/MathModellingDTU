import numpy as np
import helpFunctions as hf

# compute covariance matrix from images
def covariance(multiIm):
    # array of multiple means - means for each spectral band
    mumu = []
    for i in range(len(multiIm[0,0,:])):
        mumu.append(np.mean(multiIm[:,:,i]))

    #xa : is the pixel value in dimension a
    #xb : is the pixel value in dimension b

    # covariance assuming equal for both classes
    # number of spectral bands
    n = len(mumu)
    # number of pixels per spectral band
    m = len(multiIm[:,0,0])
    cov = np.zeros(shape=(n,n))

    for a in range(n):
        for b in range(n):
            cov[a][b] = 1/(m**2 - 1) * sum((multiIm[:,:,a].flatten()-mumu[a])*(multiIm[:,:,b].flatten()-mumu[b]))

    return cov


# compute means in meat and fat pixels
def means(multiIm,annotationIm):
    ann = 1
    [clPix, r, c] = hf.getPix(multiIm,annotationIm[:,:,ann])
    # mean vectors
    mu_fat = []
    n = len(clPix[0])
    m_fat = len(clPix[:,0])
    for i in range(n):
        mu_fat.append(np.mean(clPix[:,i]))

    ann = 2
    [clPix, r, c] = hf.getPix(multiIm,annotationIm[:,:,ann])
    mu_meat = []
    m_meat = len(clPix[:,0])
    for i in range(n):
        mu_meat.append(np.mean(clPix[:,i]))

    return mu_fat,mu_meat
