FROM python:3.12.3
WORKDIR meme_center
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Settings logging
ENV LEVEL="DEBUG"
ENV GURU="True"
ENV TRACEBACK="False"

# Application settings
ENV APP_HOST=${HOST}
ENV APP_PORT=${PORT}

# Settings logging
ENV LEVEL="INFO"
ENV GURU="True"
ENV TRACEBACK="True"

# File settings
ENV SIZE=1048576

# Settings for PostgresSQL database connections
ENV POSTGRES_DB="test_db"
ENV POSTGRES_USER="test_user"
ENV POSTGRES_PASSWORD="test_password"
ENV POSTGRES_HOST="127.0.0.1"
ENV POSTGRES_PORT="5432"
ENV POSTGRES_SCHEMA="meme_center"

ENV S3_HOST="127.0.0.1"
ENV S3_PORT=8005


# Building
RUN pip install --upgrade pip  --no-cache-dir
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY meme_center .

CMD python main.py