# add_student.py
# Run this script once to add a student to the Firebase database


from firebase_client import upload_student


STUDENT_ID = "10019893"        # Genesis student ID
NAME       = "Arjun Gilhotra"          
GRADE      = 12
HOMEROOM   = "302"  
PHOTO_PATH = "photos/10019893.jpg"

if __name__ == "__main__":
    print(f"Adding student {NAME} ({STUDENT_ID}) to database...")
    upload_student(
        student_id=STUDENT_ID,
        name=NAME,
        grade=GRADE,
        homeroom=HOMEROOM,
        photo_path=PHOTO_PATH
    )