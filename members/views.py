from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate, login

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