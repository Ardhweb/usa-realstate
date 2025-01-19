from django.db import models
# Create your models here.
from core.models import BaseModel
import shortuuid
from seller_module.models import Sellers
from agent_module.models import Agents

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

    YES = 'Yes'
    NO = 'No'

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

    property_id =  models.UUIDField(default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True) 
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, null=True)
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
    postal_code = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=100, null=True)
    county = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=100, null=True)
    zipcode4 = models.CharField(max_length=10, null=True)
    feature_id = models.IntegerField(null=True)
    image_id = models.IntegerField(null=True)# Does we assigning only single image in that case we needs to change something
    seller = models.ForeignKey(Sellers, on_delete=models.SET_NULL,null=True)
    selling_type = models.CharField(max_length=50, null=True)
    reason_selling = models.TextField(null=True)
    sell_leaseback = models.CharField(max_length=3, choices=SELL_LEASEBACK_OPTIONS, null=True)
    leaseback_month = models.FloatField(choices=LEASEBACK_MONTHS, null=True)
    garage_num = models.IntegerField(null=True)
    hoa_fee_qtr = models.DecimalField(max_digits=10, decimal_places=2, null=True)


class PropertyAgent(BaseModel):
    SELLERREP = 'SellerRep'
    BUYERREP = 'BuyerRep'
    AGENT_ROLE_TYPES = [
    (SELLERREP , 'SellerRep'),
    (BUYERREP , 'BuyerRep'),
    ]
    propertyagent_id =  models.UUIDField(default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True) 
    property = models.ForeignKey(PropertiesInfo, on_delete=models.SET_NULL,null=True)
    agent = models.ForeignKey(Agents, on_delete=models.SET_NULL,null=True)
    agent_role =  models.CharField(max_length=20, choices=AGENT_ROLE_TYPES, null=True)

class PropetyFeatures(BaseModel):
    feature_id =  models.UUIDField(default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True)
    feature_name = models.CharField(max_length=20, null=True) 
    property_conditions = models.CharField(max_length=20, null=True)


class PropertyHistory(BaseModel):
    Price = 'Price changed'
    Ownership = 'Ownership changed'
    CHANGE_TYPES = [
      (Price , 'Price changed'),
     (Ownership , 'Ownership changed')
    ]
    history_id =  models.UUIDField(default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True)
    property = models.ForeignKey(PropertiesInfo, on_delete=models.SET_NULL,null=True)
    change_date =models.DateField(auto_now=True, editable=True)
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPES, null=True)
    previous_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)

class PropertyLocation(BaseModel):
    location_id = models.UUIDField(default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True)
    property = models.ForeignKey(PropertiesInfo, on_delete=models.SET_NULL,null=True)
    city  = models.CharField(max_length=50, blank=False, null=True)
    country  = models.CharField(max_length=50, blank=False, null=True)
    region = models.CharField(max_length=50, blank=False, null=True)
    postal_code = models.CharField(max_length=50, blank=False, null=True)
