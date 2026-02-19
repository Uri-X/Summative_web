from flask import Blueprint, jsonify, request
from backend.db.connection import get_db_connection


trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/trips')
def get_trips():
    conn = get_db_connection()
    trips = conn.execute('SELECT * FROM fact_trips LIMIT 1000').fetchall()
    conn.close()
    result = [dict(row) for row in trips]
    return jsonify(result)

