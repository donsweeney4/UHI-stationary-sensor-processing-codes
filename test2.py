import requests
import pandas as pd
from datetime import datetime, timedelta

# Define the base URL and headers for the API request
base_url = 'https://www.ncei.noaa.gov/access/services/data/v1'
headers = {
    'token': 'ibZkfScUExKVfxypvvWGIomaKgsPuRKy'
}

# Define the date range for the past week
end_date = datetime.today()
start_date = end_date - timedelta(days=14)

# Define parameters for the API request
params = {
    'dataset': 'daily-summaries',  # GHCN daily dataset       daily-summaries
    'stations': 'USW00023271',  # Station ID for Livermore Municipal Airport
    'startDate': start_date.strftime('%Y-%m-%d'),
    'endDate': end_date.strftime('%Y-%m-%d'),
    'dataTypes': 'TMAX,TMIN,PRCP',  # Data types: max temp, min temp, precipitation
    'format': 'json',
    'includeAttributes': 'false',
    'units': 'standard'
}

# Make the API request
response = requests.get(base_url, headers=headers, params=params)

# Check the status code and handle errors
if response.status_code != 200:
    print(f"Error fetching data: {response.status_code}")
    print(f"Response body: {response.text}")
    raise Exception(f"Error fetching data: {response.status_code}")

# Parse the JSON response
data = response.json()

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Print the results
print(df)
