import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "weather_db",
    "user": "postgres",
    "password": "",
    "port": 5432
}

def insert_weather(record):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weather_data (city, temperature, feels_like, humidity, weather_condition, wind_speed, recorded_at, temperature_f, temp_category)
        VALUES (%(city)s, %(temperature)s, %(feels_like)s, %(humidity)s, %(weather_condition)s, %(wind_speed)s, %(recorded_at)s, %(temperature_f)s, %(temp_category)s)
    """, record)
    conn.commit()
    cur.close()
    conn.close()