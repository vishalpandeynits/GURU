from .models import Classroom

def data(request,params={}):
    user = request.user
    if user.is_authenticated:
        my_classes = Classroom.objects.all().filter(members=user).reverse()
        read = user.notifications.read()
        params ={
            'classes':my_classes,
            'read':read
        }
    return params