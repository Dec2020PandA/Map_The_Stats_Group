from django.shortcuts import render, redirect
from pprint import pprint
import requests

## API KEYS

BEA_API_KEY = "692B0866-DAF4-4161-B1FE-A1FBEB3C066F"
GOOGLE_MAPS_API_KEY = "AIzaSyDaXQ4lvSyI5ERL6GJjOtvGTpxClWGsDOA"
CENSUS_API_KEY = "51170a508f499d465f5359a5d26af29499a531d3"

## RENDERING

def index (request):
    context = {
        'gmaps' : GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'index.html', context)

## API CALLS

def state_api_call(response):
    ## BEA API call for average income for all United States, we can then search the dict for selected state // Must add three zeroes to the end of the selected states ID
    ## BEA API uses 06000 as California's FIPS code, rather than 06, must account for that.
    ## Table: CAINC1
    bea_average_income = "https://apps.bea.gov/api/data/?UserID={bea_key}&method=GetData&datasetname=Regional&TableName=CAINC1&LineCode=3&Year=2019&GeoFips=STATE&ResultFormat=json".format(
        bea_key=BEA_API_KEY
    )
    bea_response = requests.get(url=bea_average_income)
    bea_content = bea_response.json()
    pprint(f"Location Selected: {bea_content['BEAAPI']['Results']['Data'][0]['GeoName']}\nPer Capita Income: {bea_content['BEAAPI']['Results']['Data'][0]['DataValue']}\nYear: {bea_content['BEAAPI']['Results']['Data'][0]['TimePeriod']}")

    ## CENSUS API call for percentage of families below poverty level in California // Table: DP03_0119PE
    census_poverty = "https://api.census.gov/data/2019/acs/acs1/profile?get=NAME,DP03_0119PE&for=state:06&key={census_key}".format(
        census_key=CENSUS_API_KEY
    )
    census_response = requests.get(url=census_poverty)
    census_content = census_response.json()
    pprint(f"Location Selected: {census_content[1][0]}\n\nPercentage of People living below poverty: {census_content[1][1]}")

    ## CENSUS API call for estimated population in California // Accesses different database than ACS
    ## Table: pep/population
    census_population = "https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=state:06&key={census_key}".format(
        census_key=CENSUS_API_KEY
    )
    census_response = requests.get(url=census_population)
    census_content = census_response.json()
    pprint(census_content)
