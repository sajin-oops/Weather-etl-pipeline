from extract.fetch_weather import fetch_weather
from transform.transform_weather import transform_weather
from load.load_to_postgres import insert_weather
from datetime import datetime, timezone

if __name__ == "__main__":
    record = fetch_weather("London")
    record["recorded_at"] = datetime.fromtimestamp(record["recorded_at"], timezone.utc)
    print("Fetched:", record)

    transformed = transform_weather(record)
    print("Transformed:", transformed)

    insert_weather(transformed)
    print("Inserted into weather_data successfully!")