from django.shortcuts import render ,redirect

# Create your views here.

def seller_dashboard(request):
    if request.user.is_authenticated and user.member_type == 'seller':
        return render(request, "seller/dashboard.html")
    else:
        return redirect('home')