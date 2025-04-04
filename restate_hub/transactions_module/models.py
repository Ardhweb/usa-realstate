from django.db import models

# Create your models here.
from core.models import BaseModel
from buyer_module.models import Buyers
from seller_module.models import Sellers
from agent_module.models import Agents
from investors_module.models import Investors
from property_module.models import PropertiesInfo
import shortuuid
from membership_module.models import MembershipFee
from accounts.models import User
from django.utils import timezone

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



#To Track and Store Each month transcation of the user /member
class SubscriptionTransaction(BaseModel):
        membershipfee = models.ForeignKey(
              MembershipFee, on_delete=models.CASCADE, related_name="payments"
          )  # One MembershipFee can have multiple payments
      
        user = models.ForeignKey(
              User, on_delete=models.CASCADE, related_name="tanscation_user"
          )  # Each payment belongs to a user
      
        amount = models.DecimalField(max_digits=10, decimal_places=2)
        payment_date = models.DateTimeField(auto_now=True,null=True,blank=True)
        next_due_date = models.DateField(blank=True,null=True)
    
        TRANSACTION_STATUS = [
            ("PENDING", "Pending"),
            ("PAID", "Paid"),
            ("FAILED", "Failed"),
        ]
        status = models.CharField(max_length=10, choices=TRANSACTION_STATUS, default="PENDING")
    
        # Helcim API details
        transaction_id = models.CharField(max_length=100, blank=True, null=True)  # Helcim reference
        payment_method = models.CharField(max_length=50, choices=[("CARD", "Card"), ("ACH", "ACH")])
        card_last4 = models.CharField(max_length=4, blank=True, null=True)  # Last 4 digits of card
        is_first_payment = models.BooleanField(default=False)


class HelcimInfo(models.Model):
    customerId = models.CharField(max_length=200, blank=True, null=True)
    customercode  =  models.CharField(max_length=200, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_helcim_account')
    signup_date = models.DateField(auto_now_add=True)  # Stores the date when the record is created
    cancellation_trigger_date = models.DateField(null=True, blank=True)  # Optional field
    is_subscribed = models.BooleanField(default=False)
    subscriptionId = models.IntegerField(null=True,blank=True)
  
