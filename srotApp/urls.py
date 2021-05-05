from django.urls import path
from . import views

urlpatterns = [
    
    path('discussions/',views.discussions,name="discussions"),
    path('donations/sidebar/',views.sidebar,name="sidebar"),
    path('donations/plasma/',views.plasma,name="plasma"),
    path('donations/oxygen/',views.oxygen,name="oxygen"),
    path('donations/injections/',views.injections,name="injections"),
    path('donations/food/',views.food,name="food"),
    path('donations/beds/',views.beds,name="beds"),
]
