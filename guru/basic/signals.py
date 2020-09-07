from django.dispatch import Signal
my_post_delete = Signal(providing_args=['instance', 'user'])
print(my_post_delete)
