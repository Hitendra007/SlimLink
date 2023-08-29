from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
def login(request):
    if request.method =="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None :
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid username or password")
            return redirect('login')
    return render(request,'login.html')

def signup(request):
    if request.method == "POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        if(password == password1):
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already used")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Username already used")
                return redirect('signup')
            else :
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request,"Password mismatch")
            return redirect('signup')
    return render(request,'signup.html')
@login_required(login_url="login")
def logout(request):
    auth.logout(request,)
    return redirect('login')
 


