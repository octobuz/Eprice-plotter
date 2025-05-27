# Step 1: Use an official Python base image
FROM python:3.8-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements.txt into the container
COPY requirements.txt .

# Step 4: Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your application code into the container
COPY . .

# Step 6: Set the command to run your application
CMD ["python", "main.py"]
