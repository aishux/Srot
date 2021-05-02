from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def discussions(request):
    return render(request,'discussions.html')