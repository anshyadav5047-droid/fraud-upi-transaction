from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load the trained model
print("Loading trained model...")
try:
    model_data = joblib.load('upi_fraud_detection_model.pkl')
    model = model_data['model']
    label_encoder = model_data['label_encoder']
    feature_columns = model_data['feature_columns']
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Please run train_model.py first to generate the model file.")
    model = None

@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict fraud for a transaction"""
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please train the model first.'
        }), 500
    
    try:
        # Get data from request
        data = request.json
        
        # Extract features
        amount = float(data['amount'])
        oldbalanceOrg = float(data['oldbalanceOrg'])
        newbalanceOrig = float(data['newbalanceOrig'])
        oldbalanceDest = float(data['oldbalanceDest'])
        newbalanceDest = float(data['newbalanceDest'])
        
        # For prediction, we need to create all features
        # Use default values for missing features (step, type, hour)
        step = 1  # Default step
        transaction_type = 'TRANSFER'  # Default type
        hour = step % 24
        
        # Calculate derived features
        balance_change_orig = oldbalanceOrg - newbalanceOrig
        balance_change_dest = newbalanceDest - oldbalanceDest
        
        balance_ratio_orig = newbalanceOrig / oldbalanceOrg if oldbalanceOrg > 0 else 0
        amount_to_oldbalance_orig = amount / oldbalanceOrg if oldbalanceOrg > 0 else 0
        
        # Encode transaction type
        type_encoded = label_encoder.transform([transaction_type])[0]
        
        # Create feature array in the correct order
        features = np.array([[
            step,
            type_encoded,
            amount,
            oldbalanceOrg,
            newbalanceOrig,
            oldbalanceDest,
            newbalanceDest,
            hour,
            balance_change_orig,
            balance_change_dest,
            balance_ratio_orig,
            amount_to_oldbalance_orig
        ]])
        
        # Create DataFrame with correct column names
        feature_df = pd.DataFrame(features, columns=feature_columns)
        
        # Make prediction
        prediction = model.predict(feature_df)[0]
        probability = model.predict_proba(feature_df)[0]
        
        # Get fraud probability (probability of class 1)
        fraud_probability = probability[1] * 100
        
        # Determine classification
        classification = 'Fraudulent' if prediction == 1 else 'Legitimate'
        
        return jsonify({
            'classification': classification,
            'fraud_probability': round(fraud_probability, 2),
            'legitimate_probability': round(probability[0] * 100, 2)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("UPI FRAUD DETECTION SERVER")
    print("="*60)
    print("Server starting on http://127.0.0.1:8080")
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    app.run(debug=False, host='127.0.0.1', port=8080, use_reloader=False)
