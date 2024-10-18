# Pull official base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Create a user to run the application
RUN adduser --disabled-password myuser
USER myuser

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
