from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
# Create your views here.
from transactions_module.helcim import test_connection,  CustomerDataService ,checkout_session , create_subscription, get_customer , create_customer_helcim
from  .models import HelcimInfo
from membership_module.models import SubscriptionPlans
from django.shortcuts import redirect


def process_setup(request):
    if request.method == 'POST':
        match HelcimInfo.objects.filter(user_id=request.user.id).exists():
            case False:  # Equivalent to 'if not exists'
                data = {
                    "email": request.user.email,
                    "customerCode": f"CST{request.user.id}",
                    "full_name": f"{request.user.first_name} {request.user.last_name}",
                }

                customer_response = create_customer_helcim(usr_data=data)
                print(customer_response)

                # Check response status using match-case
                match customer_response.get("status_code"):
                    case 200 | 201 if "data" in customer_response:
                        customer_data = customer_response["data"]
                        HelcimInfo.objects.update_or_create(
                            user=request.user,
                            customerId=customer_data.get("customerId", ""),
                            customercode=data["customerCode"]
                        )
                        return redirect('transactions_module:process_checkout_add_card')

            case True:
                return redirect(request.META.get("HTTP_REFERER", "profile"))
    else:
        plans = SubscriptionPlans.objects.all()
        return render(request, 'transaction/process-setup.html',{"plans":plans})



def process_checkout_add_card(request):
    helcim = HelcimInfo.objects.filter(user_id=request.user.id).exists()

    return render(request, "transaction/checkoutSession.html")



def test_page(request):
    test_connection()
    return render(request, "transaction/test.html")