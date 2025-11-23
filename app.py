from flask import Flask, jsonify, render_template, request, g
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from db import db_connect, init_db, add_jobs_og
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

REQUEST_COUNT = Counter(
    "flask_request_total",
    "Total HTTP requests",
    ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "flask_request_latency_seconds",
    "Time spent processing request",
    ["endpoint"]
)

EXCEPTIONS = Counter(
    "flask_exceptions_total",
    "Total exceptions raised",
    ["endpoint"]
)

app = Flask(__name__)

@app.before_request
def log_request_info():
    g.start_time = time.time()
    logging.info(f"Incoming request: {request.method} {request.path}")

@app.after_request
def after_request(response):
    endpoint = request.endpoint if request.endpoint else "unknown"

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        http_status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(endpoint=endpoint).observe(
        time.time() - g.start_time
    )

    return response

@app.errorhandler(Exception)
def handle_exception(e):
    endpoint = request.endpoint if request.endpoint else "unknown"
    EXCEPTIONS.labels(endpoint=endpoint).inc()
    logging.error(f"Unhandled exception: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


def get_db():
    if 'db' not in g:
        logging.info("Opening DB connection")
        g.db = db_connect()
        init_db(g.db)
        add_jobs_og(g.db)
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    logging.info("Closing DB connection")
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    conn = get_db()
    with conn.cursor() as cur:
        logging.info("Pulling jobs from table")
        cur.execute("SELECT id, title, person, time_estimate, created_at FROM job_allocations ORDER BY id;")
        entries = cur.fetchall()
    return render_template('index.html', entries=entries)


@app.route('/jobs')
def jobs():
    conn = get_db()
    with conn.cursor() as cur:
        logging.info("Pulling jobs from table")
        cur.execute("SELECT * FROM job_allocations ORDER BY id;")
        entries = cur.fetchall()
    return render_template('job.html', entries=entries)

@app.route('/jobs/delete/<int:id>', methods=['POST'])
def delete(id):
    logging.info(f"Attempting to delete job with ID: {id}")
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM job_allocations WHERE id = %s;", (id,))
        conn.commit()
    logging.info(f"Successfully deleted job with ID: {id}")
    return jsonify({'success': True})

@app.route('/jobs/edit/<int:id>', methods=['POST'])
def edit(id):
    title = request.form['title']
    person = request.form['person']
    time_estimate = request.form['time_estimate']

    logging.info(f"Editing job ID {id} with new values: title={title}, person={person}, time_estimate={time_estimate}")

    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE job_allocations
            SET title = %s, person = %s, time_estimate = %s
            WHERE id = %s;
            """,
            (title, person, time_estimate, id)
        )
        conn.commit()
    logging.info(f"Successfully updated job ID {id}")
    return jsonify({'success': True})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/add-job", methods=["GET"])

def show_add_job_form():
    return render_template("add_job.html")

@app.route("/add-job", methods=["POST"])
def add_job():
    title = request.form.get("title")
    person = request.form.get("person")
    time_estimate = request.form.get("time")

    logging.info(f"Received new job submission: title={title}, person={person}, time={time_estimate}")

    if not title or not person or not time_estimate:
        logging.warning("Job submission failed: Missing fields")
        return jsonify({"error": "All fields are required"}), 400

    try:
        time_estimate = float(time_estimate)
    except ValueError:
        logging.warning("Job submission failed: Invalid time estimate")
        return jsonify({"error": "Time estimate must be a number"}), 400

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO job_allocations (title, person, time_estimate)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (title, person, time_estimate)
            )
            new_id = cur.fetchone()[0]
            conn.commit()
        logging.info(f"Job added successfully with ID: {new_id}")
        return jsonify({"message": "Job added successfully", "id": new_id}), 201
    except Exception as e:
        conn.rollback()
        logging.error(f"Job submission failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
