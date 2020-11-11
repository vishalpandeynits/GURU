from django.urls import path
from .views import *
urlpatterns = [
	path('signup/',signup,name="signup"),
    path('activate/<uidb64>/<token>/',activate,name="activate"),
    path('<str:username>/', profiles, name='profile'),
 ]