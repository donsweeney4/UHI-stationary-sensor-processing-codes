# see https://weatherlink.github.io/v2-api/tutorial

import requests

# Constants

API_KEY = 'gr6jeugtsob9hlqaheg7q0fg8ffcby2p'
API_SECRET = 'y1eefxv2sq1nrhjzekdlgu8bgdjtqf4i'



URL = f"https://api.weatherlink.com/v2/stations?api-key={API_KEY}"

# Headers
headers = {
    'X-Api-Secret': API_SECRET
}

# Make the GET request
response = requests.get(URL, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Process the JSON data
    data = response.json()
    print(data)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")