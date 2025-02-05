from django.db import models

# Create your models here.
from core.models import BaseModel
import shortuuid
from membership_module.models import MemberAddress

class Lenders(BaseModel):
    lender_id = models.CharField(max_length=50,default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True)
    first_name = models.CharField(max_length=50,blank=False, null=True)
    last_name =  models.CharField(max_length=50,blank=False, null=True)
    phone_num =  models.IntegerField()
    email = models.EmailField(max_length=254)
    join_date_at = models.DateTimeField(auto_now_add=True,editable=True)
    business_name = models.CharField(max_length=50, blank=True, null=True)
    maddress =  models.ForeignKey(MemberAddress, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=550, blank=True, null=True)
    specialized_loan_products = models.CharField(max_length=50, blank=True, null=True)
    nmls_no = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True) 