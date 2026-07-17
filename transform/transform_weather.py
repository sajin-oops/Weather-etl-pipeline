from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, round as spark_round

def get_spark_session():
    return SparkSession.builder \
        .appName("WeatherTransform") \
        .master("local[*]") \
        .getOrCreate()

def transform_weather(record):
    spark = get_spark_session()

    # Convert single record dict into a Spark DataFrame
    df = spark.createDataFrame([record])

    # Add Fahrenheit conversion
    df = df.withColumn("temperature_f", spark_round(col("temperature") * 9/5 + 32, 2))

    # Categorize temperature
    df = df.withColumn(
        "temp_category",
        when(col("temperature") <= 10, "Cold")
        .when((col("temperature") > 10) & (col("temperature") <= 25), "Moderate")
        .otherwise("Hot")
    )

    # Convert back to a dict (since we're passing single records to postgres)
    transformed_record = df.collect()[0].asDict()

    spark.stop()
    return transformed_record

if __name__ == "__main__":
    sample = {
        "city": "London",
        "temperature": 21.0,
        "feels_like": 20.83,
        "humidity": 64,
        "weather_condition": "clear sky",
        "wind_speed": 0.45,
        "recorded_at": "2026-07-17 09:08:01"
    }
    print(transform_weather(sample))