from django.shortcuts import render
from django.conf import settings

import re
import base64
from PIL import Image

from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.externals import joblib
import numpy as np


# Upload the parameters for the classifier and PCA
clf = joblib.load(settings.BASE_DIR+'/ml/svm_clf.pkl')
pca = joblib.load(settings.BASE_DIR+'/ml/pca.pkl')

#---------------------------------------------------------------------------------------------
# Display the home page of the Machine Learning application.
#---------------------------------------------------------------------------------------------

def index(request):

    if request.method== 'POST':
        imgstr = request.POST['canvasData']
        # search the begining of the image in the string
        # and decode it to bytes.
        imgstr = re.search(r'base64,(.*)', imgstr).group(1)
        imgstr = base64.b64decode(imgstr)
        
        # Save the decoded picture as a png file.
        filePath = settings.BASE_DIR+"/media/ml_number.png"
        output = open(filePath, 'wb')
        output.write(imgstr)
        output.close()
        prediction = makePrediction(clf, pca)
        return render(request, 'ml/index.html', {'username': request.user.username, 'prediction':prediction})
    else :
        return render(request, 'ml/index.html', {'username': request.user.username})


# Use a trained classifier to predict the number drawn by the user
def makePrediction(clf, pca):
    pathToImage = settings.BASE_DIR+'/media/ml_number.png'
    image = Image.open(pathToImage, 'r')
    image = image.resize((28,28,),Image.ANTIALIAS) # I resize the image to fit in my classifier

    # the getdata method return RBG values so I only keep one of these values
    # the image was in black and white anyway.
    pixels = list(image.getdata())
    blackPixels, _ , _ , _   = zip(*pixels) 
    blackPixels = np.array(blackPixels)

    # I invert the values because my classifier was trained like that.
    whitePixels = 255 - blackPixels
    prediction = clf.predict( pca.transform(whitePixels))
    return prediction[0]
