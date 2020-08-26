from django.urls import path
from .views import *
urlpatterns = [
    path('<str:username>/', profiles, name='profile'),
    path('edit-profile/<username>/',edit_profile,name="edit-profile")
 ]