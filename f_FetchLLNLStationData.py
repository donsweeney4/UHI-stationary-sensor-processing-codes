import requests
import csv
import io
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the date range for the last month
end_date = datetime.today()
start_date = end_date - timedelta(days=30)


# Function to fetch and process LLNL weather data
def fetch_llnl_weather_data(start_date, end_date):
    formatted_start_date = start_date.strftime('%Y-%m-%d')
    formatted_end_date = end_date.strftime('%Y-%m-%d')

    url = 'https://weather.llnl.gov/cgi-pub/reports/report_export.pl'

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
    response = requests.get(url, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text[:100]}")  # Print only the first 100 characters for brevity

    if response.status_code == 200:
        data = []
        reader = csv.DictReader(io.StringIO(response.text), delimiter='\t', fieldnames=['date', 'temperature', 'humidity'])
        next(reader)  # Skip header row
        for row in reader:
            if row['temperature']:  # Check if 'temperature' is not empty
                data.append({'date': row['date'], 'temperature': float(row['temperature'])})
            else:
                print(f"Skipping row with empty temperature: {row}")
        return data
    else:
        print(f"Failed to fetch data: HTTP {response.status_code}")
        return None


# Function to plot temperature data
def plot_temperature(data):
    # Assuming data is a list of dictionaries with 'date' and 'temperature' keys

    dates = [datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S') for entry in data]
    temperatures = [entry['temperature'] for entry in data]  # Corrected line
    plt.figure(figsize=(10, 5))
    plt.plot(dates, temperatures, marker='', linestyle='-', color='b')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Data from LLNL Weather Station')
    plt.grid(True)
    plt.legend()
    plt.show()

# Fetch the weather data
# Define the date range for the last week
end_date = datetime.today()
start_date = end_date - timedelta(days=7)

print(end_date)
print(start_date)  

weather_data = fetch_llnl_weather_data(start_date, end_date)

# Plot the temperature data
plot_temperature(weather_data)


