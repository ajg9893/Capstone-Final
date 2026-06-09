# add_students_batch.py
# Bulk-enroll demo students for the FaceCheck dashboard.
# Safe to re-run — uses set() so it won't create duplicates.
# Students without a real photo get photoUrl="" and won't be able
# to do face verification, but they WILL appear on the dashboard.

from firebase_client import db

# ── Class definitions ─────────────────────────────────────────────────────────
# Each entry: (student_id, name, grade, classes_list)
# classes_list controls which teacher filter shows this student.

STUDENTS = [
    # ── Mr. Haver — Data Structures ──────────────────────────────
    ("10019893", "Arjun Gilhotra",           12, ["haver"]),  # in both
    ("10019894", "Aditi Chaugule",           12, ["haver"]),
    ("10019895", "Aditya Pathak",            12, ["haver"]),
    ("10019896", "Anvi Joshi",               12, ["haver"]),
    ("10019897", "Arya Menon",               12, ["haver"]),
    ("10019898", "Naval Shah",               12, ["haver"]),
    ("10019899", "Nidhi Swaminathan",        12, ["haver"]),
    ("10019900", "Rashida Kapadia",          12, ["haver"]),
    ("10019901", "Saksham Dixit",            12, ["haver"]),
    ("10019902", "Samuel Joshua",            12, ["haver"]),
    ("10019903", "Sanjit Aita",              12, ["haver"]),
    ("10019904", "Sanskaar Srivastava",      12, ["haver"]),
    ("10019905", "Sathvika Gokulakrishnan",  12, ["haver"]),
    ("10019906", "Shrivarshini Ganeshkumar", 12, ["haver"]),
    ("10019907", "Vivaan Dev",               12, ["haver"]),
    ("10019908", "Vivek Banker",             12, ["haver"]),
]

# ─────────────────────────────────────────────────────────────────────────────

ARJUN_ID = "10019893"

if __name__ == "__main__":
    for student_id, name, grade, classes in STUDENTS:
        data = {
            "studentId": student_id,
            "name":      name,
            "grade":     grade,
            "classes":   classes,
        }
        if student_id != ARJUN_ID:
            data["photoUrl"] = ""

        db.collection("students").document(student_id).set(data, merge=True)
        print(f"✅ {name} ({student_id}) — classes: {classes}")

    print(f"\nDone. {len(STUDENTS)} students enrolled.")
