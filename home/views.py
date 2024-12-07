#*NEW* -> redirect imported
from django.shortcuts import render, redirect
#for logging out user:
from django.contrib.auth import login, authenticate, logout


def home(request):
    return render(request, 'home.html')

def logout_user(request):
    logout(request)
    return redirect('home')
