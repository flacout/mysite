from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


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
        picture_id = request.POST.get('photo_id',0)
        if picture_id!=0: return displayPicture(request, picture_id)
        else: return savePictureForm(request)
    
    else : 
        form = UploadPhotoForm()
        context = { 'form': form, 
                    'username': request.user.username}
        return render(request, 'photo/index.html', context)

def displayPicture(request, picture_id):
    form = UploadPhotoForm()
    pictureToDraw = Picture.objects.filter(id=picture_id)
    context = { 'form': form, 
                'username': request.user.username,
                'lastPicture': pictureToDraw[0]}
    return render(request, 'photo/index.html', context)

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