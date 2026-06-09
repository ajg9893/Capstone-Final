from flask import Flask, jsonify, request
from flask_cors import CORS
from firebase_client import db, archive_and_reset, get_session, set_session
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)


def _serialize(doc_dict: dict) -> dict:
    """Convert Firestore-specific types (Timestamps, etc.) to JSON-safe values."""
    out = {}
    for k, v in doc_dict.items():
        if hasattr(v, 'isoformat'):
            out[k] = v.isoformat()
        else:
            out[k] = v
    return out


# Attendance 

@app.route("/api/attendance/today", methods=["GET"])
def get_today_attendance():
    """
    Returns today's attendance records.
    Optional query param: ?status=present|tardy
    """
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    query = db.collection("attendance").where(filter=FieldFilter("timestamp", ">=", today_start))

    records = []
    for doc in query.stream():
        data = _serialize(doc.to_dict())
        data["id"] = doc.id
        records.append(data)

    # Filter by status in Python to avoid needing a Firestore composite index
    status_filter = request.args.get("status")
    if status_filter:
        records = [r for r in records if r.get("status") == status_filter]

    records.sort(key=lambda r: r.get("timestamp", ""), reverse=True)
    return jsonify(records)


@app.route("/api/stats", methods=["GET"])
def get_today_stats():
    """Returns present/tardy counts for today."""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    docs = db.collection("attendance").where(filter=FieldFilter("timestamp", ">=", today_start)).stream()

    present = tardy = 0
    for doc in docs:
        status = doc.to_dict().get("status")
        if status == "present":
            present += 1
        elif status == "tardy":
            tardy += 1

    return jsonify({"present": present, "tardy": tardy, "total": present + tardy})


# Students 

@app.route("/api/students", methods=["GET"])
def get_students():
    """Returns all enrolled students."""
    students = []
    for doc in db.collection("students").stream():
        data = _serialize(doc.to_dict())
        data["id"] = doc.id
        students.append(data)

    return jsonify(students)


@app.route("/api/students/<student_id>", methods=["GET"])
def get_student(student_id):
    """Returns a single student record by ID."""
    doc = db.collection("students").document(student_id).get()
    if not doc.exists:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(_serialize(doc.to_dict()))


@app.route("/api/attendance/absent", methods=["GET"])
def get_absent_students():
    """Returns students who have NOT checked in today."""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    checked_in_ids = {
        doc.to_dict().get("studentId")
        for doc in db.collection("attendance").where(filter=FieldFilter("timestamp", ">=", today_start)).stream()
    }

    absent = []
    for doc in db.collection("students").stream():
        if doc.id not in checked_in_ids:
            data = _serialize(doc.to_dict())
            data["id"] = doc.id
            absent.append(data)

    return jsonify(absent)


# Session 

@app.route("/api/session", methods=["GET"])
def get_session_state():
    return jsonify(_serialize(get_session()))


@app.route("/api/session/start", methods=["POST"])
def start_session():
    set_session(True)
    return jsonify({"success": True, "active": True})


@app.route("/api/session/stop", methods=["POST"])
def stop_session():
    set_session(False)
    return jsonify({"success": True, "active": False})


# Admin

@app.route("/api/reset", methods=["POST"])
def manual_reset():
    """Manually trigger archive and reset (same job APScheduler runs at 2:20 PM)."""
    try:
        archive_and_reset()
        return jsonify({"success": True, "message": "Attendance archived and reset."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Run

if __name__ == "__main__":
    app.run(debug=True, port=5000)
