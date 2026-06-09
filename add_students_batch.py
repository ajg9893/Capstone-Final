# add_students_batch.py
# Bulk-enroll Mr. Haver's Data Structures class for the FaceCheck dashboard.
# Safe to re-run — merge=True never overwrites existing fields (e.g. photoUrl).
# To add a student's photo later, run upload_student.py for that student;
# this script intentionally does not touch photoUrl.

from firebase_client import db

# ── Mr. Haver — Data Structures ──────────────────────────────────────────────
# Each entry: (student_id, name, grade)

STUDENTS = [
    ("10019893", "Arjun Gilhotra",           12),
    ("10019894", "Aditi Chaugule",           12),
    ("10019895", "Aditya Pathak",            12),
    ("10019896", "Anvi Joshi",               12),
    ("10019897", "Arya Menon",               12),
    ("10019898", "Naval Shah",               12),
    ("10019899", "Nidhi Swaminathan",        12),
    ("10019900", "Rashida Kapadia",          12),
    ("10019901", "Saksham Dixit",            12),
    ("10019902", "Samuel Joshua",            12),
    ("10019903", "Sanjit Aita",              12),
    ("10019904", "Sanskaar Srivastava",      12),
    ("10019905", "Sathvika Gokulakrishnan",  12),
    ("10019906", "Shrivarshini Ganeshkumar", 12),
    ("10019907", "Vivaan Dev",               12),
    ("10019908", "Vivek Banker",             12),
]

# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    for student_id, name, grade in STUDENTS:
        # photoUrl is intentionally omitted — merge=True leaves any existing
        # photo (set by upload_student.py) completely untouched.
        db.collection("students").document(student_id).set({
            "studentId": student_id,
            "name":      name,
            "grade":     grade,
        }, merge=True)
        print(f"✅ {name} ({student_id})")

    print(f"\nDone. {len(STUDENTS)} students enrolled.")
