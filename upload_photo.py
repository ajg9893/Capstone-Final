# upload_photo.py
# Upload a photo for an already-enrolled student and save the URL to Firestore.
#
# Steps:
#   1. Place the student's photo at  photos/<STUDENT_ID>.jpg
#   2. Set STUDENT_ID below
#   3. Run:  python upload_photo.py

from firebase_client import db, bucket

# ── Change this for each student ─────────────────────────────────────────────
STUDENT_ID = "30002516"   # Saksham Dixit
#            "10019810"   # Sanjit Aita
#            "10021472"   # Aditya Pathak
# ─────────────────────────────────────────────────────────────────────────────

PHOTO_PATH = f"photos/{STUDENT_ID}.jpg"

if __name__ == "__main__":
    doc = db.collection("students").document(STUDENT_ID).get()
    if not doc.exists:
        print(f"No student record found for ID {STUDENT_ID}. Run add_students_batch.py first.")
        raise SystemExit(1)

    name = doc.to_dict().get("name", STUDENT_ID)

    # Upload photo to Firebase Storage
    print(f"Uploading photo for {name} ({STUDENT_ID})...")
    blob = bucket.blob(f"photos/{STUDENT_ID}.jpg")
    blob.upload_from_filename(PHOTO_PATH)
    blob.make_public()
    photo_url = blob.public_url

    # Write the URL back to the student's Firestore document
    db.collection("students").document(STUDENT_ID).update({"photoUrl": photo_url})

    print(f"Done — photoUrl saved for {name}")
    print(f"   {photo_url}")
