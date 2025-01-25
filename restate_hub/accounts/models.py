from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import  ObUserManager
# Create your models here.
class User(AbstractUser):
    contact_no = models.CharField(max_length=15,null=True,blank=True)
    member_type = models.CharField(max_length=50,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #USERNAME_FIELD = 'email_address'
    #REQUIRED_FIELDS  = [email_address]
    objects = ObUserManager()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.TextField(null=True)
    full_name = models.CharField(max_length=50, default="", blank=True, null=True)
    dob = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
