from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import sqlite3
import json
import os
from datetime import datetime, time
import threading
import time as time_module
from ultralytics import YOLO
import base64
from PIL import Image
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'quantix_memory_ai_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables
camera = None
model = None
is_detecting = False
user_habits = {}
current_items = set()

class MemoryAI:
    def __init__(self):
        self.db_path = 'memory_ai.db'
        self.init_database()
        self.load_model()
        
    def init_database(self):
        """Initialize SQLite database with tables for habits and items"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create habits table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                frequency TEXT NOT NULL,
                time_of_day TEXT,
                location TEXT,
                priority INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create detection_log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detection_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                detected BOOLEAN NOT NULL,
                confidence REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert some default items
        default_items = [
            ('phone', 'daily', 'morning', 'desk', 1),
            ('keys', 'daily', 'morning', 'table', 1),
            ('wallet', 'daily', 'morning', 'desk', 1),
            ('charger', 'daily', 'morning', 'desk', 2),
            ('glasses', 'daily', 'morning', 'desk', 2),
            ('laptop', 'weekday', 'morning', 'desk', 1),
            ('water_bottle', 'daily', 'morning', 'kitchen', 3),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO habits (item_name, frequency, time_of_day, location, priority)
            VALUES (?, ?, ?, ?, ?)
        ''', default_items)
        
        conn.commit()
        conn.close()
    
    def load_model(self):
        """Load YOLOv8 model for object detection"""
        try:
            # Try to load a pre-trained model, fallback to a basic one
            self.model = YOLO('yolov8n.pt')
            print("YOLOv8 model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def get_user_habits(self):
        """Get user habits from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT item_name, frequency, time_of_day, location, priority FROM habits')
        habits = cursor.fetchall()
        conn.close()
        
        return [{
            'item_name': habit[0],
            'frequency': habit[1],
            'time_of_day': habit[2],
            'location': habit[3],
            'priority': habit[4]
        } for habit in habits]
    
    def add_habit(self, item_name, frequency, time_of_day, location, priority=1):
        """Add a new habit to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO habits (item_name, frequency, time_of_day, location, priority)
            VALUES (?, ?, ?, ?, ?)
        ''', (item_name, frequency, time_of_day, location, priority))
        conn.commit()
        conn.close()
    
    def detect_objects(self, frame):
        """Detect objects in the frame using YOLOv8"""
        if self.model is None:
            return []
        
        try:
            results = self.model(frame)
            detections = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = box.conf[0].cpu().numpy()
                        class_id = int(box.cls[0].cpu().numpy())
                        class_name = result.names[class_id]
                        
                        detections.append({
                            'class_name': class_name,
                            'confidence': float(confidence),
                            'bbox': [int(x1), int(y1), int(x2), int(y2)]
                        })
            
            return detections
        except Exception as e:
            print(f"Error in object detection: {e}")
            return []
    
    def check_missing_items(self, detected_items):
        """Check which items are missing based on user habits"""
        habits = self.get_user_habits()
        current_time = datetime.now()
        current_hour = current_time.hour
        
        # Determine time of day
        if 5 <= current_hour < 12:
            time_of_day = 'morning'
        elif 12 <= current_hour < 17:
            time_of_day = 'afternoon'
        else:
            time_of_day = 'evening'
        
        # Determine if it's a weekday
        is_weekday = current_time.weekday() < 5
        
        missing_items = []
        detected_item_names = [item['class_name'] for item in detected_items]
        
        for habit in habits:
            item_name = habit['item_name']
            
            # Check if item should be present based on frequency and time
            should_be_present = False
            
            if habit['frequency'] == 'daily':
                should_be_present = True
            elif habit['frequency'] == 'weekday' and is_weekday:
                should_be_present = True
            elif habit['frequency'] == 'weekend' and not is_weekday:
                should_be_present = True
            
            # Check time of day
            if habit['time_of_day'] and habit['time_of_day'] != time_of_day:
                should_be_present = False
            
            # If item should be present but isn't detected
            if should_be_present and item_name not in detected_item_names:
                missing_items.append({
                    'item_name': item_name,
                    'priority': habit['priority'],
                    'location': habit['location'],
                    'time_of_day': habit['time_of_day']
                })
        
        return missing_items

# Initialize Memory AI
memory_ai = MemoryAI()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page with camera feed and alerts"""
    return render_template('dashboard.html')

@app.route('/habits')
def habits():
    """Habits management page"""
    return render_template('habits.html')

@app.route('/api/habits', methods=['GET'])
def get_habits():
    """API endpoint to get user habits"""
    habits = memory_ai.get_user_habits()
    return jsonify(habits)

@app.route('/api/habits', methods=['POST'])
def add_habit():
    """API endpoint to add a new habit"""
    data = request.json
    memory_ai.add_habit(
        data['item_name'],
        data['frequency'],
        data['time_of_day'],
        data['location'],
        data.get('priority', 1)
    )
    return jsonify({'status': 'success'})

@app.route('/api/detect', methods=['POST'])
def detect_items():
    """API endpoint for object detection"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    image_bytes = file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Detect objects
    detections = memory_ai.detect_objects(frame)
    
    # Check for missing items
    missing_items = memory_ai.check_missing_items(detections)
    
    return jsonify({
        'detections': detections,
        'missing_items': missing_items
    })

def generate_frames():
    """Generate camera frames for video streaming"""
    global camera, is_detecting
    
    camera = cv2.VideoCapture(0)
    
    while is_detecting:
        success, frame = camera.read()
        if not success:
            break
        
        # Detect objects
        detections = memory_ai.detect_objects(frame)
        
        # Draw bounding boxes
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{detection['class_name']} {detection['confidence']:.2f}",
                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Check for missing items
        missing_items = memory_ai.check_missing_items(detections)
        
        # Draw status
        if missing_items:
            status_text = f"Missing: {', '.join([item['item_name'] for item in missing_items])}"
            cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "All items detected ✓", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Convert frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    if camera:
        camera.release()

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/start_detection', methods=['POST'])
def start_detection():
    """Start object detection"""
    global is_detecting
    is_detecting = True
    return jsonify({'status': 'started'})

@app.route('/api/stop_detection', methods=['POST'])
def stop_detection():
    """Stop object detection"""
    global is_detecting, camera
    is_detecting = False
    if camera:
        camera.release()
    return jsonify({'status': 'stopped'})

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print('Client connected')
    emit('status', {'message': 'Connected to Quantix Memory AI'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 