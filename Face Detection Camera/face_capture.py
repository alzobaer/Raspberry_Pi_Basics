import time
import os
import cv2
from picamera2 import Picamera2, Preview

# Create the 'images' folder if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

# Initialize Picamera2
picam = Picamera2()

# Configure the camera for preview mode
config = picam.create_preview_configuration()
picam.configure(config)

picam.start_preview(Preview.QTGL)

picam.start()

# Load the Haar cascade for face detection from OpenCV
face_cascade = cv2.CascadeClassifier('/home/zobaerpi/opencv_haarcascades/haarcascade_frontalface_default.xml')

for i in range(1, 10):
    # Capture a frame from the camera
    frame = picam.capture_array()

    # Convert the captured frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        # For each detected face, draw a rectangle around it and save the face region
        for (x, y, w, h) in faces:
            # Crop the face area
            face = frame[y:y+h, x:x+w]
            
            # Save the image with the face cropped
            face_filename = f"images/face_{i}.jpg"
            cv2.imwrite(face_filename, face)
            print(f"Captured face {i}")
        
    else:
        print(f"No face detected in image {i}")
    
    time.sleep(3)  # Wait for 3 seconds before the next capture

picam.stop()
