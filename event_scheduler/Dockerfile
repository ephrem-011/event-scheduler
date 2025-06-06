FROM python:3.11

WORKDIR /app

# Copy all your backend code into the container
COPY . .

# ✅ Now the file exists inside the container, so we can make it executable
RUN chmod +x wait-for-db.sh

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


