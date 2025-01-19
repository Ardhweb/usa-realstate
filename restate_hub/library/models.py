from django.db import models
from core.models import BaseModel
import shortuuid

# Create your models here.
class Images(BaseModel):
    image_id = models.UUIDField(default=shortuuid.ShortUUID().random(length=22), editable=False, blank=True, null=True) 
    image_url = models.URLField(max_length=500)
    image_type = models.CharField(max_length=50, blank=True, null=True)
    property_id = models.BigIntegerField(blank=False, null=True) # needs to chnage into fk near future.
   
