from django.shortcuts import render

# Create your views here.
def property_listing(request):
    return render(request,'property/listing.html')