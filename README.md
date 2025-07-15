# Quantix Memory AI 🧠

**Never forget anything again. Your smart memory companion.**

An AI-powered assistant that detects items you've forgotten to pack or carry before leaving a room, using object detection, habit tracking, and smart reminders.

## ✨ Features

- **🔍 Smart Object Detection**: Uses YOLOv8 to detect commonly used daily items
- **📊 Habit Learning**: Learns from your daily routines and provides personalized reminders
- **⏰ Time-based Alerts**: Sends alerts based on your schedule (morning, afternoon, evening)
- **🎯 Priority System**: Categorizes items by importance (high, medium, low priority)
- **📱 Real-time Monitoring**: Live camera feed with bounding boxes and status indicators
- **🔔 Smart Notifications**: Voice alerts and visual notifications for missing items
- **📈 Habit Management**: Easy-to-use interface to manage your daily items and routines

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **AI/ML**: YOLOv8 (Ultralytics) for object detection
- **Computer Vision**: OpenCV for camera feed processing
- **Database**: SQLite for storing user habits and detection logs
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Real-time**: WebSocket (Socket.IO) for live updates
- **Optional**: Text-to-Speech (pyttsx3) for voice alerts

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam (for live detection)
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd quantix-memory-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 📖 Usage Guide

### 1. Getting Started
- Visit the home page to learn about features
- Click "Get Started" to access the dashboard

### 2. Managing Habits
- Go to the "Habits" page to configure your daily items
- Add items like phone, keys, wallet, charger, etc.
- Set frequency (daily, weekdays, weekends)
- Choose time of day and location
- Set priority levels

### 3. Live Detection
- On the dashboard, click "Start Detection"
- The camera will activate and begin monitoring
- View detected items in real-time
- Get alerts for missing items

### 4. Test Detection
- Use the "Test Detection" button to upload an image
- See what items are detected in the image
- Check which items are missing based on your habits

## 🎯 How It Works

### 1. Training Phase
- YOLOv8 model is trained to recognize common objects
- Default items include: phone, keys, wallet, charger, glasses, laptop, water bottle

### 2. Monitoring Phase
- Camera feed continuously monitors your room
- AI detects objects in real-time
- Compares detected items with your habit checklist

### 3. Alert System
- If items are missing based on your routine, alerts are triggered
- Time-based filtering (morning, afternoon, evening)
- Priority-based notifications

### 4. Learning
- System learns from your patterns over time
- Improves suggestions based on your actual usage

## 📁 Project Structure

```
quantix-memory-ai/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html        # Landing page
│   ├── dashboard.html    # Main dashboard
│   └── habits.html       # Habit management
├── static/               # Static files (CSS, JS, images)
└── memory_ai.db          # SQLite database (created automatically)
```

## 🔧 Configuration

### Default Items
The system comes with pre-configured common items:
- Phone (daily, morning, desk, high priority)
- Keys (daily, morning, table, high priority)
- Wallet (daily, morning, desk, high priority)
- Charger (daily, morning, desk, medium priority)
- Glasses (daily, morning, desk, medium priority)
- Laptop (weekdays, morning, desk, high priority)
- Water bottle (daily, morning, kitchen, low priority)

### Customization
- Add your own items through the web interface
- Modify detection sensitivity
- Adjust alert preferences
- Customize time windows

## 🎨 Features in Detail

### Smart Detection
- **Object Recognition**: Identifies 80+ common objects
- **Confidence Scoring**: Shows detection confidence levels
- **Real-time Processing**: Minimal latency for live feed

### Habit Management
- **Flexible Scheduling**: Daily, weekday, or weekend patterns
- **Time Windows**: Morning, afternoon, or evening specific
- **Location Tracking**: Track where items should be
- **Priority Levels**: High, medium, low importance

### Alert System
- **Visual Notifications**: Color-coded alerts
- **Modal Popups**: Detailed missing item information
- **Status Indicators**: Real-time system status
- **Voice Alerts**: Optional text-to-speech notifications

## 🔒 Privacy & Security

- **Local Processing**: All AI processing happens locally
- **No Cloud Storage**: Your data stays on your device
- **Camera Access**: Only when detection is active
- **Secure Database**: SQLite with proper access controls

## 🐛 Troubleshooting

### Common Issues

1. **Camera not working**
   - Check camera permissions
   - Ensure no other app is using the camera
   - Try refreshing the page

2. **Detection not accurate**
   - Ensure good lighting
   - Position camera properly
   - Check if items are clearly visible

3. **App not starting**
   - Verify Python version (3.8+)
   - Check all dependencies are installed
   - Ensure port 5000 is available

### Performance Tips

- Use a modern web browser
- Ensure adequate lighting for detection
- Close unnecessary applications
- Position camera at optimal angle

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Ultralytics](https://github.com/ultralytics/ultralytics) for YOLOv8
- [OpenCV](https://opencv.org/) for computer vision
- [Flask](https://flask.palletsprojects.com/) for web framework
- [Bootstrap](https://getbootstrap.com/) for UI components

## 📞 Support

For support, questions, or feature requests:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

**Made with ❤️ for better memory management** 