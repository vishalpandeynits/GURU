from django.db.models.query import QuerySet
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(many=True,queryset = Classroom.objects.all())
    class Meta:
        model = User
        exclude = []

class ClassroomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Classroom
        exclude= ['unique_code']

class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        exclude = []