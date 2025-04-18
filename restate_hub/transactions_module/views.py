from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
# Create your views here.
from transactions_module.helcim import test_helcim_connection,checkout_session , create_subscription, get_customer , create_customer_helcim
from  .models import HelcimInfo
from membership_module.models import SubscriptionPlans
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required()
def process_setup(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    connection_response = test_helcim_connection()
    if connection_response.get("status_code") != 200:
        # 🔁 Redirect somewhere else if connection fails
        messages.error("Helcim connection has failed!")
        return redirect('membership_module:profile')  # e.g. 'profile' or a dedicated error page
    plans = SubscriptionPlans.objects.all()  # Always define it for GET or fallback render
    if request.method == 'POST':
        match HelcimInfo.objects.filter(user_id=request.user.id).exists():
            case False:
                data = {
                    "email": request.user.email,
                    "customerCode": f"CST{request.user.id}",
                    "full_name": f"{request.user.first_name} {request.user.last_name}",
                    "street1": f'{request.user.member_address.street_no}',
                    "street2": f'{request.user.member_address.street_name}',
                    "city": f"{request.user.member_address.city.name}",
                    "province": f'{request.user.member_address.state.code}',
                    "country": "USA",
                    "postalCode":f"{request.user.member_address.zip_code}",
                    'phone':int(request.user.contact_no)
                }
                customer_response = create_customer_helcim(usr_data=data)
                match customer_response.get("status_code"):
                    case 200 | 201 if "data" in customer_response:
                        customer_data = customer_response["data"]
                        HelcimInfo.objects.update_or_create(
                            user=request.user,
                            customerId=customer_data.get("customerId", ""),
                            customercode=data["customerCode"]
                        )
                        return redirect('transactions_module:process_checkout_add_card')
                    case _:
                        return render(request, 'transaction/process-setup.html', {
                            "plans": plans,
                            "error": "Failed to create Helcim customer. Please try again."
                        })

            case True:
                return redirect(request.META.get("HTTP_REFERER", "profile"))

    else:
        # GET request
        return render(request, 'transaction/process-setup.html', {"plans": plans})

@login_required()
def process_checkout_add_card(request):
    helcim = HelcimInfo.objects.filter(user_id=request.user.id).exists()

    return render(request, "transaction/checkoutSession.html")



