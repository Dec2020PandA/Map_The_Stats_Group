from django.shortcuts import render, redirect
from mapTheStats.settings import GOOGLE_MAPS_API_KEY, BEA_API_KEY
from local_library.area_codes import *
from pprint import pprint
import requests


## RENDERING

def index (request):
    context = {
        'gmaps' : GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'index.html', context)

## API CALLS

def api_call(request):
    url = "https://apps.bea.gov/api/data/?UserID={api_key}&method=GetData&datasetname=Regional&TableName=CAINC1&LineCode=3&Year=2019&GeoFips=STATE&ResultFormat=json".format(
    api_key=BEA_API_KEY
    )
    response = requests.get(url=url)
    content = response.json()
    pprint(f"Location Selected: {content['BEAAPI']['Results']['Data'][0]['GeoName']}\nPer Capita Income: {content['BEAAPI']['Results']['Data'][0]['DataValue']}\nYear: {content['BEAAPI']['Results']['Data'][0]['TimePeriod']}")
    return redirect('/')