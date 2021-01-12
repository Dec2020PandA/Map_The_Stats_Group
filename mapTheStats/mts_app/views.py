from django.shortcuts import render, redirect
from pprint import pprint
import requests
from local_library.area_codes import STATE_CODES, COUNTRY_CODES, MSA_CODES, BLS_MSA_CODES
from local_library.api_keys import BEA_API_KEY, GOOGLE_MAPS_API_KEY, CENSUS_API_KEY, WEATHERSTACK_API_KEY

## RENDERING

def index (request):
    if request.session['loc_type']:
        if request.session['loc_type'] == 'state':
            context = {
                'gmaps' : GOOGLE_MAPS_API_KEY,
                'selected_loc' : request.session['location_selected'],
                'bea_average_income' : request.session['bea_average_income'],
                'census_poverty' : request.session['census_below_poverty'],
                'census_population' : request.session['census_population'],
                'bls_unemployment' : request.session['bls_unemployment']
            }
            for key in request.session.keys():
                if key not 'location_selected' or 'loc_type':
                    del request.session[key]
            return render(request, 'index.html', context)
        else:
            context = {
                'gmaps' : GOOGLE_MAPS_API_KEY,
            }
            return render(request, 'index.html', context)

## LOCATION DECODING

def decipher_location_type(request):
    ## Checks if selected area is a Country first, due to smallest data set.
    if request.method == 'POST':
        for key in COUNTRY_CODES:
            if request.POST['location_name'] == key:
                request.session['loc_type'] = 'country'
                request.session['loc_name'] = key
                request.session['loc_id'] = COUNTRY_CODES[key]
                return redirect('/country_api_call')
        ## Checks if selected area is a State next.
        for key in STATE_CODES:
            if request.POST['location_name'] == key:
                request.session['loc_type'] = 'state'
                request.session['loc_name'] = key
                request.session['loc_id'] = STATE_CODES[key]
                return redirect('/state_api_call')
        ## Checks MSA's last due to larger data set.
        for key in MSA_CODES:
            if request.POST['location_id'] == key:
                request.session['loc_type'] = 'msa'
                request.session['loc_id'] = key
                request.session['loc_name'] = MSA_CODES[key]
                # request.session['long_lat'] = request.POST['long_lat']
                for bls_key in BLS_MSA_CODES:
                    if BLS_MSA_CODES[bls_key] == MSA_CODES[key]:
                        request.session['bls_id'] = bls_key
                return redirect('/MSA_api_call')
        else:
            ## Should redirect to an error page. Something isn't working properly.
            return redirect('/')



## API CALLS

def state_api_call(request):
    ## BEA API call for average income for all United States, we can then search the dict for selected state // Must add three zeroes to the end of the selected states ID
    bea_average_income = "https://apps.bea.gov/api/data/?UserID={bea_key}&method=GetData&datasetname=Regional&TableName=CAINC1&LineCode=3&Year=2019&GeoFips={state_code}000&ResultFormat=json".format(
        bea_key=BEA_API_KEY,
        state_code = request.session['loc_id']
    )
    bea_response = requests.get(url=bea_average_income)
    bea_content = bea_response.json()
    request.session['location_selected'] = bea_content['BEAAPI']['Results']['Data'][0]['GeoName']
    request.session['bea_average_income'] = bea_content['BEAAPI']['Results']['Data'][0]['DataValue']

    ## CENSUS API call for percentage of families below poverty level in California
    census_poverty = "https://api.census.gov/data/2019/acs/acs1/profile?get=NAME,DP03_0119PE&for=state:{state_code}&key={census_key}".format(
        census_key=CENSUS_API_KEY,
        state_code = request.session['loc_id']
    )
    census_response = requests.get(url=census_poverty)
    census_content = census_response.json()
    request.session['census_below_poverty'] = census_content[1][1]

    ## CENSUS API call for estimated population in California // Accesses different database than ACS
    census_population = "https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=state:{state_code}&key={census_key}".format(
        census_key=CENSUS_API_KEY,
        state_code = request.session['loc_id']
    )
    census_response = requests.get(url=census_population)
    census_content = census_response.json()
    request.session['census_population'] = census_content[1][1]

    ## BLS API call for unemployment rate for selected state
    bls_unemployment = "https://api.bls.gov/publicAPI/v2/timeseries/data/LAUST{state_code}0000000000003?latest=true".format(
        state_code = request.session['loc_id']
    )
    bls_response = requests.get(url=bls_unemployment)
    bls_content = bls_response.json()
    request.session['bls_unemployment'] = bls_content['Results']['series'][0]['data'][0]['value']

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
    ## BEA API call for selected MSA average income
    bea_average_income = "https://apps.bea.gov/api/data/?UserID={bea_key}&method=GetData&datasetname=Regional&TableName=CAINC1&LineCode=3&Year=2019&GeoFips={msa_code}&ResultFormat=json".format(
        bea_key=BEA_API_KEY,
        msa_code = request.session['loc_id']
    )
    bea_response = requests.get(url=bea_average_income)
    bea_content = bea_response.json()
    pprint(f"Location Selected: {bea_content['BEAAPI']['Results']['Data'][0]['GeoName']}\nPer Capita Income: {bea_content['BEAAPI']['Results']['Data'][0]['DataValue']}\nYear: {bea_content['BEAAPI']['Results']['Data'][0]['TimePeriod']}")

    ## WEATHERSTACK API call for current weather based on LONG/LAT // Only accessible via MSA
    weatherstack_current = "http://api.weatherstack.com/current?access_key={weatherstack_key}&query={long_lat}&units=f".format(
        weatherstack_key=WEATHERSTACK_API_KEY,
        long_lat = request.session['long_lat']
    )
    weatherstack_response = requests.get(url=weatherstack_current)
    weatherstack_content = weatherstack_response.json()
    pprint(f"Location: {weatherstack_content['location']['name']}\nCurrent Temperature: {weatherstack_content['current']['temperature']}")
