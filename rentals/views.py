# from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib import messages
from rentals.forms import LoginForm, SignUpForm

def home(request):
    return render(request, 'index.html')

from django.contrib.auth import login, authenticate, logout



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! 🎉")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) # type: ignore
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request) # type: ignore
    return redirect('login')
