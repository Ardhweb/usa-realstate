from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import  ObUserManager
import shortuuid
import random
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import F, ExpressionWrapper, fields

# Create your models here.
class User(AbstractUser):
    contact_no = models.CharField(max_length=20,null=True,blank=True)
    member_type = models.CharField(max_length=50,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    #USERNAME_FIELD = 'email_address'
    #REQUIRED_FIELDS  = [email_address]
    objects = ObUserManager()



class SingleFactorEmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    six_otp = models.PositiveIntegerField(null=True,  blank=True)
    attempts = models.PositiveIntegerField(default=0, null=True,  blank=True)
    max_attempts = models.IntegerField(default=3)
    u_code = models.CharField(max_length=20,default=shortuuid.ShortUUID().random(length=14), editable=False, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(default=True)

    def has_expired(self):
        return now() > self.created_at + timedelta(hours=24)

    def increment_attempts(self):
        self.attempts += 1
        if self.attempts >= self.max_attempts:
            self.is_expired = False
        self.save()



class RemoveRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    request_at = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    reason = models.TextField(null=True, blank=True)  # Optional field for the reason for the request
    comments = models.TextField(null=True, blank=True)  # Optional field for additional comments or notes

    def __str__(self):
        return f"Remove request {self.request_at}"




        


      