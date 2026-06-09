# add_student.py
# One-time enrollment for Arjun Gilhotra (already run — kept for reference).
# To upload a photo for any enrolled student, use upload_photo.py instead.

from firebase_client import db, bucket

STUDENT_ID = "10019893"
NAME       = "Arjun Gilhotra"
GRADE      = 12
PHOTO_PATH = "photos/10019893.jpg"

if __name__ == "__main__":
    blob = bucket.blob(f"photos/{STUDENT_ID}.jpg")
    blob.upload_from_filename(PHOTO_PATH)
    blob.make_public()
    photo_url = blob.public_url

    db.collection("students").document(STUDENT_ID).set({
        "studentId": STUDENT_ID,
        "name":      NAME,
        "grade":     GRADE,
        "photoUrl":  photo_url,
    }, merge=True)

    print(f"✅ {NAME} ({STUDENT_ID}) enrolled.")
    print(f"   Photo URL: {photo_url}")
