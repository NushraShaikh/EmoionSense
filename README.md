EmotionSense - Webcam Based Emotion Detection for Non-Verbal Children
=====================================================================

📁 Project Folder: EmotionSense2

💻 Description:
EmotionSense is a real-time emotion detection system designed to help identify emotions in children who cannot speak or express themselves. It uses a webcam to detect the child's face, analyzes emotions using DeepFace, gives text and voice feedback, and stores results in a CSV log file. It also includes graphs, dark/light mode, accessibility features, and multi-language support.

🛠️ How to Run:
1. Install Python (preferably 3.10 or 3.11).
2. Open CMD and navigate to the EmotionSense2 folder.
   > cd EmotionSense2
3. Install required libraries:
   > pip install -r requirements.txt
4. (Optional) Download the model beforehand:
   > python download_model.py
5. Run the application:
   > python app.py
6. Or just double-click:
   > run_emotionsense.bat

🌐 Open your browser and go to:
   http://127.0.0.1:5000

📦 Requirements:
- Flask
- DeepFace
- OpenCV (cv2)
- pyttsx3
- numpy
- googletrans==4.0.0-rc1
- matplotlib

📄 Data:
- All emotion detections are saved in 'emotion_log.csv' with timestamp, child name, and emotion.
- View log: Click "View Emotion Log"
- View charts: Click "View Summary Charts"

✅ Features:
- Webcam-based real-time emotion detection
- Text and speech feedback
- CSV emotion logging
- Dark/Light mode
- Accessibility-friendly UI (large fonts, buttons)
- Multi-language support (basic)

CONTACT
Name: Nusra Shakh
Email: nushrashaikh9@gmail.com 
