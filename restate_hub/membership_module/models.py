from django.db import models
from core.models import BaseModel,Address
import shortuuid
# Create your models here.
from buyer_module.models import Buyers
from seller_module.models import Sellers
from investors_module.models import Investors
from agent_module.models import Agents
from accounts.models import User

Seller = 'seller'
Buyer = 'buyer'
Agent = 'agent'
Home_Inspector = 'home_inspector'
Appraiser = 'appraiser'
Title_Company = 'title_company'
Contractor = 'contractor'
Lender = 'lender'

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
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="member_address")
    street_no = models.CharField(max_length=50, blank=True, null=True)
    street_name = models.CharField(max_length=500, blank=True, null=True)
    suite_no = models.CharField(max_length=50, blank=True, null=True)
    lender_id = models.IntegerField(null=True)
    member_type  = models.CharField(max_length=30,choices=MEMBER_TYPES, blank=True, null=True)# Unncessory or below one unncessory. remove
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    state_two_code = models.CharField(max_length=5, null=True,blank=True)
    
    


class MembershipFee(BaseModel):
    membership_id = models.CharField(max_length=50,default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True)
    acct_setup_fee = models.DecimalField(max_digits=10, decimal_places=2)
    membership_fee = models.DecimalField(max_digits=10, decimal_places=2)
    member_type  = models.CharField(max_length=30,choices=MEMBER_TYPES, blank=True, null=True) # Unncessory or above one unncessory. remove
    maddress = models.ForeignKey(MemberAddress, on_delete=models.SET_NULL,null=True)
    next_due = models.DateField(null=True, blank=True)  # Allows NULL values
    last_due = models.DateField(null=True, blank=True)  # Allows NULL values

class SubscriptionPlans(BaseModel):
    fee_id = models.CharField(max_length=50,default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True)
    member_type  = models.CharField(max_length=30,choices=MEMBER_TYPES, blank=True, null=True, unique=True) # Unncessory or above one unncessory. remove
    setup_fee = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_fee =  models.DecimalField(max_digits=10, decimal_places=2)
    paymentPlan = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.member_type
    



