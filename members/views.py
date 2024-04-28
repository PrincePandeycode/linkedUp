from cmath import log

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.success(request,"Invalid username or password")
            return redirect('login')
        



    else:
        return render(request,'authenticate/login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,"you are logged out ..")
    return redirect('home')

def register_user(request):
    if request.method == "POST":  # if someone filled some values in form
        form = RegisterUserForm(request.POST)
       
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username , password = password)
            login(request,user)
            messages.success(request,("Registration success. you are logged in.."))
            return redirect('home')
    else:
        form = RegisterUserForm() #if form in not filled , then just passing the django form to html


    return render(request,'authenticate/register_user.html',{
        'form':form, #passing the django form to page if not filled
    })