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
        print(user)
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request,pk):

    user=request.user
    
    post=Post.objects.get(id=pk)
   
    if(user not in post.like.all()):
        post.like.add(user)
        return Response({"The Post was liked by user":user.username})
    else:
        return Response("this post is already liked")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike(request,pk):
    user=request.user
    
    post=Post.objects.get(id=pk)
    
    if(user in post.like.all()):
        post.like.remove(user)
        return Response({"The Post was unliked by user":user.username})
    else:
        return Response("This post was not liked")
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addComment(request,pk):
    data =request.data
    user=request.user
    post=Post.objects.get(id=pk)
    comment=Comment.objects.create(user=user,post=post,comment=data['comment'])
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def getProfile(request):
    user=request.user
    profile=Profile.objects.get(user=user)
    followers=profile.follower.count()
    following=profile.following.count()
    return Response({"username":profile.user.username,"followers":followers,"following":following})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Follow(request,pk):
    followeruser=request.user
    user=User.objects.get(id=pk)
    followprofile=Profile.objects.get(user=user)
    followingprofile=Profile.objects.get(user=followeruser)
    if(user.id!=followeruser.id):
        followprofile.follower.add(followeruser)
        followingprofile.following.add(user)
        return Response({"Logged in user is following ":user.username})
    else:
        return Response("user cannot follow itself")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unFollow(request,pk):
    followeruser=request.user
    followerprofile=Profile.objects.get(user=followeruser)
    user=User.objects.get(id=pk)
    followprofile=Profile.objects.get(user=user)
    if(followeruser in followprofile.follower.all()):
        followprofile.follower.remove(followeruser)
        followerprofile.following.remove(user)
        return Response({"Logged in user has unfollowed":user.username})
    else:
        return Response("not a follower")