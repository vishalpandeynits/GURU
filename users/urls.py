from django.urls import path
from .views import *
urlpatterns = [
	path('signup/',signup,name="signup"),
    path('activate/<uidb64>/<token>/',activate,name="activate"),
    path('hello/<str:username>/',profiles),
    path('markread/',mark_notif_read,name="readall-notif"),
    path('<str:username>/', profiles, name='profile'),
 ] 