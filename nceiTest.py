import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the base URL and headers for the API request
base_url = 'https://www.ncei.noaa.gov/access/services/data/v1'
headers = {
    'token': 'ibZkfScUExKVfxypvvWGIomaKgsPuRKy'  # Replace with your actual API token
}

# Define the date range for the past week
end_date = datetime.today()
start_date = end_date - timedelta(days=7)

# Define parameters for the API request
params = {
    'dataset': 'GHCNh',  # Integrated Surface Dataset
 #   'dataset': 'ISD',  # Integrated Surface Dataset
    'stations': 'USW00023271',  # Station ID for Livermore Municipal Airport
    'startDate': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
    'endDate': end_date.strftime('%Y-%m-%dT%H:%M:%S'),
    'dataTypes': 'ALL',  # All available data types
    'format': 'json',
    'includeAttributes': 'false',
    'units': 'standard'
}

# Make the API request
response = requests.get(base_url, headers=headers, params=params)

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

# Convert date string to datetime object
df['DATE'] = pd.to_datetime(df['DATE'])

# Filter the DataFrame to keep only temperature and humidity data
df_filtered = df[df['datatype'].isin(['TEMP', 'RHUM'])]

# Pivot the data to have date as index and data types as columns
df_pivot = df_filtered.pivot(index='DATE', columns='datatype', values='value')

# Plot the data
plt.figure(figsize=(12, 6))

# Plot temperature
plt.subplot(2, 1, 1)
plt.plot(df_pivot.index, df_pivot['TEMP'], label='Temperature (F)')
plt.xlabel('Date')
plt.ylabel('Temperature (F)')
plt.title('Temperature Data for Livermore Airport - Last Week')
plt.grid(True)
plt.legend()

# Plot humidity
plt.subplot(2, 1, 2)
plt.plot(df_pivot.index, df_pivot['RHUM'], label='Relative Humidity (%)')
plt.xlabel('Date')
plt.ylabel('Relative Humidity (%)')
plt.title('Humidity Data for Livermore Airport - Last Week')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
