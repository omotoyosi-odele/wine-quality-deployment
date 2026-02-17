# 1. Start with a Python base image (The "Kitchen")
FROM python:3.9-slim

# 2. Set the working directory (The "Countertop")
WORKDIR /app

# 3. Copy requirements (The "Shopping List")
# We will create this file in a second!
COPY requirements.txt .

# 4. Install dependencies (The "Prep Work")
# --no-cache-dir keeps the image small
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the code (The "Ingredients")
COPY . .

# 6. Expose the port (The "Service Window")
EXPOSE 8080

# 7. Start the app (The "Open Sign")
# Note: We use port 8080 because Cloud Run expects it
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
