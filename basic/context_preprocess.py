from .models import Classroom

def data(request,params={}):
    user = request.user
    if user.is_authenticated:
        my_classes = Classroom.objects.all().filter(members=user).reverse()
        params ={
            'classes':my_classes,
        }
    return params