from django.shortcuts import render, redirect
from pprint import pprint
import requests

<<<<<<< HEAD
## API KEYS

BEA_API_KEY = "692B0866-DAF4-4161-B1FE-A1FBEB3C066F"
GOOGLE_MAPS_API_KEY = "AIzaSyDaXQ4lvSyI5ERL6GJjOtvGTpxClWGsDOA"
CENSUS_API_KEY = "51170a508f499d465f5359a5d26af29499a531d3"
WEATHERSTACK_API_KEY = "3f16f995c3281743b7421e3ebad06b7c"

## RENDERING

def index (request):
=======

def home (request):
>>>>>>> a0068d14ba122226a024e52facec547b7bed481b
    context = {
        'gmaps' : GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'index.html', context)

## API CALLS

def state_api_call(request):
    ## BEA API call for average income for all United States, we can then search the dict for selected state // Must add three zeroes to the end of the selected states ID
    ## BEA API uses 06000 as California's FIPS code, rather than 06, must account for that.
    ## Table: CAINC1
    bea_average_income = "https://apps.bea.gov/api/data/?UserID={bea_key}&method=GetData&datasetname=Regional&TableName=CAINC1&LineCode=3&Year=2019&GeoFips={needs_to_be_dynamic}000&ResultFormat=json".format(
        bea_key=BEA_API_KEY
    )
    bea_response = requests.get(url=bea_average_income)
    bea_content = bea_response.json()
    pprint(f"Location Selected: {bea_content['BEAAPI']['Results']['Data'][0]['GeoName']}\nPer Capita Income: {bea_content['BEAAPI']['Results']['Data'][0]['DataValue']}\nYear: {bea_content['BEAAPI']['Results']['Data'][0]['TimePeriod']}")

    ## CENSUS API call for percentage of families below poverty level in California
    ## CENSUS API responses can contain multiple arrays for each city INSIDE of an MSA, must account for this. for loop, skip 0 index.
    ## Table: acs DP03_0119PE
    census_poverty = "https://api.census.gov/data/2019/acs/acs1/profile?get=NAME,DP03_0119PE&for=state:{needs_to_be_dynamic}&key={census_key}".format(
        census_key=CENSUS_API_KEY
    )
    census_response = requests.get(url=census_poverty)
    census_content = census_response.json()
    pprint(f"Location Selected: {census_content[1][0]}\n\nPercentage of People living below poverty: {census_content[1][1]}")

    ## CENSUS API call for estimated population in California // Accesses different database than ACS
    ## Table: data pep/population
    census_population = "https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=state:{needs_to_be_dynamic}&key={census_key}".format(
        census_key=CENSUS_API_KEY
    )
    census_response = requests.get(url=census_population)
    census_content = census_response.json()
    pprint(census_content)

    ## CENSUS API call for unemployment rate in California
    ## Table: acs DP03_0009PE
    ## WE MAY WANT TO TRANSITION OVER TO THE BLS API FOR THIS STATISTIC TO BE UP TO DATE
    census_unemployment = "https://api.census.gov/data/2019/acs/acs1/profile?get=NAME,DP03_0009PE&for=state:{needs_to_be_dynamic}&key={census_key}".format(
        census_key=CENSUS_API_KEY
    )
    census_response = requests.get(url=census_unemployment)
    census_content = census_response.json()
    pprint(census_content)

def country_api_call(request):
    ## Entire US average income // Notes above
    bea_average_income = "https://apps.bea.gov/api/data/?UserID={bea_key}&method=GetData&datasetname=Regional&TableName=CAINC1&LineCode=3&Year=2019&GeoFips=STATE&ResultFormat=json".format(
        bea_key=BEA_API_KEY
    )
    bea_response = requests.get(url=bea_average_income)
    bea_content = bea_response.json()
    pprint(f"Location Selected: {bea_content['BEAAPI']['Results']['Data'][0]['GeoName']}\nPer Capita Income: {bea_content['BEAAPI']['Results']['Data'][0]['DataValue']}\nYear: {bea_content['BEAAPI']['Results']['Data'][0]['TimePeriod']}")

    ## Entire US percentage living below poverty // Notes above
    census_poverty = "https://api.census.gov/data/2019/acs/acs1/profile?get=NAME,DP03_0119PE&for=us:1&key={census_key}".format(
        census_key=CENSUS_API_KEY
    )
    census_response = requests.get(url=census_poverty)
    census_content = census_response.json()
    pprint(f"Location Selected: {census_content[1][0]}\n\nPercentage of People living below poverty: {census_content[1][1]}")

    ## Entire US population // Notes above
    census_population = "https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=us:1&key={census_key}".format(
        census_key=CENSUS_API_KEY
    )
    census_response = requests.get(url=census_population)
    census_content = census_response.json()
    pprint(census_content)

    ## Entire US unemployment rate average // Notes above
    census_unemployment = "https://api.census.gov/data/2019/acs/acs1/profile?get=NAME,DP03_0009PE&for=us:1&key={census_key}".format(
        census_key=CENSUS_API_KEY
    )
    census_response = requests.get(url=census_unemployment)
    census_content = census_response.json()
    pprint(census_content)

def msa_api_call(request):
    ## MSA average income, GeoFips must match MSA codes, that we can access via local_library
    bea_average_income = "https://apps.bea.gov/api/data/?UserID={bea_key}&method=GetData&datasetname=Regional&TableName=CAINC1&LineCode=3&Year=2019&GeoFips={needs_to_be_dynamic}&ResultFormat=json".format(
        bea_key=BEA_API_KEY
    )
    bea_response = requests.get(url=bea_average_income)
    bea_content = bea_response.json()
    pprint(f"Location Selected: {bea_content['BEAAPI']['Results']['Data'][0]['GeoName']}\nPer Capita Income: {bea_content['BEAAPI']['Results']['Data'][0]['DataValue']}\nYear: {bea_content['BEAAPI']['Results']['Data'][0]['TimePeriod']}")

    ## WEATHERSTACK API call for current weather based on LONG/LAT // Only accessible via MSA
    ## Long/Lat of selected area needs to be carried into views, and hence dynamically applied via a variable // first iteration of website will
    ## Likely only handle Country, States, and MSA's, so the longitude and latitude of current weather needs to be applied to the currently selected MSA.
    weatherstack_current = "http://api.weatherstack.com/current?access_key={weatherstack_key}&query={needs_to_be_dynamic}&units=f".format(
        weatherstack_key=WEATHERSTACK_API_KEY
    )
    weatherstack_response = requests.get(url=weatherstack_current)
    weatherstack_content = weatherstack_response.json()
    pprint(f"Location: {weatherstack_content['location']['name']}\nCurrent Temperature: {weatherstack_content['current']['temperature']}")
