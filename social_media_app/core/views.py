from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from . import models

# Create your views here.
def home (request):
    return HttpResponse(request.user)

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            error = 'Passwords do not match'
            return render(request, 'signup.html', {'error_message': error})
        if models.User.objects.filter(username=username).exists():
            error = 'Username is already taken'
            return render(request, 'signup.html', {'error_message': error})
        if models.User.objects.filter(email=email).exists():
            error = 'Email is already taken'
            return render(request, 'signup.html', {'error message': error})
        try:
            new_user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
            new_user.save()
            new_profile = models.Profile.objects.create(user=new_user, id_user=new_user.id)
            new_profile.save()
            auth.login(new_user)
            return redirect('home')
        except: 
            error = 'Error during User creation'
            return render(request, 'signup.html', {'error_message': error})
    return render(request, 'signup.html')
    
def login(request):
    if request.method == "POST": 
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        error = 'Invalid username and/or password'
        return render(request, 'login.html', {'error_message': error})
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')