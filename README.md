# Wine Quality Prediction API

This project is a Machine Learning deployment assignment that serves a Random Forest model via a REST API. The model predicts whether a red wine is of "Good" or "Bad" quality based on physicochemical properties.

The application is containerized using Docker and deployed on Google Cloud Run.

## Live Demo
**Base URL:** https://wine-api-service-264324203120.us-central1.run.app  
**Interactive Docs (Swagger UI):** [Click here to test the API](https://wine-api-service-264324203120.us-central1.run.app/docs)

---

## Project Structure
* `train_model.py`: Script to train the Random Forest model and save it as a `.joblib` file.
* `main.py`: The FastAPI application that loads the model and serves predictions.
* `Dockerfile`: Configuration for containerizing the application.
* `requirements.txt`: List of Python dependencies.
* `wine_model.joblib`: The pre-trained model artifact.

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/omotoyosi-odele/wine-quality-deployment.git](https://github.com/omotoyosi-odele/wine-quality-deployment.git)
cd wine-quality-deployment
