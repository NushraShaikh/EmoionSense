from flask import Flask, render_template, request
from deepface import DeepFace
import cv2
import numpy as np
import base64
import pyttsx3
import csv
from datetime import datetime
from googletrans import Translator
import os
import threading  # Move this to the top

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB limit

# Text-to-speech setup
engine = pyttsx3.init()

# Emotion feedback messages
feedbacks = {
    'happy': "Great! The child looks happy. Keep it up!",
    'sad': "The child seems sad. Maybe try talking to them.",
    'angry': "The child is angry. Give them some space and time.",
    'surprise': "The child is surprised. Something caught their attention.",
    'fear': "The child appears scared. Check if they’re okay.",
    'disgust': "The child seems uncomfortable. Make sure everything is fine.",
    'neutral': "The child looks calm and neutral."
}

# CSV file setup
csv_file = 'emotion_log.csv'
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Child Name', 'Emotion'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    try:
        child_name = request.form['childName']
        data_url = request.form['image']
        selected_language = request.form['language']  # NEW

        encoded_data = data_url.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)[0]
        emotion = result['dominant_emotion'].lower()
        feedback = feedbacks.get(emotion, "Emotion detected.")

        # Translate feedback
        translator = Translator()
        translated_feedback = feedback
        if selected_language != 'en':
            translated_feedback = translator.translate(feedback, dest=selected_language).text

        # Voice feedback only in English (safe for pyttsx3)
        def speak_feedback():
            try:
                engine.stop()
                if selected_language == 'en':
                    engine.say(f"{child_name}'s emotion is {emotion}. {feedback}")
                engine.runAndWait()
            except RuntimeError:
                print("Voice engine already running.")

        threading.Thread(target=speak_feedback).start()

        # Save to CSV
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), child_name, emotion])

        return render_template('index.html', emotion=emotion.capitalize(), feedback=translated_feedback, name=child_name)

    except Exception as e:
        return render_template('index.html', emotion="Error", feedback=str(e))


@app.route('/log')
def view_log():
    records = []
    try:
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            records = list(reader)
    except Exception as e:
        print("Error reading CSV:", e)

    return render_template('log.html', records=records)
import matplotlib.pyplot as plt
from collections import Counter
import io
import base64

@app.route('/summary')
def emotion_summary():
    emotions = []
    try:
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                emotions.append(row[2])  # Get the emotion column
    except Exception as e:
        return f"Error reading CSV: {e}"

    count = Counter(emotions)

    # Bar chart
    fig1, ax1 = plt.subplots()
    ax1.bar(count.keys(), count.values(), color='skyblue')
    ax1.set_title('Emotion Frequency - Bar Chart')
    ax1.set_ylabel('Count')

    img1 = io.BytesIO()
    fig1.savefig(img1, format='png')
    img1.seek(0)
    bar_chart = base64.b64encode(img1.getvalue()).decode()

    # Pie chart
    fig2, ax2 = plt.subplots()
    ax2.pie(count.values(), labels=count.keys(), autopct='%1.1f%%', startangle=90)
    ax2.set_title('Emotion Distribution - Pie Chart')

    img2 = io.BytesIO()
    fig2.savefig(img2, format='png')
    img2.seek(0)
    pie_chart = base64.b64encode(img2.getvalue()).decode()

    plt.close(fig1)
    plt.close(fig2)

    return render_template('summary.html', bar_chart=bar_chart, pie_chart=pie_chart)



if __name__ == '__main__':
    app.run(debug=True)
