FROM python:3.13-slim
LABEL authors="yumengliu"

# Create app directory
WORKDIR /app

# Install dependencies first for fast reload
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt


# Run app
COPY . /app
CMD ["uvicorn", "utils.app:app", "--host", "0.0.0.0", "--port", "8080"]
