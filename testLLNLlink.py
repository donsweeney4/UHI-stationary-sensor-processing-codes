import requests
from datetime import datetime, timedelta

from datetime import datetime, timedelta

# Calculate dates
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

# Format dates as strings in 'YYYY-MM-DD' format
formatted_start_date = start_date.strftime('%Y-%m-%d')
formatted_end_date = end_date.strftime('%Y-%m-%d')

# Modified dictionary with dates

# Define the base URL and parameters
base_url = 'https://weather.llnl.gov/cgi-pub/reports/report_export.pl'
params = {
    'format': 'tsv',
    'instrument_ids': '350,375',
    'alt_units': '',
    'min': '0',
    'max': '0',
    'avg': '1',
    'data_resolution': 'full',
    'start_date': formatted_start_date,
    'end_date': formatted_end_date
}

# Make the GET request
response = requests.get(base_url, params=params)

# Print the status code and content for debugging
print(f"Status Code: {response.status_code}")
print(f"Response Content: {response.text}")
