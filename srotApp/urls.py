from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup/", views.handleSignUp, name="signup"),
    path("login/", views.handleLogin, name="login"),
    path("logout/", views.handleLogout, name="logout"),
    path('accounts/', include('allauth.urls')),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),

    path("password_reset", views.password_reset_request, name="password_reset"),

    path('discussions/',views.discussions,name="discussions"),
    path('showComments/',views.showComments,name="showDComments"),
    path('saveDComment/',views.saveDiscussionComment,name="save_d_comment"),
    path('donations/sidebar/',views.sidebar,name="sidebar"),
    path('donations/plasma/',views.plasma,name="plasma"),
    path('donations/oxygen/',views.oxygen,name="oxygen"),
    path('donations/injections/',views.injections,name="injections"),
    path('donations/food/',views.food,name="food"),
    path('donations/beds/',views.beds,name="beds"),
    path('leads/foodleads/<int:pageno>',views.foodleads,name="foodleads"),
    path('leads/bedleads/<int:pageno>',views.bedleads,name="bedleads"),
    path('leads/injectionleads/<int:pageno>',views.injectionleads,name="injectionleads"),
    path('leads/oxygenleads/<int:pageno>',views.oxygenleads,name="oxygenleads"),
    path('leads/plasmaleads/<int:pageno>',views.plasmaleads,name="plasmaleads"),
    path('leads/<str:resource>/<str:state>/<int:pageno>/<str:city>',views.filterleads,name="filterleads"),
    path('leads/<str:resource>/<str:state>/<int:pageno>/',views.filterleads,name="filterleads"),
    path('leads/filter',views.filter,name="filter"),
    path('',views.home,name="home"),
    path('volunteer/landing',views.landing,name="landing"),
    path('volunteer/food',views.volfood,name="volfood"),
    path('editfood/',views.editfood,name="editfood"),
    path('volunteer/beds',views.volbeds,name="volbeds"),
    path('edithospital/',views.edithospital,name="edithospital"),
    path('volunteer/injections',views.volinjection,name="volinjection"),
    path('volunteer/oxygen',views.voloxygen,name="voloxygen"),
    path('volunteer/plasma',views.volplasma,name="volplasma"),
    path('deleteLead/<str:resource>/<int:id>',views.deleteLead,name="deleteLead"),
    path('verifyLead/<str:resource>/<int:id>',views.verifyLead,name="verifyLead"),
    path('editoxygen/',views.editoxygen,name="editoxygen"),
    path('editinjection/',views.editinjection,name="editinjection"),
    path('editplasma/',views.editplasma,name="editplasma"),
    path('volForm/',views.volForm,name="volForm"),
    path('bot/',views.bot,name="bot"),
]
