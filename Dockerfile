# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run migrations and collect static files
# RUN python manage.py migrate

# Expose port 8000 to allow communication to/from server
EXPOSE 8000
RUN mkdir -p /code/static && python manage.py collectstatic --no-input
# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
