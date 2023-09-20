# Use the official Python image as the base image
FROM python:3.6-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the working directory
COPY . .

# Expose the port your application will run on
EXPOSE 4000

ENV FLASK_APP=app

# Define the command to run your application
# CMD ["python", "app.py"]

CMD [ "flask", "run", "--host=0.0.0.0", "--port=4000"]
