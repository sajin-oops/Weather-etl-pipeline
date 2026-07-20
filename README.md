# Weather ETL Pipeline

An end-to-end ETL (Extract, Transform, Load) pipeline that fetches live weather data from the OpenWeatherMap API, transforms it using PySpark, and loads it into a PostgreSQL database.

## Tech Stack
- **Python** – core scripting
- **PostgreSQL** – data storage
- **PySpark** – data transformation
- **Apache Airflow** – workflow orchestration 
## Architecture

```
OpenWeatherMap API
        │
        ▼
extract/fetch_weather.py        (fetches raw weather data)
        │
        ▼
transform/transform_weather.py  (PySpark: unit conversion, categorization)
        │
        ▼
load/load_to_postgres.py.       (inserts into PostgreSQL)
```



## Features
- Fetches real-time weather data (temperature, humidity, wind speed, conditions) for a given city
- Converts temperature to Fahrenheit and categorizes it (Cold / Moderate / Hot) using PySpark
- Loads structured, transformed data into a PostgreSQL table
- Environment variables used for API key management (`.env`, not committed to version control)


## Project Structure

```
weather-etl-pipeline/
├── extract/
│   └── fetch_weather.py            # Calls OpenWeatherMap API
├── transform/
│   └── transform_weather.py        # PySpark transformation logic
├── load/
│   └── load_to_postgres.py         # Inserts data into PostgreSQL
├── run_pipeline.py                 # Orchestrates extract → transform → load
├── .env                            # API key (not committed)
├── .gitignore
└── README.md
```


## Setup & Usage

1. Clone the repo
```bash
git clone https://github.com/sajin-oops/weather-etl-pipeline.git
cd weather-etl-pipeline
```

2. Install dependencies
```bash
pip install requests psycopg2-binary pyspark python-dotenv
```

3. Create a `.env` file in the root directory

OPENWEATHER_API_KEY=your_api_key_here

4. Set up PostgreSQL and create the database/table
```sql
CREATE DATABASE weather_db;

CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature FLOAT,
    feels_like FLOAT,
    humidity INT,
    weather_condition VARCHAR(100),
    wind_speed FLOAT,
    recorded_at TIMESTAMP,
    inserted_at TIMESTAMP DEFAULT NOW(),
    temperature_f FLOAT,
    temp_category VARCHAR(20)
);
```

5. Update the `DB_CONFIG` in `load/load_to_postgres.py` with your PostgreSQL credentials

6. Run the pipeline
```bash
python run_pipeline.py
```

## Sample Output

Fetched: {'city': 'London', 'temperature': 21, 'feels_like': 20.83, 'humidity': 64, 'weather_condition': 'clear sky', 'wind_speed': 0.45, 'recorded_at': datetime.datetime(2026, 7, 17, 9, 8, 1)}
Inserted into weather_data successfully!

Transformed: {'city': 'London', 'feels_like': 20.85, 'humidity': 64, 'recorded_at': datetime.datetime(2026, 7, 17, 14, 47, 2), 'temperature': 21.02, 'weather_condition': 'clear sky', 'wind_speed': 0.89, 'temperature_f': 69.84, 'temp_category': 'Moderate'}
Inserted into weather_data successfully!


## Author
**A.K. Sajin** ([@sajin-oops](https://github.com/sajin-oops))
