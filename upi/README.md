# FraudGuard - Smart Transaction Protection

AI-powered fraud detection system for UPI transactions using Machine Learning.

## Files Included

- `app.py` - Flask web server
- `requirements.txt` - Python dependencies
- `templates/` - Frontend HTML files
- `upi_fraud_detection_model.pkl` - Trained ML model

## Setup Instructions

### 1. Install Python
Download and install Python 3.8 or higher from https://python.org

### 2. Copy Project Files
Copy these files/folders to your computer:
- app.py
- requirements.txt
- templates/ (entire folder)
- upi_fraud_detection_model.pkl

**DO NOT copy** the .venv folder (if exists)

### 3. Install Dependencies

Open terminal/command prompt in project folder and run:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 4. Run the Application

```powershell
python app.py
```

### 5. Access the Application

Open browser and go to: http://127.0.0.1:8080

## Features

- Real-time fraud detection
- 98.8% accuracy rate
- Quick test examples
- Analysis history
- Clean, modern interface

## Model Performance

- Training Accuracy: 99.20%
- Test Accuracy: 98.81%
- Training Samples: 8,000
- Response Time: <1 second

## Troubleshooting

**If model loading fails:**
- Ensure `upi_fraud_detection_model.pkl` is in the same folder as `app.py`

**If port 8080 is in use:**
- Edit `app.py` line 110 and change `port=8080` to another port like `port=5000`

**If dependencies fail to install:**
- Update pip: `python -m pip install --upgrade pip`
- Try installing individually: `pip install pandas numpy scikit-learn joblib flask`

## Stopping the Server

Press `Ctrl+C` in the terminal to stop the server.
