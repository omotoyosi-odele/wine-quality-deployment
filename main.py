from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import joblib
import pandas as pd

# 1. Initialize the App
app = FastAPI(title="Wine Quality Prediction API")

# 2. Security Setup
API_KEY = "12345secret" 
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )

# 3. Load the Model
model = joblib.load('wine_model.joblib')

# 4. Define the Input Data Structure
class WineInput(BaseModel):
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

@app.post("/predict")
def predict_wine_quality(data: WineInput, api_key: str = Security(get_api_key)):
    
    # Convert the input data (JSON) into a format the model understands (DataFrame)
    # Note: We use model_dump() because dict() is sometimes deprecated
    input_df = pd.DataFrame([data.model_dump()])
    
    # --- THE FIX IS HERE ---
    # The model was trained with column names like "fixed acidity" (with space).
    # But our API uses "fixed_acidity" (with underscore).
    # We must swap "_" for " " so the model recognizes the columns.
    input_df.columns = input_df.columns.str.replace('_', ' ')
    
    # Ask the model for a prediction
    prediction = model.predict(input_df)
    
    # Return the result
    result = "Good Quality" if prediction[0] == 1 else "Bad Quality"
    
    return {
        "prediction": int(prediction[0]),
        "interpretation": result
    }

@app.get("/")
def home():
    return {"message": "Wine Quality API is running!"}