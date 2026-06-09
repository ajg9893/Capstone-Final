# upload_photo.py
# Upload a photo for an already-enrolled student and save the URL to Firestore.
#
# Steps:
#   1. Place the student's photo at  photos/<STUDENT_ID>.jpg
#   2. Set STUDENT_ID below
#   3. Run:  python upload_photo.py

from firebase_client import db, bucket

# ── Change this for each student ─────────────────────────────────────────────
STUDENT_ID = "10019901"   # Saksham Dixit
#            "10019903"   # Sanjit Aita
#            "10019895"   # Aditya Pathak
# ─────────────────────────────────────────────────────────────────────────────

PHOTO_PATH = f"photos/{STUDENT_ID}.jpg"

if __name__ == "__main__":
    # Verify the student exists and grab their info
    doc = db.collection("students").document(STUDENT_ID).get()
    if not doc.exists:
        print(f"❌ No student record found for ID {STUDENT_ID}. Run add_students_batch.py first.")
        raise SystemExit(1)

    student = doc.to_dict()

    # Upload photo to Firebase Storage
    print(f"⬆️  Uploading photo for {student['name']} ({STUDENT_ID})...")
    blob = bucket.blob(f"photos/{STUDENT_ID}.jpg")
    blob.upload_from_filename(PHOTO_PATH)
    blob.make_public()
    photo_url = blob.public_url

    # Write back to Firestore — merge=True so no other fields are touched
    db.collection("students").document(STUDENT_ID).set({
        "studentId": student["studentId"],
        "name":      student["name"],
        "grade":     student["grade"],
        "photoUrl":  photo_url,
    }, merge=True)

    print(f"✅ Done — photoUrl saved for {student['name']}")
    print(f"   {photo_url}")
