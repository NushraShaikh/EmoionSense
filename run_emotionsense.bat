@echo off
echo Starting Flask App...

cd /d "C:\Users\Acer\EmotionSense\EmotionSense2"

call emotionenv\Scripts\activate

start "" /B python app.py

timeout /t 8 /nobreak > NUL

start "" "http://127.0.0.1:5000"

pause
