from django.db import models
from core.models import BaseModel
import shortuuid
from agent_module.models import Agents
from accounts.models import User
# Create your models here.
class Buyers(BaseModel):
    buyer_id = models.CharField(max_length=50,default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True) 
    join_date_at = models.DateTimeField(auto_now_add=True,editable=True)
    agent = models.ForeignKey(Agents,on_delete=models.SET_NULL, null=True, blank=True)
    business_name = models.CharField(max_length=50, blank=True, null=True)
    user = models.OneToOneField(User,on_delete=models.SET_NULL, null=True)

    