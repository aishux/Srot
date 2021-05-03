from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def discussions(request):
    if request.method == "POST":
        user = User.objects.filter(username="srot")[0]
        title = request.POST.get("title")
        dis_type= request.POST.get("distype")
        information = request.POST.get("main_info")
        hashtags = request.POST.get("hashtags")

        dis = Discussion(user=user,title=title,dis_type=dis_type,information=information,hashtags=hashtags)

        dis.save()

    all_dis = Discussion.objects.all()

    return render(request,'discussions.html',{"all_dis":all_dis})

def sidebar(request):
    return render(request,'donations/sidebar.html')

def plasma(request):
    return render(request,'donations/plasma.html')