from django.urls import path
from .views import *
urlpatterns = [
	path('<unique_id>/',home,name="polls"),
	path('<unique_id>/poll-page/<int:poll_id>/',poll_page,name="poll_page"),
	path('<unique_id>/voting/<poll_id>/<choice_id>',voting,name="voting")
]
