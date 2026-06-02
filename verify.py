# verify.py
# Main entry point - ties barcode scanning, face recognition, and Firebase together
# Run this script to start the check-in system: python verify.py

from barcode_reader import read_barcode
from face_rec_module import capture_snapshot, compare_faces, cleanup_temp
from firebase_client import get_student, log_attendance, check_already_checked_in, download_photo, archive_and_reset, get_session
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os
import time

load_dotenv()

SNAPSHOT_PATH = "photos/temp/live_snapshot.jpg"
SCAN_COOLDOWN_SECONDS = 30

_last_scan: dict[str, datetime] = {}


def _is_on_cooldown(student_id: str) -> bool:
    last = _last_scan.get(student_id)
    if last and (datetime.now() - last).total_seconds() < SCAN_COOLDOWN_SECONDS:
        remaining = SCAN_COOLDOWN_SECONDS - int((datetime.now() - last).total_seconds())
        print(f"⏳ ID {student_id} was just scanned. Please wait {remaining}s before scanning again.")
        return True
    return False


def run_checkin():
    print("\n" + "="*50)
    print("       FACECHECK - STUDENT CHECK-IN SYSTEM")
    print("="*50)

    # ── STEP 1: Scan ID ──────────────────────────────
    student_id = read_barcode()

    if not student_id:
        print("❌ No ID scanned. Please try again.")
        return

    if _is_on_cooldown(student_id):
        return

    _last_scan[student_id] = datetime.now()
    print(f"\n🔍 Looking up student ID: {student_id}...")

    # ── STEP 2: Look up student in Firebase ──────────
    # NOTE: When Firebase isn't available, fall back to local photo for testing
    student = None
    stored_photo_path = f"photos/{student_id}.jpg"

    try:
        student = get_student(student_id)
    except Exception as e:
        print(f"⚠️  Firebase unavailable - running in offline test mode")
        print(f"   Using local photo: {stored_photo_path}")

    if student is None and not os.path.exists(stored_photo_path):
        print(f"❌ Student ID {student_id} not found. Are you registered?")
        return

    name = student["name"] if student else f"Student {student_id}"
    print(f"✅ Found: {name}")

    # ── STEP 3: Check if already checked in ─────────
    if student:
        try:
            if check_already_checked_in(student_id):
                print(f"⚠️  {name} has already checked in today!")
                return
        except:
            pass  # skip duplicate check in offline mode

    # ── STEP 4: Capture live snapshot ───────────────
    print(f"\nHello {name}! Please look at the camera...")
    taken = capture_snapshot(SNAPSHOT_PATH)

    if not taken:
        print("❌ No snapshot taken. Check-in cancelled.")
        return

    # ── STEP 5: Download stored photo (or use local) ─
    if student and student.get("photoUrl"):
        try:
            download_photo(student["photoUrl"], stored_photo_path)
        except:
            print("⚠️  Could not download photo from Firebase - using local copy")

    if not os.path.exists(stored_photo_path):
        print(f"❌ No stored photo found for {student_id}")
        return

    # ── STEP 6: Compare faces ────────────────────────
    print("\n🔎 Comparing faces...")
    result = compare_faces(SNAPSHOT_PATH, stored_photo_path)

    # ── STEP 7: Log attendance if verified ──────────
    if result["match"]:
        if student:
            try:
                status = log_attendance(student_id, name, verified=True)
                now = datetime.now().strftime("%I:%M %p")
                print(f"\n🎉 Welcome, {name}!")
                print(f"   Checked in at {now} — {status.upper()}")
            except:
                print(f"\n🎉 Welcome, {name}! (offline mode - not logged)")
        else:
            print(f"\n🎉 Face matched! (offline mode - not logged to Firebase)")
    else:
        print(f"\n🚨 Face mismatch for ID {student_id}!")
        print("   Please see the front desk.")
        if student:
            try:
                log_attendance(student_id, name, verified=False)
            except:
                pass

    # ── STEP 8: Cleanup ──────────────────────────────
    cleanup_temp(SNAPSHOT_PATH)
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    reset_hour = int(os.getenv('RESET_HOUR', 14))
    reset_minute = int(os.getenv('RESET_MINUTE', 20))

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        archive_and_reset,
        trigger='cron',
        hour=reset_hour,
        minute=reset_minute,
        id='daily_reset'
    )
    scheduler.start()
    print(f"⏰ Auto-reset scheduled for {reset_hour:02d}:{reset_minute:02d} daily\n")

    try:
        session_was_active = False
        while True:
            session_active = get_session().get("active", False)

            if not session_active:
                if session_was_active:
                    print("\n⏹  Session ended. Waiting for next session...")
                    session_was_active = False
                else:
                    print("\r⏸  Kiosk paused — start a session from the dashboard", end="", flush=True)
                time.sleep(3)
                continue

            if not session_was_active:
                print("\n\n✅ Session active — ready to scan\n")
                session_was_active = True

            run_checkin()

    except KeyboardInterrupt:
        print("\n\nKiosk stopped.")
    finally:
        scheduler.shutdown()