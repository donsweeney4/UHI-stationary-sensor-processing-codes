# see https://weatherlink.github.io/v2-api/tutorial

import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# Constants
API_KEY = 'gr6jeugtsob9hlqaheg7q0fg8ffcby2p'
API_SECRET = 'y1eefxv2sq1nrhjzekdlgu8bgdjtqf4i'
STATION_ID = '113636'

# Function to generate UNIX timestamps for the start and end of each day in the past week
def generate_timestamps():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    for single_date in pd.date_range(start=start_date, end=end_date, freq='D'):
        yield int(single_date.timestamp()), int((single_date + timedelta(days=1) - timedelta(seconds=1)).timestamp())

# Function to fetch data
def fetch_data(start_timestamp, end_timestamp):
    URL = f"https://api.weatherlink.com/v2/historic/{STATION_ID}?api-key={API_KEY}&start-timestamp={start_timestamp}&end-timestamp={end_timestamp}"
    headers = {'X-Api-Secret': API_SECRET}
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for timestamps {start_timestamp} to {end_timestamp}")
        return None

# Main
def main():
    temperatures = []
    timestamps = []

    for start_timestamp, end_timestamp in generate_timestamps():
        data = fetch_data(start_timestamp, end_timestamp)
        #print(data)  # This prints the entire fetched data
        if data and 'sensors' in data:
            for sensor in data['sensors']:
                for record in sensor['data']:
                    # Assuming 'temp_out' is the key for temperature in the output
                    if 'temp_out' in record and 'ts' in record:
                        temperatures.append(record['temp_out'])
                        timestamps.append(datetime.fromtimestamp(record['ts']))
                        print(f"Timestamp: {datetime.fromtimestamp(record['ts'])}, Temperature: {record['temp_out']}")

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, temperatures, label='Temperature')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature at Quest Science Center Over the Past Week')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()