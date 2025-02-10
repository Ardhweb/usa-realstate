from django.db import models
from core.models import BaseModel
import shortuuid
from accounts.models import User
# Create your models here.
class Agents(BaseModel):
    agent_id = models.CharField(default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True, max_length=50) 
    first_name = models.CharField(max_length=50,blank=False, null=True)
    last_name =  models.CharField(max_length=50,blank=False, null=True)
    phone_num = models.CharField(max_length=15, blank=True, null=True)  # Use CharField to allow more flexibility  # Allow null and blank values
    email = models.EmailField(max_length=254)
    join_date_at = models.DateTimeField(auto_now_add=True,editable=True)
    business_name = models.CharField(max_length=50, blank=True, null=True)
    # buyer = models.ForeignKey(Buyers, on_delete=models.SET_NULL,null=True)
    # seller = models.ForeignKey(Sellers, on_delete=models.SET_NULL,null=True)
    investor_id = models.BigIntegerField(blank=False, null=True) # needs to chnage into fk near future.
    user =models.OneToOneField(User,on_delete=models.SET_NULL, null=True)
   
