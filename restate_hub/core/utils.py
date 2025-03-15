from django.http import JsonResponse
from core.models import State,City,County

# def get_state(request):
#     states = list(State.objects.values())
#     return JsonResponse(states, safe=False)

# def get_city_bystate(request,state_id):
#     cities = list(City.objects.filter(state__id=state_id).values())
#     return JsonResponse(cities, safe=False)

# def get_counties_bystate(request,state_id):
#     counties = list(County.objects.filter(state__id=state_id).values())
#     return JsonResponse(counties, safe=False)