from django.urls import path
from . import views

urlpatterns = [
    
    path('discussions/',views.discussions,name="discussions"),
    path('donations/sidebar/',views.sidebar,name="sidebar"),
    path('donations/plasma/',views.plasma,name="plasma"),
    
]