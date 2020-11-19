from django.contrib import admin
from .models import *

class ClassroomAdmin(admin.ModelAdmin):
	list_display = ['class_name','unique_id']
	date_hierarchy = 'created_on'
	list_display_links = ['class_name','unique_id']
	list_filter = ['class_name',]
	search_fields = ['class_name','unique_id']

# Register your models here.
admin.site.register(Classroom,ClassroomAdmin)
admin.site.register(Subject)
admin.site.register(Note)
admin.site.register(Assignment)
admin.site.register(Announcement)
admin.site.register(Submission)
admin.site.register(Subject_activity)
admin.site.register(Classroom_activity)
