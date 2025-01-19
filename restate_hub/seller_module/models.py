from django.db import models
from core.models import BaseModel
import shortuuid
from buyer_module.models import Buyers
# Create your models here.
class Sellers(BaseModel):
    seller_id = models.UUIDField(default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True) 
    first_name = models.CharField(max_length=50,blank=False, null=True)
    last_name =  models.CharField(max_length=50,blank=False, null=True)
    phone_num =  models.IntegerField()
    email = models.EmailField(max_length=254)
    agent_id = models.BigIntegerField(blank=False, null=True) # needs to chnage into fk near future.
    buyer = models.ForeignKey(Buyers, on_delete=models.SET_NULL,null=True)
    investor_id = models.BigIntegerField(blank=False, null=True) # needs to chnage into fk near future.
    property_id = models.BigIntegerField(blank=False, null=True) # needs to chnage into fk near future.
    agent_rep = models.CharField(max_length=50,blank=False, null=True)
    bac = models.BooleanField(default=False)
    bac_fee = models.DecimalField(max_digits=10, decimal_places=2)
    business_name = models.CharField(max_length=50, blank=True, null=True)
    agent_agreement = models.CharField(max_length=50, blank=True, null=True)
