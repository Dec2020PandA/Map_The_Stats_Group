from django.shortcuts import render, redirect
from pprint import pprint
import requests
from local_library.area_codes import STATE_CODES, COUNTRY_CODES, MSA_CODES, BLS_MSA_CODES
from local_library.api_keys import BEA_API_KEY, GOOGLE_MAPS_API_KEY, CENSUS_API_KEY, WEATHERSTACK_API_KEY




    ## BEA API call for average income for all United States, we can then search the dict for selected state // Must add three zeroes to the end of the selected states ID
    ## BEA API uses 06000 as California's FIPS code, rather than 06, must account for that.
    ## Table: CAINC1
# bea_average_income = "https://apps.bea.gov/api/data/?UserID={bea_key}&method=GetData&datasetname=Regional&TableName=CAINC1&LineCode=3&Year=2019&GeoFips=STATE&ResultFormat=json".format(
#     bea_key=BEA_API_KEY
# )
# bea_response = requests.get(url=bea_average_income)
# bea_content = bea_response.json()
# pprint(f"Location Selected: {bea_content['BEAAPI']['Results']['Data'][0]['GeoName']}\nPer Capita Income: {bea_content['BEAAPI']['Results']['Data'][0]['DataValue']}\nYear: {bea_content['BEAAPI']['Results']['Data'][0]['TimePeriod']}")

#     ## CENSUS API call for percentage of families below poverty level in California
#     ## CENSUS API responses can contain multiple arrays for each city INSIDE of an MSA, must account for this. for loop, skip 0 index.
#     ## Table: acs DP03_0119PE
# census_poverty = "https://api.census.gov/data/2019/acs/acs1/profile?get=NAME,DP03_0119PE&for=state:06&key={census_key}".format(
#     census_key=CENSUS_API_KEY
# )
# census_response = requests.get(url=census_poverty)
# census_content = census_response.json()
# pprint(f"Location Selected: {census_content[1][0]}\n\nPercentage of People living below poverty: {census_content[1][1]}")

#     ## CENSUS API call for estimated population in California // Accesses different database than ACS
#     ## Table: data pep/population
# census_population = "https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=state:06&key={census_key}".format(
#     census_key=CENSUS_API_KEY
# )
# census_response = requests.get(url=census_population)
# census_content = census_response.json()
# pprint(census_content)

#     ## CENSUS API call for unemployment rate in California
#     ## Table: acs DP03_0009PE
# census_unemployment = "https://api.census.gov/data/2019/acs/acs1/profile?get=NAME,DP03_0009PE&for=state:06&key={census_key}".format(
#     census_key=CENSUS_API_KEY
# )
# census_response = requests.get(url=census_unemployment)
# census_content = census_response.json()
# pprint(census_content)

#     ## WEATHERSTACK API call for current weather in Sacramento
#     ## Long/Lat of selected area needs to be carried into views
# weatherstack_current = "http://api.weatherstack.com/current?access_key={weatherstack_key}&query=38.575764,-121.4944&units=f".format(
#     weatherstack_key=WEATHERSTACK_API_KEY
# )
# weatherstack_response = requests.get(url=weatherstack_current)
# weatherstack_content = weatherstack_response.json()
# pprint(f"Location: {weatherstack_content['location']['name']}\nCurrent Temperature: {weatherstack_content['current']['temperature']}")

bls_unemployment = "https://api.bls.gov/publicAPI/v2/timeseries/data/LAUST{state_code}0000000000003?latest=true".format(
        state_code = '42'
    )
bls_response = requests.get(url=bls_unemployment)
bls_content = bls_response.json()
pprint(bls_content['Results']['series'][0]['data'][0]['value'])