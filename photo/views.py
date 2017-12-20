from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import re
import base64


#import of databade models
from .models import Picture
from .forms import UploadPhotoForm


#--------------------------------------------------------------------------------------------
# Page to upload a picture.
# And to visualize a picture.
# And to modifie the picture (make gray or red).
#--------------------------------------------------------------------------------------------

def index(request):

    if request.method== 'POST':
        # from Open Picture submit button.
        if 'select' in request.POST:
            picture_id = request.POST.get('photo_id',0)
            return displayPicture(request, picture_id)
        # from Delete submit button.
        elif 'delete' in request.POST:
            picture_id = request.POST.get('photo_id',0)
            return deletePicture(request, picture_id)

        # save picture after applying a filter.
        elif 'SaveModif' in request.POST:
            imgstr = request.POST['canvasData']
            photo_id = request.POST['photo_id']
            return updatePicture(request, imgstr, photo_id)

        # to save a picture uploaded by user.
        else: return savePictureForm(request)
    
    # No picture is open enter page to upload a new one.
    else : 
        form = UploadPhotoForm()
        context = { 'form': form, 
                    'username': request.user.username}
        return render(request, 'photo/index.html', context)

def displayPicture(request, picture_id):
    form = UploadPhotoForm()
    pictureToDraw = Picture.objects.filter(id=picture_id)
    extension = pictureToDraw[0].photo.url
    extension = extension.split('.')[-1]
    context = { 'form': form, 
                'username': request.user.username,
                'lastPicture': pictureToDraw[0],
                'extension':extension}
    return render(request, 'photo/index.html', context)

def deletePicture(request, picture_id):
    pictureToDelete = Picture.objects.filter(id=picture_id)
    filePath = settings.BASE_DIR+'/'+pictureToDelete[0].photo.url
    os.remove(filePath)
    pictureToDelete.delete()
    return redirect('/photo/allPhotos/')

def updatePicture(request, imgstr, photo_id):
    pictureToUpdate = Picture.objects.filter(id=photo_id)
    #pictureToUpdate.update(picture_name="new_name")
    filePath = settings.BASE_DIR+'/'+pictureToUpdate[0].photo.url
    os.remove(filePath)
    # search the begining of the image in the string
    imgstr = re.search(r'base64,(.*)', imgstr).group(1)
    imgstr = base64.b64decode(imgstr)
    output = open(filePath, 'wb')
    output.write(imgstr)
    output.close()
    return redirect('/photo/allPhotos/')

def savePictureForm(request):
    form = UploadPhotoForm(request.POST,request.FILES)
    if form.is_valid():
        pictureUploaded = form.save(commit=False)
        pictureUploaded.user_id = request.user.id
        pictureUploaded.save()
    context = { 'form': form, 
                'username': request.user.username}
    return render(request, 'photo/index.html', context)


#--------------------------------------------------------------------------------------------
# Display all photo in the database for a logged-in user
#--------------------------------------------------------------------------------------------
def allPhotos(request):
    myPictures = Picture.objects.filter(user_id=request.user.id).order_by('-id')
    context = {'myPictures':myPictures,
               'username': request.user.username}
    # TODO : remenber to use the session trick
    #request.session['photos'] = 'move data around'
    return render(request, 'photo/allPhotos.html', context)