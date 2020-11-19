from django import template
from os import path
register = template.Library()
@register.filter(name='filebasename')
def filebasename(value):
    return path.basename(str(value))