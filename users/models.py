from django.db import models

# Create your models here.
class Users(models.Model):
    userName = models.CharField(max_length=100,unique=True)
    userPassword = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
    lastLoginTime = models.DateField(auto_now=True)
    state = models.IntegerField(default=0)
    class Meta:
        ordering = ('created',)