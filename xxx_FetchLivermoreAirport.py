import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the base URL and parameters for the API request
base_url = 'https://www.ncei.noaa.gov/access/services/data/v1'
headers = {
    'token': 'ibZkfScUExKVfxypvvWGIomaKgsPuRKy'  # Replace with your actual API token
}

# Define the date range for the past week
end_date = datetime.today()
start_date = end_date - timedelta(days=7)

params = {
    'dataset': 'GHCND',  # Automated Surface Observing Systems dataset
    'stations': 'GHCND:USW00023271',  # Replace with the station ID for Livermore Airport
    'startDate': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
    'endDate': end_date.strftime('%Y-%m-%dT%H:%M:%S'),
    'dataTypes': ['TEMP', 'RHUM'],  # Temperature and Relative Humidity
    'format': 'json',
    'includeAttributes': 'false',
    'units': 'standard',
    'interval': '15'  # 15-minute interval
}

# Make the API request
response = requests.get(base_url, headers=headers, params=params)

# Check the status code
if response.status_code != 200:
    # Print the response body for more details on the error
    print(f"Error fetching data: {response.status_code}")
    print(f"Response body: {response.text}")
    raise Exception(f"Error fetching data: {response.status_code}")
else:
    # Parse the JSON response
    data = response.json()

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Convert date string to datetime object
df['DATE'] = pd.to_datetime(df['DATE'])

# Plot the data
plt.figure(figsize=(12, 6))

# Plot temperature
plt.subplot(2, 1, 1)
plt.plot(df['DATE'], df['TEMP'], label='Temperature (F)')
plt.xlabel('Date')
plt.ylabel('Temperature (F)')
plt.title('Temperature Data for Livermore Airport - Last Week')
plt.grid(True)
plt.legend()

# Plot humidity
plt.subplot(2, 1, 2)
plt.plot(df['DATE'], df['RHUM'], label='Relative Humidity (%)')
plt.xlabel('Date')
plt.ylabel('Relative Humidity (%)')
plt.title('Humidity Data for Livermore Airport - Last Week')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
