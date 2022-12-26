from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    follower=models.ManyToManyField(User, related_name='follower',blank=True)
    following=models.ManyToManyField(User,related_name='following',blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, null=True, blank=True)
    desc =models.TextField(max_length=500, null=True)
    datecreated=models.DateTimeField(auto_now_add=True, null=True)
    like=models.ManyToManyField(User,blank=True,related_name='like')


    def __str__(self):
        return self.title

class Comment(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment=models.TextField(max_length=500)

    def __str__(self):
        return self.comment

