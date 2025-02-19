from django.db import models
from core.models import BaseModel,Address
import shortuuid
# Create your models here.
from buyer_module.models import Buyers
from seller_module.models import Sellers
from investors_module.models import Investors
from agent_module.models import Agents

Seller = 'Seller'
Buyer = 'Buyer'
Agent = 'Agent'
Home_Inspector = 'Home_Inspector'
Appraiser = 'Appraiser'
Title_Company = 'Title_Company'
Contractor = 'Contractor'
Lender = 'Lender'

MEMBER_TYPES = [
    (Seller, 'seller'),
    (Buyer, 'buyer'),
    (Agent, 'agent'),
    (Home_Inspector, 'home_inspector'),
    (Appraiser, 'appraiser'),
    (Title_Company, 'title_company'),
    (Contractor, 'contractor'),
    (Lender, 'lender'),
]

class MemberAddress(BaseModel):
    maddress_id = models.CharField(max_length=50, default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True) 
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    street_no = models.CharField(max_length=50, blank=True, null=True)
    street_name = models.CharField(max_length=500, blank=True, null=True)
    suite_no = models.CharField(max_length=50, blank=True, null=True)
    buyer = models.ForeignKey(Buyers, on_delete=models.SET_NULL,null=True)
    seller = models.ForeignKey(Sellers, on_delete=models.SET_NULL,null=True)
    investor =models.ForeignKey(Investors, on_delete=models.SET_NULL,null=True)
    agent = models.ForeignKey(Agents, on_delete=models.SET_NULL,null=True)
    lender_id = models.IntegerField(null=True)
    member_type  = models.CharField(max_length=30,choices=MEMBER_TYPES, blank=True, null=True)# Unncessory or below one unncessory. remove
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)

class MembershipFee(BaseModel):
    membership_id = models.CharField(max_length=50,default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True)
    acct_setup_fee = models.DecimalField(max_digits=10, decimal_places=2)
    membership_fee = models.DecimalField(max_digits=10, decimal_places=2)
    member_type  = models.CharField(max_length=30,choices=MEMBER_TYPES, blank=True, null=True) # Unncessory or above one unncessory. remove
    maddress = models.ForeignKey(MemberAddress, on_delete=models.SET_NULL,null=True)