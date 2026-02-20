from connection import get_db_connection

conn = get_db_connection()
conn.execute("CREATE INDEX IF NOT EXISTS idx_pu ON fact_trips(PULocationID);")
conn.execute("CREATE INDEX IF NOT EXISTS idx_pickup ON fact_trips(pickup_datetime);")
conn.commit()
conn.close()
print("Indexes created!")