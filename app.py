from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model
model = pickle.load(open('model.pkl', 'rb'))

# Label encoding used during training
location_map = {
    'Chamkhar': 0,
    'Deothang': 1,
    'Haa': 2,
    'Kanglung': 3,
    'Mongar': 4,
    'Paro': 5,
    'Pemagatshel': 6,
    'Punakha': 7,
    'Tashiyangtse': 8,
    'simkotha': 9
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        location = request.form['location']
        year = float(request.form['year'])
        month = float(request.form['month'])
        tmax = float(request.form['tmax'])
        tmin = float(request.form['tmin'])
        rh = float(request.form['rh'])
        windspeed = float(request.form['windspeed'])

        # Convert location name to encoded integer
        if location not in location_map:
            return render_template('index.html', prediction_result=f"Error: Unknown location '{location}'")
        
        location_encoded = location_map[location]

        # Prepare features in correct order
        features = np.array([[location_encoded, year, month, tmax, tmin, rh, windspeed]])

        # Predict
        prediction = model.predict(features)
        predicted_rainfall = round(prediction[0], 2)

        return render_template('index.html', prediction_result=f"Predicted Rainfall: {predicted_rainfall} mm")

    except Exception as e:
        return render_template('index.html', prediction_result=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
