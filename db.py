import os
import time
import psycopg2
from psycopg2 import sql

dbname = os.getenv("POSTGRES_DB", "postgres")
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "pass")
host = os.getenv("POSTGRES_HOST", "db")  # matches service name in docker-compose
port = 5432

def db_connect(retries=5, delay=3):
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
            print("Connected to database")
            return conn
        except Exception as e:
            print(f"Attempt {attempt+1}: Database not ready, retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("Could not connect to Postgres after several attempts")
def populate_jobs(conn, jobs):
    """
    Insert multiple jobs into the job_allocations table.
    
    jobs: list of dictionaries, each with keys 'title', 'person', 'time_estimate'
    """
    try:
        with conn.cursor() as cur:
            for job in jobs:
                cur.execute("""
                    INSERT INTO job_allocations (title, person, time_estimate)
                    VALUES (%s, %s, %s);
                """, (job['title'], job['person'], job['time_estimate']))
            conn.commit()
            print(f"{len(jobs)} jobs inserted successfully.")

    except Exception as e:
        print(f"An error occurred while populating jobs: {e}")

    finally:
        if conn:
            conn.close()
            print("Connection closed after inserting jobs.")


