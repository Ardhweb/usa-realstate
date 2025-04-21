from django.apps import AppConfig
from django.db import models

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # def ready(self):
    #     import accounts.signal  # Make sure signals are imported
    
  