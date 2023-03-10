import numpy as np
import helpFunctions as hf
import math
import matplotlib.pyplot as plt

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

# compute parameters
## returns covariance matrix, inverse of the covariance matrix and factor
def params(multiIm):
    cov = covariance(multiIm)
    det = np.linalg.det(cov)
    fact = 1/(2*math.pi*math.sqrt(det))

    return cov, np.linalg.inv(cov), fact



# compute multivariate gaussian in general for mu and parameters

def f(x,mu,params):
    cov, inv, fact = params
    mat = np.dot(np.transpose(x-mu),inv)
    mat = np.dot(mat,(x-mu))
    return fact*math.exp(-1/2 * mat)


def Gauss(x,mu,s):
    return 1/(s*math.sqrt(2*math.pi)) * np.exp(-1/2 * 1/s**2 * (x-mu)**2)


# solve inequality 
def solveInter(func1,func2,incr,approx):
    i = 0
    r = True
    x = approx
    result = 0
    while r:
        set1 = func1(x)
        set2 = func2(x)
        if (set1 - set2) <= 0:
            r = True
            i += 1
        else:
            r = False
            result = x
        x += incr
    return result

# compute thresholds
def thresholds(multiIm,mu_meat,mu_fat):
    bands = len(multiIm[0,0,:])
    thresholds = []
    for band in range(bands):
        s = np.std(multiIm[:,:,band])
        mu_1 = mu_meat[band]
        mu_2 = mu_fat[band] 

        def func1(x):
            return Gauss(x,mu_1,s)

        def func2(x):
            return Gauss(x,mu_2,s)

        thresholds.append(solveInter(func1,func2,0.001,mu_1))
    return thresholds

# compute thresholds directly for a day
def thresholdDay(day, dirIn):
    # load images
    multiIm, annotationIm = hf.loadMulti(f'multispectral_day{day}.mat' , f'annotation_day{day}.png', dirIn)

    bands = len(multiIm[0,0,:])
    thresholds = []

    mu_meat,mu_fat = means(multiIm,annotationIm)

    for band in range(bands):
        s = np.std(multiIm[:,:,band])
        mu_1 = mu_meat[band]
        mu_2 = mu_fat[band] 

        def func1(x):
            return Gauss(x,mu_1,s)

        def func2(x):
            return Gauss(x,mu_2,s)

        thresholds.append(solveInter(func1,func2,0.001,mu_1))
    return thresholds

# function to compute error rates for the simple threshold 
def errorSimple(multiIm,annotationIm,thresholds):
    # computing error 
    # fat pixels
    ann = 1
    [clPixFat, rFat, cFat] = hf.getPix(multiIm,annotationIm[:,:,ann])
    # meat pixels
    ann = 2
    [clPixMeat, rMeat, cMeat] = hf.getPix(multiIm,annotationIm[:,:,ann])

    fatPixels = len(rFat)
    meatPixels = len(rMeat)

    # count classified pixels
    bandErrorFat = []
    bandErrorMeat = []

    # the function checkSimple returns 0 for meat and 1 for fat
    for band in range(len(clPixMeat[0])):
        t = thresholds[band]
        fatsClassification = 0
        for i in range(fatPixels):
            f = multiIm[rFat[i],cFat[i],band]
            fatsClassification += (f>t)
        meatClassification = 0
        for i in range(meatPixels):
            m = multiIm[rMeat[i],cMeat[i],band]
            meatClassification += (m<t)
        bandErrorFat.append(1-fatsClassification/fatPixels)
        bandErrorMeat.append(1-meatClassification/meatPixels)

    return bandErrorFat,bandErrorMeat

# determine the spectral band with the best discriminative properties for meat and fat
def findBestBand(bandErrorFat,bandErrorMeat):
    dist = np.sqrt(np.array(bandErrorMeat)**2 + np.array(bandErrorFat)**2)
    ind = np.where(dist == min(dist))[0][0]
    return ind

# show the best image for simple threshold method

def showClassificationSimple(multiIm,annotationIm,bandErrorFat,bandErrorMeat,thresholds):
    # classify image for salami on day 1 - band 2
    ind = findBestBand(bandErrorFat,bandErrorMeat)
    image = multiIm[:,:,ind]

    background = annotationIm[:,:,0]
    fatLayer = np.zeros(image.shape)
    meatLayer = np.zeros(image.shape)

    x,y = image.shape

    t = thresholds[ind]

    colours = [[[] for i in range(x)] for j in range(y)]
    blue = [0, 0, 255] 
    green = [0, 255, 0]
    red = [255, 0, 0]



    for i in range(x):
        for j in range(y):
            fatLayer[i][j] = (multiIm[i,j,ind] > t)
            meatLayer[i][j] = multiIm[i,j,ind] < t
            if(not background[i][j]):
                colours[i][j] = blue
            elif(fatLayer[i][j]):
                # fat
                colours[i][j] = green
            else:
                # meat
                colours[i][j] = red

    plt.imshow(colours)
    plt.title("Colour annotation")
    plt.show()



# compute simple error rates for day x
def errorRatesDay(day,dirIn,t):
    # load images
    multiIm, annotationIm = hf.loadMulti(f'multispectral_day{day}.mat' , f'annotation_day{day}.png', dirIn)

    # compute error rates
    bandErrorFat,bandErrorMeat = errorSimple(multiIm,annotationIm,t)

    # determine best spectral band
    ind = findBestBand(bandErrorFat,bandErrorMeat)

    print(f"best spectral band is {ind}")

    # return error rates of that band
    return (bandErrorFat[ind]+bandErrorMeat[ind])/2


def errorRates(training,dirIn):
    t = thresholdDay(training,dirIn)
    days = ['01','06','13','20','28']
    days.remove(training)
    print(days)

    errorRates = []
    for day in days:
        error = errorRatesDay(day,dirIn,t)
        print(day,error)
        errorRates.append(round(error,3))
    
    return errorRates

# annotation plot
def plotSimpleThresholds(multiIm,annotationIm,thresh,ind, title):
    # classify image for salami on day 1 - band 2
    image = multiIm[:,:,ind]

    background = annotationIm[:,:,0]
    fatLayer = np.zeros(image.shape)
    meatLayer = np.zeros(image.shape)

    x,y = image.shape

    colours = [[[] for i in range(x)] for j in range(y)]
    blue = [0, 0, 255] 
    green = [0, 255, 0]
    red = [255, 0, 0]

    t = thresh[ind]

    for i in range(x):
        for j in range(y):
            fatLayer[i][j] = multiIm[i,j,ind] > t
            meatLayer[i][j] = multiIm[i,j,ind] < t
            if(not background[i][j]):
                colours[i][j] = blue
            elif(fatLayer[i][j]):
                # fat
                colours[i][j] = green
            else:
                # meat
                colours[i][j] = red
    plt.imshow(colours)
    title = f"Annotation Simple - {title}"
    plt.title(title)
    plt.show()
    figname = title.replace(" ","_")
    plt.imsave(f"{figname}.png",colours)

def plotSimple(day,training,dirIn):
    # load training
    multiIm, annotationIm = hf.loadMulti(f'multispectral_day{training}.mat' , f'annotation_day{training}.png', dirIn)
    # compute thresholds
    thresh = thresholdDay(training,dirIn)
    # compute band errors
    bandErrorFat,bandErrorMeat = errorSimple(multiIm,annotationIm,thresh)
    # compute best spectral band
    ind = findBestBand(bandErrorFat,bandErrorMeat)
    
    # load test
    multiIm, annotationIm = hf.loadMulti(f'multispectral_day{day}.mat' , f'annotation_day{day}.png', dirIn)
    # plot 
    title = f"test day {day}-training day {training}"
    plotSimpleThresholds(multiIm,annotationIm,thresh,ind,title)
    






## Linear Discriminant model

# linear discriminant function
def linearDisc(x,inv,mu,p=None):
    first = np.dot(np.dot(np.transpose(x),inv),mu)
    second = -1/2*np.dot(np.dot(np.transpose(mu),inv),mu)
    if(p == None):
        third = 0
    else:
        third = np.log(p)
    return first+second+third


# function to compute error rates for the linear discriminant
def errorLinDisc(multiIm,annotationIm,params,p):
    # computing error 
    # fat pixels
    ann = 1
    [clPixFat, rFat, cFat] = hf.getPix(multiIm,annotationIm[:,:,ann])
    # meat pixels
    ann = 2
    [clPixMeat, rMeat, cMeat] = hf.getPix(multiIm,annotationIm[:,:,ann])

    fatPixels = len(rFat)
    meatPixels = len(rMeat)

    # count classified pixels
    bandErrorFat = []
    bandErrorMeat = []

    # get the parameters
    cov, inv, fact = params

    # get means
    mu_fat,mu_meat = means(multiIm,annotationIm)

    if p == None:
        p_meat = p
    else :
        p_meat = 1-p

    # the function checkSimple returns 0 for meat and 1 for fat
    fatsClassification = 0
    for i in range(fatPixels):
        f = multiIm[rFat[i],cFat[i],:]
        fatsClassification += (linearDisc(f,inv,mu_meat,p_meat) < linearDisc(f,inv,mu_fat,p))
    meatClassification = 0
    for i in range(meatPixels):
        m = multiIm[rMeat[i],cMeat[i],:]
        meatClassification += (linearDisc(f,inv,mu_meat,p_meat) < linearDisc(f,inv,mu_fat,p))
    bandErrorFat = (1-fatsClassification/fatPixels)
    bandErrorMeat = (1-meatClassification/meatPixels)

    return bandErrorFat,bandErrorMeat


# error rates for trained linear discriminant model for a specific day
def errorRatesDayLinDisc(day, dirIn, params, p):
    # load images
    multiIm, annotationIm = hf.loadMulti(f'multispectral_day{day}.mat' , f'annotation_day{day}.png', dirIn)

    # compute error rates
    bandErrorFat,bandErrorMeat = errorLinDisc(multiIm,annotationIm,params,p)
    # return error rates of that band
    return (bandErrorFat+bandErrorMeat)/2

# error rates for different training days for model 2
def errorRatesLinDisc(training,dirIn,p):
    days = ['01','06','13','20','28']
    days.remove(training)
    print(days)

    # load images
    multiIm, annotationIm = hf.loadMulti(f'multispectral_day{training}.mat' , f'annotation_day{training}.png', dirIn)
    # compute parameters
    para = params(multiIm)

    errorRates = []
    for day in days:
        error = errorRatesDayLinDisc(day,dirIn,para,p)
        print(day,error)
        errorRates.append(round(error,3))
    
    return errorRates


# annotation plot
def plotLinDiscPara(multiIm,annotationIm,inv,mu_meat,mu_fat,p, title):
    # classify image for salami on day 1 - band 2
    image = multiIm[:,:,0]

    

    background = annotationIm[:,:,0]
    fatLayer = np.zeros(image.shape)
    meatLayer = np.zeros(image.shape)

    x,y = image.shape

    colours = [[[] for i in range(x)] for j in range(y)]
    blue = [0, 0, 255] 
    green = [0, 255, 0]
    red = [255, 0, 0]

    if p == None:
        p_meat = None
    else:
        p_meat = 1 - p

    for i in range(x):
        for j in range(y):
            fatLayer[i][j] = (linearDisc(multiIm[i,j,:],inv,mu_meat,p_meat) < linearDisc(multiIm[i,j,:],inv,mu_fat,p))
            meatLayer[i][j] = not fatLayer[i][j]
            if(not background[i][j]):
                colours[i][j] = blue
            elif(fatLayer[i][j]):
                # fat
                colours[i][j] = green
            else:
                # meat
                colours[i][j] = red
    plt.imshow(colours)
    title = f"Annotation Lin Disc - {title}"
    plt.title(title)
    plt.show()
    figname = title.replace(" ","_")
    plt.imsave(f"{figname}.png",colours)

def plotLinDisc(day,training,dirIn,p):
    # load training
    multiIm, annotationIm = hf.loadMulti(f'multispectral_day{training}.mat' , f'annotation_day{training}.png', dirIn)
    # compute thresholds
    cov,inv,fact = params(multiIm)
    # compute band errors
    mu_fat,mu_meat = means(multiIm,annotationIm)
    
    # load test
    multiIm, annotationIm = hf.loadMulti(f'multispectral_day{day}.mat' , f'annotation_day{day}.png', dirIn)
    # plot 
    title = f"test day {day}-training day {training}"
    if p != None:
        title += f" p={p}"
    plotLinDiscPara(multiIm,annotationIm,inv,mu_meat,mu_fat,p,title)
    
