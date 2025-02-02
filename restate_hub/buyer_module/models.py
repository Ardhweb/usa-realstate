from django.db import models
from core.models import BaseModel
import shortuuid
from agent_module.models import Agents
# Create your models here.
class Buyers(BaseModel):
    buyer_id = models.UUIDField(default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True) 
    first_name = models.CharField(max_length=50,blank=False, null=True)
    last_name =  models.CharField(max_length=50,blank=False, null=True)
    phone_num =  models.IntegerField()
    email = models.EmailField(max_length=254)
    join_date_at = models.DateTimeField(auto_now_add=True,editable=True)
    agent = models.ForeignKey(Agents,on_delete=models.SET_NULL, null=True)
    business_name = models.CharField(max_length=50, blank=True, null=True)