from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, null=True, blank=True)
    desc =models.TextField(max_length=500, null=True)
    datecreated=models.DateTimeField(auto_now_add=True, null=True)
    like=models.ManyToManyField(User,blank=True,related_name='like')

    def __str__(self):
        return self.title