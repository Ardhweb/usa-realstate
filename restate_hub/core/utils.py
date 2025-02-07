from django.http import JsonResponse
from core.models import State,City

def get_state(request):
    states = list(State.objects.values())
    return JsonResponse(states, safe=False)

def get_city_bystate(request,state_id):
    cities = list(City.objects.filter(state__id=state_id).values())
    return JsonResponse(cities, safe=False)