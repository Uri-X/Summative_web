-- Dimension Table
CREATE TABLE IF NOT EXISTS dim_zones (
    LocationID INTEGER PRIMARY KEY,
    Borough TEXT,
    Zone TEXT,
    geom TEXT
);

-- Fact Table
CREATE TABLE IF NOT EXISTS fact_trips (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pickup_datetime TEXT,
    dropoff_datetime TEXT,
    trip_distance REAL,
    fare_amount REAL,
    total_amount REAL,
    PULocationID INTEGER,
    DOLocationID INTEGER,
    trip_duration REAL,
    speed REAL,
    fare_per_mile REAL,
    FOREIGN KEY (PULocationID) REFERENCES dim_zones(LocationID),
    FOREIGN KEY (DOLocationID) REFERENCES dim_zones(LocationID)
);
