
from dataclasses import field
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class PostSerializer(ModelSerializer):
    class Meta:
        model=Post
        fields=['title','desc','datecreated','like','id']
        


class CommentSerializer(ModelSerializer):
    class Meta:
        model=Comment
        fields=['id','comment']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']
    
    def create(self, validated_data):
        user=User.objects.create(username = validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user