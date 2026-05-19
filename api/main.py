from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load saved model and scaler
model = joblib.load("models/random_forest_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# Create FastAPI app
app = FastAPI()

# Input schema
class TrafficData(BaseModel):
    features: list

# Home route
@app.get("/")
def home():
    return {"message": "Traffic AI Security API Running"}

# Prediction route
@app.post("/predict")
def predict(data: TrafficData):

    features = data.features

    input_data = np.array(features).reshape(1, -1)

    # Scale data
    scaled_data = scaler.transform(input_data)

    # ML Prediction
    prediction = model.predict(scaled_data)[0]

    # Probability
    probability = model.predict_proba(scaled_data)[0]

    attack_probability = float(max(probability) * 100)

    # Manual logic improvement
    if (
        features[0] > 5 and
        features[2] < 5 and
        features[3] < 3 and
        features[4] < 100
    ):
        result = "Normal"
        confidence = 92
    else:
        result = "Attack"
        confidence = round(attack_probability, 2)

    return {
        "prediction": result,
        "confidence": confidence
    }