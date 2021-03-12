from django.urls import path,include
from .views import *
from django_email_verification import urls as mail_urls

urlpatterns = [
    path('',home,name="home"),
    path('signup/',signup,name="signup"),
    path('homepage/',homepage,name="homepage"),
    path('email/', include(mail_urls)),
    path('subject/<unique_id>',subjects,name="subjects"),
    path('subject/<unique_id>/<subject_id>',subject_page,name="subject_page"),
]