# Red Wine Quality Classification API

## Overview

This repository contains an end-to-end machine learning deployment project that predicts the quality of red wine based on its physicochemical properties. The project involves a predictive Random Forest model trained on the Cortez et al. (2009) [Red Wine Quality dataset from Kaggle](https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009), a robust Scikit-Learn preprocessing pipeline, and a highly scalable REST API built with FastAPI.

The application is containerized using Docker and deployed on Google Cloud Run.

## Live API Endpoint

**Base URL:** https://wine-api-service-264324203120.us-central1.run.app

**Prediction URL:** https://wine-api-service-264324203120.us-central1.run.app)/predict

**Interactive Docs (Swagger UI):** [Click here to test the API](https://wine-api-service-264324203120.us-central1.run.app/docs)

**API Key:** `super-secret-key-123`

**Method:** `POST`



## Repository Structure

* `wine_quality_train_model.ipynb`: The original Jupyter Notebook containing the Exploratory Data Analysis (EDA), model training (SVM vs. Random Forest), and evaluation.
* `wine_quality_pipeline.pkl`: The serialized Scikit-Learn pipeline containing the fitted `StandardScaler` and the chosen `RandomForestClassifier`.
* `main.py`: The FastAPI application code that loads the model, validates incoming JSON data using Pydantic, and serves predictions.
* `Dockerfile`: The configuration file used to build the isolated Python 3.9 container for the application.
* `requirements.txt`: The specific Python dependencies required to run the API.

## Local Setup & Development

### 1. Standard Python Environment

To run the API directly on your local machine without Docker:

```bash
# Clone the repository and navigate into it
git clone https://github.com/omotoyosi-odele/wine-quality-deployment.git
cd wine-quality-deployment

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn main:app --reload --port 8080

```

Once running, you can access the interactive API documentation and test the endpoint directly in your browser at: `http://localhost:8080/docs`

### 2. Docker Container Setup

To build and run the application using Docker:

```bash
# Build the Docker image
docker build --platform -t wine-api .

# Run the container locally
docker run -p 8080:8080 wine-api

```

## Testing the API

You can test the deployed API using `curl`. Ensure you replace `[[YOUR_CLOUD_RUN_URL](https://wine-api-service-264324203120.us-central1.run.app/)]` with the actual deployed URL (or `http://localhost:8080` if testing locally).

```bash
curl -X 'POST' \
  'https://wine-api-service-264324203120.us-central1.run.app/predict' \
  -H 'accept: application/json' \
  -H 'X-API-Key: super-secret-key-123' \
  -H 'Content-Type: application/json' \
  -d '{
  "fixed_acidity": 7.4,
  "volatile_acidity": 0.7,
  "citric_acid": 0.0,
  "residual_sugar": 1.9,
  "chlorides": 0.076,
  "free_sulfur_dioxide": 11.0,
  "total_sulfur_dioxide": 34.0,
  "density": 0.9978,
  "pH": 3.51,
  "sulphates": 0.56,
  "alcohol": 9.4
}'

```

**Expected Response:**

```json
{
  "prediction": 0,
  "interpretation": "Bad Quality"
}

```

## Deployment Architecture

This application follows a strict backend-only architecture:

1. **Client:** Sends a POST request with JSON payload and API Key.
2. **Google Cloud Run:** Serverless compute automatically routes the request and scales containers as needed.
3. **FastAPI (Docker):** Receives the request on port 8080, authenticates the key, maps the data schema, and passes it to the ML pipeline.
4. **Scikit-Learn Pipeline:** Scales the incoming numeric features and outputs a prediction using the pre-trained Random Forest model.

---
