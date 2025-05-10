from textblob import TextBlob
import cv2
from deepface import DeepFace
import numpy as np



def get_text_sentiment(text):
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        if sentiment_score > 0:
            return "Positive"
        elif sentiment_score < 0:
            return "Negative"
        else:
            return "Neutral"

def perform_emotion_analysis_on_frame(frame):
    if frame is None:
        return None, None, None

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    filestr = frame.read()
    npimg = np.frombuffer(filestr, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
    print('this is my type of converted image', type(frame))

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    sentiment = None
    dominant_emotion = None

    for (x, y, w, h) in faces:
        img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        face_roi = frame[y:y + h, x:x + w]
        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']
        sentiment = get_text_sentiment(dominant_emotion)
        update_sentiment_output(result, sentiment, dominant_emotion)

        cv2.putText(frame, f"Emotion: {dominant_emotion}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        cv2.putText(frame, f"Sentiment: {sentiment}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    return frame, sentiment, dominant_emotion

def update_sentiment_output(result, sentiment, emotion):
    global saved_result, saved_sentiment, saved_emotion
    saved_result = result
    saved_sentiment = sentiment
    saved_emotion = emotion
