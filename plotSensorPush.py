import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os
import io
import csv
import requests
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime, timedelta


def generate_timestamps(start_date, end_date):
    # Assuming daily intervals for simplicity
    current_date = start_date
    while current_date < end_date:
        yield int(current_date.timestamp()), int((current_date + timedelta(days=1)).timestamp())
        current_date += timedelta(days=1)

#####################################################################
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
        LLNLdata = []
        reader = csv.DictReader(io.StringIO(response.text), delimiter='\t', fieldnames=['date', 'temperature', 'humidity'])
        next(reader)  # Skip header row
        for row in reader:
            if row['temperature']:  # Check if 'temperature' is not empty
                LLNLdata.append({'date': row['date'], 'temperature': float(row['temperature'])})
            else:
                print(f"Skipping row with empty temperature: {row}")
        return LLNLdata
    else:
        print(f"Failed to fetch data: HTTP {response.status_code}")
        return None
    
#####################################################################
def fetch_QuestWeatherStation_data(start_timestamp, end_timestamp):
    API_KEY = 'gr6jeugtsob9hlqaheg7q0fg8ffcby2p'
    API_SECRET = 'y1eefxv2sq1nrhjzekdlgu8bgdjtqf4i'
    STATION_ID = '113636'
    URL = f"https://api.weatherlink.com/v2/historic/{STATION_ID}?api-key={API_KEY}&start-timestamp={start_timestamp}&end-timestamp={end_timestamp}"
    headers = {'X-Api-Secret': API_SECRET}
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for timestamps {start_timestamp} to {end_timestamp}")
        return None


#####################################################################
#####################################################################

if __name__ == '__main__':
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    temperatures_api = []
    timestamps_api = []

    LLNLdata = fetch_llnl_weather_data(start_date, end_date)

    LLNLdates = [datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S') for entry in LLNLdata]
    LLNLtemperatures = [entry['temperature'] for entry in LLNLdata]  # Corrected line
  
    

    for start_timestamp, end_timestamp in generate_timestamps(start_date, end_date):
        data = fetch_QuestWeatherStation_data(start_timestamp, end_timestamp)
        if data and 'sensors' in data:
            for sensor in data['sensors']:
                for record in sensor['data']:
                    if 'temp_out' in record and 'ts' in record:
                        temperatures_api.append(((record['temp_out']-32.)/1.8))
                        timestamps_api.append(datetime.fromtimestamp(record['ts']))


   

    # Define the file paths
    file1 = './data/Sensor10.csv'
    file2 = './data/Sensor2.csv'

    # Specify column names manually for CSV files
    column_names = ['Timestamp', 'Temperature (A°C)', 'Relative Humidity (%)']

    # Read the data from the CSV files
    df1 = pd.read_csv(file1, skiprows=1, header=None, names=column_names, parse_dates=['Timestamp'], index_col='Timestamp')
    df2 = pd.read_csv(file2, skiprows=1, header=None, names=column_names, parse_dates=['Timestamp'], index_col='Timestamp')

    # Initialize the plot
    plt.figure(figsize=(12, 6))

    # Plot the data from the first file
    plt.plot(df1.index, df1['Temperature (A°C)'], marker='', linestyle='-', label='Sensor10')

    # Plot the data from the second file
    plt.plot(df2.index, df2['Temperature (A°C)'], marker='', linestyle='-', label='Sensor2')

    plt.plot(timestamps_api, temperatures_api, label='Quest Stockman\'s Park', linestyle='-', marker='')

    plt.plot(LLNLdates, LLNLtemperatures, marker='', linestyle='-', color='y', label='LLNL Station')


    # Formatting the plot
    plt.title('Temperature as a Function of Time from Multiple Sensors')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Show plot
    plt.show()
