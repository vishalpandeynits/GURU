from django.urls import path
from .views import *
urlpatterns = [
	path('',home,name="home"),
	path('poll-list/',poll_list,name="poll_list"),
	path('poll-page/<int:poll_id>/',poll_page,name="poll_page"),
	path('voting/<poll_id>/<choice_id>',voting,name="voting")
]
