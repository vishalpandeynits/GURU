from django.db.models.query import QuerySet
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics,permissions
from .models import *
from .permissions import *
from django_filters import rest_framework as filters

# class UserView(APIView):
#     def get(self,request,format=None):
#         users = User.objects.all()
#         serializers = UserSerializer(users,many=True)
#         return Response(serializers.data)

class classroomfilter(filters.FilterSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('created_by',)

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAdminUser]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =  User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAdminUser]

class ClassroomList(generics.ListAPIView):
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Classroom.objects.all().filter(members=user)

class ClassroomDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated,IsMember]

    def get_queryset(self):
        user = self.request.user
        return Classroom.objects.filter(members=user)

class SubjectList(generics.ListCreateAPIView):
    serializer_class = SubjectSerializer
    def get_queryset(self,unique_code):
        classroom = Classroom.objects.get(unique_code = unique_code)
        return Subject.objects.filter(Classroom=classroom)
    

# class NotesList(generics.ListCreateAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NotesSerializer

# class NotesDetails(generics.RetrieveUpdateAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NotesSerializer

# class AssignmentList(generics.ListCreateAPIView):
#     queryset = Assignment.objects.all()
#     serializer_class = AssignmentSerializer

# class AssignmentDetails(generics.RetrieveUpdateAPIView):
#     queryset = Assignment.objects.all()
#     serializer_class = AssignmentSerializer