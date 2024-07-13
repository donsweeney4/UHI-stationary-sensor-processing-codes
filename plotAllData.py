import zipfile
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Constants for WeatherLink API
API_KEY = 'gr6jeugtsob9hlqaheg7q0fg8ffcby2p'
API_SECRET = 'y1eefxv2sq1nrhjzekdlgu8bgdjtqf4i'
STATION_ID = '113636'

# Path to the ZIP file
zip_file_path = './data/your_zip_file.zip'  # Update this with your actual zip file path

# Directory where the file will be extracted
extract_to_directory = './extracted_files'

# File name to extract from the ZIP file
file_name_inside_zip = 'file_inside.csv'  # Update this with your actual file name inside the zip

# Open the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Extract the specific file
    zip_ref.extract(file_name_inside_zip, extract_to_directory)

    # Path to the extracted file
    extracted_file_path = os.path.join(extract_to_directory, file_name_inside_zip)

    # Read the extracted file (assuming it's a CSV for this example)
    df_csv = pd.read_csv(extracted_file_path)

# Directory containing the CSV files
directory = './'

# Specify column names manually for CSV files
column_names = ['Timestamp', 'Temperature (A°C)', 'Relative Humidity (%)']

# Initialize the plot
plt.figure(figsize=(10, 6))

# Function to generate UNIX timestamps for the start and end of each day in the past week
def generate_timestamps():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    for single_date in pd.date_range(start=start_date, end=end_date, freq='D'):
        yield int(single_date.timestamp()), int((single_date + timedelta(days=1) - timedelta(seconds=1)).timestamp())

# Function to fetch data from WeatherLink API
def fetch_data(start_timestamp, end_timestamp):
    URL = f"https://api.weatherlink.com/v2/historic/{STATION_ID}?api-key={API_KEY}&start-timestamp={start_timestamp}&end-timestamp={end_timestamp}"
    headers = 
