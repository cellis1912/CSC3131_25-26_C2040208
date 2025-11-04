from flask import Flask, jsonify, render_template, request, g
from db import db_connect


app = Flask(__name__)

def get_db():
    """Get a DB connection for this request."""
    if 'db' not in g:
        g.db = db_connect()
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    """Close DB connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT id, title, person, time_estimate, created_at FROM job_allocations ORDER BY id;")
        entries = cur.fetchall()
    return render_template('index.html', entries=entries)


@app.route('/jobs')
def jobs():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM job_allocations ORDER BY id;")
        entries = cur.fetchall()
    return render_template('job.html', entries=entries)

@app.route('/jobs/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM job_allocations WHERE id = %s;", (id,))
        conn.commit()
    return jsonify({'success': True})

@app.route('/jobs/edit/<int:id>', methods=['POST'])
def edit(id):
    title = request.form['title']
    person = request.form['person']
    time_estimate = request.form['time_estimate']

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

    if not title or not person or not time_estimate:
        return jsonify({"error": "All fields are required"}), 400

    try:
        time_estimate = float(time_estimate)
    except ValueError:
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
        return jsonify({"message": "Job added successfully", "id": new_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
