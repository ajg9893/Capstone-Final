# Upload a photo for an already-enrolled student and save the URL to Firestore.
#
# Steps:
#   1. Place the student's photo at  photos/<STUDENT_ID>.jpg  OR  .png
#   2. Set STUDENT_ID below
#   3. Run:python upload_photo.py

from firebase_client import db, bucket
from PIL import Image
import os

# ── Change this for each student ─────────────────────────────────────────────
STUDENT_ID = ""   # Student name
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Verify the student exists in Firestore first
    doc = db.collection("students").document(STUDENT_ID).get()
    if not doc.exists:
        print(f"No student record found for ID {STUDENT_ID}. Run add_students_batch.py first.")
        raise SystemExit(1)

    name = doc.to_dict().get("name", STUDENT_ID)

    jpg_path = f"photos/{STUDENT_ID}.jpg"
    # png_path = f"photos/{STUDENT_ID}.png"

    if os.path.exists(jpg_path):
        photo_path = jpg_path
    elif os.path.exists(png_path):
        # Convert PNG → JPG so DeepFace always gets a consistent format
        print(f"Converting {STUDENT_ID}.png → {STUDENT_ID}.jpg ...")
        img = Image.open(png_path).convert("RGB")
        img.save(jpg_path, "JPEG")
        photo_path = jpg_path
        print("Converted.")
    else:
        print(f"No photo found at {jpg_path} or {png_path}. Add the file and try again.")
        raise SystemExit(1)

    # Upload to Firebase Storage
    print(f"Uploading photo for {name} ({STUDENT_ID})...")
    blob = bucket.blob(f"photos/{STUDENT_ID}.jpg")
    blob.upload_from_filename(photo_path)
    blob.make_public()
    photo_url = blob.public_url

    # Write the URL back to Firestore
    db.collection("students").document(STUDENT_ID).set({
        "studentId": STUDENT_ID,
        "name":      name,
        "grade":     doc.to_dict().get("grade"),
        "photoUrl":  photo_url,
    }, merge=True)

    print(f"Done — photoUrl saved for {name}")
    print(f"   {photo_url}")
