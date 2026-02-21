from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import joblib
import pandas as pd

# 1. Initialize the app and load the model at startup
app = FastAPI(title="Wine Quality Prediction API")
model_pipeline = joblib.load('wine_quality_pipeline.pkl')

# 2. Configure API Key Authentication
API_KEY = "super-secret-key-123" # In production, this goes in a .env file
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(status_code=403, detail="Could not validate credentials")

# 3. Define the expected JSON input (matches the wine dataset features)
class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

# 4. Create the Prediction Endpoint
@app.post("/predict", dependencies=[Depends(get_api_key)])
def predict_quality(features: WineFeatures):
    # Convert incoming JSON into a format the model understands (Pandas DataFrame)
    # The dictionary keys must perfectly match the columns the model was trained on
    input_data = pd.DataFrame([{
        "fixed acidity": features.fixed_acidity,
        "volatile acidity": features.volatile_acidity,
        "citric acid": features.citric_acid,
        "residual sugar": features.residual_sugar,
        "chlorides": features.chlorides,
        "free sulfur dioxide": features.free_sulfur_dioxide,
        "total sulfur dioxide": features.total_sulfur_dioxide,
        "density": features.density,
        "pH": features.pH,
        "sulphates": features.sulphates,
        "alcohol": features.alcohol
    }])

    # The model was trained with column names like "fixed acidity" (with space).
    # But our API uses "fixed_acidity" (with underscore).
    # We must swap "_" for " " so the model recognizes the columns.
    input_data.columns = input_data.columns.str.replace('_', ' ')   
    print(input_data.columns)

    # Predict using the loaded pipeline (scales and predicts automatically)
    prediction = model_pipeline.predict(input_data)
    
    # Return the result
    result = "Good Quality" if prediction[0] == 1 else "Bad Quality"
    
    return {
        "prediction": int(prediction[0]),
        "interpretation": result
    }

@app.get("/")
def home():
    return {"message": "Welcome to the Wine Quality Prediction API"}