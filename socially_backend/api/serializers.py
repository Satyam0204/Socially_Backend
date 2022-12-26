
from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import *


class PostSerializer(ModelSerializer):
    class Meta:
        model=Post
        fields=['title','desc','datecreated','like','id']
        