"""
Start gunicorn manually:   gunicorn -w 4 -b 0.0.0.0:8000 flask-just-sensor-push:app
See the process that is using a port: sudo lsof -i :<port_number>




"""

from flask import Flask, render_template_string
import mysql.connector
import plotly.graph_objs as go
import plotly.io as pio
from datetime import datetime, timedelta

app = Flask(__name__)

# Database connection details
db_config = {
    'user': 'uhi',
    'password': 'uhi',
    'host': 'localhost',
    'database': 'uhi'
}

# HTML template for rendering the plot
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Temperature Data Plot</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Temperature Data Plot</h1>
    <div id="temperature_plot"></div>
    <script>
        var plot_data = {{ plot_data | safe }};
        Plotly.newPlot('temperature_plot', plot_data.data, plot_data.layout);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    traces = []

    # Calculate the timestamp for 14 days ago
    fourteen_days_ago = datetime.now() - timedelta(days=14)
    fourteen_days_ago_str = fourteen_days_ago.strftime('%Y-%m-%d %H:%M:%S')

    # Loop through sensors Sensor1 to Sensor20
    for i in range(1, 21):
        if i < 10:
            sensor_id = f'Sensor{i}-'
        else:
            sensor_id = f'Sensor{i}'
      
    # Query to select temperature data for the current sensor, ordered by timestamp
        query = f"""
        SELECT timestamp, temperature 
        FROM sensor_data 
        WHERE sensorid = '{sensor_id}' 
        AND temperature IS NOT NULL 
        AND timestamp >= '{fourteen_days_ago_str}'
        ORDER BY timestamp ASC
        """
        cursor.execute(query)
        
        # Fetch the data
        rows = cursor.fetchall()
        
        if rows:
            # Extract data into lists
            timestamps = [row[0] for row in rows]
            temperatures = [row[1] for row in rows]
            
            # Create a trace for the temperature data
            trace = go.Scatter(x=timestamps, y=temperatures, mode='lines', name=sensor_id)
            traces.append(trace)
        else:
            print(f'No temperature data found for {sensor_id}')

    # Combine traces into a single figure
    fig = go.Figure(data=traces)
    
    # Set figure title and labels
    fig.update_layout(
        title='Temperature Data for All Sensors',
        xaxis_title='Time',
        yaxis_title='Temperature',
        legend_title='Sensors - click toggles visibility',
        showlegend=True  # Ensure the legend is visible
    )
    
    # Convert the figure to JSON for Plotly
    plot_data = pio.to_json(fig)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return render_template_string(html_template, plot_data=plot_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
