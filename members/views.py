from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginForm, RegisterUserForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                error_massage = "Invalid username or password."
                return render(request, 'members/login_user.html', {
                    'error_massage': error_massage,
                    'login_form': form
                })
        else:
            return render(request, 'members/login_user.html', {
                "login_form": form
            })

    else:
        return render(request, 'members/login_user.html', {
            "login_form": LoginForm()
        })

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            print(user)
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'members/register_user.html', {
                "register_form": form
            })
    else:
        form = RegisterUserForm()
        return render(request, 'members/register_user.html', {
            "register_form": form
        })