FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the APP_URL environment variable
ENV APP_URL=https://basorai-ffhwd5dzgqe7b7dm.southeastasia-01.azurewebsites.net/

# Run the startup script instead of directly running basor_AI.py
CMD ["python", "startup.py"]