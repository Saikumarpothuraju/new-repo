import requests
from datetime import datetime, timedelta
import statistics

# Set location to Hyderabad
latitude = 17.3850
longitude = 78.4867

# Define date range: last 7 days (excluding today)
end_date = datetime.today().date() - timedelta(days=1)
start_date = end_date - timedelta(days=6)

# Format dates
start = start_date.isoformat()
end = end_date.isoformat()

# Open-Meteo historical weather API
url = (
    f"https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={latitude}&longitude={longitude}"
    f"&start_date={start}&end_date={end}"
    f"&daily=temperature_2m_max,temperature_2m_min"
    f"&timezone=auto"
)

# API call
response = requests.get(url)
data = response.json()

# Extract data
dates = data['daily']['time']
temp_max = data['daily']['temperature_2m_max']
temp_min = data['daily']['temperature_2m_min']

# Filter out None values
weather_records = [
    {'date': dates[i], 'temp_max': temp_max[i], 'temp_min': temp_min[i]}
    for i in range(len(dates))
    if temp_max[i] is not None and temp_min[i] is not None
]

print("Weather Records for the Last 7 Days (Hyderabad):\n")
for record in weather_records:
    print(f"{record['date']}: Max = {record['temp_max']}°C, Min = {record['temp_min']}°C")

# Find extremes
if weather_records:
    max_record = max(weather_records, key=lambda x: x['temp_max'])
    min_record = min(weather_records, key=lambda x: x['temp_min'])

    print("\nTemperature Summary:")
    print(f"Highest Temperature: {max_record['temp_max']}°C on {max_record['date']}")
    print(f"Lowest Temperature: {min_record['temp_min']}°C on {min_record['date']}")

    # Anomaly Detection (Few-shot Prompting Simulation)
    # We'll use static historical average for August in Hyderabad (~32°C)
    historical_avg_august = 32
    threshold = 2  # degrees considered unusually high/low

    print("\nAnomalies Detected (Compared to Historical Norm ~32°C):")
    anomalies_found = False
    for record in weather_records:
        temp = record['temp_max']
        if temp > historical_avg_august + threshold:
            print(f"  🔺 Hotter than usual on {record['date']}: {temp}°C")
            anomalies_found = True
        elif temp < historical_avg_august - threshold:
            print(f"  🔻 Colder than usual on {record['date']}: {temp}°C")
            anomalies_found = True

    if not anomalies_found:
        print("  No temperature anomalies detected.")
else:
    print("\nNo valid weather data available.")
