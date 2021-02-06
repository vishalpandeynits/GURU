from django.urls import path
from .views import *
urlpatterns = [
	path('<unique_id>/',polls,name="polls"),
	path('<unique_id>/<int:poll_id>/',poll_page,name="poll_page"),
	path('<unique_id>/voting/<poll_id>/<choice_id>',voting,name="voting"),
	path('<unique_id>/<poll_id>/',delete_poll,name="delete_poll"),
]