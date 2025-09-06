#!/bin/bash

echo "Starting Quenito Production Environment"
echo "Model: claude-sonnet-4-20250514"
echo "========================================="

# Start virtual display
echo "Starting virtual display..."
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
sleep 2

# Start window manager
echo "Starting window manager..."
mutter &
sleep 2

# Start VNC server on port 5900
echo "Starting VNC server on port 5900..."
x11vnc -display :99 -forever -shared -passwd quenito123 -rfbport 5900 &
sleep 2

# Launch Chrome instead of Firefox
echo "Starting Google Chrome..."
google-chrome --no-sandbox --disable-gpu --disable-dev-shm-usage --window-size=1024,768 --new-window about:blank &
sleep 3

# Start monitoring API (optional)
echo "Starting monitoring API on port 8080..."
cd /app && python3 monitor.py &
sleep 2

# Run main orchestrator
echo "========================================="
echo "Ready for manual setup!"
echo "VNC: vnc://localhost:5900 (password: quenito123)"
echo "Browser: Google Chrome (ready)"
echo "========================================="
cd /app && python3 orchestrator.py