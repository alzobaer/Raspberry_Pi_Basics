import cv2
import time
from servo_control import ServoController

# Initialize servos on GPIO 17 (horizontal) and GPIO 27 (vertical)
servo = ServoController(17, 27)

# Initialize camera
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Explicitly set the V4L2 backend

# Load OpenCV's pre-trained Haar cascade for face detection
face_cascade = cv2.CascadeClassifier('/home/zobaerpi/opencv_haarcascades/haarcascade_frontalface_default.xml')

frame_width = 640
frame_height = 480

# Center position for frame
center_x = frame_width // 2
center_y = frame_height // 2

# Sensitivity for movement
sensitivity = 20

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (frame_width, frame_height))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            # Get the largest face
            (x, y, w, h) = max(faces, key=lambda b: b[2] * b[3])

            # Calculate face center
            face_center_x = x + w // 2
            face_center_y = y + h // 2

            # Calculate difference from center of frame
            delta_x = face_center_x - center_x
            delta_y = face_center_y - center_y

            # Move horizontally if necessary
            if abs(delta_x) > sensitivity:
                h_movement = -5 if delta_x > 0 else 5
                servo.set_angle(h_movement, 0)

            # Move vertically if necessary
            if abs(delta_y) > sensitivity:
                v_movement = -5 if delta_y > 0 else 5
                servo.set_angle(0, v_movement)

        # Display frame for debugging
        cv2.imshow("Face Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    servo.stop()
