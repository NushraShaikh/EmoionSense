import cv2
import numpy as np
from download_model import load_pretrained_emotion_model

# Load Haar Cascade and pre-trained model
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
model = load_pretrained_emotion_model()

# Emotion labels
emotion_list = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

# Function to get suggestions based on emotion
def get_suggestion(emotion):
    if emotion in ["sad", "angry", "fearful"]:
        return "Pay more attention to this child."
    elif emotion == "happy":
        return "Child is in a good mood!"
    elif emotion == "surprised":
        return "Check surroundings, child may be startled."
    else:
        return "Keep observing the child's behavior."

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Use the original color frame for emotion prediction
        face = frame[y:y+h, x:x+w]
        face = cv2.resize(face, (48, 48)).astype("float32") / 255.0
        face = np.expand_dims(face, axis=0)  # Shape: (1, 48, 48, 3)

        # Predict emotion
        preds = model.predict(face)[0]
        emotion = emotion_list[np.argmax(preds)]
        suggestion = get_suggestion(emotion)

        # Draw rectangle and text on the frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        cv2.putText(frame, suggestion, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Show the frame
    cv2.imshow("Emotion Sense - Press Q to Quit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
