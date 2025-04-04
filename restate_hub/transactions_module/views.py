from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
# Create your views here.
from transactions_module.helcim import  CustomerDataService ,checkout_session , create_subscription, get_customer , create_customer_helcim

from transactions_module.paymone import capture_payment_info ,generate_idempotency_key
from  .models import HelcimInfo
from membership_module.models import SubscriptionPlans

def checkout(request):
    #customer_data = customer_service.get_customer_data()
    #customer_service = CustomerDataService(request.user)
    #print(customer_data)
    checkoutcode = None
    # checkoutcode = checkout_session(usr_id=request.user.id)
    # print(checkoutcode)
    return render(request, "transaction/checkout.html", {'checkoutcode':checkoutcode})



def subscribe_process(request):
    #customer = get_customer(usr_id=request.user.id)  # Call get_customer
    
    #if isinstance(customer, dict) and "errors" in customer and customer["errors"] == "Invalid customerId":
        # then we create customer
    data = {
        "full_name": f"Dssdsdsd",
        "email": f"johndoe@example.com",
        "customerCode": f"CST2010084"
    }
    customer = create_customer_helcim(usr_data=data)
    print(customer)
        #create checkout token
       # checkoutcode = checkout_session(usr_id=request.user.id)


    return render(request, "transaction/subscribe.html")

from django.shortcuts import redirect

'''
def process_setup(request):
    
    if not HelcimInfo.objects.filter(user_id=request.user.id).exists():
        data = {
            "email": request.user.email,
            "customerCode": f"CST{request.user.id}",
            "full_name": f"{request.user.first_name} {request.user.last_name}",
        }

        customer_response = create_customer_helcim(usr_data=data)
        print(customer_response)

        # Proceed only if customer creation was successful (status 200 or 201)
        if customer_response.get("status_code") in [200, 201] and "data" in customer_response:
            customer_data = customer_response["data"]
            HelcimInfo.objects.update_or_create(
                user=request.user,
                customerId=customer_data.get("customerId", ""),
                customercode=data["customerCode"]
            )

        return redirect(request.META.get("HTTP_REFERER", "profile"))
    else:
        
        return render(request ,'transaction/process-setup.html')
'''

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
    checkoutCode = checkout_session(usr_id=request.user.id)
    return render(request, "transaction/checkoutSession.html", {'checkoutCode':checkoutCode})

def confirm_subscription(request):
    if request.method == "POST":
        # Fetch subscription plan
        plan = get_object_or_404(SubscriptionPlans, member_type=request.user.member_type)
        
        # Fetch Helcim info
        hInfo = get_object_or_404(HelcimInfo, user=request.user)
        
        # Create subscription
        subscribe = create_subscription(
            paymentPlanId=plan.paymentPlan,
            dateActive=hInfo.signup_date,
            usr_id=request.user.id
        )
        
        match subscribe.get("status_code"):
            case 200 | 201 if "data" in subscribe:
                subscribe_data = subscribe["data"]
                hInfo.is_subscribed = True
                hInfo.subscriptionId = subscribe_data.get("id", "")  # Fixed access issue
                hInfo.save()

        return redirect("membership_module:profile")
    
    return render(request, "transaction/confirm_subscription.html")
