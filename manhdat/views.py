from django.shortcuts import render, loader, redirect
from django.http import HttpResponse
from .models import ManhDat, UserManhDat
from django.contrib.auth.models import User

# Create your views here.
def lands(request):
    if not 'account' in request.session:
        return redirect('login') 
    user_lands = UserManhDat.objects.filter(user__id=request.session['account']['id'])
    lands = []
    for user_land in user_lands:
        lands.append(user_land.manhdat)
    template = loader.get_template('manhdat/lands.html')
    context = {
        'lands': lands,
    }
    return HttpResponse(template.render(context, request))

def land_details(request, id):
    land = ManhDat.objects.get(id=id)
    template = loader.get_template('manhdat/land_details.html')
    context = {
        'land': land,
    }
    return HttpResponse(template.render(context, request))

def users_of_land(request, id):
    land = ManhDat.objects.get(id=id)
    user_manhdat_list = UserManhDat.objects.filter(manhdat=land)
    users = []
    for user_manhdat in user_manhdat_list:
        user = User.objects.filter(id = user_manhdat.user.id).first()
        temp = {}
        temp['user'] = user
        temp['role'] = user_manhdat.role
        users.append(temp)

    template = loader.get_template('manhdat/users_of_land.html')
    context = {
        'land_id': id,
        'users': users,
    }
    return HttpResponse(template.render(context, request))

def delete_user_of_land(request, land_id, user_id):
    land = ManhDat.objects.get(id=land_id)
    user = User.objects.get(id=user_id)
    user_of_land = UserManhDat.objects.filter(manhdat=land, user=user).first()
    user_of_land.delete()
    return redirect('users-of-land', id=land_id)
