from flask import Blueprint, jsonify, request
from db.connection import get_db_connection
import math

trips_bp = Blueprint('trips', __name__)


@trips_bp.route('/trips')
def get_trips():
    conn = get_db_connection()
    trips = conn.execute('SELECT * FROM fact_trips LIMIT 1000').fetchall()
    conn.close()
    return jsonify([dict(row) for row in trips])


@trips_bp.route('/trips/summary')
def get_summary():
    conn = get_db_connection()
    row = conn.execute('''
        SELECT
            COUNT(*) AS total_trips,
            AVG(trip_distance) AS avg_distance,
            AVG(fare_amount) AS avg_fare,
            AVG(trip_duration) AS avg_duration,
            AVG(CASE 
                WHEN trip_duration > 0 AND trip_distance > 0 
                THEN (trip_distance / trip_duration) * 60 
                END) AS avg_speed
        FROM fact_trips
    ''').fetchone()
    conn.close()
    import math
    data = dict(row)
    for key, val in data.items():
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            data[key] = None
    data['avg_distance'] = round(data['avg_distance'], 2) if data['avg_distance'] else None
    data['avg_fare'] = round(data['avg_fare'], 2) if data['avg_fare'] else None
    data['avg_duration'] = round(data['avg_duration'], 2) if data['avg_duration'] else None
    data['avg_speed'] = round(data['avg_speed'], 2) if data['avg_speed'] else None
    return jsonify(data)

@trips_bp.route('/trips/by-hour')
def trips_by_hour():
    conn = get_db_connection()
    rows = conn.execute('''
        SELECT
            CAST(strftime('%H', pickup_datetime) AS INTEGER) AS hour,
            COUNT(*) AS trip_count,
            ROUND(AVG(fare_amount), 2) AS avg_fare
        FROM fact_trips
        WHERE pickup_datetime IS NOT NULL
        GROUP BY hour
        ORDER BY hour
    ''').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@trips_bp.route('/trips/by-borough')
def trips_by_borough():
    conn = get_db_connection()
    rows = conn.execute('''
        SELECT
            z.Borough,
            COUNT(*) AS trip_count,
            ROUND(AVG(t.fare_amount), 2) AS avg_fare,
            ROUND(AVG(t.trip_distance), 2) AS avg_distance
        FROM fact_trips t
        JOIN dim_zones z ON t.PULocationID = z.LocationID
        WHERE z.Borough IS NOT NULL
        GROUP BY z.Borough
        ORDER BY trip_count DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@trips_bp.route('/trips/top-zones')
def top_zones():
    conn = get_db_connection()
    rows = conn.execute('''
        SELECT
            z.Zone,
            z.Borough,
            COUNT(*) AS trip_count
        FROM fact_trips t
        JOIN dim_zones z ON t.PULocationID = z.LocationID
        WHERE z.Zone IS NOT NULL
        GROUP BY z.Zone, z.Borough
        ORDER BY trip_count DESC
        LIMIT 10
    ''').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])