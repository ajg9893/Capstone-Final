# FaceCheck — Biometric Attendance System

A dual-factor student check-in kiosk that combines **barcode scanning** and **face recognition** to automate classroom attendance. Built as a senior capstone project at South Brunswick High School.

---

## How It Works

1. A student scans their school ID barcode at the kiosk
2. The system looks up the student in Firebase
3. If a photo is enrolled, the webcam opens and DeepFace compares the live face against the stored photo
4. Attendance is logged to Firestore as **Present**, **Tardy**, or with a **Face Mismatch** flag
5. The teacher dashboard updates in real time — students move from "Not Yet Checked In" to the attendance table within 5 seconds

---

## Tech Stack

| Layer | Technology |
|---|---|
| Kiosk (Python) | OpenCV, DeepFace (VGG-Face), APScheduler |
| Barcode input | Netum NSL3 USB HID scanner |
| Backend API | Flask, flask-cors |
| Database | Firebase Firestore |
| Photo storage | Firebase Storage |
| Teacher dashboard | React + Vite |
| Auth / config | python-dotenv |

---

## Project Structure

```
FinalProject/
├── verify.py              # Main kiosk entry point — run this to start check-in
├── face_rec_module.py     # Webcam capture + DeepFace comparison
├── barcode_reader.py      # USB barcode scanner input
├── firebase_client.py     # All Firestore / Storage operations
├── app.py                 # Flask REST API (port 5000)
├── add_students_batch.py  # Bulk-enroll a class roster
├── add_student.py         # One-time enrollment for a single student
├── upload_photo.py        # Upload a photo for an already-enrolled student
├── requirements.txt
├── .env                   # Secret config (not committed)
├── serviceAccountKey.json # Firebase credentials (not committed)
├── photos/
│   └── <student_id>.jpg   # Enrollment photos
└── dashboard/             # React + Vite teacher dashboard
    └── src/
        ├── App.jsx
        └── components/
            ├── Header.jsx
            ├── StatsBar.jsx
            ├── AttendanceTable.jsx
            └── AbsentList.jsx
```

---

## Setup

### Prerequisites

- Python 3.11
- Node.js 18+
- A Firebase project with Firestore and Storage enabled

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/FaceCheck.git
cd FaceCheck
```

### 2. Python environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate      # macOS / Linux
pip install -r requirements.txt
```

### 3. Firebase credentials

- Download your Firebase service account key and save it as `serviceAccountKey.json` in the project root
- Create a `.env` file:

```
STORAGE_BUCKET=your-project-id.appspot.com
TARDY_HOUR=7
TARDY_MINUTE=40
RESET_HOUR=14
RESET_MINUTE=20
```

### 4. Dashboard dependencies

```bash
cd dashboard
npm install
```

---

## Running the Project

Open **three terminals**:

**Terminal 1 — Kiosk**
```bash
source .venv/bin/activate
python verify.py
```

**Terminal 2 — API**
```bash
source .venv/bin/activate
python app.py
```

**Terminal 3 — Dashboard**
```bash
cd dashboard
npm run dev
```

Then open [http://localhost:5173](http://localhost:5173) in a browser, click **Start Session**, and the kiosk is live.

---

## Enrolling Students

### Add a class roster (no photos)

Edit the `STUDENTS` list in `add_students_batch.py`, then run:

```bash
python add_students_batch.py
```

Students without photos will still appear on the dashboard and can check in — face verification is simply skipped for them.

### Upload a photo for a student

1. Place the photo at `photos/<student_id>.jpg`
2. Set `STUDENT_ID` at the top of `upload_photo.py`
3. Run:

```bash
python upload_photo.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/attendance/today` | Today's check-ins (optional `?status=present\|tardy`) |
| GET | `/api/attendance/absent` | Students not yet checked in |
| GET | `/api/stats` | Present / tardy counts |
| GET | `/api/students` | All enrolled students |
| GET | `/api/students/<id>` | Single student record |
| GET | `/api/session` | Current session state |
| POST | `/api/session/start` | Start a check-in session |
| POST | `/api/session/stop` | End a check-in session |
| POST | `/api/reset` | Manually archive and reset attendance |

---

## Notes

- `serviceAccountKey.json` and `.env` are in `.gitignore` and are never committed
- Attendance auto-archives daily at 2:20 PM via APScheduler
- Built and tested on macOS (Apple Silicon M1) with TensorFlow 2.21 native ARM64
