FROM python:3.6.12-buster

# Make a directory for app
WORKDIR /app

# Install dependencies
COPY requirements.txt .

# install talib

RUN pip install -r requirements.txt

# Copy Source Code
COPY /app .


# Run the application
CMD ["python", "main_loop.py"]
