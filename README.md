# Spam Detector Image Generator

This project is a lightweight Flask app that classifies a message as spam or not spam and generates a shareable image with the result.

## Quick start

```bash
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` to use the app.

## How it works

The app checks the message against a short list of common spam keywords. It then generates a PNG image using Pillow so you can download the result.
