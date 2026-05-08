# FaceCheck — Dual-Factor Biometric Attendance System

> A smart school check-in system that replaces manual ID scanning with dual-factor verification — matching each student's live face to their yearbook photo and ID barcode automatically, with a real-time attendance dashboard for security and teachers.

---

## Overview

FaceCheck is a biometric attendance system built for high school environments. Instead of manually scanning IDs or relying on teachers to take attendance, students simply walk up to a check-in station, scan their school ID barcode, and look at the camera. The system simultaneously verifies their identity using facial recognition and logs their arrival — flagging anyone who arrives after the tardy threshold.

This project was inspired by dual-factor biometric verification systems used in airports and secure facilities, adapted for a school setting.

---

## Features

- **Dual-Factor Verification** — Combines barcode scanning and live facial recognition to confirm identity, preventing ID sharing or misuse
- **Real-Time Check-In Logging** — Every check-in is timestamped and written to Firebase instantly
- **Tardy Detection** — Automatically flags students who arrive after 7:40 AM
- **Admin Dashboard** — Security staff and teachers can view live attendance, filter by homeroom or grade, and search by student name or ID
- **Mismatch Alerts** — If a face doesn't match the scanned ID, the system flags it and alerts the front desk
- **Yearbook Photo Integration** — Uses each student's existing yearbook photo as their registered face — no separate enrollment needed

---

## Tech Stack

| Layer | Technology |
|---|---|
| Face Recognition | DeepFace (Python) |
| Barcode Reading | USB barcode scanner + Python input handler |
| Backend API | FastAPI (Python) |
| Database | Firebase Firestore |
| Photo Storage | Firebase Storage |
| Frontend | React + Tailwind CSS |
| Auth | Firebase Authentication |

---

## Project Structure

```
facecheck/
├── backend/
│   ├── main.py               # FastAPI app entry point
│   ├── verify.py             # Core verification logic (face + barcode)
│   ├── attendance.py         # Check-in logging and tardy detection
│   ├── firebase.py           # Firebase connection and helpers
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CheckInDisplay.jsx    # Entrance screen (green/red result panel)
│   │   │   ├── AdminDashboard.jsx    # Attendance table and filters
│   │   │   └── AlertPanel.jsx        # Mismatch and unknown ID alerts
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── tailwind.config.js
├── scripts/
│   └── seed_students.py      # Script to populate Firebase with student data
├── README.md
└── .env.example
```

---

## How It Works

### Verification Flow
1. Student approaches the check-in station
2. USB barcode scanner reads their school ID → extracts student ID number
3. System fetches the student's record and yearbook photo from Firebase
4. Webcam captures a live frame of the student's face
5. DeepFace compares the live face to the stored yearbook photo
6. If confidence score exceeds threshold → **Verified**
7. If faces don't match → **Mismatch flagged**
8. Result is logged to Firestore with a timestamp and present/tardy status

### Tardy Logic
- Check-ins before **7:40 AM** → marked **Present**
- Check-ins at or after **7:40 AM** → marked **Tardy**
- Duplicate check-ins (same student, same day) → ignored after first

---

## Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- Firebase project (Firestore + Storage enabled)
- USB barcode scanner
- Webcam

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/facecheck.git
cd facecheck
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` and add your Firebase credentials.

```bash
uvicorn main:app --reload
```

### 3. Seed the Database
```bash
cd scripts
python seed_students.py
```
This populates Firebase with student records and uploads yearbook photos to Firebase Storage.

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/verify` | Run dual-factor verification for a student |
| `GET` | `/attendance/today` | Get all check-ins for today |
| `GET` | `/attendance/{student_id}` | Get a specific student's attendance history |
| `GET` | `/attendance/tardy` | Get all tardy students for today |
| `GET` | `/students/{student_id}` | Get a student's profile |

---

## Admin Dashboard

The admin dashboard is accessible to security staff and teachers and includes:

- **Live Check-In Feed** — updates in real time as students arrive
- **Attendance Table** — filterable by homeroom, grade, and tardy status
- **Search** — find any student by name or ID number
- **Summary Stats** — total present, total tardy, total not yet arrived
- **Alert Panel** — flags mismatches and unknown barcodes for staff review

---

## Future Work

- **Genesis SIS Integration** — In a full school deployment, this system would connect to the Genesis Student Information System via API, automatically syncing attendance records and eliminating the need for teachers to take attendance manually
- **Mobile Teacher View** — A lightweight mobile interface for teachers to check their class roster from anywhere
- **Multi-Entrance Support** — Scale to multiple camera/scanner stations across different school entrances
- **Analytics** — Tardiness trends over time, most common late arrival windows, homeroom comparisons

---

## 📄 License

This project was built as a Computer Science Capstone project at South Brunswick High School. Not licensed for commercial use.

---

## 👤 Author

Built by Arjun Gilhotra · South Brunswick High School · Class of 2026

*Capstone Project — Computer Science*
