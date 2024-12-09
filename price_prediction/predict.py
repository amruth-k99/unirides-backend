from flask import Flask, request, jsonify
import joblib
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Load the trained model
model = joblib.load('/home/ubuntu/price_prediction/lr_grid.pkl')

@app.route('/')
def home():
    return "Welcome to the Machine Learning API!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input data as JSON
        data = request.json  # Data should be sent as JSON
        features = data.get('features', [])
        
        if not features:
            return jsonify({'error': 'No input features provided'}), 400
        
        # Convert input to numpy array (ensure 2D array)
        input_data = np.array(features).reshape(1, -1)  # Assuming 1 row of data
        
        # Make prediction using the model
        prediction = model.predict(input_data)
        
        # Return the prediction as JSON response
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

