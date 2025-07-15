#!/usr/bin/env python3
"""
Quantix Memory AI - Startup Script
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask',
        'flask-socketio',
        'opencv-python',
        'ultralytics',
        'pillow',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing dependencies:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing dependencies...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("Please run: pip install -r requirements.txt")
            sys.exit(1)
    else:
        print("✅ All dependencies are installed")

def create_directories():
    """Create necessary directories"""
    directories = ['templates', 'static', 'logs']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def check_camera():
    """Check if camera is available"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera is available")
            cap.release()
        else:
            print("⚠️  Camera not detected - some features may not work")
    except ImportError:
        print("⚠️  OpenCV not installed - camera features will not work")
    except Exception as e:
        print(f"⚠️  Camera check failed: {e}")

def main():
    """Main startup function"""
    print("🧠 Quantix Memory AI - Starting up...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check dependencies
    check_dependencies()
    
    # Create directories
    create_directories()
    
    # Check camera
    check_camera()
    
    print("\n🚀 Starting Quantix Memory AI...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the application")
    print("=" * 50)
    
    # Start the application
    try:
        from app import app, socketio
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Quantix Memory AI...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 