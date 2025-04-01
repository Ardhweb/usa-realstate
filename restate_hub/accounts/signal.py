from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from transactions_module.helcim import create_customer_helcim,CustomerDataService





@receiver(post_save, sender=User)
def post_create_customer_helcim_db(sender, instance, created, **kwargs):
    if created:
        customer_data = customer_service.get_customer_data()
        customer_service = CustomerDataService(request.user)
        print(customer_data)
        customer = create_customer_helcim(usr_data=customer_data)
        print(customer)

        print(f"New instance of {sender.__name__} created: {instance}")
    else:
        print(f"Instance of {sender.__name__} updated: {instance}")
