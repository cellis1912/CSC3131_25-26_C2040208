import os
print(f"--- AZURE DEBUG: My app is starting. DATABASE_URL = {os.getenv('DATABASE_URL')} ---")
import time
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")


dbname_local = os.getenv("POSTGRES_DB")
user_local = os.getenv("POSTGRES_USER")
password_local = os.getenv("POSTGRES_PASSWORD")
host_local = os.getenv("POSTGRES_HOST") 
port_local = os.getenv("POSTGRES_PORT")


def db_connect(retries=5, delay=3):
    """Try connecting to PostgreSQL with retries."""
    for attempt in range(retries):
        try:
            if DATABASE_URL:
                conn = psycopg2.connect(DATABASE_URL)
                print(f"Connected to Postgres via DATABASE_URL.")
            else:
                print(f"DATABASE_URL not found. Attempting local connection to {host_local}...")
                conn = psycopg2.connect(
                    dbname=dbname_local,
                    user=user_local,
                    password=password_local,
                    host=host_local,
                    port=port_local
                )
                print(f"Connected to local Postgres at {host_local}:{port_local}")
            print(f"Connection attempt {attempt+1} successful.")
            return conn
            
        except Exception as e:
            print(f"Connection attempt {attempt+1} failed: {e}")
            time.sleep(delay)
    raise Exception("Could not connect to Postgres after several attempts")


def init_db(conn):
    """Create the job_allocations table if it doesn't exist."""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS job_allocations (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    person TEXT NOT NULL,
                    time_estimate NUMERIC(6,2) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("Table 'job_allocations' is ready.")
    except Exception as e:
        print(f"Error creating table: {e}")
        conn.rollback()

def delete_all_rows(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM job_allocations;")
            conn.commit()
            print("All rows deleted from job_allocations.")
    except Exception as e:
        print(f"Error deleting rows: {e}")
        conn.rollback()


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
        conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Connection closed after inserting jobs.")


def add_jobs_og(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO job_allocations (title, person, time_estimate)
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
                    ('Product Demo Prep', 'Jack Patel', 3.25);
            """)
            conn.commit()
            print("Seed data inserted successfully.")
    except Exception as e:
        print(f"Error seeding data: {e}")
        conn.rollback()