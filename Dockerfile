FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

RUN cd /app && pip install --upgrade pip && pip install -r requirements.txt

RUN cd /app && python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. finetune_service.proto

# Expose the port the app runs on
EXPOSE 50051

# Command to run the application
CMD ["python", "index.py"]