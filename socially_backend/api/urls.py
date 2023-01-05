from django.urls import path
from .views import *
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# from rest_framework_simplejwt.views import TokenRefreshView
# from .views import EmailTokenObtainPairView



urlpatterns = [
    path('',viewRoutes, name='viewRoutes'),
    path('register/',Register.as_view(),name='register'),
    path('authenticate/',  MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('all_posts/',getPosts,name="getuserposts"),
    path('all_users_posts/',getallPosts,name="getallposts"),
    path('posts/<str:pk>/',getSpecificPost,name="getspecificpost"),
    # path('deleteposts/<str:pk>/',deletePost,name="deletespecificpost"),
    path('posts/', createPost,name="createpost"),
    path('like/<str:pk>/',like,name="like"),
    path('unlike/<str:pk>/',unlike,name="unlike"),
    path('comment/<str:pk>/',addComment,name="comment"),
    path('follow/<str:pk>/',Follow,name="addfollower"),
    path('unfollow/<str:pk>/',unFollow,name="removefollower"),
    path('user',getProfile,name="getuser"),
    path('search',search,name="searchprofile"),
    path('profile/<str:pk>/',viewProfile,name="getprofile"),
]
