import requests
from datetime import datetime, timedelta
import statistics

# Set your desired location
latitude = 40.7128  # Example: New York City
longitude = -74.0060

# Calculate date range (last 7 days)
end_date = datetime.today().date() - timedelta(days=1)
start_date = end_date - timedelta(days=6)

# Format dates as strings
start = start_date.isoformat()
end = end_date.isoformat()

# Request historical weather data (daily max and min temperatures)
url = (
    f"https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={latitude}&longitude={longitude}"
    f"&start_date={start}&end_date={end}"
    f"&daily=temperature_2m_max,temperature_2m_min"
    f"&timezone=auto"
)

# Make API call
response = requests.get(url)
data = response.json()

# Extract temperature and date data
dates = data['daily']['time']
temp_max = data['daily']['temperature_2m_max']
temp_min = data['daily']['temperature_2m_min']

# Combine data into a list of dicts, skipping entries with None
weather_records = [
    {
        'date': dates[i],
        'temp_max': temp_max[i],
        'temp_min': temp_min[i]
    }
    for i in range(len(dates))
    if temp_max[i] is not None and temp_min[i] is not None
]

# Print records
print("Weather Records for the Last 7 Days:\n")
for record in weather_records:
    print(f"{record['date']}: Max = {record['temp_max']}°C, Min = {record['temp_min']}°C")

# Check if there is valid data to process
if not weather_records:
    print("\nNo valid temperature data available for analysis.")
else:
    # Extract valid max and min temperatures and dates
    valid_max_temps = [(i, record['temp_max']) for i, record in enumerate(weather_records)]
    valid_min_temps = [(i, record['temp_min']) for i, record in enumerate(weather_records)]

    # Find max and min temperatures with corresponding dates
    max_temp_index, max_temp = max(valid_max_temps, key=lambda x: x[1])
    min_temp_index, min_temp = min(valid_min_temps, key=lambda x: x[1])

    max_temp_date = weather_records[max_temp_index]['date']
    min_temp_date = weather_records[min_temp_index]['date']

    print("\nTemperature Summary:")
    print(f"Highest Temperature: {max_temp}°C on {max_temp_date}")
    print(f"Lowest Temperature: {min_temp}°C on {min_temp_date}")

    # Get just the temperature values for statistics
    max_temp_values = [record['temp_max'] for record in weather_records]

    # Ensure there are enough data points for statistical analysis
    if len(max_temp_values) > 1:
        mean_max = statistics.mean(max_temp_values)
        std_max = statistics.stdev(max_temp_values)

        high_threshold = mean_max + 2 * std_max
        low_threshold = mean_max - 2 * std_max

        print("\nAnomalies Detected:")
        anomalies_found = False
        for record in weather_records:
            temp = record['temp_max']
            if temp > high_threshold:
                print(f"  🔺 High Anomaly on {record['date']}: {temp}°C")
                anomalies_found = True
            elif temp < low_threshold:
                print(f"  🔻 Low Anomaly on {record['date']}: {temp}°C")
                anomalies_found = True

        if not anomalies_found:
            print("  No anomalies detected.")
    else:
        print("\nNot enough data for anomaly detection.")
