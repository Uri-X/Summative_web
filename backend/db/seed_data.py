import os
import pandas as pd
import sqlite3

# Absolute imports for utils modules
from backend.utils.data_cleaning import clean_trips
from backend.utils.feature_engineering import add_features

# Defining project root and data folder here
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

# --- 3. Define file paths ---
trips_file = os.path.join(DATA_DIR, 'yellow_tripdata_2022-01.parquet')
zones_file = os.path.join(DATA_DIR, 'taxi_zone_lookup.csv')

# --- 4. Check if files exist ---
if not os.path.exists(trips_file):
    raise FileNotFoundError(f"Trips file not found at {trips_file}")
if not os.path.exists(zones_file):
    raise FileNotFoundError(f"Zones file not found at {zones_file}")

# --- 5. Load raw data ---
trips = pd.read_parquet(trips_file)
zones = pd.read_csv(zones_file)

# --- 6. Clean data and create features ---
trips = clean_trips(trips)
trips = add_features(trips)

# --- 7. Define SQLite database path ---
DB_PATH = os.path.join(PROJECT_ROOT, 'backend', 'nyc_taxi.db')

# --- 8. Save data to SQLite ---
conn = sqlite3.connect(DB_PATH)
zones.to_sql('dim_zones', conn, if_exists='replace', index=False)
trips.to_sql('fact_trips', conn, if_exists='replace', index=False)
conn.close()

print("Database seeded successfully!")
