# face_recognition_module.py
# Handles all face capture and comparison logic using DeepFace

import cv2
import os
from deepface import DeepFace
from datetime import datetime


def capture_snapshot(save_path: str) -> bool:
    """
    Opens the webcam and auto-captures when a face is held inside the
    guide box for 2 seconds. Times out after 15 seconds if no face appears.
    Returns True if snapshot was taken, False if cancelled or timed out.
    """
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Could not open webcam. Check your camera connection.")
        return False

    print("\n📸 Camera opened! Position your face inside the box.")
    print("   → Hold still for 2 seconds to auto-capture")
    print("   → Press ESC to cancel\n")

    HOLD_SECONDS = 2
    TIMEOUT_SECONDS = 15

    face_detected_at = None
    start_time = datetime.now()
    snapshot_taken = False

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to read from camera.")
            break

        elapsed = (datetime.now() - start_time).total_seconds()
        if elapsed > TIMEOUT_SECONDS:
            print("⏱️  No face detected — check-in cancelled.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80)
        )

        display = frame.copy()
        h, w = frame.shape[:2]

        # Guide box: centred, half the width, two-thirds the height
        bx, by = w // 4, h // 6
        bw, bh = w // 2, h * 2 // 3
        cv2.rectangle(display, (bx, by), (bx + bw, by + bh), (0, 200, 255), 2)

        face_in_box = False
        for (fx, fy, fw, fh) in faces:
            cx, cy = fx + fw // 2, fy + fh // 2
            if bx < cx < bx + bw and by < cy < by + bh:
                face_in_box = True
                cv2.rectangle(display, (fx, fy), (fx + fw, fy + fh), (0, 255, 0), 2)

        if face_in_box:
            if face_detected_at is None:
                face_detected_at = datetime.now()
            held = (datetime.now() - face_detected_at).total_seconds()
            remaining = max(0.0, HOLD_SECONDS - held)
            cv2.putText(display, f"Hold still... {remaining:.1f}s",
                        (bx, by - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if held >= HOLD_SECONDS:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                success = cv2.imwrite(save_path, frame)
                if not success:
                    print(f"Failed to save snapshot to {save_path}")
                    break
                print(f"Snapshot captured.")
                snapshot_taken = True
                break
        else:
            face_detected_at = None
            cv2.putText(display, "Position face in box",
                        (bx, by - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

        cv2.imshow("FaceCheck - Look at the camera", display)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            print("Check-in cancelled.")
            break

    cam.release()
    cv2.destroyAllWindows()
    return snapshot_taken


def compare_faces(snapshot_path: str, stored_photo_path: str) -> dict:
    """
    Compares a live snapshot against a stored yearbook photo using DeepFace.
    Returns a dict with:
        - match (bool): True if faces match
        - confidence (float): similarity percentage
        - message (str): human readable result
    """
    try:
        result = DeepFace.verify(
            img1_path=snapshot_path,
            img2_path=stored_photo_path,
            model_name="VGG-Face",
            enforce_detection=False   # don't crash if face detection is uncertain
        )

        is_match = result["verified"]
        distance = result["distance"]
        threshold = result["threshold"]

        # Convert distance to a confidence percentage
        confidence = round((1 - distance / threshold) * 100, 1)
        confidence = max(0, min(confidence, 100))  # clamp between 0-100

        if is_match:
            message = f"Face matched! Confidence: {confidence}%"
        else:
            message = f"Face mismatch. Confidence: {confidence}%"

        print(message)
        return {
            "match": is_match,
            "confidence": confidence,
            "message": message
        }

    except Exception as e:
        print(f"Face comparison error: {e}")
        return {
            "match": False,
            "confidence": 0,
            "message": f"Error during face comparison: {str(e)}"
        }


def cleanup_temp(path: str):
    """Delete a temporary snapshot file after comparison."""
    if os.path.exists(path):
        os.remove(path)
        print(f"Temp file deleted: {path}")


if __name__ == "__main__":
    # Quick standalone test - captures your face and compares to your yearbook photo
    SNAPSHOT_PATH = "photos/temp/test_snapshot.jpg"
    STORED_PHOTO  = "photos/10019893.jpg"   # your yearbook photo

    print("=== Face Recognition Test ===")
    print(f"Will compare snapshot against: {STORED_PHOTO}\n")

    # Step 1 - capture
    taken = capture_snapshot(SNAPSHOT_PATH)

    if taken:
        # Step 2 - compare
        result = compare_faces(SNAPSHOT_PATH, STORED_PHOTO)
        print(f"\nResult: {result['message']}")

        # Step 3 - cleanup
        cleanup_temp(SNAPSHOT_PATH)
    else:
        print("No snapshot taken - test cancelled.")