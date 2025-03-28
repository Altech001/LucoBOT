FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask

EXPOSE $PORT

# Command to run the application
CMD ["python", "main.py"]