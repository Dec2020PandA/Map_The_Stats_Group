from .api_keys import BEA_API_KEY, GOOGLE_MAPS_API_KEY, CENSUS_API_KEY, WEATHERSTACK_API_KEY, BLS_API_KEY
import requests
# Create the URL.
bls_unemployment = "https://api.bls.gov/publicAPI/v2/timeseries/data/?registrationkey=2aabac0a2be3495ea50b1483275b1b92&latest=True"
request.session['loc_id'] = '06'
# Define the payload.
data = {
    "seriesid":[
        "LAUST{state_id}0000000000003"
    ]
}

# Set the headers.
headers = {
    "Content-type": "application/json"
}

# Grab the response.
bls_response = requests.post(
    url=bls_unemployment,
    headers=headers,
    json=data
)

# Parse the response.
bls_content = bls_response.json()

# Grab the data.
series_data = bls_content['Results']['series'][0]['data']

# Loop through the data.
for set_data in series_data:
    print(set_data)

state_id = '06'
# Define the payload.
