from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


#import of databade models
from .models import Picture
from .forms import UploadPhotoForm


def index(request):
    if request.method== 'POST':
        form = UploadPhotoForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        else : 
            filePath = settings.BASE_DIR+"/media/pictures/aa.jpg"
            picture_file=open(filePath,'wb')
            picture_file.write(request.FILES['picture'].read())
            picture_file.close()
        return render(request, 'photo/index.html',{'form':form})
    
    else : 
        form = UploadPhotoForm()
        return render(request, 'photo/index.html', {'form': form})

def allPhotos(request):
    myPictures = Picture.objects.all()
    context = {'myPictures':myPictures}
    return render(request, 'photo/allPhotos.html', context)