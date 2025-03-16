from django.db import models
# Create your models here.
from core.models import BaseModel
import shortuuid
from seller_module.models import Sellers
from agent_module.models import Agents
import random
import string
import time
import time
import random
import string


def generate_unique_id(length=12):
    """Generate a non-sequential unique ID using a timestamp and random suffix."""
    timestamp = str(int(time.time() * 1000))  # Milliseconds timestamp (13 digits)
    
    # Ensure the final ID length is exactly `length`
    random_length = max(0, length - len(timestamp))  # Avoid negative values
    random_suffix = ''.join(random.choices(string.digits, k=random_length))  

    unique_id = timestamp + random_suffix
    return unique_id[:length] 

class PropertiesInfo(BaseModel):
    RESIDENTIAL = 'residential'
    COMMERCIAL = 'commercial'
    LAND = 'land'
    INDUSTRIAL = 'industrial'
    LISTING_TYPES = [
        (RESIDENTIAL, 'Residential'),
        (COMMERCIAL, 'Commercial'),
        (LAND, 'Land'),
        (INDUSTRIAL, 'Industrial'),
    ]

    SINGLE_FAMILY = 'single family'
    TOWNHOME = 'townhome'
    CONDO = 'condo'

    PROPERTY_TYPES = [
        (SINGLE_FAMILY, 'Single Family'),
        (TOWNHOME, 'Townhome'),
        (CONDO, 'Condo'),
    ]
    ACTIVE = 'active'
    PENDING = 'pending'
    SOLD = 'sold'
    LEASED = 'leased'

    LISTING_STATUSES = [
        (ACTIVE, 'Active'),
        (PENDING, 'Pending'),
        (SOLD, 'Sold'),
        (LEASED, 'Leased'),
    ]

    YES = 'yes'
    NO = 'no'

    SELL_LEASEBACK_OPTIONS = [
        (YES, 'Yes'),
        (NO, 'No'),
    ]

    LEASEBACK_MONTHS = [
        (1, '1 Month'),
        (1.5, '1.5 Months'),
        (6, '6 Months'),
        (12, '12 Months'),
    ]

    property_id =  models.CharField(default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True,max_length=50) 
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, null=True)
    listing_id = models.CharField(default=generate_unique_id(),blank=True, null=True, max_length=200)
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPES, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    house_size = models.FloatField(null=True)
    lot_size = models.FloatField(null=True)
    bedrooms = models.IntegerField(null=True)
    bathrooms = models.FloatField(null=True)
    year_built = models.IntegerField(null=True)
    description = models.TextField(null=True)
    listing_status = models.CharField(max_length=10, choices=LISTING_STATUSES, null=True)
    listing_created_date = models.DateTimeField(auto_now_add=True)
    listing_updated_date = models.DateTimeField(auto_now=True)
    street_num = models.CharField(max_length=10, null=True)
    street_name = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=10, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=100, null=True)
    county = models.CharField(max_length=50, null=True)
    area = models.CharField(max_length=100, null=True)
    feature_id = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='property/images/')  # Store images in 'media/images/'
    seller = models.ForeignKey(Sellers, on_delete=models.SET_NULL,null=True, blank=True)
    selling_type = models.CharField(max_length=50, null=True)
    reason_selling = models.TextField(null=True)
    sell_leaseback = models.CharField(max_length=3, choices=SELL_LEASEBACK_OPTIONS, null=True)
    leaseback_month = models.FloatField(choices=LEASEBACK_MONTHS, null=True)
    garage_num = models.IntegerField(null=True)
    hoa_fee_qtr = models.DecimalField(max_digits=10, decimal_places=2, null=True)
   
    
    def save(self, *args, **kwargs):
        if self.latitude is not None and self.longitude is not None:
            self.point = Point(self.longitude, self.latitude)  # (lng, lat)
        super().save(*args, **kwargs)

class PropertyAgent(BaseModel):
    SELLERREP = 'SellerRep'
    BUYERREP = 'BuyerRep'
    AGENT_ROLE_TYPES = [
    (SELLERREP , 'SellerRep'),
    (BUYERREP , 'BuyerRep'),
    ]
    propertyagent_id =  models.CharField(max_length=50, default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True) 
    property = models.ForeignKey(PropertiesInfo, on_delete=models.SET_NULL,null=True)
    agent = models.ForeignKey(Agents, on_delete=models.SET_NULL,null=True)
    agent_role =  models.CharField(max_length=20, choices=AGENT_ROLE_TYPES, null=True)

class PropetyFeatures(BaseModel):
    feature_id =  models.CharField(max_length=50,default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True)
    feature_name = models.CharField(max_length=20, null=True) 
    property_conditions = models.CharField(max_length=20, null=True)


class PropertyHistory(BaseModel):
    Price = 'Price changed'
    Ownership = 'Ownership changed'
    CHANGE_TYPES = [
      (Price , 'Price changed'),
     (Ownership , 'Ownership changed')
    ]
    history_id =  models.CharField(max_length=50,default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True)
    property = models.ForeignKey(PropertiesInfo, on_delete=models.SET_NULL,null=True)
    change_date =models.DateField(auto_now=True, editable=True)
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPES, null=True)
    previous_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
