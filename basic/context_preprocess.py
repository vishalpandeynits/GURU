from .models import Classroom
def data(request,params={}):
    if request.user.is_authenticated:
        my_classes = Classroom.objects.all().filter(members=request.user).reverse()
        params ={
            'classes':my_classes,
        }
    return params