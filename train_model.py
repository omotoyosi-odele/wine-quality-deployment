import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib

# 1. Load the data
# Make sure the csv file is in the same folder as this script!
print("Loading data...")
data = pd.read_csv('winequality-red.csv')

# Separate features (X) and target (y)
# 'quality' is usually the target in this dataset
X = data.drop('quality', axis=1)

# We turn quality into a classification problem (good vs bad) for simplicity
# If quality > 6 it's "good" (1), else "bad" (0)
y = (data['quality'] > 6).astype(int)

# 2. Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Create the "Robot Arm" (Pipeline)
# The assignment requires robust preprocessing[cite: 18].
# This pipeline does two things automatically:
# Step A: Imputer - Fills in any missing numbers with the mean (just in case)
# Step B: Scaler - Standardizes the numbers (makes them easier for the model to understand)
# Step C: Model - The actual Random Forest Classifier
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])

# 4. Train the Pipeline
print("Training model...")
pipeline.fit(X_train, y_train)

# 5. Check accuracy (Optional, but good for your report)
accuracy = pipeline.score(X_test, y_test)
print(f"Model Training Complete! Accuracy: {accuracy:.2f}")

# 6. Save (Pickle) the "Brain"
# This creates the file we need for the next step [cite: 25]
joblib.dump(pipeline, 'wine_model.joblib')
print("Success! Model saved as 'wine_model.joblib'")