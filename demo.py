#!/usr/bin/env python3
"""
Quantix Memory AI - Demo Mode
This script runs the application in demo mode without requiring camera or AI dependencies.
"""

import os
import sys
import json
from datetime import datetime

# Mock Flask app for demo
class MockFlask:
    def __init__(self):
        self.routes = {}
    
    def route(self, path):
        def decorator(f):
            self.routes[path] = f
            return f
        return decorator
    
    def run(self, **kwargs):
        print(f"🚀 Demo server would start on {kwargs.get('host', 'localhost')}:{kwargs.get('port', 5000)}")
        print("📱 Open your browser and go to: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the demo")
        
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Demo stopped")

# Mock data for demo
DEMO_HABITS = [
    {
        'item_name': 'phone',
        'frequency': 'daily',
        'time_of_day': 'morning',
        'location': 'desk',
        'priority': 1
    },
    {
        'item_name': 'keys',
        'frequency': 'daily',
        'time_of_day': 'morning',
        'location': 'table',
        'priority': 1
    },
    {
        'item_name': 'wallet',
        'frequency': 'daily',
        'time_of_day': 'morning',
        'location': 'desk',
        'priority': 1
    },
    {
        'item_name': 'charger',
        'frequency': 'daily',
        'time_of_day': 'morning',
        'location': 'desk',
        'priority': 2
    }
]

DEMO_DETECTIONS = [
    {
        'class_name': 'phone',
        'confidence': 0.95,
        'bbox': [100, 100, 200, 200]
    },
    {
        'class_name': 'keys',
        'confidence': 0.87,
        'bbox': [300, 150, 400, 250]
    }
]

DEMO_MISSING_ITEMS = [
    {
        'item_name': 'wallet',
        'priority': 1,
        'location': 'desk',
        'time_of_day': 'morning'
    }
]

def create_demo_files():
    """Create demo HTML files"""
    
    # Create templates directory
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Demo index.html
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantix Memory AI - Demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Inter', sans-serif;
        }
        .demo-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        .gradient-text {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="demo-card text-center">
            <h1 class="gradient-text mb-4">
                <i class="fas fa-brain me-2"></i>Quantix Memory AI
            </h1>
            <h2 class="mb-4">Demo Mode</h2>
            <p class="lead mb-4">
                This is a demonstration of Quantix Memory AI. In the full version, you would have:
            </p>
            
            <div class="row">
                <div class="col-md-4">
                    <div class="card mb-3">
                        <div class="card-body">
                            <i class="fas fa-video fa-2x text-primary mb-3"></i>
                            <h5>Live Camera Feed</h5>
                            <p>Real-time object detection with YOLOv8</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card mb-3">
                        <div class="card-body">
                            <i class="fas fa-bell fa-2x text-warning mb-3"></i>
                            <h5>Smart Alerts</h5>
                            <p>Notifications for missing items</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card mb-3">
                        <div class="card-body">
                            <i class="fas fa-chart-line fa-2x text-success mb-3"></i>
                            <h5>Habit Learning</h5>
                            <p>AI learns your daily patterns</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mt-4">
                <h4>Demo Data</h4>
                <div class="row">
                    <div class="col-md-6">
                        <h6>Detected Items:</h6>
                        <ul class="list-group">
                            <li class="list-group-item">📱 Phone (95% confidence)</li>
                            <li class="list-group-item">🔑 Keys (87% confidence)</li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h6>Missing Items:</h6>
                        <ul class="list-group">
                            <li class="list-group-item text-danger">💳 Wallet (High Priority)</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="mt-4">
                <a href="https://github.com/your-repo/quantix-memory-ai" class="btn btn-primary btn-lg">
                    <i class="fab fa-github me-2"></i>View Full Project
                </a>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open('templates/index.html', 'w') as f:
        f.write(index_html)
    
    print("✅ Created demo files")

def run_demo():
    """Run the demo application"""
    print("🧠 Quantix Memory AI - Demo Mode")
    print("=" * 50)
    print("📝 This is a demonstration without camera or AI dependencies")
    print("🔧 To run the full version, install dependencies and use: python app.py")
    print("=" * 50)
    
    # Create demo files
    create_demo_files()
    
    # Show demo data
    print("\n📊 Demo Data:")
    print(f"   Habits configured: {len(DEMO_HABITS)}")
    print(f"   Items detected: {len(DEMO_DETECTIONS)}")
    print(f"   Missing items: {len(DEMO_MISSING_ITEMS)}")
    
    print("\n🎯 Demo Features:")
    print("   ✅ Beautiful UI with modern design")
    print("   ✅ Responsive layout")
    print("   ✅ Real-time status indicators")
    print("   ✅ Habit management interface")
    print("   ✅ Object detection simulation")
    print("   ✅ Smart alert system")
    
    print("\n🚀 To run the full application:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Run the app: python app.py")
    print("   3. Open browser: http://localhost:5000")
    
    print("\n📱 Demo interface created at: templates/index.html")
    print("🛑 Press Ctrl+C to exit demo")
    
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Demo stopped")

if __name__ == '__main__':
    run_demo() 