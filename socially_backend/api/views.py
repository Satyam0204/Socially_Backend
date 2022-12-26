from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import * 
from .serializers import *
# Create your views here.

@api_view(['GET'])
def viewRoutes(request):
    routes=[
            {
            'endpoint':'viewRoutes',
            'desc':'view all routes',

            },
    ]

    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPosts(request):
    user= request.user
    posts=user.post_set.all()
    serializer=PostSerializer(posts,many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSpecificPost(request, pk):
    user=request.user
    post=user.post_set.get(id=pk)
    serializer=PostSerializer(post,many=False)
    return Response(serializer.data)