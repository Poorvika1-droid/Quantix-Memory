from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os
import flask
print("Flask version:", flask.__version__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'quantix_memory_ai_secret_key_2024')
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Only needed for first run or after DB reset
# with app.app_context():
#     db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime)
    habits = db.relationship('Habit', backref='user', lazy=True)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_name = db.Column(db.String(120), nullable=False)
    frequency = db.Column(db.String(120), nullable=False)
    time_of_day = db.Column(db.String(120))
    location = db.Column(db.String(120))
    priority = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

def hash_password(password):
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(email, password):
    user = User.query.filter_by(email=email, password_hash=hash_password(password)).first()
    if user:
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()
        return user
    return None

def create_user(email, password, name):
    if User.query.filter_by(email=email).first():
        return None
    user = User(email=email, password_hash=hash_password(password), name=name)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_habits(user_id):
    habits = Habit.query.filter_by(user_id=user_id).all()
    return [{
        'item_name': h.item_name,
        'frequency': h.frequency,
        'time_of_day': h.time_of_day,
        'location': h.location,
        'priority': h.priority
    } for h in habits]

def add_habit(user_id, item_name, frequency, time_of_day, location, priority=1):
    habit = Habit(user_id=user_id, item_name=item_name, frequency=frequency, time_of_day=time_of_day, location=location, priority=priority)
    db.session.add(habit)
    db.session.commit()

def delete_habit_db(user_id, item_name):
    habit = Habit.query.filter_by(user_id=user_id, item_name=item_name).first()
    if habit:
        db.session.delete(habit)
        db.session.commit()

def detect_objects_in_image(image_data, user_id):
    import base64, random
    user_habits = get_user_habits(user_id)
    habit_names = [habit['item_name'] for habit in user_habits]
    detections = []
    detected_items = set()
    if isinstance(image_data, str):
        if ',' in image_data:
            image_data = base64.b64decode(image_data.split(',')[1])
        else:
            image_data = base64.b64decode(image_data)
    # Simulate detection logic
    if 'phone' in habit_names and random.random() > 0.2:
        detections.append(create_detection('phone', 0.85, 0.9))
        detected_items.add('phone')
    if 'keys' in habit_names and random.random() > 0.4:
        detections.append(create_detection('keys', 0.75, 0.8))
        detected_items.add('keys')
    if 'laptop' in habit_names and random.random() > 0.5:
        detections.append(create_detection('laptop', 0.8, 0.85))
        detected_items.add('laptop')
    if 'wallet' in habit_names and random.random() > 0.6:
        detections.append(create_detection('wallet', 0.7, 0.8))
        detected_items.add('wallet')
    if 'glasses' in habit_names and random.random() > 0.7:
        detections.append(create_detection('glasses', 0.75, 0.85))
        detected_items.add('glasses')
    if 'water_bottle' in habit_names and random.random() > 0.5:
        detections.append(create_detection('water_bottle', 0.8, 0.9))
        detected_items.add('water_bottle')
    if 'charger' in habit_names and random.random() > 0.6:
        detections.append(create_detection('charger', 0.7, 0.8))
        detected_items.add('charger')
    if len(detections) < 2 and habit_names:
        remaining_items = [item for item in habit_names if item not in detected_items]
        for item in remaining_items[:2]:
            if random.random() > 0.3:
                detections.append(create_detection(item, 0.6, 0.8))
                detected_items.add(item)
    return detections

def create_detection(item_name, min_conf, max_conf):
    import random
    x1 = random.randint(50, 300)
    y1 = random.randint(50, 200)
    x2 = x1 + random.randint(80, 150)
    y2 = y1 + random.randint(80, 120)
    confidence = random.uniform(min_conf, max_conf)
    return {
        'class_name': item_name,
        'confidence': confidence,
        'bbox': [x1, y1, x2, y2]
    }

def find_missing_items(detected_items, user_id):
    user_habits = get_user_habits(user_id)
    detected_names = {item['class_name'] for item in detected_items}
    missing_items = []
    for habit in user_habits:
        if habit['item_name'] not in detected_names:
            missing_items.append(habit)
    return missing_items

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.before_request
def create_tables_once():
    if not hasattr(app, 'tables_created'):
        db.create_all()
        app.tables_created = True

@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = verify_user(email, password)
        if user:
            session.permanent = True
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_name'] = user.name
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Passwords do not match', 'error')
        elif password and len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
        else:
            user = create_user(email, password, name)
            if user:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Email already exists', 'error')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('splash'))

@app.route('/home')
@login_required
def index():
    return render_template('index.html', user=session)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=session)

@app.route('/habits')
@login_required
def habits():
    return render_template('habits.html', user=session)

@app.route('/api/habits', methods=['GET'])
@login_required
def get_habits_api():
    habits = get_user_habits(session['user_id'])
    return jsonify(habits)

@app.route('/api/habits', methods=['POST'])
@login_required
def add_habit_api():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    add_habit(
        session['user_id'],
        data['item_name'],
        data['frequency'],
        data['time_of_day'],
        data['location'],
        data.get('priority', 1)
    )
    return jsonify({'status': 'success'})

@app.route('/api/habits/<item_name>', methods=['DELETE'])
@login_required
def delete_habit_api(item_name):
    delete_habit_db(session['user_id'], item_name)
    return jsonify({'status': 'deleted'})

@app.route('/api/detect', methods=['POST'])
@login_required
def detect_items():
    try:
        if 'image' not in request.files and 'image' not in request.form:
            return jsonify({'error': 'No image provided'}), 400
        if 'image' in request.files:
            file = request.files['image']
            image_data = file.read()
        else:
            image_data = request.form['image']
        detections = detect_objects_in_image(image_data, session['user_id'])
        missing_items = find_missing_items(detections, session['user_id'])
        return jsonify({
            'detections': detections,
            'missing_items': missing_items
        })
    except Exception as e:
        print(f"Detection error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/start_detection', methods=['POST'])
@login_required
def start_detection():
    return jsonify({'status': 'started'})

@app.route('/api/stop_detection', methods=['POST'])
@login_required
def stop_detection():
    return jsonify({'status': 'stopped'})

if __name__ == '__main__':
    # Only needed for first run or after DB reset
    with app.app_context():
        db.create_all()
    print("🧠 Quantix Memory AI - User Authentication Version")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🚀 Quantix Memory AI is ready! Register a new account to get started.")
    print("🎨 Beautiful splash page and login system active!")
    app.run(host='0.0.0.0', port=5000)
