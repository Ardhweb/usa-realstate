from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from seller_module.models import Sellers
from property_module.models import PropertiesInfo
from accounts.models import User
# Create your views here.
from django.http import JsonResponse,Http404,HttpResponseNotFound
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from membership_module.models import MembershipFee, MemberAddress
from buyer_module.models import Buyers
from agent_module.models import Agents
from django.db.models import F
from django.forms.models import model_to_dict

@login_required() 
def admin_custom_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        total_users = User.objects.exclude(is_superuser=True).exclude(is_staff=True).count()
        total_property = PropertiesInfo.objects.count()
        sold_property = PropertiesInfo.objects.filter(listing_status='sold').count()
        context = {'active_page':'dashboard',
         "total_property":total_property,
         'sold_property': sold_property,
         "total_users":total_users ,
        }

        return render(request, "members/dashboard.html", context)
    else:
         return HttpResponseNotFound(render(request, "error/404.html"))

