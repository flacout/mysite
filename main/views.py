from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'main/index.html', {'username': request.user.username})


def loggedin(request):
    return render_to_response('main/index.html', {'username': request.user.username})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register/complete')

    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html', {'form': form})

def registration_complete(request):
    return render_to_response('registration/registration_complete.html')

def logout_view(request):
    logout(request)
    switch=1
    return render(request, 'main/index.html', {'username': request.user.username,'switch':switch})