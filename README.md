# 🧠 Quantix Memory AI
![GitHub Repo Stars](https://img.shields.io/github/stars/Poorvika1-droid/Quantix-Memory?style=social)
![GitHub Forks](https://img.shields.io/github/forks/Poorvika1-droid/Quantix-Memory?style=social)
![Hackathon Submission](https://img.shields.io/badge/For%20The%20Love%20Of%20Code-Hackathon-blueviolet)

> ✨ A smart AI assistant that helps you avoid forgetting things! Quantix Memory simulates object tracking and memory reminders to enhance your everyday productivity.

---

## 🌐 Live Demo
🔗 [Click here to open Quantix Memory](https://quantix-memory-ai.onrender.com)

---

## 🖼 Website Preview

![Quantix Memory Screenshot](./assets/screenshot.png)

---

## 🧠 Key Features

- 🚀 Detects forgotten items using memory assistant logic
- 🔁 Simulates real-time feedback system
- 📱 Clean, responsive UI
- 🔒 Secure password hashing (Werkzeug)
- ☁ Hosted using Render for instant access

---

## 🛠 Built With

- Python (Flask, SQLAlchemy)
- HTML, CSS, JavaScript
- Render (Deployment)
- GitHub (Version Control)

---

## 🚀 Deploy on Render

1. **Fork/Clone this repo**
2. **Create a new Web Service on [Render](https://render.com/)**
3. **Set the following environment variables:**
   - `SECRET_KEY` (required, use a strong random value)
   - `DATABASE_URL` (recommended: use a Render Postgres instance)
4. **Build Command:** (leave blank or use `pip install -r requirements.txt`)
5. **Start Command:**
   ```
   gunicorn app_simple:app
   ```
6. **(Optional) Add a Postgres database on Render and set `DATABASE_URL`**

---

## ⚡ Local Development

```bash
git clone https://github.com/Poorvika1-droid/Quantix-Memory.git
cd Quantix-Memory
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables (optional, but recommended for production)
export SECRET_KEY='your-strong-secret-key'
export DATABASE_URL='sqlite:///local.db'  # Or your Postgres URL

python app_simple.py
```

App will be available at [http://localhost:5000](http://localhost:5000)

---

## 🔒 Security
- Passwords are securely hashed using Werkzeug (not plain SHA256).
- Always set a strong `SECRET_KEY` in production.
- For production, use Gunicorn (see Procfile) and a managed database (Postgres recommended).

---

## 📄 License
MIT
