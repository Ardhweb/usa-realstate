from django.db import models

# Create your models here.

class MyModel(models.Model):
    name = models.CharField(max_length=100)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


