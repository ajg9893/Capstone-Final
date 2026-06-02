import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime
from dotenv import load_dotenv
import os
import requests

load_dotenv()

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': os.getenv('STORAGE_BUCKET')
})

db = firestore.client()
bucket = storage.bucket()


def get_student(student_id: str):
    doc = db.collection("students").document(student_id).get()
    if doc.exists:
        return doc.to_dict()
    return None


def log_attendance(student_id: str, name: str, verified: bool):
    now = datetime.now()
    tardy_hour = int(os.getenv('TARDY_HOUR', 7))
    tardy_minute = int(os.getenv('TARDY_MINUTE', 40))
    tardy_cutoff = now.replace(hour=tardy_hour, minute=tardy_minute, second=0, microsecond=0)
    status = "tardy" if now >= tardy_cutoff else "present"

    db.collection("attendance").add({
        "studentId": student_id,
        "name": name,
        "timestamp": now,
        "status": status,
        "verified": verified
    })

    return status


def archive_and_reset():
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    print(f"[{now}] Starting archive and reset for {date_str}...")

    records = db.collection("attendance").stream()
    archive_ref = db.collection("attendance_archive").document(date_str).collection("records")

    count = 0
    for record in records:
        data = record.to_dict()
        archive_ref.add(data)
        record.reference.delete()
        count += 1

    print(f"[{now}] Archived {count} records. Attendance reset complete.")


def get_session() -> dict:
    doc = db.collection("config").document("session").get()
    if doc.exists:
        return doc.to_dict()
    return {"active": False}


def set_session(active: bool):
    now = datetime.now()
    data = {"active": active}
    if active:
        data["startedAt"] = now
    else:
        data["stoppedAt"] = now
    db.collection("config").document("session").set(data, merge=True)


def check_already_checked_in(student_id: str) -> bool:
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    records = (
        db.collection("attendance")
        .where(filter=FieldFilter("studentId", "==", student_id))
        .where(filter=FieldFilter("timestamp", ">=", today_start))
        .stream()
    )
    return any(True for _ in records)


def upload_student(student_id: str, name: str, grade: int, homeroom: str, photo_path: str):
    """Add a new student to Firestore and upload their photo to Firebase Storage."""

    # Upload photo to Firebase Storage
    blob = bucket.blob(f"photos/{student_id}.jpg")
    blob.upload_from_filename(photo_path)
    blob.make_public()
    photo_url = blob.public_url

    # Save student record to Firestore
    db.collection("students").document(student_id).set({
        "studentId": student_id,
        "name": name,
        "grade": grade,
        "homeroom": homeroom,
        "photoUrl": photo_url
    })

    print(f"Student {name} ({student_id}) added successfully.")
    print(f"Photo URL: {photo_url}")
    return photo_url


def download_photo(photo_url: str, save_path: str):
    response = requests.get(photo_url)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    return save_path