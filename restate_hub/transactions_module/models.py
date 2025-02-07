from django.db import models

# Create your models here.
from core.models import BaseModel
from buyer_module.models import Buyers
from seller_module.models import Sellers
from agent_module.models import Agents
from investors_module.models import Investors
from property_module.models import PropertiesInfo
import shortuuid

class Tansactions(BaseModel):
    Sale = 'sale'
    Rent = 'rent'
    Lease = 'lease'
    TRANSCTION_TYPES = [
     (Sale ,'sale'),
    (Rent , 'rent'),
    (Lease , 'lease'),
    ]
    transaction_id = models.CharField(max_length=50,default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True) 
    property = models.ForeignKey(PropertiesInfo, on_delete=models.SET_NULL,null=True,blank=True)
    buyer = models.ForeignKey(Buyers, on_delete=models.SET_NULL,null=True,blank=True)
    seller = models.ForeignKey(Sellers, on_delete=models.SET_NULL,null=True,blank=True)
    agent = models.ForeignKey(Agents, on_delete=models.SET_NULL,null=True,blank=True)
    transaction_type =  models.CharField(max_length=20, choices= TRANSCTION_TYPES, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True,editable=True)
    sold_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20,  null=True)
    investor = models.ForeignKey(Investors, on_delete=models.SET_NULL,null=True,blank=True)