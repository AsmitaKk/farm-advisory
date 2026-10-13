@echo off
echo ========================================================
echo         AGRICULTURE HELPER - PROJECT LAUNCHER
echo ========================================================
echo.

echo Checking and installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================================
echo   Server is starting at: http://127.0.0.1:5000
echo ========================================================
echo.
echo   DEMO CREDENTIALS & 2 DIFFERENT DASHBOARDS:
echo.
echo   1) FARMER / USER DASHBOARD: http://127.0.0.1:5000/dashboard
echo      - Email:    farmer@gmail.com
echo      - Password: 12345
echo      - Features: Weather advisory, crop advisor, live mandi rates,
echo                  order history, ask expert inquiries.
echo.
echo   2) SINGLE ADMIN DASHBOARD: http://127.0.0.1:5000/admin-dashboard
echo      - Username: admin   (or Email: admin@gmail.com)
echo      - Password: 123
echo      - Access:   ONLY ONE person in the system can log in as Admin.
echo      - Features: Manage entire website, crops, mandi prices, orders, users.
echo ========================================================
echo.

python python\app.py
pause
