from django.contrib import admin
from .models import *
# Register your models here. 

admin.site.register(Choice)

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    pass