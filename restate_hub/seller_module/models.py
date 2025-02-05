from django.db import models
from core.models import BaseModel
import shortuuid
from agent_module.models import Agents
# Create your models here.
Foreclosure = 'Foreclosure'
Retirement = 'Retirement'
Need_Funds = 'Need_Funds'
Leisure = 'Leisure'

REASON_SELLING_TYPES = [
    (Foreclosure, 'foreclosure'),
    (Retirement, 'retirement'),
    (Need_Funds, 'need_funds'),
    (Leisure, 'leisure'),
]

Urgent = 'Urgent'
ASAP = 'ASAP'
Have_Some_Time_To_Wait = 'Have_Some_Time_To_Wait'
The_Price_Is_Right = 'The_Price_Is_Right'

SELLING_TYPES = [
    (Urgent, 'urgent'),
    (ASAP, 'asap'),
    (Have_Some_Time_To_Wait, 'have_some_time_to_wait'),
    (The_Price_Is_Right, 'the_price_is_right'),
]


class Sellers(BaseModel):
    seller_id = models.CharField(max_length=50,default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True) 
    first_name = models.CharField(max_length=50,blank=False, null=True)
    last_name =  models.CharField(max_length=50,blank=False, null=True)
    phone_num =  models.IntegerField()
    email = models.EmailField(max_length=254)
    agent = models.ForeignKey(Agents, on_delete=models.SET_NULL, null=True, blank=True)
    agent_rep = models.CharField(max_length=50,blank=False, null=True)
    bac = models.BooleanField(default=False)
    bac_fee = models.DecimalField(max_digits=10, decimal_places=2)
    business_name = models.CharField(max_length=50, blank=True, null=True)
    agent_agreement = models.CharField(max_length=50, blank=True, null=True)


class ReasonSelling(BaseModel):
    reason_selling_id = models.CharField(max_length=50,default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True) 
    reason_selling = models.CharField(max_length=50, choices=REASON_SELLING_TYPES,blank=False, null=True)
    seller = models.ForeignKey(Sellers, on_delete=models.SET_NULL,null=True)


# class SellingType(BaseModel):
#     selling_type_id = models.UUIDField(default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True)
#     selling_type = models.CharField(max_length=50, choices=SELLING_TYPES,blank=False, null=True) 
#     seller = models.ForeignKey(Sellers, on_delete=models.SET_NULL,null=True)
#     property = models.ForeignKey(PropertiesInfo, on_delete=models.SET_NULL,null=True)