import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Directory containing the CSV files
directory = './'

# Specify column names manually
column_names = ['Timestamp', 'Temperature (A°C)', 'Relative Humidity (%)']

# Initialize the plot
plt.figure(figsize=(10, 6))

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Construct the full file path
        filepath = os.path.join(directory, filename)
        # Load the CSV file, specifying column names
        df = pd.read_csv(filepath, skiprows=1, header=None, names=column_names, parse_dates=['Timestamp'], index_col='Timestamp')
        # Plotting
        plt.plot(df.index, df['Temperature (A°C)'], marker='o', linestyle='-', label=filename)

# Formatting the plot
plt.title('Temperature as a Function of Time')
plt.xlabel('Time')
plt.ylabel('Temperature (A°C)')
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.legend()
plt.tight_layout()

# Show plot
plt.show()