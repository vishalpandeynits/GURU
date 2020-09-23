from .models import *
def note_delete_notify(request,note):
	activity = Subject_activity(subject=note.subject_name,actor=request.user)
	activity.action = "A note is deleted by " + request.user.username
	activity.save()

def assignment_delete_notify(request,assignment):
	activity = Subject_activity(subject=assignment.subject_name,actor=request.user)
	activity.action = "An Assignment is deleted by "+ request.user.username
	activity.save()

def announcement_delete_notify(request,announcement):
	activity = Subject_activity(subject=announcement.subject_name,actor=request.user)
	activity.action = "An Announcement is deleted by "+ request.user.username
	activity.save()