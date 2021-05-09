from django.urls import path
from . import views

urlpatterns = [
    
    path('discussions/',views.discussions,name="discussions"),
    path('showComments/',views.showComments,name="showDComments"),
    path('saveDComment/',views.saveDiscussionComment,name="save_d_comment"),
    path('donations/sidebar/',views.sidebar,name="sidebar"),
    path('donations/plasma/',views.plasma,name="plasma"),
    path('donations/oxygen/',views.oxygen,name="oxygen"),
    path('donations/injections/',views.injections,name="injections"),
    path('donations/food/',views.food,name="food"),
    path('donations/beds/',views.beds,name="beds"),
    path('tables',views.tables,name="tables"),
    path('leads/foodleads',views.foodleads,name="foodleads"),
    path('leads/bedleads',views.bedleads,name="bedleads"),
    path('leads/injectionleads',views.injectionleads,name="injectionleads"),
    path('leads/oxygenleads',views.oxygenleads,name="oxygenleads"),
    path('leads/plasmaleads',views.plasmaleads,name="plasmaleads"),
]
