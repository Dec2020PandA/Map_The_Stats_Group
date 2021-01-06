from django.shortcuts import render
from mapTheStats.settings import GOOGLE_MAPS_API_KEY


def home (request):
    context = {
        'gmaps' : GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'home.html', context)
