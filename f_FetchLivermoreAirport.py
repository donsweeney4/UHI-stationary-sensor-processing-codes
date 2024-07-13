import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

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
data = response.json()

# Extract hourly temperature data
weather_data = []
for day in data['data']['weather']:
    date = day['date']
    for hour in day['hourly']:
        time = hour['time'].zfill(4)  # Ensure the time string is always four digits
        temp = float(hour['tempC'])  # Ensure the temperature is treated as a float
        weather_data.append([f"{date} {time}", temp])

# Create a DataFrame
df = pd.DataFrame(weather_data, columns=['DateTime', 'Temperature'])
df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H%M')

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(df['DateTime'], df['Temperature'], marker='', linestyle='-')
plt.xlabel('Date and Time')
plt.ylabel('Temperature (°C)')
plt.title('Hourly Temperature for Week at Livermore Municipal Airport (LVK)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
