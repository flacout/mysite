# # Predict a real Image
# The idea is to show what comes next down the pipeline once you have trained your classifier and obtain a good test score.  
# So I make prediction on numbers that I write myself, and save as png or jpeg files.  
# Then I feed the classifier with it and check the result.

# ## Train the classifier
# I use one of the classic PCA feature transform and a support vector classifier  
# It gives a good result on the test set.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from PIL import Image
from sklearn.externals import joblib

print( "training Classifier...........")
#labeled_images = pd.read_csv('ml/train.csv')
labeled_images = pd.read_csv('train.csv')
images = labeled_images.iloc[:,1:]
labels = labeled_images.iloc[:,:1]
train_images, test_images,train_labels, test_labels = train_test_split(images, labels, train_size=0.8, random_state=0)

pca = PCA(n_components=75, whiten=True)
train_pca = pca.fit_transform(train_images)
test_pca = pca.transform(test_images)

svc = SVC().fit(train_pca, train_labels)
print("train", svc.score(train_pca,train_labels))
print("test", svc.score(test_pca,test_labels))

# save classifier and PCA parameter to a file.
joblib.dump(svc, 'svm_clf.pkl')
joblib.dump(pca, 'pca.pkl')

# MAKE THE PREDICTION
def makePrediction():
    clf = joblib.load('svm_clf.pkl')
    pca = joblib.load('pca.pkl')
    pathToImage = '../media/ml_number.png'
    image = Image.open(pathToImage, 'r')
    image = image.resize((28,28,),Image.ANTIALIAS) # I resize the image to fit my classifier

    # the getdata method return RBG values so I only keep one of these values
    # the image was in black and white anyway
    pixels = list(image.getdata())
    blackPixels, _ , _ , _   = zip(*pixels) 
    blackPixels = np.array(blackPixels)

    # I invert the values because my classifier was trained like that.
    whitePixels = 255 - blackPixels
    prediction = clf.predict( pca.transform(whitePixels))
    print (prediction[0])
    return prediction[0]

if __name__=="__main__":
    makePrediction()
