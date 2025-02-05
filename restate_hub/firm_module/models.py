from django.db import models
# Create your models here.
from buyer_module.models import Buyers
from seller_module.models import Sellers
from agent_module.models import Agents
from investors_module.models import Investors
import shortuuid
from core.models import BaseModel

class TitleCompany(BaseModel):
    title_id =  models.CharField(max_length=50,default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True) 
    company_name = models.CharField(max_length=50, blank=False, null=True)
    phone_num = models.IntegerField(null=True)
    email = models.EmailField(max_length=254, null=True)
    agent = models.ForeignKey(Agents, on_delete=models.SET_NULL,null=True)
    buyer = models.ForeignKey(Buyers, on_delete=models.SET_NULL,null=True)
    seller = models.ForeignKey(Sellers, on_delete=models.SET_NULL,null=True)
    investor = models.ForeignKey(Investors, on_delete=models.SET_NULL,null=True)
    escrow_agent_name = models.CharField(max_length=50, blank=False, null=True)
    address_complete = models.TextField()