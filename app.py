from flask import Flask, jsonify, render_template
from db import db_connect, add_jobs_og
from psycopg2 import sql
import os

host = os.getenv("POSTGRES_HOST", "localhost")

app = Flask(__name__)
conn = db_connect()
add_jobs_og(conn)

print(conn)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/jobs")
def get_jobs():
    if conn is None:
        return {"error": "Database connection not initialized"}, 500
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, person, time_estimate, created_at FROM job_allocations;")
            rows = cur.fetchall()
            jobs = []
            for row in rows:
                jobs.append({
                    "id": row[0],
                    "title": row[1],
                    "person": row[2],
                    "time_estimate": float(row[3]),
                    "created_at": str(row[4])
                })
            return jsonify(jobs)
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/add-job")
def add_job():
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO job_allocations (title, person, time_estimate)
                VALUES (%s, %s, %s) RETURNING id;
            """, ("Example Job", "Alice", 3.5))
            conn.commit()
            new_id = cur.fetchone()[0]
            return {"message": "Job added", "id": new_id}
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
