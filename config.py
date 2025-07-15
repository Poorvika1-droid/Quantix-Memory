"""
Configuration file for Quantix Memory AI
"""

import os

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'quantix_memory_ai_secret_key_2024'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Server Configuration
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Database Configuration
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'memory_ai.db')
    
    # AI Model Configuration
    MODEL_PATH = os.environ.get('MODEL_PATH', 'yolov8n.pt')
    CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', 0.5))
    
    # Camera Configuration
    CAMERA_INDEX = int(os.environ.get('CAMERA_INDEX', 0))
    FRAME_WIDTH = int(os.environ.get('FRAME_WIDTH', 640))
    FRAME_HEIGHT = int(os.environ.get('FRAME_HEIGHT', 480))
    FPS = int(os.environ.get('FPS', 30))
    
    # Detection Configuration
    DETECTION_INTERVAL = float(os.environ.get('DETECTION_INTERVAL', 1.0))  # seconds
    ALERT_COOLDOWN = int(os.environ.get('ALERT_COOLDOWN', 30))  # seconds
    
    # Time Windows (24-hour format)
    MORNING_START = 5   # 5 AM
    MORNING_END = 12    # 12 PM
    AFTERNOON_START = 12 # 12 PM
    AFTERNOON_END = 17  # 5 PM
    EVENING_START = 17  # 5 PM
    EVENING_END = 24    # 12 AM
    
    # Default Items Configuration
    DEFAULT_ITEMS = [
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
        },
        {
            'item_name': 'glasses',
            'frequency': 'daily',
            'time_of_day': 'morning',
            'location': 'desk',
            'priority': 2
        },
        {
            'item_name': 'laptop',
            'frequency': 'weekday',
            'time_of_day': 'morning',
            'location': 'desk',
            'priority': 1
        },
        {
            'item_name': 'water_bottle',
            'frequency': 'daily',
            'time_of_day': 'morning',
            'location': 'kitchen',
            'priority': 3
        }
    ]
    
    # UI Configuration
    THEME_COLORS = {
        'primary': '#6366f1',
        'secondary': '#8b5cf6',
        'success': '#10b981',
        'warning': '#f59e0b',
        'danger': '#ef4444',
        'info': '#06b6d4'
    }
    
    # Notification Configuration
    ENABLE_VOICE_ALERTS = os.environ.get('ENABLE_VOICE_ALERTS', 'False').lower() == 'true'
    ENABLE_PUSH_NOTIFICATIONS = os.environ.get('ENABLE_PUSH_NOTIFICATIONS', 'True').lower() == 'true'
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'quantix_memory_ai.log')
    
    # Security Configuration
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    
    @staticmethod
    def get_time_of_day(hour):
        """Determine time of day based on hour"""
        if Config.MORNING_START <= hour < Config.MORNING_END:
            return 'morning'
        elif Config.AFTERNOON_START <= hour < Config.AFTERNOON_END:
            return 'afternoon'
        else:
            return 'evening'
    
    @staticmethod
    def is_weekday(weekday):
        """Check if it's a weekday (0=Monday, 6=Sunday)"""
        return weekday < 5 