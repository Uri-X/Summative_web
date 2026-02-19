from flask import Blueprint, jsonify
from backend.db.connection import get_db_connection


zones_bp = Blueprint('zones', __name__)

@zones_bp.route('/', methods=['GET'])
def get_zones():
    conn = get_db_connection()
    zones = conn.execute("SELECT * FROM dim_zones").fetchall()
    conn.close()
    return jsonify([dict(row) for row in zones])
