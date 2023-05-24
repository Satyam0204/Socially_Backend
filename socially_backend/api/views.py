from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import * 
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
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



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def viewRoutes(request):
    routes=[
            {
            'endpoint':'viewRoutes',
            'desc':'view all routes',

            },
    ]

    return Response(routes)
class Register(APIView):
    @classmethod
    def post(self, request):
        userdata=request.data
        serialize=UserSerializer(data=userdata)



        if (not serialize.is_valid()):
            
            return Response(serialize.errors)
        serialize.save()
        user=User.objects.get(username=serialize.data['username'])
        Profile.objects.create(user=user)
        refresh = RefreshToken.for_user(user)
        return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPosts(request):
    user= request.user
    posts=user.post_set.all()
    serializer=PostSerializer(posts,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getallPosts(request):
 
    posts=Post.objects.all()
    serializer=PostSerializer(posts,many=True)
    return Response(serializer.data)


@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def getSpecificPost(request, pk):
    user=request.user
    if request.method=='GET':
        try:
            post=user.post_set.get(id=pk)
            serializer=PostSerializer(post,many=False)
            return Response(serializer.data)
        except:
            return Response("post with this id doesn't exist")
    if request.method=='DELETE':
        try:
            post=user.post_set.get(id=pk)
            post.delete()
            return Response('post was deleted')
        except:
            return Response("id was invalid")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPost(request):
    data=request.data
    user=request.user
    if(data['title'] and data['desc']):
        post=Post.objects.create(user=user,title=data['title'],desc=data['desc'])
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)
    else:
        return Response("Title or desc cannot be empty")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request,pk):
    try:
        user=request.user
        
        post=Post.objects.get(id=pk)
    
        if(user not in post.like.all()):
            post.like.add(user)
            return Response({"The Post was liked by user":user.username})
        else:
            return Response("this post is already liked")
    except:
        return Response("id was invalid")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike(request,pk):
    user=request.user
    try:
        post=Post.objects.get(id=pk)
        
        if(user in post.like.all()):
            post.like.remove(user)
            return Response({"The Post was unliked by user":user.username})
        else:
            return Response("This post was not liked")
    except:
        return Response("id was invalid")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addComment(request,pk):
    data =request.data
    user=request.user
    try:
        post=Post.objects.get(id=pk)
        if(data['comment']):
            comment=Comment.objects.create(user=user,post=post,comment=data['comment'])
            serializer = CommentSerializer(comment, many=False)
            return Response(serializer.data)
        else:
            return Response("you cannot post an empty comment")
    except:
        return Response("id was invalid")

        
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
    followingprofile=Profile.objects.get(user=followeruser)
    try:
        user=User.objects.get(id=pk)
        followprofile=Profile.objects.get(user=user)
        if(user.id!=followeruser.id):
            followprofile.follower.add(followeruser)
            followingprofile.following.add(user)
            return Response({"Logged in user is following ":user.username})
        else:
            return Response("user cannot follow itself")
    except:
        return Response("id was invalid")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unFollow(request,pk):
    followeruser=request.user
    followerprofile=Profile.objects.get(user=followeruser)
    try:
        user=User.objects.get(id=pk)
        followprofile=Profile.objects.get(user=user)
        if(followeruser in followprofile.follower.all()):
            followprofile.follower.remove(followeruser)
            followerprofile.following.remove(user)
            return Response({"Logged in user has unfollowed":user.username})
        else:
            return Response("not a follower")
    except:
        return Response("id was invalid")

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def viewProfile(request,pk):
    followers_arr=[]
    following_arr=[]
    user=User.objects.get(id=pk)
    profile= Profile.objects.get(user = user)
    followers=profile.follower.all()
    following=profile.following.all()
    for follower in followers:
        followers_arr.append(follower.id)
    for following_user in following:
        following_arr.append(following_user.id)
    return Response({"user_id":profile.user.id,"username":profile.user.username,"followers":followers.count(),"following":following.count(),"followers_arr":followers_arr,"following_arr":following_arr})


@api_view(['POST'])
def search(request):
    data = request.data
    search_results=[]
    if(data['profile']):
        profiles=User.objects.filter(username__icontains=data['profile'])
        for profile in profiles:
            search_results.append({"username":profile.username,"user_id":profile.id})
        return Response(search_results)
        
    else:
        return Response({
          "Failure": "Error", 
          "Error_list": {"field1": "This field is required"}
     },
     status=status.HTTP_400_BAD_REQUEST)


