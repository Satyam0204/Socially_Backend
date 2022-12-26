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


@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def getSpecificPost(request, pk):
    if request.method=='GET':
        user=request.user
        post=user.post_set.get(id=pk)
        serializer=PostSerializer(post,many=False)
        return Response(serializer.data)
    if request.method=='DELETE':
        user=request.user
        post=Post.objects.get(user=user,id=pk)
        post.delete()
        return Response('post was deleted')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPost(request):
    data=request.data
    user=request.user
    post=Post.objects.create(user=user,title=data['title'],desc=data['desc'])
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)

# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def deletePost(request,pk):
#     user=request.user
#     post=Post.objects.get(user=user,id=pk)
#     post.delete()
#     return Response('post was deleted')