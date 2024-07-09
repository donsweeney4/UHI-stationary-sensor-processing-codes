import plotly.graph_objs as go
from flask import Flask, render_template
import pandas as pd
from datetime import datetime, timedelta
import requests
import csv
import io
import gunicorn

###########################################################################
def generate_timestamps(start_date, end_date):
    current_date = start_date
    while current_date < end_date:
        yield int(current_date.timestamp()), int((current_date + timedelta(days=1)).timestamp())
        current_date += timedelta(days=1)

###########################################################################
def fetch_airport_weather_data(start_date, end_date):
    # Replace 'YOUR_TRIAL_API_KEY' with your actual trial API key
    API_KEY = 'f4b2bc4e96f14522bd502646240507'
    LOCATION = 'Livermore, CA'
    NUM_DAYS = 7

    # Generate the date strings for the past 1 day
    end_date = datetime.now()
    start_date = end_date - timedelta(days=NUM_DAYS)

    # Format dates as 'YYYY-MM-DD'
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # API endpoint for historical weather data
    url = f"http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={API_KEY}&q={LOCATION}&format=json&date={start_date_str}&enddate={end_date_str}&tp=1"

    # Fetch the data
    response = requests.get(url)
    airportData = response.json()   
    return airportData




# fetch_llnl_weather_data and other data fetching functions are defined elsewhere
###########################################################################
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
    print(f"Response Content: {response.text[:100]}")

    if response.status_code == 200:
        LLNLdata = []
        reader = csv.DictReader(io.StringIO(response.text), delimiter='\t', fieldnames=['date', 'temperature', 'humidity'])
        next(reader)
        for row in reader:
            if row['temperature']:
                LLNLdata.append({'date': row['date'], 'temperature': float(row['temperature'])})
            else:
                print(f"Skipping row with empty temperature: {row}")
        return LLNLdata
    else:
        print(f"Failed to fetch data: HTTP {response.status_code}")
        return None
    
###########################################################################
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

###########################################################################
###########################################################################

app = Flask(__name__)

@app.route('/')
def plot():
    # Example data fetching
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
# Fetch data (using your data fetching functions)
###########################################################################
    LLNLdata = fetch_llnl_weather_data(start_date, end_date)
    LLNLdates = [datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S') for entry in LLNLdata]
    LLNLtemperatures = [entry['temperature'] for entry in LLNLdata]

# Fetch the sensorPush data
###########################################################################
    # Define the file paths
    file1 = './data/Sensor10.csv'
    file2 = './data/Sensor2.csv'

    # Specify column names manually for CSV files
    column_names = ['Timestamp', 'Temperature (A°C)', 'Relative Humidity (%)']

    # Read the data from the CSV files
    df1 = pd.read_csv(file1, skiprows=1, header=None, names=column_names, parse_dates=['Timestamp'], index_col='Timestamp')
    df2 = pd.read_csv(file2, skiprows=1, header=None, names=column_names, parse_dates=['Timestamp'], index_col='Timestamp')

# Fetch the Quest weather station data
###########################################################################
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

# Fetch the airport Livermore airport data

    airportData = fetch_airport_weather_data(start_date, end_date)
# Extract hourly temperature data
    airportWeatherData = []
    for day in airportData['data']['weather']:
        date = day['date']
        for hour in day['hourly']:
            airportTime = hour['time'].zfill(4)  # Ensure the time string is always four digits
            airportTemp = float(hour['tempC'])  # Ensure the temperature is treated as a float
            airportWeatherData.append([f"{date} {airportTime}", airportTemp])

    # Create a DataFrame
    df = pd.DataFrame(airportWeatherData, columns=['airportDateTime', 'airportTemperature'])
    df['airportDateTime'] = pd.to_datetime(df['airportDateTime'], format='%Y-%m-%d %H%M')

###########################################################################
 # Plot the data   
    
    fig = go.Figure()  # Create Plotly figure
    
# Add traces for each sensor

# LLNL
    fig.add_trace(go.Scatter(x=LLNLdates, y=LLNLtemperatures, mode='lines', name='LLNL Weather Station'))


# Quest Weather Station 
    fig.add_trace(go.Scatter(x=timestamps_api, y=temperatures_api, mode='lines', name='Quest Weather Station'))    


# Livermore Airport    
 #    line5, = ax.plot(df['airportDateTime'], df['airportTemperature'], marker='', linestyle='-', color='r', label='Airport Station') 
    fig.add_trace(go.Scatter(x=df['airportDateTime'], y=df['airportTemperature'], mode='lines', name='Livermore Airport'))      
               
# SensorPush    
    fig.add_trace(go.Scatter(x=df1.index, y=df1['Temperature (A°C)'], mode='lines', name='Sensor 10'))      
    fig.add_trace(go.Scatter(x=df2.index, y=df2['Temperature (A°C)'], mode='lines', name='Sensor 2'))
  
        
    # Customize layout
    fig.update_layout(title='Multiple Sensors - click name in legend to toggle visibility',               
                      xaxis_title='Time',
                      yaxis_title='Temperature (°C)',
                      legend_title='Sensor - click toggles visibility',showlegend=True)    
    
    # Convert the figure to HTML and return it
    graphHTML = fig.to_html(full_html=False)
    return render_template('plot.html', plot=graphHTML)



if __name__ == '__main__':
    app.run(debug=True)