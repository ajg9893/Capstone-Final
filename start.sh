#!/bin/bash
# start.sh — start all three FaceCheck processes
# API and dashboard run in the background; kiosk runs in the foreground
# so keyboard input (typing a student ID) works when no scanner is connected.

cd "$(dirname "$0")"

PYTHON=".venv/bin/python"

# Start API in background
$PYTHON app.py &
API_PID=$!
echo "✅ API started"

# Start dashboard in background
(cd dashboard && npm run dev) &
DASH_PID=$!
echo "✅ Dashboard started"

echo ""
echo "FaceCheck is running → open http://localhost:5173"
echo "Press Ctrl+C to stop everything"
echo ""

# Kill background jobs on exit
trap "echo ''; echo 'Stopping...'; kill $API_PID $DASH_PID 2>/dev/null; exit" INT TERM

# Run kiosk in the FOREGROUND so keyboard input works
$PYTHON verify.py
