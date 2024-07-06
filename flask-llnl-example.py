import plotly.graph_objs as go
from flask import Flask, render_template
import pandas as pd
from datetime import datetime, timedelta
import requests
import csv
import io




# Assume fetch_llnl_weather_data and other data fetching functions are defined elsewhere
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
    
app = Flask(__name__)

@app.route('/')
def plot():
    # Example data fetching
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    # Fetch data (using your data fetching functions)
    LLNLdata = fetch_llnl_weather_data(start_date, end_date)
    LLNLdates = [datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S') for entry in LLNLdata]
    LLNLtemperatures = [entry['temperature'] for entry in LLNLdata]
    
    # Create Plotly figure
    fig = go.Figure()
    
    # Add traces for each sensor
    fig.add_trace(go.Scatter(x=LLNLdates, y=LLNLtemperatures, mode='lines', name='LLNL Station'))
    # Repeat the above line for other sensors, changing the x and y values accordingly
    
    # Customize layout
    fig.update_layout(title='Temperature as a Function of Time from Multiple Sensors',
                      xaxis_title='Time',
                      yaxis_title='Temperature (°C)',
                      legend_title='Sensor',showlegend=True)    
    
    # Convert the figure to HTML and return it
    graphHTML = fig.to_html(full_html=False)
    return render_template('plot.html', plot=graphHTML)

if __name__ == '__main__':
    app.run(debug=True)