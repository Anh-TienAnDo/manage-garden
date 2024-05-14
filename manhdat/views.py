from django.shortcuts import render, loader, redirect
from django.http import HttpResponse
from .models import ManhDat, UserManhDat

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
