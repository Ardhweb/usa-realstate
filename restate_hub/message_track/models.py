from django.db import models

# Create your models here.
from core.models import BaseModel
from buyer_module.models import Buyers
from seller_module.models import Sellers
from agent_module.models import Agents
from lender_module.models import Lenders
CATEGORY_CHOICES = [
        ('inquiry', 'inquiry'),
    ]
class MessageTrack(models.Model):
    message_in = models.TextField() #message  memeber to Admin
    message_out = models.TextField() #message Admin to  Member
    msg_date = models.DateTimeField(auto_now_add=True)
    
    # Seller, Buyer, Agent, Lender, Contractor relation
    seller = models.ForeignKey(Sellers, on_delete=models.SET_NULL, null=True, blank=True, related_name='seller_messages')
    buyer = models.ForeignKey(Buyers, on_delete=models.SET_NULL, null=True, blank=True, related_name='buyer_messages')
    agent = models.ForeignKey(Agents, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_messages')
    lender = models.ForeignKey(Lenders, on_delete=models.SET_NULL, null=True, blank=True, related_name='lender_messages')
    contractor = models.BigIntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    message_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)
    property = models.CharField(max_length=100, null=True, blank=True) # Needs to chnage intofk



