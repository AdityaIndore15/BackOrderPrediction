# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8501 to allow communication to/from the container
EXPOSE 8501

# Command to run the Streamlit app
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]

