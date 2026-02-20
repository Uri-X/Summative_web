def add_features(trips):
    trips['trip_duration'] = (trips['tpep_dropoff_datetime'] - trips['tpep_pickup_datetime']).dt.total_seconds()/60
    trips['speed'] = trips['trip_distance'] / (trips['trip_duration']/60)
    trips['fare_per_mile'] = trips['total_amount'] / trips['trip_distance']
    
    # Rename columns to match db schema
    trips.rename(columns={
        'tpep_pickup_datetime': 'pickup_datetime',
        'tpep_dropoff_datetime': 'dropoff_datetime',
        'PULocationID': 'PULocationID',
        'DOLocationID': 'DOLocationID'
    }, inplace=True)
    
    return trips
