import os
import time
import psycopg2
from psycopg2 import sql

# Read from environment (with sensible defaults for local dev)
dbname = os.getenv("POSTGRES_DB", "jobdb")
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "pass")
host = os.getenv("POSTGRES_HOST", "db")
port = os.getenv("POSTGRES_PORT", "5432")

def db_connect(retries=5, delay=3):
    """Try connecting to PostgreSQL with retries."""
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            return conn
        except Exception as e:
            time.sleep(delay)
    raise Exception("Could not connect to Postgres after several attempts")

def populate_jobs(conn, jobs):
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
        print(f"Error populating jobs: {e}")
    finally:
        if conn:
            conn.close()
            print("Connection closed after inserting jobs.")

def add_jobs_og(conn):
    try:
        with conn.cursor() as cur:
            cur.execute('''INSERT INTO job_allocations (title, person, time_estimate)
            VALUES 
            ('Design Homepage', 'Alice Johnson', 12.50),
            ('Write Blog Post', 'Ben Carter', 3.75),
            ('Database Optimization', 'Clara Zhang', 8.25),
            ('Client Meeting', 'David Lee', 2.00),
            ('Code Review', 'Ella Thompson', 4.50),
            ('Marketing Strategy', 'Frank O’Neil', 6.00),
            ('UX Testing', 'Grace Kim', 5.25),
            ('Server Maintenance', 'Henry Wallace', 7.00),
            ('Social Media Campaign', 'Isla Morgan', 4.75),
            ('Product Demo Prep', 'Jack Patel', 3.25);''')
            conn.commit()
    except Exception as e:
        print(e)
