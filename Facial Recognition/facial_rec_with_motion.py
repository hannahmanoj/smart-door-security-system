import face_recognition
import cv2
import numpy as np
from picamera2 import Picamera2
import time
import pickle
from gpiozero import LED, MotionSensor
import sqlite3
from datetime import datetime
import os

# Initialize motion sensor
green_led = LED(17)
pir = MotionSensor(4)
green_led.off()

# Load pre-trained face encodings
print("[INFO] loading encodings...")
with open("encodings.pickle", "rb") as f:
    data = pickle.loads(f.read())
known_face_encodings = data["encodings"]
known_face_names = data["names"]

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1280, 720)}))
picam2.start()

cv_scaler = 4  # Scale factor for performance
face_locations = []
face_encodings = []
face_names = []
frame_count = 0
start_time = time.time()
fps = 0

prev_detected_names = set()

# Dictionary to track last insertion time per person
last_insert_times = {}

def image_to_blob(image):
    """Convert image (numpy array) to binary format (BLOB)"""
    _, buffer = cv2.imencode('.jpg', image)
    return buffer.tobytes()

def save_to_database(name, frame):
    global last_insert_times
    
    current_time = datetime.now()
    
    #check if this person has bee logged in the last five minutes
    if name in last_insert_times and (current_time - last_insert_times[name]).total_seconds() < 300:
        print(f"Skipping insertion for {name}. Less than 5 minutes since last save. ")
        return
    
    #update the last insert time for this person
    last_insert_times[name] = current_time
    
    #connect to the sqlite database (faces.db)
    conn = sqlite3.connect("faces_log.db")
    cursor = conn.cursor()
    
    #generate a timestamp for database entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    #define folder where images will be saved
    folder = "logs"
    
    #checks if folder exists if not it will create it
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    # Convert the image to BLOB format
    image_blob = image_to_blob(frame)
    
    
    # Insert a record into the "face_logs" table with name, timestamp, and image path
    cursor.execute("INSERT INTO face_logs (name, timestamp, image) VALUES (?, ?, ?)", 
                   (name, timestamp, image_blob))
    
    # Commit the transaction to save changes in the database
    conn.commit()
    
    # Close the database connection
    conn.close()
    
    print(f"Saved {name} to database at {timestamp}")

def process_frame(frame):
    global face_locations, face_encodings, face_names, prev_detected_names
    resized_frame = cv2.resize(frame, (0, 0), fx=(1/cv_scaler), fy=(1/cv_scaler))
    rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_resized_frame)
    face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')
    
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            
        face_names.append(name)
        
        #save recognised/unrecognised face to database
        save_to_database(name, frame)
        
    detected_set = set(face_names)
        
    if detected_set != prev_detected_names:
        print(f"Detected: {', '.join(detected_set)}")
        prev_detected_names = detected_set
        
    return frame

def draw_results(frame):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= cv_scaler
        right *= cv_scaler
        bottom *= cv_scaler
        left *= cv_scaler
        cv2.rectangle(frame, (left, top), (right, bottom), (244, 42, 3), 3)
        cv2.rectangle(frame, (left - 3, top - 35), (right + 3, top), (244, 42, 3), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)
    return frame

def calculate_fps():
    global frame_count, start_time, fps
    frame_count += 1
    elapsed_time = time.time() - start_time
    if elapsed_time > 1:
        fps = frame_count / elapsed_time
        frame_count = 0
        start_time = time.time()
    return fps

while True:
    pir.wait_for_motion()
    print("Motion Detected")
    green_led.on()
    
    while pir.motion_detected:
        frame = picam2.capture_array()
        processed_frame = process_frame(frame)
        display_frame = draw_results(processed_frame)
        current_fps = calculate_fps()
        cv2.putText(display_frame, f"FPS: {current_fps:.1f}", (display_frame.shape[1] - 150, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Video', display_frame)
        if cv2.waitKey(1) == ord("q"):
            break
    
    green_led.off()
    print("Motion Stopped")
    cv2.destroyAllWindows()

cv2.destroyAllWindows()
picam2.stop()