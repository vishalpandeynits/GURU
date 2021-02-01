from django.urls import path
from django.urls.resolvers import URLPattern
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .rest_views import *
urlpatterns = [
    path('users',UserView.as_view(),name="user-list"),
    path('user/<pk>',UserDetail.as_view(),name="user-detail"),
    path('classrooms',ClassroomList.as_view(),name="classroom-list"),
    path('classroom/<pk>',ClassroomDetails.as_view(),name="classroom-detail")

]
urlpatterns = format_suffix_patterns(urlpatterns)