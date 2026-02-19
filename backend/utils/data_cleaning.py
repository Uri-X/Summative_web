import pandas as pd

def clean_trips(trips: pd.DataFrame) -> pd.DataFrame:
    # Remove duplicates
    trips = trips.drop_duplicates()
    
    # Drop trips with missing critical values
    trips = trips.dropna(subset=['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'trip_distance', 'total_amount'])
    
    # Remove outliers
    trips = trips[(trips['trip_distance'] > 0) & (trips['trip_distance'] < 200)]
    trips = trips[(trips['total_amount'] > 0) & (trips['total_amount'] < 1000)]
    
    # Standardize timestamps
    trips['tpep_pickup_datetime'] = pd.to_datetime(trips['tpep_pickup_datetime'])
    trips['tpep_dropoff_datetime'] = pd.to_datetime(trips['tpep_dropoff_datetime'])
    
    return trips
