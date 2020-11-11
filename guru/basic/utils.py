import string
from random import choice,randint
from django.core.paginator import Paginator
import re
from django.utils.text import slugify


def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)

def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value
    
def extension_type(file_name):
	videos = ['WEBM','MPG', 'MP2', 'MPEG','MPE', 'MPV', 'OGG', 'MP4', 'M4P' , 'M4V', 'AVI', 'WMV', 'MOV', 'QT','FLV', 'SWF','MKV']
	images = ["JPG","PNG","GIF","PSD","RAW","BMP","SVG","AI","EPS","JPEG"]
	
	file_extension = str(file_name).split('.')[-1].upper()
	if file_extension in videos:
		return 'video'
	if file_extension in images:
		return 'image'
	return 'other'

def proper_pagination(object,index):
    start_index,end_index = 0,10
    if object.number>index:
        start_index = object.number-index
        end_index = start_index + end_index
    return (start_index,end_index)

def pagination(request,object):
        paginator = Paginator(object,6)
        page_num=1
        if request.GET.get('page'):
            page_num = request.GET.get('page')
        query = paginator.page(page_num)
        start_index,end_index = proper_pagination(query,index=4)
        page_range = list(paginator.page_range)[start_index:end_index]
        return query,page_range

def unique_id():
    characters = string.ascii_letters + string.digits
    return  "".join(choice(characters) for x in range(randint(7,15)))