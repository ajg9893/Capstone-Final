# Add a single student to the FaceCheck database.
# Fill in the fields below and run:  python add_student.py
#
# PHOTO_PATH is optional — leave it as "" if you don't have a photo yet.
# The student will still appear on the dashboard; face verification will be
# skipped when they check in until a photo is uploaded via upload_photo.py.

from firebase_client import db, bucket
import os

# ── Fill these in ─────────────────────────────────────────────────────────────
STUDENT_ID = ""        
NAME       = ""        
GRADE      = 12
PHOTO_PATH = ""        
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not STUDENT_ID or not NAME:
        print("Fill in STUDENT_ID and NAME before running.")
        raise SystemExit(1)

    data = {
        "studentId": STUDENT_ID,
        "name":      NAME,
        "grade":     GRADE,
    }

    if PHOTO_PATH and os.path.exists(PHOTO_PATH):
        print(f"Uploading photo for {NAME}...")
        blob = bucket.blob(f"photos/{STUDENT_ID}.jpg")
        blob.upload_from_filename(PHOTO_PATH)
        blob.make_public()
        data["photoUrl"] = blob.public_url
        print(f"Photo uploaded.")
    elif PHOTO_PATH:
        print(f"Warning: photo file '{PHOTO_PATH}' not found — adding student without photo.")

    db.collection("students").document(STUDENT_ID).set(data, merge=True)
    print(f"{NAME} ({STUDENT_ID}) added to database.")
