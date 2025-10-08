import os
import time
import psycopg2
from psycopg2 import sql
from flask import Flask
'''
app = Flask(__name__)

@app.route("/")
def hello():
    return {"Hello": "World"}

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
'''
# Wait for the database to be ready
# This is a robust way to ensure the app doesn't try to connect too early
time.sleep(10)
# Database connection parameters
dbname = 'your_database'
user = 'your_usernamePOSTGRES'
password = 'pass'
host = 'localhost'  # or your database host
port = '5432'       # default PostgreSQL port6432

# Establish the connection
try:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    print("Connected to the database.")
    
    with conn.cursor() as cur:
        # Create a table and insert data
        cur.execute("""
            CREATE TABLE IF NOT EXISTS job_allocations (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            person VARCHAR(255) NOT NULL,
            time_estimate DECIMAL(5, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        print("Table 'job_allocations' created successfully.")
        conn.commit()

        # Query the database
        cur.execute("SELECT * FROM us job_allocations;")
        records = cur.fetchall()
        print("Connected to PostgreSQL and retrieved data:", records)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the cursor and connection
    if conn:
        cur.close()
        conn.close()
        print("Connection closed.")