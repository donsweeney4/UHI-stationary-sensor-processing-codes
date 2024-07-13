import zipfile
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def generate_timestamps(start_date, end_date):
    # Assuming daily intervals for simplicity
    current_date = start_date
    while current_date < end_date:
        yield int(current_date.timestamp()), int((current_date + timedelta(days=1)).timestamp())
        current_date += timedelta(days=1)

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

if __name__ == '__main__':
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    temperatures_api = []
    timestamps_api = []

    for start_timestamp, end_timestamp in generate_timestamps(start_date, end_date):
        data = fetch_QuestWeatherStation_data(start_timestamp, end_timestamp)
        if data and 'sensors' in data:
            for sensor in data['sensors']:
                for record in sensor['data']:
                    if 'temp_out' in record and 'ts' in record:
                        temperatures_api.append(((record['temp_out']-32.)/1.8))
                        timestamps_api.append(datetime.fromtimestamp(record['ts']))

    plt.plot(timestamps_api, temperatures_api, label='Quest Stockman\'s Park', linestyle='-', marker='')

    plt.title('Temperature Data from Quest Weather Station')
    plt.xlabel('Time')
    plt.ylabel('Temperature (C)')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=12))
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()