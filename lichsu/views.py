from django.shortcuts import render, redirect
from .models import *

#add id to the parameter
def get_ds_lichsu(request, id):
    ds_lichsu = LichSuCamBien.objects.filter(manhdat__id=id)[:30]
    return render(request, 'lichsu/lichsu.html', {
        'ds_lichsu': ds_lichsu,
        'land_id': id,
    })

# change this snippet from ManageGarden/lichsu/views.py:
def add_lichsu(request):
    manhdat = ManhDat.objects.get(pk=1)
    lichsu = LichSuCamBien(
        manhdat = manhdat,
        nhiet_do = 30,
        do_am = 60,
        do_am_dat = 80,
        anh_sang = 220,
    )
    lichsu.save()
    return redirect(to='ds-lichsu')