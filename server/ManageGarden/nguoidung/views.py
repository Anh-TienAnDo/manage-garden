from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .serializers import UserSerializer
import json

# Create your views here.
#generate login, logout, change password, profile, edit from django.contrib.auth import views as auth_views

# Login view
def login_user(request):
    method = request.method
    if method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = User.objects.filter(username=username)
        if user.exists() and user[0].check_password(password):
            userSerializer = UserSerializer(user[0]).data
            request.session['account'] = userSerializer
            return redirect(to='home')
        # Invalid username and password
        else:
            render(request, 'user/login.html', {'error': 'Invalid username or password'})
    if method == 'GET':
        content = {}
        if 'account' in request.session:
            return redirect(to='home')
        return render(request, 'user/login.html', content)

    
def logout_user(request):
    if 'account' in request.session:
        del request.session['account']
    return redirect(login_user)

def informations(request):
    return render(request, "user/informations.html")

def update_password(request):
    notifications = ""
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            notifications = "Password and confirm password are not the same"
        else:
            user = request.session['account']
            user.set_password(password)
            user.save()
            return redirect(to='informations-user')
    return render(request, "user/change-password.html", {'notifications': notifications})


def update_user(request):
    data = request.session['account']
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user = User.objects.get(id=data['id'])
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        request.session['account'] = UserSerializer(user).data
        user.save()
        return redirect(to='informations-user')

    return render(request, "user/update-user.html")
